#!/usr/bin/env python3
"""
ACT-3.5.6 Bootstrap-KI for V3-modellen (stykkevis lineær produktivitet).

Som 10_bootstrap.py, men kjører V3-S2 (k_β = 0.5) per iterasjon i stedet for
v2-S2. Gir 95 %-konfidensbånd på den reviderte gevinstanslaget.

Kjøring (~30 s):
  cd "006 analysis"
  uv run python aktiviteter/3_5_analyse_og_resultater/scripts/11_bootstrap_piecewise.py
"""

from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[4]
INTERN_DATA_DIR = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_3_casebeskrivelse_og_datainnsamling" / "resultat" / "intern"
)
CLEAN_PARQUET = INTERN_DATA_DIR / "salg_renset.parquet"
LP_SCRIPT = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_4_data_metode_og_modellering" / "scripts" / "11_lp_piecewise.py"
)
FIG_DIR = Path(__file__).resolve().parents[1] / "figurer"
FIG_INTERN = FIG_DIR / "intern"
RESULT_DIR = Path(__file__).resolve().parents[1] / "resultat"
RESULT_INTERN = RESULT_DIR / "intern"

sys.path.insert(0, str(REPO_ROOT / "006 analysis"))

spec = importlib.util.spec_from_file_location("lp_piecewise", LP_SCRIPT)
lp_pw = importlib.util.module_from_spec(spec)
sys.modules["lp_piecewise"] = lp_pw
spec.loader.exec_module(lp_pw)

B = 1000
SEED = 42
SCENARIO_KEY = "V3_S2_primaer_sek"


def aggregate_with_fallback(df_b: pd.DataFrame,
                            stats_full: pd.DataFrame) -> pd.DataFrame:
    stats_b = lp_pw.aggregate(df_b)
    missing = set(stats_full.index) - set(stats_b.index)
    if missing:
        stats_b = pd.concat([stats_b, stats_full.loc[sorted(missing)]])
    return stats_b.loc[stats_full.index]


def run_iter(df, stats_full, weeks, scenario, rng):
    sampled = rng.choice(weeks, size=len(weeks), replace=True)
    parts = [df[df["UkeNr"] == w] for w in sampled]
    df_b = pd.concat(parts, ignore_index=True)
    stats_b = aggregate_with_fallback(df_b, stats_full)
    total_cap = int(stats_b["facings"].sum())
    baseline_margin = float((stats_b["mean_sales"] * stats_b["margin"]).sum())
    baseline_volume = float(stats_b["mean_sales"].sum())
    demand = lp_pw.compute_demand_cap(stats_b, scenario.overserve_factor)
    x_min = lp_pw.compute_x_min(stats_b, scenario)
    res = lp_pw.solve_piecewise(stats_b, demand, x_min, scenario, total_cap)
    lp_margin = res["objective"]
    lp_volume = float(res["per_product"]["sales_optimal"].sum())
    return {
        "baseline_margin": baseline_margin,
        "lp_margin": lp_margin,
        "baseline_volume": baseline_volume,
        "lp_volume": lp_volume,
        "gain_pct": 100 * (lp_margin - baseline_margin) / baseline_margin,
        "vol_gain_pct": 100 * (lp_volume - baseline_volume) / baseline_volume,
        "n_unique_weeks": int(pd.unique(sampled).size),
    }


def percentiles(values):
    qs = [2.5, 5, 25, 50, 75, 95, 97.5]
    out = {f"p{q}": float(np.percentile(values, q)) for q in qs}
    out["mean"] = float(values.mean())
    out["std"] = float(values.std(ddof=1))
    return out


def plot_distribution(gains, point_estimate, path, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(gains, bins=40, color="#2E86AB", edgecolor="white", alpha=0.85)
    p2_5, p50, p97_5 = np.percentile(gains, [2.5, 50, 97.5])
    ax.axvline(point_estimate, color="#E63946", linewidth=2,
               label=f"Punktestimat (full data): {point_estimate:.1f}%")
    ax.axvline(p50, color="#1B5E7E", linewidth=2, linestyle="--",
               label=f"Median: {p50:.1f}%")
    ax.axvspan(p2_5, p97_5, color="#9DB4C0", alpha=0.25,
               label=f"95% bånd: [{p2_5:.1f}%, {p97_5:.1f}%]")
    ax.set_xlabel("Margin-gevinst over baseline (%)")
    ax.set_ylabel("Antall bootstrap-iterasjoner")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def build_report(gain_stats, vol_stats, margin_stats,
                 point_estimate, vol_point_estimate, B_actual, unique_mean):
    lines = []
    lines.append("# Bootstrap-KI for V3-S2 (stykkevis lineær)")
    lines.append("")
    lines.append(f"Empirisk fordeling av margin- og volum-gevinst i V3-S2 over "
                 f"**B = {B_actual} bootstrap-iterasjoner**, med k_β = 0.5. "
                 "Hver iterasjon resampler de 10 ukene med tilbakelegging og "
                 "kjører V3-S2 LP-modellen på det re-aggregerte datagrunnlaget.")
    lines.append("")
    lines.append(f"Gjennomsnittlig antall unike uker per iterasjon: "
                 f"**{unique_mean:.2f} av 10**.")
    lines.append("")
    lines.append("## Margin-gevinst (%)")
    lines.append("")
    lines.append("| Statistikk | Verdi |")
    lines.append("|---|---:|")
    lines.append(f"| Punktestimat (full data) | **+{point_estimate:.1f}%** |")
    lines.append(f"| Mean | +{gain_stats['mean']:.1f}% |")
    lines.append(f"| Median | +{gain_stats['p50']:.1f}% |")
    lines.append(f"| Standardavvik | {gain_stats['std']:.2f} pp |")
    lines.append(f"| 95 % konfidensbånd | "
                 f"[+{gain_stats['p2.5']:.1f}%, +{gain_stats['p97.5']:.1f}%] |")
    lines.append(f"| 90 % konfidensbånd | "
                 f"[+{gain_stats['p5']:.1f}%, +{gain_stats['p95']:.1f}%] |")
    lines.append(f"| Interkvartil (p25–p75) | "
                 f"[+{gain_stats['p25']:.1f}%, +{gain_stats['p75']:.1f}%] |")
    lines.append("")
    lines.append("## Volum-gevinst (%)")
    lines.append("")
    lines.append("| Statistikk | Verdi |")
    lines.append("|---|---:|")
    lines.append(f"| Punktestimat (full data) | **+{vol_point_estimate:.1f}%** |")
    lines.append(f"| Median | +{vol_stats['p50']:.1f}% |")
    lines.append(f"| 95 % bånd | "
                 f"[+{vol_stats['p2.5']:.1f}%, +{vol_stats['p97.5']:.1f}%] |")
    return "\n".join(lines)


def main():
    for d in (FIG_DIR, FIG_INTERN, RESULT_DIR, RESULT_INTERN):
        d.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CLEAN_PARQUET)
    weeks = np.array(sorted(df["UkeNr"].unique()))
    print(f"Bootstrap V3: B = {B}, uker = {list(weeks)}")

    stats_full = lp_pw.aggregate(df)
    total_cap_full = int(stats_full["facings"].sum())
    baseline_margin_full = float((stats_full["mean_sales"] * stats_full["margin"]).sum())
    baseline_vol_full = float(stats_full["mean_sales"].sum())

    s2 = next(s for s in lp_pw.SCENARIOS if s.key == SCENARIO_KEY)
    demand_full = lp_pw.compute_demand_cap(stats_full, s2.overserve_factor)
    x_min_full = lp_pw.compute_x_min(stats_full, s2)
    res_full = lp_pw.solve_piecewise(stats_full, demand_full, x_min_full, s2, total_cap_full)
    point_gain = 100 * (res_full["objective"] - baseline_margin_full) / baseline_margin_full
    point_vol_gain = 100 * (res_full["per_product"]["sales_optimal"].sum() - baseline_vol_full) / baseline_vol_full
    print(f"Punktestimat V3-S2: +{point_gain:.2f}% margin, +{point_vol_gain:.2f}% volum")

    rng = np.random.default_rng(SEED)
    rows = []
    t0 = time.time()
    for b in range(B):
        rows.append(run_iter(df, stats_full, weeks, s2, rng))
        if (b + 1) % 100 == 0:
            elapsed = time.time() - t0
            print(f"  {b+1}/{B}  {elapsed:.1f}s")
    print(f"Ferdig på {time.time() - t0:.1f}s.")

    boot = pd.DataFrame(rows)
    boot.to_csv(RESULT_DIR / "v3_bootstrap_gevinst.csv", index=False)
    boot.to_csv(RESULT_INTERN / "v3_bootstrap_gevinst.csv", index=False)

    gains = boot["gain_pct"].to_numpy()
    vol_gains = boot["vol_gain_pct"].to_numpy()
    lp_margins = boot["lp_margin"].to_numpy()

    gain_stats = percentiles(gains)
    vol_stats = percentiles(vol_gains)
    margin_stats = percentiles(lp_margins)

    pd.DataFrame({
        "metric": ["margin_gain_pct", "vol_gain_pct", "lp_margin"],
        **{k: [gain_stats[k], vol_stats[k], margin_stats[k]] for k in gain_stats},
    }).to_csv(RESULT_DIR / "v3_bootstrap_percentiler.csv", index=False)

    report = build_report(gain_stats, vol_stats, margin_stats,
                          point_gain, point_vol_gain, B,
                          float(boot["n_unique_weeks"].mean()))
    (RESULT_DIR / "v3_bootstrap_rapport.md").write_text(report, encoding="utf-8")
    (RESULT_INTERN / "v3_bootstrap_rapport.md").write_text(report, encoding="utf-8")

    plot_distribution(gains, point_gain,
                      FIG_DIR / "v3_bootstrap_distribusjon.png",
                      title=f"Bootstrap-fordeling av V3-S2 margin-gevinst (k_β=0.5, B={B})")
    plot_distribution(gains, point_gain,
                      FIG_INTERN / "v3_bootstrap_distribusjon.png",
                      title=f"Bootstrap-fordeling av V3-S2 margin-gevinst (k_β=0.5, B={B})")

    print()
    print(f"95% bånd: [+{gain_stats['p2.5']:.1f}%, +{gain_stats['p97.5']:.1f}%]")
    print(f"Median:   +{gain_stats['p50']:.1f}%")


if __name__ == "__main__":
    main()
