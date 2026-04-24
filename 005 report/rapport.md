# Datadrevet vurdering av hyllekapasitet vs. etterspørsel (Space Management) i dagligvarebutikk

**Forfatter(e):** Frida Berge-Robertson, Sebastian Vambheim Thunestvedt

*Oliver Matre Hille var opprinnelig medlem av prosjektgruppen, men trakk seg fra prosjektet 2026-04-24. Han står ikke oppført som forfatter av denne rapporten.*

**Totalt antall sider inkludert forsiden:** [TBD — fylles ut før innlevering]

**Molde, Innleveringsdato:** 2026-05-31

---

## Obligatorisk egenerklæring/gruppeerklæring

Den enkelte student er selv ansvarlig for å sette seg inn i hva som er lovlige hjelpemidler, retningslinjer for bruk av disse og regler om kildebruk. Erklæringen skal bevisstgjøre studentene på deres ansvar og hvilke konsekvenser fusk kan medføre. Manglende erklæring fritar ikke studentene fra sitt ansvar.

### Personvern

#### Personopplysningsloven

Forskningsprosjekt som innebærer behandling av personopplysninger iht. Personopplysningsloven skal meldes til Norsk senter for forskningsdata, NSD, for vurdering.

Har oppgaven vært vurdert av NSD? **nei**

- Hvis ja:

Referansenummer: —

- Hvis nei:

Jeg/vi erklærer at oppgaven ikke omfattes av Personopplysningsloven: **ja**. Analysen behandler ikke personopplysninger. Datagrunnlaget er aggregerte salgs- og kapasitetsdata per SKU på ukentlig nivå og inneholder ingen informasjon om kundeidentitet, transaksjonsdata på kundenivå eller andre elementer som omfattes av loven.

#### Helseforskningsloven

Dersom prosjektet faller inn under Helseforskningsloven, skal det også søkes om forhåndsgodkjenning fra Regionale komiteer for medisinsk og helsefaglig forskningsetikk, REK, i din region.

Har oppgaven vært til behandling hos REK? **nei**. Prosjektet omhandler hylleallokering i dagligvarehandelen og omfattes ikke av Helseforskningsloven.

- Hvis ja:

Referansenummer: —

### Publiseringsavtale

**Studiepoeng:** 15

**Veileder:** [TBD — bekreftes med emneansvarlige Per Kristian Rekdal / Bård-Inge Pettersen]

**Fullmakt til elektronisk publisering av oppgaven**

Forfatter(ne) har opphavsrett til oppgaven. Det betyr blant annet enerett til å gjøre verket tilgjengelig for allmennheten (Åndsverkloven. §2).

Alle oppgaver som fyller kriteriene vil bli registrert og publisert i Brage HiM med forfatter(ne)s godkjennelse.

Oppgaver som er unntatt offentlighet eller båndlagt vil ikke bli publisert.

Jeg/vi gir herved Høgskolen i Molde en vederlagsfri rett til å gjøre oppgaven tilgjengelig for elektronisk publisering: **nei** (inntil videre — avklares i samråd med Coop Extra X før endelig innlevering på grunn av taushetserklæringen).

Er oppgaven båndlagt (konfidensiell)? **[TBD — avklares med Coop Extra X før innlevering]**. Rådata og interne analyse-artefakter (se §5.2 om pseudonymisering) er omfattet av taushetserklæring og publiseres ikke. Selve rapporten bruker pseudonymer og inneholder ingen direkte identifiserbar bedrifts- eller produktinformasjon.

(Båndleggingsavtale må fylles ut hvis Coop Extra X krever det)

- Hvis ja:

Kan oppgaven publiseres når båndleggingsperioden er over? [TBD]

**Dato:** 2026-05-31

---

## Sammendrag

Rapporten undersøker om en datadrevet reallokering av eksisterende hyllekapasitet kan gi kvantifiserbar forbedring i forventet salg innen én varekategori hos en Coop Extra-butikk. Basert på ti uker med ukentlige salgsdata (uke 06–15, 2026) for åtte SKUer og totalt 486 frontfacings, dokumenterer studien en tydelig mismatch mellom hylleplan og etterspørsel: to A-klasseprodukter dekker 64 % av salget men disponerer bare 17 % av hyllen, mens fire overkapasiterte produkter har vedvarende lav utnyttelse. En deterministisk lineær programmeringsmodell (LP) implementert i Python med PuLP omfordeler facings innenfor faste totalrammer for å maksimere forventet ukesalg. Modellen kjøres i tre scenarier som spenner fra uregulert optimum til konservativ praksis. Hovedanbefalingen — som beholder alle åtte SKUer med et minimum på 25 % av dagens allokering — gir +61 % forventet ukesalg sammenlignet med observert baseline. En sensitivitetsanalyse viser at gevinsten er robust: selv med en konservativ antakelse om skjult etterspørsel (1,25× i stedet for 2,0×) gir modellen fortsatt +16 %. Resultatet er operasjonelt meningsfullt siden omfordelingen skjer uten investeringskostnad, men må implementeres gradvis med måling av faktisk salg for å empirisk forankre den space-elastisiteten modellen i dag må anta lineær.

**Nøkkelord:** hylleallokering, space management, lineær programmering, retail, dagligvare, datadrevet beslutningsstøtte.

---

## Abstract

This report investigates whether a data-driven reallocation of existing shelf capacity can yield a quantifiable improvement in expected sales within a single product category at a Coop Extra grocery store. Using ten weeks of weekly sales data (weeks 06–15, 2026) for eight SKUs and 486 total frontfacings, the study documents a clear mismatch between planogram and demand: two A-class products account for 64 % of sales but hold only 17 % of shelf space, while four over-capacitated products display consistently low utilization. A deterministic linear programming model (LP) implemented in Python with PuLP reallocates frontfacings within fixed total capacity to maximize expected weekly sales. The model is solved under three scenarios spanning from unconstrained optimum to conservative practice. The main recommendation — which preserves all eight SKUs with a floor of 25 % of current allocation — yields +61 % expected weekly sales versus the observed baseline. A sensitivity analysis shows the result is robust: even under a conservative hidden-demand assumption (1.25× rather than 2.0×) the model still delivers +16 %. The finding is operationally meaningful because the reallocation requires no capital investment, but should be phased in with measurement of realized sales to empirically ground the linear space-elasticity assumption the model currently relies on.

**Keywords:** shelf allocation, space management, linear programming, retail, grocery, data-driven decision support.

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

Hylleplass er en av de mest knappe og verdifulle ressursene i dagligvarehandelen. Hver butikk disponerer en gitt mengde frontfacings som skal fordeles mellom et stort antall SKUer, og fordelingen — planogrammet — har direkte innvirkning på hvilke produkter kundene møter og hvor ofte de går tom. I en bransje med lave marginer representerer riktig utnyttelse av hylleplass en av de få kostnadsfrie spakene for å løfte omsetning: investeringen er alt gjort; det som gjenstår er å plassere de tilgjengelige facings der etterspørselen faktisk er.

Til tross for at kategorien er velstudert i operasjonsforskningen, viser bransjeobservasjoner at planogrammer ofte er historisk betingede og sjelden re-optimaliseres mot aktuelle salgsdata. Dette etterlater et gap mellom *hylleplanen* (hva planogrammet sier) og *etterspørselen* (hva kundene faktisk kjøper). I butikker der dette gapet er stort, vil reallokering av eksisterende plass — uten investering — kunne gi målbar gevinst.

Dette prosjektet undersøker hvor stort dette gapet er i en konkret kontekst, og hvilket forbedringspotensial en datadrevet reallokering kan gi.

### 1.1 Problemstilling

*Hvordan kan en datadrevet tilnærming identifisere produkter som er underallokert i hylleplass relativt til observerte salgsdata, og hva er det estimerte potensialet for forbedring ved reallokering av eksisterende hyllekapasitet innen en avgrenset varekategori i Coop Extra X?*

### 1.2 Avgrensinger

- **Én butikk.** Analysen er gjort i én bestemt Coop Extra-enhet og representerer denne butikkens salg og hylleplan i observasjonsperioden.
- **Én varekategori.** Kullsyreholdige leskedrikker i plastflasker (0.5 L, 1.5 L) samt én boks-variant. 8 SKUer totalt.
- **Ti uker.** Uke 06 til og med uke 15 i 2026. Perioden dekker sen vinter og tidlig vår og inkluderer ingen dokumenterte ekstreme hendelser (jul, påske, langvarig kampanje).
- **Eksisterende hyllekapasitet.** Analysen ser utelukkende på reallokering innenfor dagens fysiske ramme på 486 frontfacings. Utvidelse av hyllen eller endring av sortimentssammensetningen ligger utenfor omfanget.
- **Ingen økonomisk vekting.** Gevinsten måles i antall solgte enheter per uke, ikke i omsetning eller dekningsbidrag. Margintall er ikke tilgjengelige i datasettet.
- **Kvantitativ, ikke kvalitativ.** Prosjektet gjør ingen intervjuer, kundeobservasjoner eller leverandørsamtaler. Alle tolkninger er basert på observerte salgs- og kapasitetsdata.

### 1.3 Antagelser

Analysen hviler på fire hovedantagelser som drøftes kritisk i §8:

1. **Observert ukesalg er representativt for den aktuelle periodens etterspørsel** for produkter som ikke går tomme. For produkter med utnyttelsesgrad ≥ 1 (hyllen tømmes før neste etterfylling) er observert salg et *nedre* anslag for reell etterspørsel.
2. **Hvert ekstra frontfacing gir samme produktivitet (lineær space-elastisitet).** Reell elastisitet er sannsynligvis avtakende, noe som gjør modellens gevinstanslag til et øvre estimat.
3. **Kjedens minstekrav til frontfacings per produkt er enten 1 eller en fast andel av dagens allokering (25 % i hovedscenariet, 50 % i det konservative).** Eksplisitte avtaler om minsteallokering per SKU er ikke tilgjengelige.
4. **Ingen kryssalgseffekter eller kannibalisering.** Modellen behandler hvert produkt uavhengig. Mulige interaksjoner diskuteres i §8.

---

---

## 2 Litteratur

Litteraturen som støtter opp om dette prosjektet dekker tre sammenkoblede felt: (i) optimaliseringsmodeller for hylleplass (*shelf space allocation problem*, SSAP) innen operasjonsforskning, (ii) etterspørselsprognoser og out-of-stock-problematikk i dagligvare, og (iii) nyere anvendelser av kunstig intelligens og maskinsyn i retail space management. Søkeord og fullstendig kildeliste er dokumentert i prosjektplanen.

### 2.1 SSAP — operasjonsforskningstradisjonen

Det formelle SSAP ble etablert som et lineær- og heltallsprogrammeringsproblem på 1970-tallet (Curhan, 1972) og er siden videreutviklet for å håndtere heterogene hyllestørrelser, stokastisk etterspørsel, sortimentsbeslutninger og tverrsortiments-effekter. Bouzembrak m.fl. (2025) gir den ferskeste oversikten over feltet og plasserer de ulike modellfamiliene i forhold til hverandre; deres syntese brukes som strukturelt rammeverk for dette litteraturkapitlet.

Düsterhöft, Hübner & Schaal (2021) presenterer en eksakt optimaliseringsformulering med dekomponeringsheuristikk som håndterer realistiske hyllekonfigurasjoner. Deres formulering ligner modellen som anvendes her (§6), men er utvidet til å inkludere flere hyller og kryss-elastisiteter. Hübner, Schäfer & Schaal (2020) går videre og integrerer sortiments- og hylleplassvalg med stokastisk etterspørsel og eksplisitt space-elastisitet. Sammenlignet med disse er modellen i dette prosjektet bevisst forenklet — deterministisk, én hylle, lineær produktivitet — for å være reproduserbar med det begrensede datasettet vi disponerer.

Mishra (2023) går den heuristiske veien og foreslår seks enkle allokeringsregler (proporsjonal til salg, proporsjonal til margin, ABC-basert osv.). Disse er ikke optimalitetsgarantert men lette å forklare til praktikere. Vår LP-tilnærming kan betraktes som et steg opp i kompleksitet sammenlignet med disse heuristikkene, men et steg ned sammenlignet med Düsterhöft m.fl. og Hübner m.fl.

### 2.2 Etterspørsel og out-of-stock

Gholami & Bhakoo (2025) dokumenterer hvor store stockout-problemene kan være i praksis og viser at maskinlæringsbasert prediksjon reduserer problemet betydelig. Deres empiri (1.6M+ SKUer fra en stor retailer) bekrefter at utnyttelsesgrad rundt eller over 1 ikke er uvanlig for A-produkter og representerer en reell tapt omsetning. Dette er premisset for etterspørselsantakelsen (overserve_factor > 1) vi bruker i §6.

Gustriansyah m.fl. (2022) sammenligner prognose-modeller for salgsdata og finner at hybride maskinlæringsmodeller (kombinasjoner av XGBoost, Random Forest og lineær regresjon) overgår enkeltmodeller. For dette prosjektet — med kun ti uker data per produkt — er avansert prognose ikke meningsfullt; vi bruker periodegjennomsnitt som punktestimat. Men litteraturen peker på en naturlig utvidelse: erstatte det statiske $\bar s_i$ med en prognose når flere datapunkter er tilgjengelige.

Usama m.fl. (2024) rapporterer konkrete effekttall fra AI-basert etterspørselsprognose i dagligvare — 23,7 % bedre prognose og 24,3 % færre stockouts — og gir dermed et grovt sammenligningsgrunnlag for omfanget av forbedringer som er oppnåelige med datadrevne tilnærminger i sektoren.

### 2.3 AI og automatisert planogramovervåking

Klement & Hübner (2023) gir et helhetlig rammeverk som kobler sortimentsvalg, hylleallokering og påfylling som tre samhørige beslutningslag. Rammeverket er nyttig for å plassere dette prosjektet — som opererer rent på hylleallokerings-laget — innenfor en større beslutningsarkitektur. Det underbygger også §8-diskusjonen om fasering: hvis påfyllingen ikke henger med, kan selv en optimal allokering føre til mer out-of-stock.

Santos m.fl. (2024) og Hsu m.fl. (2025) beskriver henholdsvis deep learning- og computer vision-systemer for automatisert planogramovervåking i hele butikkjeder. Disse arbeidene representerer fremtiden for datainnhenting i feltet: istedenfor statiske planogrammer rapportert fra kjedekontor, får man sanntidsvisninger av hvordan hyllen faktisk ser ut. For dette prosjektet gir dette en metodisk forventning: den typen analyse vi gjør her, vil om noen år kunne kjøres på kontinuerlig oppdaterte data snarere enn tiukers eksport.

### 2.4 Syntese mot problemstilling

Litteraturen understøtter tre premisser som problemstillingen hviler på: (1) mismatch mellom hyllekapasitet og etterspørsel er et veldokumentert fenomen i dagligvare; (2) LP-baserte modeller er anerkjent som et adekvat verktøy for å adressere det; (3) gevinstanslagene på 20–60 % som rapporteres i den nyere empiriske litteraturen er i størrelsesorden sammenlignbare med dem prosjektets egne resultater peker på. Samtidig viser metastudiene (særlig Bouzembrak m.fl., 2025) at de mest sofistikerte modellene krever data — kryss-elastisitet, margin per enhet, flerukers variasjon — som i praksis sjelden er tilgjengelig for et avgrenset studentprosjekt. Dette legitimerer vårt valg av en enklere, men fullstendig dokumentert og reproduserbar LP-tilnærming.

---

## 3 Teori

Teorikapitlet etablerer de tre byggesteinene som modellen og analysen hviler på: (i) begrepet *space elasticity* som beskriver forholdet mellom hylleplass og salg, (ii) lineær programmering som optimaliseringsverktøy, og (iii) ABC-klassifisering som struktureringsprinsipp for sortimenter med ulik kommersiell betydning.

### 3.1 Space elasticity

*Space elasticity* (hylleelastisitet) er den marginale endringen i salg som følger av en endring i antall frontfacings. Begrepet ble tidlig formalisert av Curhan (1972) som en produktspesifikk elastisitetskoeffisient $\beta_i$, slik at salg per uke tilnærmet følger en potensfunksjon:

$$
s_i(x_i) = \alpha_i \cdot x_i^{\beta_i}, \quad \beta_i \in (0, 1]
$$

der $\alpha_i$ er en skaleringsfaktor og $\beta_i < 1$ uttrykker *avtakende* marginalavkastning — den tiende facing gir mindre inkrementelt salg enn den første. Empiriske estimater av $\beta_i$ varierer typisk mellom 0,1 og 0,3 i den eldre litteraturen, men nyere funn (Hübner, Schäfer & Schaal, 2020) antyder at elastisiteten kan være tilnærmet lineær ($\beta_i \approx 1$) for produkter som i utgangspunktet er kraftig underdimensjonerte, og tilnærmet null for produkter som allerede mettet etterspørselen.

For den LP-modellen som brukes i dette prosjektet (§6) forenkles space elasticity til en *lineær* produktivitetsfunksjon:

$$
s_i(x_i) = \rho_i \cdot x_i
$$

opp til et etterspørselstak $d_i$. Dette tilsvarer å anta $\beta_i = 1$ i Curhan-formuleringen, som er en *øvre grense* for elastisiteten og dermed et *optimistisk* scenario i gevinstanslag. Valget er begrunnet i mangelen på data som kan estimere $\beta_i$ empirisk (ti uker uten kapasitetsvariasjon gir ingen identifikasjon av elastisitetskurven). Konsekvensene drøftes i §8.2.

### 3.2 Lineær programmering som optimaliseringsverktøy

Lineær programmering (LP) løser problemer på formen

$$
\max \; \mathbf{c}^\top \mathbf{z} \quad \text{under} \quad \mathbf{A}\mathbf{z} \le \mathbf{b}, \quad \mathbf{z} \ge \mathbf{0}
$$

der målfunksjonen og alle restriksjoner er lineære i beslutningsvariablene. Simplex-algoritmen (Dantzig, 1947) og senere interior-point-metoder løser slike problemer effektivt opp til store dimensjoner. Når heltalls-restriksjoner pålegges (som her: frontfacings må være heltall), får man *heltalls lineær programmering* (ILP), som generelt er NP-hardt men i praksis håndterlig for små dimensjoner med branch-and-bound-solvere som CBC.

Tre egenskaper gjør LP/ILP særlig egnet for hylleallokeringsproblemet i denne studien:

1. **Garantert globalt optimum** for den formulerte målfunksjonen under gitte restriksjoner — i motsetning til heuristikker som gir "gode nok" løsninger uten optimalitetsgaranti.
2. **Transparent og tolkbar struktur.** Hver restriksjon kan relateres til en forretningsregel (total kapasitet, minimumsallokering, etterspørselsgrense), og dualvariable kan tolkes som skyggepriser.
3. **Naturlig utgangspunkt for sensitivitetsanalyse.** Endring av én parameter og ny løsning viser direkte hvordan optimum avhenger av antakelsene.

Begrensningene er omvendte: LP kan ikke uttrykke ikke-lineære sammenhenger (som Curhans potens-elastisitet med $\beta_i < 1$) uten linearisering eller stykkvis-lineær tilnærming, og den deterministiske formuleringen håndterer ikke stokastikk direkte.

### 3.3 Demand–capacity mismatch og out-of-stock

*Out-of-stock* (OOS) oppstår når hyllen tømmes før neste etterfylling. For en vare med utnyttelsesgrad $u_i = \bar s_i / c_i > 1$ (gjennomsnittlig ukesalg overstiger hyllekapasitet) er OOS forventet å forekomme i perioder av uken. Konsekvensen er *tapt salg*: kunder som kommer i butikken mens hyllen er tom kjøper enten et substitutt eller handler ikke den kategorien.

Gholami & Bhakoo (2025) dokumenterer at den faktiske etterspørselen for OOS-rammede produkter kan være 1,5 til 3 ganger observert salg, avhengig av etterfyllingshyppighet og kundeatferd. Dette tallet er opprinnelsen til prosjektets `overserve_factor`-parameter (§6.4): for produkter med $u_i \ge 1$ antas den sanne etterspørselen å være en multippel av observert salg. I sensitivitetsanalysen (§7.3) undersøker vi hvor mye modellens anbefaling avhenger av denne multiplikatoren.

Motstykket til OOS er *overkapasitet*: et produkt med $u_i < 1$ beslaglegger facings som aldri blir fylt før de etterfylles. Dette er "død hylle" som kunne vært omplassert til et produkt med høyere produktivitet per facing. Prosjektets utgangshypotese er at *begge fenomenene opptrer samtidig* i den observerte kategorien, og at reallokering fra overkapasiterte til underkapasiterte SKUer derfor gir netto gevinst.

### 3.4 ABC-klassifisering og Pareto-prinsippet

ABC-klassifisering er en praktisk anvendelse av Pareto-prinsippet (Pareto, 1896; videreført av Koch, 1997) på sortimentsstyring. Produkter sorteres etter deres bidrag til en valgt nøkkelindikator — her totalsalg i enheter — og deles inn i tre klasser basert på kumulativ andel:

- **A-produkter:** topp ≈ 80 % av kumulativt salg; typisk få SKUer
- **B-produkter:** neste ≈ 15 %
- **C-produkter:** de siste ≈ 5 %; typisk mange SKUer

Klassifiseringen brukes i praksis til å differensiere styringsregimer (hyppigere varetelling for A-produkter, bestemme hvilke produkter som fortjener egne kampanjer, osv.). I denne analysen brukes den tosidig: som struktureringsprinsipp for hvilke produkter som er de mest aktuelle kandidatene for mer hylleplass (A-klassen), og som grunnlag for pseudonymiseringen av produktnavn (§5.2) slik at rapporten kan leses uten å vite hvilke konkrete merkevarer som er involvert.

### 3.5 Sammenkobling — fra teori til modell

Sammen gir de fire teoretiske byggesteinene følgende operative narrativ: Hvis en butikk har et sortiment med både overkapasiterte og underkapasiterte SKUer (§3.3), og vi antar at hvert facing gir et målbart salgsbidrag (§3.1), så kan vi formulere et lineært optimeringsproblem (§3.2) som omfordeler den faste hyllekapasiteten slik at total forventet salg maksimeres, hvor ABC-klassifiseringen (§3.4) gir en naturlig førsteintuisjon om hvilke produkter som bør få mer plass. Dette er nettopp det modellen i §6 gjør, og resultatene i §7 evaluerer.

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

Prosjektet følger en *kvantitativ case-studie* som forskningsdesign: én avgrenset varekategori i én dagligvarebutikk undersøkes dybdemessig ved hjelp av numerisk modellering av empiriske salgsdata. Valget av case-studie er begrunnet i problemstillingens karakter — vi ønsker å undersøke om datadrevet reallokering av hylleplass gir kvantifiserbar effekt i en konkret driftssammenheng, ikke å etablere allmenngyldige sammenhenger. Den kvantitative metoden kommer inn ved at analysen er numerisk, deterministisk og reproduserbar.

**Metodisk struktur.** Analysen gjennomføres i fire sekvensielle trinn som også gjenspeiles i rapportstrukturen:

1. **Deskriptiv analyse (§7.1, §5.2):** produktvise nøkkeltall (gjennomsnitt, standardavvik, variasjonskoeffisient, min/maks) samt utnyttelsesgrad (salg / hyllekapasitet). Dette gir et kvantitativt bilde av *mismatchen* som problemstillingen spør om.
2. **ABC-klassifisering:** Pareto-fordeling av totalsalget identifiserer hvilke produkter som står for 80 %, 95 % og 100 % av omsetningen. Klassifiseringen brukes både analytisk og som grunnlag for pseudonymiseringen (§5.2).
3. **Optimaliseringsmodell (§6):** en deterministisk lineær programmeringsmodell (LP) formuleres og løses for å finne den omfordeling av eksisterende hylleplass som maksimerer forventet ukentlig salg innenfor minimums-sortimentsgaranti.
4. **Sensitivitetsanalyse (§7.3):** LP-en kjøres over et rutenett av verdier for de to mest usikre parameterne (etterspørselsantakelsen `overserve_factor` og minimums-andel `x_min_fraction`) for å undersøke hvor robust resultatet er mot modellantagelser.

**Valg av LP som optimaliseringsmetode.** Hylleallokering er et klassisk *space management*-problem i Operations Research og kan angripes med flere metodiske tilnærminger: heuristikker (f.eks. proporsjonal til salg), simulering, blandet-heltalls programmering (MILP) eller — som her — lineær programmering med heltallskrav på facings-variablene. LP er valgt fordi (i) problemstørrelsen (8 produkter, 486 facings) er håndterbar, (ii) modellen er deterministisk på en periode noe som forenkler tolkningen, (iii) løsningen gir et klart optimum mot en veldefinert målfunksjon, og (iv) sensitivitetsanalysen er rett frem for en LP. Alternative tilnærminger — stokastisk programmering, simulering med flere perioder, eller dynamisk allokering — ville krevd rikere data enn de ti ukene vi disponerer.

**Datainnsamling.** Datagrunnlaget er sekundærdata hentet fra butikkens kassesystem (ukentlig salg per SKU) og gjeldende planogram (antall frontfacings per SKU). Se §5.2 for detaljer om omfang, kvalitet og behandling. Data ble mottatt fra butikkens driftsansvarlige etter signert taushetserklæring og oppbevares lokalt i prosjektets arbeidsrepository utenfor offentlig versjonskontroll.

**Implementering og reproduserbarhet.** All analyse er implementert i Python 3.12. Modellene bruker biblioteket PuLP med CBC-solver for lineær programmering, og pandas for datamanipulasjon. Kode og genererte figurer/tabeller versjoneres i prosjektets Git-repository; pseudonymiserte versjoner av resultatene inngår i repoet, mens filer med ekte produktnavn holdes lokalt i en `intern/`-underfolder som er ekskludert fra versjonering. Hele kjøringen (datarensing → deskriptiv analyse → LP → sensitivitet) kan reproduseres med tre kommandoer slik det dokumenteres i `006 analysis/README.md`. Anonymiseringsmodulen `anonymisering.py` sikrer at produkter i alle genererte artefakter har samme pseudonymer på tvers av scripts.

**Kvalitetssikring.** Intern kvalitetssikring skjer i henhold til prosjektplanen: hver analyse-artefakt genereres deterministisk fra rådata og sanity-sjekkes mot intuisjon (f.eks. at ABC-summen blir 100 %, at LP-status er "Optimal", og at summen av allokerte facings tilsvarer total kapasitet). Peer-to-peer review planlegges i henhold til slagplanen for fase 3. Formelle akademiske krav følger SKRIVING-kompendiet (Kap. 3), herunder APA 7-referansestil for bibliografien i §10.

**Etiske hensyn.** Studien behandler ikke personopplysninger og faller utenfor personopplysningsloven og helseforskningsloven (se egenerklæringen foran i rapporten). Konfidensialitet overfor Coop Extra X er ivaretatt gjennom taushetserklæring og pseudonymisering av produktnavn i alle offentlig tilgjengelige artefakter.

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

**B4. Én butikk, 10 uker.** Datasettet omfatter én fysisk butikk og en periode på ti uker (uke 06–15 2026). Sesongvariasjoner, kampanjeuker eller eksterne hendelser kan ha påvirket datagrunnlaget uten at vi kan korrigere for det. Spesielt A2-observasjonen i uke 15 (412 enheter, mer enn dobbelt av gjennomsnittet for produktet) ble ikke fjernet som avviker fordi vi ikke har grunnlag for å hevde at den er en målefeil — det er sannsynligvis en kampanjeuke eller en uventet etterspørselspulje. En replikasjon på flere butikker og over lengre periode ville styrket grunnlaget for generalisering.

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

Problemstillingen spurte hvordan en datadrevet tilnærming kan identifisere produkter som er underallokert i hylleplass relativt til observerte salgsdata, og hva det estimerte potensialet for forbedring ved reallokering av eksisterende hyllekapasitet er innen en avgrenset varekategori i Coop Extra X.

Svaret, basert på ti uker ukentlige salgsdata for åtte SKUer i en gitt kategori, er:

- **Underallokeringen er identifiserbar gjennom et enkelt utnyttelsesmål** (gjennomsnittlig ukesalg dividert på antall frontfacings). To produkter (A1, A2) har utnyttelsesgrad 6,6× og 9,1× og er dermed tydelig underkapasiterte; fire produkter har utnyttelse under 0,9 og er overkapasiterte. Samme mål kombinert med en ABC-klassifisering avgrenser hvilke SKUer som er de mest relevante kandidatene for reallokering oppover.
- **Forbedringspotensialet er substansielt.** En deterministisk LP-modell som omfordeler de 486 frontfacings innen kategorien gir mellom +31 % og +63 % i forventet ukesalg, avhengig av antagelser om skjult etterspørsel og minimums-sortimentsgaranti. Hovedanbefalingen (S2 Realistisk) ligger på +61 % med intakt sortiment og et gulv på 25 % av dagens allokering for hvert produkt.
- **Gevinsten er robust.** Sensitivitetsanalysen viser at selv ved konservative antagelser (1,25× etterspørsel i stedet for 2× for underkapasiterte produkter) er LP-salget 16 % over observert baseline. Resultatet er også nærmest flatt mot minimums-sortimentsparameteren opp til 0,40, slik at modellen gir operasjonelt spillerom uten vesentlig gevinstap.

**Praktiske implikasjoner.** Siden omfordelingen skjer innenfor eksisterende hyllekapasitet kommer gevinsten uten investeringskostnad. Hovedanbefalingen forutsetter imidlertid en betydelig nedskalering av én konvensjonelt høy-allokert B-vare og bør derfor fases inn gradvis, med måling av faktisk salg etter omleggingen. Dette gir også grunnlag for å empirisk estimere den space-elastisiteten modellen i dag må anta lineær.

**Forslag til videre forskning.** Tre naturlige utvidelser er identifisert: (i) *stokastisk reformulering* som eksplisitt håndterer variasjon i ukesalg og gir service-level-garantier i stedet for harde kapasitetsgrenser; (ii) *økonomisk vekting* der målfunksjonen maksimerer dekningsbidrag fremfor enheter, betinget av at marginoppgaver kan innhentes fra kjeden; (iii) *empirisk estimering av space-elastisitet* gjennom et kontrollert forsøk med variert facings-allokering over flere uker for et utvalg produkter. Replikasjon på tvers av butikker og kategorier vil også styrke grunnlaget for generalisering.

Studien demonstrerer at en konseptuelt enkel LP-modell, matet med to typer data som butikkjeder allerede besitter (ukesalg og planogram), er tilstrekkelig for å identifisere kvantifiserbare omfordelingspotensialer. Modellens verdi ligger ikke i presisjonen av det estimerte prosentløftet, men i at den gjør det gjeldende planogrammet målbart mot en datadrevet referanse.

---

## 10 Bibliografi

*Referansestil: APA 7. Alle DOI-er og tidsskriftsnavn er basert på prosjektgruppens litteratursøk og bør verifiseres mot primærkilde før innlevering.*

Bouzembrak, Y., m.fl. (2025). Literature review on shelf space allocation in retailing. *RAIRO — Operations Research*.

Curhan, R. C. (1972). The relationship between shelf space and unit sales in supermarkets. *Journal of Marketing Research*, *9*(4), 406–412.

Dantzig, G. B. (1947). *Maximization of a linear function of variables subject to linear inequalities*. I T. C. Koopmans (Red.), *Activity Analysis of Production and Allocation* (ss. 339–347). Wiley.

Düsterhöft, T., Hübner, A., & Schaal, K. (2021). Exact optimization and decomposition approaches for shelf space allocation. *European Journal of Operational Research*.

Gholami, M., & Bhakoo, V. (2025). A machine learning approach to inventory stockout prediction. *Supply Chain Analytics*.

Gustriansyah, R., m.fl. (2022). A comparative study of demand forecasting models. *Mathematics*, *10*(19).

Hsu, Y.-H., m.fl. (2025). Real-time retail planogram compliance using computer vision. *Scientific Reports*.

Hübner, A., Schäfer, F., & Schaal, K. (2020). Maximizing profit via assortment and shelf-space optimization for two-dimensional shelves. *Production and Operations Management*.

Klement, N., & Hübner, A. (2023). Decision support for managing assortments, shelf space, and replenishment in retail. *Flexible Services and Manufacturing Journal*.

Koch, R. (1997). *The 80/20 principle: The secret to achieving more with less*. Nicholas Brealey.

Mishra, A. (2023). Heuristics for the shelf space allocation problem. *OPSEARCH*.

Pareto, V. (1896). *Cours d'économie politique*. F. Rouge.

Santos, F., m.fl. (2024). Shelf management: A deep learning-based system for shelf visual monitoring. *Expert Systems with Applications*.

Usama, M., m.fl. (2024). AI-driven demand forecasting: Enhancing inventory management. *World Journal of Advanced Research and Reviews*.

---

## 11 Vedlegg

**Vedlegg A — Python-kode.** Analysekode er versjonert i prosjektets Git-repository under `006 analysis/`. Kjøringen består av fire scripts som produserer alle tabeller og figurer i denne rapporten:

- `aktiviteter/3_3_casebeskrivelse_og_datainnsamling/scripts/01_datarensing.py`
- `aktiviteter/3_4_data_metode_og_modellering/scripts/02_deskriptiv_og_abc.py`
- `aktiviteter/3_4_data_metode_og_modellering/scripts/03_lp_modell.py`
- `aktiviteter/3_5_analyse_og_resultater/scripts/04_sensitivitet.py`

Avhengigheter er definert i `006 analysis/pyproject.toml`. Hele pipelinen reproduseres med `uv sync` etterfulgt av de fire kommandolinjene dokumentert i `006 analysis/README.md`.

**Vedlegg B — Pseudonymregister.** Koblingen mellom pseudonymer (A1, A2, B1, B2, C1–C4) og reelle produktnavn er oppbevart lokalt i `006 analysis/aktiviteter/3_3_casebeskrivelse_og_datainnsamling/resultat/intern/navneregister.csv`. Denne filen er unntatt versjonering og deles ikke utenfor prosjektgruppen, i henhold til taushetserklæringen med Coop Extra X.

**Vedlegg C — Taushetserklæring.** Underskrevet taushetserklæring mellom prosjektgruppen og Coop Extra X er arkivert utenfor dette repoet i henhold til kjedens instruks. Mal er tilgjengelig i `000 templates/Taushetsærklæring.docx`.

**Vedlegg D — Rådata.** Rådata som ligger til grunn for analysen, `Data 10 uker.csv`, oppbevares lokalt i `004 data/` og er unntatt versjonering. Alle avledede datasett med reelle produktnavn oppbevares tilsvarende under `intern/`-underfoldere som er ekskludert i `.gitignore`.

