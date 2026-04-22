---
description: Hjelp brukeren sette opp SSH-tilgang til Windows-VMen for MS Project-automasjon
allowed-tools: Bash, Read, Write, Edit
---

Guide brukeren gjennom oppsett av SSH-tilgang fra Mac til Windows-VM i UTM, slik at `msproject_ssh.py` kan automatisere MS Project headless.

Vis først oppsett-instruksjonene:

```
python3 "004 data/msproject_ssh.py" setup-help
```

Deretter, be brukeren om:
1. Om OpenSSH Server er aktivert på Windows (gi PowerShell-kommandoer hvis ikke)
2. VM-IP (`ipconfig` på Windows)
3. Windows-brukernavn
4. Om Mac har en SSH-nøkkel; hvis ikke, foreslå:
   ```
   ssh-keygen -t ed25519 -C "log650-msproject"
   ```

Hjelp med å:
- Kopiere Mac public key (`cat ~/.ssh/id_ed25519.pub`) til `C:\Users\<bruker>\.ssh\authorized_keys`
- Opprette `~/.config/log650/msproject-ssh.json` basert på oppgitt info
- Teste tilkobling med `python3 "004 data/msproject_ssh.py" check`

Når oppsettet er fullført og check lykkes: foreslå brukeren å kjøre `/msproject-verify` som første test.

Viktig: config-filen (`~/.config/log650/msproject-ssh.json`) skal IKKE committes til git — den er utenfor repo-roten som standard og inneholder host/bruker-detaljer. Bekreft med brukeren før du lagrer noe sensitivt.
