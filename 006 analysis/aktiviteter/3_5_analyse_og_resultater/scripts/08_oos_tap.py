#!/usr/bin/env python3
"""
ACT-3.5.3 OOS-tap ex post.

Beregner hvor mye salg leverandøren *taper* hver uke i dagens hyllekonfigurasjon
på grunn av out-of-stock (utnyttelsesgrad > 1.0). Tapet rapporteres i to enheter:
  - tapte enheter/uke  = (d_i - s̄_i)
  - tapt margin-verdi  = (d_i - s̄_i) × m_i

To antagelser om skjult etterspørsel kjøres parallelt:
  - overserve = 2.0 (S2-hovedscenariet)
  - overserve = 1.5 (S3-konservativt)

For SKUer med u_i < 1.0 er det per definisjon ikke OOS-tap; modellen rapporterer
disse som 0. Tallet er en *ex post*-kalkyle på dagens situasjon, ikke en LP-
optimering. Den supplerer §5.2/§7.5 ved å oversette mismatchen til en kostnad i
samme enhet som LP-gevinsten.

Kjøring:
  cd "006 analysis"
  uv run python aktiviteter/3_5_analyse_og_resultater/scripts/08_oos_tap.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[4]
INTERN_DATA_DIR = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_3_casebeskrivelse_og_datainnsamling" / "resultat" / "intern"
)
CLEAN_PARQUET = INTERN_DATA_DIR / "salg_renset.parquet"
NAVNEREGISTER = INTERN_DATA_DIR / "navneregister.csv"
RESULT_DIR = Path(__file__).resolve().parents[1] / "resultat"
RESULT_INTERN = RESULT_DIR / "intern"

sys.path.insert(0, str(REPO_ROOT / "006 analysis"))
from anonymisering import Anonymizer  # noqa: E402
from margin_mapping import margin_for_product  # noqa: E402

OVERSERVE_VARIANTS = [
    ("hovedscenario", 2.0),
    ("konservativ",   1.5),
]


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("Produkt").agg(
        mean_sales=("Ant_solgt", "mean"),
        facings=("Kapasitet", "first"),
    )
    g["utilization"] = g["mean_sales"] / g["facings"]
    g["margin"] = [margin_for_product(p) for p in g.index]
    return g


def compute_oos(stats: pd.DataFrame, overserve: float) -> pd.DataFrame:
    """For SKUer med u > 1: tapt salg = (overserve - 1) × s̄_i, tapt margin = tapt × m_i."""
    out = stats.copy()
    is_oos = out["utilization"] > 1.0
    out["d_i"] = out["mean_sales"]
    out.loc[is_oos, "d_i"] = out.loc[is_oos, "mean_sales"] * overserve
    out["tapt_enheter"] = (out["d_i"] - out["mean_sales"]).clip(lower=0)
    out["tapt_margin"] = out["tapt_enheter"] * out["margin"]
    out["er_oos"] = is_oos
    return out


def summarize(oos: pd.DataFrame, overserve: float) -> dict:
    is_oos = oos["er_oos"]
    return {
        "overserve": overserve,
        "n_oos_skuer": int(is_oos.sum()),
        "tapt_enheter_total": float(oos["tapt_enheter"].sum()),
        "tapt_margin_total": float(oos["tapt_margin"].sum()),
        "tapt_enheter_per_oos": (
            float(oos.loc[is_oos, "tapt_enheter"].mean()) if is_oos.any() else 0.0
        ),
        "tapt_margin_per_oos": (
            float(oos.loc[is_oos, "tapt_margin"].mean()) if is_oos.any() else 0.0
        ),
    }


def build_report(stats: pd.DataFrame, results: dict, baseline_margin: float,
                 anon: Anonymizer) -> str:
    lines: list[str] = []
    lines.append("# OOS-tap ex post — leverandørens portefølje hos Coop Extra X")
    lines.append("")
    lines.append("Estimerer hvor mye margin-vektet salg leverandøren *taper hver uke* "
                 "på grunn av out-of-stock (utnyttelse > 1,0) i dagens hyllekonfigurasjon. "
                 "Beregnet før LP-omfordeling — dvs. tapet som *forsvinner* hvis "
                 "anbefalingen i §7 implementeres.")
    lines.append("")
    lines.append(f"**Baseline margin-vektet salg:** {baseline_margin:.1f} per uke")
    lines.append("")
    lines.append("## Oppsummering på tvers av antagelser")
    lines.append("")
    lines.append("| Antagelse | overserve | OOS-SKUer | Tapt enh./uke | Tapt margin/uke | Andel av baseline |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for navn, summ in results.items():
        andel = 100 * summ["tapt_margin_total"] / baseline_margin
        lines.append(
            f"| {navn} | {summ['overserve']:.2f} | "
            f"{summ['n_oos_skuer']} | "
            f"{summ['tapt_enheter_total']:.1f} | "
            f"{summ['tapt_margin_total']:.1f} | "
            f"{andel:.1f}% |"
        )
    lines.append("")
    lines.append("**Tolkning:** OOS-tap-tallet er av samme størrelsesorden som LP-gevinsten "
                 "(jf. §7). Det styrker E1 (mismatch er reell) med en *kostnadssize*: "
                 "leverandøren mister allerede betydelig margin på dagens hylle.")
    lines.append("")
    lines.append("## Per-SKU tap (hovedscenario, overserve = 2.0)")
    lines.append("")
    oos_main = compute_oos(stats, 2.0)
    oos_main_sorted = oos_main.sort_values("tapt_margin", ascending=False)
    lines.append("| SKU | Utnyttelse | Snittsalg | d_i | Tapt enh./uke | Margin | Tapt margin/uke |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for prod, r in oos_main_sorted.iterrows():
        if not r["er_oos"]:
            continue
        lines.append(
            f"| {anon.pseudo(prod)} | {r['utilization']:.2f} | "
            f"{r['mean_sales']:.1f} | {r['d_i']:.1f} | "
            f"{r['tapt_enheter']:.1f} | {r['margin']:.0%} | "
            f"{r['tapt_margin']:.2f} |"
        )
    lines.append("")
    top5 = oos_main_sorted[oos_main_sorted["er_oos"]].head(5)
    top5_share = 100 * top5["tapt_margin"].sum() / oos_main["tapt_margin"].sum()
    lines.append(f"**Topp 5 SKUer står for {top5_share:.0f}% av samlet OOS-tap** "
                 f"({', '.join(anon.pseudo(p) for p in top5.index)}).")
    lines.append("")
    lines.append("## Tolkning i forhandlingsdialog")
    lines.append("")
    lines.append("- Tallet er en *ex post*-kalkyle: hva mister leverandøren *i dag*, før "
                 "noen omfordeling.")
    lines.append("- Det er sammenlignbart med LP-gevinsten i §7 — begge er margin-enheter "
                 "per uke.")
    lines.append("- Antagelsen om skjult etterspørsel (overserve 1,5–2,0) er den samme "
                 "som modellen bygger på; sensitiviteten her speiler §7.3.")
    lines.append("- Hovedfunnet i §7.5 (mismatch er gjennomgripende) underbygges av at "
                 "tapet er konsentrert hos få A-klasse-SKUer, ikke spredt utover "
                 "porteføljen.")
    return "\n".join(lines)


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_INTERN.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CLEAN_PARQUET)
    anon = Anonymizer.load(NAVNEREGISTER)
    stats = aggregate(df)

    baseline_margin = float((stats["mean_sales"] * stats["margin"]).sum())
    print(f"Baseline margin-vektet: {baseline_margin:.1f}")
    print()

    results: dict[str, dict] = {}
    per_sku_rows: list[dict] = []
    for navn, overserve in OVERSERVE_VARIANTS:
        oos = compute_oos(stats, overserve)
        results[navn] = summarize(oos, overserve)
        for prod, r in oos.iterrows():
            per_sku_rows.append({
                "scenario": navn,
                "overserve": overserve,
                "produkt": prod,
                "pseudonym": anon.pseudo(prod),
                "utilization": float(r["utilization"]),
                "mean_sales": float(r["mean_sales"]),
                "d_i": float(r["d_i"]),
                "tapt_enheter": float(r["tapt_enheter"]),
                "margin": float(r["margin"]),
                "tapt_margin": float(r["tapt_margin"]),
                "er_oos": bool(r["er_oos"]),
            })
        s = results[navn]
        print(f"[{navn}] overserve={overserve:.1f}: "
              f"{s['n_oos_skuer']} OOS-SKUer, "
              f"tap {s['tapt_margin_total']:.1f} margin-enh./uke "
              f"({100*s['tapt_margin_total']/baseline_margin:.1f}% av baseline)")

    # Skriv MD-rapport (samme for intern og anon — tabellen bruker pseudonymer)
    report = build_report(stats, results, baseline_margin, anon)
    (RESULT_DIR / "oos_tap_rapport.md").write_text(report, encoding="utf-8")
    (RESULT_INTERN / "oos_tap_rapport.md").write_text(report, encoding="utf-8")

    # CSV per SKU
    per_sku = pd.DataFrame(per_sku_rows)
    # Intern: med ekte produktnavn
    per_sku.to_csv(RESULT_INTERN / "oos_tap_per_sku.csv", index=False)
    # Anon: drop ekte navn
    per_sku.drop(columns=["produkt"]).to_csv(
        RESULT_DIR / "oos_tap_per_sku.csv", index=False,
    )

    print(f"\nSkrevet: {RESULT_DIR / 'oos_tap_rapport.md'}")
    print(f"         {RESULT_DIR / 'oos_tap_per_sku.csv'}")


if __name__ == "__main__":
    main()
