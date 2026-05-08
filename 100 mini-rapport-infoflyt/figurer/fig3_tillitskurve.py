"""Figur 3 — Tillit i kunderelasjonen som funksjon av antall kundebesøk.

Modellerer compound erosjon når selger gjentatte ganger besøker samme
kunde med utdatert informasjon. Konseptuell figur — ikke empirisk —
inspirert av Morgan & Hunt (1994).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".png")

besok = np.arange(0, 13)  # 0 til 12 besøk

# Tillit holder seg når selger har oppdatert info (mild slitasje pga. naturlig drift)
tillit_oppdatert = 100 * np.exp(-0.005 * besok)

# Tillit faller raskere når selger gjentatte ganger leverer utdatert info.
# Modelleres som eksponensielt fall mot et nedre platå (~55 %).
platå = 55.0
tillit_utdatert = platå + (100 - platå) * np.exp(-0.25 * besok)

fig, ax = plt.subplots(figsize=(8.5, 4.6))

ax.plot(besok, tillit_oppdatert, marker="o", linewidth=2.0,
        color="#1f6f3f", label="Selger med oppdatert KAM-info")
ax.plot(besok, tillit_utdatert, marker="s", linewidth=2.0,
        color="#c0392b", label="Selger med utdatert KAM-info")

ax.fill_between(besok, tillit_oppdatert, tillit_utdatert,
                color="#c0392b", alpha=0.10)

ax.set_xlabel("Antall besøk hos samme kunde (over 6 måneder)")
ax.set_ylabel("Oppfattet kompetanse / tillit (% av startnivå)")
ax.set_title("Figur 3. Compound erosjon av tillit ved gjentatte uoppdaterte kundebesøk",
             fontsize=11, loc="left")
ax.legend(loc="lower left", fontsize=9, frameon=False)
ax.set_ylim(45, 105)
ax.set_xticks(besok)
ax.grid(True, linestyle=":", alpha=0.4)

ax.text(11.2, 60, "≈ -40 %\ntillit", fontsize=9, color="#c0392b", ha="center")

fig.tight_layout()
fig.savefig(OUT, dpi=180, bbox_inches="tight")
print(f"→ {OUT}")
