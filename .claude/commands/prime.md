---
description: Sesjonsstart — les Tier 1-filer, git-historikk, rapport status. Tar valgfritt kapittel/aktivitet for Tier 2-load.
argument-hint: [kapittel eller aktivitet du skal jobbe med — valgfritt]
allowed-tools: Bash, Read, Glob, Grep
---

Du starter en ny sesjon på LOG650 G22-prosjektet (Space Management for Coop-leverandør). Bygg opp kontekst på under 30 sekunder.

## Steg 1 — Tier 1-filer (les alltid)

Les disse parallelt:
- @CLAUDE.md
- @AGENTS.md
- @012 fase 2 - plan/status.md
- @slagplan-fase3.md

## Steg 2 — Git-orientering

Kjør i parallell:

```bash
git log --oneline -15
git status --short
git branch --show-current
git diff --stat HEAD~5..HEAD 2>/dev/null | tail -5
```

## Steg 3 — Sanity-sjekk

Verifiser at ingen sensitive filer er endret eller utracket:

```bash
git status --porcelain | grep -E "intern/|\.env|^\?\? .*\.csv" | head -10
```

## Steg 4 — Oppsummer for brukeren (5 linjer maks)

- **Hvor er vi:** milepæl (M2/M3), uke i slagplanen, dager til 31.05
- **Siste arbeid:** topp 3 commits parafrasert
- **Pågående:** hva står øverst i status.md "Pågående / neste"
- **Advarsler:** ucommitterte endringer i `intern/`, manglende sync, etc.
- **Denne uka iflg slagplan:** kort sammenfatning

## Steg 5 — Hvis $ARGUMENTS er gitt

Last Tier 2-filer for det aktuelle kapittelet/aktiviteten:

| Argument inneholder | Last også |
|---|---|
| §4 / case | `006 analysis/aktiviteter/3_3_*/scripts/01_datarensing.py`, `resultat/datarensing-rapport.md` |
| §5 / metode / data | `006 analysis/anonymisering.py`, `006 analysis/margin_mapping.py`, `006 analysis/aktiviteter/3_4_*/resultat/deskriptiv-og-abc-rapport.md` |
| §6 / modell / LP | `006 analysis/aktiviteter/3_4_*/scripts/03_lp_modell.py` |
| §7 / analyse / resultat / sensitivitet | `006 analysis/aktiviteter/3_4_*/resultat/lp-scenarier-oppsummering.md`, `006 analysis/aktiviteter/3_5_*/scripts/04_sensitivitet.py` |
| §2 / §3 / litteratur / teori | `003 references/kildevurdering-2026-04-24.md` + ls `003 references/*.pdf` |
| §10 / bibliografi / APA | `003 references/kildevurdering-2026-04-24.md`, sammenlign mot bibliografien i rapport.md |
| MS Project / plan | `012 fase 2 - plan/schedule.json`, `wbs.json`, `core.json` |

## Steg 6 — Spør

Avslutt med: **"Hva skal vi jobbe med i denne sesjonen?"** (med mindre $ARGUMENTS allerede sa det — da: foreslå første konkrete handling).

## Last aldri

For å spare kontekst:
- `006 analysis/aktiviteter/*/resultat/intern/` (gitignored, ekte merkenavn)
- `003 references/forelesninger/raw_srt/`, `clean_txt/`, `.chunks/` (bruk kun `cleaned_llm/` ved behov)
- `005 report/rapport.docx` (generert)
- `__pycache__/`, `.venv/`, `.pytest_cache/`
- `015 Prosjektinformasjon/`, `Research/`, `011 fase 1*/`, `013 fase 3*/`, `014 fase 4*/`
