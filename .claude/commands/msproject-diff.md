---
description: Sammenlign PM-redigert MS Project XML mot JSON-kildene (reverse sync)
argument-hint: [--xml PATH] [--report PATH]
allowed-tools: Bash, Read
---

Kjør reverse-sync: les en MSPDI XML (PM sin redigerte versjon), sammenlign mot JSON-kildene, og rapporter hva som har endret seg basert på field ownership:
- **PM-eid** (dato, ressurser): forslag til å oppdatere JSON
- **Dev-eid** (navn, %, struktur): konflikt som krever manuell beslutning
- **PM-lagt til**: nye oppgaver uten `ExtendedAttribute`

Eventuelle argumenter fra brukeren: $ARGUMENTS

Utfør:

```
python3 "004 data/msproject_to_json_diff.py" $ARGUMENTS
```

Etter kjøring:
1. Oppsummer antall konflikter vs. PM-eide datoendringer vs. PM-lagt til
2. Hvis eksisterende `msproject-mapping.json` har foreldreløse nøkler, påpek det
3. Foreslå neste steg: `/msproject-apply` hvis det er PM datoendringer å anvende
