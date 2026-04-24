#!/usr/bin/env python3
"""
ACT-3.4.3/4 Formulering og implementering av LP-modell for hylleallokering.

Modellen:
  max Σ y_i                                    (total forventet salg/uke)
  s.t.
       Σ x_i = T                               (total hyllekapasitet)
       y_i ≤ ρ_i · x_i  ∀i                     (produktivitet per facing)
       y_i ≤ d_i       ∀i                      (etterspørselsgrense)
       x_i ≥ x_min      ∀i                     (sortimentsgaranti)
       x_i ∈ ℤ≥0,  y_i ∈ ℝ≥0

Produktivitet ρ_i = observert mean_sales_i / current_facings_i.
Etterspørselsgrense d_i = mean_sales_i        hvis utnyttelse < 1
                         = 2·mean_sales_i     hvis utnyttelse ≥ 1 (hovedscenario).

Kjøring:
  cd "006 analysis"
  uv run python aktiviteter/3_4_data_metode_og_modellering/scripts/03_lp_modell.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pulp

REPO_ROOT = Path(__file__).resolve().parents[4]
INTERN_DATA_DIR = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_3_casebeskrivelse_og_datainnsamling" / "resultat" / "intern"
)
CLEAN_PARQUET = INTERN_DATA_DIR / "salg_renset.parquet"
NAVNEREGISTER = INTERN_DATA_DIR / "navneregister.csv"
FIG_DIR = Path(__file__).resolve().parents[1] / "figurer"
FIG_INTERN = FIG_DIR / "intern"
RESULT_DIR = Path(__file__).resolve().parents[1] / "resultat"
RESULT_INTERN = RESULT_DIR / "intern"

sys.path.insert(0, str(REPO_ROOT / "006 analysis"))
from anonymisering import Anonymizer  # noqa: E402

plt.rcParams.update({
    "figure.figsize": (10, 6),
    "figure.dpi": 110,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 10,
})


# =====================================================================
# MODELLBYGGING
# =====================================================================
def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """Aggreger rådata til én rad per produkt med mean_sales, max_sales og facings."""
    g = df.groupby("Produkt").agg(
        mean_sales=("Ant_solgt", "mean"),
        max_sales=("Ant_solgt", "max"),
        facings=("Kapasitet", "first"),
    )
    g["productivity"] = g["mean_sales"] / g["facings"]
    g["utilization"] = g["mean_sales"] / g["facings"]  # samme, men navngitt tydelig
    return g


def compute_demand_cap(stats: pd.DataFrame, overserve_factor: float = 2.0) -> pd.Series:
    """Estimér etterspørselsgrense d_i."""
    d = stats["mean_sales"].copy()
    overserved = stats["utilization"] >= 1.0
    d[overserved] = stats.loc[overserved, "mean_sales"] * overserve_factor
    return d


def solve_lp(stats: pd.DataFrame, demand: pd.Series, *, total_capacity: int,
             x_min: int = 1) -> dict:
    """Bygg og løs LP. Returner resultater per produkt + global info."""
    prods = list(stats.index)

    model = pulp.LpProblem("hylleallokering", pulp.LpMaximize)

    x = {p: pulp.LpVariable(f"x_{p}", lowBound=x_min, cat="Integer") for p in prods}
    y = {p: pulp.LpVariable(f"y_{p}", lowBound=0) for p in prods}

    # Målfunksjon: total forventet salg
    model += pulp.lpSum(y[p] for p in prods)

    # R1: Total hyllekapasitet
    model += pulp.lpSum(x[p] for p in prods) == total_capacity

    # R2+R3: Produktivitet og etterspørsel
    for p in prods:
        rho = stats.loc[p, "productivity"]
        model += y[p] <= rho * x[p], f"prod_cap_{p}"
        model += y[p] <= demand[p], f"demand_cap_{p}"

    solver = pulp.PULP_CBC_CMD(msg=False)
    status = model.solve(solver)

    return {
        "status": pulp.LpStatus[status],
        "objective": pulp.value(model.objective),
        "per_product": pd.DataFrame({
            "facings_original": stats["facings"].astype(int),
            "facings_optimal": [int(round(x[p].value())) for p in prods],
            "sales_original": stats["mean_sales"].round(1),
            "sales_optimal": [round(y[p].value(), 1) for p in prods],
            "demand_cap": demand.round(1),
            "productivity": stats["productivity"].round(3),
        }, index=prods),
    }


def format_per_product_table(res: pd.DataFrame) -> pd.DataFrame:
    """Legg til delta-kolonner for lesbarhet."""
    out = res.copy()
    out["delta_facings"] = out["facings_optimal"] - out["facings_original"]
    out["delta_sales"] = (out["sales_optimal"] - out["sales_original"]).round(1)
    out["sales_gain_pct"] = (
        out["delta_sales"] / out["sales_original"] * 100
    ).round(1)
    return out[[
        "facings_original", "facings_optimal", "delta_facings",
        "sales_original", "sales_optimal", "delta_sales", "sales_gain_pct",
        "demand_cap", "productivity",
    ]]


# =====================================================================
# VISUELL OUTPUT
# =====================================================================
def plot_allocation_compare(table: pd.DataFrame, path: Path) -> None:
    """Side-ved-side: facings før vs. etter."""
    fig, ax = plt.subplots(figsize=(10, 6))
    x_pos = range(len(table))
    width = 0.4
    ax.bar([p - width/2 for p in x_pos], table["facings_original"],
           width=width, label="Nåværende", color="#9DB4C0")
    ax.bar([p + width/2 for p in x_pos], table["facings_optimal"],
           width=width, label="LP-optimal", color="#E63946")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(table.index, rotation=30, ha="right")
    ax.set_ylabel("Antall frontfacings")
    ax.set_title("Hylleallokering per produkt — nåværende vs. LP-optimal")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_sales_compare(table: pd.DataFrame, path: Path) -> None:
    """Sammenligning av forventet salg per uke."""
    fig, ax = plt.subplots(figsize=(10, 6))
    x_pos = range(len(table))
    width = 0.4
    ax.bar([p - width/2 for p in x_pos], table["sales_original"],
           width=width, label="Observert", color="#9DB4C0")
    ax.bar([p + width/2 for p in x_pos], table["sales_optimal"],
           width=width, label="Modellert (LP)", color="#2E86AB")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(table.index, rotation=30, ha="right")
    ax.set_ylabel("Forventet ukesalg (enheter)")
    ax.set_title("Forventet salg per produkt — observert vs. LP-optimal")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# RAPPORT
# =====================================================================
def generate_report(table: pd.DataFrame, status: str, objective: float,
                    baseline_total: float, total_capacity: int,
                    anonymized: bool) -> str:
    lines: list[str] = []
    tittel = "LP-modell: hylleallokering"
    tittel += " (anonymisert)" if anonymized else " (intern)"
    lines.append(f"# {tittel}")
    lines.append("")
    lines.append(f"- Solver-status: **{status}**")
    lines.append(f"- Total hyllekapasitet: **{total_capacity}** frontfacings")
    lines.append(f"- Observert total ukesalg (baseline): **{baseline_total:.1f}** enheter")
    lines.append(f"- LP-optimalt total ukesalg: **{objective:.1f}** enheter")
    gain = objective - baseline_total
    pct = 100 * gain / baseline_total if baseline_total > 0 else 0
    lines.append(f"- Gevinst: **+{gain:.1f}** enheter/uke (**+{pct:.1f}%**)")
    lines.append("")

    lines.append("## Allokering per produkt")
    lines.append("")
    lines.append("| Produkt | Facings nå | Facings ny | Δ | Salg nå | Salg ny | Δ | Gev % |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for prod, r in table.iterrows():
        delta_f = int(r["delta_facings"])
        delta_s = r["delta_sales"]
        lines.append(
            f"| {prod} | {int(r['facings_original'])} | {int(r['facings_optimal'])} | "
            f"{delta_f:+d} | {r['sales_original']:.1f} | {r['sales_optimal']:.1f} | "
            f"{delta_s:+.1f} | {r['sales_gain_pct']:+.1f}% |"
        )
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    winners = table[table["delta_facings"] > 0].index.tolist()
    losers = table[table["delta_facings"] < 0].index.tolist()
    uendret = table[table["delta_facings"] == 0].index.tolist()
    lines.append(f"- **Produkter som får mer plass ({len(winners)}):** {', '.join(winners)}")
    lines.append(f"- **Produkter som gir fra seg plass ({len(losers)}):** {', '.join(losers)}")
    if uendret:
        lines.append(f"- **Uendret:** {', '.join(uendret)}")
    lines.append("")
    lines.append("Gevinsten skyldes i hovedsak reallokering fra overkapasiterte "
                 "produkter til underkapasiterte, innenfor rammen av estimert "
                 "etterspørsel per produkt.")
    return "\n".join(lines)


# =====================================================================
# MAIN
# =====================================================================
def main() -> None:
    for d in (FIG_DIR, FIG_INTERN, RESULT_DIR, RESULT_INTERN):
        d.mkdir(parents=True, exist_ok=True)

    # Last renset data (med ekte navn)
    df = pd.read_parquet(CLEAN_PARQUET)
    anon = Anonymizer.load(NAVNEREGISTER)

    # Aggregér + beregn parameters (på ekte navn)
    stats = aggregate(df)
    demand = compute_demand_cap(stats, overserve_factor=2.0)
    total_capacity = int(stats["facings"].sum())
    print(f"Total hyllekapasitet: {total_capacity}")
    print(f"Antall produkter: {len(stats)}")

    # Løs LP
    result = solve_lp(stats, demand, total_capacity=total_capacity, x_min=1)
    print(f"Solver-status: {result['status']}")
    print(f"Optimal verdi (sum y): {result['objective']:.1f}")
    baseline_total = stats["mean_sales"].sum()
    print(f"Baseline total: {baseline_total:.1f}")

    per_prod = format_per_product_table(result["per_product"])

    # Intern output (ekte navn)
    per_prod.to_csv(RESULT_INTERN / "lp_allokering.csv")
    plot_allocation_compare(per_prod, FIG_INTERN / "lp_allokering_compare.png")
    plot_sales_compare(per_prod, FIG_INTERN / "lp_salg_compare.png")
    (RESULT_INTERN / "lp-rapport.md").write_text(
        generate_report(per_prod, result["status"], result["objective"],
                        baseline_total, total_capacity, anonymized=False),
        encoding="utf-8",
    )
    print(f"Intern skrevet: {RESULT_INTERN}/")

    # Anonymisert output
    per_prod_anon = per_prod.copy()
    per_prod_anon.index = [anon.pseudo(p) for p in per_prod.index]
    per_prod_anon = per_prod_anon.sort_index()
    per_prod_anon.to_csv(RESULT_DIR / "lp_allokering.csv")
    plot_allocation_compare(per_prod_anon, FIG_DIR / "lp_allokering_compare.png")
    plot_sales_compare(per_prod_anon, FIG_DIR / "lp_salg_compare.png")
    (RESULT_DIR / "lp-rapport.md").write_text(
        generate_report(per_prod_anon, result["status"], result["objective"],
                        baseline_total, total_capacity, anonymized=True),
        encoding="utf-8",
    )
    print(f"Anonymisert: {RESULT_DIR}/")


if __name__ == "__main__":
    main()
