#!/usr/bin/env python3
"""
ACT-3.5.4 Heuristikk-benchmark mot LP S2.

Implementerer fire enkle allokeringsregler som *en category manager realistisk
kunne brukt uten LP-modell*, og sammenligner margin/volum-gevinsten mot S2 LP
(hovedanbefalingen). Formålet er å vise hva LP faktisk *kjøper* — er løftet
+40,6% over dagens (jf. §7) primært et utslag av sunn fornuft, eller krever det
optimeringen?

Fire heuristikker (alle respekterer x_min = 3 × Dybde_i ≈ 1 kolli per SKU og
totalbudsjettet T = 1079 hylleenheter):

  H1 — Proporsjonal til salg
       x_i = x_min + andel(s̄_i) × pool

  H2 — Proporsjonal til margin × salg
       x_i = x_min + andel(m_i · s̄_i) × pool

  H3 — ABC-flatt 80/15/5
       80% av pool fordelt likt blant A-SKUer, 15% B, 5% C

  H4 — Behold dagens (baseline)
       x_i = c_i (ingen omfordeling)

For hver allokering: y_i = min(d_i, ρ_i · x_i), der ρ_i = s̄_i / c_i og d_i =
2 × s̄_i for u_i > 1, ellers d_i = s̄_i. Margin = Σ m_i · y_i.

Kjøring:
  cd "006 analysis"
  uv run python aktiviteter/3_5_analyse_og_resultater/scripts/09_heuristikker.py
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
LP_S2_CSV = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_4_data_metode_og_modellering" / "resultat" / "intern"
    / "lp_allokering_S2_primaer_sek.csv"
)
RESULT_DIR = Path(__file__).resolve().parents[1] / "resultat"
RESULT_INTERN = RESULT_DIR / "intern"

sys.path.insert(0, str(REPO_ROOT / "006 analysis"))
from anonymisering import Anonymizer  # noqa: E402
from margin_mapping import margin_for_product  # noqa: E402

OVERSERVE = 2.0
X_MIN_FACINGS = 3


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("Produkt").agg(
        mean_sales=("Ant_solgt", "mean"),
        facings=("Kapasitet", "first"),
        dybde=("Dybde", "first"),
    )
    g["productivity"] = g["mean_sales"] / g["facings"]
    g["utilization"] = g["mean_sales"] / g["facings"]
    g["margin"] = [margin_for_product(p) for p in g.index]
    g["x_min"] = (g["dybde"] * X_MIN_FACINGS).astype(int)
    g["d_i"] = g["mean_sales"]
    over = g["utilization"] > 1.0
    g.loc[over, "d_i"] = g.loc[over, "mean_sales"] * OVERSERVE
    return g


def compute_abc(stats: pd.DataFrame, thresholds=(0.80, 0.95)) -> pd.Series:
    tot = stats["mean_sales"].sort_values(ascending=False)
    cum = tot.cumsum() / tot.sum()
    out = pd.Series(index=stats.index, dtype=object)
    for prod, pct in cum.items():
        if pct <= thresholds[0]:
            out[prod] = "A"
        elif pct <= thresholds[1]:
            out[prod] = "B"
        else:
            out[prod] = "C"
    return out


def allocate_proportional(weights: pd.Series, x_min: pd.Series, T: int) -> pd.Series:
    """Gulvallokering + proporsjonal fordeling av overskuddspool."""
    x = x_min.astype(int).copy()
    pool = T - int(x.sum())
    if pool <= 0:
        return x
    w = weights / weights.sum()
    extra_raw = w * pool
    extra = extra_raw.round().astype(int)
    diff = pool - int(extra.sum())
    if diff != 0:
        # Fordel residual til SKUer med høyest brøkdel (eller laveste hvis negativ)
        frac = (extra_raw - extra_raw.round()).sort_values(
            ascending=(diff < 0)
        )
        idx = frac.head(abs(diff)).index
        for i in idx:
            extra.loc[i] += (1 if diff > 0 else -1)
    return x + extra


def allocate_abc_flat(abc: pd.Series, x_min: pd.Series, T: int,
                      shares=(0.80, 0.15, 0.05)) -> pd.Series:
    """80/15/5 — A-klasse får 80% av pool likt fordelt, B 15%, C 5%."""
    x = x_min.astype(int).copy()
    pool = T - int(x.sum())
    if pool <= 0:
        return x
    extra = pd.Series(0, index=x.index, dtype=int)
    klasse_share = {"A": shares[0], "B": shares[1], "C": shares[2]}
    for kls, share in klasse_share.items():
        members = abc[abc == kls].index
        n = len(members)
        if n == 0:
            continue
        per_sku = int(round(share * pool / n))
        extra.loc[members] = per_sku
    # Justér slack til sum stemmer
    diff = pool - int(extra.sum())
    if diff != 0:
        a_members = abc[abc == "A"].index.tolist()
        for i in range(abs(diff)):
            sku = a_members[i % len(a_members)]
            extra.loc[sku] += (1 if diff > 0 else -1)
    return x + extra


def realize(allocation: pd.Series, stats: pd.DataFrame) -> dict:
    """Beregn realisert salg/margin gitt en allokering."""
    rho = stats["productivity"]
    d = stats["d_i"]
    y = pd.concat([rho * allocation, d], axis=1).min(axis=1)
    margin = float((y * stats["margin"]).sum())
    volume = float(y.sum())
    return {
        "allocation": allocation.astype(int),
        "sales": y.round(2),
        "margin": margin,
        "volume": volume,
    }


def load_lp_s2() -> pd.DataFrame:
    """LP S2 baseline-resultat — fra 03_lp_modell.py intern-CSV (ekte produktnavn som indeks)."""
    df = pd.read_csv(LP_S2_CSV, index_col=0)
    return df


def build_report(rules_results: dict, baseline_margin: float, baseline_volume: float,
                 lp_s2_margin: float, lp_s2_volume: float,
                 anon: Anonymizer, stats: pd.DataFrame) -> str:
    lines: list[str] = []
    lines.append("# Heuristikk-benchmark mot LP S2")
    lines.append("")
    lines.append("Fire enkle allokeringsregler sammenlignet med LP-hovedanbefalingen (S2). "
                 "Formålet er å kvantifisere hva LP-optimeringen *legger til* utover sunn "
                 "fornuft.")
    lines.append("")
    lines.append(f"- **Baseline (dagens hyllekonfigurasjon)**: margin {baseline_margin:.1f}, "
                 f"volum {baseline_volume:.0f}")
    lines.append(f"- **LP S2 (hovedanbefaling)**: margin {lp_s2_margin:.1f}, "
                 f"volum {lp_s2_volume:.0f} "
                 f"(+{100*(lp_s2_margin-baseline_margin)/baseline_margin:.1f}% margin)")
    lines.append("")

    lines.append("## Sammenligning")
    lines.append("")
    lines.append("| Regel | Margin | Δ vs baseline | Volum | LP-gap (pp) |")
    lines.append("|---|---:|---:|---:|---:|")
    lp_pct = 100 * (lp_s2_margin - baseline_margin) / baseline_margin
    for name, res in rules_results.items():
        pct = 100 * (res["margin"] - baseline_margin) / baseline_margin
        gap = lp_pct - pct
        lines.append(
            f"| {name} | {res['margin']:.1f} | "
            f"{pct:+.1f}% | {res['volume']:.0f} | "
            f"{gap:+.1f} |"
        )
    lines.append(f"| **LP S2** | **{lp_s2_margin:.1f}** | "
                 f"**+{lp_pct:.1f}%** | **{lp_s2_volume:.0f}** | **0** |")
    lines.append("")
    lines.append("**LP-gap** = avstand fra heuristikken til LP-optimum i prosentpoeng på "
                 "margin-gevinsten. Lavt gap betyr at heuristikken er nesten like god som LP.")
    lines.append("")

    # Tolkning
    best_heur_name, best_heur_res = max(
        rules_results.items(), key=lambda kv: kv[1]["margin"],
    )
    best_pct = 100 * (best_heur_res["margin"] - baseline_margin) / baseline_margin
    gap = lp_pct - best_pct
    lines.append("## Tolkning")
    lines.append("")
    lines.append(f"- **Beste heuristikk**: *{best_heur_name}* med +{best_pct:.1f}% "
                 f"margin-gevinst. LP-gap: {gap:.1f} prosentpoeng.")
    if gap < 5.0:
        lines.append(f"- LP-løftet utover beste heuristikk er **moderat** ({gap:.1f} pp). "
                     "Mye av gevinsten i §7 ligger i den åpenbare omfordelingen — "
                     "LP-modellens hovedverdi blir i så fall transparensen, "
                     "sensitivitetsanalysen og den eksplisitte håndteringen av "
                     "sortimentsgulv, ikke det absolutte gevinst-tallet.")
    else:
        lines.append(f"- LP-løftet utover beste heuristikk er **betydelig** ({gap:.1f} pp). "
                     "Optimeringen henter ut gevinst som enkle regler ikke fanger — "
                     "særlig håndtering av minimumssortiment, sekundærplasser og "
                     "demand-cap simultant.")
    lines.append("- Behold-dagens (H4) representerer baseline; differansen til H1–H3 viser "
                 "hva *enkel omfordeling* alene gir.")
    lines.append("")

    # Per-SKU sammenligning
    lines.append("## Allokering per SKU (alle regler + LP)")
    lines.append("")
    lp_alloc = pd.read_csv(LP_S2_CSV, index_col=0)["facings_optimal"]
    cols = ["Dagens"] + list(rules_results.keys()) + ["LP S2"]
    lines.append("| SKU | " + " | ".join(cols) + " |")
    lines.append("|---|" + "|".join(["---:"] * len(cols)) + "|")
    skus_sorted = sorted(stats.index, key=lambda p: anon.pseudo(p))
    for prod in skus_sorted:
        row = [anon.pseudo(prod), str(int(stats.loc[prod, "facings"]))]
        for name, res in rules_results.items():
            row.append(str(int(res["allocation"][prod])))
        row.append(str(int(lp_alloc[prod])))
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_INTERN.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CLEAN_PARQUET)
    anon = Anonymizer.load(NAVNEREGISTER)
    stats = aggregate(df)
    abc = compute_abc(stats)
    T = int(stats["facings"].sum())

    print(f"T = {T} hylleenheter, {len(stats)} SKUer, x_min sum = {stats['x_min'].sum()}")

    # Baseline (dagens)
    base_alloc = stats["facings"].astype(int)
    base = realize(base_alloc, stats)

    # LP S2 fra fil
    lp_df = load_lp_s2()
    lp_alloc = lp_df["facings_optimal"].astype(int)
    lp_realized = realize(lp_alloc, stats)
    # Note: LP S2 har også sekundærplasser; vi sammenligner her bare primær.
    # LP-margin/volum fra CSV er det "ekte" S2-tallet (inkluderer sekundær).
    lp_s2_margin_ekte = float((lp_df["sales_optimal"] * stats["margin"]).sum())
    lp_s2_volume_ekte = float(lp_df["sales_optimal"].sum())

    # Heuristikker
    rules_results: dict[str, dict] = {}
    rules_results["H1 Prop-salg"] = realize(
        allocate_proportional(stats["mean_sales"], stats["x_min"], T), stats,
    )
    rules_results["H2 Prop-margin×salg"] = realize(
        allocate_proportional(stats["mean_sales"] * stats["margin"], stats["x_min"], T),
        stats,
    )
    rules_results["H3 ABC-flatt 80/15/5"] = realize(
        allocate_abc_flat(abc, stats["x_min"], T), stats,
    )
    rules_results["H4 Behold dagens"] = base

    # Verifiser at allokeringene summerer riktig
    for name, res in rules_results.items():
        s = int(res["allocation"].sum())
        assert s == T, f"{name}: sum={s} != T={T}"

    # Sammendrag til konsoll
    print(f"\nBaseline:                          {base['margin']:.1f} (volum {base['volume']:.0f})")
    for name, res in rules_results.items():
        pct = 100 * (res["margin"] - base["margin"]) / base["margin"]
        print(f"{name:35} {res['margin']:.1f} (+{pct:.1f}%, volum {res['volume']:.0f})")
    lp_pct = 100 * (lp_s2_margin_ekte - base["margin"]) / base["margin"]
    print(f"{'LP S2 (med sekundær)':35} {lp_s2_margin_ekte:.1f} (+{lp_pct:.1f}%, "
          f"volum {lp_s2_volume_ekte:.0f})")

    # Rapport
    report = build_report(
        rules_results, base["margin"], base["volume"],
        lp_s2_margin_ekte, lp_s2_volume_ekte, anon, stats,
    )
    (RESULT_DIR / "heuristikker_rapport.md").write_text(report, encoding="utf-8")
    (RESULT_INTERN / "heuristikker_rapport.md").write_text(report, encoding="utf-8")

    # CSV: per-regel sammendrag
    summary_rows = []
    for name, res in rules_results.items():
        summary_rows.append({
            "regel": name,
            "margin": res["margin"],
            "volum": res["volume"],
            "gain_pct_margin": 100 * (res["margin"] - base["margin"]) / base["margin"],
            "lp_gap_pp": lp_pct - 100 * (res["margin"] - base["margin"]) / base["margin"],
        })
    summary_rows.append({
        "regel": "LP S2",
        "margin": lp_s2_margin_ekte,
        "volum": lp_s2_volume_ekte,
        "gain_pct_margin": lp_pct,
        "lp_gap_pp": 0.0,
    })
    pd.DataFrame(summary_rows).to_csv(
        RESULT_DIR / "heuristikker_sammenligning.csv", index=False,
    )
    pd.DataFrame(summary_rows).to_csv(
        RESULT_INTERN / "heuristikker_sammenligning.csv", index=False,
    )

    # CSV: per-SKU allokering for hver regel
    alloc_rows = []
    for prod in stats.index:
        row = {
            "pseudonym": anon.pseudo(prod),
            "dagens": int(stats.loc[prod, "facings"]),
            "lp_s2": int(lp_alloc[prod]),
        }
        for name, res in rules_results.items():
            row[name] = int(res["allocation"][prod])
        alloc_rows.append(row)
    alloc_df = pd.DataFrame(alloc_rows).set_index("pseudonym").sort_index()
    alloc_df.to_csv(RESULT_DIR / "heuristikker_allokering.csv")

    # Intern: behold ekte navn også
    alloc_df_intern = alloc_df.copy()
    alloc_df_intern["produkt"] = [
        next(p for p in stats.index if anon.pseudo(p) == ps)
        for ps in alloc_df_intern.index
    ]
    alloc_df_intern.to_csv(RESULT_INTERN / "heuristikker_allokering.csv")

    print(f"\nSkrevet: {RESULT_DIR / 'heuristikker_rapport.md'}")
    print(f"         {RESULT_DIR / 'heuristikker_sammenligning.csv'}")
    print(f"         {RESULT_DIR / 'heuristikker_allokering.csv'}")


if __name__ == "__main__":
    main()
