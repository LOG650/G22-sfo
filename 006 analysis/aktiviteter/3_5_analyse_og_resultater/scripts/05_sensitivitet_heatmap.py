#!/usr/bin/env python3
"""
ACT-3.5 Sensitivitets-heatmap (2D).

Kjører LP-modellen over et 2D-rutenett (overserve_factor × x_min_fraction)
og produserer en seaborn-heatmap som viser margin-vektet salg.

Erstatter de to 1D-figurene med ett bilde som viser begge dimensjonene
samtidig — bedre for §7.3.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pulp
import seaborn as sns

REPO_ROOT = Path(__file__).resolve().parents[4]
INTERN_DATA_DIR = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_3_casebeskrivelse_og_datainnsamling" / "resultat" / "intern"
)
CLEAN_PARQUET = INTERN_DATA_DIR / "salg_renset.parquet"
FIG_DIR = Path(__file__).resolve().parents[1] / "figurer"

sys.path.insert(0, str(REPO_ROOT / "006 analysis"))
from margin_mapping import margin_for_product  # noqa: E402

plt.rcParams.update({
    "figure.dpi": 110,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
})


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("Produkt").agg(
        mean_sales=("Ant_solgt", "mean"),
        facings=("Kapasitet", "first"),
    )
    g["productivity"] = g["mean_sales"] / g["facings"]
    g["utilization"] = g["mean_sales"] / g["facings"]
    g["margin"] = [margin_for_product(p) for p in g.index]
    return g


def solve_one(stats: pd.DataFrame, overserve: float, x_min_frac: float,
              total_cap: int) -> tuple[float, float]:
    prods = list(stats.index)
    demand = stats["mean_sales"].copy()
    over = stats["utilization"] >= 1.0
    demand[over] = stats.loc[over, "mean_sales"] * overserve

    floor = stats["facings"].apply(lambda c: max(3, int(c * x_min_frac)))

    m = pulp.LpProblem("sens", pulp.LpMaximize)
    x = {p: pulp.LpVariable(f"x_{p}", lowBound=int(floor[p]), cat="Integer")
         for p in prods}
    y = {p: pulp.LpVariable(f"y_{p}", lowBound=0) for p in prods}
    m += pulp.lpSum(stats.loc[p, "margin"] * y[p] for p in prods)
    m += pulp.lpSum(x[p] for p in prods) == total_cap
    for p in prods:
        rho = stats.loc[p, "productivity"]
        m += y[p] <= rho * x[p]
        m += y[p] <= demand[p]
    m.solve(pulp.PULP_CBC_CMD(msg=False))
    margin_obj = float(pulp.value(m.objective))
    volume = float(sum(y[p].value() for p in prods))
    return margin_obj, volume


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(CLEAN_PARQUET)
    stats = aggregate(df)
    total_cap = int(stats["facings"].sum())
    baseline_margin = float((stats["mean_sales"] * stats["margin"]).sum())
    baseline_volume = float(stats["mean_sales"].sum())

    overserve_grid = [1.25, 1.50, 1.75, 2.00, 2.50, 3.00]
    xmin_grid = [0.00, 0.10, 0.25, 0.40, 0.50, 0.60, 0.80]

    margin_pct = np.zeros((len(xmin_grid), len(overserve_grid)))
    volume_pct = np.zeros((len(xmin_grid), len(overserve_grid)))

    for i, xmin in enumerate(xmin_grid):
        for j, ov in enumerate(overserve_grid):
            obj_m, obj_v = solve_one(stats, ov, xmin, total_cap)
            margin_pct[i, j] = 100 * (obj_m - baseline_margin) / baseline_margin
            volume_pct[i, j] = 100 * (obj_v - baseline_volume) / baseline_volume
            print(f"  xmin={xmin:.2f} ov={ov:.2f} → margin {obj_m:.1f} "
                  f"({margin_pct[i,j]:+.1f}%)")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    for ax, data, title in (
        (axes[0], margin_pct, "Margin-vektet gevinst (%)"),
        (axes[1], volume_pct, "Volum-gevinst (%)"),
    ):
        sns.heatmap(
            data,
            annot=True, fmt=".1f", cmap="YlGnBu",
            xticklabels=[f"{v:.2f}" for v in overserve_grid],
            yticklabels=[f"{v:.2f}" for v in xmin_grid],
            ax=ax, cbar_kws={"label": "% over baseline"},
        )
        ax.set_xlabel("overserve_factor (etterspørsels-multiplikator)")
        ax.set_ylabel("x_min_fraction (sortimentsgulv)")
        ax.set_title(title)
        # Marker S2-punktet
        s2_x = overserve_grid.index(2.00) + 0.5
        s2_y = xmin_grid.index(0.25) + 0.5
        ax.plot(s2_x, s2_y, marker="o", markersize=14, markerfacecolor="none",
                markeredgecolor="red", markeredgewidth=2.2)
    fig.suptitle("Sensitivitet — to-dimensjonalt rutenett (S2-punkt markert i rødt)",
                 fontsize=12, y=1.02)
    fig.tight_layout()
    out = FIG_DIR / "sensitivitet_2d_heatmap.png"
    fig.savefig(out, bbox_inches="tight", dpi=130)
    plt.close(fig)
    print(f"\nLagret: {out}")


if __name__ == "__main__":
    main()
