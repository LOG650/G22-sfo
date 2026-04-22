---
description: Valider MS Project XML strukturelt (og valgfritt mot XSD)
argument-hint: [--xml PATH] [--xsd auto|--strict-xsd]
allowed-tools: Bash
---

Kjør validering av MSPDI XML:
- **Strukturell** (alltid): UID-unikhet, predecessor-integritet, assignment-integritet, datoformat, milepæl-regler
- **XSD** (valgfritt): strengere validering mot MSPDI 2007-skjemaet. Moderne MS Project-utvidelser gir advarsler — bruk `--strict-xsd` for å feile på dem.

Eventuelle argumenter fra brukeren: $ARGUMENTS

Utfør:

```
python3 "004 data/validate_msproject_xml.py" $ARGUMENTS
```

Etter kjøring:
1. Hvis strukturell validering feiler, identifiser årsaken (peker mot bug i generatoren)
2. Hvis bare XSD-advarsler: forklar at dette er normalt for moderne MSPDI-felt
3. Foreslå neste steg basert på resultat
