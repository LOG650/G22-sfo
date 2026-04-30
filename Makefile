REPORT_DIR := 005 report
TEMPLATE   := 000 templates/Mal prosjekt LOG650 v2.docx
SRC        := $(REPORT_DIR)/rapport.md
OUT        := $(REPORT_DIR)/rapport.docx
BIB        := $(REPORT_DIR)/references.bib
CSL        := 000 templates/Referansestiler/apa-7th-norsk.csl

PANDOC_FLAGS := \
	--from=markdown+smart+pipe_tables+yaml_metadata_block+implicit_figures+raw_tex \
	--to=docx \
	--reference-doc="$(TEMPLATE)" \
	--toc --toc-depth=3 \
	--number-sections \
	--standalone \
	--resource-path="$(REPORT_DIR):."

ifneq (,$(shell command -v pandoc-crossref 2>/dev/null))
PANDOC_FLAGS += --filter pandoc-crossref
endif

ifneq (,$(wildcard $(BIB)))
PANDOC_FLAGS += --citeproc --bibliography="$(BIB)"
ifneq (,$(wildcard $(CSL)))
PANDOC_FLAGS += --csl="$(CSL)"
endif
endif

.PHONY: docx clean check-deps

docx: check-deps
	pandoc "$(SRC)" $(PANDOC_FLAGS) -o "$(OUT)"
	@echo "→ $(OUT)"

check-deps:
	@command -v pandoc >/dev/null || { echo "pandoc mangler: brew install pandoc"; exit 1; }
	@command -v pandoc-crossref >/dev/null || echo "tips: brew install pandoc-crossref for figur/tabell-kryssref"

clean:
	rm -f "$(OUT)"
