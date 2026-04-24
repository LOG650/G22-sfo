#!/usr/bin/env python3
"""
ACT-3.4.3/4 LP-modell for hylleallokering — tre scenarier.

Modellen (felles formulering):
  max Σ y_i
  s.t.
       Σ x_i = T
       y_i ≤ ρ_i · x_i
       y_i ≤ d_i
       x_i ≥ x_min_i
       x_i ∈ ℤ≥0, y_i ∈ ℝ≥0

Scenarier:
  S1  Baseline      — x_min = 1 enhet/produkt, d = 2·mean (for underkap.)
  S2  Realistisk    — x_min = 25% av nåværende allokering, d = 2·mean
  S3  Konservativ   — x_min = 50% av nåværende allokering, d = 1.5·mean

Kjøring:
  cd "006 analysis"
  uv run python aktiviteter/3_4_data_metode_og_modellering/scripts/03_lp_modell.py
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
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
# SCENARIODEFINISJON
# =====================================================================
@dataclass
class Scenario:
    key: str
    name: str
    description: str
    x_min_fraction: float       # andel av opprinnelig facings som minimum
    x_min_floor: int            # absolutt minimum (aldri lavere enn dette)
    overserve_factor: float     # etterspørselsmultiplikator for underkap. produkter


SCENARIOS = [
    Scenario(
        key="S1_baseline",
        name="S1 Baseline",
        description=("Minimum 1 facing per produkt, etterspørsel for underkapasiterte "
                     "antas 2× mean."),
        x_min_fraction=0.0,
        x_min_floor=1,
        overserve_factor=2.0,
    ),
    Scenario(
        key="S2_realistisk",
        name="S2 Realistisk",
        description=("Minimum 25% av dagens allokering, etterspørsel for "
                     "underkapasiterte antas 2× mean. Hovedanbefaling."),
        x_min_fraction=0.25,
        x_min_floor=1,
        overserve_factor=2.0,
    ),
    Scenario(
        key="S3_konservativ",
        name="S3 Konservativ",
        description=("Minimum 50% av dagens allokering, etterspørsel for "
                     "underkapasiterte antas 1.5× mean."),
        x_min_fraction=0.50,
        x_min_floor=1,
        overserve_factor=1.5,
    ),
]


# =====================================================================
# MODELLBYGGING
# =====================================================================
def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("Produkt").agg(
        mean_sales=("Ant_solgt", "mean"),
        max_sales=("Ant_solgt", "max"),
        facings=("Kapasitet", "first"),
    )
    g["productivity"] = g["mean_sales"] / g["facings"]
    g["utilization"] = g["mean_sales"] / g["facings"]
    return g


def compute_demand_cap(stats: pd.DataFrame, overserve_factor: float) -> pd.Series:
    d = stats["mean_sales"].copy()
    overserved = stats["utilization"] >= 1.0
    d[overserved] = stats.loc[overserved, "mean_sales"] * overserve_factor
    return d


def compute_x_min(stats: pd.DataFrame, scenario: Scenario) -> pd.Series:
    """Minimum facings per produkt iht. scenario."""
    floor = pd.Series(scenario.x_min_floor, index=stats.index)
    frac = (stats["facings"] * scenario.x_min_fraction).apply(math.floor)
    return pd.concat([floor, frac], axis=1).max(axis=1).astype(int)


def solve_lp(stats: pd.DataFrame, demand: pd.Series, x_min: pd.Series,
             *, total_capacity: int) -> dict:
    prods = list(stats.index)

    model = pulp.LpProblem("hylleallokering", pulp.LpMaximize)

    x = {p: pulp.LpVariable(f"x_{p}", lowBound=int(x_min[p]), cat="Integer")
         for p in prods}
    y = {p: pulp.LpVariable(f"y_{p}", lowBound=0) for p in prods}

    model += pulp.lpSum(y[p] for p in prods)
    model += pulp.lpSum(x[p] for p in prods) == total_capacity
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
            "facings_min": x_min.astype(int),
            "facings_optimal": [int(round(x[p].value())) for p in prods],
            "sales_original": stats["mean_sales"].round(1),
            "sales_optimal": [round(y[p].value(), 1) for p in prods],
            "demand_cap": demand.round(1),
            "productivity": stats["productivity"].round(3),
        }, index=prods),
    }


def format_per_product_table(res: pd.DataFrame) -> pd.DataFrame:
    out = res.copy()
    out["delta_facings"] = out["facings_optimal"] - out["facings_original"]
    out["delta_sales"] = (out["sales_optimal"] - out["sales_original"]).round(1)
    out["sales_gain_pct"] = (
        out["delta_sales"] / out["sales_original"] * 100
    ).round(1)
    return out[[
        "facings_original", "facings_min", "facings_optimal", "delta_facings",
        "sales_original", "sales_optimal", "delta_sales", "sales_gain_pct",
        "demand_cap", "productivity",
    ]]


# =====================================================================
# VISUELL OUTPUT
# =====================================================================
def plot_allocation_compare(table: pd.DataFrame, path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    x_pos = range(len(table))
    width = 0.4
    ax.bar([p - width / 2 for p in x_pos], table["facings_original"],
           width=width, label="Nåværende", color="#9DB4C0")
    ax.bar([p + width / 2 for p in x_pos], table["facings_optimal"],
           width=width, label="LP-optimal", color="#E63946")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(table.index, rotation=30, ha="right")
    ax.set_ylabel("Antall frontfacings")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_sales_compare(table: pd.DataFrame, path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    x_pos = range(len(table))
    width = 0.4
    ax.bar([p - width / 2 for p in x_pos], table["sales_original"],
           width=width, label="Observert", color="#9DB4C0")
    ax.bar([p + width / 2 for p in x_pos], table["sales_optimal"],
           width=width, label="Modellert (LP)", color="#2E86AB")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(table.index, rotation=30, ha="right")
    ax.set_ylabel("Forventet ukesalg (enheter)")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_scenario_compare(results: dict[str, pd.DataFrame], path: Path) -> None:
    """Sammenlign facings-allokering på tvers av scenarier."""
    # Alle tabeller har samme produkt-indeks
    first_key = next(iter(results))
    products = list(results[first_key].index)

    fig, ax = plt.subplots(figsize=(12, 7))
    n_scen = len(results)
    n_prod = len(products)
    width = 0.8 / (n_scen + 1)

    positions = range(n_prod)
    baseline_original = results[first_key]["facings_original"]
    ax.bar([p - width * (n_scen / 2) for p in positions], baseline_original,
           width=width, label="Nåværende", color="#9DB4C0")

    palette = ["#E63946", "#2E86AB", "#F4A261"]
    for idx, (scen_key, table) in enumerate(results.items()):
        offset = width * (idx - n_scen / 2 + 1)
        ax.bar([p + offset for p in positions], table["facings_optimal"],
               width=width, label=scen_key, color=palette[idx % len(palette)])

    ax.set_xticks(positions)
    ax.set_xticklabels(products, rotation=30, ha="right")
    ax.set_ylabel("Antall frontfacings")
    ax.set_title("Hylleallokering per produkt — nåværende vs. tre LP-scenarier")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# RAPPORT
# =====================================================================
def scenario_report(scenario: Scenario, table: pd.DataFrame, status: str,
                    objective: float, baseline_total: float, total_capacity: int,
                    anonymized: bool) -> str:
    lines: list[str] = []
    tittel = f"{scenario.name}"
    tittel += " (anonymisert)" if anonymized else " (intern)"
    lines.append(f"# {tittel}")
    lines.append("")
    lines.append(f"*{scenario.description}*")
    lines.append("")
    lines.append(f"- Solver-status: **{status}**")
    lines.append(f"- Total hyllekapasitet: **{total_capacity}** frontfacings")
    lines.append(f"- Observert total ukesalg: **{baseline_total:.1f}** enheter")
    lines.append(f"- LP-optimal ukesalg: **{objective:.1f}** enheter")
    gain = objective - baseline_total
    pct = 100 * gain / baseline_total if baseline_total > 0 else 0
    lines.append(f"- Gevinst: **+{gain:.1f}** enheter/uke (**+{pct:.1f}%**)")
    lines.append("")
    lines.append("## Allokering per produkt")
    lines.append("")
    lines.append("| Produkt | Nå | Min | Ny | Δ | Salg nå | Salg ny | Δ | Gev % |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for prod, r in table.iterrows():
        delta_f = int(r["delta_facings"])
        lines.append(
            f"| {prod} | {int(r['facings_original'])} | {int(r['facings_min'])} | "
            f"{int(r['facings_optimal'])} | {delta_f:+d} | "
            f"{r['sales_original']:.1f} | {r['sales_optimal']:.1f} | "
            f"{r['delta_sales']:+.1f} | {r['sales_gain_pct']:+.1f}% |"
        )
    lines.append("")
    winners = table[table["delta_facings"] > 0].index.tolist()
    losers = table[table["delta_facings"] < 0].index.tolist()
    uendret = table[table["delta_facings"] == 0].index.tolist()
    lines.append(f"**Vinnere ({len(winners)}):** {', '.join(winners) or '—'}")
    lines.append("")
    lines.append(f"**Avgir plass ({len(losers)}):** {', '.join(losers) or '—'}")
    if uendret:
        lines.append("")
        lines.append(f"**Uendret:** {', '.join(uendret)}")
    return "\n".join(lines)


def scenario_summary(scenarios: list[Scenario],
                     objectives: dict[str, float],
                     baseline_total: float,
                     anonymized: bool) -> str:
    lines = []
    tittel = "LP-scenarier — oppsummering"
    tittel += " (anonymisert)" if anonymized else " (intern)"
    lines.append(f"# {tittel}")
    lines.append("")
    lines.append(f"Baseline observert total ukesalg: **{baseline_total:.1f}** enheter.")
    lines.append("")
    lines.append("| Scenario | Beskrivelse | LP-salg | Gevinst | Gev % |")
    lines.append("|---|---|---:|---:|---:|")
    for scen in scenarios:
        obj = objectives[scen.key]
        gain = obj - baseline_total
        pct = 100 * gain / baseline_total if baseline_total > 0 else 0
        lines.append(
            f"| {scen.name} | {scen.description} | {obj:.1f} | +{gain:.1f} | +{pct:.1f}% |"
        )
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append(
        "- **S1 (baseline)** viser det teoretiske maksimum under gitte parameter-"
        "antakelser. Allokeringen er kommersielt uspiselig: flere kjernekategorier "
        "reduseres til ett facing.")
    lines.append(
        "- **S2 (realistisk)** introduserer en minimums-allokering på 25% av "
        "nåværende hylleplass per produkt, som reflekterer at kjeden ikke fjerner "
        "listede SKUer over natten. Dette er hovedanbefalingen.")
    lines.append(
        "- **S3 (konservativ)** legger minimum på 50% av dagens allokering og bruker "
        "en mindre aggressiv etterspørselsantakelse (1.5× mean i stedet for 2.0×). "
        "Beste egnet når kjeden er risikoavers eller data er preget av out-of-stock.")
    return "\n".join(lines)


# =====================================================================
# MAIN
# =====================================================================
def write_outputs(key: str, scenario: Scenario, per_prod: pd.DataFrame,
                  per_prod_anon: pd.DataFrame, status: str, objective: float,
                  baseline_total: float, total_capacity: int) -> None:
    """Skriv intern + anonym output for ett scenario."""
    # Intern
    per_prod.to_csv(RESULT_INTERN / f"lp_allokering_{key}.csv")
    plot_allocation_compare(
        per_prod, FIG_INTERN / f"lp_allokering_{key}.png",
        title=f"{scenario.name} — allokering (intern)",
    )
    plot_sales_compare(
        per_prod, FIG_INTERN / f"lp_salg_{key}.png",
        title=f"{scenario.name} — forventet salg (intern)",
    )
    (RESULT_INTERN / f"lp-rapport_{key}.md").write_text(
        scenario_report(scenario, per_prod, status, objective,
                        baseline_total, total_capacity, anonymized=False),
        encoding="utf-8",
    )
    # Anonym
    per_prod_anon.to_csv(RESULT_DIR / f"lp_allokering_{key}.csv")
    plot_allocation_compare(
        per_prod_anon, FIG_DIR / f"lp_allokering_{key}.png",
        title=f"{scenario.name} — allokering",
    )
    plot_sales_compare(
        per_prod_anon, FIG_DIR / f"lp_salg_{key}.png",
        title=f"{scenario.name} — forventet salg",
    )
    (RESULT_DIR / f"lp-rapport_{key}.md").write_text(
        scenario_report(scenario, per_prod_anon, status, objective,
                        baseline_total, total_capacity, anonymized=True),
        encoding="utf-8",
    )


def main() -> None:
    for d in (FIG_DIR, FIG_INTERN, RESULT_DIR, RESULT_INTERN):
        d.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CLEAN_PARQUET)
    anon = Anonymizer.load(NAVNEREGISTER)

    stats = aggregate(df)
    total_capacity = int(stats["facings"].sum())
    baseline_total = stats["mean_sales"].sum()

    results_anon: dict[str, pd.DataFrame] = {}
    objectives: dict[str, float] = {}

    for scenario in SCENARIOS:
        demand = compute_demand_cap(stats, scenario.overserve_factor)
        x_min = compute_x_min(stats, scenario)
        result = solve_lp(stats, demand, x_min, total_capacity=total_capacity)
        per_prod = format_per_product_table(result["per_product"])

        # Anonymiser
        per_prod_anon = per_prod.copy()
        per_prod_anon.index = [anon.pseudo(p) for p in per_prod.index]
        per_prod_anon = per_prod_anon.sort_index()

        write_outputs(
            scenario.key, scenario, per_prod, per_prod_anon,
            result["status"], result["objective"], baseline_total, total_capacity,
        )

        results_anon[scenario.name] = per_prod_anon
        objectives[scenario.key] = result["objective"]

        gain_pct = 100 * (result["objective"] - baseline_total) / baseline_total
        print(f"{scenario.name:20} → salg {result['objective']:.1f} "
              f"({gain_pct:+.1f}% vs. baseline)")

    # Sammenligningsrapport + figur
    plot_scenario_compare(results_anon, FIG_DIR / "lp_scenario_compare.png")

    summary_anon = scenario_summary(SCENARIOS, objectives, baseline_total,
                                     anonymized=True)
    (RESULT_DIR / "lp-scenarier-oppsummering.md").write_text(summary_anon,
                                                              encoding="utf-8")

    summary_intern = scenario_summary(SCENARIOS, objectives, baseline_total,
                                       anonymized=False)
    (RESULT_INTERN / "lp-scenarier-oppsummering.md").write_text(summary_intern,
                                                                 encoding="utf-8")

    print(f"\nScenarie-sammenlikning: {FIG_DIR / 'lp_scenario_compare.png'}")
    print(f"Oppsummering: {RESULT_DIR / 'lp-scenarier-oppsummering.md'}")


if __name__ == "__main__":
    main()
