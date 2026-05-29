#!/usr/bin/env python3
"""
Lag usensorert versjon av rapporten — bytter pseudonymer (A1, A2, B1, C1 osv.)
tilbake til reelle SKU-navn fra navneregisteret. KUN for lokal bruk — kjør
aldri i CI eller skriv resultatet til versjonskontroll. .gitignore er
konfigurert for å ekskludere 005 report/rapport_intern.* og 005 report/intern/.

Strategi:
  - A1–A14 og C1–C11 substitueres trygt (ingen kollisjoner med annen tekst)
  - B1–B9 *ekskluderes* fordi B1–B7 også er begrensnings-labels i §8.2;
    diskriminering uten kontekstanalyse er upålitelig. B-pseudonymene
    forblir, og leseren kan slå opp i navneregisteret hvis de trengs.
  - Math-segmenter ($...$ og $$...$$) substitueres ikke, fordi SKU-navn med
    mellomrom og punktum bryter LaTeX-subscripts.

Kjøring:
  cd "006 analysis"
  uv run python usensorering.py
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NAVNEREGISTER = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_3_casebeskrivelse_og_datainnsamling" / "resultat" / "intern"
    / "navneregister.csv"
)
DEFAULT_INPUT_MD = REPO_ROOT / "005 report" / "rapport.md"
DEFAULT_OUTPUT_MD = REPO_ROOT / "005 report" / "rapport_intern.md"

# A og C er trygge; B kolliderer med begrensnings-labels (B1-B7) i §8.2
SAFE_PREFIXES = ("A", "C")


def load_mapping() -> dict[str, str]:
    out: dict[str, str] = {}
    with open(NAVNEREGISTER, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pseudo = row["Pseudonym"]
            if pseudo.startswith(SAFE_PREFIXES):
                out[pseudo] = row["Produkt"]
    return out


def substitute_non_math(text: str, pseudo_to_real: dict[str, str]) -> str:
    """Bytt pseudonymer til ekte navn, men ikke inni $...$ eller $$...$$."""
    # Sortér nøkler etter lengde desc — så A14 matcher før A1 i alternation
    keys = sorted(pseudo_to_real.keys(), key=lambda x: -len(x))
    pattern = re.compile(r"\b(" + "|".join(re.escape(k) for k in keys) + r")\b")

    # Splitt på math-blokker (display og inline). Match $$...$$ først (greedy)
    # for å unngå overlapp med inline $...$
    math_pattern = re.compile(r"(\$\$[\s\S]+?\$\$|\$[^\n$]+?\$)")
    parts = math_pattern.split(text)

    result: list[str] = []
    for part in parts:
        if part.startswith("$"):
            result.append(part)  # math — behold som er
        else:
            result.append(
                pattern.sub(lambda m: pseudo_to_real[m.group(1)], part)
            )
    return "".join(result)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-i", "--input", type=Path, default=DEFAULT_INPUT_MD,
                    help=f"Kilde-MD (default: {DEFAULT_INPUT_MD})")
    ap.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT_MD,
                    help=f"Ut-MD (default: {DEFAULT_OUTPUT_MD})")
    args = ap.parse_args()

    input_md = args.input
    output_md = args.output

    if not NAVNEREGISTER.exists():
        sys.exit(f"Mangler navneregister: {NAVNEREGISTER}")
    if not input_md.exists():
        sys.exit(f"Mangler input: {input_md}")

    mapping = load_mapping()
    print(f"Lastet {len(mapping)} pseudonymer (A/C-klasse) for substitusjon.")
    print(f"  B1–B9 forblir uforandret (kolliderer med begrensnings-labels).")

    text = input_md.read_text(encoding="utf-8")
    new_text = substitute_non_math(text, mapping)

    # Sett inn en synlig advarsel øverst i intern-versjonen.
    # HTML-kommentar for kildelesing + LaTeX-ramme for synlig advarsel i PDF.
    warning = (
        "<!-- ADVARSEL: INTERN VERSJON — INNEHOLDER REELLE SKU-NAVN UNDER NDA -->\n"
        "<!-- Denne filen og dens PDF skal aldri deles utenfor prosjektgruppen. -->\n\n"
        "```{=latex}\n"
        "\\begin{center}\n"
        "\\fcolorbox{red!60!black}{red!10}{%\n"
        "  \\parbox{0.92\\linewidth}{%\n"
        "    \\centering\\Large\\bfseries\\color{red!70!black}%\n"
        "    INTERN VERSJON --- IKKE DELES\\\\[0.4em]\n"
        "    \\normalsize\\mdseries\\color{black}%\n"
        "    Denne PDF-en inneholder reelle SKU-navn under NDA med Coop Extra X.\\\\\n"
        "    Den skal aldri deles, sendes eller publiseres utenfor prosjektgruppen.\n"
        "  }%\n"
        "}\n"
        "\\end{center}\n"
        "\\vspace{1em}\n"
        "```\n\n"
    )
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(warning + new_text, encoding="utf-8")

    # Statistikk
    n_before = sum(text.count(p) for p in mapping)
    n_after = sum((warning + new_text).count(p) for p in mapping)
    n_substituted = n_before - n_after
    print(f"Substituerte {n_substituted} forekomster av A/C-pseudonymer.")
    print(f"Skrevet: {output_md}")


if __name__ == "__main__":
    main()
