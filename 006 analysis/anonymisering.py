"""
Felles anonymiseringsmodul for Coop Extra X-data.

Gir stabile pseudonymer basert på ABC-klasse + rangering, slik at alle
scripts bruker samme koder i rapportene. Navneregisteret lagres i intern/
(gitignored) slik at koblingen reell → pseudo forblir lokalt.

Pseudonym-skjema:
  A-produkter: A1, A2, ... (etter totalsalg desc)
  B-produkter: B1, B2, ...
  C-produkter: C1, C2, ...

Bruk:
    from anonymisering import Anonymizer
    anon = Anonymizer.build_from_sales(df_renset)
    anon.save(intern_dir)                 # lagre navneregister lokalt
    df_a = anon.apply(df_renset)          # bytter produktnavn → pseudonymer
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class Anonymizer:
    """Holder mapping reelt-navn → pseudonym samt ABC-klasse per produkt."""
    mapping: dict[str, str]
    klasse: dict[str, str]

    @classmethod
    def build_from_sales(cls, df: pd.DataFrame,
                         abc_thresholds: tuple[float, float] = (0.80, 0.95)
                         ) -> "Anonymizer":
        """Generer pseudonymer fra rensede salgsdata."""
        tot = df.groupby("Produkt")["Ant_solgt"].sum().sort_values(ascending=False)
        kumulativ = tot.cumsum() / tot.sum()

        klasse: dict[str, str] = {}
        for produkt, pct in kumulativ.items():
            if pct <= abc_thresholds[0]:
                klasse[produkt] = "A"
            elif pct <= abc_thresholds[1]:
                klasse[produkt] = "B"
            else:
                klasse[produkt] = "C"

        # Teller per klasse, rangert etter totalsalg desc
        counters = {"A": 0, "B": 0, "C": 0}
        mapping: dict[str, str] = {}
        for produkt in tot.index:
            cls_ = klasse[produkt]
            counters[cls_] += 1
            mapping[produkt] = f"{cls_}{counters[cls_]}"

        return cls(mapping=mapping, klasse=klasse)

    @classmethod
    def load(cls, path: Path) -> "Anonymizer":
        """Last navneregister fra intern/ lokalitet."""
        df = pd.read_csv(path)
        return cls(
            mapping=dict(zip(df["Produkt"], df["Pseudonym"])),
            klasse=dict(zip(df["Produkt"], df["Klasse"])),
        )

    def save(self, intern_dir: Path) -> Path:
        """Lagre navneregister til intern-mappen (gitignored)."""
        intern_dir.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame([
            {"Produkt": p, "Pseudonym": ps, "Klasse": self.klasse[p]}
            for p, ps in self.mapping.items()
        ]).sort_values("Pseudonym")
        path = intern_dir / "navneregister.csv"
        df.to_csv(path, index=False)
        return path

    def apply(self, df: pd.DataFrame, col: str = "Produkt") -> pd.DataFrame:
        """Returner kopi med produkt-kolonne erstattet av pseudonymer."""
        out = df.copy()
        out[col] = out[col].map(self.mapping)
        if out[col].isnull().any():
            missing = df.loc[out[col].isnull(), col].unique()
            raise KeyError(f"Mangler pseudonym for: {list(missing)}")
        return out

    def pseudo(self, real_name: str) -> str:
        """Hent pseudonym for ett navn."""
        return self.mapping[real_name]

    def sorted_pseudos(self) -> list[str]:
        """Returner pseudonymer sortert A1, A2, B1, B2, C1, ..."""
        order = {"A": 0, "B": 1, "C": 2}
        return sorted(
            self.mapping.values(),
            key=lambda p: (order[p[0]], int(p[1:]))
        )
