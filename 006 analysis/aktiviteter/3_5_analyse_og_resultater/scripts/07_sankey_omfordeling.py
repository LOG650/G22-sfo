#!/usr/bin/env python3
"""
ACT-3.5 Sankey-diagram av omfordelingen i S2 (hovedanbefaling).

Viser hylleplass-flyten fra «Nåværende allokering» til «LP S2 allokering».
Hver SKU er kilde og destinasjon; båndtykkelsen tilsvarer antall facings flyttet.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

REPO_ROOT = Path(__file__).resolve().parents[4]
LP_CSV = (
    REPO_ROOT / "006 analysis" / "aktiviteter"
    / "3_4_data_metode_og_modellering" / "resultat"
    / "lp_allokering_S2_primaer_sek.csv"
)
FIG_DIR = Path(__file__).resolve().parents[1] / "figurer"


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(LP_CSV)
    df = df.rename(columns={df.columns[0]: "Produkt"})

    # Sortér etter klasse (A → B → C) og innen klasse etter produktivitet
    df["klasse"] = df["Produkt"].str[0]
    df = df.sort_values(["klasse", "Produkt"]).reset_index(drop=True)

    df["delta"] = df["facings_optimal"] - df["facings_original"]
    losers = df[df["delta"] < 0].copy()
    winners = df[df["delta"] > 0].copy()

    # Total tap = total gevinst
    total_loss = -losers["delta"].sum()
    total_gain = winners["delta"].sum()
    print(f"Tap fra losers: {total_loss}, gevinst til winners: {total_gain}")

    # Bygg node-liste: alle losers (kilder) + alle winners (mål)
    src_labels = losers["Produkt"].tolist()
    dst_labels = winners["Produkt"].tolist()
    node_labels = src_labels + dst_labels

    # Fargesett — A blå, B grønn, C oransje
    klasse_color = {"A": "#1976D2", "B": "#388E3C", "C": "#F57C00"}
    node_colors = [klasse_color[p[0]] for p in node_labels]

    # Build flows: distribute each loser's loss proportionally across winners
    # by winner's gain (as fraction of total winner gain).
    sources, targets, values = [], [], []
    src_idx = {p: i for i, p in enumerate(src_labels)}
    dst_offset = len(src_labels)

    for _, lr in losers.iterrows():
        lost = -lr["delta"]
        for j, (_, wr) in enumerate(winners.iterrows()):
            share = wr["delta"] / total_gain
            flow = lost * share
            if flow >= 0.5:  # filter ut bittesmå strømmer
                sources.append(src_idx[lr["Produkt"]])
                targets.append(dst_offset + j)
                values.append(round(flow, 1))

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=10,
            thickness=14,
            line=dict(color="#37474F", width=0.5),
            label=node_labels,
            color=node_colors,
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(120,144,156,0.35)",
        ),
    )])
    fig.update_layout(
        title=dict(
            text=("S2 Primær + sekundær — omfordeling av frontfacings "
                  "(blå = A-klasse, grønn = B, oransje = C)"),
            font=dict(size=13),
        ),
        font=dict(family="Helvetica", size=10),
        margin=dict(l=20, r=20, t=60, b=20),
        height=620,
    )

    png_out = FIG_DIR / "sankey_omfordeling_S2.png"
    html_out = FIG_DIR / "sankey_omfordeling_S2.html"
    fig.write_image(png_out, width=1200, height=620, scale=2)
    fig.write_html(html_out, include_plotlyjs="cdn")
    print(f"Lagret: {png_out}")
    print(f"Lagret: {html_out}")


if __name__ == "__main__":
    main()
