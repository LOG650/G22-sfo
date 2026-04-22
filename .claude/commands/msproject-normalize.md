---
description: La MS Project åpne+lagre XML for å få kanonisk MSPDI-form (via SSH)
argument-hint: [path.xml]
allowed-tools: Bash
---

Be MS Project om å åpne XML-filen og lagre den tilbake. Dette gir en kanonisk MSPDI-form (MS Project re-serialiserer sitt eget format), som gir mer konsistente diffs når PM senere redigerer.

Brukes typisk:
- Etter `/msproject-generate` for å normalisere før PM får den
- Før diff hvis du mistenker whitespace/formateringsforskjeller forurenser diffen

Eventuelle argumenter fra brukeren: $ARGUMENTS

Utfør:

```
python3 "004 data/msproject_ssh.py" normalize ${ARGUMENTS:-"004 data/LOG650_G22_from_json.xml"}
```

Etter kjøring: kjør `/msproject-validate` for å bekrefte at normalisert XML fortsatt består strukturell validering.
