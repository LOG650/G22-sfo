# Tiltaksplan etter peer review

**Mottatt:** 2026-05-03 (datert) / 2026-05-08 (mottatt-dato i schedule.json)
**Vurderende gruppe:** [navngitt i originalfilen, ikke gjengitt her]
**Vurdert rapport:** Hovedutkast `005 report/rapport.md` per 2026-04-27
**Original peer review:** `/Volumes/DevSSD/Downloads/main (1).pdf` (ikke versjonert)

## Helhetsinntrykk fra reviewer

> Sterk, original og godt strukturert rapport. Viktigste løft ligger i presisjonsarbeid snarere enn større innholdsmessige omarbeidinger.

Tre hovedlinjer:
1. **Rydde inkonsistenser og uferdige formalia.**
2. **Styrke kobling modelloptimum ↔ praktisk implementerbart forslag.**
3. **Gjøre problemstilling-sporbarhet og kunnskapshull skarpere.**

---

## MUST-FIX (kritisk for innlevering)

### M1 — Numerisk inkonsistens i §5.1

**Tilbakemelding:** s. 16 oppgir "8 produkter, 486 facings"; resten av rapporten bruker konsekvent 34 SKU og 1 079 frontfacings. Restløs fra tidligere versjon.

**Tiltak:**
- Søk i `rapport.md` etter "8 produkter" og "486" — rett til 34 SKU og 1 079.
- Gjør et fullt konsistens-pass på alle tallforekomster i §5.

**Estimat:** 15 min.

### M2 — Fjern frontstoff-plassholdere

**Tilbakemelding:** Forsiden / s. 1–3 har åpne plassholdere: totalt sidetall, veileder, publisering/båndlegging, `[TBD]`-elementer.

**Tiltak:**
- Fyll inn / fjern alle `[TBD]`.
- Bekrefte veiledernavn (Berit Helgheim?) og publiseringsstatus med Sebastian.
- Generere endelig PDF for å låse sidetall.

**Estimat:** 30 min (etter at andre endringer er låst — bør gjøres helt sist).

### M3 — APA 7-referansesjekk for nyere kilder

**Tilbakemelding:** Flere nyere referanser kan ha unøyaktige metadata (forfattere, årstall, tidsskrift, titler).

**Status etter sesjon 2026-05-10:**

**✓ Tre verifiserte rettelser (PDF-er fysisk i `003 references/`):**

| Gammel bib-nøkkel | Korrigert til | Endring |
|---|---|---|
| `klement2023` (Klement & Hübner, FSMJ 2023) | `hubnerkuhn2023` (Hübner & Kuhn, FSMJ 2023, DOI 10.1007/s10696-023-09492-z) | LLM-hallusinerte forfattere; tittel/tidsskrift var korrekt |
| `bouzembrak2025` (Bouzembrak+ RAIRO-OR 2025) | `ziari2025` (Ziari & Sheikh Sajadieh, RAIRO-OR 2025, vol 59, pp 2721–2748, DOI 10.1051/ro/2025037) | LLM-hallusinerte forfattere; tittel/tidsskrift var korrekt |
| `gholami2025` (Gholami & Bhakoo, Supply Chain Analytics 2025) | `liu2025` (Liu, Kalaitzi, Wang, Papanagnou, Journal of Digital Economy 2025, vol 4, pp 144–155, DOI 10.1016/j.jdec.2025.06.002) | LLM-hallusinerte forfattere og tidsskrift; tittel var korrekt |

Sitater i `005 report/rapport.md` er oppdatert til de nye nøklene.

**✓ Dantzig standardisert** som `@incollection{dantzig1951, ...}` med korrekt år (1951, ikke 1947), full Cowles Monograph-serie­info, Koopmans full editor-navn, New York-adresse. Sitering i §3 oppdatert.

**⚠ Gjenstår — ikke verifiserbare uten primærkilde:**

| Bib-nøkkel | Status | Anbefaling |
|---|---|---|
| `dusterhoft2021` (Düsterhöft+Hübner+Schaal EJOR 2021) | Markert med `note` for verifisering | Sjekk DOI/volume/pages før innlevering. Per kildevurdering 2026-04-24 vurder erstatning med Ostermeier+Düsterhöft+Hübner (2021) Omega |
| `hubner2020` (Hübner+Schäfer+Schaal POM 2020) | Markert | Sjekk DOI/volume/pages |
| `nordfalt2018` (Nordfält & Ahlbom IRRDC 2018) | Markert | Sjekk fullt tidsskriftsnavn (kortform: IRRDC vs full IJRDCR) |
| `mishra2023` (Mishra OPSEARCH 2023) | Markert | Per kildevurdering: vurder å erstatte med Ziari (2025) som allerede er inne |
| `hsu2025`, `santos2024`, `usama2024`, `gustriansyah2022` | Markert | Per kildevurdering: lavt bidrag, vurder å fjerne |

**OK uten ytterligere sjekk** (klassikere reviewer kommenterte som konsistente): Curhan 1972, Chevalier 1975, Pareto 1896, Koch 1997.

**Anbefalt sluttforberedelse før innlevering:**
1. Verifiser de fem markerte uverifiserte nyere referansene mot Google Scholar / DOI.org
2. Beslut om Hsu/Santos/Usama/Gustriansyah skal fjernes (kildevurdering anbefaler dropping)
3. Bygg `references.bib` med ren `note`-felt-fjerning før endelig PDF

**Brukt tid:** ~30 min (av estimert 1–2 t — resten er manuelt verifikasjons­arbeid som krever web-tilgang)

---

## SHOULD-FIX (løfter rapporten)

### S1 — Bryt problemstilling i §1 ned

**Tilbakemelding:** Sporbarhet fra problemstilling til analyse/diskusjon kunne vært sterkere. Foreslått form: ett hovedspørsmål + delspørsmål eller evalueringskriterier.

**Reviewers konkrete eksempel:** "(1) om mismatch kan påvises, (2) om en LP-modell gir et robust forbedringsforslag, (3) om resultatet er praktisk anvendbart i forhandling".

**Tiltak:** Avslutt §1 med kort liste over hva rapporten skal dokumentere, og bruk samme tre-fire punkter som rød tråd i §7-konklusjon-koblingen.

**Estimat:** 30 min.

### S2 — Avklar §2.4 (AI / planogramovervåking)

**Tilbakemelding:** Delkapitlet brukes ikke direkte i modellvalg/empirisk analyse. Leseren blir usikker på rolle: bakgrunn, framtidsperspektiv eller fundament?

**Tiltak (velg):**
- (a) Kort ned §2.4 og merk eksplisitt som kontekst / framtidig datainnsamling, ELLER
- (b) Forklar mer eksplisitt hvorfor dette delkapitlet er nødvendig for studiens bidrag.

**Estimat:** 30 min.

### S3 — Skarpere kunnskapshull

**Tilbakemelding:** Formuler kunnskapshullet som et **praktisk-metodisk gap**: eksisterende modeller er avanserte, men leverandører mangler ofte datagrunnlaget for å bruke dem direkte.

**Tiltak:** Skriv om §2.5 (syntese) til å lande denne formuleringen eksplisitt.

**Estimat:** 20 min.

### S4 — Datarensing-tabell + data/modell-antakelser

**Tilbakemelding:** Håndtering av manglende observasjoner er rimelig forklart, men kunne vært kortere/mer eksplisitt. Dataantakelser og modellantakelser flyter sammen mellom innledning, metode, diskusjon.

**Tiltak:**
- Legg til kort tabell eller én setning i §5: hvor mange mulige obs fantes, hvor mange manglet, hvorfor manglet, hvorfor valgt behandling forsvarlig.
- Skille tydeligere data-antakelser (om input) vs. modell-antakelser (om LP-formuleringen) — kanskje to underseksjoner i §6 eller §8.

**Estimat:** 1 time.

### S5 — Endringsgrenser per SKU / "implementerbarhetsscenario"

**Tilbakemelding:** A4 i S2 reduseres fra 168 → 3 facings (s. 33). Numerisk optimalt, men praktisk sensitivt. Skille modelloptimum og implementerbart forslag.

**Tiltak (velg):**
- (a) Legg inn ekstra scenario S4 = "gjennomførbarhetsscenario" med endringsgrenser per SKU (f.eks. ±50 % vs. dagens facings, eller min/max-flyt), kjør LP, sammenlign mot S2.
- (b) Kun diskutere konseptet i §7-§8 uten å kjøre nytt scenario.

**Estimat:** (a) 3–4 timer (kode + kjøring + tabell + figur + tekst). (b) 1 time.

**Anbefaling:** (a) hvis tid tillater — det er reviewers konkrete forslag og vil løfte rapporten merkbart. Ellers (b).

### S6 — Oppsummeringstabell §7

**Tilbakemelding:** Tabell med "største vinnere", "største tapere", "praktisk kommentar" — leseren ser raskere hvilke funn som er beslutningsrelevante.

**Tiltak:** Lag tabell (markdown eller CSV → bilde) med ~5 rader: SKU, dagens facings, foreslått, ∆, praktisk kommentar.

**Estimat:** 45 min.

### S7 — Ranger B1–B7

**Tilbakemelding:** Begrensningene får delvis lik tyngde. Rang dem etter påvirkning på (a) **nivå** på gevinst vs. (b) **retning** på anbefaling.

**Tiltak:** I §8, legg til en kort prioritering: "Begrensninger som først og fremst påvirker gevinst-nivået: B1, B3, B5. Begrensninger som kan utfordre retningen på konklusjonen: B2, B6."

**Estimat:** 30 min.

### S8 — A2-kampanjeeffekt og robusthet

**Tilbakemelding:** Koble A2-avvik / mulig kampanjeeffekt eksplisitt til om hovedfunn består.

**Tiltak:** Én ekstra setning i §8: "Selv hvis A2-observasjonen delvis er kampanjedrevet, består hovedfunnet om at mismatch eksisterer fordi B-/C-segmentet og A1, A3, A5 viser samme mønster uavhengig av A2."

**Estimat:** 15 min.

### S9 — Konklusjon mindre talltung

**Tilbakemelding:** §9 gjentar prosenttall fra §7. Mer syntese, mindre rapportering. Avslutt med beslutningsorientert formulering.

**Reviewers eksempel:** "Modellen gir et godt **første forhandlingsgrunnlag**, men anbefalt omfordeling bør **testes trinnvis i butikk** før full implementering."

**Tiltak:** Skriv om §9 — fjern prosent-gjentakelser, behold problemstilling-svar + bidragsoppsummering + beslutningssetning.

**Estimat:** 1 time.

### S10 — Sankey-figur s. 33

**Tilbakemelding:** Visuelt interessant, men tett og vanskelig å lese i utskrift.

**Tiltak (velg):**
- (a) Forenkle (færre noder, større tekst).
- (b) Behold full versjon i vedlegg, sett enklere oppsummeringsfigur i hovedtekst.
- (c) Stor forklarende figurtekst.

**Estimat:** 1 time.

---

## Anbefalt rekkefølge

**Uke 19 (2026-05-09 til 2026-05-15) — implementere endringer:**
1. M1 (15 min) — quick win, retter åpenbar feil
2. S1 (30 min) — strukturerer revisjonen ved å låse problemstillings-rammen
3. S3, S2 (50 min) — litteratur ferdig
4. S4 (1 t) — metode/data ferdig
5. S5 (3–4 t hvis (a), 1 t hvis (b)) — analyse-løftet
6. S6, S7, S8 (90 min) — diskusjon/resultat presisjon
7. S9 (1 t) — konklusjon

**Uke 20 (2026-05-16 til 2026-05-22) — formalia og finish:**
8. M3 (1–2 t) — APA 7-sjekk, kan splittes på Frida
9. S10 (1 t) — Sankey-figur
10. M2 (30 min) — frontstoff helt på slutten, etter at sidetall er låst

**Total estimert arbeid:** 11–14 timer over to uker.

## Sporbarhet

Når et tiltak er implementert, kryss av i denne fila og vis lenkje til commit-hash. Ved tvil: ta opp i statusmøte (mandag/torsdag).
