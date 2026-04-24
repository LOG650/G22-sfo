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

Rapporten undersøker hvordan en dagligvareleverandør kan bruke ukentlige sell-out-data fra en kjede-butikk som beslutningsstøtte i forhandlinger om hylleplass, og kvantifiserer reallokeringsgevinsten som kan dokumenteres overfor kjeden innen leverandørens egen portefølje hos Coop Extra X. Perspektivet er leverandørens; data på konkurrerende produkter inngår ikke, hvilket speiler den informasjons­asymmetri som kjennetegner reelle leverandør-kjede-forhandlinger. Basert på ukentlige sell-out-data for leverandørens SKUer over ti uker (uke 06–15, 2026), formuleres en deterministisk lineær programmerings­modell (LP) implementert i Python med PuLP. Modellen omfordeler den kontraktuelle hylleallokeringen leverandøren har hos butikken slik at forventet samlet sell-out maksimeres, under forutsetning av produktspesifikke minimums­gulv som reflekterer sortimentsgarantier. Analysen avdekker en tydelig mismatch mellom hyllefordeling og etterspørsel: to A-klasse­produkter står for 64 % av salget men har bare 17 % av porteføljens hylleplass, mens fire overkapasiterte produkter har vedvarende lav utnyttelse. Modellen kjøres i tre scenarier som spenner fra uregulert optimum til konservativ praksis. Hovedanbefalingen — som beholder alle porteføljens SKUer med et gulv på 25 % av dagens allokering — gir +61 % forventet ukentlig sell-out innen porteføljen sammenlignet med observert baseline. En sensitivitetsanalyse viser at gevinsten er robust mot de sentrale parameterantakelsene. Resultatet er operasjonelt meningsfullt i en forhandlings­kontekst siden det dokumenterer et kvantifisert reallokerings­potensial innen leverandørens egen portefølje — et utgangspunkt for kategoridialog med kjeden som krever verken investering eller utvidelse av leverandørens totale hylleallokering.

**Nøkkelord:** hylleallokering, space management, lineær programmering, retail, dagligvare, datadrevet beslutningsstøtte.

---

## Abstract

This report examines how a grocery supplier can use weekly sell-out data from a chain store as decision support in shelf-space negotiations, and quantifies the reallocation gain that can be documented towards the chain within the supplier's own portfolio at a Coop Extra store. The perspective is the supplier's; competing products are not included in the dataset — mirroring the information asymmetry typical of real supplier–retailer negotiations. Using ten weeks of weekly sell-out data for the supplier's SKUs (weeks 06–15, 2026), a deterministic linear programming model (LP) implemented in Python with PuLP reallocates the shelf allocation the supplier holds at the store to maximize expected total sell-out, subject to minimum-floor constraints reflecting assortment commitments. The analysis surfaces a clear mismatch between shelf and demand: two A-class products account for 64 % of sales but hold only 17 % of the portfolio's shelf units, while four over-capacitated products show persistently low utilization. The model is solved under three scenarios ranging from an unconstrained optimum to conservative practice. The main recommendation — which preserves all portfolio SKUs with a floor of 25 % of current allocation — yields +61 % expected weekly sell-out within the portfolio compared to the observed baseline. A sensitivity analysis shows the result is robust to the key parameter assumptions. The finding is operationally meaningful in a negotiation context because it documents a quantified reallocation potential within the supplier's own portfolio — a starting point for category dialogue with the chain that requires neither capital investment nor expansion of the supplier's total shelf allocation.

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

Hylleplass i dagligvarebutikken er en knapp ressurs og en kontraktuell størrelse. Leverandørens andel av kjedens hylleplass er resultat av forhandlinger som gjennomføres i kategoribesøk og Joint Business Planning (JBP)-møter, der leverandøren argumenterer for at deres SKU-portefølje fortjener en gitt kontraktuell allokering. I disse møtene brukes rutinemessig salgs- og lagerdata som underlag, men **kvantifiserte reallokerings­forslag innen leverandørens egen portefølje** baseres ofte på erfaringsbasert skjønn snarere enn eksplisitt matematisk modellering. Dette prosjektet utvikler en enkel, reproduserbar modell for nettopp dette — et beslutningsstøtte­verktøy en leverandør kan bruke for å gå inn i hylledialogen med kjeden med en tallfestet argumentasjon.

Motivasjonen er konkret: en leverandør har innsyn i egne SKUers **sell-out** (faktisk registrert kundekjøp i kassen, per butikk og uke), men ikke i konkurrentenes tilsvarende tall. Leverandøren har kontraktuell kjennskap til egen hyllekapasitet hos kjeden, men ikke detaljerte planogram­data for øvrige merkevarer. Denne informasjons­asymmetrien er den naturlige skoperings­grensen for analyser av leverandørens type: modellen som bygges må kunne gi verdi basert på *den data leverandøren realistisk disponerer*.

Forskjellen mellom leverandørens hylleplan og det faktiske salget — *mismatchen* mellom hvor kunden kjøper og hvor leverandøren har fått plass — er det sentrale fenomenet som modellen skal kvantifisere og argumentere for å korrigere.

### 1.1 Problemstilling

*Hvordan kan en dagligvareleverandør bruke ukentlige sell-out-data fra en kjede-butikk som beslutningsstøtte i forhandlinger om hylleplass, og hvilket salgspotensial kan dokumenteres ved reallokering innenfor leverandørens egen portefølje hos Coop Extra X?*

### 1.2 Avgrensinger

- **Én butikk.** Analysen er gjort på sell-out-data fra én konkret Coop Extra-enhet og representerer denne butikkens situasjon i observasjonsperioden.
- **Én leverandørs portefølje, ikke hele kategorien.** Datasettet dekker SKUer som distribueres av den aktuelle leverandøren hos butikken. Andre leverandørers produkter i samme kategori inngår ikke, hvilket speiler det realistiske informasjons­bildet leverandøren selv har tilgang til.
- **Ti uker.** Uke 06 til og med uke 15 i 2026. Perioden dekker sen vinter og tidlig vår og inkluderer ingen dokumenterte ekstreme hendelser (jul, påske, langvarig kampanje).
- **Kontraktuell hyllekapasitet som fast ramme.** Analysen omfordeler innenfor leverandørens nåværende samlede hylleallokering hos butikken. Forhandling om *utvidelse* av leverandørens totalallokering er et separat — og mer krevende — argumentasjons­løp som ligger utenfor omfanget.
- **Ingen økonomisk vekting.** Salgspotensialet måles i antall solgte enheter per uke, ikke i omsetning eller dekningsbidrag. Margintall og priser er ikke inkludert i det tilgjengelige datasettet.
- **Kvantitativ, ikke kvalitativ.** Prosjektet gjør ingen intervjuer med kategori­ansvarlige, butikk­sjefer eller forhandlings­parter. Alle tolkninger er basert på observerte sell-out- og kapasitets­data.

### 1.3 Antagelser

Analysen hviler på fire hovedantagelser som drøftes kritisk i §8:

1. **Observert ukentlig sell-out er representativt for den aktuelle periodens etterspørsel** for produkter som ikke går tomme. For produkter med utnyttelsesgrad ≥ 1 (hyllen tømmes før neste etterfylling) er observert salg et *nedre* anslag for reell etterspørsel.
2. **Hvert ekstra enhet hylleplass gir samme produktivitet (lineær space-elastisitet).** Reell elastisitet er sannsynligvis avtakende, noe som gjør modellens gevinst­anslag til et øvre estimat.
3. **Leverandørens minstekrav til hylleplass per SKU er enten 1 enhet eller en fast andel av dagens allokering (25 % i hovedscenariet, 50 % i det konservative).** Eksplisitte kontraktsgulv per SKU er ikke tilgjengelige i dette prosjektet.
4. **Ingen kryssalgseffekter eller kannibalisering innen porteføljen.** Modellen behandler hvert produkt uavhengig. Mulige interaksjoner diskuteres i §8.

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

### 2.3 Category management og leverandør-kjede-forhandlinger

Utover den rene optimaliseringslitteraturen finnes et omfattende arbeidsfelt rundt *category management* og samarbeidsmønstre mellom kjede og leverandør. Klement & Hübner (2023) påpeker at sortiments-, hylle- og påfyllings­beslutninger i praksis fattes i dialog mellom kategori­ansvarlige hos kjeden og såkalte *category captains* på leverandørsiden — leverandører som får forsterket rolle i å foreslå og begrunne planogram-endringer basert på data de selv eier. Bouzembrak m.fl. (2025) nevner i sin oversikt at modellbaserte forslag i slike forhandlinger typisk er underutnyttet sammenlignet med hva tilgjengelig litteratur muliggjør, og løfter frem beslutningsstøtte for leverandør-sidens posisjonering som et område hvor praksis henger etter teori.

Dette prosjektet plasserer seg tydelig i dette gapet: i stedet for å optimalisere butikkens totale kategorihylle (en kjede-beslutning som krever kryssleverandør-data), optimaliserer det *leverandørens egen portefølje innenfor den kontraktuelle hyllen leverandøren allerede disponerer*. Perspektivet matcher den realistiske informasjons­situasjonen for en leverandør og gir et verktøy som kan brukes i forhandlings- og kategorimøter.

### 2.4 AI og automatisert planogramovervåking

Klement & Hübner (2023) gir et helhetlig rammeverk som kobler sortimentsvalg, hylleallokering og påfylling som tre samhørige beslutningslag. Rammeverket er nyttig for å plassere dette prosjektet — som opererer rent på hylleallokerings-laget — innenfor en større beslutningsarkitektur. Det underbygger også §8-diskusjonen om fasering: hvis påfyllingen ikke henger med, kan selv en optimal allokering føre til mer out-of-stock.

Santos m.fl. (2024) og Hsu m.fl. (2025) beskriver henholdsvis deep learning- og computer vision-systemer for automatisert planogramovervåking i hele butikkjeder. Disse arbeidene representerer fremtiden for datainnhenting i feltet: istedenfor statiske planogrammer rapportert fra kjedekontor, får man sanntidsvisninger av hvordan hyllen faktisk ser ut. For dette prosjektet gir dette en metodisk forventning: den typen analyse vi gjør her, vil om noen år kunne kjøres på kontinuerlig oppdaterte data snarere enn tiukers eksport.

### 2.5 Syntese mot problemstilling

Litteraturen understøtter fire premisser som problemstillingen hviler på: (1) mismatch mellom hyllekapasitet og etterspørsel er et veldokumentert fenomen i dagligvare; (2) LP-baserte modeller er anerkjent som et adekvat verktøy for å adressere det; (3) gevinstanslagene på 20–60 % som rapporteres i den nyere empiriske litteraturen er i størrelses­orden sammenlignbare med dem prosjektets egne resultater peker på; og (4) leverandørens rolle som category captain er et veletablert, men i dette prosjektets bruk­tilfelle underutnyttet, beslutnings­miljø. Samtidig viser metastudiene (særlig Bouzembrak m.fl., 2025) at de mest sofistikerte modellene krever data — kryss-elastisitet, margin per enhet, fleruker­svariasjon — som i praksis sjelden er tilgjengelig for et avgrenset studentprosjekt. Dette legitimerer vårt valg av en enklere, men fullstendig dokumentert og reproduserbar LP-tilnærming anvendt på *den datatypen en leverandør realistisk disponerer*.

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

Case-studien tar utgangspunkt i leverandørens perspektiv. Leverandøren er en stor, global produsent av kullsyreholdige leskedrikker med et bredt porteføljetilbud og en etablert kontraktuell hylleallokering hos Coop-kjeden i Norge. Analyse­enheten er leverandørens portefølje slik den er representert hos én konkret Coop Extra-butikk ("Coop Extra X"). Av hensyn til taushetserklæring inngått mellom prosjektgruppen og butikken/leverandøren er hverken butikkens geografiske lokasjon, leverandørens navn eller faktiske produktnavn gjengitt i rapporten; alle produkter er omtalt med pseudonymer (se §5.2).

### 4.1 Leverandørens portefølje som analyse-enhet

Case-studien ser på leverandørens SKU-portefølje slik den finnes i butikkens sortiment i observasjonsperioden. Porteføljen dekker kullsyreholdige leskedrikker i plastflasker (0.5 L og 1.5 L), energidrikk i boks, og en idrettsdrikk. Konkurrerende merkevarer fra andre leverandører er *ikke* inkludert — verken i sell-out-data eller i kapasitets­oversikten — i tråd med den informasjons­asymmetrien en leverandør realistisk arbeider under.

Porteføljen valg gjenspeiler den datatypen leverandøren disponerer i sin forhandlings­forberedelse: sell-out per uke for egne SKUer, samt nåværende kontraktuell hylleallokering per SKU hos butikken. Det leverandøren *ikke* har innsyn i — konkurrenters salg, konkurrenters hylleplass, kundesegmentering utover kjedens aggregater — er også det modellen ikke forutsetter å kjenne.

### 4.2 Hyllekontrakt og rammebetingelser

Leverandørens *hylle-allokering* hos butikken er et kontraktuelt tall: antall hylleenheter (frontfacings × dybde × antall hyller) fordelt mellom leverandørens SKUer i butikkens planogram. Analyseperioden har holdt denne fordelingen konstant, hvilket betyr at variasjon i salg ikke kan forklares av endringer i hylleplass. Reallokering innenfor leverandørens kontraktuelle ramme krever dialog med butikken/kjeden men vanligvis ikke reforhandling av kontrakten — og representerer derfor en relativt lav-friksjons endring sammenlignet med å argumentere for utvidelse av totalrammen.

**Samlet hylleallokering som leverandøren disponerer hos Coop Extra X i observasjons­perioden: [TBD når nytt datasett er innhentet; pilot-beregninger i §7 er basert på et tidligere utsnitt av porteføljen og skal oppdateres.]**

Etterfylling skjer fra baklager hver dag eller annenhver dag, så observert *salg per uke* er rimelig proxy for *reell etterspørsel* så lenge hyllen ikke går tom. For produkter med utnyttelsesgrad nær eller over 1,0 er tapt salg pga. utsolgt hylle (out-of-stock) en relevant kilde til undervurdert etterspørsel. Dette diskuteres i §8.

### 4.3 Dataeiere og tilgang

Analysen bygger på to datakilder som reflekterer de to partene i den operasjonelle kategorihåndteringen:

1. **Sell-out-data per uke og SKU** — hentet fra butikkens POS-system via butikkens driftsansvarlige, eller alternativt via leverandørens egne sell-out-rapporter fra kjeden. Begge kildene speiler de samme kundetransaksjonene i butikken.
2. **Kontraktuell hylleallokering per SKU** — hentet fra leverandøren basert på gjeldende planogramavtale med Coop.

Data er stilt til rådighet etter signert taushetserklæring mellom prosjektgruppen og den aktuelle leverandøren/butikken (2026-02). Studentene er ikke ansatt eller engasjert av verken Coop eller leverandøren og har ingen øvrig kommersiell relasjon til partene.

---

## 5 Metode og data

### 5.1 Metode

Prosjektet følger en *kvantitativ case-studie* som forskningsdesign: én leverandørs portefølje i én Coop Extra-butikk undersøkes dybdemessig ved hjelp av numerisk modellering av empiriske sell-out-data. Valget av case-studie er begrunnet i problemstillingens karakter — vi ønsker å undersøke om en datadrevet reallokerings­analyse kan fungere som operativ beslutningsstøtte i en leverandør-forhandlings­kontekst, ikke å etablere allmenngyldige sammenhenger. Den kvantitative metoden kommer inn ved at analysen er numerisk, deterministisk og reproduserbar.

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

Datagrunnlaget består av to sammenslåtte kilder: **ukentlig sell-out per SKU** (kundekjøp registrert i butikkens POS-system) og **kontraktuell hylleallokering per SKU** (antall enheter tildelt SKU i leverandørens del av planogrammet). Begge kilder dekker *leverandørens portefølje* hos Coop Extra X i observasjons­perioden; konkurrerende SKUer fra andre leverandører er ikke inkludert, i tråd med scope definert i §1.2.

Pilot-analysen som ligger til grunn for §7 ble gjennomført på et utsnitt av porteføljen (åtte SKUer) før det utvidede datasettet for hele porteføljen var innhentet. Den endelige rapporten vil oppdateres når full porteføljedata foreligger; §7-resultatene er da å forstå som pilot og skal re-kjøres på utvidet datasett før innlevering 31.05.2026.

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

Reallokerings­problemet formuleres som en lineær programmerings­modell (LP) der målet er å fordele leverandørens *kontraktuelle hylleallokering* mellom egne SKUer slik at forventet samlet sell-out maksimeres innenfor produktspesifikke etterspørsels­grenser og sortiments­gulv. Modellen omfordeler utelukkende innen leverandørens portefølje; SKUer fra andre leverandører inngår hverken i målfunksjonen eller i kapasitets­restriksjonen. Formuleringen er deterministisk og periode­gjennomsnittlig: en enkelt «typisk uke» representerer perioden uke 06–15 2026.

### 6.1 Mengder og indekser

| Symbol | Beskrivelse |
|---|---|
| $P$ | Mengde av leverandørens SKUer i butikkens sortiment, $i \in P$. Andre leverandørers SKUer inngår ikke i $P$. Pilot-analysen (§7) bruker $\lvert P \rvert = 8$; full portefølje­analyse oppdateres når utvidet datasett er innhentet. |

### 6.2 Parametere

| Symbol | Enhet | Beskrivelse | Verdi / kilde |
|---|---|---|---|
| $T$ | enheter | Leverandørens samlede kontraktuelle hylleallokering hos butikken, konstant i perioden. Dekker *ikke* kategoriens totale hylleplass. | 486 (pilot) / [TBD full portefølje] |
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

For SKUer med observert utnyttelse under 1,0 legges det til grunn at målt ukentlig sell-out svarer til etterspørselen ($d_i = \bar s_i$). For SKUer der observert sell-out overstiger hylleallokering, er salget begrenset av hylle og ikke av etterspørsel; den sanne etterspørselen er høyere enn observert sell-out men er ikke direkte målbar. I hovedscenariet brukes $d_i = 2\bar s_i$, en antakelse som reflekterer at out-of-stock-situasjoner er observert i flere uker for disse produktene. Alternative verdier prøves i sensitivitetsanalysen (§7.3).

### 6.5 Målfunksjon

Modellen maksimerer total forventet salg per uke:

$$
\max \sum_{i \in P} y_i
$$

### 6.6 Restriksjoner

**R1 — Leverandørens kontraktuelle hylleramme.** Omfordelingen skjer innenfor den hylleallokering leverandøren allerede disponerer, uten netto endring mot resten av kategorien. Leverandøren forhandler altså ikke om mer plass i denne modellen; den reallokerer det som er:

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

Kapitlet presenterer resultatene av LP-modellen fra §6 anvendt på **pilot-datasettet** fra §5.2 — åtte av leverandørens SKUer hvor data var tilgjengelig tidlig i prosjektet. Resultatene skal oppdateres på utvidet portefølje­datasett før endelig innlevering (se §5.2). Analysen er strukturert i tre deler: (i) en sammenligning av tre allokerings­scenarier som spenner fra matematisk optimum til konservativ praksis, (ii) en detaljert gjennomgang av hovedanbefalingen på produktnivå, og (iii) en sensitivitets­analyse av de to viktigste modell­parameterne.

### 7.1 Scenariesammenligning (pilot)

Tre scenarier ble kjørt med samme underliggende LP, men med ulike verdier for etterspørsels­antagelsen i §6.4 og minimums-sortimentet i R4. Tabell 7.1 oppsummerer forutsetninger og resultat. Alle tall gjelder *innen leverandørens pilot-portefølje* (åtte SKUer) og vil oppdateres når utvidet portefølje­datasett er tilgjengelig.

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

### 8.3 Implikasjoner for leverandørens forhandlings­posisjon

Sett fra leverandørens perspektiv er hovedfunnet at egen portefølje sannsynligvis ikke står optimalt allokert innenfor den hyllerammen leverandøren allerede disponerer. S3 (konservativ) indikerer minst +31 % ukentlig sell-out bare ved intern omfordeling, og hovedanbefalingen S2 gir +61 %. Dette er et tall leverandøren kan bringe med seg inn i neste kategori­besøk som dokumentert grunnlag for å endre planogrammet.

**Hva anbefalingen gir leverandøren konkret:**

- **Et kvantitativt argument i JBP.** I stedet for å si "vi bør ha mer plass til A2" basert på magefølelse, kan leverandøren presentere "modellen estimerer +X % sell-out per uke hvis A2 får 2× plass på bekostning av B2".
- **En strukturert prioriterings­liste.** Modellen identifiserer hvilke SKUer som er over- og underallokerte, og i hvilken størrelsesorden. Dette gir category managers en konkret rekkefølge for endringer, ikke en ubestemmelig "optimaliser alt".
- **En metode som skalerer.** Samme modell kan kjøres på flere butikker når data er tilgjengelig. Gevinsten kan sammenlignes på tvers og brukes til å velge hvor leverandøren bør fokusere.

**Operasjonelle forbehold.** For at anbefalingen skal være gjennomførbar i dialog med kjeden bør den fases inn gradvis og kombineres med overvåking av sell-out etter omleggingen. Leverandøren kan foreslå en delvis implementering (f.eks. halve omfordelingen) i to–fire uker, måle effekten, og deretter justere basert på observert respons. Dette gir også et naturlig grunnlag for å empirisk estimere space-elastisiteten som modellen i dag antar lineær — en elastisitets­estimasjon som i seg selv er forhandlings­verdifull for leverandøren.

**Sortiments­reduksjon er det mest politisk sensitive elementet.** Anbefalingen inkluderer betydelige reduksjoner for flere SKUer (ned mot 25 % av dagens plass). Kjeden kan ha interesse i å beholde høyere minimumsplassering av hensyn til kundetilgjengelighet, og leverandørens egne kontrakts­forpliktelser kan ha tilsvarende gulv. Når disse er kjent, skal modellen re-kjøres med skreddersydde $x_i^{\min}$-verdier per SKU.

### 8.4 Generaliserbarhet

Resultatene gjelder spesifikt for den valgte kategorien i den spesifikke butikken i den observerte perioden. De metodiske funnene — at en enkel deterministisk LP med minimums-sortimentsgaranti identifiserer meningsfulle omfordelingspotensialer, og at gevinsten i stor grad drives av A-klassen — har bredere overføringsverdi. Metodens styrke er nettopp at den krever lite data (ukessalg og kapasitet) og er rask å formulere og kjøre. Den kan derfor rulles ut som en innledende screening på tvers av butikker og kategorier før mer datakrevende analyser iverksettes.

### 8.5 Oppsummering av diskusjonen

Analysen peker på reell omfordelingsgevinst som er robust mot rimelige variasjoner i antagelsene. Modellens nøkkelbegrensning er den antatt lineære produktivitetsfunksjonen og fraværet av økonomiske vektinger; begge svakhetene forsterker poenget om at den kvantifiserte gevinsten bør tolkes som en retning og et størrelsesorden-estimat, ikke en presis prognose. Den operasjonelle implikasjonen — at hylleplanen i dag er tydelig ute av takt med observert etterspørsel for denne kategorien — står uavhengig av modellens svakheter.

---

## 9 Konklusjon

Problemstillingen spurte hvordan en dagligvare­leverandør kan bruke ukentlige sell-out-data fra en kjede-butikk som beslutningsstøtte i forhandlinger om hylleplass, og hvilket salgspotensial som kan dokumenteres ved reallokering innenfor leverandørens egen portefølje hos Coop Extra X.

Svaret, basert på pilot-analysen av åtte SKUer i leverandørens portefølje, er:

- **Under- og overallokerte SKUer kan identifiseres rutinemessig** gjennom et enkelt utnyttelsesmål (gjennomsnittlig ukentlig sell-out dividert på hylleallokering) kombinert med en ABC-klassifisering. I pilot­dataene peker modellen på to klart underallokerte A-klasse­produkter og fire overallokerte B/C-klasse­produkter.
- **Reallokerings­potensialet innen leverandørens portefølje er betydelig.** En deterministisk LP-modell som omfordeler leverandørens kontraktuelle hylleramme gir mellom +31 % og +63 % i forventet ukentlig sell-out — avhengig av antagelser om skjult etterspørsel og sortiments­gulv. Hovedanbefalingen (S2 Realistisk) gir +61 % med intakt sortiment og et gulv på 25 % av dagens allokering per SKU.
- **Gevinsten er robust.** Sensitivitets­analysen viser at selv ved konservative antagelser (1,25× skjult etterspørsel) ligger LP-salget 16 % over observert baseline. Resultatet er også nærmest flatt mot minimums-sortimentsparameteren opp til 0,40, noe som gir leverandøren operasjonelt spillerom for å forhandle om strengere sortiments­gulv uten å miste vesentlig av argumentet.
- **Scope gir metoden naturlig skalerbarhet.** Siden modellen bare krever data leverandøren allerede disponerer — sell-out per SKU og egen hylleallokering — kan samme analyse kjøres på flere butikker, tidsperioder og porteføljer uten å forutsette kategoriovergripende informasjon.

**Praktiske implikasjoner.** Metoden gir leverandøren et kvantitativt argument som kan brukes direkte i JBP- og kategori­besøk. I stedet for å argumentere for "mer plass" generelt, dokumenterer leverandøren et konkret reallokerings­forslag innenfor eksisterende hylleramme. Siden forslaget ikke krever utvidet plass, senker det forhandlings­friksjonen og øker sannsynligheten for at kjeden aksepterer endringen — i det minste som en delvis utrulling med oppfølgende måling.

**Forslag til videre forskning.** Tre naturlige utvidelser er identifisert: (i) *stokastisk reformulering* som eksplisitt håndterer variasjon i sell-out og gir service-level-garantier i stedet for harde kapasitets­grenser; (ii) *økonomisk vekting* der målfunksjonen maksimerer dekningsbidrag fremfor enheter, betinget av at margintall kan innhentes fra leverandørens egne systemer; (iii) *empirisk estimering av space-elastisitet* gjennom et kontrollert forsøk hos leverandørens butikker, der forslag fra modellen implementeres på noen butikker og sell-out-responsen måles mot kontrollbutikker. Replikasjon på tvers av butikker og kategorier vil også styrke grunnlaget for generalisering.

Studien demonstrerer at en konseptuelt enkel LP-modell, matet med den datatypen en leverandør realistisk disponerer (sell-out og egen hylleallokering), er tilstrekkelig for å identifisere kvantifiserbare reallokerings­potensialer. Modellens verdi ligger ikke i presisjonen av det estimerte prosent­løftet, men i at den gjør leverandørens kontraktuelle hylle­situasjon målbar mot egen sell-out — et utgangspunkt for kategori­dialog som i dag ofte mangler tallfestet underlag.

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

