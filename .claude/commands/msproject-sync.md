---
description: Full forward-sync — generer XML, valider strukturelt, og verifiser med MS Project hvis SSH er oppe
argument-hint: [--dry-run]
allowed-tools: Bash, Read
---

Kjør frem-syncen som én operasjon (Workflow B fra integrasjonsdesignet):
1. `generate_msproject_from_json.py` — generer MSPDI XML fra JSON-kildene
2. `validate_msproject_xml.py` — strukturell validering
3. Hvis SSH er konfigurert: `msproject_ssh.py verify` — bekreft at MS Project faktisk kan åpne filen headless
4. Vis endelig sammendrag

Eventuelle argumenter fra brukeren: $ARGUMENTS

Steg 1 — generer:

```
python3 "004 data/generate_msproject_from_json.py" $ARGUMENTS
```

Steg 2 — valider strukturelt:

```
python3 "004 data/validate_msproject_xml.py" --xsd auto
```

Steg 3 — MS Project-verifikasjon (best-effort, skipper hvis SSH ikke er oppe):

```
python3 "004 data/msproject_ssh.py" check 2>/dev/null && \
  python3 "004 data/msproject_ssh.py" verify "004 data/LOG650_G22_from_json.xml"
```

Etter kjøring:
- Hvis alle steg grønne: filen er klar for PM. Vis sti og kort oppsummering.
- Hvis strukturell validering feiler: STOPP, rapporter — det tyder på bug i generator.
- Hvis SSH-check feiler: nevn at MS Project-verifikasjon ble hoppet over; foreslå `/msproject-ssh-setup` hvis brukeren vil aktivere den.
- Hvis SSH er oppe men verify feiler: rapporter feilen fra MS Project (f.eks. XML-strukturfeil MS Project har oppdaget som XSD/strukturell ikke fanget).
