"""Figur 5 — Foreslått to-be informasjonsarkitektur (hub-and-spoke).

KAM som hub. Selger får direkte tilgang til kundespesifikk og haste-info
via et delt verktøylag. Ledere får parallell koordinerings-strøm uten
å være flaskehals.
"""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".png")

fig, ax = plt.subplots(figsize=(8.5, 6.0))
ax.set_aspect("equal")
ax.set_xlim(-5, 5)
ax.set_ylim(-4.5, 4.5)
ax.axis("off")

# Sentrum: shared info-lag
hub = mpatches.FancyBboxPatch((-1.3, -0.6), 2.6, 1.2,
                              boxstyle="round,pad=0.1",
                              linewidth=1.6, edgecolor="#1f4068",
                              facecolor="#dde9f2")
ax.add_patch(hub)
ax.text(0, 0.15, "Delt info-lag", ha="center", va="center",
        fontsize=11, fontweight="bold", color="#1f4068")
ax.text(0, -0.25, "(mobilapp + dashboard)", ha="center", va="center",
        fontsize=8, color="#1f4068")

# Spokes — definerer rolle, posisjon (vinkel), farge
spokes = [
    ("KAM",        90,  "#1f6f3f", "Eier kilden\n(pris, kampanje, listing)"),
    ("Selger",    -90,  "#c0392b", "Direkte pull av\nhaste-info"),
    ("Salgssjef", 210,  "#888888", "Koordinering,\nikke flaskehals"),
    ("Region",    150,  "#888888", "Aggregert KPI,\nikke videresending"),
    ("Direktør",   30,  "#888888", "Strategi,\nbeslutninger"),
    ("Execution",  -30, "#888888", "Operative\noppgaver"),
]

R = 3.2
for name, deg, color, sub in spokes:
    rad = np.deg2rad(deg)
    x, y = R * np.cos(rad), R * np.sin(rad)
    ax.add_patch(mpatches.Circle((x, y), 0.55, edgecolor=color,
                                 facecolor="white", linewidth=1.8))
    ax.text(x, y + 0.08, name, ha="center", va="center",
            fontsize=10, fontweight="bold", color=color)
    # Sub-tekst utenfor sirkelen
    sx = x + 0.95 * np.cos(rad)
    sy = y + 0.95 * np.sin(rad)
    ax.text(sx, sy, sub, ha="center", va="center", fontsize=7.5,
            color=color, alpha=0.9)

    # Linje fra hub til spoke
    is_primary = name in ("KAM", "Selger")
    lw = 2.4 if is_primary else 1.2
    ls = "-" if is_primary else "--"
    alpha = 1.0 if is_primary else 0.55
    ax.plot([0, x * 0.83], [0, y * 0.83],
            color=color, linewidth=lw, linestyle=ls, alpha=alpha)

ax.text(0, 4.1, "Figur 5. Foreslått informasjonsarkitektur — hub-and-spoke med direkte KAM ↔ selger",
        ha="center", fontsize=11, fontweight="bold", color="#1f4068")
ax.text(0, -4.1,
        "Heltrukken linje = direkte info-flyt. Stiplet = parallell koordinering, ikke flaskehals.",
        ha="center", fontsize=8.5, color="#555")

fig.tight_layout()
fig.savefig(OUT, dpi=180, bbox_inches="tight")
print(f"→ {OUT}")
