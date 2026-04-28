---
description: Avslutt sesjonen — oppsummer arbeid, oppdater status.md + schedule.json, regenerer MS Project XML, foreslå commit
argument-hint: [valgfri kontekst eller aktivitets-ID, f.eks. ACT-3.5]
allowed-tools: Bash, Read, Edit, Write
---

Du avslutter en arbeidsøkt på LOG650 G22. Brukerkontekst: $ARGUMENTS

## Steg 1 — Kartlegg endringer

```bash
git status --short
git diff --stat
git log --oneline -5
```

## Steg 2 — Oppsummer arbeidet (3-5 punkter)

Basert på:
- Filer endret/lagt til/slettet
- Samtalehistorikk i denne sesjonen
- Eventuell brukerkommentar i $ARGUMENTS

Skriv i klartekst hva som ble gjort. Vær konkret med filnavn og innholdsendringer.

## Steg 3 — Sanity-sjekk FØR endringer commits

**STOPP-betingelser** — meld til bruker og avbryt hvis truffet:

```bash
# Endringer i intern/ (skal aldri versjoneres)
git status --porcelain | grep "intern/" && echo "ADVARSEL: intern/ endret"

# .env eller hemmeligheter
git diff --name-only | grep -E "\.env$|credentials|api[_-]?key" -i

# Mistanke om ekte merkenavn i versjonerte filer (be brukeren oppgi merkenavn-tabell hvis usikker)
grep -nE "Tine|Q-Meieriene|Synnøve" "005 report/rapport.md" 2>/dev/null | head -5
```

(Dette er ikke uttømmende — be brukeren verifisere mot `006 analysis/anonymisering.py`-mappingen.)

## Steg 4 — Oppdater `012 fase 2 - plan/status.md`

1. Les nåværende status.md
2. Foreslå konkrete edits:
   - Oppdater `Statusdato:` på toppen til i dag
   - Flytt aktiviteter fra "Pågående / neste" til "Gjennomført"-tabellen hvis fullført
   - Legg til nye linjer i "Pågående / neste" hvis nye oppgaver oppstod
   - Oppdater "Vurdering"-seksjonen hvis risikoer endret seg
3. **Vis diff for brukeren og spør om bekreftelse FØR Edit kjøres.**

## Steg 5 — Oppdater `012 fase 2 - plan/schedule.json`

Hvis sesjonen relateres til en aktivitet (ACT-X.X):

1. Identifiser aktiviteten — be brukeren bekrefte ID hvis uklart. Liste tilgjengelige:
   ```bash
   python3 -c "import json; d=json.load(open('012 fase 2 - plan/schedule.json')); [print(f\"{a['activityId']:12s} {a['status']:12s} {a['percentComplete']:3d}%  {a['name'][:60]}\") for a in d['schedule']['activities']]"
   ```

2. Foreslå oppdateringer (vis diff før Edit):
   - `percentComplete`: oppdatert prosent (0-100)
   - `status`: `not-started` → `in-progress` → `completed`
   - `execution.lastEvent`: én setning hva som ble gjort i denne sesjonen
   - `execution.startedAt`: hvis status nettopp gikk til `in-progress`
   - `execution.completedAt`: hvis status nettopp gikk til `completed`
   - `execution.sessionId`: kort kode (f.eks. dato + initialer)
   - Toppnivå `audit.updatedAt`: ISO-tidsstempel nå
   - Toppnivå `audit.updatedBy`: kort beskrivelse (f.eks. "/handoff fra sebastian")

3. Be om bekreftelse, gjør Edit.

## Steg 6 — Regenerer MS Project XML

Hvis `schedule.json`, `wbs.json`, eller `core.json` ble endret:

```bash
python3 "004 data/generate_msproject_from_json.py"
python3 "004 data/validate_msproject_xml.py" --xsd auto
```

Hvis SSH-VM er konfigurert, kjør også verify (best-effort):
```bash
python3 "004 data/msproject_ssh.py" check 2>/dev/null && \
  python3 "004 data/msproject_ssh.py" verify "004 data/LOG650_G22_from_json.xml"
```

Rapporter resultatet kort. Hvis validering feiler: STOPP og rapporter — sannsynligvis bug i generator eller manuell feil i JSON.

## Steg 7 — Foreslå commit

1. Norsk commit-melding, **maks 70 tegn på første linje**, evt. lengre body for kontekst.
2. Eksempler på tone:
   - `Oppdater §7 sensitivitet med 2D-heatmap og diskuter implikasjoner`
   - `Rens datarensingsskript og legg til docstring per funksjon`
3. Vis foreslått melding + git-add-plan til brukeren.
4. **Ikke commit automatisk.** Vent på bekreftelse.
5. **Aldri push.** Det skal brukeren gjøre manuelt.

## Steg 8 — Avsluttende huskeliste

Sjekk at brukeren har:
- [ ] Lagret eventuell upoplerett tekst (rapport.md autosaves vanligvis)
- [ ] Kommentert konsekvenser av sesjonen i status.md hvis det er noe peer-reviewer eller fagansvarlig bør merke seg
- [ ] Vurdert om noen memory-filer skulle oppdateres

Avslutt med kort kvittering: "Sesjon avsluttet. X aktiviteter oppdatert, Y filer endret, neste fokus iflg slagplan: ..."
