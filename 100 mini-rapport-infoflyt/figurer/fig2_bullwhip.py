"""Figur 2 — Bullwhip-analogi for intern informasjonsflyt.

Viser hvordan et rent informasjonssignal hos KAM forvrenges og forsterkes
nedover kaskaden av ledelsesledd. Inspirert av Lee, Padmanabhan & Whang
(1997) sin bullwhip-figur i Management Science.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".png")

rng = np.random.default_rng(seed=42)
t = np.linspace(0, 14, 200)  # 14 dager

# Originalsignalet hos KAM: en steg-endring (ny kampanjepris) på dag 3
signal_kam = np.where(t < 3, 0.0, 1.0)

# Hvert ledd legger til (a) tidsforsinkelse og (b) støy/overreaksjon.
def cascade(signal, delay_days, noise_sigma, gain):
    delayed = np.interp(t - delay_days, t, signal, left=0.0)
    noise = rng.normal(0, noise_sigma, size=t.size)
    return gain * delayed + noise

signal_dir = cascade(signal_kam, delay_days=1.0, noise_sigma=0.06, gain=1.05)
signal_reg = cascade(signal_dir, delay_days=1.5, noise_sigma=0.10, gain=1.10)
signal_sjf = cascade(signal_reg, delay_days=1.5, noise_sigma=0.14, gain=1.15)
signal_sel = cascade(signal_sjf, delay_days=2.0, noise_sigma=0.20, gain=1.20)

fig, ax = plt.subplots(figsize=(8.5, 4.6))

ax.plot(t, signal_kam, label="KAM (kilde)", linewidth=2.2, color="#1f4068")
ax.plot(t, signal_dir, label="Direktør", linewidth=1.6, color="#2c6e9f", alpha=0.85)
ax.plot(t, signal_reg, label="Regionssjef", linewidth=1.4, color="#4a8fc3", alpha=0.8)
ax.plot(t, signal_sjf, label="Salgssjef", linewidth=1.3, color="#7eb1d7", alpha=0.75)
ax.plot(t, signal_sel, label="Selger", linewidth=1.6, color="#c0392b", alpha=0.95)

ax.axvline(3, linestyle="--", color="grey", alpha=0.6, linewidth=0.8)
ax.text(3.1, 1.55, "Ny info\nhos KAM", fontsize=8.5, color="grey")

ax.set_xlabel("Dager etter at informasjonen ble produsert hos KAM")
ax.set_ylabel("Informasjon mottatt (skalert)")
ax.set_title("Figur 2. Bullwhip-analogi: informasjon forvrenges og forsinkes gjennom ledd",
             fontsize=11, loc="left")
ax.legend(loc="lower right", fontsize=9, frameon=False)
ax.set_ylim(-0.3, 1.8)
ax.grid(True, linestyle=":", alpha=0.4)

fig.tight_layout()
fig.savefig(OUT, dpi=180, bbox_inches="tight")
print(f"→ {OUT}")
