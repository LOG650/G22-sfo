# UTM shared folder setup — Mac host ↔ Windows guest for MS Project

En steg-for-steg-guide for å dele `004 data/` mellom macOS (hvor Python-pipelinen kjører) og Windows 11 ARM i UTM (hvor MS Project kjører), slik at samme XML-fil kan åpnes begge steder uten kopiering.

## Forutsetninger

- UTM ≥ 4.5 på Mac
- Windows 11 ARM-VM som kjører
- MS Project Professional installert på Windows-VMen
- OpenJDK 17 på Mac (allerede installert via `brew install openjdk@17`)
- Python-pipelinen virker på Mac (`python3 "004 data/generate_msproject_from_json.py"`)

---

## Steg 1 — Aktiver VirtioFS shared folder i UTM

1. Stopp Windows-VMen
2. Høyreklikk VM i UTM → **Edit**
3. Gå til **Sharing** i sidepanelet
4. **Directory Share Mode: VirtioFS** (høyere ytelse enn SPICE WebDAV)
5. Klikk **+** og velg mappen:
   ```
   /Volumes/DevSSD/Projects/LOG650/G22-sfo/004 data
   ```
6. Sett **Read only: off**
7. Save, start VM

---

## Steg 2 — Installer UTM Guest Tools i Windows

UTM Guest Tools inkluderer VirtioFS-driver for Windows.

1. Last ned siste Guest Tools ISO fra [mac.getutm.app/gallery](https://mac.getutm.app/)
2. I UTM: VM → Devices → CD/DVD → velg ISO-en
3. I Windows: åpne File Explorer → D:\ (eller tilsvarende) → kjør installer
4. Ved prompt om VirtioFS-driver: velg "Install"
5. Reboot Windows

Verifiser etter reboot:
- File Explorer → "This PC" skal ha en ny enhet som heter **Z: (VirtioFS)** eller lignende
- Hvis ikke, se feilsøking nederst

---

## Steg 3 — Map til fast drive-bokstav (anbefalt)

Av og til får shared folder forskjellig bokstav ved reboot. Pin til Z::

1. Åpne **PowerShell som administrator** i Windows
2. Kjør:
   ```powershell
   net use Z: \\spice\shared /persistent:yes
   ```
   (Alternativt hvis VirtioFS: `\\virtiofs\shared` eller drive-bokstaven som ble tildelt automatisk — finn den i "This PC")

3. Verifiser:
   ```powershell
   dir Z:\LOG650_G22_from_json.xml
   ```
   Filen skal vises med samme størrelse som Mac-siden.

---

## Steg 4 — Importer auto-save-XML-makroen

Slik at PM ikke må huske "Save As → XML Format" hver gang.

1. I Windows: åpne MS Project med et prosjekt (f.eks. `Z:\LOG650_G22_from_json.xml`)
2. Trykk **Alt + F11** (åpner VBA Editor)
3. **File → Import File** → naviger til `Z:\auto_save_xml.bas` → Open
4. I prosjekt-treet til venstre: dobbeltklikk **ThisProject**
5. Lim inn i kodevinduet:
   ```vb
   Private Sub Project_AfterSave(ByVal pj As MSProject.Project, _
                                  ByVal Info As EventInfo)
       AutoSaveXML.SaveAsMSPDIXML pj
   End Sub
   ```
6. Save (Ctrl+S). MS Project spør om lagring som "Enabled Macro" — velg **Yes**
7. Lukk VBA Editor
8. Første gang makroer kjører: godkjenn popup ("Enable Macros")

Test: gjør en liten endring, Ctrl+S, sjekk at `.xml` blir oppdatert ved siden av `.mpp`.

---

## Steg 5 — Verifiser full round-trip

### På Mac:
```bash
cd /Volumes/DevSSD/Projects/LOG650/G22-sfo
python3 "004 data/generate_msproject_from_json.py"
# → 004 data/LOG650_G22_from_json.xml oppdatert
```

### På Windows:
1. MS Project → File → Open → `Z:\LOG650_G22_from_json.xml`
2. Flytt én oppgave en uke frem
3. Ctrl+S → velg "Save as XML" (eller la auto-makroen gjøre det hvis du lagrer som .mpp)
4. **Lukk filen** (viktig pga. fillås)

### Tilbake på Mac:
```bash
python3 "004 data/msproject_to_json_diff.py"
# Skal rapportere PM-datoendringen du gjorde
```

---

## Daglig arbeidsflyt

```
┌──────────────────┐          ┌─────────────────┐
│  Mac (Terminal)   │          │ UTM Windows/MS   │
│                   │          │ Project          │
│  /msproject-      │  XML-    │                  │
│  generate         │─────────►│ Åpne Z:\...xml   │
│                   │ oppd.    │ Rediger          │
│                   │          │ Ctrl+S (auto-    │
│                   │◄─────────│   save XML)      │
│                   │ XML      │ LUKK MS Project  │
│  /msproject-diff  │ oppd.    │                  │
│  /msproject-apply │          │                  │
└──────────────────┘          └─────────────────┘
```

---

## Feilsøking

### "Drive Z: ikke tilgjengelig" etter reboot
- `net use` uten `/persistent:yes` forsvinner ved reboot. Bruk flagget.
- Hvis VirtioFS ikke auto-mounter: åpne Device Manager → "Storage controllers" → VirtioFS driver. Reinstaller hvis mangler.

### "Cannot save: file is locked"
- MS Project er fortsatt åpen et sted. Sjekk Task Manager → avslutt alle `WINPROJ.EXE`-prosesser.
- Alternativt: Windows-siden kan ha hengt fillås. Lukk VM og start på nytt.

### Makroen virker ikke
- Sjekk **Trust Center → Macro Settings → Enable all macros**
- Verifiser at `Project_AfterSave` ligger i **ThisProject**, ikke i en vanlig modul
- Sjekk at `Option Explicit` ikke blokkerer (makroen er Option Explicit-safe)

### PM lagrer som .mpp og XML blir ikke oppdatert
- Sjekk at makroen er aktivert (nevnte Trust Center)
- Siste fallback: Bruk MPXJ på Mac til å konvertere `.mpp → .xml`:
  ```bash
  JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home" \
    python3 "004 data/read_mpp_mpxj.py" --mpp "004 data/LOG650_G22_from_json.mpp"
  ```

### Unicode / norske tegn i paths
- VirtioFS håndterer æ/ø/å korrekt
- Mellomrom i paths (som `"004 data"`) krever quoting. Drive-bokstaven Z: omgår dette.

---

## Sikkerhet

- VirtioFS deler mappen med full lese/skrive-tilgang for VMen. Vurder å kun dele `004 data/` (ikke hele repo-roten) for å begrense blast radius.
- XML-filene inneholder prosjektdata; hold Windows-VMen oppdatert og ikke eksponér RDP på internett.

---

## Alternativer hvis VirtioFS er ustabil

### SMB fra macOS
1. System Settings → General → Sharing → **File Sharing: ON**
2. Legg til `004 data/`, velg brukere med skrivetilgang
3. I Windows: File Explorer → `\\<mac-ip>\004_data` → Map network drive → Z:
4. Ytelse: tregere enn VirtioFS, men svært stabil

### Syncthing
1. Installer Syncthing på Mac og i Windows-VM (begge via officielle builds)
2. Sett opp én delt mappe (`004 data/`) mellom begge
3. Synking tar < 1 sekund ved endringer
4. Ulempe: dobbel kopi lagret

### Git-basert (ikke anbefalt for aktiv PM-arbeid)
- Uegnet for hyppige XML-endringer pga. store diff og merge-konflikter
