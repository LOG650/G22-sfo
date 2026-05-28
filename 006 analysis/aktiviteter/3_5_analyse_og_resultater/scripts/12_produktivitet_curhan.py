#!/usr/bin/env python3
"""
ACT-3.5.X Sensitivitet på produktivitetsantakelse under c_i (Curhan vs v3).

v3-modellen (`11_lp_piecewise.py`) bruker konstant gjennomsnittsproduktivitet
ρ_i = mean_sales_i / c_i opp til c_i, deretter k_β · ρ_i over c_i (default 0.5).
Antagelsen er asymmetrisk: ρ_i er målt VED c_i facings, men antas å gjelde
lineært ned til kolli-gulvet.

Curhans space-elasticity (s = α · x^β, β<1) gir i stedet en konkav kurve som
kalibreres s(c_i) = mean_sales og predikerer høyere salg ved x < c_i.
Dette har størst konsekvens for SKUer som v3 krymper til kolli-gulv (A3, A4).

Analyse:
  1. Figur — produktivitetskurver for A1, A3, A4, A6 (v2 / v3 / Curhan)
  2. Post-hoc — salg ved v3-S2-allokering under Curhan
  3. LP-optimal under Curhan-produktivitet (piecewise linearisert)

Kjøring:
  cd "006 analysis"
  uv run python aktiviteter/3_5_analyse_og_resultater/scripts/12_produktivitet_curhan.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pulp

REPO_ROOT = Path(__file__).resolve().parents[4]
INTERN_DATA_DIR = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_3_casebeskrivelse_og_datainnsamling" / "resultat" / "intern"
)
CLEAN_PARQUET = INTERN_DATA_DIR / "salg_renset.parquet"
NAVNEREGISTER = INTERN_DATA_DIR / "navneregister.csv"
V3_S2_CSV = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_4_data_metode_og_modellering" / "resultat"
    / "v3_allokering_V3_S2_primaer_sek.csv"
)
FIG_DIR = Path(__file__).resolve().parents[1] / "figurer"
RESULT_DIR = Path(__file__).resolve().parents[1] / "resultat"

sys.path.insert(0, str(REPO_ROOT / "006 analysis"))
from anonymisering import Anonymizer  # noqa: E402
from margin_mapping import margin_for_product, brand_for_product  # noqa: E402

plt.rcParams.update({
    "figure.figsize": (12, 8),
    "figure.dpi": 110,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 10,
})

BETA = 0.5
BETA_SWEEP = [0.3, 0.5, 0.7]
K_BETA_V3 = 0.5
OVERSERVE_FACTOR = 2.0
SECONDARY_BUDGET = 3
SECONDARY_K = 1.5


# =====================================================================
# DATA
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


def compute_demand_cap_uniform(stats: pd.DataFrame, factor: float) -> pd.Series:
    """Anvend over-serve-faktor på ALLE SKUer (også util<1).
    Brukes for å teste hvor mye av A4-kollapsen som skyldes d_i = mean_sales."""
    return stats["mean_sales"] * factor


def compute_x_min(stats: pd.DataFrame, x_min_facings: int = 3) -> pd.Series:
    return (stats["dybde"] * x_min_facings).astype(int)


# =====================================================================
# PRODUKTIVITETSFUNKSJONER
# =====================================================================
def v2_sales(x: float, productivity: float) -> float:
    return productivity * x


def v3_sales(x: float, c_i: float, productivity: float,
             k_beta: float = K_BETA_V3) -> float:
    if x <= c_i:
        return productivity * x
    return productivity * c_i + k_beta * productivity * (x - c_i)


def curhan_sales(x: float, c_i: float, mean_sales: float,
                 beta: float = BETA) -> float:
    if x <= 0:
        return 0.0
    return mean_sales * (x / c_i) ** beta


# =====================================================================
# FIGUR — produktivitetskurver
# =====================================================================
def plot_productivity_curves(stats: pd.DataFrame, demand: pd.Series,
                              real_skus: list[str], anon: Anonymizer,
                              path: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axes = axes.flatten()
    for ax, sku in zip(axes, real_skus):
        c_i = stats.loc[sku, "facings"]
        ms = stats.loc[sku, "mean_sales"]
        rho = stats.loc[sku, "productivity"]
        d_i = demand[sku]
        x_max = max(3 * c_i, 250)
        xs = np.linspace(1, x_max, 200)
        v2 = [min(v2_sales(x, rho), d_i) for x in xs]
        v3 = [min(v3_sales(x, c_i, rho), d_i) for x in xs]
        cur = [min(curhan_sales(x, c_i, ms), d_i) for x in xs]
        ax.plot(xs, v2, label="v2 lineær (ρ konstant)", color="#9DB4C0",
                linestyle="--", linewidth=1.5)
        ax.plot(xs, v3, label="v3 piecewise (knekk ved c_i)", color="#2E86AB",
                linewidth=2)
        ax.plot(xs, cur, label=f"Curhan β={BETA}", color="#E63946", linewidth=2)
        ax.axvline(c_i, color="black", linestyle=":", alpha=0.5)
        ax.axhline(ms, color="gray", linestyle=":", alpha=0.4)
        ax.axhline(d_i, color="orange", linestyle=":", alpha=0.5,
                   label=f"d_i = {d_i:.0f}")
        # Marker dagens punkt
        ax.scatter([c_i], [ms], color="black", zorder=5, s=40,
                   label=f"Nå: ({int(c_i)}, {ms:.0f})")
        ax.set_xlabel("Hylleenheter x_i")
        ax.set_ylabel("Antatt salg s_i(x)")
        ax.set_title(
            f"{anon.pseudo(sku)} — {sku}\n"
            f"ρ = {rho:.2f}, util = {stats.loc[sku, 'utilization']:.2f}",
            fontsize=9,
        )
        ax.legend(fontsize=8, loc="lower right")
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
    fig.suptitle(
        "Produktivitetsantakelser: v2 lineær vs v3 piecewise vs Curhan β=0.5",
        fontsize=13, fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# POST-HOC — Curhan-salg ved v3-S2-allokering
# =====================================================================
def post_hoc_at_v3(stats: pd.DataFrame, demand: pd.Series,
                   v3_alloc: pd.DataFrame, anon: Anonymizer) -> pd.DataFrame:
    rows = []
    for sku in stats.index:
        x = int(v3_alloc.loc[sku, "facings_optimal"])
        c_i = stats.loc[sku, "facings"]
        ms = stats.loc[sku, "mean_sales"]
        rho = stats.loc[sku, "productivity"]
        d_i = demand[sku]
        margin = stats.loc[sku, "margin"]
        v3_pred = min(v3_sales(x, c_i, rho), d_i)
        cur_pred = min(curhan_sales(x, c_i, ms), d_i)
        rows.append({
            "SKU": anon.pseudo(sku),
            "merke": stats.loc[sku, "brand"],
            "facings_nå": int(c_i),
            "facings_v3": x,
            "salg_v3": round(v3_pred, 1),
            "salg_curhan": round(cur_pred, 1),
            "diff": round(cur_pred - v3_pred, 1),
            "margin": margin,
            "diff_margin": round((cur_pred - v3_pred) * margin, 2),
        })
    return pd.DataFrame(rows).set_index("SKU").sort_index()


# =====================================================================
# LP UNDER CURHAN — piecewise linearisert
# =====================================================================
def build_curhan_segments(c_i: int, mean_sales: float, x_min: int,
                          beta: float = BETA) -> list[tuple[int, int, float]]:
    """Returner segmenter (lower, width, slope) for piecewise linearisering
    av s(x) = mean_sales · (x/c_i)^β. Breakpoints velges som heltall ≥ x_min."""
    bps = sorted({x_min, max(x_min, c_i // 2),
                  c_i, int(1.5 * c_i),
                  2 * c_i, 3 * c_i})
    bps = [b for b in bps if b >= x_min]
    if bps[0] != x_min:
        bps = [x_min, *bps]
    bps = sorted(set(bps))
    segs = []
    for i in range(len(bps) - 1):
        lo, hi = bps[i], bps[i + 1]
        width = hi - lo
        if width <= 0:
            continue
        slope = (curhan_sales(hi, c_i, mean_sales, beta)
                 - curhan_sales(lo, c_i, mean_sales, beta)) / width
        segs.append((lo, width, slope))
    return segs


def solve_curhan_lp(stats: pd.DataFrame, demand: pd.Series, x_min: pd.Series,
                    total_capacity: int,
                    secondary_budget: int = SECONDARY_BUDGET,
                    secondary_k: float = SECONDARY_K,
                    beta: float = BETA) -> dict:
    prods = list(stats.index)
    m = pulp.LpProblem("curhan", pulp.LpMaximize)

    segments_by_p = {}
    sigma = {}
    for p in prods:
        c_i = int(stats.loc[p, "facings"])
        ms = float(stats.loc[p, "mean_sales"])
        xm = int(x_min[p])
        segs = build_curhan_segments(c_i, ms, xm, beta)
        segments_by_p[p] = segs
        sigma[p] = [
            pulp.LpVariable(f"sig_{p}_{k}", lowBound=0, upBound=seg[1],
                            cat="Integer")
            for k, seg in enumerate(segs)
        ]

    y = {p: pulp.LpVariable(f"y_{p}", lowBound=0) for p in prods}
    s_sec = {p: pulp.LpVariable(f"s_{p}", lowBound=0, cat="Integer")
             for p in prods}

    # Total kapasitet = sum(x_min) + sum(sigma)
    total_xmin = int(x_min.sum())
    m += (pulp.lpSum(sigma[p][k] for p in prods for k in range(len(sigma[p])))
          == total_capacity - total_xmin), "primaer_kap"

    m += pulp.lpSum(s_sec[p] for p in prods) <= secondary_budget, "sekundaer_kap"

    for p in prods:
        c_i = int(stats.loc[p, "facings"])
        ms = float(stats.loc[p, "mean_sales"])
        rho = float(stats.loc[p, "productivity"])
        xm = int(x_min[p])
        s_at_xmin = curhan_sales(xm, c_i, ms, beta)
        segs = segments_by_p[p]
        prod_expr = s_at_xmin + pulp.lpSum(
            seg[2] * sigma[p][k] for k, seg in enumerate(segs)
        )
        prod_expr = prod_expr + secondary_k * rho * s_sec[p]
        m += y[p] <= prod_expr, f"prod_cap_{p}"
        m += y[p] <= demand[p], f"demand_cap_{p}"

    m += pulp.lpSum(stats.loc[p, "margin"] * y[p] for p in prods)

    m.solve(pulp.PULP_CBC_CMD(msg=False))

    rows = []
    for p in prods:
        xm = int(x_min[p])
        x_total = xm + sum(int(round(sigma[p][k].value()))
                           for k in range(len(sigma[p])))
        rows.append({
            "facings_original": int(stats.loc[p, "facings"]),
            "facings_min": xm,
            "facings_optimal": x_total,
            "delta_facings": x_total - int(stats.loc[p, "facings"]),
            "secondary_optimal": int(round(s_sec[p].value())),
            "sales_original": round(stats.loc[p, "mean_sales"], 1),
            "sales_optimal": round(y[p].value(), 1),
            "demand_cap": round(demand[p], 1),
            "margin": stats.loc[p, "margin"],
            "brand": stats.loc[p, "brand"],
        })
    per_product = pd.DataFrame(rows, index=prods)

    return {
        "status": pulp.LpStatus[m.status],
        "objective": pulp.value(m.objective),
        "per_product": per_product,
    }


# =====================================================================
# RAPPORT
# =====================================================================
def margin_weighted(sales: pd.Series, margin: pd.Series) -> float:
    return float((sales * margin).sum())


def write_report(stats: pd.DataFrame, baseline_margin: float,
                 posthoc_df: pd.DataFrame,
                 curhan_lp: dict,
                 curhan_relaxed: dict,
                 beta_sweep: pd.DataFrame,
                 anon: Anonymizer,
                 path: Path) -> None:
    lines: list[str] = []
    lines.append("# Produktivitet under c_i — Curhan vs v3-piecewise")
    lines.append("")
    lines.append(f"Baseline margin-vektet salg: **{baseline_margin:.1f}**.")
    lines.append("")
    lines.append("## Antakelse")
    lines.append("")
    lines.append("v3-modellen bruker konstant produktivitet ρ_i = mean_sales_i / c_i "
                 "opp til c_i, deretter k_β · ρ_i over c_i. ρ_i er målt VED c_i, "
                 "men antas lineært under c_i — i strid med Curhans empiri.")
    lines.append("")
    lines.append(f"Curhans space-elasticity (s = α · x^β, β<1) gir konkav kurve. "
                 f"Kalibrert s(c_i) = mean_sales: α_i = mean_sales_i / c_i^β. "
                 f"Vi bruker β = {BETA}.")
    lines.append("")

    v3_total = margin_weighted(posthoc_df["salg_v3"], posthoc_df["margin"])
    cur_total = margin_weighted(posthoc_df["salg_curhan"], posthoc_df["margin"])
    lines.append("## Post-hoc evaluering av v3-S2-allokering")
    lines.append("")
    lines.append("Salg ved samme allokering, evaluert under begge produktivitetsantakelser:")
    lines.append("")
    lines.append("| Produktivitetsantakelse | Margin-vektet salg | Δ vs baseline |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Baseline (dagens allokering, observert) | {baseline_margin:.1f} | — |")
    lines.append(f"| v3 piecewise (ρ konstant under c_i) | {v3_total:.1f} | "
                 f"+{100*(v3_total-baseline_margin)/baseline_margin:.1f}% |")
    lines.append(f"| Curhan β={BETA} (konkav) | {cur_total:.1f} | "
                 f"+{100*(cur_total-baseline_margin)/baseline_margin:.1f}% |")
    lines.append("")

    movers = posthoc_df.copy()
    movers["abs_diff"] = movers["diff"].abs()
    movers = movers.sort_values("abs_diff", ascending=False).head(10)
    lines.append("**Topp 10 SKUer der antakelsene divergerer (sortert |Δ|):**")
    lines.append("")
    lines.append("| SKU | Merke | Facings v3 | Salg v3 | Salg Curhan | Δ salg | Δ margin |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for sku, r in movers.iterrows():
        lines.append(
            f"| {sku} | {r['merke']} | {int(r['facings_v3'])} | "
            f"{r['salg_v3']:.1f} | {r['salg_curhan']:.1f} | "
            f"{r['diff']:+.1f} | {r['diff_margin']:+.2f} |"
        )
    lines.append("")
    lines.append("## LP-optimal under Curhan-produktivitet")
    lines.append("")
    cur_obj = curhan_lp["objective"]
    cur_pct = 100 * (cur_obj - baseline_margin) / baseline_margin
    lines.append(f"- Solver-status: **{curhan_lp['status']}**")
    lines.append(f"- LP-margin: **{cur_obj:.1f}**  (+{cur_pct:.1f}% vs baseline)")
    lines.append(
        f"- Sammenligning: v3-S2 ga **+24.3 %**. LP under Curhan gir "
        f"**+{cur_pct:.1f} %** under samme totalbudsjett og sekundærplasser."
    )
    lines.append("")
    pp = curhan_lp["per_product"].copy()
    pp.index = [anon.pseudo(p) for p in pp.index]
    pp = pp.sort_index()
    lines.append("### Allokering per SKU under Curhan-LP")
    lines.append("")
    lines.append("| SKU | Merke | Marg | Nå | Optimal | Δ | Sek | Salg nå | Salg ny |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for sku, r in pp.iterrows():
        lines.append(
            f"| {sku} | {r['brand']} | {r['margin']:.0%} | "
            f"{int(r['facings_original'])} | {int(r['facings_optimal'])} | "
            f"{int(r['delta_facings']):+d} | {int(r['secondary_optimal'])} | "
            f"{r['sales_original']:.1f} | {r['sales_optimal']:.1f} |"
        )
    lines.append("")
    # SENSITIVITET 1 — relaxed demand cap
    lines.append("## Sensitivitet 1 — relaxed demand cap")
    lines.append("")
    lines.append(
        "Kjør Curhan-LP med d_i = 2·mean_sales for ALLE SKUer (også util<1). "
        "Tester hvor mye av A4-kollapsen som skyldes antakelsen d_i = mean_sales "
        "for under-utiliserte SKUer."
    )
    lines.append("")
    rel_obj = curhan_relaxed["objective"]
    rel_pct = 100 * (rel_obj - baseline_margin) / baseline_margin
    lines.append(f"- LP-margin (relaxed demand): **{rel_obj:.1f}**  (+{rel_pct:.1f}% vs baseline)")
    lines.append("")
    pp_rel = curhan_relaxed["per_product"].copy()
    pp_rel.index = [anon.pseudo(p) for p in pp_rel.index]
    pp_rel = pp_rel.sort_index()
    # Sammenlign A3, A4 spesielt
    lines.append("**Endring i A3/A4-allokering under relaxed demand:**")
    lines.append("")
    lines.append("| SKU | Nå | v3-S2 | Curhan (orig d_i) | Curhan (relaxed d_i) |")
    lines.append("|---|---:|---:|---:|---:|")
    pp_orig = curhan_lp["per_product"].copy()
    pp_orig.index = [anon.pseudo(p) for p in pp_orig.index]
    for sku in ["A3", "A4"]:
        nå = int(pp_orig.loc[sku, "facings_original"])
        cur_orig = int(pp_orig.loc[sku, "facings_optimal"])
        cur_rel = int(pp_rel.loc[sku, "facings_optimal"])
        lines.append(f"| {sku} | {nå} | 21 | {cur_orig} | {cur_rel} |")
    lines.append("")

    # SENSITIVITET 2 — β-sweep
    lines.append("## Sensitivitet 2 — β-sweep")
    lines.append("")
    lines.append(
        f"Curhan-LP med β ∈ {BETA_SWEEP}. β=1 ville gjøre Curhan-kurven "
        "lineær (samme som v2). β=0 ville gjøre den flat (ingen marginal-avkastning)."
    )
    lines.append("")
    lines.append("| β | LP-margin | Gevinst | Gev % |")
    lines.append("|---:|---:|---:|---:|")
    for _, r in beta_sweep.iterrows():
        gain = r["lp_margin"] - baseline_margin
        pct = 100 * gain / baseline_margin
        lines.append(
            f"| {r['beta']:.2f} | {r['lp_margin']:.1f} | "
            f"+{gain:.1f} | +{pct:.1f}% |"
        )
    lines.append("")

    lines.append("## Tolkning")
    lines.append("")
    lines.append(
        "v3-modellen behandler produktiviteten asymmetrisk: avtakende avkastning "
        "over c_i (k_β = 0.5), men konstant slope under c_i. Curhans empiri "
        "støtter ikke denne asymmetrien — slope bør falle på begge sider av c_i."
    )
    lines.append("")
    lines.append(
        "Post-hoc-evalueringen viser hvor mye av v3-S2-løftet som er en *prediksjons-"
        "feil*, ikke et reelt løft. LP-resultatet under Curhan viser hvor mye "
        "modellen forutsier som realiserbart med riktig produktivitetsantakelse "
        "OG riktig allokering."
    )
    lines.append("")
    lines.append(
        "Sensitivitet 1 (relaxed demand) avklarer rollen til demand-cap-antakelsen: "
        "hvis vi tror under-utiliserte SKUer kan vokse, endres A4-anbefalingen "
        "kvalitativt. Det betyr at A4-kollapsen i v3 og baseline Curhan-LP er "
        "mer et resultat av demand-cap-antakelsen enn av produktivitetskurven."
    )
    lines.append("")
    lines.append(
        "Sensitivitet 2 (β-sweep) viser robustheten av Curhan-LP-resultatet. "
        "Ved β=0.3 (mer aggressiv avtaking) faller gevinsten; ved β=0.7 "
        "(nesten lineær) nærmer resultatet seg v3-tallet."
    )
    path.write_text("\n".join(lines), encoding="utf-8")


# =====================================================================
# MAIN
# =====================================================================
def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CLEAN_PARQUET)
    anon = Anonymizer.load(NAVNEREGISTER)
    stats = aggregate(df)
    total_capacity = int(stats["facings"].sum())
    demand = compute_demand_cap(stats, OVERSERVE_FACTOR)
    x_min = compute_x_min(stats)
    baseline_margin = margin_weighted(stats["mean_sales"], stats["margin"])

    print("=== CURHAN VS V3-PIECEWISE PRODUKTIVITET ===")
    print(f"Total primær kapasitet: {total_capacity}")
    print(f"SKUer: {len(stats)}")
    print(f"Baseline margin: {baseline_margin:.1f}")
    print()

    # Last v3-S2 allokering (anonymisert CSV → mappe tilbake til reelle navn)
    v3_anon = pd.read_csv(V3_S2_CSV, index_col=0)
    pseudo_to_real = {anon.pseudo(p): p for p in stats.index}
    v3_alloc = v3_anon.copy()
    v3_alloc.index = [pseudo_to_real[p] for p in v3_anon.index]

    # Velg SKUer å plotte
    real_for_pseudo = {anon.pseudo(p): p for p in stats.index}
    skus_to_plot = [real_for_pseudo[p] for p in ("A1", "A3", "A4", "A6")]

    # 1) Figur
    fig_path = FIG_DIR / "fig_produktivitet_curhan.png"
    plot_productivity_curves(stats, demand, skus_to_plot, anon, fig_path)
    print(f"Figur: {fig_path}")

    # 2) Post-hoc
    posthoc = post_hoc_at_v3(stats, demand, v3_alloc, anon)
    posthoc.to_csv(RESULT_DIR / "tab_curhan_posthoc.csv")
    v3_total = margin_weighted(posthoc["salg_v3"], posthoc["margin"])
    cur_total = margin_weighted(posthoc["salg_curhan"], posthoc["margin"])
    print(f"\nPost-hoc ved v3-S2-allokering:")
    print(f"  v3 forutsigelse:     {v3_total:.1f} "
          f"(+{100*(v3_total-baseline_margin)/baseline_margin:.1f}%)")
    print(f"  Curhan forutsigelse: {cur_total:.1f} "
          f"(+{100*(cur_total-baseline_margin)/baseline_margin:.1f}%)")
    print(f"  Predikssjonsdiff:    {cur_total - v3_total:+.1f} margin-enheter")

    # 3) LP under Curhan (baseline d_i)
    curhan_lp = solve_curhan_lp(stats, demand, x_min, total_capacity)
    cur_pct = 100 * (curhan_lp["objective"] - baseline_margin) / baseline_margin
    print(f"\nLP under Curhan β={BETA} (baseline d_i):")
    print(f"  Status:  {curhan_lp['status']}")
    print(f"  Margin:  {curhan_lp['objective']:.1f} (+{cur_pct:.1f}%)")
    print(f"  Vs v3-S2 (+24.3%): {cur_pct - 24.3:+.1f} pp differanse")

    # 4) Sensitivitet 1 — relaxed demand (alle SKUer får 2× over-serve)
    demand_relaxed = compute_demand_cap_uniform(stats, OVERSERVE_FACTOR)
    curhan_relaxed = solve_curhan_lp(stats, demand_relaxed, x_min, total_capacity)
    rel_pct = 100 * (curhan_relaxed["objective"] - baseline_margin) / baseline_margin
    print(f"\nLP under Curhan β={BETA} (relaxed d_i = 2·mean for alle):")
    print(f"  Margin:  {curhan_relaxed['objective']:.1f} (+{rel_pct:.1f}%)")
    pp_rel = curhan_relaxed["per_product"]
    print(f"  A3 allokering: {int(pp_rel.loc[next(p for p in stats.index if anon.pseudo(p) == 'A3'), 'facings_optimal'])}")
    print(f"  A4 allokering: {int(pp_rel.loc[next(p for p in stats.index if anon.pseudo(p) == 'A4'), 'facings_optimal'])}")

    # 5) Sensitivitet 2 — β-sweep
    beta_rows = []
    print(f"\nβ-sweep (baseline d_i):")
    for b in BETA_SWEEP:
        res = solve_curhan_lp(stats, demand, x_min, total_capacity, beta=b)
        pct = 100 * (res["objective"] - baseline_margin) / baseline_margin
        beta_rows.append({"beta": b, "lp_margin": res["objective"], "gain_pct": pct})
        print(f"  β={b}: margin {res['objective']:.1f} (+{pct:.1f}%)")
    beta_sweep_df = pd.DataFrame(beta_rows)
    beta_sweep_df.to_csv(RESULT_DIR / "tab_curhan_beta_sweep.csv", index=False)

    # Rapport
    rep_path = RESULT_DIR / "produktivitet_curhan_rapport.md"
    write_report(stats, baseline_margin, posthoc, curhan_lp, curhan_relaxed,
                 beta_sweep_df, anon, rep_path)
    print(f"\nRapport: {rep_path}")

    # CSV av Curhan-LP-allokeringen (baseline + relaxed)
    pp = curhan_lp["per_product"].copy()
    pp.index = [anon.pseudo(p) for p in pp.index]
    pp = pp.sort_index()
    pp.to_csv(RESULT_DIR / "tab_curhan_lp_allokering.csv")

    pp_rel_out = curhan_relaxed["per_product"].copy()
    pp_rel_out.index = [anon.pseudo(p) for p in pp_rel_out.index]
    pp_rel_out = pp_rel_out.sort_index()
    pp_rel_out.to_csv(RESULT_DIR / "tab_curhan_lp_allokering_relaxed.csv")


if __name__ == "__main__":
    main()
