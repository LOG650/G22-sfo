---
description: Oppdater schedule.json automatisk med PM-eide datoendringer fra MS Project XML
argument-hint: [--xml PATH] [--dry-run]
allowed-tools: Bash, Read
---

Kjør apply-sync: anvend PM-eide datoendringer fra en MS Project XML tilbake til `schedule.json` automatisk. Konflikter på dev-eide felt (navn, %) hoppes over og flagges for manuell gjennomgang. Lager backup `schedule.json.bak` før skriving.

Eventuelle argumenter fra brukeren: $ARGUMENTS

Utfør:

```
python3 "004 data/apply_diff.py" $ARGUMENTS
```

Etter kjøring:
1. Rapporter hvor mange endringer som ble anvendt (PM-eid) og hoppet over (konflikt)
2. Liste opp PM-lagt til oppgaver som krever manuell håndtering
3. Påpek at backup ligger i `schedule.json.bak` hvis endringer ble gjort
4. Foreslå å re-generere XML med `/msproject-generate` for å sync frem mapping-filen
