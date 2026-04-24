# Prompt for neste sesjon — LOG650 G22 rapport-ferdigstilling

Lim inn hele innholdet under som første melding til Claude Code i neste sesjon.

---

Hei. Jeg fortsetter på LOG650 G22-prosjektet (datadrevet hylleforvaltning for leverandør hos Coop Extra). Jeg har en hard deadline **torsdag 30. april kl 23:59** — rapporten skal være lesbar for peer-to-peer review innen da.

**Les først:**
- `MEMORY.md` og alle filer det peker på (spesielt `current_work.md`, `team_update.md`, `secondary_exposure_research.md`, `quantitative_methods.md`, `canonical_files.md`)
- `slagplan-fase3.md` på repo-root
- `005 report/rapport.md` — nåværende rapportutkast

**Kontekst (kort oppsummering):**

Sesjonen før denne gjorde en stor omskrivning av rapporten fra butikk-POV til leverandør-forhandlings-POV, og kjørte hele LP-pipelinen på det utvidede CCEP-datasettet (34 SKUer i én Coop Extra-butikk). Modellen ble også oppgradert til:
- Margin-vektet målfunksjon (Monster 30 %, Burn 50 %, resten 55 %)
- Global x_min = 3 facings (1 kolli) per SKU
- Sekundæreksponering som beslutningsvariabel (S_max = 3, k = 1.5)

**Nye hovedresultater (34 SKUer, margin-vektet):**
- Baseline margin: 846,9
- S1 Primær-omfordeling: +49,5 %
- S2 Primær + sekundær: +49,8 % (hovedanbefaling)
- S3 Konservativ: +25,2 %

Siste commit i git er LP-extension (`03_lp_modell.py` oppgradert, nye resultat- og figur-filer). Rapport-teksten er IKKE oppdatert ennå med disse nye tallene — den refererer fortsatt til pilot-tall fra 8-SKU-settet.

## Oppgaver i prioritert rekkefølge

### Prioritet 1 — Rapport-oppdatering (kritisk før 30.04)

Lese de ferskeste resultat-filene og oppdatere rapporten tilsvarende:

**Resultater å hente tall fra:**
- `006 analysis/aktiviteter/3_4_data_metode_og_modellering/resultat/lp-scenarier-oppsummering.md`
- `006 analysis/aktiviteter/3_4_data_metode_og_modellering/resultat/lp-rapport_S2_primaer_sek.md` (hovedanbefaling)
- `006 analysis/aktiviteter/3_4_data_metode_og_modellering/resultat/deskriptiv-og-abc-rapport.md`
- `006 analysis/aktiviteter/3_3_casebeskrivelse_og_datainnsamling/resultat/datarensing-rapport.md`

**Rapport-seksjoner som må oppdateres:**

1. **Sammendrag og Abstract** — nye tall: 34 SKUer, +49,8 % margin-vektet, sekundæreksponering som komplementær strategi
2. **§4.2 Fysiske rammebetingelser** — total primær kapasitet 1 079 (ikke 486), bekreft tolkning av "Facings × dybde"
3. **§5.2 Data**
   - Tabell 5.2.1 må erstattes med 34-SKU-tabell fra `deskriptiv-og-abc-rapport.md`
   - Fjern "pilot"-merkingen
   - Oppdater ABC-fordeling (14 A / 9 B / 11 C)
4. **§6.2 Parametere** — `T = 1079`, oppdater noter om minimum facings (x_min = 3 global), legg til k og S_max
5. **§6.3 Beslutningsvariabler** — legg til `s_i ∈ ℤ_{≥0}` sekundæreksponering
6. **§6.4 Etterspørselsantagelse** — uendret, men sjekk tekst
7. **§6.5 Målfunksjon** — endre til `max Σ m_i · y_i` med margin-vekt
8. **§6.6 Restriksjoner** — legg til R2b: `y_i ≤ ρ_i · (x_i + k · s_i)` og R5: `Σ s_i ≤ S_max`
9. **§7 Analyse og resultater** — hele kapitlet re-skrives mot nye tall:
   - §7.1 Scenariesammenligning: S1 Primær (+49,5 %), S2 Primær+sekundær (+49,8 %), S3 Konservativ (+25,2 %)
   - §7.2 S2 hovedanbefaling på produktnivå — hent tabell fra lp-rapport_S2_primaer_sek.md
   - §7.3 Sensitivitet — må re-kjøres (se Prioritet 2)
   - Sentrale funn: sekundær-bidrag er marginalt (+0,3pp) — bekrefter 80/90-regelen
10. **§8 Diskusjon** — legg til:
    - **§8.x Dobbeltperspektiv** (bekreft dette mot user før skriv): både leverandør-mål og butikk-drifts-mål
    - **Ny begrensning B7**: margin-estimater er basert på bransjetypiske intervaller, ikke verifiserte per SKU
    - **Ny begrensning B8**: sekundær-effektivitet k=1.5 er litteratur-basert, ikke empirisk estimert for dette caset
11. **§9 Konklusjon** — oppdater tall til 49,8 % margin-gevinst og 54 % volum-gevinst
12. **Bibliografi §10** — legg til:
    - Chevalier, M. (1975). *Increase in sales due to in-store display.* Journal of Marketing Research, 12(4), 426–431.
    - Nordfält, J. & Ahlbom, C.-P. (2018). *Assessing the sales effectiveness of differently located endcaps in a supermarket.* Journal of Retailing and Consumer Services.
    - Bezawada, R., Balachander, S., Kannan, P. K., & Shankar, V. (2009). *Cross-Category Effects of Aisle and Display Placements.* Journal of Marketing.
13. **§3 Teori** — legg til ny §3.x om sekundæreksponerings-teori med Chevalier og Nordfält-referanser; bruk funnene i `secondary_exposure_research.md`

### Prioritet 2 — Oppdater sensitivitetsanalyse

`04_sensitivitet.py` bruker fortsatt volumbasert LP. Oppgrader til:
- Margin-vektet målfunksjon
- Legg til tredje sweep: sekundær-effektivitet `k ∈ [1.0, 1.5, 2.0, 3.0]`
- Legg til fjerde sweep: margin-antagelser (±5pp for 55 %-merker; 25 %, 30 %, 35 % for Monster)

Kjør deretter og oppdater tabeller/figurer i §7.3.

### Prioritet 3 — Figurer

Etter at tall er oppdatert, regenerer og sjekk:
- `lp_scenario_compare.png` (nå med 34 SKUer)
- `lp_allokering_S2_primaer_sek.png`
- `sensitivitet_*.png` (nye etter P2)

Bekreft at figur-kryssreferanser i rapport-teksten matcher.

### Prioritet 4 — Konsistenssjekk

Kjør en lignende scan som før:
```python
# Finn kryssreferanser som ikke matcher, ekte produktnavn som lekker,
# tomme seksjoner, og TBD-markører som må løses.
```

**Forventede [TBD] som MÅ løses før 30.04:**
- Veileder-navn (bekreft med emneansvarlige)
- Antall sider (fyll ut)

**[TBD] som kan stå til 31.05:**
- Publiseringsavtale (avklares med Coop)
- Båndleggingsbeslutning

### Prioritet 5 — Commit-hygiene

Gjør atomiske commits per kapittel-oppdatering, ikke én stor commit. Bruk attribution:
```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### Prioritet 6 — MS Project

Etter rapport-oppdatering, kjør:
```bash
python3 "004 data/generate_msproject_from_json.py" --status-date today
```
For at Gantt-visningen i MS Project reflekterer dagens fremdrift.

## Data som kan komme inn i løpet av sesjonen

Brukeren kan sende:
- Mer presise min-facings per SKU
- Utsalgspriser (hvis tilgjengelig fra kassalapp.no)
- OOS-flagg fra Coop POS (hvis CCEP har tilgang)

Hvis noe av dette kommer inn, re-kjør relevante scripts og oppdater tekst.

## Husk

- **All forretningssensitiv data** må holdes i `intern/` (gitignored)
- **Alle rapport-tekster** bruker pseudonymer (A1, A2, B1, ... C11)
- **Butikknavnet** er "EXTRA DANMARKSPLASS, HORDALAND" — omtalt som "Coop Extra X"
- **Oliver** er "frafall per 2026-04-24" — beholdes i Gantt t.o.m. 31.03
- **Team** er nå Sebastian + Frida

## Arbeidsflyt-forslag

1. Les minnet og rapporten
2. Kjør `python3 -m pytest "004 data/tests/"` for å bekrefte at scripts fortsatt virker
3. Ta Prioritet 1 i rekkefølge — commit per kapittel
4. Når P1 er ferdig, Prioritet 2 (sensitivitet)
5. Deretter P3-P6 i sekvens
6. Send rapport.md til Frida via git push når alt er grønt

Lykke til. Sebastian står klar for å svare på spørsmål underveis.
