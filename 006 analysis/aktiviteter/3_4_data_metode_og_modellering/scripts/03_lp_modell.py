#!/usr/bin/env python3
"""
ACT-3.4.3/4 LP-modell for hylleallokering med margin og sekundæreksponering.

Modellen:
  max Σ m_i · y_i                              (total forventet brutto margin/uke)
  s.t.
       Σ x_i = T                               (primær hyllekapasitet)
       Σ s_i ≤ S_MAX                           (sekundær plassbudsjett)
       y_i ≤ ρ_i · (x_i + k · s_i)            (produktivitet primær + sekundær)
       y_i ≤ d_i                              (etterspørselsgrense)
       x_i ≥ X_MIN, s_i ≥ 0                   (sortimentsgulv)
       x_i, s_i ∈ ℤ≥0, y_i ∈ ℝ≥0

Parameterforklaringer:
  m_i  = marginprosent (bransjetypisk 30-60 %), fra margin_mapping
  ρ_i  = produktivitet per primær-facing (mean_sales / facings_current)
  d_i  = etterspørselstak (2× mean for underkapasiterte)
  k    = sekundær-effektivitet relativt til primær (default 1.5)
  S_MAX = maksimalt antall sekundærplasser totalt i kategorien (default 3)
  X_MIN = minimum facings per SKU (default 3 = 1 kolli)

Tre scenarier:
  S1 Primær-omfordeling       — kun primær, uten sekundær (s_i = 0)
  S2 Primær + sekundær         — hovedanbefaling, begge handlingsrom brukes
  S3 Konservativ               — strammere gulv, 1.5× etterspørselstak, uten sekundær
"""

from __future__ import annotations

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
from margin_mapping import margin_for_product, brand_for_product  # noqa: E402

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
    x_min: int
    overserve_factor: float
    secondary_budget: int         # antall tilgjengelige sekundærplasser
    secondary_effectiveness: float  # k: sekundær salg/enhet / primær salg/enhet


SCENARIOS = [
    Scenario(
        key="S1_primaer",
        name="S1 Primær-omfordeling",
        description=("Reallokering kun innen primær hylle, x_min = 3 facings "
                     "(1 kolli), 2× etterspørsel, ingen sekundæreksponering."),
        x_min=3,
        overserve_factor=2.0,
        secondary_budget=0,
        secondary_effectiveness=0.0,
    ),
    Scenario(
        key="S2_primaer_sek",
        name="S2 Primær + sekundær",
        description=("Hovedanbefaling: primær-omfordeling pluss 3 sekundærplasser "
                     "som tildeles mest effektive SKUer. k = 1.5× primær-effektivitet."),
        x_min=3,
        overserve_factor=2.0,
        secondary_budget=3,
        secondary_effectiveness=1.5,
    ),
    Scenario(
        key="S3_konservativ",
        name="S3 Konservativ",
        description=("Konservativ: x_min = 50% av dagens allokering (ned til 3), "
                     "1.5× etterspørsel, ingen sekundæreksponering."),
        x_min=3,                    # floor i tillegg til fraction
        overserve_factor=1.5,
        secondary_budget=0,
        secondary_effectiveness=0.0,
    ),
]


# =====================================================================
# MODELLBYGGING
# =====================================================================
def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("Produkt").agg(
        mean_sales=("Ant_solgt", "mean"),
        facings=("Kapasitet", "first"),
    )
    g["productivity"] = g["mean_sales"] / g["facings"]
    g["utilization"] = g["mean_sales"] / g["facings"]
    g["margin"] = [margin_for_product(p) for p in g.index]
    g["brand"] = [brand_for_product(p) for p in g.index]
    return g


def compute_demand_cap(stats: pd.DataFrame, overserve_factor: float) -> pd.Series:
    d = stats["mean_sales"].copy()
    over = stats["utilization"] >= 1.0
    d[over] = stats.loc[over, "mean_sales"] * overserve_factor
    return d


def compute_x_min(stats: pd.DataFrame, scenario: Scenario) -> pd.Series:
    """Minimum facings per SKU. For S3 også 50% av dagens i tillegg til floor."""
    floor = pd.Series(scenario.x_min, index=stats.index)
    if scenario.key == "S3_konservativ":
        frac = (stats["facings"] * 0.5).apply(lambda v: int(v))
        return pd.concat([floor, frac], axis=1).max(axis=1).astype(int)
    return floor.astype(int)


def solve(stats: pd.DataFrame, demand: pd.Series, x_min: pd.Series,
          scenario: Scenario, total_capacity: int) -> dict:
    prods = list(stats.index)
    m = pulp.LpProblem(scenario.key, pulp.LpMaximize)

    x = {p: pulp.LpVariable(f"x_{p}", lowBound=int(x_min[p]), cat="Integer")
         for p in prods}
    y = {p: pulp.LpVariable(f"y_{p}", lowBound=0) for p in prods}
    s = {p: pulp.LpVariable(f"s_{p}", lowBound=0, cat="Integer") for p in prods}

    # Målfunksjon: margin-vektet salg
    m += pulp.lpSum(stats.loc[p, "margin"] * y[p] for p in prods)

    # Primær total kapasitet
    m += pulp.lpSum(x[p] for p in prods) == total_capacity, "primaer_kap"

    # Sekundær budsjett
    m += pulp.lpSum(s[p] for p in prods) <= scenario.secondary_budget, "sekundaer_kap"

    # Produktivitet + etterspørsel
    k = scenario.secondary_effectiveness
    for p in prods:
        rho = stats.loc[p, "productivity"]
        m += y[p] <= rho * (x[p] + k * s[p]), f"prod_cap_{p}"
        m += y[p] <= demand[p], f"demand_cap_{p}"

    m.solve(pulp.PULP_CBC_CMD(msg=False))

    return {
        "status": pulp.LpStatus[m.status],
        "objective": pulp.value(m.objective),
        "per_product": pd.DataFrame({
            "facings_original": stats["facings"].astype(int),
            "facings_min": x_min.astype(int),
            "facings_optimal": [int(round(x[p].value())) for p in prods],
            "secondary_optimal": [int(round(s[p].value())) for p in prods],
            "sales_original": stats["mean_sales"].round(1),
            "sales_optimal": [round(y[p].value(), 1) for p in prods],
            "demand_cap": demand.round(1),
            "productivity": stats["productivity"].round(3),
            "margin": stats["margin"],
            "brand": stats["brand"],
        }, index=prods),
    }


def format_per_product_table(res: pd.DataFrame) -> pd.DataFrame:
    out = res.copy()
    out["delta_facings"] = out["facings_optimal"] - out["facings_original"]
    out["delta_sales"] = (out["sales_optimal"] - out["sales_original"]).round(1)
    out["sales_gain_pct"] = (
        out["delta_sales"] / out["sales_original"] * 100
    ).round(1)
    out["margin_nok_ish"] = (out["sales_optimal"] * out["margin"]).round(2)
    return out[[
        "facings_original", "facings_min", "facings_optimal", "delta_facings",
        "secondary_optimal",
        "sales_original", "sales_optimal", "delta_sales", "sales_gain_pct",
        "demand_cap", "productivity", "margin", "brand",
    ]]


# =====================================================================
# RAPPORT
# =====================================================================
def margin_weighted_sum(sales: pd.Series, margin: pd.Series) -> float:
    return float((sales * margin).sum())


def scenario_report(scenario: Scenario, table: pd.DataFrame, status: str,
                    objective: float, baseline_margin: float,
                    baseline_sales: float, total_capacity: int,
                    anonymized: bool) -> str:
    lines: list[str] = []
    tittel = f"{scenario.name}"
    tittel += " (anonymisert)" if anonymized else " (intern)"
    lines.append(f"# {tittel}")
    lines.append("")
    lines.append(f"*{scenario.description}*")
    lines.append("")
    lines.append(f"- Solver-status: **{status}**")
    lines.append(f"- Total primær hyllekapasitet: **{total_capacity}** enheter")
    lines.append(f"- Sekundær-budsjett: **{scenario.secondary_budget}** plasser "
                 f"(k = {scenario.secondary_effectiveness})")
    lines.append(f"- Baseline margin-vektet salg: **{baseline_margin:.1f}**")
    lines.append(f"- LP-optimal margin-vektet salg: **{objective:.1f}**")
    gain = objective - baseline_margin
    pct = 100 * gain / baseline_margin if baseline_margin > 0 else 0
    lines.append(f"- Gevinst (margin-verdi): **+{gain:.1f}** (**+{pct:.1f}%**)")
    total_new_sales = table["sales_optimal"].sum()
    vol_pct = 100 * (total_new_sales - baseline_sales) / baseline_sales
    lines.append(f"- Gevinst (volum enheter): {baseline_sales:.0f} → "
                 f"{total_new_sales:.0f} (+{vol_pct:.1f}%)")
    lines.append("")
    lines.append("## Allokering per produkt")
    lines.append("")
    lines.append("| Produkt | Merke | Margin | Nå | Min | Ny | Sek | Salg nå | Salg ny | Gev % |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for prod, r in table.iterrows():
        lines.append(
            f"| {prod} | {r['brand']} | {r['margin']:.0%} | "
            f"{int(r['facings_original'])} | {int(r['facings_min'])} | "
            f"{int(r['facings_optimal'])} | {int(r['secondary_optimal'])} | "
            f"{r['sales_original']:.1f} | {r['sales_optimal']:.1f} | "
            f"{r['sales_gain_pct']:+.1f}% |"
        )
    lines.append("")
    winners = table[table["delta_facings"] > 0].index.tolist()
    losers = table[table["delta_facings"] < 0].index.tolist()
    secondaries = table[table["secondary_optimal"] > 0].index.tolist()
    lines.append(f"**Får mer primær plass ({len(winners)}):** {', '.join(winners) or '—'}")
    lines.append("")
    lines.append(f"**Gir fra seg primær plass ({len(losers)}):** {', '.join(losers) or '—'}")
    if secondaries:
        lines.append("")
        s_summary = ", ".join(f"{p} ({int(table.loc[p, 'secondary_optimal'])})"
                              for p in secondaries)
        lines.append(f"**Sekundæreksponering:** {s_summary}")
    return "\n".join(lines)


def scenario_summary(scenarios: list[Scenario],
                     objectives: dict[str, float],
                     baseline_margin: float,
                     anonymized: bool) -> str:
    lines = []
    tittel = "LP-scenarier — oppsummering (margin-vektet)"
    tittel += " (anonymisert)" if anonymized else " (intern)"
    lines.append(f"# {tittel}")
    lines.append("")
    lines.append(f"Baseline margin-vektet salg: **{baseline_margin:.1f}**.")
    lines.append("Målfunksjon = Σ (margin_i × forventet_salg_i). Marginprosent = "
                 "leverandørens brutto margin per enhet fra prislisten til Coop.")
    lines.append("")
    lines.append("| Scenario | Beskrivelse | LP-margin | Gevinst | Gev % |")
    lines.append("|---|---|---:|---:|---:|")
    for scen in scenarios:
        obj = objectives[scen.key]
        gain = obj - baseline_margin
        pct = 100 * gain / baseline_margin if baseline_margin > 0 else 0
        lines.append(
            f"| {scen.name} | {scen.description} | {obj:.1f} | +{gain:.1f} | +{pct:.1f}% |"
        )
    return "\n".join(lines)


# =====================================================================
# VISUELL OUTPUT
# =====================================================================
def plot_primary_vs_secondary(table: pd.DataFrame, path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    x_pos = range(len(table))
    width = 0.35
    ax.bar([p - width / 2 for p in x_pos], table["facings_original"],
           width=width, label="Nåværende (primær)", color="#9DB4C0")
    ax.bar([p + width / 2 for p in x_pos], table["facings_optimal"],
           width=width, label="LP primær", color="#2E86AB")
    # Sekundær stabled på toppen av LP primær
    ax.bar([p + width / 2 for p in x_pos],
           table["secondary_optimal"] * 7,  # antydet mengde (dybde 7)
           bottom=table["facings_optimal"],
           width=width, label="Sekundær (antydet)", color="#E63946", alpha=0.6)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(table.index, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Hylleenheter / indikativ sekundærvolum")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# MAIN
# =====================================================================
def main() -> None:
    for d in (FIG_DIR, FIG_INTERN, RESULT_DIR, RESULT_INTERN):
        d.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CLEAN_PARQUET)
    anon = Anonymizer.load(NAVNEREGISTER)

    stats = aggregate(df)
    total_capacity = int(stats["facings"].sum())
    baseline_sales = stats["mean_sales"].sum()
    baseline_margin = margin_weighted_sum(stats["mean_sales"], stats["margin"])

    print(f"Total primær hyllekapasitet: {total_capacity}")
    print(f"Antall SKUer: {len(stats)}")
    print(f"Baseline volum: {baseline_sales:.1f} enheter/uke")
    print(f"Baseline margin-vektet: {baseline_margin:.1f}")
    print()

    objectives: dict[str, float] = {}

    for scenario in SCENARIOS:
        demand = compute_demand_cap(stats, scenario.overserve_factor)
        x_min = compute_x_min(stats, scenario)
        result = solve(stats, demand, x_min, scenario, total_capacity)
        per_prod = format_per_product_table(result["per_product"])

        # Anonymisert utgave
        per_prod_anon = per_prod.copy()
        per_prod_anon.index = [anon.pseudo(p) for p in per_prod.index]
        per_prod_anon = per_prod_anon.sort_index()

        # Intern
        per_prod.to_csv(RESULT_INTERN / f"lp_allokering_{scenario.key}.csv")
        (RESULT_INTERN / f"lp-rapport_{scenario.key}.md").write_text(
            scenario_report(scenario, per_prod, result["status"],
                            result["objective"], baseline_margin, baseline_sales,
                            total_capacity, anonymized=False),
            encoding="utf-8",
        )
        plot_primary_vs_secondary(
            per_prod, FIG_INTERN / f"lp_allokering_{scenario.key}.png",
            title=f"{scenario.name} — intern",
        )
        # Anonym
        per_prod_anon.to_csv(RESULT_DIR / f"lp_allokering_{scenario.key}.csv")
        (RESULT_DIR / f"lp-rapport_{scenario.key}.md").write_text(
            scenario_report(scenario, per_prod_anon, result["status"],
                            result["objective"], baseline_margin, baseline_sales,
                            total_capacity, anonymized=True),
            encoding="utf-8",
        )
        plot_primary_vs_secondary(
            per_prod_anon, FIG_DIR / f"lp_allokering_{scenario.key}.png",
            title=f"{scenario.name}",
        )

        objectives[scenario.key] = result["objective"]
        gain_pct = 100 * (result["objective"] - baseline_margin) / baseline_margin
        print(f"{scenario.name:30} → margin {result['objective']:.1f} "
              f"({gain_pct:+.1f}%)")

    (RESULT_DIR / "lp-scenarier-oppsummering.md").write_text(
        scenario_summary(SCENARIOS, objectives, baseline_margin, anonymized=True),
        encoding="utf-8",
    )
    (RESULT_INTERN / "lp-scenarier-oppsummering.md").write_text(
        scenario_summary(SCENARIOS, objectives, baseline_margin, anonymized=False),
        encoding="utf-8",
    )
    print(f"\nOppsummering: {RESULT_DIR / 'lp-scenarier-oppsummering.md'}")


if __name__ == "__main__":
    main()
