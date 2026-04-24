# Prosjektstyringsplan

## Datadrevet vurdering av hyllekapasitet vs. etterspørsel (Space Management) i dagligvarebutikk

**Dato:** 2026-03-08

**Utarbeidet av:** Frida Berge-Robertson, Oliver Matre Hille, Sebastian Vambheim Thunestvedt

**Emne:** LOG650 Forskningsprosjekt: Logistikk og kunstig intelligens (Vår 2026)

**Bedrift:** Coop Extra X (forutsatt datatilgang og samtykke)

---

## Innhold

1. [Sammendrag](#1-sammendrag) — Bakgrunn, problemstilling, mål, avgrensninger, faglig forankring (5 begreper), rollefordeling, behov, sponsor, kunde, forretningscase, alternativer, gevinster, budsjett, interessenter
2. [Omfang (Scope)](#2-omfang-scope) — Krav, løsning, WBS
3. [Tidsplan (Schedule)](#3-tidsplan-schedule) — Gantt-input, kritisk linje, milepæler, referanseplan
4. [Risiko](#4-risiko) — Risikoregister med S×K-scoring
5. [Ressurser](#5-ressurser) — Team, verktøy, arbeidsinnsats
6. [Kommunikasjon](#6-kommunikasjon) — Interne/eksterne møter, statusrapportering
7. [Kvalitet](#7-kvalitet) — Rapportstruktur, formelle krav, konfidensialitet, akademisk skriving, review, omfangsverifikasjon
8. [Litteratursøk](#8-litteratursøk) — 3 søkedimensjoner, 10 referanser
9. [Saker (Issues)](#9-saker-issues) — Åpne saker og oppfølgingspunkter
10. [Anskaffelser](#10-anskaffelser) — Innkjøp og verktøy
11. [Endringskontroll](#11-endringskontroll) — Prosess for håndtering av endringer
12. [Styringsdata (JSON-filer)](#12-styringsdata-json-filer) — Referanser til strukturerte planfiler

---

## 1. Sammendrag

### 1.1 Bakgrunn

I dagligvarehandelen er hylleplass en knapp ressurs. Planogramsystemer (space management) fordeler hylleplass til produkter basert på kategoristrategier og leverandøravtaler, men denne fordelingen kan i praksis avvike fra faktisk etterspørsel. Når produkter med høy etterspørsel har for lav hyllekapasitet (for få facings eller lav fyllingsgrad), oppstår risiko for tomme hyller, tapt salg og ineffektiv utnyttelse av begrenset butikkareal.

### 1.2 Problemstilling

*Hvordan kan en datadrevet tilnærming identifisere produkter som er underallokert i hylleplass relativt til observerte salgsdata, og hva er det estimerte potensialet for forbedring ved reallokering av eksisterende hyllekapasitet innen en avgrenset varekategori i Coop Extra X?*

Prosjektet skal utvikle en kvantitativ modell som:
1. Analyserer misforholdet mellom hyllekapasitet og etterspørsel per produkt
2. Foreslår en reallokering av hylleplass som maksimerer forventet omsetning
3. Kvantifiserer forbedringen sammenlignet med nåværende allokering

### 1.3 Mål

**Hovedmål:** Utvikle og teste en optimaliseringsmodell for hylleallokering i én varekategori hos Coop Extra X, implementert i Python, som demonstrerer potensialet for datadrevet space management.

**Delmål:**
- Kartlegge nåværende hyllekapasitet vs. faktisk etterspørsel for utvalgte produkter
- Formulere og løse et optimaliseringsproblem for reallokering
- Validere modellens resultater gjennom sensitivitetsanalyse
- Dokumentere funn i vitenskapelig rapport

### 1.4 Avgrensninger

- Én butikk (Coop Extra X)
- Én varekategori (defineres i samarbeid med butikken)
- Maksimalt 10 produkter (SKU) i analysen
- Kampanjer, prisendringer og sesongeffekter modelleres ikke eksplisitt
- Ingen fysisk implementering — prosjektet leverer analyse og forslag til reallokering

### 1.5 Antagelser

- Historiske salgsdata er representative for fremtidig etterspørsel i analyseperioden
- Hylleplassdata reflekterer faktisk fysisk plassering i butikken
- Sammenhengen mellom hylleplass og salg kan modelleres kvantitativt (space elasticity)
- Coop Extra X gir tilgang til nødvendige data i tide

### 1.6 Faglig forankring — De fem begrepene

Prosjektet følger rammeverket fra pensum (Kvantitative metoder i logistikk, Kap. i):

| Nr. | Begrep | Vårt prosjekt |
|-----|--------|---------------|
| 1 | **Område** | Detaljhandel / Space management (hylleallokering i dagligvare) |
| 2 | **Problemstilling** | Hvordan kan reallokering av hylleplass maksimere forventet omsetning gitt mismatch mellom kapasitet og etterspørsel? |
| 3 | **Modell** | LP-modell med beslutningsvariabler x_i (hylleplass per produkt), målfunksjon: maks total omsetning, restriksjoner: fast totalkapasitet, min/maks per produkt |
| 4 | **Prosess** | Steg 1: Datainnsamling (salg + hylle) → Steg 2: Sjekk antagelser (statistiske tester) → Steg 3: Løs modell (LP med PuLP) → Steg 4: Validering (sensitivitetsanalyse) → Steg 5: Anvendelse (anbefalinger til butikken) |
| 5 | **Metoder** | **LP** (lineær programmering/PuLP), **Tid** (deskriptiv tidsrekkeanalyse), **ABC** (klassifisering av produkter), sensitivitetsanalyse, visualisering (matplotlib) |

### 1.7 Rollefordeling — Student vs. KI

Basert på pensum (Kap. iii) er ansvarsfordelingen:

| Studentens rolle | KIs rolle |
|------------------|-----------|
| Velge område og formulere problemstilling | Foreslå relevante metoder og tilnærminger |
| Skaffe og vurdere data | Prosessere og analysere data |
| Velge metode og validere resultater | Bygge modell, generere kode og løse modellen |
| Kvalitetssikre og presentere | Generere rapport og visualiseringer |

Studentene har ansvar for de faglige valgene og kvalitetssikringen. KI brukes som verktøy.

### 1.8 Behov

Coop Extra X har begrenset hylleplass. Nåværende planogramallokering er i stor grad basert på kategoristrategi og leverandøravtaler, og samsvarer ikke nødvendigvis med faktisk etterspørsel. Dette medfører risiko for tomme hyller, tapt salg og ineffektiv utnyttelse av butikkarealet. Det er behov for en datadrevet tilnærming som kvantifiserer avviket mellom tildelt hylleplass og observert etterspørsel, og som foreslår en forbedret allokering.

### 1.9 Sponsor

Emneansvarlig LOG650 (Rekdal/Pettersen) er prosjektets sponsor. Sponsor har myndighet til å godkjenne prosjektforslag (proposal), prosjektplan og endelige leveranser (rapport, kode, presentasjon).

### 1.10 Kunde

Coop Extra X er caseselskapet og fungerer som prosjektets kunde i den forstand at analysen er rettet mot deres butikkdrift. I praksis er det prosjektgruppen, emneansvarlige og medstudenter som vurderer hvorvidt analysen er relevant og anvendelig.

### 1.11 Forretningscase

Bedre hylleallokering gir potensielt høyere omsetning per kvadratmeter, færre tilfeller av tomme hyller (stockouts) og bedre kundeopplevelse. For studentgruppen innebærer prosjektet kompetansebygging innen kvantitativ modellering, lineær programmering, dataanalyse og prosjektstyring — ferdigheter med direkte overføringsverdi til arbeidslivet.

### 1.12 Alternativer

Tre alternative tilnærminger ble vurdert i initieringsfasen:

| # | Alternativ | Vurdering | Beslutning |
|---|-----------|-----------|------------|
| A1 | Manuell gjennomgang av salgsdata uten modellering | Ikke tilstrekkelig kvantitativ. Gir ingen optimaliseringsgrunnlag og oppfyller ikke kravene i LOG650 til bruk av formelle metoder. | Forkastet |
| A2 | LP-optimaliseringsmodell for reallokering av hylleplass | Passer problemet godt, data er tilgjengelig, riktig kompleksitetsnivå for tidsrammen, og gir klare, reproduserbare resultater. | **Valgt** |
| A3 | Avansert ML/AI-tilnærming med etterspørselsprediksjon og dynamisk optimalisering | For komplekst gitt tidsrammen og tilgjengelige data. Krever mer treningsdata og mer avansert infrastruktur enn det som er tilgjengelig. | Forkastet |

### 1.13 Gevinster

**For Coop Extra X:**
- Bedre utnyttelse av hylleplass basert på faktisk etterspørsel
- Redusert risiko for stockouts på populære produkter
- Grunnlag for datadrevne beslutninger om hylleallokering

**For prosjektgruppen:**
- Kompetanse i lineær programmering (LP) og optimaliseringsmodellering
- Praktisk erfaring med Python (pandas, PuLP, matplotlib)
- Erfaring med dataanalyse på reelle forretningsdata
- Prosjektstyringserfaring (MS Project, WBS, risikoanalyse)

### 1.14 Interessenter

| Interessent | Rolle | Innflytelse | Interesse | Håndtering |
|-------------|-------|:-----------:|:---------:|------------|
| Emneansvarlig LOG650 (Rekdal/Pettersen) | Sponsor / godkjenner | Høy | Høy | Informeres ved milepæler. Godkjenner plan, utkast og sluttrapport. |
| Prosjektgruppen (Sebastian, Frida, Oliver) | Utførende team | Høy | Høy | Daglig koordinering via Teams. Arbeidsmøter 2× per uke. |
| Coop Extra X kontaktperson | Dataleverandør | Middels | Middels | Kontaktes for datatilgang (uke 11–14). Holdes orientert om funn. |
| Koordinator Erik Langelo | Administrativ støtte | Lav | Lav | Kontaktes ved praktiske/administrative spørsmål. |
| Medstudenter | Fagfellevurdering (peer review) | Lav | Middels | Peer-to-peer review i uke 18. Gir og mottar tilbakemelding på hovedutkast. |

---

## 2. Omfang (Scope)

### 2.1 Krav

| # | Krav | Type |
|---|------|------|
| K1 | Modellen skal ta inn historiske salgsdata (ukentlig) og hylleplassdata per produkt | Data |
| K2 | Modellen skal identifisere produkter med mismatch mellom etterspørsel og hyllekapasitet | Funksjonell |
| K3 | Modellen skal foreslå reallokering av hylleplass innen fast total kapasitet | Funksjonell |
| K4 | Målfunksjonen skal maksimere forventet total omsetning gitt fast hyllekapasitet | Funksjonell |
| K5 | Sekundære indikatorer: kapasitetsmismatch og risiko for tomme hyller | Funksjonell |
| K6 | Beslutningsvariabler: tildelt hylleplass per produkt (facings/hyllemeter) | Modell |
| K7 | Modellen skal implementeres i Python (pandas, PuLP/scipy, matplotlib) | Teknisk |
| K8 | Resultater skal valideres gjennom sensitivitetsanalyse | Kvalitet |
| K9 | Data skal anonymiseres i rapport og presentasjoner | Etikk |

### 2.2 Løsning

Løsningen består av følgende hovedkomponenter:

1. **Datainnhenting og klargjøring** — Samle salgsdata og hylleplassdata fra Coop Extra X, rense og strukturere for analyse
2. **Etterspørselsanalyse** — Analysere salgsmønstre per produkt, estimere etterspørselsnivå og identifisere mismatch
3. **Optimaliseringsmodell** — Formulere og løse LP/MIP for reallokering av hylleplass med målfunksjon: maks omsetning
4. **Validering** — Sensitivitetsanalyse, sammenligning nåværende vs. foreslått allokering
5. **Rapportering** — Vitenskapelig rapport i henhold til LOG650-malen med Python-kode

### 2.3 Arbeidsnedbrytningsstruktur (WBS)

WBS er strukturert etter prosjektets fire faser og er input til Gantt-diagrammet i MS Project.

```
FASE 1 — INITIERING (ferdig) (Begreper: Område, Problemstilling, Metode)
  1.1  Proposal: område, problemstilling, mål, metodevalg, avgrensning
       ◆ Milepæl M0: Godkjent proposal (9. feb) ✓

FASE 2 — PLANLEGGING (nå) (Begrep: Modell)
  2.1  Prosjektplan (dette dokumentet)
  2.2  WBS og Gantt-diagram (MS Project + referanseplan/baseline)
  2.3  Risikoanalyse
  2.4  Litteratursøk — identifisere nøkkelreferanser
  2.5  Skjelett av rapporten — opprette struktur i Word-mal
       ◆ Milepæl M1: Godkjent prosjektplan + Gantt (9. mar)

FASE 3 — GJENNOMFØRING (Begreper: Prosess, Metoder)
  3.1  Innledning og problemstilling — første utkast
  3.2  Teori og litteratursøk
       3.2.1  Lese utvalgte referanser (mha. KI-oppsummering)
       3.2.2  Skrive teorikapittel: space elasticity, LP-teori, etterspørselsmodellering
  3.3  Casebeskrivelse og datainnsamling [PROSESS-STEG 1: Datainnsamling]
       3.3.1  Avklare datatilgang + signere taushetserklæring (konfidensialitet)
       3.3.2  Innhente salgsdata og hylleplassdata
       3.3.3  Datarensing og strukturering (pandas)
       3.3.4  Skrive casebeskrivelse-kapittel (kun kontekst, ikke analyse)
  3.4  Data/metode og modellering [PROSESS-STEG 2–3: Sjekk antagelser + Løsning]
       3.4.1  Beskrive metodevalg (kvantitativ, case-studie, LP)
       3.4.2  Statistiske tester: sjekk antagelser om datagrunnlaget
       3.4.3  Deskriptiv analyse: etterspørsel per produkt, ABC-klassifisering
       3.4.4  Formulere LP-modell: variabler, parametere, målfunksjon, restriksjoner
       3.4.5  Implementere og løse modell i Python (PuLP)
       3.4.6  Skrive metode- og modelleringskapittel (separert!)
  3.5  Analyse og resultater [PROSESS-STEG 4: Sjekk av løsning]
       3.5.1  Presentere resultater objektivt (tabeller, figurer med forklarende tekst)
       3.5.2  Sensitivitetsanalyse: robusthet mot parameterendringer
       3.5.3  Sammenligning: nåværende vs. foreslått allokering
       3.5.4  Skrive resultatkapittel (ingen tolkning — hører til diskusjon)
  3.6  Diskusjon [PROSESS-STEG 5: Anvendelse]
       3.6.1  Tolke funn i lys av teori og tidligere forskning
       3.6.2  Vurdere praktiske implikasjoner for Coop Extra X
       3.6.3  Diskutere styrker/svakheter, generaliserbarhet
       3.6.4  Skrive diskusjonskapittel (ikke introdusere nye resultater)
  3.7  Hovedutkast — samle alle kapitler
  3.8  Peer-to-peer review av annen gruppes utkast
       ◆ Milepæl M2: Godkjent hovedutkast + peer review (27. apr)

FASE 4 — AVSLUTNING (Dokumentere og presentere)
  4.1  Konklusjon — besvar problemstillingen eksplisitt (kort, presis, ingen nye funn)
  4.2  Innledning ferdigstilles (skrives til slutt!)
  4.3  Kvalitetssikring: grovredigering → språk → finjustering (jf. SKRIVING 2.3.5)
  4.4  Korrektur, referanseliste (APA 7), figursjekk
  4.5  Ferdigstille Python-kode og dokumentasjon (vedlegg)
  4.6  Forberede muntlig presentasjon
  4.7  Muntlig eksamen
       ◆ Milepæl M3: Muntlig presentasjon + innlevert rapport (31. mai)
```

---

## 3. Tidsplan (Schedule)

### 3.1 WBS-input til Gantt (MS Project)

Tabellen under er direkte input for MS Project. Legg inn oppgavene, varigheter, avhengigheter og ressurser, og lagre referanseplan (baseline) etter godkjenning.

| WBS | Oppgave | Varighet | Start | Slutt | Avhengighet | Ressurs |
|-----|---------|----------|-------|-------|-------------|---------|
| **FASE 2** | **Planlegging** | **4 u** | **9. feb** | **9. mar** | | |
| 2.1 | Prosjektplan | 2 u | 24. feb | 9. mar | — | Alle |
| 2.2 | WBS og Gantt (MS Project) | 1 u | 3. mar | 9. mar | 2.1 | Sebastian |
| 2.3 | Risikoanalyse | 1 u | 3. mar | 9. mar | 2.1 | Frida |
| 2.4 | Litteratursøk — identifisere referanser | 2 u | 24. feb | 9. mar | — | Oliver, Frida |
| 2.5 | Rapportskjelett i Word-mal | 1 u | 3. mar | 9. mar | — | Sebastian |
| | ◆ **M1: Godkjent prosjektplan + Gantt** | 0 d | **9. mar** | | 2.1–2.5 | |
| **FASE 3** | **Gjennomføring** | **7 u** | **9. mar** | **27. apr** | | |
| 3.1 | Innledning + problemstilling (1. utkast) | 2 u | 9. mar | 22. mar | M1 | Frida |
| 3.2.1 | Lese utvalgte referanser + KI-summary | 3 u | 9. mar | 29. mar | M1 | Oliver, Frida |
| 3.2.3 | Skrive teorikapittel | 2 u | 23. mar | 5. apr | 3.2.1 | Frida |
| 3.3.1 | Avklare datatilgang Coop Extra X | 2 u | 9. mar | 22. mar | M1 | Oliver |
| 3.3.2 | Signere taushetserklæring | 1 u | 9. mar | 15. mar | M1 | Oliver |
| 3.3.3 | Innhente salgsdata + hylleplassdata | 2 u | 16. mar | 29. mar | 3.3.1 | Oliver |
| 3.3.4 | Datarensing og strukturering | 2 u | 23. mar | 5. apr | 3.3.3SS+1u | Sebastian |
| 3.3.5 | Skrive casebeskrivelse | 1 u | 30. mar | 5. apr | 3.3.3 | Oliver |
| 3.4.1 | Beskrive metodevalg | 1 u | 9. mar | 15. mar | M1 | Sebastian |
| 3.4.2 | Etterspørselsanalyse (deskriptiv) | 1 u | 6. apr | 12. apr | 3.3.4 | Sebastian |
| 3.4.3 | Formulere optimaliseringsmodell | 1 u | 6. apr | 12. apr | 3.3.4 | Sebastian, Frida |
| 3.4.4 | Implementere modell i Python | 2 u | 6. apr | 19. apr | 3.4.3SS | Sebastian |
| 3.4.5 | Kjøre modell og generere resultater | 1 u | 13. apr | 19. apr | 3.4.4SS+1u | Sebastian |
| 3.4.6 | Skrive metode-/modelleringskapittel | 1 u | 13. apr | 19. apr | 3.4.3 | Frida |
| 3.5.1 | Presentere resultater (tabeller/figurer) | 1 u | 14. apr | 20. apr | 3.4.5SS | Sebastian |
| 3.5.2 | Sensitivitetsanalyse | 1 u | 14. apr | 20. apr | 3.4.5SS | Sebastian |
| 3.5.4 | Skrive resultatkapittel | 1 u | 14. apr | 20. apr | 3.5.1SS | Frida |
| 3.6 | Skrive diskusjonskapittel | 1 u | 20. apr | 26. apr | 3.5.4 | Alle |
| 3.7 | Samle hovedutkast | 3 d | 21. apr | 24. apr | 3.6SS | Sebastian |
| 3.8 | Peer-to-peer review | 3 d | 27. apr | 29. apr | 3.7 | Alle |
| | ◆ **M2: Godkjent hovedutkast + peer review** | 0 d | **27. apr** | | 3.7 | |
| **FASE 4** | **Avslutning** | **5 u** | **27. apr** | **31. mai** | | |
| 4.1 | Skrive konklusjon | 1 u | 28. apr | 4. mai | M2 | Alle |
| 4.2 | Ferdigstille innledning | 1 u | 28. apr | 4. mai | M2 | Frida |
| 4.3 | Kvalitetssikring, korrektur, referanser | 2 u | 5. mai | 18. mai | 4.1, 4.2 | Alle |
| 4.4 | Ferdigstille Python-kode + dokumentasjon | 1 u | 5. mai | 11. mai | M2 | Sebastian |
| 4.5 | Forberede muntlig presentasjon | 2 u | 12. mai | 25. mai | 4.3SS | Alle |
| 4.6 | Muntlig eksamen | 1 u | 25. mai | 31. mai | 4.5 | Alle |
| | ◆ **M3: Rapport + kode innlevert, presentasjon** | 0 d | **31. mai** | | 4.3–4.6 | |

*SS = Start-to-Start, u = uke(r), d = dag(er)*

### 3.2 Gantt-diagram (ASCII-oversikt)

Detaljert Gantt lages i MS Project basert på tabellen over. Under er en visuell oversikt:

```
                              Mar                 Apr                     Mai
Oppgave                  Uke: 10   11   12   13 | 14   15   16   17  | 18   19   20   21   22
                               2-8  9-15 16-22 23-29 30-5 6-12 13-19 20-26 27-3 4-10 11-17 18-24 25-31

FASE 2 — PLANLEGGING
  Prosjektplan + Gantt    ████
  Litteratursøk           ████ ▓▓▓▓
  Rapportskjelett         ████
◆ M1 Godkjent plan       ──◆

FASE 3 — GJENNOMFØRING
  Innledning (1. utkast)       ████ ████
  Lese referanser + summary    ████ ████ ████
  Teorikapittel                          ████ ████
  Datatilgang Coop Extra X     ████ ████
  Datainnhenting                    ████ ████
  Datarensing                            ████ ████
  Casebeskrivelse                        ████
  Metodevalg                   ████
  Etterspørselsanalyse                        ████
  Optimaliseringsmodell                       ████ ████
  Resultater + validering                          ████
  Diskusjon                                        ████
  Samle hovedutkast                                ████
  Peer-to-peer review                                   ████
◆ M2 Hovedutkast + review                          ──◆

FASE 4 — AVSLUTNING
  Konklusjon                                             ████
  Ferdigstille innledning                                ████
  Kvalitetssikring                                            ████ ████
  Kode-dokumentasjon                                          ████
  Forbered presentasjon                                            ████ ████
  Muntlig eksamen                                                       ████
◆ M3 Innlevert + presentasjon                                           ──◆

████ = aktivt arbeid    ▓▓▓▓ = fortsetter fra forrige uke
```

### 3.3 Kritisk linje (Critical Path)

```
M1 → Datatilgang avklart → Datainnhenting → Datarensing → Modellering → Resultater → Hovedutkast → M2
```

Forsinkelser i **datatilgang** forsinker hele prosjektet. Beredskap: parallelt arbeid med teori/litteratur, og syntetisk data som fallback.

### 3.4 Milepæler

| Milepæl | Dato | Leveranse | Godkjennes av |
|---------|------|-----------|---------------|
| M0 | 9. feb ✓ | Godkjent proposal | Emneansvarlig |
| M1 | **9. mar** | **Godkjent prosjektplan + Gantt-diagram** | **Emneansvarlig** |
| M2 | 27. apr | Godkjent hovedutkast + peer-to-peer review | Emneansvarlig |
| M3 | 31. mai | Innlevert rapport + kode + muntlig presentasjon | Emneansvarlig |

### 3.5 Referanseplan (Baseline)

Etter godkjenning av prosjektplanen (M1) lagres referanseplan i MS Project:
1. **Prosjekt-fanen → Lagre referanseplan (Set Baseline)**
2. Velg «Lagre referanseplan» for hele prosjektet
3. Bytt til **Oppfølgings-Gantt (Tracking Gantt)** for å se avvik

Referanseplanen revideres ved slutt av fase 3 (M2) dersom vesentlige endringer har oppstått.

---

## 4. Risiko

### 4.1 Prosess for risikostyring

Risikoregisteret gjennomgås på hvert gruppemøte (2× per uke). Hvert gruppemedlem overvåker risikoer knyttet til sine oppgaver. Risikotiltak iverksettes proaktivt. Ved utløst risiko aktiveres beredskapsplanen.

### 4.2 Risikoregister

| # | Risiko | S | K | Risikoverdi | Eier | Tiltak (forebyggende) | Beredskapsplan (reaktiv) |
|---|--------|:-:|:-:|:-----------:|------|----------------------|--------------------------|
| R1 | Manglende/forsinket datatilgang fra Coop Extra X | 3 | 5 | **15 — Høy** | Oliver | Ta kontakt umiddelbart (uke 11). Følge opp ukentlig. Ha taushetserklæring klar. | Bruke simulerte/syntetiske data basert på realistiske parametere fra tilgjengelige datasett. |
| R2 | Datakvalitet utilstrekkelig (manglende verdier, inkonsistens) | 3 | 3 | **9 — Middels** | Sebastian | Avklare dataformat tidlig. Sette av 2 uker til datarensing. | Avgrense til produkter/perioder med komplett data. Supplere med realistiske antagelser. |
| R3 | Optimaliseringsmodell for kompleks for tidsrammen | 2 | 3 | **6 — Lav** | Sebastian | Start med enkel LP-modell, utvid gradvis. «God modell ≠ komplisert modell.» | Levere enklere, men komplett modell fremfor avansert, ufullstendig. |
| R4 | Gruppemedlem utilgjengelig (sykdom) | 2 | 3 | **6 — Lav** | Alle | Alle har oversikt over hele prosjektet. Kode og docs deles via GitHub. | Omfordele oppgaver. Justere omfang om nødvendig. |
| R5 | Tidspress mot slutten av semesteret | 3 | 3 | **9 — Middels** | Sebastian | Jevn innsats. Starte rapportskriving tidlig (fase 2). Følge Gantt. | Prioritere kjerneleveranser (modell + rapport). Droppe «nice-to-have». |
| R6 | Peer-to-peer review avdekker vesentlige mangler | 2 | 3 | **6 — Lav** | Frida | Levere solid utkast ved å følge rapportstrukturen konsekvent. | Revisjonsbuffer (uke 19) etter review. Fokuser på kritiske punkter. |

**Skala:** Sannsynlighet (S) og Konsekvens (K): 1–5. Risikoverdi = S × K. Høy ≥ 12, Middels 6–11, Lav ≤ 5.

---

## 5. Ressurser

### 5.1 Prosjektteam

| Navn | Rolle | Hovedansvar |
|------|-------|-------------|
| Sebastian Vambheim Thunestvedt | Prosjektleder / utvikler | Prosjektstyring, Python-implementering, MS Project |
| Frida Berge-Robertson | Analytiker / forfatter | Dataanalyse, litteratursøk, teorikapittel, rapportskriving |
| Oliver Matre Hille | GitHub / analytiker | Litteratursøk, casebeskrivelse, validering |

*Rollene er fleksible — alle bidrar på tvers av oppgaver etter behov.*

### 5.2 Problemstilling (gjentatt for klarhet)

*Hvordan kan en datadrevet tilnærming identifisere produkter som er underallokert i hylleplass relativt til observerte salgsdata, og hva er det estimerte potensialet for forbedring ved reallokering av eksisterende hyllekapasitet innen en avgrenset varekategori i Coop Extra X?*

### 5.3 Verktøy

| Verktøy | Formål | Metode (jf. kompendiet) |
|---------|--------|-------------------------|
| **Python** (pandas, PuLP, matplotlib, numpy) | Dataanalyse, optimalisering, visualisering | LP (Lineær programmering), Tid (deskriptiv analyse), ABC (klassifisering) |
| **MS Project** | Gantt-diagram, referanseplan (baseline), fremdriftsoppfølging | — |
| **GitHub** | Versjonskontroll for kode og dokumenter | — |
| **Microsoft Teams** | Kommunikasjon, møter, gruppechat | — |
| **Word** (LOG650-mal fra Høgskolen) | Rapportskriving (skriv direkte i malen, Times New Roman 12pt, 1.5 linjeavstand) | — |

### 5.4 Estimert arbeidsinnsats

| Fase | Periode | Timer/pers./uke | Totalt (3 pers.) |
|------|---------|:---:|:---:|
| Fase 2 — Planlegging | Uke 7–11 | 8–10 | ~120 t |
| Fase 3 — Gjennomføring | Uke 11–18 | 12–15 | ~300 t |
| Fase 4 — Avslutning | Uke 18–22 | 10–12 | ~150 t |
| **Totalt** | | | **~570 t** |

---

## 6. Kommunikasjon

### 6.1 Interne gruppemøter

| Hva | Hyppighet | Når | Varighet | Format |
|-----|-----------|-----|----------|--------|
| Arbeidsmøte / koordinering | 2× per uke | Mandag og torsdag | 1–2 timer | Teams / fysisk |
| Kort statussjekk | Daglig (hverdager) | Morgen | 5–10 min | Teams-chat |

**Agenda for arbeidsmøter:**
1. Status på oppgaver siden forrige møte
2. Gjennomgang av risikoregister (kort)
3. Planlegging av neste oppgaver
4. Eventuelle blokkere eller behov for hjelp

**Møtelogg:** Kort oppsummering etter hvert møte lagres i Teams-kanalen.

### 6.2 Ekstern kommunikasjon

| Hvem | Hyppighet | Kanal |
|------|-----------|-------|
| Emneansvarlige (Rekdal/Pettersen) | Ved behov, minimum ved milepæler | Teams / e-post |
| Coop Extra X kontaktperson | Primært uke 11–14 (datainnhenting) | E-post / telefon |
| Koordinator (Erik Langelo) | Ved administrative spørsmål | Teams / e-post |

### 6.3 Teams-kanal og statusrapportering

- Egen Teams-kanal for gruppen (opprettes av koordinator)
- All kode versjoneres i **GitHub**
- Rapportutkast skrives direkte i **Word-malen** og deles via Teams
- Statusoppdatering til emneansvarlige ved hver milepæl

---

## 7. Kvalitet

### 7.1 Rapportstruktur (LOG650-malen)

Rapporten følger strukturen fra `Mal prosjekt LOG650 v2.docx` og retningslinjene fra SKRIVING-kompendiet (Kap. 4):

| Kapittel | Skal være med | Skal IKKE være med | Typiske feil |
|----------|--------------|---------------------|--------------|
| **1. Introduksjon** (Alle) | Kort motivasjon, presis problemstilling, faglige avgrensninger | Detaljert teori, casebeskrivelse, resultater, metode, diskusjon | For lang (3–5 s) med historikk; problemstilling uklart; brukes som «mini-sammendrag» |
| **2. Teori og litteratur** (Alle) | Definisjoner, begreper, modeller, tidligere forskning, syntese mot problemstilling, kildekritikk | Empiri/casebeskrivelse, matematisk modellformulering, egne resultater | Teori og empiri blandes; lange referater uten kobling til problemstilling |
| **3. Casebeskrivelse** (Case) | Kort beskrivelse av Coop Extra X, relevante prosesser, nøkkeldata for analysen, rammebetingelser | Teoridiskusjon, metodevalg, modellering, analyse, historikk uten relevans | Blir bedriftsrapport; analyse «sniker seg inn» |
| **4. Data og metode** (Fleste) | Datagrunnlag (type, kilde, periode), forskningsdesign (case-studie), innsamlingsmetoder, datarensing, analysemetoder (LP, Python), reproduserbarhet | Resultater, diskusjon, teoridiskusjon, casebeskrivelse | Bare *hva* — mangler *hvordan* og *hvorfor*; analyse starter her |
| **5. Modellering** (Modell) | Variabler, parametere, mengder, antakelser, målfunksjon, restriksjoner, symboltabell, modellvarianter | Numeriske resultater, tolkning, teorihistorikk, implementasjonsdetaljer | Tall blandes inn i formuleringen; modell og analyse slås sammen |
| **6. Analyse og resultater** (Fleste) | Resultater fra modellkjøringer (tabeller, figurer), sensitivitetsanalyse, delresultater koblet til problemstilling | Tolkning/vurdering (→ diskusjon), teorirepetisjon, metode/databeskrivelse | Resultat og diskusjon blandes; tabeller mangler forklarende tekst |
| **7. Diskusjon** (Alle) | Tolkning av funn, sammenligning med teori/litteratur, styrker/svakheter, generaliserbarhet, praktiske implikasjoner | Nye resultater/analyser, metodegjennomgang, tekniske detaljer | Gjentar resultater i stedet for å tolke; nye tall som «ekstra funn» |
| **8. Konklusjon** (Alle) | Eksplisitt svar på problemstillingen, kort oppsummering av funn, implikasjoner, forslag til videre forskning | Nye data/analyser/argumenter, utfyllende metode/teori | Problemstillingen besvares ikke; nye funn introduseres |
| 9. Bibliografi | APA 7-stil, kun referanser brukt i teksten | | Kilder i tekst mangler i listen eller omvendt |
| 10. Vedlegg | Python-kode, datasett, taushetserklæring, detaljerte beregninger | Hovedfunn, drøfting, teori, vesentlige metodevalg | Brukes som erstatning for analyse |

**Viktige kvalitetsskiller (fra pensum):**
- **Resultater ≠ Diskusjon** — objektiv presentasjon vs. tolkning (*hva* vs. *hvorfor*)
- **Modell ≠ Metode** — formuleringen vs. fremgangsmåten
- **Teori ≠ Empiri** — litteratur vs. egne funn, hold dem adskilt
- **Innledning skrives til slutt!**
- **Vedlegg = dokumentasjon**, ikke erstatning for analyse

### 7.2 Formelle krav (Kap. 3, SKRIVING-kompendiet)

| Krav | Spesifikasjon |
|------|--------------|
| **Referansestil** | APA 7 (7. utgave, Publication Manual of the APA) |
| **Font** | Times New Roman, 12 pt |
| **Linjeavstand** | 1.5 i hovedtekst |
| **Marger** | 2.5 cm på alle sider |
| **Mal** | Word-malen fra Høgskolen i Molde (`Mal prosjekt LOG650 v2.docx`) |
| **Språk** | Norsk (kan inkludere engelske fagtermer der norsk term ikke er etablert) |
| **Omfang** | ~18 000–21 000 ord (tommelfingerregel for 3 studenter, ikke formelt krav) |
| **Figurer/tabeller** | Nummereres separat, titler *under*, alle omtales i tekst før de vises, selvforklarende figurtekst |
| **Vedlegg** | Nummereres, refereres eksplisitt i tekst, brukes som dokumentasjon (ikke erstatning for analyse) |

### 7.3 Konfidensialitet

Prosjektet benytter data fra Coop Extra X. Vurdering:
- Salgsdata og hylleplassdata kan inneholde forretningssensitiv informasjon
- **Tiltak:** Taushetserklæring signeres før datatilgang. Data anonymiseres i rapport og presentasjon
- **Formelt krav:** Dersom konfidensiell → skriftlig avtale mellom studenter, veileder, bedrift og studieprogramkoordinator (se mal i SKRIVING Kap. 3.8)
- Avklares med Coop Extra X i forbindelse med datatilgang (uke 11)

### 7.4 Akademisk skriving (Kap. 5, SKRIVING-kompendiet)

Nøkkelregler for hele rapporten:
- **Saklig og objektivt** — bygget på data og teori, unngå subjektive vurderinger
- **Presis** — bruk fagtermer konsekvent, definer ved første bruk, unngå upresise ord (*mye, mange, viktig*)
- **Analytisk** — forklar *hvorfor*, ikke bare *hva*. Argumentasjonsstruktur: påstand → begrunnelse → evidens
- **Nøytralt** — unngå personlig pronomen (*jeg, vi*), bruk aktiv form uten pronomen eller passiv
- **Ingen metaforer** — unngå «kjøre seg fast», «ha kontroll på sakene»
- **Ingen fyllord** — fjern «i forhold til», «som sagt», «på en måte», «ganske»
- **Dempere med måte** — «kan indikere», «tyder på» ved usikre funn
- **Forkortelser** — skriv full form første gang: «Linear Programming (LP)»

### 7.5 Peer-to-peer review

I fase 3 gjennomfører gruppen en peer-to-peer review med annen gruppe (tildelt av emneansvarlige):
- Hovedutkast ferdig innen **27. april**
- Review gjennomføres **27.–29. april**

**Reviewkriterier:**
- Er problemstillingen tydelig og kvantitativ?
- Er modellen riktig formulert og implementert?
- Er resultatene presentert objektivt (tabeller/figurer med forklarende tekst)?
- Er diskusjonen adskilt fra resultatene?
- Er referansene konsistente (APA 7)?
- Er innhold plassert i riktig kapittel (teori ≠ case, modell ≠ analyse)?

### 7.6 Intern kvalitetssikring

Revisjonsprosess (fra SKRIVING Kap. 2.3.5):
1. **Grovredigering** — struktur og argumentasjon
2. **Språkforbedring** — klarhet, faglig presisjon
3. **Finjustering** — tabeller, figurer, begrepsbruk, referanser

Øvrig:
- Hvert rapportkapittel gjennomgås av minst ett annet gruppemedlem
- Python-kode gjennomgås (code review) via GitHub
- Resultater valideres gjennom sensitivitetsanalyse
- Data lagres strukturert: `004 data/raw/` (rå, uendret) + `004 data/processed/` (arbeidskopier)

### 7.7 Omfangsverifikasjon

Hver leveranse gjennomgår intern verifikasjon før den anses som ferdig:

| Leveranse | Verifikasjonsmetode | Ansvarlig |
|-----------|---------------------|-----------|
| Datagrunnlag | Kontroll av datakvalitet: komplett, konsistent, riktig format. Sammenligning mot forventede verdier. | Sebastian |
| Optimaliseringsmodell | Sensitivitetsanalyse på nøkkelparametere. Kontroll av at restriksjoner og målfunksjon er korrekt implementert. | Sebastian, Frida |
| Rapportkapitler | Gjennomlesing av minst ett annet gruppemedlem. Sjekk mot rapportstruktur og kvalitetskriterier. | Alle |
| Hovedutkast | Intern QA + ekstern peer-to-peer review (uke 18). | Alle |
| Sluttrapport | Trestegs revisjon (grovredigering → språk → finjustering). Referansesjekk (APA 7). | Alle |

### 7.8 Referansehåndtering

- **APA 7** — konsekvent gjennom hele rapporten
- Referanser legges inn manuelt (bachelornivå, ikke referanseverktøy som EndNote)
- Alle teorier, modeller, tall og figurer fra andre kilder refereres
- KI-generert faglig innhold refereres eksplisitt
- Parafraser fremfor direkte sitat der mulig; direkte sitat med sidetall
- Kilder i tekst = kilder i referanselisten (og omvendt)

### 7.9 Godkjenningskriterier

Godkjent = krav omtrent som til karakter «C» (fase 1–3), karakter «B» (fase 4).

---

## 8. Litteratursøk

Tre strategiske litteratursøk er gjennomført for å dekke prosjektets faglige bredde:

### Søk 1: Optimaliseringsmodeller for hylleplass (OR-grunnlaget)

**Søkeord:** *shelf space allocation optimization grocery retail linear programming*

| Referanse | Relevans |
|-----------|----------|
| Düsterhöft, Hübner & Schaal (2021). *Exact optimization and decomposition approaches for shelf space allocation.* European Journal of Operational Research. | Eksakt og dekomponeringsbasert løsningsmetode for hylleallokering med heterogene hyllestørrelser — direkte relevant for vår modellformulering. |
| Hübner, Schäfer & Schaal (2020). *Maximizing Profit via Assortment and Shelf-Space Optimization for Two-Dimensional Shelves.* Production and Operations Management. | Integrerer sortiment og hylleplass med stokastisk etterspørsel og space-elastisitet. |
| Mishra (2023). *Heuristics for the shelf space allocation problem.* OPSEARCH (Springer). | 6 heuristikker for hylleallokering med produktgruppering — praktisk tilnærming. |
| Bouzembrak et al. (2025). *Literature review on shelf space allocation in retailing.* RAIRO Operations Research. | Fersk litteraturoversikt over hele SSAP-feltet — svært nyttig startpunkt for litteraturkapittelet. |

### Søk 2: Etterspørselsprognoser og out-of-stock i dagligvare

**Søkeord:** *demand forecasting out-of-stock retail planogram machine learning*

| Referanse | Relevans |
|-----------|----------|
| Gholami & Bhakoo (2025). *A machine learning approach to inventory stockout prediction.* Supply Chain Analytics (Elsevier). | ML-basert stockout-prediksjon med 1.6M+ SKU fra ekte retailer — kvantifiserer kapasitet-etterspørsel mismatch. |
| Gustriansyah et al. (2022). *A Comparative Study of Demand Forecasting Models.* Mathematics (MDPI). | Hybrid ML-modell (XGBoost, RF, LR) for salgsprognose — relevant input til optimalisering. |
| Usama et al. (2024). *AI-driven demand forecasting: Enhancing inventory management.* WJARR. | 23.7% bedre prognose, 24.3% færre stockouts i dagligvare med AI — kvantitativ evidens. |

### Søk 3: KI/AI-anvendelser i retail space management

**Søkeord:** *AI deep learning planogram optimization retail shelf space*

| Referanse | Relevans |
|-----------|----------|
| Klement & Hübner (2023). *Decision support for managing assortments, shelf space, and replenishment in retail.* Flexible Services and Manufacturing (Springer). | Helhetlig rammeverk som kobler sortiment, hylleplass og påfylling — binder våre delproblemer sammen. |
| Santos et al. (2024). *Shelf Management: A deep learning-based system for shelf visual monitoring.* Expert Systems with Applications. | DL-pipeline for automatisert hyllemonitorering — viser fremtidig datainnhenting. |
| Hsu et al. (2025). *Real-time retail planogram compliance using computer vision.* Scientific Reports (Nature). | CV-system for planogram-etterlevelse i 7000+ butikker — produksjonsskala AI i shelf management. |

**Prioriterte artikler å lese først:**
1. **Bouzembrak et al. (2025)** — fersk litteraturoversikt, gir hele landskapet
2. **Düsterhöft, Hübner & Schaal (2021)** — kjerne-OR-modellen for hylleallokering
3. **Gholami & Bhakoo (2025)** — ML-basert stockout-prediksjon med ekte data
4. **Klement & Hübner (2023)** — helhetlig rammeverk sortiment + hylleplass + påfylling

---

## 9. Saker (Issues)

Åpne saker og oppfølgingspunkter som må avklares. Tabellen oppdateres løpende på gruppemøter.

| # | Sak | Ansvarlig | Frist | Status |
|---|-----|-----------|-------|--------|
| S1 | Datatilgang fra Coop Extra X ikke bekreftet ennå | Oliver | Uke 12 | Åpen |
| S2 | Taushetserklæring må signeres | Oliver | Uke 11 | Åpen |
| S3 | Avklare hvilken varekategori som analyseres | Alle | Uke 12 | Åpen |
| S4 | Bekrefte at salgsdata og hylleplassdata er tilgjengelige i riktig format | Sebastian | Uke 13 | Åpen |

---

## 10. Anskaffelser

Det er ingen anskaffelser i dette prosjektet. Alle nødvendige verktøy er gratis eller tilgjengelig gjennom Høgskolen i Molde:

| Verktøy | Lisens / tilgang |
|---------|-----------------|
| Python (pandas, PuLP, matplotlib, numpy) | Open source / gratis |
| MS Project | Tilgjengelig via HiMolde-lisens |
| GitHub | Gratis (studentkonto) |
| Microsoft Teams | Tilgjengelig via HiMolde |
| Word (LOG650-mal) | Tilgjengelig via HiMolde |

---

## 11. Endringskontroll

Følgende prosess gjelder for endringer som påvirker prosjektets omfang, milepæler eller leveranser:

1. **Beskriv endringen og begrunnelsen** — Hva skal endres, og hvorfor? Dokumenteres skriftlig (Teams eller i planfiler).
2. **Gruppen vurderer konsekvenser** — Hvilken innvirkning har endringen på omfang, milepæler, arbeidsmengde og risiko?
3. **Eskaler ved behov** — Dersom endringen påvirker godkjente leveranser eller milepæler, eskaleres beslutningen til emneansvarlig.
4. **Oppdater plandokumenter** — Godkjente endringer oppdateres i prosjektplan, tidsplan og relevante JSON-filer. Endringen kommuniseres til hele gruppen.

Mindre justeringer (f.eks. omfordeling av oppgaver innad i en uke) håndteres direkte i gruppemøter uten formell eskaleringsprosess.

---

## 12. Styringsdata (JSON-filer)

Prosjektets strukturerte styringsdata vedlikeholdes i JSON-filer og supplerende dokumenter i samme katalog som denne prosjektplanen. Disse filene brukes som input til MS Project, risikooppfølging og statusrapportering.

| Fil | Innhold | Beskrivelse |
|-----|---------|-------------|
| [`core.json`](core.json) | Prosjektkjerne | Prosjektets grunndata: tittel, gruppe, problemstilling, mål, avgrensninger, faser og milepæler. |
| [`wbs.json`](wbs.json) | Arbeidsnedbrytningsstruktur (WBS) | Komplett WBS med oppgaver, varigheter, avhengigheter og ressurser — direkte input til MS Project. |
| [`schedule.json`](schedule.json) | Fremdriftsplan | Tidsplan med start-/sluttdatoer, milepæler og kritisk linje. |
| [`requirements.json`](requirements.json) | Krav | Funksjonelle, tekniske og kvalitetskrav til prosjektets leveranser. |
| [`risk.json`](risk.json) | Risikoregister | Identifiserte risikoer med sannsynlighet, konsekvens, tiltak og beredskapsplaner. |
| [`status.md`](status.md) | Statusrapport | Løpende statusrapportering med fremdrift, avvik og beslutninger. |

*Diagrammer:*
| Fil | Innhold |
|-----|---------|
| [`wbs_diagram.png`](wbs_diagram.png) | Visuelt WBS-diagram generert fra `wbs.json`. |

---

## Vedlegg

### Vedlegg A — Taushetserklæring

Taushetserklæring signeres med Coop Extra X før datatilgang innvilges. Mal: `000 templates/Taushetsærklæring.docx`.

### Vedlegg B — Referanse til proposal

Godkjent prosjektbeskrivelse (proposal) finnes i `015 Prosjektinformasjon/Proposal DOCX/`. Proposalet definerer område, problemstilling, data, beslutningsvariabler, målfunksjon og avgrensninger som denne prosjektplanen bygger videre på.

### Vedlegg C — Datakilder (prioritert rekkefølge)

1. **Bedriftsdata** fra Coop Extra X (salg + hylleplass)
2. **Eksisterende datasett** fra nett/forskning (KI-støttet søk)
3. **Genererte/simulerte data** som backup (realistiske parametere)
