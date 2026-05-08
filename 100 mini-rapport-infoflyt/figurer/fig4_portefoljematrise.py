"""Figur 4 — Porteføljedifferensiert informasjonsbehov.

Heatmap som viser hvor raskt ulike typer informasjon må nå selger,
differensiert per porteføljesegment. Bygger på Fiocca (1982) og
Zolkiewski & Turnbull (2002).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".png")

segmenter = ["A — strategisk\n(høy verdi, høy kompleksitet)",
             "B — vekstkunde\n(middels verdi)",
             "C — volum/standard\n(lav kompleksitet)"]

info_typer = ["Kunde-\nspesifikk", "Pris", "Kampanje", "Listing", "Lager"]

# Hastenivå: 1 = umiddelbart, 2 = samme dag, 3 = innen uken, 4 = batch ukentlig
data = np.array([
    [1, 1, 1, 2, 2],   # A
    [2, 2, 2, 3, 3],   # B
    [3, 3, 3, 4, 4],   # C
])

labels = {1: "Umidd.", 2: "Dag", 3: "Uke", 4: "Batch"}

fig, ax = plt.subplots(figsize=(8.5, 4.6))

cmap = plt.cm.RdYlGn_r  # rød = haster, grønn = batch
im = ax.imshow(data, cmap=cmap, vmin=1, vmax=4, aspect="auto")

# Annoter hver celle
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        ax.text(j, i, labels[data[i, j]],
                ha="center", va="center",
                color="white" if data[i, j] <= 2 else "black",
                fontsize=10, fontweight="bold")

ax.set_xticks(range(len(info_typer)))
ax.set_xticklabels(info_typer, fontsize=9)
ax.set_yticks(range(len(segmenter)))
ax.set_yticklabels(segmenter, fontsize=9)

ax.set_title("Figur 4. Differensiert informasjonshastighet per porteføljesegment",
             fontsize=11, loc="left")

cbar = fig.colorbar(im, ax=ax, ticks=[1, 2, 3, 4], shrink=0.7)
cbar.ax.set_yticklabels(["Umiddelbart", "Samme dag", "Innen uken", "Ukentlig batch"],
                        fontsize=8)

fig.tight_layout()
fig.savefig(OUT, dpi=180, bbox_inches="tight")
print(f"→ {OUT}")
