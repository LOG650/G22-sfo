"""Figur 1 — Swimlane av dagens informasjonsflyt fra KAM til selger.

Visualiserer kaskaden KAM → Direktør → Regionssjef → Salgssjef → Selger
med tidsforsinkelser. Selgerens kundebesøk markeres for å vise at info
ofte ankommer etter at besøket er gjennomført.
"""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".png")

baner = ["Selger", "Salgssjef", "Regionssjef", "Direktør", "KAM"]
y_pos = {bane: i for i, bane in enumerate(baner)}

fig, ax = plt.subplots(figsize=(9.5, 4.8))

# Bane-bakgrunn
for i, bane in enumerate(baner):
    color = "#f5f5f5" if i % 2 == 0 else "#ebebeb"
    ax.axhspan(i - 0.4, i + 0.4, color=color, zorder=0)
    ax.text(-0.4, i, bane, fontsize=10, fontweight="bold",
            ha="right", va="center")

# Tidsstempler (dager)
arrivals = [
    ("KAM",        0.0, "Ny kampanje\nbesluttet"),
    ("Direktør",   1.2, "E-post\nvideresendt"),
    ("Regionssjef", 2.5, "Diskutert i\nukesmøte"),
    ("Salgssjef",  4.0, "Videresendt\ntil felt"),
    ("Selger",     5.5, "Selger leser\ne-post"),
]

box_color = "#2c6e9f"
for bane, day, label in arrivals:
    y = y_pos[bane]
    ax.add_patch(mpatches.FancyBboxPatch(
        (day - 0.25, y - 0.18), 0.5, 0.36,
        boxstyle="round,pad=0.02",
        linewidth=1.2, edgecolor=box_color, facecolor="white"))
    ax.text(day, y, label, fontsize=8, ha="center", va="center")

# Piler mellom ledd
for (b1, d1, _), (b2, d2, _) in zip(arrivals[:-1], arrivals[1:]):
    y1, y2 = y_pos[b1], y_pos[b2]
    ax.annotate("", xy=(d2 - 0.27, y2), xytext=(d1 + 0.27, y1),
                arrowprops=dict(arrowstyle="->", color="#888",
                                linewidth=1.2, alpha=0.85))
    delay = d2 - d1
    ax.text((d1 + d2) / 2, (y1 + y2) / 2 + 0.15,
            f"+{delay:.1f} d", fontsize=8, color="#666",
            ha="center")

# Selgerens kundebesøk
visits = [(1.5, "Besøk\nA-kunde"), (3.5, "Besøk\nB-kunde"), (5.0, "Besøk\nA-kunde")]
for day, label in visits:
    ax.scatter(day, y_pos["Selger"] - 0.55, marker="v",
               s=140, color="#c0392b", zorder=5)
    ax.text(day, y_pos["Selger"] - 0.85, label, fontsize=8,
            color="#c0392b", ha="center")

ax.set_xlim(-1.0, 7.2)
ax.set_ylim(-1.4, len(baner) - 0.3)
ax.set_xlabel("Dager fra KAM beslutter ny info")
ax.set_yticks([])
ax.set_title("Figur 1. Dagens informasjonsflyt: kaskade fra KAM til selger med tidsforsinkelse",
             fontsize=11, loc="left")
ax.grid(axis="x", linestyle=":", alpha=0.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Forklaring
ax.text(7.0, -1.2, "▼ = selgerens kundebesøk", fontsize=8,
        color="#c0392b", ha="right")

fig.tight_layout()
fig.savefig(OUT, dpi=180, bbox_inches="tight")
print(f"→ {OUT}")
