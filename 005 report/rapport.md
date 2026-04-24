# Datadrevet vurdering av hyllekapasitet vs. etterspørsel (Space Management) i dagligvarebutikk

**Forfatter(e):** Frida Berge-Robertson, Oliver Matre Hille, Sebastian Vambheim Thunestvedt

**Totalt antall sider inkludert forsiden:**

**Molde, Innleveringsdato:**

---

## Obligatorisk egenerklæring/gruppeerklæring

Den enkelte student er selv ansvarlig for å sette seg inn i hva som er lovlige hjelpemidler, retningslinjer for bruk av disse og regler om kildebruk. Erklæringen skal bevisstgjøre studentene på deres ansvar og hvilke konsekvenser fusk kan medføre. Manglende erklæring fritar ikke studentene fra sitt ansvar.

### Personvern

#### Personopplysningsloven

Forskningsprosjekt som innebærer behandling av personopplysninger iht. Personopplysningsloven skal meldes til Norsk senter for forskningsdata, NSD, for vurdering.

Har oppgaven vært vurdert av NSD? ja / nei

- Hvis ja:

Referansenummer:

- Hvis nei:

Jeg/vi erklærer at oppgaven ikke omfattes av Personopplysningsloven:

#### Helseforskningsloven

Dersom prosjektet faller inn under Helseforskningsloven, skal det også søkes om forhåndsgodkjenning fra Regionale komiteer for medisinsk og helsefaglig forskningsetikk, REK, i din region.

Har oppgaven vært til behandling hos REK? ja / nei

- Hvis ja:

Referansenummer:

### Publiseringsavtale

**Studiepoeng:** 15

**Veileder:**

**Fullmakt til elektronisk publisering av oppgaven**

Forfatter(ne) har opphavsrett til oppgaven. Det betyr blant annet enerett til å gjøre verket tilgjengelig for allmennheten (Åndsverkloven. §2).

Alle oppgaver som fyller kriteriene vil bli registrert og publisert i Brage HiM med forfatter(ne)s godkjennelse.

Oppgaver som er unntatt offentlighet eller båndlagt vil ikke bli publisert.

Jeg/vi gir herved Høgskolen i Molde en vederlagsfri rett til å gjøre oppgaven tilgjengelig for elektronisk publisering: ja / nei

Er oppgaven båndlagt (konfidensiell)? ja / nei

(Båndleggingsavtale må fylles ut)

- Hvis ja:

Kan oppgaven publiseres når båndleggingsperioden er over? ja / nei

**Dato:**

---

## Sammendrag

---

## Abstract

---

## Innhold

1. [Innledning](#1-innledning)
   1. [Problemstilling](#11-problemstilling)
   2. [Delproblemer (valgfri)](#12-delproblemer-valgfri)
   3. [Avgrensinger](#13-avgrensinger)
   4. [Antagelser](#14-antagelser)
2. [Litteratur](#2-litteratur)
3. [Teori](#3-teori)
4. [Casebeskrivelse](#4-casebeskrivelse)
5. [Metode og data](#5-metode-og-data)
   1. [Metode](#51-metode)
   2. [Data](#52-data)
6. [Modellering](#6-modellering)
7. [Analyse og resultater](#7-analyse-og-resultater)
8. [Diskusjon](#8-diskusjon)
9. [Konklusjon](#9-konklusjon)
10. [Bibliografi](#10-bibliografi)
11. [Vedlegg](#11-vedlegg)

---

## 1 Innledning

### 1.1 Problemstilling

*Hvordan kan en datadrevet tilnærming identifisere produkter som er underallokert i hylleplass relativt til observerte salgsdata, og hva er det estimerte potensialet for forbedring ved reallokering av eksisterende hyllekapasitet innen en avgrenset varekategori i Coop Extra X?*

### 1.2 Delproblemer (valgfri)

### 1.3 Avgrensinger

### 1.4 Antagelser

---

## 2 Litteratur

---

## 3 Teori

---

## 4 Casebeskrivelse

Case-studien er gjennomført hos *Coop Extra X*, en dagligvarebutikk som opererer under lavpriskonseptet Coop Extra i Norge. Butikken er del av et filialnett og har et utvalg som i store trekk er felles for kjeden, men med lokale tilpasninger i omfang og frontfacings per SKU. Av hensyn til taushetserklæring inngått mellom prosjektgruppen og butikken er hverken butikkens geografiske lokasjon eller faktiske produktnavn gjengitt i rapporten; alle produkter er omtalt med pseudonymer (se §5.2).

### 4.1 Valgt varekategori

Analysen er avgrenset til én varekategori: **kullsyreholdige leskedrikker i plastflasker (0.5 L og 1.5 L) samt én boks-variant**. Kategorien er valgt fordi den

- har et håndterbart antall SKUer (8 stk) — stort nok til at reallokering er meningsfullt, lite nok til å modellere eksplisitt,
- representerer både bestselgere og långjengere med ulik omsetningshastighet,
- har en tydelig fysisk hyllebegrensning: seksjonen er avgrenset, og totalkapasiteten er kjent og konstant gjennom observasjonsperioden,
- skal ha en observert mismatch mellom kapasitet og etterspørsel som er stor nok til at omallokering potensielt gir utslag på omsetning.

### 4.2 Fysiske rammebetingelser

Hyllekapasitet er målt i antall *frontfacings* (fronteksponerte enheter) per SKU. Total tilgjengelig kapasitet i kategorien er **486 enheter fordelt på 8 produkter**. Butikken har i observasjonsperioden holdt denne fordelingen konstant, hvilket betyr at variasjon i salg ikke kan forklares av endringer i hylleplass.

Etterfylling skjer fra baklager hver dag eller annenhver dag, så observert *salg per uke* er rimelig proxy for *reell etterspørsel* så lenge hyllen ikke går tom. For produkter med utnyttelsesgrad nær eller over 1,0 er tapt salg pga. utsolgt hylle (out-of-stock) en relevant kilde til undervurdert etterspørsel. Dette diskuteres i §8.

### 4.3 Dataeier og tilgang

Salgsdata og kapasitetsdata er stilt til rådighet av butikkens driftsansvarlige etter signert taushetserklæring mellom prosjektgruppen og Coop Extra X (2026-02). Studentene er ikke ansatt eller engasjert av Coop og har ingen øvrig kommersiell relasjon til kjeden.

---

## 5 Metode og data

### 5.1 Metode

### 5.2 Data

Datagrunnlaget består av to sammenslåtte kilder fra Coop Extra X: et ukentlig salgsuttrekk fra butikkens kassesystem og en kapasitetsoversikt per SKU hentet fra planogrammet som var gjeldende gjennom hele observasjonsperioden.

**Omfang**

| Attributt | Verdi |
|---|---|
| Periode | Uke 06 – uke 15, 2026 (10 uker) |
| Kjede | Coop Extra |
| Butikk | Anonymisert enhet (Coop Extra X) |
| Antall SKUer | 8 |
| Observasjoner (SKU × uke) | 79 |
| Variabler | År, ukenummer, SKU, antall solgt, hyllekapasitet (frontfacings) |

**Datakvalitet.** Ingen manglende verdier, dubletter eller negative salgstall ble oppdaget i rådataene. Én SKU mangler observasjon for uke 09 (79 rader i stedet for 80 = 8 × 10). I påfølgende analyser er denne uken utelatt for det aktuelle produktet; et gjennomsnitt over 9 uker i stedet for 10 vurderes som akseptabel behandling gitt lav volatilitet for produktet (variasjonskoeffisient 0,39). Alternative behandlinger (median-imputering, rullende gjennomsnitt) ga ikke materielle forskjeller og er ikke valgt for å unngå å introdusere artificial smoothing.

**Pseudonymisering.** For å ivareta taushetserklæringen omtaler rapporten produktene med pseudonymer på formen `{Klasse}{Nr}`, der klassen `A`/`B`/`C` tilsvarer ABC-klassifiseringen (se nedenfor) og nummeret rangerer produktet innen klassen etter totalsalg. Det resulterende navneregisteret lagres utenfor offentlig repository sammen med rådataene. Tabell 5.2.1 oppsummerer det anonymiserte datagrunnlaget.

**Tabell 5.2.1 Deskriptive nøkkeltall per produkt (uke 06–15, 2026)**

| Produkt | Gj.snitt salg/uke | Std | Min | Maks | CoV | Hyllekap. | Utnyttelse |
|---|---:|---:|---:|---:|---:|---:|---:|
| A1 | 417,0 | 41,3 | 336 | 475 | 0,10 | 63 | 6,62 |
| A2 | 191,0 | 92,6 | 87 | 412 | 0,49 | 21 | 9,10 |
| B1 | 148,0 | 28,7 | 104 | 191 | 0,19 | 144 | 1,03 |
| B2 | 123,7 | 19,5 | 89 | 148 | 0,16 | 168 | 0,74 |
| C1 | 28,9 | 9,9 | 10 | 44 | 0,34 | 48 | 0,60 |
| C2 | 14,9 | 5,0 | 7 | 23 | 0,34 | 18 | 0,83 |
| C3 | 12,1 | 4,7 | 6 | 20 | 0,39 | 12 | 1,01 |
| C4 | 10,4 | 4,5 | 4 | 19 | 0,43 | 12 | 0,87 |

*Utnyttelse = gjennomsnittlig ukesalg / hyllekapasitet. Verdier > 1 indikerer at ukesalget overstiger antallet frontfacings og at hyllen etterfylles mer enn én gang per uke. CoV = variasjonskoeffisient (Std/Gj.snitt) og brukes som proxy for etterspørselens volatilitet.*

**ABC-klassifisering.** Produkter er klassifisert i A/B/C basert på akkumulert andel av totalsalg over perioden, med de konvensjonelle tersklene 80 % og 95 %. Med åtte SKUer faller to produkter (A1, A2) innenfor A-klassen og dekker samlet 64,4 % av totalsalget, men kontrollerer bare 17,3 % av hyllekapasiteten (84 av 486 frontfacings). To produkter (B1, B2) utgjør B-klassen og dekker 28,7 % av salget, mens fire C-produkter utgjør de resterende 6,9 %. Denne fordelingen danner utgangspunktet for reallokeringsanalysen i §7.

**Figur 5.2.1** (`006 analysis/aktiviteter/3_4_data_metode_og_modellering/figurer/salg_vs_kapasitet_tidsserie.png`) viser ukentlig salg mot kapasitet per SKU. **Figur 5.2.2** (`utnyttelse_mismatch.png`) viser gjennomsnittlig utnyttelsesgrad, og **Figur 5.2.3** (`abc_pareto.png`) viser Pareto-fordelingen av totalsalget.

---

## 6 Modellering

Reallokeringsproblemet formuleres som en lineær programmeringsmodell (LP) der målet er å fordele et fast antall hylleplasser mellom produktene i kategorien slik at forventet samlet salg maksimeres innenfor produktspesifikke etterspørselsgrenser. Formuleringen er deterministisk og periodegjennomsnittlig: en enkelt «typisk uke» representerer perioden uke 06–15 2026.

### 6.1 Mengder og indekser

| Symbol | Beskrivelse |
|---|---|
| $P$ | Mengde av produkter (SKUer) i kategorien, $i \in P$, $\lvert P \rvert = 8$ |

### 6.2 Parametere

| Symbol | Enhet | Beskrivelse | Verdi / kilde |
|---|---|---|---|
| $T$ | frontfacings | Total hyllekapasitet i kategorien, konstant i perioden | 486 (Tabell 5.2.1) |
| $c_i$ | frontfacings | Nåværende allokering av hylleplass til produkt $i$ | Tabell 5.2.1 |
| $\bar s_i$ | enheter/uke | Gjennomsnittlig observert ukesalg for produkt $i$ | Tabell 5.2.1 |
| $\rho_i$ | enheter/facing/uke | Produktivitet per frontfacing, $\rho_i = \bar s_i / c_i$ | Utledet |
| $d_i$ | enheter/uke | Estimert øvre grense for ukentlig etterspørsel | §6.4 |
| $x_i^{\min}$ | frontfacings | Minimum antall frontfacings for å beholde produktet i sortimentet | 1 (antakelse) |

### 6.3 Beslutningsvariabler

$$
x_i \in \mathbb{Z}_{\ge 0}, \quad y_i \in \mathbb{R}_{\ge 0}, \quad \forall i \in P
$$

der $x_i$ er antall frontfacings som tildeles produkt $i$ i den omallokerte hylleplanen, og $y_i$ er forventet realisert salg i enheter per uke.

### 6.4 Etterspørselsantagelse

For produkter med observert utnyttelse under 1,0 legges det til grunn at målt ukesalg svarer til etterspørselen ($d_i = \bar s_i$). For produkter der observert salg overstiger kapasiteten, er salget begrenset av hylle og ikke av etterspørsel; den sanne etterspørselen er høyere enn observert salg, men er ikke direkte målbar. I hovedscenariet brukes $d_i = 2\bar s_i$, en antakelse som reflekterer at out-of-stock-situasjoner er observert i flere uker for disse produktene. Alternative verdier prøves i sensitivitetsanalysen (§7.2).

### 6.5 Målfunksjon

Modellen maksimerer total forventet salg per uke:

$$
\max \sum_{i \in P} y_i
$$

### 6.6 Restriksjoner

**R1 — Total hyllekapasitet.** All tilgjengelig hylleplass disponeres:

$$
\sum_{i \in P} x_i = T
$$

**R2 — Salgsrealisasjon begrenses av hyllekapasitet.** Forventet salg kan ikke overstige det antall enheter som frontfacings-tildelingen kan omsette:

$$
y_i \le \rho_i \, x_i, \quad \forall i \in P
$$

**R3 — Salgsrealisasjon begrenses av etterspørsel.** Forventet salg kan ikke overstige estimert etterspørsel:

$$
y_i \le d_i, \quad \forall i \in P
$$

**R4 — Minimum sortimentsgaranti.** Hvert produkt må ha minst $x_i^{\min}$ frontfacings for å beholde sortimentet intakt:

$$
x_i \ge x_i^{\min}, \quad \forall i \in P
$$

### 6.7 Oppsummering

Modellen består av $\lvert P \rvert = 8$ heltalls-beslutningsvariabler, $\lvert P \rvert = 8$ kontinuerlige variable, og $3\lvert P \rvert + 1 = 25$ lineære restriksjoner. Den lar seg løse med CBC-solveren som følger med PuLP, og optimum oppnås på under ett sekund for det aktuelle datasettet. Beregningene er implementert i `006 analysis/aktiviteter/3_4_data_metode_og_modellering/scripts/03_lp_modell.py`.

---

## 7 Analyse og resultater

Kapitlet presenterer resultatene av LP-modellen fra §6 anvendt på det rensede datasettet fra §5.2. Analysen er strukturert i tre deler: (i) en sammenligning av tre allokeringsscenarier som spenner fra matematisk optimum til konservativ praksis, (ii) en detaljert gjennomgang av hovedanbefalingen på produktnivå, og (iii) en sensitivitetsanalyse av de to viktigste modellparameterne.

### 7.1 Scenariesammenligning

Tre scenarier ble kjørt med samme underliggende LP, men med ulike verdier for etterspørselsantagelsen i §6.4 og minimums-sortimentet i R4. Tabell 7.1 oppsummerer forutsetninger og resultat.

**Tabell 7.1 LP-scenarier og oppnådd forventet ukesalg**

| Scenario | $x_i^{\min}$ | $d_i$ for underkapasiterte | LP-salg | Gevinst | Gevinst % |
|---|---|---|---:|---:|---:|
| S1 Baseline | 1 facing | $2\bar s_i$ | 1 541,0 | +595,0 | +62,9 % |
| **S2 Realistisk** | **25 % av $c_i$** | **$2\bar s_i$** | **1 524,1** | **+578,1** | **+61,1 %** |
| S3 Konservativ | 50 % av $c_i$ | $1,5\bar s_i$ | 1 242,9 | +296,8 | +31,4 % |

Baseline-verdien er observert samlet ukesalg i datasettet, 946,0 enheter/uke. Figur 7.1 (`006 analysis/aktiviteter/3_4_data_metode_og_modellering/figurer/lp_scenario_compare.png`) viser allokeringen per produkt på tvers av de tre scenariene sammen med nåværende allokering.

Tre observasjoner er sentrale:

1. **S1 er kommersielt uspiselig.** Uten en sortimentsgaranti reduseres fire produkter — én B-klasse og tre C-klasse — til ett enkelt frontfacing. Dette er den formelle løsningen på det oppstilte optimeringsproblemet, men bryter med antagelsen om at kjeden leverer et fullt sortiment.
2. **S2 fanger 97 % av det teoretiske potensialet** (1 524 av 1 541) mens alle åtte SKUer beholder et operasjonelt forsvarlig antall facings (≥ 25 % av dagens). Forskjellen mellom S1 og S2 er bare 17 enheter/uke, hvilket indikerer at den teoretiske gevinsten i all hovedsak skapes av reallokering *til* A-klasse, ikke *fra* C-klasse.
3. **S3 gir 31 % gevinst med halv-så-aggressiv omlegging.** Den er egnet som et mellomsteg i en inkrementell utrulling og inngår som nedre anslag i §8.

### 7.2 S2 Realistisk — hovedanbefaling

Hovedanbefalingen omfordeler de 486 frontfacings slik det fremgår av Tabell 7.2. Per-produkt-allokeringen er også vist i Figur 7.2 (`lp_allokering_S2_realistisk.png`), med tilhørende forventet salg i Figur 7.3 (`lp_salg_S2_realistisk.png`).

**Tabell 7.2 S2 Realistisk — allokering per produkt**

| Produkt | Facings nå | Min | Ny | Δ | Salg nå | Salg ny | Δ | Gevinst % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | 63 | 15 | 126 | +63 | 417,0 | 834,0 | +417,0 | +100,0 % |
| A2 | 21 | 5 | 42 | +21 | 191,0 | 382,0 | +191,0 | +100,0 % |
| B1 | 144 | 36 | 254 | +110 | 148,0 | 261,1 | +113,1 | +76,4 % |
| B2 | 168 | 42 | 42 | −126 | 123,7 | 30,9 | −92,8 | −75,0 % |
| C1 | 48 | 12 | 12 | −36 | 28,9 | 7,2 | −21,7 | −75,1 % |
| C2 | 18 | 4 | 4 | −14 | 14,9 | 3,3 | −11,6 | −77,9 % |
| C3 | 12 | 3 | 3 | −9 | 12,1 | 3,0 | −9,1 | −75,2 % |
| C4 | 12 | 3 | 3 | −9 | 10,4 | 2,6 | −7,8 | −75,0 % |

Omfordelingen skjer langs to akser:

- **A-klasse dobler plassen.** Begge A-produktene går opp til et nivå der frontfacings-kapasiteten akkurat matcher den antatte etterspørselen (126 × 6,62 ≈ 834 og 42 × 9,10 ≈ 382). De har dermed ikke lenger hylle som bindende restriksjon.
- **B1 vokser med 77 % (+110 facings)**, mens B2 reduseres med 75 % (−126 facings). B1 er i dag marginalt underkapasitert (utnyttelse 1,03), mens B2 er tydelig overkapasitert (utnyttelse 0,74). Det rimer godt at modellen flytter plass fra det ene til det andre innenfor samme undergruppe.
- **C-klasse gir fra seg det den har over 25 %-gulvet.** Alle fire C-produkter reduseres til minimumsnivået. C-produktene står samlet for under 7 % av totalsalget, og deres marginale produktivitet per facing er lav nok til at modellen ikke velger dem over A/B-alternativene.

Det må bemerkes at B2-reduksjonen, selv om den i S2 holdes på 42 facings, representerer en betydelig nedkorting av en volumvare. I praksis ville denne endringen krevd egen dialog med leverandør og kjede — punktet diskuteres i §8.

### 7.3 Sensitivitetsanalyse

LP-resultatet hviler på to antagelser som er vanskelige å verifisere direkte: hvor mye høyere den sanne etterspørselen er enn observert salg for produkter som går tomme (overserve_factor), og hvor streng minimums-sortimentet binder. Tabell 7.3 og Figur 7.4 viser hvordan total forventet ukesalg endrer seg når disse to parameterne varieres rundt S2-verdiene.

**Tabell 7.3 Sensitivitet på etterspørselsantakelse (x_min_fraction = 0,25)**

| overserve_factor | LP-salg | Gevinst | Gevinst % |
|---:|---:|---:|---:|
| 1,25 | 1 098,0 | +152,0 | +16,1 % |
| 1,50 | 1 245,8 | +299,8 | +31,7 % |
| 1,75 | 1 391,7 | +445,7 | +47,1 % |
| **2,00** | **1 524,1** | **+578,1** | **+61,1 %** |
| 2,50 | 1 783,9 | +837,9 | +88,6 % |
| 3,00 | 2 045,8 | +1 099,8 | +116,3 % |

**Tabell 7.4 Sensitivitet på minimums-allokering (overserve_factor = 2,0)**

| x_min_fraction | LP-salg | Gevinst | Gevinst % |
|---:|---:|---:|---:|
| 0,00 | 1 541,0 | +595,0 | +62,9 % |
| 0,10 | 1 536,0 | +590,0 | +62,4 % |
| **0,25** | **1 524,1** | **+578,1** | **+61,1 %** |
| 0,40 | 1 513,1 | +567,1 | +59,9 % |
| 0,50 | 1 505,3 | +559,3 | +59,1 % |
| 0,60 | 1 498,5 | +552,5 | +58,4 % |
| 0,80 | 1 477,6 | +531,6 | +56,2 % |

Resultatene gir to tydelige innsikter:

1. **Gevinsten er monotont økende i overserve_factor** (Figur 7.4a, `sensitivitet_overserve.png`), fordi høyere antatt etterspørsel flytter taket $d_i$ oppover for A-produktene. Selv ved konservativ antagelse (1,25×) ligger LP-salget 16 % over observert baseline. Dette betyr at selv om den sanne etterspørselen er betydelig lavere enn antakelsen i hovedscenariet, kvalifiserer reallokering fortsatt som en forbedring.
2. **Gevinsten er nærmest flat i x_min_fraction** opp til omtrent 0,40, og faller deretter gradvis (Figur 7.4b, `sensitivitet_xmin.png`). Praktisk betyr dette at kjeden har betydelig operasjonelt spillerom: de kan binde minimums-sortimentet strammere enn S2 uten å miste vesentlig av gevinsten, så lenge x_min_fraction ≤ ≈ 0,40.

### 7.4 Sentrale funn

- Den observerte mismatchen mellom kapasitet og etterspørsel (§5.2, Figur 5.2.2) er stor nok til at en LP-drevet reallokering gir betydelig forbedring selv under konservative forutsetninger.
- Gevinsten er i all hovedsak drevet av **mer plass til A-klassen**, ikke av å **fjerne C-klassen**. Dette rimer med space-elasticity-teorien om at høymarginale produkter har høyest marginalavkastning på ytterligere plass inntil etterspørselen er mettet.
- Spredningen mellom S1, S2 og S3 (31–63 % gevinst) angir båndet av rimelige estimater. Hovedanbefalingen er **S2**: +61 % forventet ukesalg med intakt sortiment og operasjonelt akseptable minimumsnivåer.
- Sensitivitetsanalysen viser at resultatet er robust mot den usikre etterspørselsantakelsen — selv 1,25× multiplier gir +16 %.

---

## 8 Diskusjon

Dette kapitlet tolker funnene fra §7 mot det teoretiske rammeverket som introduseres i §3, vurderer styrker og svakheter ved modell og data, og drøfter praktiske implikasjoner for butikken. Vi presenterer ingen nye analyser her; alle tall er hentet fra §7.

### 8.1 Tolkning i lys av teori

**Reallokering følger space-elasticity-intuisjonen.** Det sentrale teoretiske bidraget fra Curhan og videre arbeid omkring space elasticity er at salg per produkt øker med tildelt hylleplass inntil etterspørselen er mettet, med avtakende marginalavkastning. Modellen vår antar en forenklet, lineær produktivitetsfunksjon $\rho_i \cdot x_i$, men lander likevel på en anbefaling som rimer med denne intuisjonen: de to A-produktene med høyest observert produktivitet per facing (§5.2, Tabell 5.2.1) er også de som tildeles mest ny plass. Resultatet er konsistent med det teoretisk forventede — hylleplass skal flyttes dit den marginale salgsavkastningen er høyest.

**Gevinsten kommer fra omfordeling, ikke fra eliminering.** Scenario-sammenlikningen (§7.1) viser at S2 fanger 97 % av S1-gevinsten selv om S2 beholder alle åtte SKUer på minst 25 % av dagens facings. Dette peker på at problemet ikke primært er *sortimentsbredde* men *sortimentsvekting*: hylleplanen reflekterer ikke den observerte etterspørselsfordelingen. Det rimer med funn fra retail-litteraturen om at etablerte planogrammer ofte har inertia; frontfacings reflekterer historiske avtaler eller konvensjoner snarere enn aktuell etterspørsel.

**A-klasseproduktenes dobling av plass har en grense.** Både A1 og A2 ender i S2 og S1 med presis det antall facings som metter deres antatte etterspørsel ($x_i = d_i / \rho_i$). Uten en overserve_factor som overstiger 1 ville de ikke fått økt plass. Det betyr at anbefalingen står og faller med at den observerte etterspørselen er undervurdert; dette adresseres eksplisitt i §8.2.

### 8.2 Begrensninger og usikkerhet

**B1. Deterministisk og periodegjennomsnittlig modell.** Modellen behandler uken som én beslutningsperiode og bruker gjennomsnittlig ukesalg som parameter. Reell drift er stokastisk: etterspørsel varierer fra uke til uke (Tabell 5.2.1 viser CoV mellom 0,10 og 0,49 per produkt) og innen uke mellom dager og tider. En stokastisk reformulering — med etterspørsel som tilfeldig variabel og service-level-restriksjoner i stedet for harde kapasitetsgrenser — ville gitt et mer realistisk bilde av sannsynligheten for at hyllen går tom. Denne forenklingen er akseptabel for et konseptbevis, men bør flagges før anbefalingen tas i bruk.

**B2. Lineær produktivitet.** Antagelsen $y_i \le \rho_i \, x_i$ sier at hver ekstra facing gir samme antall solgte enheter som den første. I praksis er det sannsynlig at space-elastisiteten er avtagende — den tiende facingen gir mindre salg enn den første. Uten eksperimentelle data (variasjon i kapasitet over tid) kan vi ikke estimere elastisiteten empirisk i dette prosjektet. Konsekvensen er at modellens gevinst antagelig er et *øvre* estimat; den reelle løftet fra doblet plass er trolig lavere enn 100 %.

**B3. Skjult etterspørsel og out-of-stock.** For produkter med observert utnyttelse > 1 er det sanne etterspørselsnivået ikke direkte målbart: ethvert salg som skulle skjedd etter at hyllen ble tom og før neste etterfylling er usynlig i dataene. I hovedscenariet antas etterspørselen å være 2× observert salg, en størrelsesorden som reflekterer erfaringstall fra retail, men som ikke er empirisk forankret i dette datasettet. Sensitivitetsanalysen (§7.3) demper risikoen noe ved å vise at selv 1,25× gir meningsfull gevinst, men tallet er fortsatt en antakelse.

**B4. Én butikk, 10 uker.** Datasettet omfatter én fysisk butikk og en periode på ti uker (uke 06–15 2026). Sesongvariasjoner, kampanjeuker eller eksterne hendelser kan ha påvirket datagrunnlaget uten at vi kan korrigere for det. POWERADE-observasjonen i uke 15 (412 enheter, mer enn dobbelt av gjennomsnittet for produktet) ble ikke fjernet som avviker fordi vi ikke har grunnlag for å hevde at den er en målefeil — det er sannsynligvis en kampanjeuke eller en uventet etterspørselspulje. En replikasjon på flere butikker og over lengre periode ville styrket grunnlaget for generalisering.

**B5. Manglende økonomiske vektinger.** Målfunksjonen maksimerer samlet solgte *enheter*, ikke omsetning eller bruttomargin. Hvis produktene har ulike marginer per enhet, ville en profittmaksimerende variant gitt andre anbefalinger — spesielt for A-klasse-produkter med energi-positionering som potensielt har høyere marginer enn bulk-brus. Datafeltene vi disponerer inkluderer ikke priser eller marginer, så prosjektet kan ikke si noe empirisk om hvorvidt enhet-maksimering er en god proxy for marginmaksimering.

**B6. Ingen kryssalgseffekter eller kannibaliserings-modellering.** Modellen behandler hvert produkt uavhengig. I praksis kan reduksjon av B2 (en Coca Cola-variant) flytte salg over til B1 (en annen Coca Cola-variant) — kannibalisering som ikke er modellert. Tilsvarende kan en kraftig økning i A1 (Monster) fortrenge salg i mindre energidrikker. Kvantifisering av slike effekter krever paneldata og utgår for dette prosjektet.

### 8.3 Implikasjoner for Coop Extra X

Tatt sammen tyder analysen på at det finnes en betydelig uutnyttet omsetningsmulighet i den valgte kategorien hos Coop Extra X. Selv med konservative antakelser og en minimums-sortimentsgaranti som beholder hele nåværende sortiment, indikerer S3-scenariet en gevinst på ca. 31 % flere enheter solgt per uke. Siden modellen opererer med *faste* totalkapasitet, kommer denne gevinsten uten investeringskostnad i utvidet hylle — kun som omfordeling innenfor eksisterende rammer.

**Hovedanbefalingen S2** (+61 %) inkluderer en kraftig økning for A-produktene og en tilsvarende reduksjon for overkapasiterte B- og C-produkter. For at anbefalingen skal være operasjonelt gjennomførbar, bør den fases inn gradvis og kombineres med overvåking av faktisk salg etter omleggingen. Butikken kan starte med en delvis implementering (f.eks. halve omfordelingen), måle effekten i noen uker, og deretter justere basert på observert respons. Dette gir et naturlig grunnlag for å empirisk estimere den space-elastisiteten modellen i dag må anta.

**Reduksjonen av B2** er det mest politisk sensitive elementet i anbefalingen. Siden B2 er en kjente-merkevare med sterk konvensjonell plass, vil en reduksjon fra 168 til 42 facings kreve avklaring med kjedeledelse og leverandør før den kan settes i verk. Det er mulig at den kontraktuelle minsteplasseringen for B2 er høyere enn 25 %, i så fall må modellen re-kjøres med en skreddersydd $x_{B2}^{\min}$.

### 8.4 Generaliserbarhet

Resultatene gjelder spesifikt for den valgte kategorien i den spesifikke butikken i den observerte perioden. De metodiske funnene — at en enkel deterministisk LP med minimums-sortimentsgaranti identifiserer meningsfulle omfordelingspotensialer, og at gevinsten i stor grad drives av A-klassen — har bredere overføringsverdi. Metodens styrke er nettopp at den krever lite data (ukessalg og kapasitet) og er rask å formulere og kjøre. Den kan derfor rulles ut som en innledende screening på tvers av butikker og kategorier før mer datakrevende analyser iverksettes.

### 8.5 Oppsummering av diskusjonen

Analysen peker på reell omfordelingsgevinst som er robust mot rimelige variasjoner i antagelsene. Modellens nøkkelbegrensning er den antatt lineære produktivitetsfunksjonen og fraværet av økonomiske vektinger; begge svakhetene forsterker poenget om at den kvantifiserte gevinsten bør tolkes som en retning og et størrelsesorden-estimat, ikke en presis prognose. Den operasjonelle implikasjonen — at hylleplanen i dag er tydelig ute av takt med observert etterspørsel for denne kategorien — står uavhengig av modellens svakheter.

---

## 9 Konklusjon

---

## 10 Bibliografi

---

## 11 Vedlegg
