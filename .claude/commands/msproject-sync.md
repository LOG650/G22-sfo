---
description: Full pipeline — generer XML, valider, og vis sammendrag
argument-hint: [--dry-run]
allowed-tools: Bash, Read
---

Kjør hele frem-syncen i én operasjon:
1. `generate_msproject_from_json.py` — generer MSPDI XML fra JSON-kildene
2. `validate_msproject_xml.py` — strukturell validering av resultatet
3. Vis endelig sammendrag

Eventuelle argumenter fra brukeren: $ARGUMENTS

Utfør sekvensielt:

```
python3 "004 data/generate_msproject_from_json.py" $ARGUMENTS && \
python3 "004 data/validate_msproject_xml.py" --xsd auto
```

Etter kjøring:
1. Hvis begge steg lyktes, vis filsti og instruks om å åpne i MS Project
2. Hvis generatoren feilet, ikke kjør validering; rapporter feilen
3. Hvis validering fant strukturfeil, påpek at det tyder på bug i generatoren
