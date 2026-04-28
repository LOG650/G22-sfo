#!/usr/bin/env python3
"""
ACT-3.5 Pipeline-flytdiagram via Graphviz.

Produserer et oversiktsdiagram av analyse-pipelinen som vedlegg/figur i §5/§11:
rådata → datarensing → deskriptiv+ABC → LP-modell → sensitivitet → rapport.
"""

from __future__ import annotations

from pathlib import Path

import graphviz

FIG_DIR = Path(__file__).resolve().parents[1] / "figurer"


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    g = graphviz.Digraph(
        "pipeline",
        format="png",
        graph_attr={
            "rankdir": "LR",
            "fontname": "Helvetica",
            "fontsize": "11",
            "bgcolor": "white",
            "splines": "ortho",
            "nodesep": "0.4",
            "ranksep": "0.55",
        },
        node_attr={
            "fontname": "Helvetica",
            "fontsize": "10",
            "shape": "box",
            "style": "rounded,filled",
            "color": "#37474F",
            "penwidth": "1.2",
        },
        edge_attr={
            "fontname": "Helvetica",
            "fontsize": "9",
            "color": "#546E7A",
            "arrowsize": "0.7",
        },
    )

    # Datakilder
    g.node("raw", "Sell-out CSV\n(uke 06–15 2026)\n34 SKU + margin",
           fillcolor="#FFE082")
    g.node("plan", "Planogram\n(frontfacings\nper SKU)", fillcolor="#FFE082")
    g.node("margin", "Margin-mapping\n(brutto % per SKU)", fillcolor="#FFE082")

    # Trinn
    g.node("clean", "01 Datarensing\npandas + anonymisering",
           fillcolor="#B3E5FC")
    g.node("desc", "02 Deskriptiv + ABC\nutnyttelse, Pareto",
           fillcolor="#B3E5FC")
    g.node("lp", "03 LP-modell (PuLP/CBC)\nmax Σ m·y\ns.t. primær + sekundær",
           fillcolor="#A5D6A7")
    g.node("sens", "04 Sensitivitet\noverserve × x_min",
           fillcolor="#A5D6A7")

    # Outputs
    g.node("fig", "Figurer\n(matplotlib, seaborn,\nplotly Sankey)",
           fillcolor="#FFCCBC")
    g.node("rep", "Rapport\n§5 + §6 + §7 + §8",
           fillcolor="#FFCCBC", shape="folder")

    # Edges
    g.edge("raw", "clean")
    g.edge("plan", "clean")
    g.edge("margin", "lp", style="dashed", label="m_i")
    g.edge("clean", "desc", label="renset")
    g.edge("desc", "lp", label="ρ_i, c_i")
    g.edge("lp", "sens", label="LP-grunn")
    g.edge("lp", "fig", label="S1/S2/S3")
    g.edge("sens", "fig", label="heatmap")
    g.edge("desc", "fig", label="ABC, mismatch")
    g.edge("fig", "rep")
    g.edge("lp", "rep", style="dashed", label="tabeller")

    out = FIG_DIR / "analyse_pipeline"
    g.render(out, cleanup=True)
    print(f"Lagret: {out}.png")


if __name__ == "__main__":
    main()
