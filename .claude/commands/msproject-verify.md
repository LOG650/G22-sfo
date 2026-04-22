---
description: Verifisér at generert XML kan åpnes av MS Project (headless, via SSH til Windows-VM)
argument-hint: [path.xml]
allowed-tools: Bash
---

Kjør en headless MS Project "åpne"-test mot XML-filen for å bekrefte at den faktisk er gyldig — ikke bare strukturelt gyldig som XML. Krever at `msproject_ssh.py` er konfigurert. Bruk før du sender filen til PM.

Eventuelle argumenter fra brukeren: $ARGUMENTS

Først, sjekk om SSH er oppe:

```
python3 "004 data/msproject_ssh.py" check
```

Hvis check er OK, kjør verify mot den aktuelle XML-filen (default: `004 data/LOG650_G22_from_json.xml` hvis ikke annet er oppgitt):

```
python3 "004 data/msproject_ssh.py" verify ${ARGUMENTS:-"004 data/LOG650_G22_from_json.xml"}
```

Hvis verify lykkes: rapportér tasks/resources/datoer tilbake til brukeren og bekreft at filen er trygg å dele med PM.

Hvis SSH ikke er konfigurert: foreslå å kjøre `/msproject-ssh-setup` eller `python3 "004 data/msproject_ssh.py" setup-help`.
