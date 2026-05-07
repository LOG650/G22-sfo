# Mini-rapport Informasjonsflyt — Implementasjonsplan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bygge en 6–8 siders fagnotat-PDF som dokumenterer dagens informasjonsflyt-utfordring i en FMCG-salgsorganisasjon og foreslår en porteføljebevisst alternativ-modell, med fem figurer, 14 APA-7-referanser og samme Eisvogel/pandoc-pipeline som LOG650.

**Architecture:** Markdown → PDF via pandoc + Eisvogel-mal + xelatex (TeX Live 2026). Figurer genereres med matplotlib/seaborn fra Python-script i `figurer/`-mappa. APA 7 sitering via `--citeproc` mot `refs.bib` og norsk APA-CSL fra `000 templates/Referansestiler/`. Egen `Makefile` i `100 mini-rapport-infoflyt/` gjenbruker LOG650-konfigurasjon med justerte stier.

**Tech Stack:** Python 3.12 (uv), matplotlib, seaborn, pandoc, pandoc-citeproc, xelatex (TeX Live 2026), Eisvogel-template, BibTeX, APA-7th-norsk CSL.

**Spec:** `100 mini-rapport-infoflyt/docs/superpowers/specs/2026-05-07-mini-rapport-infoflyt-design.md`
**Kildekartlegging:** `100 mini-rapport-infoflyt/research/kildekartlegging.md`

---

## Filstruktur som planen produserer

```
100 mini-rapport-infoflyt/
├── Makefile                         (Task 1)
├── .gitignore                       (Task 1)
├── refs.bib                         (Task 2)
├── figurer/
│   ├── fig2_bullwhip.py            (Task 3)
│   ├── fig2_bullwhip.png            (Task 3 output)
│   ├── fig3_tillitskurve.py         (Task 4)
│   ├── fig3_tillitskurve.png        (Task 4 output)
│   ├── fig4_portefoljematrise.py    (Task 5)
│   ├── fig4_portefoljematrise.png   (Task 5 output)
│   ├── fig1_swimlane.py             (Task 6)
│   ├── fig1_swimlane.png            (Task 6 output)
│   ├── fig5_to_be_hub.py            (Task 7)
│   └── fig5_to_be_hub.png           (Task 7 output)
├── rapport.md                       (Task 8 skjelett, Task 9–14 innhold)
└── output/
    └── rapport.pdf                  (gitignored, build-output)
```

**Konvensjoner:**
- Norsk i all rapporttekst, figurtekster og kommentarer.
- UTF-8 uten BOM.
- Cite-keys i refs.bib bruker etternavn + årstall (f.eks. `lee1997`, `morgan_hunt1994`).
- Figur-script kan kjøres alene fra `100 mini-rapport-infoflyt/`-mappa.
- `make pdf` skal bygge ferdig PDF fra rapport.md uten manuelle skritt.

---

## Task 1: Pipeline-oppsett (Makefile + .gitignore)

**Files:**
- Create: `100 mini-rapport-infoflyt/Makefile`
- Create: `100 mini-rapport-infoflyt/.gitignore`

- [ ] **Step 1: Skriv Makefile**

```makefile
REPORT_DIR  := .
PDFTEMPLATE := ../000 templates/pandoc/eisvogel.latex
SRC         := rapport.md
PDF_OUT     := output/rapport.pdf
BIB         := refs.bib
CSL         := ../000 templates/Referansestiler/apa-7th-norsk.csl

# TeX Live på ekstern disk
TEXLIVE_BIN := /Volumes/DevSSD/texlive/2026/bin/universal-darwin
PDF_PATH    := $(TEXLIVE_BIN):$(PATH)

COMMON_FLAGS := \
	--from=markdown+smart+pipe_tables+yaml_metadata_block+implicit_figures+raw_tex \
	--toc --toc-depth=2 \
	--number-sections \
	--standalone \
	--resource-path=".:figurer"

ifneq (,$(shell command -v pandoc-crossref 2>/dev/null))
COMMON_FLAGS += --filter pandoc-crossref
endif

ifneq (,$(wildcard $(BIB)))
COMMON_FLAGS += --citeproc --bibliography="$(BIB)"
ifneq (,$(wildcard $(CSL)))
COMMON_FLAGS += --csl="$(CSL)"
endif
endif

PDF_FLAGS := $(COMMON_FLAGS) \
	--to=latex \
	--pdf-engine=xelatex \
	--template="$(PDFTEMPLATE)" \
	-V lang=nb-NO \
	-V babel-lang=norsk \
	-V mainfont="Helvetica Neue" \
	-V monofont="Menlo" \
	-V geometry:margin=2.5cm \
	-V titlepage=true \
	-V toc-own-page=false \
	-V colorlinks=true \
	-V linkcolor=Maroon \
	-V urlcolor=NavyBlue \
	-V citecolor=ForestGreen \
	-V titlepage-rule-color=2e2e2e \
	-V book=false \
	-M title="Informasjonsflyt i en FMCG-salgsorganisasjon: diagnose og forslag" \
	-M author="Sebastian V. Thunestvedt" \
	-M date="2026-05"

.PHONY: pdf figurer clean check-deps check-tex

pdf: check-deps check-tex figurer
	@mkdir -p output
	PATH="$(PDF_PATH)" pandoc "$(SRC)" $(PDF_FLAGS) -o "$(PDF_OUT)"
	@echo "→ $(PDF_OUT)"

figurer:
	@for f in figurer/fig*.py; do \
		echo "Genererer $$f"; \
		(cd figurer && python "$$(basename $$f)") || exit 1; \
	done

check-deps:
	@command -v pandoc >/dev/null || { echo "pandoc mangler: brew install pandoc"; exit 1; }
	@command -v python >/dev/null || { echo "python mangler"; exit 1; }

check-tex:
	@test -x "$(TEXLIVE_BIN)/xelatex" || { echo "xelatex ikke funnet i $(TEXLIVE_BIN)"; exit 1; }
	@test -f "$(PDFTEMPLATE)" || { echo "Eisvogel-template mangler: $(PDFTEMPLATE)"; exit 1; }

clean:
	rm -rf output/
```

- [ ] **Step 2: Skriv .gitignore**

```gitignore
output/
__pycache__/
*.pyc
.DS_Store
```

- [ ] **Step 3: Verifiser at make-targets parser**

Run: `cd "100 mini-rapport-infoflyt" && make -n pdf`
Expected: ingen syntaksfeil; viser de planlagte kommandoene (mkdir, pandoc-kall etc.)

- [ ] **Step 4: Commit**

```bash
git add "100 mini-rapport-infoflyt/Makefile" "100 mini-rapport-infoflyt/.gitignore"
git commit -m "Sett opp Makefile og .gitignore for mini-rapport"
```

---

## Task 2: Bibliografi (refs.bib med 14 kilder)

**Files:**
- Create: `100 mini-rapport-infoflyt/refs.bib`

- [ ] **Step 1: Skriv refs.bib med alle 14 kilder**

```bibtex
@book{adamson2015challenger,
  author    = {Adamson, Brent and Dixon, Matthew and Spenner, Pat and Toman, Nick},
  title     = {The Challenger Customer: Selling to the Hidden Influencer Who Can Multiply Your Results},
  publisher = {Portfolio/Penguin},
  address   = {New York},
  year      = {2015}
}

@article{aldrich_herker1977,
  author  = {Aldrich, Howard E. and Herker, Diane},
  title   = {Boundary Spanning Roles and Organization Structure},
  journal = {Academy of Management Review},
  volume  = {2},
  number  = {2},
  pages   = {217--230},
  year    = {1977},
  doi     = {10.5465/AMR.1977.4409044}
}

@book{dixon_adamson2011,
  author    = {Dixon, Matthew and Adamson, Brent},
  title     = {The Challenger Sale: Taking Control of the Customer Conversation},
  publisher = {Portfolio/Penguin},
  address   = {New York},
  year      = {2011}
}

@article{fiocca1982,
  author  = {Fiocca, Renato},
  title   = {Account Portfolio Analysis for Strategy Development},
  journal = {Industrial Marketing Management},
  volume  = {11},
  number  = {1},
  pages   = {53--62},
  year    = {1982},
  doi     = {10.1016/0019-8501(82)90040-1}
}

@misc{forrester_salescomms,
  author       = {{Forrester}},
  title        = {Measuring Revenue Enablement: Sales Communications Effectiveness Defined},
  howpublished = {Forrester Research Report RES180702},
  year         = {n.d.},
  url          = {https://www.forrester.com/report/measuring-revenue-enablement-sales-communications-effectiveness-defined/RES180702}
}

@article{galbraith1974,
  author  = {Galbraith, Jay R.},
  title   = {Organization Design: An Information Processing View},
  journal = {Interfaces},
  volume  = {4},
  number  = {3},
  pages   = {28--36},
  year    = {1974},
  doi     = {10.1287/inte.4.3.28}
}

@book{galbraith2005,
  author    = {Galbraith, Jay R.},
  title     = {Designing the Customer-Centric Organization: A Guide to Strategy, Structure, and Process},
  publisher = {Jossey-Bass},
  address   = {San Francisco},
  year      = {2005}
}

@misc{gartner2024_trends,
  author       = {{Gartner}},
  title        = {Three Trends Chief Sales Officers Must Consider in 2025},
  howpublished = {Press release},
  month        = dec,
  day          = {9},
  year         = {2024},
  url          = {https://www.gartner.com/en/newsroom/press-releases/2024-12-09-three-trends-chief-sales-officers-must-consider-in-2025}
}

@misc{gartner2024_transformation,
  author       = {{Gartner}},
  title        = {Gartner Survey Reveals Only 11\% of Sales Organizations Are Able to Drive Commercial Success While Executing a Transformation},
  howpublished = {Press release},
  month        = dec,
  day          = {18},
  year         = {2024},
  url          = {https://www.gartner.com/en/newsroom/press-releases/2024-12-18-gartner-survey-reveals-only-eleven-percent-of-sales-organizations-are-able-to-drive-commercial-success-while-executing-a-transformation}
}

@article{homburg2008,
  author  = {Homburg, Christian and Jensen, Ove and Krohmer, Harley},
  title   = {Configurations of Marketing and Sales: A Taxonomy},
  journal = {Journal of Marketing},
  volume  = {72},
  number  = {2},
  pages   = {133--154},
  year    = {2008},
  doi     = {10.1509/jmkg.72.2.133}
}

@article{lee1997,
  author  = {Lee, Hau L. and Padmanabhan, V. and Whang, Seungjin},
  title   = {Information Distortion in a Supply Chain: The Bullwhip Effect},
  journal = {Management Science},
  volume  = {43},
  number  = {4},
  pages   = {546--558},
  year    = {1997},
  doi     = {10.1287/mnsc.43.4.546}
}

@article{marcoscuevas2014,
  author  = {Marcos-Cuevas, Javier and N{\"a}tti, Satu and Palo, Teea and Ryals, Lynette J.},
  title   = {Implementing Key Account Management: Intraorganizational Practices and Associated Dilemmas},
  journal = {Industrial Marketing Management},
  volume  = {43},
  number  = {7},
  pages   = {1216--1224},
  year    = {2014},
  doi     = {10.1016/j.indmarman.2014.06.013}
}

@misc{mckinsey2022_hybrid,
  author       = {{McKinsey \& Company}},
  title        = {The Future of B2B Sales is Hybrid},
  year         = {2022},
  url          = {https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/the-future-of-b2b-sales-is-hybrid}
}

@article{morgan_hunt1994,
  author  = {Morgan, Robert M. and Hunt, Shelby D.},
  title   = {The Commitment-Trust Theory of Relationship Marketing},
  journal = {Journal of Marketing},
  volume  = {58},
  number  = {3},
  pages   = {20--38},
  year    = {1994},
  doi     = {10.1177/002224299405800302}
}

@article{shah2006,
  author  = {Shah, Denish and Rust, Roland T. and Parasuraman, A. and Staelin, Richard and Day, George S.},
  title   = {The Path to Customer Centricity},
  journal = {Journal of Service Research},
  volume  = {9},
  number  = {2},
  pages   = {113--124},
  year    = {2006},
  doi     = {10.1177/1094670506294666}
}

@misc{telus2024,
  author       = {{TELUS Agriculture \& Consumer Goods}},
  title        = {Real-Time FMCG Retail Execution: Closing the Gap Between Strategy and Store},
  year         = {2024},
  url          = {https://www.telus.com/agcg/en/blog-resources/real-time-fmcg-retail-execution}
}

@article{zolkiewski2002,
  author  = {Zolkiewski, Judy and Turnbull, Peter},
  title   = {Do Relationship Portfolios and Networks Provide the Key to Successful Relationship Management?},
  journal = {Journal of Business \& Industrial Marketing},
  volume  = {17},
  number  = {7},
  pages   = {575--597},
  year    = {2002},
  doi     = {10.1108/08858620210451100}
}
```

(16 BibTeX-poster — Gartner og Adamson/Dixon teller som to poster hver fordi de har separate inngangspunkter; samlet sett 14 unike kilder slik spec angir, fordelt på 16 bibtex-entries fordi Gartner har to pressemeldinger og Adamson-teamet har to bøker.)

- [ ] **Step 2: Verifiser BibTeX-syntaks**

Run: `cd "100 mini-rapport-infoflyt" && python -c "import bibtexparser; bibtexparser.parse_file('refs.bib')" 2>&1 | head -5`

Hvis `bibtexparser` ikke er installert, fall tilbake til:
Run: `pandoc -s --bibliography=refs.bib --citeproc /dev/null 2>&1 | head -5`
Expected: Ingen feilmelding om manglende felter eller dårlig syntaks.

- [ ] **Step 3: Commit**

```bash
git add "100 mini-rapport-infoflyt/refs.bib"
git commit -m "Legg til refs.bib med 14 kilder for mini-rapport"
```

---

## Task 3: Figur 2 — Bullwhip-analogi (info-forvrengning gjennom ledd)

**Files:**
- Create: `100 mini-rapport-infoflyt/figurer/fig2_bullwhip.py`
- Output: `100 mini-rapport-infoflyt/figurer/fig2_bullwhip.png`

**Hva figuren viser:** Et opprinnelig "rent" informasjonssignal hos KAM forvrenges
og forsterkes gjennom hvert ledd (Direktør → Region → Salgssjef → Selger).
Y-akse: avvik fra original. X-akse: tid. Fire kurver med stigende
varians/forsinkelse.

- [ ] **Step 1: Skriv figur-script**

```python
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
```

- [ ] **Step 2: Kjør og verifiser at PNG genereres**

Run: `cd "100 mini-rapport-infoflyt/figurer" && python fig2_bullwhip.py`
Expected: `→ .../fig2_bullwhip.png` og fil-eksistens bekreftes med `ls -la fig2_bullwhip.png`

- [ ] **Step 3: Visuell sjekk**

Åpne PNG i bilde-viewer (`open fig2_bullwhip.png`) og verifiser:
- Original-signalet (KAM) er en ren steg-funksjon
- Selger-kurven er forsinket og har størst varians
- Tekst leses tydelig
- Figurtekst er på norsk

- [ ] **Step 4: Commit**

```bash
git add "100 mini-rapport-infoflyt/figurer/fig2_bullwhip.py" "100 mini-rapport-infoflyt/figurer/fig2_bullwhip.png"
git commit -m "Legg til figur 2: bullwhip-analogi for info-flyt"
```

---

## Task 4: Figur 3 — Tillitskurve (compound erosjon)

**Files:**
- Create: `100 mini-rapport-infoflyt/figurer/fig3_tillitskurve.py`
- Output: `100 mini-rapport-infoflyt/figurer/fig3_tillitskurve.png`

**Hva figuren viser:** Selger besøker samme kunde 12 ganger over 6 måneder.
Hver gang ny KAM-info er forsinket = tillitstap. Eksponensielt fall fra 100 %
ned mot et lavere platå. To linjer: "med oppdatert info" (holder tilliten),
"med utdatert info" (compound erosjon).

- [ ] **Step 1: Skriv figur-script**

```python
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
```

- [ ] **Step 2: Kjør og verifiser**

Run: `cd "100 mini-rapport-infoflyt/figurer" && python fig3_tillitskurve.py`
Expected: PNG genereres uten feil.

- [ ] **Step 3: Visuell sjekk**

Verifiser:
- Grønn linje (oppdatert) holder seg ~95–100 %
- Rød linje (utdatert) faller bratt og stabiliseres rundt 55–60 %
- Skravert område mellom kurvene viser kostnaden
- Notat "≈ -40 % tillit" leses tydelig

- [ ] **Step 4: Commit**

```bash
git add "100 mini-rapport-infoflyt/figurer/fig3_tillitskurve.py" "100 mini-rapport-infoflyt/figurer/fig3_tillitskurve.png"
git commit -m "Legg til figur 3: tillitskurve compound erosjon"
```

---

## Task 5: Figur 4 — Porteføljematrise (A/B/C × info-type)

**Files:**
- Create: `100 mini-rapport-infoflyt/figurer/fig4_portefoljematrise.py`
- Output: `100 mini-rapport-infoflyt/figurer/fig4_portefoljematrise.png`

**Hva figuren viser:** Heatmap-matrise. Rader: A/B/C-segmenter etter
porteføljeposisjon (Fiocca 1982; Zolkiewski & Turnbull 2002). Kolonner:
typer informasjon (pris, kampanje, listing, lager, kundespesifikk).
Cellefarge = hastenivå (hvor raskt info må til selger).

- [ ] **Step 1: Skriv figur-script**

```python
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
```

- [ ] **Step 2: Kjør og verifiser**

Run: `cd "100 mini-rapport-infoflyt/figurer" && python fig4_portefoljematrise.py`
Expected: PNG genereres uten feil.

- [ ] **Step 3: Visuell sjekk**

Verifiser:
- A-segmentet er rødt/oransje (haster)
- C-segmentet er grønt (batch OK)
- Tekstetiketter i celler er lesbare
- Fargebar viser fire nivåer

- [ ] **Step 4: Commit**

```bash
git add "100 mini-rapport-infoflyt/figurer/fig4_portefoljematrise.py" "100 mini-rapport-infoflyt/figurer/fig4_portefoljematrise.png"
git commit -m "Legg til figur 4: portefolje-matrise hastighet vs info-type"
```

---

## Task 6: Figur 1 — Swimlane (dagens kaskade med tidsstempler)

**Files:**
- Create: `100 mini-rapport-infoflyt/figurer/fig1_swimlane.py`
- Output: `100 mini-rapport-infoflyt/figurer/fig1_swimlane.png`

**Hva figuren viser:** Vertikal swimlane med 5 baner (KAM, Direktør,
Regionssjef, Salgssjef, Selger). Tidsakse horisontal (dager 0–7). Bokser
viser når informasjonen ankommer hver bane. Piler mellom banene viser
forsinkelse. Røde markører på dager der "ny info som burde nådd selger
tidligere" akkumuleres.

- [ ] **Step 1: Skriv figur-script**

```python
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
```

- [ ] **Step 2: Kjør og verifiser**

Run: `cd "100 mini-rapport-infoflyt/figurer" && python fig1_swimlane.py`
Expected: PNG genereres uten feil.

- [ ] **Step 3: Visuell sjekk**

Verifiser:
- 5 horisontale baner med navn til venstre
- 5 bokser (én per ledd) med tekst om hva som skjer
- Piler mellom bokser viser forsinkelse i dager
- Røde trekanter for selgerens kundebesøk
- Selgerens første A-kundebesøk (dag 1,5) skjer FØR selger får info (dag 5,5)

- [ ] **Step 4: Commit**

```bash
git add "100 mini-rapport-infoflyt/figurer/fig1_swimlane.py" "100 mini-rapport-infoflyt/figurer/fig1_swimlane.png"
git commit -m "Legg til figur 1: swimlane av dagens info-kaskade"
```

---

## Task 7: Figur 5 — To-be hub-and-spoke

**Files:**
- Create: `100 mini-rapport-infoflyt/figurer/fig5_to_be_hub.py`
- Output: `100 mini-rapport-infoflyt/figurer/fig5_to_be_hub.png`

**Hva figuren viser:** Hub-and-spoke. KAM er sentrum (hub), selger og
ledere er spokes. Direkte kanal KAM → selger for haste-info. Ledere er
ikke borte — de får parallell strøm for koordinering. Verktøy-laget i
midten (mobil app / shared dashboard).

- [ ] **Step 1: Skriv figur-script**

```python
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
```

- [ ] **Step 2: Kjør og verifiser**

Run: `cd "100 mini-rapport-infoflyt/figurer" && python fig5_to_be_hub.py`
Expected: PNG genereres uten feil.

- [ ] **Step 3: Visuell sjekk**

Verifiser:
- Hub i midten ("Delt info-lag")
- 6 spokes rundt: KAM (top), Selger (bottom), 4 andre roller
- KAM og Selger har heltrukne tykkere linjer
- Andre ledd har stiplede tynnere linjer

- [ ] **Step 4: Commit**

```bash
git add "100 mini-rapport-infoflyt/figurer/fig5_to_be_hub.py" "100 mini-rapport-infoflyt/figurer/fig5_to_be_hub.png"
git commit -m "Legg til figur 5: to-be hub-and-spoke arkitektur"
```

---

## Task 8: Skjelett rapport.md (frontmatter + 7 tomme kapitler)

**Files:**
- Create: `100 mini-rapport-infoflyt/rapport.md`

- [ ] **Step 1: Skriv skjelett**

````markdown
---
title: "Informasjonsflyt i en FMCG-salgsorganisasjon: diagnose og forslag"
subtitle: "Et internt arbeidsdokument fra selgerperspektiv"
author: "Sebastian V. Thunestvedt"
date: "Mai 2026"
lang: nb-NO
---

# 1. Innledning {#sec:innledning}

<!-- Skrives i Task 14 -->
*[Plassholder — innledning skrives sist når kapittel 2–6 er ferdige.]*

# 2. Dagens modell — slik fungerer informasjonsflyten i dag {#sec:as-is}

<!-- Skrives i Task 10 -->
*[Plassholder — beskrivelse av kaskaden + figur 1 swimlane.]*

# 3. Litteraturramme — hvorfor kaskaden svikter {#sec:litteratur}

<!-- Skrives i Task 9 -->
*[Plassholder — bullwhip + boundary spanner + Galbraith + commitment-trust + Challenger.]*

# 4. Diagnose — operativ og relasjonell pris {#sec:diagnose}

<!-- Skrives i Task 11 -->
*[Plassholder — kostnadsmodell + tillitskurve.]*

# 5. Alternativ modell — porteføljebevisst informasjonsflyt {#sec:to-be}

<!-- Skrives i Task 12 -->
*[Plassholder — porteføljematrise + hub-and-spoke.]*

# 6. Implementasjon og risiko {#sec:implementasjon}

<!-- Skrives i Task 13 -->
*[Plassholder — tre skritt + det vi ikke foreslår.]*

# 7. Kilder

<!-- Genereres automatisk av pandoc-citeproc fra refs.bib -->
::: {#refs}
:::
````

- [ ] **Step 2: Verifiser at pandoc parser frontmatter**

Run: `cd "100 mini-rapport-infoflyt" && pandoc rapport.md --citeproc --bibliography=refs.bib --csl="../000 templates/Referansestiler/apa-7th-norsk.csl" --to=html -o /tmp/test.html && head -20 /tmp/test.html`
Expected: HTML genereres uten feil; tittel og forfatter er synlig.

- [ ] **Step 3: Commit**

```bash
git add "100 mini-rapport-infoflyt/rapport.md"
git commit -m "Legg til rapport.md skjelett med frontmatter og 7 kapitler"
```

---

## Task 9: §3 Litteraturramme

**Files:**
- Modify: `100 mini-rapport-infoflyt/rapport.md` (kapittel 3)

**Mål:** ~440–500 ord. Plasserer figur 2 (bullwhip-analogi). Henter inn
sentrale narrativer fra kildekartleggingen for å forklare *hvorfor*
kaskaden svikter.

- [ ] **Step 1: Skriv §3-innholdet**

Erstatt `*[Plassholder — bullwhip + boundary spanner + Galbraith + commitment-trust + Challenger.]*` med:

````markdown
Litteraturen tilbyr fire linser som hver enkelt beskriver en del av problemet,
og som samlet forklarer hvorfor en hierarkisk kaskade leverer for sent
i en hektisk hverdag.

**Bullwhip — informasjon forvrenges gjennom ledd.** Lee, Padmanabhan &
Whang [-@lee1997] viste i sin klassiker fra *Management Science* at
etterspørselssignaler forvrenges og forsterkes når de passerer gjennom
ledd i en forsyningskjede. Mekanismene de identifiserte —
signalprosessering, rasjoneringsspill, ordrebatching og prisvariasjoner —
har analoger i intern informasjonsflyt: hvert ledelseslag tolker, prioriterer,
ompakker og forsinker. Anbefalingen deres er like aktuell internt som i
forsyningskjeden: del data direkte med dem som bruker den, ikke gjennom
mellomledd.

![*Figur 2. Bullwhip-analogi: et rent informasjonssignal hos KAM forvrenges og
forsinkes gjennom hvert ledd i kaskaden, før det når selger.*](figurer/fig2_bullwhip.png){ width=80% }

**Selger som grenserolle.** Aldrich og Herker [-@aldrich_herker1977]
viste at *boundary-spanning roles* har to funksjoner: prosessering av
informasjon inn til organisasjonen, og representasjon utad. Selger er en
arketypisk grenserolle. Når informasjonsstrømmen *til* grenserollen er
treg, svikter både inngangen (markedsinnsikt blir ikke fanget) og
utgangen (selger representerer en utdatert organisasjon). Homburg, Jensen
og Krohmer [-@homburg2008] dokumenterer empirisk at de mest vellykkede
salg-/marketing-konfigurasjonene kjennetegnes av sterke strukturelle
koblinger mellom funksjonene — ikke av kaskader.

**Hierarkiet er for smalt for hektisk hverdag.** Galbraith
[-@galbraith1974] argumenterte for at oppgave-usikkerhet — det vil si
hvor mye informasjon organisasjonen må behandle for å fungere — øker
behovet for informasjonsbehandlingskapasitet. Når oppgaven krever mer enn
hierarkiet kan levere, må organisasjonen utvides med *lateral relations*
(tverrgående grupper, integrator-roller, direkte kontakt) eller
*vertikale informasjonssystemer* (IT). I oppfølgeren *Designing the
Customer-Centric Organization* [@galbraith2005] understreker han at en
KAM-tittel ikke er nok — strukturen, prosessene og målingene må faktisk
levere informasjonen til der kunden møtes. Shah med flere [-@shah2006]
finner det samme: kundesentrisitet feiler typisk på fire barrierer —
kultur, struktur, prosess og målinger.

**Tillit er beholdningsverdien som forvitrer.** Morgan og Hunt
[-@morgan_hunt1994] sin *commitment-trust*-teori viser at langvarige
relasjoner styres av tillit, og at tillit produseres når den andre
parten konsistent leverer kompetanse — og brytes ned av oppfattet
inkompetanse eller upålitelighet. Dixon og Adamson [-@dixon_adamson2011]
finner i CEB-data at **53 % av B2B-kundens lojalitet** driver fra
*salgs-opplevelsen* (innsikt, utfordring, tilpasning) — ikke fra produkt
eller pris. En selger som besøker kunden uten oppdatert informasjon
leverer det motsatte av en Challenger.

Til slutt: praktikerlitteratur fra Gartner [-@gartner2024_transformation]
og Forrester [-@forrester_salescomms] dokumenterer at problemet ikke er
informasjonsmangel, men feil tid og format — 70 % av selgerne i Gartners
2024-undersøkelse rapporterer at de er overveldet av antallet
teknologier de må bruke.

````

- [ ] **Step 2: Bygg PDF og verifiser**

Run: `cd "100 mini-rapport-infoflyt" && make pdf 2>&1 | tail -10`
Expected: PDF genereres; ingen "Citation not found"-advarsler.

Run: `pandoc rapport.md --citeproc --bibliography=refs.bib --csl="../000 templates/Referansestiler/apa-7th-norsk.csl" --to=html 2>&1 | grep -i "citation not found" || echo "Alle siteringer funnet"`
Expected: "Alle siteringer funnet"

- [ ] **Step 3: Commit**

```bash
git add "100 mini-rapport-infoflyt/rapport.md"
git commit -m "Skriv §3 Litteraturramme med fire linser + figur 2"
```

---

## Task 10: §2 Dagens modell (as-is)

**Files:**
- Modify: `100 mini-rapport-infoflyt/rapport.md` (kapittel 2)

**Mål:** ~440–500 ord. Plasserer figur 1 (swimlane). Beskriver
kaskaden konkret med roller og typiske forsinkelser.

- [ ] **Step 1: Skriv §2-innholdet**

Erstatt plassholderen i §2 med:

````markdown
I en typisk FMCG-salgsorganisasjon fungerer informasjonsflyten ned mot
selger som en **firetrinns kaskade**:

> KAM → Direktør → Regionssjef → Salgssjef → Selger

Omtrent 90 % av selgerens inngående arbeidsinformasjon — pris,
kampanjer, listinger, lager, kundespesifikke beslutninger — har
opprinnelsen sin i KAM-teamet. Et execution-team opererer på siden av
linjeorganisasjonen og bidrar med operative koordineringsoppgaver. KAM
sitter sentralt og avtaler kategori- og kundebeslutninger med kjeden;
direktør, regionssjef og salgssjef har hver sin koordinerende rolle.
Selger er nederst — og samtidig den som besøker kunden hver dag.

![*Figur 1. Dagens informasjonsflyt: kaskade fra KAM til selger med
typiske tidsforsinkelser. Røde trekanter markerer kundebesøk som ofte
skjer før selger har mottatt den nye informasjonen.*](figurer/fig1_swimlane.png){ width=80% }

I praksis ser det ut omtrent som figur 1. KAM beslutter en ny
kampanjepris dag null. Direktør videresender e-post dag én. Regionssjef
diskuterer det i ukesmøtet dag to-tre. Salgssjef videresender til felt
dag fire. Selger leser e-posten dag fem-seks — to dager etter at samme
selger var hos en A-kunde og presenterte forrige ukes priser.

Tre strukturelle trekk forsterker dette mønsteret:

**Mange kokker.** Informasjon kommer ikke bare fra KAM. Kategori,
marketing, supply, brand management, finans og execution-team genererer
også beskjeder mot felt — alle gjennom sine egne kanaler. Selger må
selv filtrere hva som er relevant, hva som er duplisert, og hva som er
utdatert. Forrester [-@forrester_salescomms] dokumenterer at selgere i
snitt bruker 1,9 timer per uke på å behandle interne kommunikasjons-
meldinger — uten at det nødvendigvis betyr at de er informert.

**Hver leder filtrerer.** Hvert ledd i kaskaden gjør en
nytte-vurdering: er dette relevant for mine selgere akkurat nå?
Resultatet er at lederen ofte holder informasjon tilbake til neste
fellesmøte, eller pakker den om i egne ord. Dette er ikke uflaks — det
er en rasjonell respons på begrensede møtearenaer og overvåking-
kapasitet. Men effekten er forsinkelse og forvrengning.

**Selgerens kalender venter ikke.** En selger med 60–80 kunder i en
rute besøker hver kunde 4–8 ganger i året. Dagen er strukturert rundt
kundebesøk, ikke rundt e-postlesing eller møter. Det betyr at
informasjon som ankommer dag fem ofte havner *etter* at selgeren
allerede har vært hos kunden i henhold til sin rute — og kunden får
informasjonen fra et annet hold før selgeren får mulighet til å bringe
den.

Resultatet av disse tre trekkene oppsummeres enkelt: selger får riktig
informasjon, men på feil tidspunkt.
````

- [ ] **Step 2: Bygg PDF og verifiser**

Run: `cd "100 mini-rapport-infoflyt" && make pdf 2>&1 | tail -5`
Expected: Bygger uten feil.

- [ ] **Step 3: Commit**

```bash
git add "100 mini-rapport-infoflyt/rapport.md"
git commit -m "Skriv §2 Dagens modell med figur 1 swimlane"
```

---

## Task 11: §4 Diagnose

**Files:**
- Modify: `100 mini-rapport-infoflyt/rapport.md` (kapittel 4)

**Mål:** ~440–500 ord. Plasserer figur 3 (tillitskurve). Operativ
+ relasjonell pris. Hypotetisk kostnadsmodell tydelig merket.

- [ ] **Step 1: Skriv §4-innholdet**

Erstatt plassholderen i §4 med:

````markdown
Kostnaden av treg informasjonsflyt har to ansikter: en operativ pris
som er enkel å regne på, og en relasjonell pris som er vanskeligere å
måle, men sannsynligvis større.

**Den operative prisen.** Når selger får ny informasjon etter at
kunden er besøkt, finnes det to handlingsalternativer: besøke kunden
på nytt, eller la være. Begge koster.

En enkel modell — *illustrativ, ikke empirisk* — gjør størrelsesorden
synlig. Anta:

- 50 selgere i salgsstyrken
- 2 ekstra kundebesøk per selger per uke som direkte konsekvens av
  forsinket informasjon
- 1,5 time per ekstra besøk inkludert reise og forberedelse

Det gir 50 × 2 × 1,5 = **150 timer per uke**, som tilsvarer omtrent
fire fulltids-årsverk. Med en realistisk timekost havner man fort i
millionklassen i året — for én organisasjon. Tallene er illustrative og
varierer med rutestørrelse og informasjonstetthet, men poenget står:
selv en moderat informasjonsforsinkelse summerer seg raskt når den
gjentas på tvers av en hel salgsstyrke i en hel uke.

**Den relasjonelle prisen.** Selger forvalter ikke en transaksjonskø,
men en portefølje av kunder som besøkes 4–8 ganger i året. Hver gang
samme A-kunde møter en selger som ikke vet om kampanjen kunden allerede
har lest om, eroderer relasjonens kvalitet litt. Effekten er
*compound*: tap i tidlig periode forsterker tapet i neste periode.

![*Figur 3. Konseptuell modell av tillitserosjon ved gjentatte
uoppdaterte kundebesøk. Den røde kurven illustrerer compound-effekten
når selger gjentatte ganger møter samme kunde uten oppdatert
informasjon. Figuren er illustrativ — ikke empirisk.*](figurer/fig3_tillitskurve.png){ width=80% }

Morgan og Hunt [-@morgan_hunt1994] sin *commitment-trust*-teori
forklarer mekanismen: tillit produseres av oppfattet kompetanse og
pålitelighet, og brytes ned av det motsatte. En selger som tre ganger
på rad ikke kjente til en kampanjepris kunden allerede hadde sett,
oppfattes ikke som en strategisk samarbeidspartner — men som
"ordretaker fra leverandøren". Dixon og Adamson [-@dixon_adamson2011]
sin Challenger-undersøkelse viser at 53 % av kundens lojalitet driver
fra hvilken type interaksjon selger leverer. En relasjon basert på
utdatert informasjon er per definisjon *anti-Challenger*.

**Symptom eller årsak?** Det er fristende å lese disse kostnadene som
"selger jobber ikke effektivt nok" eller "ledere må kommunisere
bedre". Men diagnosen er strukturell. Galbraith [-@galbraith1974]
formulerer det presist: når oppgave-usikkerheten øker uten at
informasjonsbehandlingskapasiteten øker tilsvarende, faller ytelsen.
FMCG-hverdagen i 2026 er ikke roligere enn den var i 1995 da
fire-leddskaskaden ble innført — den er hektigere. Tiltaket er ikke å
løpe raskere i samme system, men å bygge ut selve kapasiteten.

Det leder til neste kapittel: hvordan kapasiteten kan bygges ut.
````

- [ ] **Step 2: Bygg og verifiser**

Run: `cd "100 mini-rapport-infoflyt" && make pdf 2>&1 | tail -5`

- [ ] **Step 3: Commit**

```bash
git add "100 mini-rapport-infoflyt/rapport.md"
git commit -m "Skriv §4 Diagnose med tillitskurve og kostnadsmodell"
```

---

## Task 12: §5 Alternativ modell

**Files:**
- Modify: `100 mini-rapport-infoflyt/rapport.md` (kapittel 5)

**Mål:** ~700–800 ord. Plasserer figur 4 (porteføljematrise) og
figur 5 (hub-and-spoke). Konkret to-be med rutinger og verktøy.

- [ ] **Step 1: Skriv §5-innholdet**

Erstatt plassholderen i §5 med:

````markdown
Den foreslåtte modellen bygger på tre prinsipper hentet fra
litteraturen: differensier informasjonen etter porteføljesegment, kort
ned avstanden mellom kilde (KAM) og bruker (selger), og bevar lederne
sin koordinerende rolle uten å la dem være flaskehalsen for
hastighetskritisk informasjon.

## 5.1 Differensier etter porteføljesegment

Ikke all informasjon er like haste-kritisk, og ikke alle kunder krever
samme tempo. Fiocca [-@fiocca1982] og Zolkiewski og Turnbull
[-@zolkiewski2002] tilbyr et språk for dette: kundene segmenteres etter
strategisk verdi og kompleksitet, og ressursene differensieres
deretter. Samme prinsipp gjelder informasjonsflyt.

![*Figur 4. Differensiert informasjonshastighet per porteføljesegment.
Strategiske A-kunder krever umiddelbar varsling for kundespesifikk og
prisrelatert informasjon, mens C-kunder kan håndteres i ukentlige
batcher.*](figurer/fig4_portefoljematrise.png){ width=80% }

For en strategisk A-kunde må kundespesifikk informasjon, prisendringer
og kampanjebeslutninger nå selger umiddelbart — i praksis innen samme
arbeidsdag som beslutningen tas. For en C-kunde i volumsegmentet er en
ukentlig batch tilstrekkelig. Mellomsegmentet B faller imellom: samme
dag for kritisk info, innen uken for normal driftsinformasjon.

Dette er ikke en organisatorisk omveltning — det er en
prioriteringsregel som kan implementeres uten at man rør selve
linjeorganisasjonen.

## 5.2 Direkte KAM ↔ selger via et delt info-lag

I dag flyter informasjonen fra KAM gjennom fire ledelsesledd før den
når selger. To av disse leddene legger til reell beslutnings-verdi
(direktør og regionssjef vurderer strategiske implikasjoner). De to
andre fungerer i praksis som en ren videresending av e-post — med
forsinkelse og tap.

Den foreslåtte arkitekturen erstatter videresending med direkte tilgang
gjennom et delt informasjons-lag. KAM publiserer informasjonen ett
sted; selger leser den der. Lederne får parallell tilgang for
koordinering og oversikt — men de er ikke lenger en flaskehals i
kjeden.

![*Figur 5. Foreslått hub-and-spoke-arkitektur. KAM eier kilden, selger
har direkte pull-tilgang via et delt info-lag (mobil + dashboard).
Lederne har parallell strøm for koordinering og strategi, ikke for
videresending.*](figurer/fig5_to_be_hub.png){ width=80% }

Dette korresponderer med Galbraith [-@galbraith1974] sin anbefaling om
*lateral relations* og *vertikale informasjonssystemer* — ikke som
erstatning for hierarkiet, men som utvidelse av dets kapasitet.
Praktikerlitteraturen viser at modne verktøy for nettopp dette
eksisterer i FMCG-segmentet: TELUS [-@telus2024] og lignende
leverandører dokumenterer **18–25 % økt selgerproduktivitet** ved
overgang til real-time retail execution-plattformer.

McKinsey [-@mckinsey2022_hybrid] viser at to tredeler av B2B-vinnerne
har konto-nivå informasjons-tilgang for selgere; bare halvparten av
de tregere har det samme. Forskjellen er ikke flere e-poster — det er
en annen arkitektur.

## 5.3 Tre rutings-prinsipper

Tre konkrete rutinger oversetter prinsippene til hverdag:

1. **Kundespesifikk og hastekritisk informasjon for A-/B-kunder
   ruter direkte fra KAM til selger** via push-varsling i et delt
   verktøy. Direktør og regionssjef ser samme informasjon i sitt
   dashbord, men trenger ikke å videresende den.
2. **Generell kampanje- og prisinformasjon publiseres i et felles
   feed** med rolle- og porteføljebasert filtrering, slik Forrester
   [-@forrester_salescomms] anbefaler. Selger ser bare det som er
   relevant for sin rute og sitt kundesegment.
3. **Strategisk og taktisk koordinering forblir i ledergruppene** —
   regionssjef og salgssjef bruker informasjonen til å prioritere,
   coache og beslutte ressursfordeling, men de er ikke
   informasjonens transportlag.

Resultatet er en arkitektur som *legger til* hastighet og
porteføljedifferensiering uten å ta bort lederrollene som
koordinatorer.
````

- [ ] **Step 2: Bygg og verifiser**

Run: `cd "100 mini-rapport-infoflyt" && make pdf 2>&1 | tail -5`

- [ ] **Step 3: Commit**

```bash
git add "100 mini-rapport-infoflyt/rapport.md"
git commit -m "Skriv §5 Alternativ modell med portefolje-matrise og hub-figur"
```

---

## Task 13: §6 Implementasjon og risiko

**Files:**
- Modify: `100 mini-rapport-infoflyt/rapport.md` (kapittel 6)

**Mål:** ~175–250 ord. Tre konkrete skritt + det vi ikke foreslår.

- [ ] **Step 1: Skriv §6-innholdet**

Erstatt plassholderen i §6 med:

````markdown
Forslaget kan tas i tre skritt.

**Skritt 1 — pilot på A-kunder.** Definer porteføljematrisen (figur 4)
for ett distrikt eller én kategori. Etabler en direkte kanal mellom
KAM og selger for kundespesifikk og pris-relatert informasjon for
A-kunder. Mål: tid fra KAM-beslutning til selger-mottak på A-kunde-
informasjon (target: under 24 timer). Tidsramme: 6–8 uker.

**Skritt 2 — utvid med shared feed.** Utvid den direkte kanalen til en
felles feed med rolle- og porteføljebasert filtrering. Ledere får
parallell tilgang. Verktøy: enten eksisterende salgsplattform med
utvidelse, eller et lett retail execution-tilskudd (figur 5). Mål:
redusere "intern e-post"-tid for selger fra ~1,9 t/uke
[@forrester_salescomms] til under 1 t/uke.

**Skritt 3 — institusjonaliser KPI-er og målinger.** Shah med flere
[-@shah2006] er klar på at kundesentrisitet svikter når målingene ikke
følger med. Mål tid-til-felt for ny KAM-informasjon, andel besøk med
oppdatert informasjon, og A-kunde-tillit (NPS eller tilsvarende) i
ledelsesdashbord.

**Det forslaget *ikke* gjør.** Det rør ikke linjeorganisasjonen,
fjerner ikke lederlag, og innfører ikke nye rapporteringskrav nedover.
Det legger heller ikke opp til å erstatte mellommenneskelig
koordinering med teknologi — verktøyene er hjelp, ikke svar. Risikoen
ligger ikke i å innføre dette stegvis; den ligger i å la status quo
fortsette i en hverdag som blir hektigere år for år.
````

- [ ] **Step 2: Bygg og verifiser**

Run: `cd "100 mini-rapport-infoflyt" && make pdf 2>&1 | tail -5`

- [ ] **Step 3: Commit**

```bash
git add "100 mini-rapport-infoflyt/rapport.md"
git commit -m "Skriv §6 Implementasjon og risiko"
```

---

## Task 14: §1 Innledning (skrives sist) + sluttsjekk av §7

**Files:**
- Modify: `100 mini-rapport-infoflyt/rapport.md` (kapittel 1)

**Mål:** ~280–320 ord. Selger-perspektiv i førsteperson. Konkret
smerte-anekdote. Tese.

- [ ] **Step 1: Skriv §1-innholdet**

Erstatt plassholderen i §1 med:

````markdown
Som selger i en FMCG-organisasjon kjenner jeg dette mønsteret godt.
Jeg besøker en strategisk viktig kunde mandag morgen — gjennomgår
sortimentet, snakker om neste kampanje, planlegger plassering i
butikken. Onsdag ettermiddag treffer en e-post innboksen min: KAM har
forhandlet en ny kampanjepris som gjelder fra denne uken. Den
informasjonen burde jeg hatt mandag.

Konsekvensen er enkel: enten reiser jeg tilbake til kunden — som
koster en halv dag og bryter kundens egen ruteplanlegging — eller jeg
lar være. Begge alternativene er dårlige. Det første er ineffektivt;
det andre eroderer kundens oppfatning av at jeg er en oppdatert
samarbeidspartner.

Jeg skriver dette dokumentet fordi mønsteret ikke er en personlig
uflaks, og fordi det ikke skyldes at noen i kjeden gjør jobben sin
dårlig. KAM tar gode beslutninger. Direktør, regionssjef og salgssjef
gjør sin del. Selve modellen — informasjon som flyter gjennom fire
ledd før den når feltet — er den som ikke holder takten i en hverdag
preget av ukentlige kampanjer, raskt skiftende kundekrav og en
voksende kundeportefølje per selger.

Dette dokumentet har tre formål. Først å beskrive dagens modell og
tidsforsinkelsene den produserer. Deretter å vise — gjennom etablert
litteratur — hvorfor problemet er strukturelt og forutsigbart. Til
slutt å foreslå en alternativ informasjonsflyt-modell som er
porteføljebevisst, kort på avstand mellom KAM og selger, og som
bevarer lederlagene som koordinatorer uten å la dem være
flaskehalser.

Hovedbudskapet kan formuleres slik: dagens kaskade ble bygget for en
roligere hverdag enn den vi har. Resultatet er ikke bare ekstra
besøk — det er compound erosjon av tilliten i en kundeportefølje som
er beholdningsverdien vår. Løsningen finnes i etablert litteratur og
i modne verktøy, og kan innføres stegvis.
````

- [ ] **Step 2: Bygg og verifiser at hele PDF-en bygges**

Run: `cd "100 mini-rapport-infoflyt" && make pdf 2>&1 | tail -5`
Expected: PDF genereres uten feil.

Run: `cd "100 mini-rapport-infoflyt" && pandoc rapport.md --citeproc --bibliography=refs.bib --csl="../000 templates/Referansestiler/apa-7th-norsk.csl" --to=html 2>&1 | grep -i "warning\|citation not found" | head`
Expected: Ingen output, eller bare uskyldige advarsler.

- [ ] **Step 3: Commit**

```bash
git add "100 mini-rapport-infoflyt/rapport.md"
git commit -m "Skriv §1 Innledning fra selger-perspektiv"
```

---

## Task 15: Sluttpolering + sidetelling + final build

**Files:**
- Modify: `100 mini-rapport-infoflyt/rapport.md` (justeringer)
- Output: `100 mini-rapport-infoflyt/output/rapport.pdf`

- [ ] **Step 1: Bygg PDF og åpne**

Run: `cd "100 mini-rapport-infoflyt" && make clean && make pdf && open output/rapport.pdf`
Expected: PDF åpnes i Preview/forhåndsvisning.

- [ ] **Step 2: Verifiser sidetall**

Tell sider: skal være 6–8 sider inkludert tittelside og kilder.

Hvis < 6 sider: ikke noe å gjøre — innholdet er kompakt nok.
Hvis > 8 sider: kutt eksempler, ikke poenger. Typiske kandidater for
kutt:
- Lengre eksempel-anekdoter i §1 og §2
- Underseksjon 5.3 hvis 5.1 og 5.2 dekker tilstrekkelig
- Reduser figurbredde fra 80% til 70% hvis figurer dominerer

- [ ] **Step 3: Visuell konsistens-sjekk**

Åpne hver figur og verifiser:
- Konsistent fontstørrelse i figurtekst (8–11 pt)
- Konsistent fargebruk (blå/grønn/rød har samme betydning på tvers)
- Alle figurtekster på norsk
- Ingen avkuttet tekst

- [ ] **Step 4: APA-referansesjekk**

Run: `cd "100 mini-rapport-infoflyt" && grep -oE "@[a-z_]+[0-9]+(_[a-z]+)?" rapport.md | sort -u`
Verifiser at hver cite-key finnes som BibTeX-entry i refs.bib:

Run: `cd "100 mini-rapport-infoflyt" && for key in $(grep -oE "@[a-z_]+[0-9]+(_[a-z]+)?" rapport.md | sort -u | sed 's/@//'); do grep -q "^@.*{$key," refs.bib && echo "OK: $key" || echo "MANGLER: $key"; done`
Expected: Alle "OK: ..."; ingen "MANGLER: ...".

- [ ] **Step 5: Språk-/typo-sjekk**

Les igjennom hele PDF-en. Spesielt:
- Tese i §1 og hovedbudskap i §6 stemmer overens
- Figur 1 refereres i §2, figur 2 i §3, figur 3 i §4, figur 4 og 5 i §5
- Alle siterings-formuleringer er på norsk ("med flere", "viser at", etc.)
- Konsistens i tegnsetting (norsk anførselstegn « » eller "" — én stil hele veien)

- [ ] **Step 6: Final commit**

```bash
git add "100 mini-rapport-infoflyt/rapport.md"
git commit -m "Sluttpolering av mini-rapport: sidetall, figurkonsistens, APA-sjekk"
```

- [ ] **Step 7: Build-output (valgfri commit)**

Hvis du ønsker å committe selve PDF-en (bemerk at output/ er i .gitignore):

```bash
git add -f "100 mini-rapport-infoflyt/output/rapport.pdf"
git commit -m "Legg til ferdig PDF av mini-rapport"
```

Eller la PDF-en være ute av versjonskontroll og bygges på nytt fra
kilde ved behov.

---

## Etter implementasjon

Mini-rapporten ligger ferdig i `100 mini-rapport-infoflyt/output/rapport.pdf`.
For nye iterasjoner: rediger `rapport.md`, kjør `make pdf`, commit endringer.

For å dele rapporten: PDF-en er selvstendig (kilder embeddet via citeproc).
Den kan sendes som e-postvedlegg til ledelsen.
