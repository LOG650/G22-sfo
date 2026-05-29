#!/usr/bin/env python3
"""
ACT-3.4.7 LP-modell med STYKKEVIS LINEÆR produktivitet (v3-modellen).

Erstatter den lineære antagelsen y_i ≤ ρ_i · x_i (B2 i v2-rapporten) med en
stykkevis lineær formulering: produktiviteten er ρ_i opp til nåværende
kapasitet c_i, og k_β · ρ_i over c_i. Dette uttrykker eksplisitt avtakende
marginalavkastning på hylleplass — i tråd med Curhans space-elasticity-formel
(s_i = α_i · x_i^β, β < 1) men i en linearisert form som passer i LP.

Reformulering av R2:
  x_i = x1_i + x2_i                    (sum av "under-c_i" og "over-c_i" plass)
  x1_i ≤ c_i                            (slope ρ_i opp til c_i)
  y_i ≤ ρ_i · x1_i + k_β · ρ_i · x2_i + k · ρ_i · z_i
  y_i ≤ d_i                            (etterspørselstak, uendret)

Begrunnelse for knekkpunktet ved c_i:
  - c_i er det eneste empirisk observerte produktivitetspunktet
  - Extrapolering oppover med samme slope er ekvivalent med å påstå at den
    observerte gjennomsnittsproduktiviteten holder seg ved doblet plass
  - Den stykkevise reduksjonen reflekterer at additional facings betjener
    mindre intens etterspørsel (kunder som ellers ikke ville sett produktet)

Hovedscenario: k_β = 0.5 (halvert marginal-produktivitet over c_i).
Sensitivitet: k_β ∈ {0.3, 0.5, 0.7}.

Fire scenarier (samme struktur som 03_lp_modell.py):
  V3-S1 Primær-omfordeling, stykkevis lineær
  V3-S2 Primær + sekundær, stykkevis lineær (hovedanbefaling)
  V3-S3 Konservativ
  V3-S4 Implementerbar (±50%)
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

K_BETA_MAIN = 0.5
K_BETA_SENSITIVITY = [0.3, 0.5, 0.7]


@dataclass
class Scenario:
    key: str
    name: str
    description: str
    x_min_facings: int
    overserve_factor: float
    secondary_budget: int
    secondary_effectiveness: float
    max_change_pct: float | None = None
    k_beta: float = K_BETA_MAIN


SCENARIOS = [
    Scenario(
        key="V3_S1_primaer",
        name="V3-S1 Primær-omfordeling",
        description=("Stykkevis lineær produktivitet (k_β=0.5). Reallokering kun "
                     "innen primær hylle, x_min = 1 kolli per SKU, 2× etterspørsel, "
                     "ingen sekundæreksponering."),
        x_min_facings=3,
        overserve_factor=2.0,
        secondary_budget=0,
        secondary_effectiveness=0.0,
    ),
    Scenario(
        key="V3_S2_primaer_sek",
        name="V3-S2 Primær + sekundær",
        description=("Stykkevis lineær produktivitet (k_β=0.5). Hovedanbefaling: "
                     "primær-omfordeling pluss 3 sekundærplasser. k = 1.5× primær."),
        x_min_facings=3,
        overserve_factor=2.0,
        secondary_budget=3,
        secondary_effectiveness=1.5,
    ),
    Scenario(
        key="V3_S3_konservativ",
        name="V3-S3 Konservativ",
        description=("Stykkevis lineær produktivitet (k_β=0.5). Konservativ: "
                     "x_min = max(50% av dagens, 1 kolli), 1.5× etterspørsel."),
        x_min_facings=3,
        overserve_factor=1.5,
        secondary_budget=0,
        secondary_effectiveness=0.0,
    ),
    Scenario(
        key="V3_S4_implementerbar",
        name="V3-S4 Implementerbar",
        description=("Stykkevis lineær produktivitet (k_β=0.5). Som V3-S2 men "
                     "med ±50% endringsgrense per SKU."),
        x_min_facings=3,
        overserve_factor=2.0,
        secondary_budget=3,
        secondary_effectiveness=1.5,
        max_change_pct=0.5,
    ),
]


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("Produkt").agg(
        mean_sales=("Ant_solgt", "mean"),
        facings=("Kapasitet", "first"),
        dybde=("Dybde", "first"),
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
    kolli = (stats["dybde"] * scenario.x_min_facings).astype(int)
    if "konservativ" in scenario.key:
        frac = (stats["facings"] * 0.5).apply(int)
        return pd.concat([kolli, frac], axis=1).max(axis=1).astype(int)
    return kolli


def solve_piecewise(stats: pd.DataFrame, demand: pd.Series, x_min: pd.Series,
                    scenario: Scenario, total_capacity: int) -> dict:
    """LP med stykkevis lineær produktivitet:
       y_i ≤ ρ_i · x1_i + k_β · ρ_i · x2_i + k · ρ_i · z_i
       der x1_i ≤ c_i og x_i = x1_i + x2_i."""
    prods = list(stats.index)
    m = pulp.LpProblem(scenario.key, pulp.LpMaximize)

    # Splitt x_i i to deler: x1_i (under c_i) og x2_i (over c_i)
    x1 = {p: pulp.LpVariable(f"x1_{p}", lowBound=0, cat="Integer") for p in prods}
    x2 = {p: pulp.LpVariable(f"x2_{p}", lowBound=0, cat="Integer") for p in prods}
    y = {p: pulp.LpVariable(f"y_{p}", lowBound=0) for p in prods}
    s = {p: pulp.LpVariable(f"s_{p}", lowBound=0, cat="Integer") for p in prods}

    # Målfunksjon
    m += pulp.lpSum(stats.loc[p, "margin"] * y[p] for p in prods)

    # Total kapasitet
    m += pulp.lpSum(x1[p] + x2[p] for p in prods) == total_capacity, "primaer_kap"

    # Sekundær-budsjett
    m += pulp.lpSum(s[p] for p in prods) <= scenario.secondary_budget, "sekundaer_kap"

    # x_min og x_max (per SKU)
    k = scenario.secondary_effectiveness
    k_beta = scenario.k_beta
    for p in prods:
        c_i = int(stats.loc[p, "facings"])
        rho = stats.loc[p, "productivity"]
        # Stykkevis lineær R2
        m += y[p] <= rho * x1[p] + k_beta * rho * x2[p] + k * rho * s[p], f"prod_cap_{p}"
        m += y[p] <= demand[p], f"demand_cap_{p}"
        # x1_i ≤ c_i (slope ρ_i bare gjelder under c_i)
        m += x1[p] <= c_i, f"tier1_cap_{p}"
        # x_min binder summen x1+x2
        m += x1[p] + x2[p] >= int(x_min[p]), f"x_min_{p}"

    # Endringsgrense per SKU
    if scenario.max_change_pct is not None:
        theta = scenario.max_change_pct
        for p in prods:
            c_i = int(stats.loc[p, "facings"])
            upper = int((1 + theta) * c_i)
            lower = max(int((1 - theta) * c_i), int(x_min[p]))
            m += x1[p] + x2[p] <= upper, f"change_upper_{p}"
            m += x1[p] + x2[p] >= lower, f"change_lower_{p}"

    m.solve(pulp.PULP_CBC_CMD(msg=False))

    rows = []
    for p in prods:
        x1_val = int(round(x1[p].value()))
        x2_val = int(round(x2[p].value()))
        rows.append({
            "facings_original": int(stats.loc[p, "facings"]),
            "facings_min": int(x_min[p]),
            "facings_tier1": x1_val,
            "facings_tier2": x2_val,
            "facings_optimal": x1_val + x2_val,
            "secondary_optimal": int(round(s[p].value())),
            "sales_original": round(stats.loc[p, "mean_sales"], 1),
            "sales_optimal": round(y[p].value(), 1),
            "demand_cap": round(demand[p], 1),
            "productivity": round(stats.loc[p, "productivity"], 3),
            "margin": stats.loc[p, "margin"],
            "brand": stats.loc[p, "brand"],
        })
    per_product = pd.DataFrame(rows, index=prods)

    return {
        "status": pulp.LpStatus[m.status],
        "objective": pulp.value(m.objective),
        "per_product": per_product,
        "k_beta": k_beta,
    }


def format_per_product_table(res: pd.DataFrame) -> pd.DataFrame:
    out = res.copy()
    out["delta_facings"] = out["facings_optimal"] - out["facings_original"]
    out["delta_sales"] = (out["sales_optimal"] - out["sales_original"]).round(1)
    out["sales_gain_pct"] = (
        out["delta_sales"] / out["sales_original"] * 100
    ).round(1)
    return out[[
        "facings_original", "facings_min", "facings_tier1", "facings_tier2",
        "facings_optimal", "delta_facings",
        "secondary_optimal",
        "sales_original", "sales_optimal", "delta_sales", "sales_gain_pct",
        "demand_cap", "productivity", "margin", "brand",
    ]]


def margin_weighted_sum(sales: pd.Series, margin: pd.Series) -> float:
    return float((sales * margin).sum())


def scenario_report(scenario: Scenario, table: pd.DataFrame, status: str,
                    objective: float, baseline_margin: float,
                    baseline_sales: float, total_capacity: int,
                    anonymized: bool) -> str:
    lines: list[str] = []
    tittel = f"{scenario.name} (k_β = {scenario.k_beta})"
    tittel += " — anonymisert" if anonymized else " — intern"
    lines.append(f"# {tittel}")
    lines.append("")
    lines.append(f"*{scenario.description}*")
    lines.append("")
    lines.append(f"- Solver-status: **{status}**")
    lines.append(f"- Total primær hyllekapasitet: **{total_capacity}** enheter")
    lines.append(f"- Sekundær-budsjett: **{scenario.secondary_budget}** plasser "
                 f"(k = {scenario.secondary_effectiveness})")
    lines.append(f"- Stykkevis lineær: full slope ρ_i opp til c_i, deretter "
                 f"k_β · ρ_i over c_i (k_β = {scenario.k_beta})")
    lines.append(f"- Baseline margin-vektet salg: **{baseline_margin:.1f}**")
    lines.append(f"- LP-optimal margin-vektet salg: **{objective:.1f}**")
    gain = objective - baseline_margin
    pct = 100 * gain / baseline_margin if baseline_margin > 0 else 0
    lines.append(f"- Gevinst (margin-verdi): **+{gain:.1f}** (**+{pct:.1f}%**)")
    total_new_sales = table["sales_optimal"].sum()
    vol_pct = 100 * (total_new_sales - baseline_sales) / baseline_sales
    lines.append(f"- Gevinst (volum enheter): {baseline_sales:.0f} → "
                 f"{total_new_sales:.0f} (+{vol_pct:.1f}%)")
    n_split = (table["facings_tier2"] > 0).sum()
    lines.append(f"- SKUer som strekkes over c_i (tier 2 brukt): **{n_split}**")
    lines.append("")
    lines.append("## Allokering per produkt")
    lines.append("")
    lines.append("| Produkt | Merke | Marg | Nå | Min | Tier1 | Tier2 | Ny | Sek | Salg nå | Salg ny | Gev % |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for prod, r in table.iterrows():
        lines.append(
            f"| {prod} | {r['brand']} | {r['margin']:.0%} | "
            f"{int(r['facings_original'])} | {int(r['facings_min'])} | "
            f"{int(r['facings_tier1'])} | {int(r['facings_tier2'])} | "
            f"{int(r['facings_optimal'])} | {int(r['secondary_optimal'])} | "
            f"{r['sales_original']:.1f} | {r['sales_optimal']:.1f} | "
            f"{r['sales_gain_pct']:+.1f}% |"
        )
    return "\n".join(lines)


def run_sensitivity(stats: pd.DataFrame, base_scenario: Scenario,
                    total_capacity: int, baseline_margin: float,
                    baseline_volume: float) -> tuple[str, pd.DataFrame]:
    """Variér k_β og rapporter gevinst-fordeling for V3-S2."""
    rows = []
    lines = []
    lines.append("## Sensitivitet på k_β (slope over c_i)")
    lines.append("")
    lines.append("| k_β | LP-margin | Gevinst | Gev % | Volum-gev % |")
    lines.append("|---:|---:|---:|---:|---:|")
    for kb in K_BETA_SENSITIVITY:
        scen = Scenario(
            key=f"V3_S2_kbeta_{int(kb*100)}",
            name=f"V3-S2 sensitivitet k_β={kb}",
            description="",
            x_min_facings=base_scenario.x_min_facings,
            overserve_factor=base_scenario.overserve_factor,
            secondary_budget=base_scenario.secondary_budget,
            secondary_effectiveness=base_scenario.secondary_effectiveness,
            k_beta=kb,
        )
        demand = compute_demand_cap(stats, scen.overserve_factor)
        x_min = compute_x_min(stats, scen)
        res = solve_piecewise(stats, demand, x_min, scen, total_capacity)
        margin_pct = 100 * (res["objective"] - baseline_margin) / baseline_margin
        vol = float(res["per_product"]["sales_optimal"].sum())
        vol_pct = 100 * (vol - baseline_volume) / baseline_volume
        rows.append({
            "k_beta": kb,
            "lp_margin": res["objective"],
            "gain": res["objective"] - baseline_margin,
            "gain_pct": margin_pct,
            "vol_gain_pct": vol_pct,
        })
        lines.append(
            f"| {kb} | {res['objective']:.1f} | "
            f"+{res['objective'] - baseline_margin:.1f} | "
            f"+{margin_pct:.1f}% | +{vol_pct:.1f}% |"
        )
    return "\n".join(lines), pd.DataFrame(rows)


def main() -> None:
    for d in (FIG_DIR, FIG_INTERN, RESULT_DIR, RESULT_INTERN):
        d.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CLEAN_PARQUET)
    anon = Anonymizer.load(NAVNEREGISTER)

    stats = aggregate(df)
    total_capacity = int(stats["facings"].sum())
    baseline_sales = stats["mean_sales"].sum()
    baseline_margin = margin_weighted_sum(stats["mean_sales"], stats["margin"])

    print("=== V3-MODELLEN: STYKKEVIS LINEÆR PRODUKTIVITET ===")
    print(f"Total primær hyllekapasitet: {total_capacity}")
    print(f"Antall SKUer: {len(stats)}")
    print(f"Baseline volum: {baseline_sales:.1f} enheter/uke")
    print(f"Baseline margin-vektet: {baseline_margin:.1f}")
    print(f"Hovedscenario k_β: {K_BETA_MAIN}")
    print()

    summary_rows = []
    for scenario in SCENARIOS:
        demand = compute_demand_cap(stats, scenario.overserve_factor)
        x_min = compute_x_min(stats, scenario)
        result = solve_piecewise(stats, demand, x_min, scenario, total_capacity)
        per_prod = format_per_product_table(result["per_product"])

        per_prod_anon = per_prod.copy()
        per_prod_anon.index = [anon.pseudo(p) for p in per_prod.index]
        per_prod_anon = per_prod_anon.sort_index()

        # Intern + anon
        per_prod.to_csv(RESULT_INTERN / f"v3_allokering_{scenario.key}.csv")
        (RESULT_INTERN / f"v3-rapport_{scenario.key}.md").write_text(
            scenario_report(scenario, per_prod, result["status"],
                            result["objective"], baseline_margin, baseline_sales,
                            total_capacity, anonymized=False),
            encoding="utf-8",
        )
        per_prod_anon.to_csv(RESULT_DIR / f"v3_allokering_{scenario.key}.csv")
        (RESULT_DIR / f"v3-rapport_{scenario.key}.md").write_text(
            scenario_report(scenario, per_prod_anon, result["status"],
                            result["objective"], baseline_margin, baseline_sales,
                            total_capacity, anonymized=True),
            encoding="utf-8",
        )

        vol = float(per_prod["sales_optimal"].sum())
        margin_pct = 100 * (result["objective"] - baseline_margin) / baseline_margin
        vol_pct = 100 * (vol - baseline_sales) / baseline_sales
        summary_rows.append({
            "scenario": scenario.key,
            "k_beta": scenario.k_beta,
            "margin": result["objective"],
            "gain_pct_margin": margin_pct,
            "volume": vol,
            "gain_pct_volume": vol_pct,
            "n_tier2": int((per_prod["facings_tier2"] > 0).sum()),
        })
        print(f"{scenario.name:35} margin {result['objective']:.1f} "
              f"({margin_pct:+.1f}%, volum {vol:.0f} {vol_pct:+.1f}%, "
              f"tier2-SKUer: {(per_prod['facings_tier2'] > 0).sum()})")

    pd.DataFrame(summary_rows).to_csv(
        RESULT_DIR / "v3_scenarier_oppsummering.csv", index=False,
    )

    # Sensitivitet på k_β
    print()
    print("--- Sensitivitet på k_β ---")
    s2_base = next(s for s in SCENARIOS if s.key == "V3_S2_primaer_sek")
    sens_text, sens_df = run_sensitivity(
        stats, s2_base, total_capacity, baseline_margin, baseline_sales,
    )
    sens_df.to_csv(RESULT_DIR / "v3_sensitivitet_kbeta.csv", index=False)
    sens_df.to_csv(RESULT_INTERN / "v3_sensitivitet_kbeta.csv", index=False)
    print(sens_text)
    print()
    print(f"Skrevet: {RESULT_DIR}/v3_*.csv og v3-rapport_*.md")


if __name__ == "__main__":
    main()
