# LOG650 G22 — Space Management

LOG650 26V Forskningsprosjekt: Logistikk og kunstig intelligens (HiMolde). Innleveringsfrist **2026-05-31**.

**Gruppe:** Sebastian Vambheim Thunestvedt + Frida Berge-Robertson. Oliver Matre Hille trakk seg 2026-04-24 — ressursfordeling i `prosjektplan.md` er foreldet på dette punktet.

**Tema:** Datadrevet vurdering av hyllekapasitet vs. etterspørsel for en dagligvareleverandør hos Coop Extra X. LP-modell med margin-vektet målfunksjon, ABC-klassifisering og sensitivitetsanalyse.

## Start hver sesjon med å lese disse

- `012 fase 2 - plan/status.md` — autoritativ status (oppdateres løpende)
- `AGENTS.md` — språk-, formatering- og kodekonvensjoner for repoet
- `slagplan-fase3.md` — fem-ukers gjennomføringsplan til 31.05

## Kjernekilder

| Hva | Hvor |
|---|---|
| Hovedrapport | `005 report/rapport.md` (11 kapitler ferdig per 2026-04-27) |
| Analyse-kode | `006 analysis/aktiviteter/3_*` (én mappe per kapittel) |
| Anonymisering | `006 analysis/anonymisering.py` (A1–A14, B1–B9, C1–C11) |
| Margin-mapping | `006 analysis/margin_mapping.py` |
| Rådata (gitignored) | `004 data/raw/` |
| Strukturerte data | `004 data/processed/` |
| Forelesninger (LLM-renset) | `003 references/forelesninger/cleaned_llm/` (31 stk) |
| MS Project-pipeline | `012 fase 2 - plan/` + slash commands `/msproject-*` |

## Konvensjoner

- **Norsk** i all rapporttekst, planfiler og statusfiler. UTF-8 uten BOM.
- **APA 7** for referanser. Alle kilder må eksistere fysisk i `003 references/` — KI-foreslåtte kilder verifiseres alltid.
- **Pseudonymer** i alle versjonerte filer: produkter heter A1–A14, B1–B9, C1–C11. Ekte produktnavn ALDRI i git.
- **Python 3.12 + uv** for hele `006 analysis/`. Felles `uv.lock` commitet.
- **LP-modell:** PuLP + CBC-solver. Margin-vektet målfunksjon (max Σ m_i · y_i) med restriksjoner R1–R5.
- **Figurer:** matplotlib/seaborn/plotly via Python (ikke PowerPoint). HTML-img i rapport.md med 80% bredde, kursiv figurtekst.
- **Filnavn i analyse:** `fig_*.png` og `tab_*.csv` per aktivitetsmappe.

## Sensitive områder

- **`intern/`-mappa** (i 006 analysis) inneholder rapporter med ekte merkenavn — ekskludert fra git via `.gitignore`. Sjekk før commit.
- **Taushetserklæring** med Coop Extra X gjelder. Vedlegg C i rapporten.
- **`.env`** under `003 references/forelesninger/` har ANTHROPIC_API_KEY — gitignored.

## Vanlige operasjoner

```bash
# Kjør LP-modell
cd "006 analysis" && uv run python aktiviteter/3_5_analyse_og_resultater/scripts/03_lp_modell.py

# Generer figurer
uv run python aktiviteter/3_5_analyse_og_resultater/scripts/06_pipeline_diagram.py

# MS Project sync (slash command)
/msproject-sync   # generer XML + valider + verifisér mot Windows-VM

# Rapport → DOCX (pandoc)
pandoc "005 report/rapport.md" -o "005 report/rapport.docx"
```

## Memory (auto-loaded)

Relevante memory-filer ligger under `~/.claude/projects/-Volumes-DevSSD-Projects-LOG650-G22-sfo/memory/`:
- `canonical_files.md` — hva er styrende dokumenter
- `quantitative_methods.md` — metodevalg (LP primær, ABC + sensitivitet støtte)
- `forelesninger.md` — pipeline for forelesningstranskripsjoner
- `team_update.md` — teamendring 2026-04-24
- `current_work.md` — pågående arbeid
- `secondary_exposure_research.md` — Chevalier 1975, k=1.5 default

## Kritisk akkurat nå (per 2026-04-28)

Hovedutkast levert. Peer review-uke (uke 18). 5 uker til innlevering. Fokus: review-tilbakemeldinger, KI-erklæring, anonymiseringssjekk, presentasjons-prep. Se `slagplan-fase3.md` for ukentlig nedbryting.
