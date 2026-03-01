# Prosjektstyringsplan

## Datadrevet vurdering av hyllekapasitet vs. etterspørsel (Space Management) i dagligvarebutikk

**Dato:** 2026-03-01

**Utarbeidet av:** Frida Berge-Robertson, Oliver Matre Hille, Sebastian Vambheim Thunestvedt

**Emne:** LOG650 Forskningsprosjekt: Logistikk og kunstig intelligens (Vår 2026)

**Bedrift:** Coop Extra X

---

## Innhold

1. [Sammendrag](#1-sammendrag)
2. [Omfang](#2-omfang)
3. [Fremdrift](#3-fremdrift)
4. [Risiko](#4-risiko)
5. [Ressurser](#5-ressurser)
6. [Kommunikasjon](#6-kommunikasjon)
7. [Kvalitet](#7-kvalitet)

---

## 1. Sammendrag

### 1.1 Behov

I dagligvarehandelen er hylleplass en knapp ressurs. Planogramsystemer fordeler hylleplass til produkter, men denne fordelingen kan i praksis avvike fra faktisk etterspørsel. Når produkter med høy etterspørsel har for lav hyllekapasitet, oppstår risiko for tomme hyller, tapt salg og ineffektiv utnyttelse av begrenset butikkareal.

Det finnes et behov for en datadrevet tilnærming som systematisk identifiserer misforholdet mellom hyllekapasitet og etterspørsel, og som kan kvantifisere forbedringspotensialet ved reallokering.

### 1.2 Veileder og bedrift

- **Emneansvarlige:** Per Kristian Rekdal og Bård-Inge Pettersen (Høgskolen i Molde)
- **Bedrift:** Coop Extra X (forutsatt datatilgang og samtykke)

### 1.3 Forretningscase

Prosjektet har potensial til å forbedre omsetningen innen en varekategori ved å optimalisere fordelingen av eksisterende hylleplass. Gevinsten realiseres gjennom:

- Økt tilgjengelighet av etterspurte produkter
- Redusert risiko for tomme hyller (out-of-stock)
- Bedre utnyttelse av begrenset hylleareal

Prosjektet krever ingen investering utover arbeidstimer fra gruppen og tilgang til salgs-/hylledata fra bedriften.

#### Forutsetninger

- Coop Extra X gir tilgang til historiske salgsdata og hylleplassdata for én varekategori.
- Data kan anonymiseres for bruk i rapporten.
- Gruppen får tilstrekkelig veiledning fra emneansvarlige.

---

## 2. Omfang

### 2.1 Mål

**Prosjektmål:** Utvikle en kvantitativ modell som identifiserer produkter som er underallokert i hylleplass relativt til observerte salgsdata, og estimere potensialet for forbedring ved reallokering av eksisterende hyllekapasitet innen én avgrenset varekategori i Coop Extra X.

**Forutsetninger:**
- Historiske salgsdata er representative for fremtidig etterspørsel i analyseperioden.
- Hylleplassdata reflekterer faktisk fysisk plassering i butikken.
- Sammenhengen mellom hylleplass og salg kan modelleres kvantitativt.

**Begrensninger:**
- Én butikk (Coop Extra X).
- Én varekategori (defineres i samarbeid med butikken).
- Maksimalt 10 produkter (SKU) i analysen.
- Kampanjer, prisendringer og sesongeffekter modelleres ikke eksplisitt.
- Ingen fysisk implementering — prosjektet leverer analyse og forslag.

### 2.2 Krav

| # | Krav | Type |
|---|------|------|
| K1 | Modellen skal ta inn historiske salgsdata (ukentlig) og hylleplassdata per produkt | Data |
| K2 | Modellen skal identifisere produkter med mismatch mellom etterspørsel og hyllekapasitet | Funksjonell |
| K3 | Modellen skal foreslå reallokering av hylleplass innen fast total kapasitet | Funksjonell |
| K4 | Målfunksjonen skal maksimere forventet total omsetning gitt fast hyllekapasitet | Funksjonell |
| K5 | Sekundære indikatorer: kapasitetsmismatch og risiko for tomme hyller | Funksjonell |
| K6 | Beslutningsvariabler: tildelt hylleplass per produkt (facings/hyllemeter) | Modell |
| K7 | Modellen skal implementeres i Python | Teknisk |
| K8 | Resultater skal valideres mot faktiske data (sensitivitetsanalyse) | Kvalitet |
| K9 | Data skal anonymiseres i rapport og presentasjoner | Etikk |

### 2.3 Løsning

Den overordnede løsningen består av følgende hovedkomponenter:

1. **Datainnhenting og klargjøring** — Samle inn salgsdata og hylleplassdata, rense og strukturere for analyse.
2. **Etterspørselsanalyse** — Analysere salgsmønstre per produkt for å estimere etterspørselsnivå.
3. **Kapasitets-/etterspørselsmodell** — Bygge en kvantitativ modell som kobler hyllekapasitet til etterspørsel og identifiserer mismatch.
4. **Optimaliseringsmodell** — Formulere og løse et optimaliseringsproblem for reallokering av hylleplass.
5. **Validering og sensitivitetsanalyse** — Teste modellens robusthet og følsomhet for parameterendringer.
6. **Rapportering** — Dokumentere funn i vitenskapelig rapport med Python-kode.

### 2.4 Arbeidsnedbrytningsstruktur (WBS)

```
1. Prosjektstyring
   1.1 Prosjektplan (denne)
   1.2 Ukentlig koordinering
   1.3 Statusrapportering

2. Litteratur og teori
   2.1 Litteratursøk (space management, shelf allocation)
   2.2 Teorikapittel i rapport

3. Data
   3.1 Avklaring av datatilgang med Coop Extra X
   3.2 Datainnhenting
   3.3 Datarensing og strukturering
   3.4 Anonymisering

4. Modell og analyse
   4.1 Etterspørselsanalyse (deskriptiv statistikk, trender)
   4.2 Kapasitets-/etterspørselsmodell
   4.3 Optimaliseringsmodell (formulering og implementering)
   4.4 Løsning og resultater

5. Validering
   5.1 Sensitivitetsanalyse
   5.2 Sammenligning nåværende vs. foreslått allokering

6. Rapport
   6.1 Innledning og problemstilling
   6.2 Casebeskrivelse
   6.3 Data og metode
   6.4 Modell
   6.5 Analyse og resultater
   6.6 Diskusjon
   6.7 Konklusjon
   6.8 Referanser

7. Presentasjon
   7.1 Forberedelse muntlig presentasjon
   7.2 Muntlig eksamen
```

---

## 3. Fremdrift

### 3.1 Gantt-plan

```
Aktivitet                        Uke: 10   11   12   13   14   15   16   17   18   19   20   21   22
                                      Mar              Apr                    Mai
                                      2-8  9-15 16-22 23-29 30-5 6-12 13-19 20-26 27-3 4-10 11-17 18-24 25-31

1.  Prosjektplan (fase 2)        ████
2.  Litteratursøk                ████ ████ ████
3.  Avklare datatilgang               ████ ████
4.  Datainnhenting                         ████ ████
5.  Datarensing/strukturering                   ████ ████
6.  Etterspørselsanalyse                             ████ ████
7.  Optimaliseringsmodell                                  ████ ████ ████
8.  Resultater og validering                                         ████ ████
9.  Hovedutkast rapport          ---- ---- ---- ---- ---- ---- ---- ████ ████
10. Peer-to-peer review                                                   ████
11. Revisjon etter review                                                      ████
12. Ferdigstillelse rapport                                                         ████ ████
13. Muntlig presentasjon                                                                  ████ ████

████ = aktivt arbeid    ---- = pågående bakgrunnsarbeid
```

### 3.2 Kritisk linje

Den kritiske linjen i prosjektet er:

**Datatilgang avklart → Datainnhenting → Datarensing → Modellutvikling → Resultater → Hovedutkast**

Forsinkelser i datatilgang vil direkte forsinke hele prosjektet. Derfor er tidlig kontakt med Coop Extra X og parallelt arbeid med litteratur/teori avgjørende.

### 3.3 Milepæler

| Milepæl | Dato | Beskrivelse |
|---------|------|-------------|
| M1 | 9. mars | Godkjent prosjektplan (fase 2) |
| M2 | 22. mars | Datatilgang avklart med Coop Extra X |
| M3 | 5. april | Datasett ferdig renset og strukturert |
| M4 | 19. april | Modell implementert og kjørt |
| M5 | 27. april | Hovedutkast til rapport levert (fase 3) |
| M6 | 29. april | Peer-to-peer review gjennomført |
| M7 | 18. mai | Endelig rapport og kode levert |
| M8 | 25.–31. mai | Muntlig presentasjon (fase 4) |

---

## 4. Risiko

### 4.1 Prosess for risikostyring

Risikoregisteret gjennomgås på hvert gruppemøte. Hvert gruppemedlem har ansvar for å overvåke risikoer knyttet til sine oppgaver og varsle gruppen tidlig ved tegn til at en risiko kan inntreffe.

### 4.2 Risikoregister

| # | Risiko | Sannsynlighet | Konsekvens | Risikoverdi | Tiltak | Beredskapsplan |
|---|--------|:---:|:---:|:---:|--------|----------------|
| R1 | Manglende eller forsinket datatilgang fra Coop Extra X | Middels | Høy | **Høy** | Ta kontakt tidlig (uke 10). Følge opp ukentlig. Ha taushetserklæring klar. | Bruke simulerte/syntetiske data basert på realistiske parametere. |
| R2 | Datakvalitet er utilstrekkelig (manglende verdier, inkonsistens) | Middels | Middels | **Middels** | Sette av nok tid til datarensing. Avklare dataformat tidlig. | Avgrense til produkter/perioder med komplett data. Supplere med antagelser. |
| R3 | Optimaliseringsmodellen blir for kompleks for tidsrammen | Lav | Middels | **Lav** | Starte med enkel modell og utvide gradvis. Følge prinsippet «god modell ≠ komplisert modell». | Levere en enklere, men fullstendig modell fremfor en avansert, ufullstendig en. |
| R4 | Gruppemedlem blir utilgjengelig (sykdom, annet) | Lav | Middels | **Lav** | Alle har oversikt over hele prosjektet. Kode og dokumenter deles via GitHub. | Omfordele oppgaver. Justere omfang om nødvendig. |
| R5 | Tidspress mot slutten av semesteret | Middels | Middels | **Middels** | Jevn innsats gjennom hele semesteret. Starte rapportskriving tidlig. Følge Gantt-planen. | Prioritere kjerneleveranser (modell + rapport) over perfeksjon i detaljer. |
| R6 | Peer-to-peer review avdekker vesentlige mangler | Lav | Middels | **Lav** | Levere solid hovedutkast ved å følge rapportstrukturen fra forelesningene. | Sette av revisjonsbuffer (uke 19) etter review. |

---

## 5. Ressurser

### 5.1 Prosjektteam

| Navn | Rolle | Hovedansvar |
|------|-------|-------------|
| Sebastian Vambheim Thunestvedt | Prosjektleder / utvikler | Prosjektstyring, modellimplementering (Python), GitHub |
| Frida Berge-Robertson | Analytiker / forfatter | Dataanalyse, litteratursøk, rapportskriving |
| Oliver Matre Hille | Bedriftskontakt / analytiker | Kontakt med Coop Extra X, datainnhenting, validering |

*Rollene er fleksible — alle bidrar på tvers av oppgaver etter behov.*

### 5.2 Verktøy og ressurser

| Verktøy | Formål |
|---------|--------|
| Python (pandas, scipy/PuLP, matplotlib) | Dataanalyse, optimalisering, visualisering |
| GitHub | Versjonskontroll for kode og rapport |
| Microsoft Teams | Kommunikasjon og møter |
| Word / Markdown | Rapportskriving |
| Gantt-verktøy (f.eks. Excel/Mermaid) | Fremdriftsoppfølging |

### 5.3 Estimert arbeidsinnsats

| Fase | Periode | Estimerte timer per person per uke | Totalt (3 pers.) |
|------|---------|:---:|:---:|
| Fase 2 — Planlegging | Uke 10–11 | 10 | 60 t |
| Fase 3 — Gjennomføring | Uke 11–18 | 12–15 | ~300 t |
| Fase 4 — Avslutning | Uke 19–22 | 10–12 | ~130 t |
| **Totalt** | | | **~490 t** |

---

## 6. Kommunikasjon

### 6.1 Interne gruppemøter

| Hva | Hyppighet | Når | Varighet | Format |
|-----|-----------|-----|----------|--------|
| Arbeidsmøte / koordinering | 2× per uke | Mandag og torsdag | 1–2 timer | Teams / fysisk |
| Kort statussjekk | Daglig (hverdager) | Morgen | 10 min | Teams-chat |

**Agenda for ukentlige møter:**
1. Status på oppgaver siden forrige møte
2. Gjennomgang av risikoregister (kort)
3. Planlegging av neste ukes oppgaver
4. Eventuelle blokkere eller behov for hjelp

### 6.2 Ekstern kommunikasjon

| Hvem | Hyppighet | Kanal |
|------|-----------|-------|
| Emneansvarlige (Rekdal/Pettersen) | Ved behov, minimum ved fasemilepæler | Teams / e-post |
| Coop Extra X kontaktperson | Ved behov, primært i datainnhentingsperioden | E-post / telefon |
| Koordinator (Erik Langelo) | Ved administrative spørsmål | Teams / e-post |

### 6.3 Dokumentdeling og versjonskontroll

- All kode versjoneres i GitHub-repositoriet.
- Rapportutkast deles via GitHub eller Teams.
- Navnekonvensjon for filer: `[dato]_[beskrivelse]_[versjon]` (f.eks. `2026-04-27_hovedutkast_v1`).

---

## 7. Kvalitet

### 7.1 Kvalitetsprinsipper

Prosjektet følger rapportstrukturen definert i forelesningene:

1. Innledning → 2. Teori/litteratur → 3. Casebeskrivelse → 4. Data og metode → 5. Modell → 6. Analyse og resultater → 7. Diskusjon → 8. Konklusjon → 9. Referanser

**Viktige kvalitetsskiller:**
- Resultater ≠ Diskusjon (objektiv presentasjon vs. tolkning)
- Modell ≠ Metode (formuleringen vs. fremgangsmåten)
- Data ≠ Tolkning (fakta vs. analyse)

### 7.2 Fagfellevurdering (peer-to-peer review)

I fase 3 skal gruppen gjennomføre en peer-to-peer review med en annen gruppe (tildelt av emneansvarlige). Hovedutkastet skal være ferdig innen **27. april**, og review gjennomføres **29. april**.

Reviewkriterier:
- Er problemstillingen tydelig og kvantitativ?
- Er modellen riktig formulert og implementert?
- Er resultatene presentert objektivt?
- Er diskusjonen skilt fra resultatene?
- Er referansene konsistente (APA/Harvard)?

### 7.3 Intern kvalitetssikring

- Hvert rapportkapittel gjennomgås av minst ett annet gruppemedlem før sammenslåing.
- Python-kode gjennomgås (code review) via GitHub.
- Resultater valideres gjennom sensitivitetsanalyse.
- Alle data lagres strukturert: rådatamappe (uendret) + arbeidskopier.

### 7.4 Referansehåndtering

- Konsekvent bruk av APA/Harvard-stil.
- Alle teorier, modeller, tall og figurer fra andre kilder refereres.
- KI-generert faglig innhold refereres eksplisitt.
- Parafraser brukes fremfor direkte sitat der mulig.

---

## Vedlegg

### Vedlegg A — Taushetserklæring

Taushetserklæring signeres med Coop Extra X før datatilgang innvilges. Mal finnes i `000 templates/Taushetsærklæring.docx`.

### Vedlegg B — Referanse til proposal

Godkjent prosjektbeskrivelse (proposal) finnes i prosjektets dokumentasjon. Proposalet definerer området, problemstillingen, data, beslutningsvariabler, målfunksjon og avgrensninger som denne prosjektplanen bygger videre på.
