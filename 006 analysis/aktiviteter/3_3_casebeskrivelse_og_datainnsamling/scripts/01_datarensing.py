#!/usr/bin/env python3
"""
ACT-3.3.4 Datarensing — LOG650 G22

Leser rå salgsdata fra 004 data/Data 10 uker.csv og produserer:
  - resultat/intern/          — faktiske produktnavn (gitignored, NDA)
  - resultat/                  — pseudonymer A1/B1/C1 (committes, publiserbart)
  - resultat/intern/navneregister.csv — kobling (kun lokalt)

Kjøring:
  cd "006 analysis"
  uv run python aktiviteter/3_3_casebeskrivelse_og_datainnsamling/scripts/01_datarensing.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[4]
# Utvidet CCEP-datasett (35 SKUer, én butikk, uke 06-15 2026)
RAW_CSV = REPO_ROOT / "004 data" / "Salgsdata u6-15 26.csv"
RESULT_DIR = Path(__file__).resolve().parents[1] / "resultat"
INTERN_DIR = RESULT_DIR / "intern"

# Legg 006 analysis/ til sys.path for å finne anonymisering-modulen
sys.path.insert(0, str(REPO_ROOT / "006 analysis"))
from anonymisering import Anonymizer  # noqa: E402


def load_raw(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig", dtype={"UkeNr": str})
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rens + beregn fysisk hyllekapasitet.

    Merk: Kolonnen 'Kapasitet MAX' i råfila er en gjennomstrømnings-metrikk
    (= Ant_solgt × dybde + sekundær_plassering) og IKKE statisk hyllekapasitet.
    Fysisk kapasitet beregnes derfor som Facings × dybde (+ sekundær der relevant).
    """
    df = df.copy()
    df["UkeNr"] = df["UkeNr"].astype(int)
    df["År"] = df["År"].astype(int)
    df["Ant_solgt"] = df["Ant solgt"].astype(int)

    # Ny skjema-tolkning
    df["Dybde"] = pd.to_numeric(df["dybde (antall flasker) MAX"],
                                 errors="coerce").fillna(0).astype(int)
    df["Facings"] = pd.to_numeric(df["Facings MAX"],
                                   errors="coerce").fillna(0).astype(int)
    df["Sekundaer"] = pd.to_numeric(df["Sekundær plassering antall salgsenheter"],
                                     errors="coerce").fillna(0).astype(int)

    # Fysisk kapasitet = facings × dybde (uten sekundær — sekundær er oftest kampanje)
    df["Kapasitet"] = df["Facings"] * df["Dybde"]

    df = df.rename(columns={"Vare": "Produkt"})

    # Fjern SKUer uten hylleplass (Facings=0 → ikke i nåværende planogram)
    valid = df["Kapasitet"] > 0
    dropped = df[~valid]["Produkt"].unique()
    if len(dropped) > 0:
        print(f"Forkaster {len(dropped)} SKU(er) uten hylleplass: {list(dropped)}")
    df = df[valid]

    assert df["Kjede"].nunique() == 1
    assert df["Butikk"].nunique() == 1

    return df[[
        "År", "UkeNr", "Produkt", "Ant_solgt",
        "Facings", "Dybde", "Sekundaer", "Kapasitet",
    ]].sort_values(["Produkt", "UkeNr"]).reset_index(drop=True)


def sanity_report(df: pd.DataFrame, anonymize: bool, anon: Anonymizer | None) -> str:
    """Markdown-rapport. Hvis anonymize=True, bruk pseudonymer."""
    def name(p: str) -> str:
        return anon.pseudo(p) if anonymize and anon else p

    lines: list[str] = []
    lines.append("# Datarensing — sanity-rapport"
                 + (" (anonymisert)" if anonymize else " (intern)"))
    lines.append("")
    lines.append(f"- Rader: **{len(df)}**")
    lines.append(f"- Produkter: **{df['Produkt'].nunique()}**")
    lines.append(f"- Uker: **{df['UkeNr'].min()}–{df['UkeNr'].max()}** "
                 f"({df['UkeNr'].nunique()} unike)")
    lines.append(f"- År: {sorted(df['År'].unique())}")
    lines.append("")

    lines.append("## Observasjoner per produkt")
    lines.append("")
    counts = df.groupby("Produkt")["UkeNr"].count().sort_values(ascending=False)
    expected_weeks = df["UkeNr"].nunique()
    lines.append("| Produkt | Antall uker | Manglende? |")
    lines.append("|---|---:|---|")
    for prod, n in counts.items():
        missing = "Nei" if n == expected_weeks else f"Ja ({expected_weeks - n})"
        lines.append(f"| {name(prod)} | {n} | {missing} |")
    lines.append("")

    lines.append("## Nøkkeltall per produkt")
    lines.append("")
    stats = df.groupby("Produkt").agg(
        gjennomsnitt_salg=("Ant_solgt", "mean"),
        min_salg=("Ant_solgt", "min"),
        max_salg=("Ant_solgt", "max"),
        kapasitet=("Kapasitet", "first"),
    ).round(1)
    stats["utnyttelse"] = (stats["gjennomsnitt_salg"] / stats["kapasitet"]).round(2)
    stats = stats.sort_values("utnyttelse", ascending=False)
    lines.append("| Produkt | Gj.snitt | Min | Maks | Kapasitet | Utnyttelse |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for prod, row in stats.iterrows():
        lines.append(
            f"| {name(prod)} | {row['gjennomsnitt_salg']:.1f} | {int(row['min_salg'])} | "
            f"{int(row['max_salg'])} | {int(row['kapasitet'])} | "
            f"{row['utnyttelse']:.2f} |"
        )
    lines.append("")
    lines.append("Utnyttelse >1 = underkapasitet (salg > hylleplass). "
                 "Utnyttelse <1 = overkapasitet.")
    lines.append("")

    lines.append("## Datakvalitet")
    lines.append("")
    null_count = df.isnull().sum().sum()
    dup_count = df.duplicated(subset=["Produkt", "UkeNr"]).sum()
    lines.append(f"- Nullverdier totalt: **{null_count}**")
    lines.append(f"- Dubletter (produkt+uke): **{dup_count}**")
    neg = (df["Ant_solgt"] < 0).sum()
    lines.append(f"- Negative salgsverdier: **{neg}**")
    return "\n".join(lines)


def main() -> None:
    print(f"Leser: {RAW_CSV}")
    raw = load_raw(RAW_CSV)
    df = clean(raw)
    print(f"Renset: {len(df)} rader, {df['Produkt'].nunique()} produkter")

    INTERN_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    # Bygg pseudonymer fra renset data
    anon = Anonymizer.build_from_sales(df)
    register_path = anon.save(INTERN_DIR)
    print(f"Navneregister (intern): {register_path}")

    # Intern output — ekte navn
    df.to_parquet(INTERN_DIR / "salg_renset.parquet", index=False)
    df.to_csv(INTERN_DIR / "salg_renset.csv", index=False)
    (INTERN_DIR / "datarensing-rapport.md").write_text(
        sanity_report(df, anonymize=False, anon=None), encoding="utf-8"
    )
    print(f"Intern: {INTERN_DIR}/")

    # Committbar output — pseudonymer
    df_anon = anon.apply(df)
    df_anon.to_parquet(RESULT_DIR / "salg_renset.parquet", index=False)
    df_anon.to_csv(RESULT_DIR / "salg_renset.csv", index=False)
    (RESULT_DIR / "datarensing-rapport.md").write_text(
        sanity_report(df, anonymize=True, anon=anon), encoding="utf-8"
    )
    print(f"Anonymisert: {RESULT_DIR}/")


if __name__ == "__main__":
    main()
