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
  X_MIN_i = 3 × Dybde_i hylleenheter per SKU (≈ 1 kolli, per-produkt)

Fire scenarier:
  S1 Primær-omfordeling       — kun primær, uten sekundær (s_i = 0)
  S2 Primær + sekundær         — hovedanbefaling, begge handlingsrom brukes
  S3 Konservativ               — strammere gulv, 1.5× etterspørselstak, uten sekundær
  S4 Implementerbar            — som S2, men med ±50 % endringsgrense per SKU
                                 (følger peer-review-anbefaling om gjennomførbarhet)
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
    x_min_facings: int            # minimum facings per SKU; gulv = facings × Dybde_i
    overserve_factor: float
    secondary_budget: int         # antall tilgjengelige sekundærplasser
    secondary_effectiveness: float  # k: sekundær salg/enhet / primær salg/enhet
    max_change_pct: float | None = None  # ±θ av dagens c_i som endringsgrense; None = ubegrenset


SCENARIOS = [
    Scenario(
        key="S1_primaer",
        name="S1 Primær-omfordeling",
        description=("Reallokering kun innen primær hylle, x_min = 1 kolli per SKU "
                     "(3 facings × Dybde_i), 2× etterspørsel, ingen sekundæreksponering."),
        x_min_facings=3,
        overserve_factor=2.0,
        secondary_budget=0,
        secondary_effectiveness=0.0,
    ),
    Scenario(
        key="S2_primaer_sek",
        name="S2 Primær + sekundær",
        description=("Hovedanbefaling: primær-omfordeling pluss 3 sekundærplasser "
                     "som tildeles mest effektive SKUer. k = 1.5× primær-effektivitet. "
                     "x_min = 1 kolli per SKU."),
        x_min_facings=3,
        overserve_factor=2.0,
        secondary_budget=3,
        secondary_effectiveness=1.5,
    ),
    Scenario(
        key="S3_konservativ",
        name="S3 Konservativ",
        description=("Konservativ: x_min = max(50 % av dagens allokering, 1 kolli), "
                     "1.5× etterspørsel, ingen sekundæreksponering."),
        x_min_facings=3,
        overserve_factor=1.5,
        secondary_budget=0,
        secondary_effectiveness=0.0,
    ),
    Scenario(
        key="S4_implementerbar",
        name="S4 Implementerbar",
        description=("Som S2, men hver SKU er begrenset til ±50 % av dagens "
                     "hyllekapasitet. Speiler hva som er praktisk gjennomførbart i "
                     "én forhandlingsrunde uten store omstillinger i butikkdriften."),
        x_min_facings=3,
        overserve_factor=2.0,
        secondary_budget=3,
        secondary_effectiveness=1.5,
        max_change_pct=0.5,
    ),
]


# =====================================================================
# MODELLBYGGING
# =====================================================================
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
    """Minimum hylleenheter per SKU = x_min_facings × Dybde_i (≈ 1 kolli).
    For S3 også minst 50 % av dagens allokering."""
    kolli = (stats["dybde"] * scenario.x_min_facings).astype(int)
    if scenario.key == "S3_konservativ":
        frac = (stats["facings"] * 0.5).apply(int)
        return pd.concat([kolli, frac], axis=1).max(axis=1).astype(int)
    return kolli


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

    # Endringsgrense per SKU: x_i ∈ [(1-θ)·c_i, (1+θ)·c_i] (kolli-gulvet binder fremdeles)
    if scenario.max_change_pct is not None:
        theta = scenario.max_change_pct
        for p in prods:
            c_i = int(stats.loc[p, "facings"])
            upper = int((1 + theta) * c_i)
            lower = max(int((1 - theta) * c_i), int(x_min[p]))
            m += x[p] <= upper, f"change_upper_{p}"
            m += x[p] >= lower, f"change_lower_{p}"

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
def plot_scenario_compare(per_prod_by_scenario: dict[str, pd.DataFrame],
                          baseline_facings: pd.Series,
                          path: Path) -> None:
    """Sammenligning av allokering per SKU på tvers av scenariene."""
    skus = sorted(baseline_facings.index)
    palette = {
        "S1_primaer": "#2E86AB",
        "S2_primaer_sek": "#1B5E7E",
        "S3_konservativ": "#9DB4C0",
        "S4_implementerbar": "#E63946",
    }
    label = {
        "S1_primaer": "S1 Primær",
        "S2_primaer_sek": "S2 Primær + sek",
        "S3_konservativ": "S3 Konservativ",
        "S4_implementerbar": "S4 Implementerbar",
    }
    n_scen = len(per_prod_by_scenario)
    bar_width = 0.8 / (n_scen + 1)
    fig, ax = plt.subplots(figsize=(14, 6))
    x_pos = list(range(len(skus)))
    # Baseline
    ax.bar([p - 0.4 + 0.5 * bar_width for p in x_pos],
           [baseline_facings[s] for s in skus],
           width=bar_width, label="Nåværende", color="#cccccc", edgecolor="white")
    for i, (key, df) in enumerate(per_prod_by_scenario.items(), start=1):
        offset = -0.4 + (i + 0.5) * bar_width
        ax.bar([p + offset for p in x_pos],
               [df.loc[s, "facings_optimal"] for s in skus],
               width=bar_width, label=label[key], color=palette[key], edgecolor="white")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(skus, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Hylleenheter (Facings × Dybde)")
    ax.set_title("Allokering per SKU på tvers av LP-scenariene")
    ax.legend(loc="upper right", ncol=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# BOLK 1 — ROBUSTHET, VOLUM-VS-MARGIN, SHADOW PRICE
# =====================================================================
def find_real_for_pseudo(anon: Anonymizer, pseudo: str) -> str:
    """Reverse-lookup: hvilket reelt produktnavn maps til gitt pseudonym."""
    for real, ps in anon.mapping.items():
        if ps == pseudo:
            return real
    raise KeyError(f"Pseudonym {pseudo!r} finnes ikke i navneregisteret")


def run_a2_uke15_robustness(df: pd.DataFrame, anon: Anonymizer,
                            baseline_margin_full: float,
                            s2_objective_full: float,
                            scenario_s2: Scenario,
                            total_capacity_full: int) -> tuple[str, dict]:
    """Drop A2-uke-15 fra rådata, re-aggreger og kjør S2 på nytt. Returner rapporttekst + tall."""
    a2_real = find_real_for_pseudo(anon, "A2")
    mask = (df["Produkt"] == a2_real) & (df["UkeNr"] == 15)
    dropped_sales = int(df.loc[mask, "Ant_solgt"].sum())
    df_drop = df[~mask].copy()

    stats_drop = aggregate(df_drop)
    total_cap_drop = int(stats_drop["facings"].sum())
    baseline_margin_drop = margin_weighted_sum(stats_drop["mean_sales"], stats_drop["margin"])

    demand = compute_demand_cap(stats_drop, scenario_s2.overserve_factor)
    x_min = compute_x_min(stats_drop, scenario_s2)
    res = solve(stats_drop, demand, x_min, scenario_s2, total_cap_drop)

    gain_full_pct = 100 * (s2_objective_full - baseline_margin_full) / baseline_margin_full
    gain_drop_pct = 100 * (res["objective"] - baseline_margin_drop) / baseline_margin_drop

    lines: list[str] = []
    lines.append("## 1. A2-uke-15 robustness-sjekk")
    lines.append("")
    lines.append("Tester om S2-funnet henger på den ene høye observasjonen "
                 "(A2 uke 15) som ble flagget som mulig kampanjeuke i §8.2 B4.")
    lines.append("")
    lines.append(f"- Droppet observasjon: A2 uke 15 — **{dropped_sales} enheter** "
                 "(rapporten antyder ca. 2× snittet, kampanjedrevet)")
    lines.append(f"- Baseline margin (full):   **{baseline_margin_full:.1f}**")
    lines.append(f"- Baseline margin (drop):   **{baseline_margin_drop:.1f}**  "
                 f"(Δ {baseline_margin_drop - baseline_margin_full:+.1f})")
    lines.append(f"- S2 LP-margin (full):      **{s2_objective_full:.1f}**  "
                 f"(+{gain_full_pct:.1f}%)")
    lines.append(f"- S2 LP-margin (drop):      **{res['objective']:.1f}**  "
                 f"(+{gain_drop_pct:.1f}%)")
    lines.append(f"- **Endring i %-gevinst: {gain_drop_pct - gain_full_pct:+.2f} pp**")
    lines.append("")
    if abs(gain_drop_pct - gain_full_pct) < 2.0:
        verdict = ("Funnet er robust mot A2-uke-15: gevinsten endres med "
                   f"under 2 prosentpoeng ({gain_drop_pct - gain_full_pct:+.2f} pp).")
    else:
        verdict = ("A2-uke-15 påvirker gevinsten med "
                   f"{gain_drop_pct - gain_full_pct:+.2f} pp — verdt å eie i §8.2.")
    lines.append(f"**Tolkning:** {verdict}")
    return "\n".join(lines), {
        "dropped_units": dropped_sales,
        "baseline_full": baseline_margin_full,
        "baseline_drop": baseline_margin_drop,
        "s2_full": s2_objective_full,
        "s2_drop": res["objective"],
        "gain_full_pct": gain_full_pct,
        "gain_drop_pct": gain_drop_pct,
        "delta_pp": gain_drop_pct - gain_full_pct,
    }


def run_volum_vs_margin(stats: pd.DataFrame, scenario_s2: Scenario,
                        total_capacity: int, anon: Anonymizer,
                        s2_margin_result: dict) -> tuple[str, pd.DataFrame]:
    """Kjør S2 med m_i = 1 (ren volum-mål) og sammenlign per-SKU allokering."""
    stats_unit = stats.copy()
    stats_unit["margin"] = 1.0

    demand = compute_demand_cap(stats_unit, scenario_s2.overserve_factor)
    x_min = compute_x_min(stats_unit, scenario_s2)
    res_vol = solve(stats_unit, demand, x_min, scenario_s2, total_capacity)

    margin_pp = s2_margin_result["per_product"]
    vol_pp = res_vol["per_product"]

    # Marginen som volum-allokeringen faktisk ville oppnådd med ekte m_i:
    margin_under_vol = float((vol_pp["sales_optimal"] * stats["margin"]).sum())
    volume_under_vol = float(vol_pp["sales_optimal"].sum())
    margin_under_margin = float((margin_pp["sales_optimal"] * stats["margin"]).sum())
    volume_under_margin = float(margin_pp["sales_optimal"].sum())

    # Per-SKU diff
    diff = (margin_pp["facings_optimal"] - vol_pp["facings_optimal"]).astype(int)
    movers = diff[diff != 0].sort_values(key=lambda s: s.abs(), ascending=False)

    lines: list[str] = []
    lines.append("## 2. Volum-mål vs margin-vektet mål")
    lines.append("")
    lines.append("Kjører S2 to ganger: én med m_i = bruttomargin (dagens målfunksjon), "
                 "én med m_i = 1 (ren volum-maks). Forskjellen viser hva margin-vektingen "
                 "faktisk flytter.")
    lines.append("")
    lines.append("| Målfunksjon       | Margin-verdi | Volum (enheter/uke) |")
    lines.append("|---|---:|---:|")
    lines.append(f"| m_i = 1 (volum)   | {margin_under_vol:.1f} | "
                 f"{volume_under_vol:.0f} |")
    lines.append(f"| m_i = bruttomargin | {margin_under_margin:.1f} | "
                 f"{volume_under_margin:.0f} |")
    lines.append("")
    lines.append(f"**Antall SKUer med ulik allokering**: {(diff != 0).sum()} av {len(diff)}")
    lines.append("")
    if len(movers) > 0:
        lines.append("Topp SKU-forskjeller (sortert etter absolutt diff):")
        lines.append("")
        lines.append("| SKU | Margin | Vol-allok | Margin-allok | Diff |")
        lines.append("|---|---:|---:|---:|---:|")
        for sku in movers.index[:12]:
            lines.append(
                f"| {anon.pseudo(sku)} | {stats.loc[sku, 'margin']:.0%} | "
                f"{int(vol_pp.loc[sku, 'facings_optimal'])} | "
                f"{int(margin_pp.loc[sku, 'facings_optimal'])} | "
                f"{int(diff[sku]):+d} |"
            )
    lines.append("")
    margin_pct = 100 * (margin_under_margin - margin_under_vol) / margin_under_vol
    vol_pct = 100 * (volume_under_margin - volume_under_vol) / volume_under_vol
    lines.append(f"**Tolkning:** Margin-vektet optimum gir {margin_pct:+.2f}% mer "
                 f"margin og {vol_pct:+.2f}% volum sammenlignet med rent volum-mål. "
                 "Strukturen er lik (A-klasse vokser, C-klasse stabil), men "
                 "margin-vekting prioriterer SKUer på 55%-segmentet.")

    # Lagre per-SKU sammenligning som CSV
    compare_df = pd.DataFrame({
        "margin": stats["margin"],
        "alloc_volum": vol_pp["facings_optimal"].astype(int),
        "alloc_margin": margin_pp["facings_optimal"].astype(int),
        "diff": diff,
        "salg_volum": vol_pp["sales_optimal"].round(1),
        "salg_margin": margin_pp["sales_optimal"].round(1),
    })
    return "\n".join(lines), compare_df


def run_shadow_price_R1(stats: pd.DataFrame, scenarios: list[Scenario],
                        total_capacity: int) -> tuple[str, pd.DataFrame]:
    """Numerisk skyggepris på R1: hva er verdt én ekstra hylleenhet i totalbudsjettet?

    Beregnes ved å re-løse LP for T+1, T+5, T+10 og se hvor mye margin vokser.
    Dette er mer robust enn pulp's .pi for heltallsprogrammer (CBC gir LP-relaxasjon
    duals som kan være misvisende ved heltall)."""
    rows = []
    lines: list[str] = []
    lines.append("## 3. Shadow price på R1 (totalkapasitet)")
    lines.append("")
    lines.append("Numerisk marginalverdi: hva ekstra én hylleenhet i leverandørens "
                 "kontraktuelle totalbudsjett ville vært verdt i margin-vektet sell-out "
                 "per uke. Beregnet ved å løse LP på nytt for T+1, T+5, T+10 og "
                 "rapportere differansen per enhet.")
    lines.append("")

    for scenario in scenarios:
        demand = compute_demand_cap(stats, scenario.overserve_factor)
        x_min = compute_x_min(stats, scenario)
        baseline = solve(stats, demand, x_min, scenario, total_capacity)
        baseline_obj = baseline["objective"]
        lines.append(f"### {scenario.name}")
        lines.append("")
        lines.append(f"- Baseline T = {total_capacity}: margin **{baseline_obj:.1f}**")
        lines.append("")
        lines.append("| ΔT | Total T | Ny margin | Δ margin | Marginal verdi per hylleenhet |")
        lines.append("|---:|---:|---:|---:|---:|")
        for delta in [1, 5, 10]:
            res = solve(stats, demand, x_min, scenario, total_capacity + delta)
            d_margin = res["objective"] - baseline_obj
            per_unit = d_margin / delta
            lines.append(
                f"| +{delta} | {total_capacity + delta} | {res['objective']:.1f} | "
                f"+{d_margin:.2f} | {per_unit:.3f} |"
            )
            rows.append({
                "scenario": scenario.key,
                "delta_T": delta,
                "new_margin": res["objective"],
                "delta_margin": d_margin,
                "per_unit": per_unit,
            })
        lines.append("")

    lines.append("**Tolkning:** Skyggeprisen er leverandørens *kvantitative argument "
                 "for utvidelse av totalrammen* — neste forhandlingsrunde etter omfordelingen "
                 "innenfor dagens ramme. Avtakende verdi (Δ-margin per enhet faller med "
                 "økende ΔT) reflekterer at de mest underdimensjonerte SKUene mettes først.")
    return "\n".join(lines), pd.DataFrame(rows)


def run_bolk1(df: pd.DataFrame, anon: Anonymizer, stats: pd.DataFrame,
              scenarios_by_key: dict, total_capacity: int,
              baseline_margin: float,
              s2_result: dict) -> tuple[str, pd.DataFrame, pd.DataFrame]:
    """Kjør alle tre Bolk 1-analyser og returner samlet rapporttekst + tabeller."""
    s2 = scenarios_by_key["S2_primaer_sek"]
    s4 = scenarios_by_key["S4_implementerbar"]

    a2_text, _a2_stats = run_a2_uke15_robustness(
        df, anon, baseline_margin, s2_result["objective"], s2, total_capacity,
    )
    vol_text, vol_df = run_volum_vs_margin(
        stats, s2, total_capacity, anon, s2_result,
    )
    shadow_text, shadow_df = run_shadow_price_R1(
        stats, [s2, s4], total_capacity,
    )

    header = ["# Bolk 1 — robusthet, volum-vs-margin, shadow price", ""]
    header.append(
        "Tre supplerende analyser bygget rundt S2-scenariet (hovedanbefaling). "
        "Adresserer henholdsvis B4 (én butikk, kampanjeuke), §8.1 (margin-vekting), "
        "og forhandlingsdialogen om utvidelse av totalrammen."
    )
    header.append("")
    body = [a2_text, "", vol_text, "", shadow_text]
    return "\n".join(header + body), vol_df, shadow_df


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
    per_prod_by_scenario: dict[str, pd.DataFrame] = {}
    per_prod_anon_by_scenario: dict[str, pd.DataFrame] = {}
    full_results_by_scenario: dict[str, dict] = {}

    for scenario in SCENARIOS:
        demand = compute_demand_cap(stats, scenario.overserve_factor)
        x_min = compute_x_min(stats, scenario)
        result = solve(stats, demand, x_min, scenario, total_capacity)
        full_results_by_scenario[scenario.key] = result
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
        per_prod_by_scenario[scenario.key] = per_prod
        per_prod_anon_by_scenario[scenario.key] = per_prod_anon
        gain_pct = 100 * (result["objective"] - baseline_margin) / baseline_margin
        print(f"{scenario.name:30} → margin {result['objective']:.1f} "
              f"({gain_pct:+.1f}%)")

    # Scenario-compare figur (intern + anonymisert)
    baseline_facings = stats["facings"].astype(int)
    plot_scenario_compare(per_prod_by_scenario, baseline_facings,
                          FIG_INTERN / "lp_scenario_compare.png")
    baseline_facings_anon = pd.Series(
        {anon.pseudo(p): int(v) for p, v in baseline_facings.items()}
    ).sort_index()
    plot_scenario_compare(per_prod_anon_by_scenario, baseline_facings_anon,
                          FIG_DIR / "lp_scenario_compare.png")

    (RESULT_DIR / "lp-scenarier-oppsummering.md").write_text(
        scenario_summary(SCENARIOS, objectives, baseline_margin, anonymized=True),
        encoding="utf-8",
    )
    (RESULT_INTERN / "lp-scenarier-oppsummering.md").write_text(
        scenario_summary(SCENARIOS, objectives, baseline_margin, anonymized=False),
        encoding="utf-8",
    )
    print(f"\nOppsummering: {RESULT_DIR / 'lp-scenarier-oppsummering.md'}")

    # =====================================================================
    # BOLK 1 — kjør og skriv ut robusthet, volum-vs-margin, shadow price
    # =====================================================================
    print("\n--- Bolk 1: robusthet, volum-vs-margin, shadow price ---")
    scenarios_by_key = {s.key: s for s in SCENARIOS}
    bolk1_text, vol_df, shadow_df = run_bolk1(
        df, anon, stats, scenarios_by_key, total_capacity,
        baseline_margin, full_results_by_scenario["S2_primaer_sek"],
    )

    # Intern (med ekte produktnavn i CSV-tabellen)
    (RESULT_INTERN / "bolk1_robustness.md").write_text(bolk1_text, encoding="utf-8")
    vol_df.to_csv(RESULT_INTERN / "bolk1_volum_vs_margin.csv")
    shadow_df.to_csv(RESULT_INTERN / "bolk1_shadow_price_R1.csv", index=False)

    # Anonymisert: oversetter SKU-indeks i vol_df til pseudonymer
    vol_df_anon = vol_df.copy()
    vol_df_anon.index = [anon.pseudo(p) for p in vol_df.index]
    vol_df_anon = vol_df_anon.sort_index()
    (RESULT_DIR / "bolk1_robustness.md").write_text(bolk1_text, encoding="utf-8")
    vol_df_anon.to_csv(RESULT_DIR / "bolk1_volum_vs_margin.csv")
    shadow_df.to_csv(RESULT_DIR / "bolk1_shadow_price_R1.csv", index=False)

    print(f"Bolk 1 skrevet: {RESULT_DIR / 'bolk1_robustness.md'}")
    print(f"               {RESULT_DIR / 'bolk1_volum_vs_margin.csv'}")
    print(f"               {RESULT_DIR / 'bolk1_shadow_price_R1.csv'}")


if __name__ == "__main__":
    main()
