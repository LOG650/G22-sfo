#!/usr/bin/env python3
"""
ACT-3.4.2 Etterspørselsanalyse (deskriptiv + ABC)

Leser renset + anonymisert data fra ACT-3.3.4 og produserer pseudonym-baserte
figurer og tabeller som trygt kan deles/committes. Ekte-navn-versjoner skrives
til intern/ (gitignored).

Kjøring:
  cd "006 analysis"
  uv run python aktiviteter/3_4_data_metode_og_modellering/scripts/02_deskriptiv_og_abc.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

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


def plot_timeseries(df: pd.DataFrame, path: Path, title_suffix: str = "") -> None:
    produkter = df["Produkt"].unique()
    n = len(produkter)
    ncols = 2
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 3 * nrows), sharex=True)
    axes = axes.flatten()

    for ax, prod in zip(axes, produkter):
        sub = df[df["Produkt"] == prod].sort_values("UkeNr")
        ax.plot(sub["UkeNr"], sub["Ant_solgt"], marker="o",
                label="Salg", color="#2E86AB")
        ax.axhline(sub["Kapasitet"].iloc[0], linestyle="--", color="#E63946",
                   label="Kapasitet")
        ax.set_title(prod, fontsize=9)
        ax.set_xlabel("Ukenr")
        ax.set_ylabel("Enheter")
        ax.legend(loc="upper right", fontsize=8)
    for ax in axes[len(produkter):]:
        ax.set_visible(False)
    fig.suptitle(f"Salg vs. hyllekapasitet per produkt (uke 06–15, 2026){title_suffix}",
                 fontsize=13, y=1.00)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_utilization(df: pd.DataFrame, path: Path) -> None:
    df = df.copy()
    df["Utnyttelse"] = df["Ant_solgt"] / df["Kapasitet"]
    stats = df.groupby("Produkt").agg(
        avg_utilization=("Utnyttelse", "mean"),
    ).sort_values("avg_utilization")

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#E63946" if u > 1 else "#2E86AB" for u in stats["avg_utilization"]]
    ax.barh(stats.index, stats["avg_utilization"], color=colors)
    ax.axvline(1.0, color="black", linestyle="--", linewidth=1,
               label="Kapasitet = etterspørsel")
    ax.set_xlabel("Gjennomsnittlig utnyttelse (salg / kapasitet)")
    ax.set_title("Mismatch: rød = underkapasitet, blå = overkapasitet")
    ax.legend()
    for i, (prod, row) in enumerate(stats.iterrows()):
        ax.text(row["avg_utilization"] + 0.1, i,
                f"{row['avg_utilization']:.2f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def abc_classification(df: pd.DataFrame) -> pd.DataFrame:
    tot = df.groupby("Produkt")["Ant_solgt"].sum().sort_values(ascending=False)
    kumulativ = tot.cumsum() / tot.sum()
    klasse = pd.Series(index=tot.index, dtype="object")
    for prod, pct in kumulativ.items():
        if pct <= 0.80:
            klasse[prod] = "A"
        elif pct <= 0.95:
            klasse[prod] = "B"
        else:
            klasse[prod] = "C"
    return pd.DataFrame({
        "Totalt_salg": tot,
        "Andel": (tot / tot.sum()).round(3),
        "Kumulativ_andel": kumulativ.round(3),
        "Klasse": klasse,
    })


def plot_abc(abc: pd.DataFrame, path: Path) -> None:
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = range(1, len(abc) + 1)
    ax1.bar(x, abc["Totalt_salg"], color="#2E86AB", alpha=0.7)
    ax1.set_xticks(x)
    ax1.set_xticklabels(abc.index, rotation=30, ha="right", fontsize=8)
    ax1.set_ylabel("Totalt salg (10 uker)", color="#2E86AB")
    ax1.tick_params(axis="y", labelcolor="#2E86AB")

    ax2 = ax1.twinx()
    ax2.plot(x, abc["Kumulativ_andel"] * 100, marker="o", color="#E63946",
             linewidth=2, label="Kumulativ %")
    ax2.axhline(80, linestyle=":", color="gray", label="80%-grense (A/B)")
    ax2.axhline(95, linestyle=":", color="darkgray", label="95%-grense (B/C)")
    ax2.set_ylabel("Kumulativ andel av total (%)", color="#E63946")
    ax2.tick_params(axis="y", labelcolor="#E63946")
    ax2.set_ylim(0, 105)
    ax2.legend(loc="center right", fontsize=9)
    fig.suptitle("ABC-analyse (Pareto)", fontsize=13)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def summary_markdown(df: pd.DataFrame, abc: pd.DataFrame, anonymized: bool) -> str:
    df = df.copy()
    df["Utnyttelse"] = df["Ant_solgt"] / df["Kapasitet"]
    lines: list[str] = []
    tittel = "Deskriptiv analyse + ABC-klassifisering"
    tittel += " (anonymisert)" if anonymized else " (intern)"
    lines.append(f"# {tittel}")
    lines.append("")
    lines.append(f"Periode: uke {df['UkeNr'].min():02d}–{df['UkeNr'].max():02d} 2026, "
                 f"{df['UkeNr'].nunique()} uker, {df['Produkt'].nunique()} produkter.")
    lines.append("")

    lines.append("## Deskriptive nøkkeltall")
    lines.append("")
    stats = df.groupby("Produkt").agg(
        Gj_snitt=("Ant_solgt", "mean"),
        Std=("Ant_solgt", "std"),
        Min=("Ant_solgt", "min"),
        Maks=("Ant_solgt", "max"),
        CoV=("Ant_solgt", lambda s: s.std() / s.mean()),
        Kapasitet=("Kapasitet", "first"),
    )
    stats["Utnyttelse"] = df.groupby("Produkt")["Utnyttelse"].mean()
    stats = stats.round(2).sort_values("Utnyttelse", ascending=False)
    lines.append("| Produkt | Gj.snitt | Std | Min | Maks | CoV | Kap | Utnyttelse |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for prod, r in stats.iterrows():
        lines.append(
            f"| {prod} | {r['Gj_snitt']:.1f} | {r['Std']:.1f} | {int(r['Min'])} | "
            f"{int(r['Maks'])} | {r['CoV']:.2f} | {int(r['Kapasitet'])} | "
            f"{r['Utnyttelse']:.2f} |"
        )
    lines.append("")
    lines.append("CoV = variasjonskoeffisient (Std / Gj.snitt).")
    lines.append("")

    lines.append("## ABC-klassifisering")
    lines.append("")
    lines.append("| Produkt | Totalt salg | Andel | Kum. | Klasse |")
    lines.append("|---|---:|---:|---:|:---:|")
    for prod, r in abc.iterrows():
        lines.append(
            f"| {prod} | {int(r['Totalt_salg'])} | {r['Andel']:.1%} | "
            f"{r['Kumulativ_andel']:.1%} | **{r['Klasse']}** |"
        )
    lines.append("")
    klasser = abc["Klasse"].value_counts().sort_index()
    lines.append(f"Fordeling: A={klasser.get('A', 0)}, "
                 f"B={klasser.get('B', 0)}, C={klasser.get('C', 0)}")
    lines.append("")

    lines.append("## Sentrale funn")
    lines.append("")
    over = stats[stats["Utnyttelse"] > 1].index.tolist()
    under = stats[stats["Utnyttelse"] < 0.9].index.tolist()
    lines.append(f"- **Underkapasitet (salg > kapasitet):** {len(over)} produkter "
                 f"— {', '.join(over)}")
    lines.append(f"- **Overkapasitet (<90% utnyttelse):** {len(under)} produkter "
                 f"— {', '.join(under)}")
    lines.append("- A-produkter dekker 80% av salget; C-produkter kan gi fra seg hylleplass.")
    return "\n".join(lines)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    FIG_INTERN.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_INTERN.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CLEAN_PARQUET)
    anon = Anonymizer.load(NAVNEREGISTER)
    df_anon = anon.apply(df)
    print(f"Lastet {len(df)} rader + navneregister ({len(anon.mapping)} prod)")

    # INTERN (ekte navn)
    plot_timeseries(df, FIG_INTERN / "salg_vs_kapasitet_tidsserie.png", " — intern")
    plot_utilization(df, FIG_INTERN / "utnyttelse_mismatch.png")
    abc_intern = abc_classification(df)
    plot_abc(abc_intern, FIG_INTERN / "abc_pareto.png")
    abc_intern.to_csv(RESULT_INTERN / "abc_klassifisering.csv")
    (RESULT_INTERN / "deskriptiv-og-abc-rapport.md").write_text(
        summary_markdown(df, abc_intern, anonymized=False), encoding="utf-8"
    )
    print(f"Intern: {FIG_INTERN}/ + {RESULT_INTERN}/")

    # ANONYMISERT (committbar)
    plot_timeseries(df_anon, FIG_DIR / "salg_vs_kapasitet_tidsserie.png")
    plot_utilization(df_anon, FIG_DIR / "utnyttelse_mismatch.png")
    abc_anon = abc_classification(df_anon)
    plot_abc(abc_anon, FIG_DIR / "abc_pareto.png")
    abc_anon.to_csv(RESULT_DIR / "abc_klassifisering.csv")
    (RESULT_DIR / "deskriptiv-og-abc-rapport.md").write_text(
        summary_markdown(df_anon, abc_anon, anonymized=True), encoding="utf-8"
    )
    print(f"Anonymisert: {FIG_DIR}/ + {RESULT_DIR}/")


if __name__ == "__main__":
    main()
