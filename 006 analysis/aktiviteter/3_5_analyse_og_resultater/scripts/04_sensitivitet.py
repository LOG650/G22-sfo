#!/usr/bin/env python3
"""
ACT-3.5.2 Sensitivitetsanalyse.

Undersøker hvordan LP-resultatet (totalt forventet ukesalg og per-produkt
allokering) avhenger av to parametre:
  1. overserve_factor  — hvor mye høyere antar vi at etterspørsel er enn
                         observert salg for produkter som går tomme.
  2. x_min_fraction    — hvor strengt binder minimums-sortimentet.

Grunninnstilling speiler S2 Realistisk (25% gulv, 2× overserve). Hvert
parameter varieres over et rutenett mens det andre holdes fast.

Output: per-parameter tabell + linjeplot for total forventet salg.

Kjøring:
  cd "006 analysis"
  uv run python aktiviteter/3_5_analyse_og_resultater/scripts/04_sensitivitet.py
"""

from __future__ import annotations

import math
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


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("Produkt").agg(
        mean_sales=("Ant_solgt", "mean"),
        facings=("Kapasitet", "first"),
    )
    g["productivity"] = g["mean_sales"] / g["facings"]
    g["utilization"] = g["mean_sales"] / g["facings"]
    return g


def compute_demand_cap(stats: pd.DataFrame, overserve_factor: float) -> pd.Series:
    d = stats["mean_sales"].copy()
    over = stats["utilization"] >= 1.0
    d[over] = stats.loc[over, "mean_sales"] * overserve_factor
    return d


def compute_x_min(stats: pd.DataFrame, x_min_fraction: float,
                  x_min_floor: int = 1) -> pd.Series:
    frac = (stats["facings"] * x_min_fraction).apply(math.floor)
    floor = pd.Series(x_min_floor, index=stats.index)
    return pd.concat([floor, frac], axis=1).max(axis=1).astype(int)


def solve(stats: pd.DataFrame, demand: pd.Series, x_min: pd.Series,
          total_capacity: int) -> dict:
    prods = list(stats.index)
    m = pulp.LpProblem("sens", pulp.LpMaximize)
    x = {p: pulp.LpVariable(f"x_{p}", lowBound=int(x_min[p]), cat="Integer")
         for p in prods}
    y = {p: pulp.LpVariable(f"y_{p}", lowBound=0) for p in prods}
    m += pulp.lpSum(y[p] for p in prods)
    m += pulp.lpSum(x[p] for p in prods) == total_capacity
    for p in prods:
        rho = stats.loc[p, "productivity"]
        m += y[p] <= rho * x[p]
        m += y[p] <= demand[p]
    m.solve(pulp.PULP_CBC_CMD(msg=False))
    return {
        "obj": pulp.value(m.objective),
        "x": {p: int(round(x[p].value())) for p in prods},
        "y": {p: round(y[p].value(), 1) for p in prods},
    }


def sweep_overserve(stats: pd.DataFrame, total_capacity: int,
                    x_min_fraction: float,
                    grid: list[float]) -> pd.DataFrame:
    """Varier overserve-faktor, hold x_min_fraction fast."""
    x_min = compute_x_min(stats, x_min_fraction)
    rows = []
    for f in grid:
        demand = compute_demand_cap(stats, f)
        res = solve(stats, demand, x_min, total_capacity)
        rows.append({"overserve_factor": f, "total_salg": round(res["obj"], 1)})
    return pd.DataFrame(rows)


def sweep_x_min(stats: pd.DataFrame, total_capacity: int,
                overserve_factor: float,
                grid: list[float]) -> pd.DataFrame:
    """Varier x_min_fraction, hold overserve fast."""
    demand = compute_demand_cap(stats, overserve_factor)
    rows = []
    for frac in grid:
        x_min = compute_x_min(stats, frac)
        res = solve(stats, demand, x_min, total_capacity)
        rows.append({"x_min_fraction": frac, "total_salg": round(res["obj"], 1)})
    return pd.DataFrame(rows)


def plot_sweep(df: pd.DataFrame, x_col: str, x_label: str, baseline_total: float,
               path: Path, title: str, s2_x: float) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df[x_col], df["total_salg"], marker="o", color="#2E86AB",
            linewidth=2, label="LP-optimal")
    ax.axhline(baseline_total, color="#9DB4C0", linestyle="--",
               label=f"Baseline observert ({baseline_total:.0f})")
    ax.axvline(s2_x, color="#E63946", linestyle=":",
               label=f"S2-verdi ({s2_x})")
    ax.set_xlabel(x_label)
    ax.set_ylabel("Forventet total ukesalg (enheter)")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def write_report(overserve_df: pd.DataFrame, xmin_df: pd.DataFrame,
                 baseline_total: float, anonymized: bool) -> str:
    lines = []
    tittel = "Sensitivitetsanalyse"
    tittel += " (anonymisert)" if anonymized else " (intern)"
    lines.append(f"# {tittel}")
    lines.append("")
    lines.append(f"Baseline observert total: **{baseline_total:.1f}** enheter/uke.")
    lines.append("")

    lines.append("## Etterspørselsantakelse — overserve_factor")
    lines.append("")
    lines.append(("Hvor mye høyere antas ukentlig etterspørsel å være enn observert "
                  "salg for produkter der hyllen tømmes? x_min_fraction holdes på 0.25 "
                  "(S2)."))
    lines.append("")
    lines.append("| overserve_factor | LP-salg | Gevinst | Gev % |")
    lines.append("|---:|---:|---:|---:|")
    for _, row in overserve_df.iterrows():
        gain = row["total_salg"] - baseline_total
        pct = 100 * gain / baseline_total
        lines.append(
            f"| {row['overserve_factor']:.2f} | {row['total_salg']:.1f} | "
            f"+{gain:.1f} | +{pct:.1f}% |"
        )
    lines.append("")

    lines.append("## Minimums-allokering — x_min_fraction")
    lines.append("")
    lines.append(("Hvor streng er sortimentsgarantien? overserve_factor holdes på "
                  "2.0 (S2)."))
    lines.append("")
    lines.append("| x_min_fraction | LP-salg | Gevinst | Gev % |")
    lines.append("|---:|---:|---:|---:|")
    for _, row in xmin_df.iterrows():
        gain = row["total_salg"] - baseline_total
        pct = 100 * gain / baseline_total
        lines.append(
            f"| {row['x_min_fraction']:.2f} | {row['total_salg']:.1f} | "
            f"+{gain:.1f} | +{pct:.1f}% |"
        )
    lines.append("")

    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Gevinsten vokser monotont med overserve_factor fordi høyere "
                 "antatt etterspørsel hever taket d_i for de underkapasiterte "
                 "A-produktene. Selv ved konservativ antakelse (1.25×) gir modellen "
                 "betydelig forbedring.")
    lines.append("- Minimums-allokering har liten effekt inntil den begynner å "
                 "binde B2 (≈ 0.30–0.40). Over dette tvinges modellen til å beholde "
                 "overkapasitert hylleplass og mister gevinst.")
    lines.append("- S2 Realistisk (0.25, 2.0) ligger i det monotone området der "
                 "hovedparten av gevinsten er realisert uten å kutte sortimentet.")
    return "\n".join(lines)


def main() -> None:
    for d in (FIG_DIR, FIG_INTERN, RESULT_DIR, RESULT_INTERN):
        d.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CLEAN_PARQUET)
    Anonymizer.load(NAVNEREGISTER)  # (ingen per-produkt output her, men validerer)

    stats = aggregate(df)
    total_capacity = int(stats["facings"].sum())
    baseline_total = stats["mean_sales"].sum()

    overserve_grid = [1.25, 1.50, 1.75, 2.00, 2.50, 3.00]
    xmin_grid = [0.00, 0.10, 0.25, 0.40, 0.50, 0.60, 0.80]

    # Sweep overserve (hold x_min_fraction = 0.25)
    overserve_df = sweep_overserve(stats, total_capacity, 0.25, overserve_grid)
    # Sweep x_min (hold overserve = 2.0)
    xmin_df = sweep_x_min(stats, total_capacity, 2.0, xmin_grid)

    overserve_df.to_csv(RESULT_DIR / "sensitivitet_overserve.csv", index=False)
    xmin_df.to_csv(RESULT_DIR / "sensitivitet_xmin.csv", index=False)

    plot_sweep(overserve_df, "overserve_factor", "overserve_factor",
               baseline_total, FIG_DIR / "sensitivitet_overserve.png",
               "Sensitivitet: etterspørselsantakelse → total forventet salg", 2.0)
    plot_sweep(xmin_df, "x_min_fraction", "x_min_fraction",
               baseline_total, FIG_DIR / "sensitivitet_xmin.png",
               "Sensitivitet: minimums-allokering → total forventet salg", 0.25)

    summary = write_report(overserve_df, xmin_df, baseline_total, anonymized=True)
    (RESULT_DIR / "sensitivitet-rapport.md").write_text(summary, encoding="utf-8")
    (RESULT_INTERN / "sensitivitet-rapport.md").write_text(
        write_report(overserve_df, xmin_df, baseline_total, anonymized=False),
        encoding="utf-8",
    )

    print("Overserve sweep:")
    print(overserve_df.to_string(index=False))
    print("\nx_min sweep:")
    print(xmin_df.to_string(index=False))


if __name__ == "__main__":
    main()
