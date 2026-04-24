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

---

## 7 Analyse og resultater

---

## 8 Diskusjon

---

## 9 Konklusjon

---

## 10 Bibliografi

---

## 11 Vedlegg
