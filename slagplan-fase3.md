# Slagplan Fase 3 — LOG650 G22

**Opprettet:** 2026-04-24
**Status:** 5 uker til innlevering, alle kapitler i `005 report/rapport.md` er tomme.
**Team:** Sebastian Vambheim Thunestvedt (prosjektleder/utvikler), Frida Berge-Robertson (analytiker/forfatter).
**NB:** Oliver Matre Hille er ikke lenger med i prosjektet per 2026-04-24. Ansvarsfordeling under er oppdatert.

---

## 1. Kontekst

- **Innleveringsdato:** 2026-05-31 (M3)
- **Gjenstående tid:** 5 uker og 1 helg
- **Opprinnelig M2:** 2026-04-27 (utkast + peer review) — **utsatt til 2026-05-10**
- **Opprinnelig skippertaks-risiko:** Prosjektet har ligget etter plan. Fase 3 aktiviteter er ikke påbegynt i praksis.

## 2. Relevant kvantitativ metode

**Primærmetode: Lineær programmering (LP)** via Python + PuLP.
Problemstillingen er et klassisk *space allocation problem* / *assortment optimization*-problem innen Operations Research.

**Støttemetoder:**

| Metode | Formål | Kapittel |
|---|---|---|
| **Lineær programmering (LP)** | Optimal reallokering av hyllekapasitet per produkt for maks forventet omsetning | §6 Modellering, §7 Resultater |
| **Deskriptiv statistikk** | Salgsmønstre, kapasitetsgrad, mismatch per produkt | §5.2 Data, §7 |
| **ABC-klassifisering** | Pareto-analyse: identifisere A/B/C-produkter etter omsetning | §7 Analyse |
| **Sensitivitetsanalyse** | Robusthet mot endringer i etterspørsels-parameterne | §7 Analyse |

Modellens kjerne (fra prosjektplan):

- Beslutningsvariabler: `x_i` = antall frontfacings for produkt `i`
- Målfunksjon: maksimer Σ(forventet omsetning per produkt)
- Restriksjoner: total hyllekapasitet, minimum/maksimum per produkt

Ingen ML/AI-modeller brukes som fagmetode. KI brukes som arbeidsverktøy (kodegenerering, tekstproduksjon, sparring) men er ikke gjenstand for analyse.

## 3. Ukentlig plan

### Uke 17: Datafundament og modell (24.04–30.04)

| Dag | Aktivitet | Leveranse | Ansvar |
|---|---|---|---|
| Fre 24.04 | Datarensing med pandas | `006 analysis/data_clean.ipynb`, renset CSV | Sebastian |
| Lør–Søn 25–26.04 | Etterspørselsanalyse (deskriptiv + ABC) | Tabeller + figurer | Sebastian |
| Man–Tir 27–28.04 | LP-modell formulering matematisk | `rapport.md` §6 utkast | Sebastian + Frida |
| Ons–Tor 29–30.04 | Implementere LP i PuLP | `006 analysis/lp_model.py` + baseline resultater | Sebastian |

### Uke 18: Parallellskriving (01.05–04.05)

| Dag | Aktivitet | Leveranse | Ansvar |
|---|---|---|---|
| Fre 01.05 (fri) | Lese 3–4 prioriterte referanser, KI-sammendrag | Stikkord til §2 + §3 | Frida |
| Lør–Søn 02–03.05 | Skrive teori + casebeskrivelse parallelt | §3 Teori, §4 Casebeskrivelse | Frida (teori), Sebastian (case) |
| Man 04.05 | Skrive metode + data-kapittel | §5 Metode og data | Sebastian |

### Uke 19: Resultater og hovedutkast → ny M2 (05.05–11.05)

| Dag | Aktivitet | Leveranse |
|---|---|---|
| Tir–Tor 05–07.05 | Sensitivitetsanalyse, figurer, tabeller | §7 Analyse og resultater |
| Fre–Lør 08–09.05 | Diskusjonskapittel | §8 Diskusjon |
| **Søn 10.05** | **Ny M2: Hovedutkast komplett, send til peer review** | Rapport med innhold i alle kapitler |

### Uke 20: Revisjon (12.05–18.05)

- Motta peer review-tilbakemeldinger, revidere
- Skrive innledning + konklusjon (til sist — iht. SKRIVING-kompendium §4)
- Kvalitetssikring, figur-sjekk, konsistens mot problemstilling

### Uke 21: Ferdigstilling (19.05–25.05)

- Korrektur
- APA 7-referanseliste
- Forberede muntlig presentasjon
- Rydde Python-kode, README for vedlegg

### Uke 22: Innlevering + muntlig (26.05–31.05)

- **31.05**: Endelig innlevering + muntlig eksamen (M3)

## 4. Risiko og mitigering

| Risiko | Sannsynlighet | Konsekvens | Tiltak |
|---|---|---|---|
| LP-modell gir ikke meningsfulle resultater | Middels | Høy | Kjør dummydata først, sammenlign med intuitiv baseline |
| Peer review-partner forsinket | Middels | Middels | Start diskusjon med rev-gruppen nå om levering 10.05 |
| For mye tid på kode, for lite på rapport | Høy | Høy | 60% av tiden etter uke 18 SKAL være skriving, ikke kode |
| Oliver-utgang forsinker analytiske oppgaver | Middels | Middels | Sebastian tar over hans oppgaver; Frida tar mer skriving |

## 5. Daglig kadens

- **Mandag + torsdag 09:00**: 1–2t arbeidsmøte (iht. prosjektplan §6.1)
- **Mandag–fredag morgen**: 5 min statussjekk i Teams-chat
- **Hver kveld**: commit arbeidet til git

## 6. Definition of done for hvert kapittel

| Kapittel | DOD |
|---|---|
| §1 Innledning | Problemstilling → presis. Avgrensning → tydelig. Ingen resultater nevnt. |
| §2 Litteratur | Minst 5 referanser, koblet til problemstilling |
| §3 Teori | LP-teori, space elasticity, demand-capacity mismatch forklart |
| §4 Casebeskrivelse | Kontekst Coop Extra X, valgt kategori (brus 0.5L) beskrevet |
| §5 Metode og data | Hva-hvorfor-hvordan for datarensing + LP. Reproduserbar |
| §6 Modellering | Matematisk formulering med symboltabell. Ingen tall |
| §7 Resultater | Tabeller og figurer. Objektiv presentasjon. |
| §8 Diskusjon | Tolkning mot teori. Styrker/svakheter. Implikasjoner |
| §9 Konklusjon | Eksplisitt svar på problemstilling. Ingen nye funn |
| Bibliografi | APA 7, komplett |

## 7. Neste konkrete handling (i dag)

Sebastian starter med datarensing og første deskriptive analyse. Dette låser opp alt annet.

Konkret: opprette `006 analysis/` struktur med notebook som leser `004 data/Data 10 uker.csv`, renser, og skriver forberedte datasett for LP-modellen.
