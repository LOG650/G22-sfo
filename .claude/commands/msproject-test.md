---
description: Kjør test-suite for JSON ↔ MS Project-integrasjonen
argument-hint: [-v] [-k SELECTOR]
allowed-tools: Bash
---

Kjør pytest-suiten som verifiserer integrasjonen mellom JSON-kildene og MSPDI XML:
- UID-stabilitet på tvers av kjøringer
- Strukturell og predecessor-integritet i generert XML
- Round-trip diff er clean
- Nye aktiviteter får nye UIDs uten å påvirke eksisterende
- ExtendedAttributes (identitet) på alle oppgaver
- Milepæl- og ressurs-invarianter

Eventuelle argumenter fra brukeren: $ARGUMENTS

Utfør:

```
python3 -m pytest "004 data/tests/" $ARGUMENTS
```

Hvis pytest ikke er installert, foreslå `pip install pytest`.
