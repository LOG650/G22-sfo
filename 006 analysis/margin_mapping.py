"""
Margin-tildeling per SKU basert på merkevare.

Bruker margin som relativ vekt i LP-målfunksjonen. Siden marginprosenten er
fast i transaksjonen leverandør→butikk er dette tilstrekkelig for å rangere
SKUer uten å trenge eksplisitte utsalgspriser.

Verdier: midtpunkt i det spennet leverandøren oppga (2026-04-24).
"""

from __future__ import annotations


BRAND_MARGIN: dict[str, float] = {
    "COCA COLA": 0.55,
    "FANTA": 0.55,
    "SPRITE": 0.55,
    "URGE": 0.55,
    "POWERADE": 0.55,
    "BONAQUA": 0.55,
    "BURN": 0.50,
    "MONSTER": 0.30,
}


def margin_for_product(product_name: str) -> float:
    """Match produktnavn mot brand-nøkkel. Case-insensitive prefix match."""
    name = product_name.upper()
    # Match mot lengste brand-prefix for å unngå ambiguitet
    for brand in sorted(BRAND_MARGIN, key=len, reverse=True):
        if name.startswith(brand):
            return BRAND_MARGIN[brand]
    raise KeyError(
        f"Ukjent merke for produkt '{product_name}'. "
        f"Legg til i BRAND_MARGIN i margin_mapping.py."
    )


def brand_for_product(product_name: str) -> str:
    name = product_name.upper()
    for brand in sorted(BRAND_MARGIN, key=len, reverse=True):
        if name.startswith(brand):
            return brand
    return "UKJENT"
