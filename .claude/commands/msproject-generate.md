---
description: Generer MS Project XML (MSPDI) fra JSON-kildene i '012 fase 2 - plan/'
argument-hint: [--dry-run] [--no-mapping] [--output PATH]
allowed-tools: Bash
---

Kjør generatoren som konverterer JSON-kildene (`core.json`, `wbs.json`, `schedule.json`) til en MSPDI XML-fil som MS Project åpner direkte. Behold stabile UIDs via `msproject-mapping.json`.

Eventuelle argumenter fra brukeren: $ARGUMENTS

Utfør:

```
python3 "004 data/generate_msproject_from_json.py" $ARGUMENTS
```

Etter kjøring, vis brukeren kort oppsummering:
- Antall oppgaver / milepæler / ressurser
- Prosjektstart og prosjektslutt
- Mapping-statistikk (gjenbrukt / ny / foreldreløse)
- Hvor XML-filen ble lagret
