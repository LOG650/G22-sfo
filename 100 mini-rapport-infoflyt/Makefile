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
