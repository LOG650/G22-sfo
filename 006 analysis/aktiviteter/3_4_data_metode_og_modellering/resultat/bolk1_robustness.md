# Bolk 1 — robusthet, volum-vs-margin, shadow price

Tre supplerende analyser bygget rundt S2-scenariet (hovedanbefaling). Adresserer henholdsvis B4 (én butikk, kampanjeuke), §8.1 (margin-vekting), og forhandlingsdialogen om utvidelse av totalrammen.

## 1. A2-uke-15 robustness-sjekk

Tester om S2-funnet henger på den ene høye observasjonen (A2 uke 15) som ble flagget som mulig kampanjeuke i §8.2 B4.

- Droppet observasjon: A2 uke 15 — **412 enheter** (rapporten antyder ca. 2× snittet, kampanjedrevet)
- Baseline margin (full):   **846.9**
- Baseline margin (drop):   **833.4**  (Δ -13.5)
- S2 LP-margin (full):      **1190.9**  (+40.6%)
- S2 LP-margin (drop):      **1163.9**  (+39.7%)
- **Endring i %-gevinst: -0.96 pp**

**Tolkning:** Funnet er robust mot A2-uke-15: gevinsten endres med under 2 prosentpoeng (-0.96 pp).

## 2. Volum-mål vs margin-vektet mål

Kjører S2 to ganger: én med m_i = bruttomargin (dagens målfunksjon), én med m_i = 1 (ren volum-maks). Forskjellen viser hva margin-vektingen faktisk flytter.

| Målfunksjon       | Margin-verdi | Volum (enheter/uke) |
|---|---:|---:|
| m_i = 1 (volum)   | 1188.5 | 3035 |
| m_i = bruttomargin | 1190.9 | 3024 |

**Antall SKUer med ulik allokering**: 5 av 34

Topp SKU-forskjeller (sortert etter absolutt diff):

| SKU | Margin | Vol-allok | Margin-allok | Diff |
|---|---:|---:|---:|---:|
| B1 | 30% | 32 | 21 | -11 |
| C3 | 55% | 24 | 32 | +8 |
| C1 | 55% | 18 | 21 | +3 |
| A14 | 30% | 42 | 39 | -3 |
| A2 | 55% | 39 | 42 | +3 |

**Tolkning:** Margin-vektet optimum gir +0.20% mer margin og -0.34% volum sammenlignet med rent volum-mål. Strukturen er lik (A-klasse vokser, C-klasse stabil), men margin-vekting prioriterer SKUer på 55%-segmentet.

## 3. Shadow price på R1 (totalkapasitet)

Numerisk marginalverdi: hva ekstra én hylleenhet i leverandørens kontraktuelle totalbudsjett ville vært verdt i margin-vektet sell-out per uke. Beregnet ved å løse LP på nytt for T+1, T+5, T+10 og rapportere differansen per enhet.

### S2 Primær + sekundær

- Baseline T = 1079: margin **1190.9**

| ΔT | Total T | Ny margin | Δ margin | Marginal verdi per hylleenhet |
|---:|---:|---:|---:|---:|
| +1 | 1080 | 1191.6 | +0.69 | 0.694 |
| +5 | 1084 | 1194.4 | +3.47 | 0.693 |
| +10 | 1089 | 1197.9 | +6.93 | 0.693 |

### S4 Implementerbar

- Baseline T = 1079: margin **1039.9**

| ΔT | Total T | Ny margin | Δ margin | Marginal verdi per hylleenhet |
|---:|---:|---:|---:|---:|
| +1 | 1080 | 1040.6 | +0.69 | 0.687 |
| +5 | 1084 | 1043.3 | +3.44 | 0.687 |
| +10 | 1089 | 1046.7 | +6.79 | 0.679 |

**Tolkning:** Skyggeprisen er leverandørens *kvantitative argument for utvidelse av totalrammen* — neste forhandlingsrunde etter omfordelingen innenfor dagens ramme. Avtakende verdi (Δ-margin per enhet faller med økende ΔT) reflekterer at de mest underdimensjonerte SKUene mettes først.