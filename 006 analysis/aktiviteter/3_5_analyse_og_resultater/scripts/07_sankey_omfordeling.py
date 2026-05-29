#!/usr/bin/env python3
"""
ACT-3.5 Sankey-diagram av omfordelingen i S2 (hovedanbefaling).

Genererer to versjoner:
  - sankey_omfordeling_S2_aggregert.png/html  — ABC-aggregert (5 noder), egnet for hovedtekst
  - sankey_omfordeling_S2.png/html            — full per-SKU-versjon (vedlegg)

Begge viser hylleplass-flyten fra «Nåværende allokering» til «LP S2 allokering».
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

    # ----- Aggregert ABC-versjon (for hovedtekst) -----
    klasse_color = {"A": "#1976D2", "B": "#388E3C", "C": "#F57C00"}
    src_nodes = []   # (label, klasse, total_loss)
    dst_nodes = []   # (label, klasse, total_gain)
    for k in ("A", "B", "C"):
        loss_k = -losers.loc[losers["klasse"] == k, "delta"].sum()
        gain_k = winners.loc[winners["klasse"] == k, "delta"].sum()
        if loss_k > 0:
            src_nodes.append((f"Over-allokerte {k}-SKUer", k, loss_k))
        if gain_k > 0:
            dst_nodes.append((f"Under-allokerte {k}-SKUer", k, gain_k))

    agg_node_labels = [n[0] for n in src_nodes] + [n[0] for n in dst_nodes]
    agg_node_colors = [klasse_color[n[1]] for n in src_nodes] + [klasse_color[n[1]] for n in dst_nodes]

    total_gain_agg = sum(n[2] for n in dst_nodes)
    agg_sources, agg_targets, agg_values = [], [], []
    for i, src in enumerate(src_nodes):
        for j, dst in enumerate(dst_nodes):
            share = dst[2] / total_gain_agg
            flow = src[2] * share
            if flow >= 0.5:
                agg_sources.append(i)
                agg_targets.append(len(src_nodes) + j)
                agg_values.append(round(flow, 1))

    fig_agg = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=30,
            thickness=22,
            line=dict(color="#37474F", width=0.8),
            label=agg_node_labels,
            color=agg_node_colors,
        ),
        link=dict(
            source=agg_sources,
            target=agg_targets,
            value=agg_values,
            color="rgba(120,144,156,0.45)",
        ),
    )])
    fig_agg.update_layout(
        title=dict(
            text=("S2 — omfordeling av hylleenheter aggregert per ABC-klasse "
                  "(blå = A, grønn = B, oransje = C)"),
            font=dict(size=14),
        ),
        font=dict(family="Helvetica", size=13),
        margin=dict(l=20, r=20, t=70, b=20),
        height=420,
    )
    agg_png = FIG_DIR / "sankey_omfordeling_S2_aggregert.png"
    agg_html = FIG_DIR / "sankey_omfordeling_S2_aggregert.html"
    fig_agg.write_image(agg_png, width=1100, height=420, scale=2)
    fig_agg.write_html(agg_html, include_plotlyjs="cdn")
    print(f"Lagret: {agg_png}")
    print(f"Lagret: {agg_html}")


if __name__ == "__main__":
    main()
