REPORT_DIR  := 005 report
TEMPLATE    := 000 templates/Mal prosjekt LOG650 v2.docx
PDFTEMPLATE := 000 templates/pandoc/eisvogel.latex
SRC         := $(REPORT_DIR)/rapport.md
OUT         := $(REPORT_DIR)/rapport.docx
PDF_OUT     := $(REPORT_DIR)/rapport.pdf
BIB         := $(REPORT_DIR)/references.bib
CSL         := 000 templates/Referansestiler/apa-7th-norsk.csl

# TeX Live på ekstern disk — leggs til PATH for pdf-target
TEXLIVE_BIN := /Volumes/DevSSD/texlive/2026/bin/universal-darwin
PDF_PATH    := $(TEXLIVE_BIN):$(PATH)

COMMON_FLAGS := \
	--from=markdown+smart+pipe_tables+yaml_metadata_block+implicit_figures+raw_tex \
	--toc --toc-depth=3 \
	--number-sections \
	--shift-heading-level-by=-1 \
	--standalone \
	--resource-path="$(REPORT_DIR):."

ifneq (,$(shell command -v pandoc-crossref 2>/dev/null))
COMMON_FLAGS += --filter pandoc-crossref
endif

# Bruk `shell test -f` i stedet for `wildcard` — sistnevnte håndterer ikke
# mellomrom i sti (f.eks. "005 report/") og dropper bibflagget stille.
ifeq (1,$(shell test -f "$(BIB)" && echo 1))
COMMON_FLAGS += --citeproc --bibliography="$(BIB)"
ifeq (1,$(shell test -f "$(CSL)" && echo 1))
COMMON_FLAGS += --csl="$(CSL)"
endif
endif

DOCX_FLAGS := $(COMMON_FLAGS) --to=docx --reference-doc="$(TEMPLATE)"

PDF_FLAGS := $(COMMON_FLAGS) \
	--to=latex \
	--pdf-engine=xelatex \
	--template="$(PDFTEMPLATE)" \
	--include-in-header="000 templates/pandoc/header-includes.tex" \
	-V lang=nb-NO \
	-V babel-lang=norsk \
	-V mainfont="texgyrepagella-regular.otf" \
	-V mainfontoptions:Path="/Volumes/DevSSD/texlive/2026/texmf-dist/fonts/opentype/public/tex-gyre/" \
	-V mainfontoptions:BoldFont="texgyrepagella-bold.otf" \
	-V mainfontoptions:ItalicFont="texgyrepagella-italic.otf" \
	-V mainfontoptions:BoldItalicFont="texgyrepagella-bolditalic.otf" \
	-V monofont="Menlo" \
	-V geometry:margin=2.5cm \
	-V titlepage=true \
	-V toc-own-page=true \
	-V lof=true \
	-V lot=true \
	-V colorlinks=true \
	-V linkcolor=Maroon \
	-V urlcolor=NavyBlue \
	-V citecolor=ForestGreen \
	-V titlepage-rule-color=2e2e2e \
	-M title="Datadrevet vurdering av hyllekapasitet vs. etterspørsel (Space Management) i dagligvarebutikk" \
	-M subtitle="LOG650 26V — Forskningsprosjekt: Logistikk og kunstig intelligens" \
	-M author="Frida Berge-Robertson; Sebastian Vambheim Thunestvedt" \
	-V supervisor="Per Kristian Rekdal og Bård-Inge Pettersen" \
	-V institute="Høgskolen i Molde — Vitenskapelig høgskole i logistikk" \
	-V course="Avdeling for logistikk" \
	-V studypoints="15" \
	-M date="Molde, 2026-05-31"

.PHONY: docx pdf pdf-intern clean check-deps check-tex

docx: check-deps
	pandoc "$(SRC)" $(DOCX_FLAGS) -o "$(OUT)"
	@echo "→ $(OUT)"

pdf: check-deps check-tex
	PATH="$(PDF_PATH)" pandoc "$(SRC)" $(PDF_FLAGS) -o "$(REPORT_DIR)/rapport.tex"
	cd "$(REPORT_DIR)" && PATH="$(PDF_PATH)" latexmk -xelatex -interaction=nonstopmode -halt-on-error rapport.tex >/dev/null
	cd "$(REPORT_DIR)" && PATH="$(PDF_PATH)" latexmk -c rapport.tex >/dev/null
	rm -f "$(REPORT_DIR)/rapport.tex"
	@echo "→ $(PDF_OUT)"

# Usensorert intern PDF — KUN FOR LOKAL BRUK, INNEHOLDER NDA-MATERIALE
# Forutsetter at rapport_intern.md er generert med 006 analysis/usensorering.py
pdf-intern: check-deps check-tex
	@test -f "$(REPORT_DIR)/rapport_intern.md" || { echo "Kjør først: cd '006 analysis' && uv run python usensorering.py"; exit 1; }
	@mkdir -p "$(REPORT_DIR)/intern"
	PATH="$(PDF_PATH)" pandoc "$(REPORT_DIR)/rapport_intern.md" $(PDF_FLAGS) \
		-o "$(REPORT_DIR)/rapport_intern.tex"
	cd "$(REPORT_DIR)" && PATH="$(PDF_PATH)" latexmk -xelatex -interaction=nonstopmode -halt-on-error rapport_intern.tex >/dev/null
	cd "$(REPORT_DIR)" && PATH="$(PDF_PATH)" latexmk -c rapport_intern.tex >/dev/null
	mv "$(REPORT_DIR)/rapport_intern.pdf" "$(REPORT_DIR)/intern/rapport_intern.pdf"
	rm -f "$(REPORT_DIR)/rapport_intern.tex"
	@echo "→ $(REPORT_DIR)/intern/rapport_intern.pdf  (INTERN — IKKE DELES)"

check-deps:
	@command -v pandoc >/dev/null || { echo "pandoc mangler: brew install pandoc"; exit 1; }
	@command -v pandoc-crossref >/dev/null || echo "tips: brew install pandoc-crossref for figur/tabell-kryssref"

check-tex:
	@test -x "$(TEXLIVE_BIN)/xelatex" || { echo "xelatex ikke funnet i $(TEXLIVE_BIN) — kjør TeX Live-installasjonen først"; exit 1; }
	@test -f "$(PDFTEMPLATE)" || { echo "Eisvogel-template mangler: $(PDFTEMPLATE)"; exit 1; }

clean:
	rm -f "$(OUT)" "$(PDF_OUT)"
