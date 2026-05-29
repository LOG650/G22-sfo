#!/usr/bin/env python3
"""
PDF-basert usensorering — annoterer pseudonymer (A1-A14, C1-C11) med reelle
SKU-navn direkte i en ferdig rendret PDF, uten å gå via markdown-kilde.
Brukes når en spesifikk PDF-versjon (f.eks. rapport_v3.pdf) ikke har en
matchende .md-kilde i repoet.

Strategi (revidert):
  - Bevarer original visuell layout 100 %. Pseudonymene blir IKKE byttet ut
    in-place — de er for smale (f.eks. "A1" = ~8 pt) til at hele SKU-navn
    får plass uten å overskrive nabokolonner.
  - I stedet:
      * Hvert A/C-pseudonym får en farget highlight-annotasjon (A=blå, C=grønn)
        med popup som viser reelt navn. PDF-lesere viser navnet på hover/klikk.
      * En glossar-side med full pseudonym → reelt navn-tabell prepends foran
        rapporten, sammen med en synlig NDA-advarsel.
  - B1-B9 røres ikke (kolliderer med begrensnings-labels B1-B7 i §8.2).
  - Lengste pseudonymer matches først (A14 før A1) for å unngå overlapp.

Output havner under '005 report/intern/' (gitignored).

Kjøring:
  cd "006 analysis"
  uv run python usensorering_pdf.py /Volumes/DevSSD/Downloads/rapport_v3.pdf
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import fitz

REPO_ROOT = Path(__file__).resolve().parents[1]
NAVNEREGISTER = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_3_casebeskrivelse_og_datainnsamling" / "resultat" / "intern"
    / "navneregister.csv"
)
INTERN_DIR = REPO_ROOT / "005 report" / "intern"

SAFE_PREFIXES = ("A", "C")
FALLBACK_FONT = "helv"

# RGB farger for highlight per klasse (lyse pasteller, leselig under tekst)
COLOR_A = (0.70, 0.85, 1.00)   # lys blå
COLOR_C = (0.75, 0.95, 0.75)   # lys grønn


def load_mapping() -> dict[str, str]:
    out: dict[str, str] = {}
    with open(NAVNEREGISTER, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pseudo = row["Pseudonym"]
            if pseudo.startswith(SAFE_PREFIXES):
                out[pseudo] = row["Produkt"]
    return out


def shorten(real: str) -> str:
    """Kompakt form til glossar når SKU-navnet er svært langt."""
    tokens = real.split()
    if len(tokens) <= 2:
        return real
    return f"{tokens[0]} {tokens[-2]} {tokens[-1]}"


def rects_overlap(a: fitz.Rect, b: fitz.Rect, tol: float = 0.5) -> bool:
    """Hører rect a sannsynligvis sammen med (er innenfor) rect b?"""
    return (
        a.x0 >= b.x0 - tol
        and a.x1 <= b.x1 + tol
        and a.y0 >= b.y0 - tol
        and a.y1 <= b.y1 + tol
    )


def build_glossary_page(doc: fitz.Document, mapping: dict[str, str]) -> None:
    """Sett inn en NDA-advarsel + full glossar-side foran rapporten."""
    page = doc.new_page(pno=0, width=595, height=842)  # A4
    margin = 50
    y = margin

    # NDA-advarsel
    warn_rect = fitz.Rect(margin, y, 595 - margin, y + 110)
    page.draw_rect(warn_rect, color=(0.7, 0.1, 0.1), fill=(1.0, 0.92, 0.92), width=1.5)
    page.insert_textbox(
        fitz.Rect(margin + 10, y + 10, 595 - margin - 10, y + 100),
        "INTERN VERSJON - IKKE DELES\n\n"
        "Denne PDF-en er v3-rapporten med usensorerings-annotasjoner. "
        "A-pseudonymer (A1-A14) er markert med blaa highlight, C-pseudonymer "
        "(C1-C11) med groenn. Hold musepekeren over (eller klikk paa) en "
        "highlight i en PDF-leser for aa se reelt SKU-navn. Full tabell under. "
        "B-pseudonymer (B1-B9) er bevart fordi de kolliderer med "
        "begrensnings-labels B1-B7 i §8.2.",
        fontname="helv",
        fontsize=10,
        align=fitz.TEXT_ALIGN_LEFT,
        color=(0.4, 0.0, 0.0),
    )
    y += 130

    # Glossar-tabell
    page.insert_text(
        (margin, y),
        "Pseudonym  ->  Reelt SKU-navn",
        fontname="hebo",
        fontsize=14,
    )
    y += 24

    col_w = (595 - 2 * margin) / 2
    row_h = 13
    items = sorted(
        mapping.items(),
        key=lambda kv: (kv[1][0], int(kv[0][1:])),  # klasse + nummer
    )
    half = (len(items) + 1) // 2
    left_col = items[:half]
    right_col = items[half:]

    for col_idx, col_items in enumerate((left_col, right_col)):
        x = margin + col_idx * col_w
        cy = y
        for pseudo, real in col_items:
            page.insert_text((x, cy), f"{pseudo:>4}", fontname="hebo", fontsize=9)
            page.insert_text(
                (x + 30, cy),
                real if fitz.get_text_length(real, "helv", 9) <= col_w - 35
                else shorten(real),
                fontname="helv",
                fontsize=9,
            )
            cy += row_h


def annotate_page(
    page: fitz.Page,
    mapping: dict[str, str],
) -> int:
    """Legg highlight + popup på hvert A/C-pseudonym. Returnerer antall."""
    # Lengste pseudonymer først (A14 før A1) for å unngå at A1 matcher inni A14
    keys = sorted(mapping.keys(), key=lambda k: -len(k))

    claimed: list[fitz.Rect] = []
    n = 0

    for pseudo in keys:
        real = mapping[pseudo]
        klasse = pseudo[0]
        color = COLOR_A if klasse == "A" else COLOR_C
        rects = page.search_for(pseudo)
        for r in rects:
            if any(rects_overlap(r, c) for c in claimed):
                continue
            claimed.append(r)

            annot = page.add_highlight_annot(r)
            annot.set_colors(stroke=color)
            annot.set_info(
                title=pseudo,
                content=f"{pseudo} = {real}",
            )
            annot.update()
            n += 1
    return n


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_pdf", type=Path, help="PDF som skal usensoreres")
    ap.add_argument("-o", "--output", type=Path, default=None)
    args = ap.parse_args()

    if not NAVNEREGISTER.exists():
        sys.exit(f"Mangler navneregister: {NAVNEREGISTER}")
    if not args.input_pdf.exists():
        sys.exit(f"Mangler input PDF: {args.input_pdf}")

    INTERN_DIR.mkdir(parents=True, exist_ok=True)
    out_path = args.output or (INTERN_DIR / f"{args.input_pdf.stem}_intern.pdf")

    mapping = load_mapping()
    print(f"Lastet {len(mapping)} A/C-pseudonymer.")

    doc = fitz.open(args.input_pdf)
    print(f"Åpnet {args.input_pdf.name}: {len(doc)} sider.")

    total = 0
    for pno in range(len(doc)):
        page = doc[pno]
        n = annotate_page(page, mapping)
        if n:
            print(f"  side {pno+1:>3}: {n} annotasjoner")
        total += n

    build_glossary_page(doc, mapping)

    doc.save(out_path, garbage=4, deflate=True)
    doc.close()
    print(f"\nTotalt {total} highlight-annotasjoner. Skrevet: {out_path}")
    print("  + glossar-side satt inn som side 1.")
    print("  Hover/klikk en highlight i Acrobat/Preview for å se reelt SKU-navn.")
    print("  ADVARSEL: NDA-materiale — ikke del.")


if __name__ == "__main__":
    main()
