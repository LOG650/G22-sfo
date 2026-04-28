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

### Bruk av kunstig intelligens

I tråd med Høgskolen i Moldes retningslinjer for KI-bruk i studentarbeider redegjør forfatterne her for hvordan kunstig intelligens er benyttet i prosjektet.

**Verktøy som er brukt.** Claude Code (Anthropic; Opus 4.7, Sonnet 4.6 og Haiku 4.5) som primær KI-agent for kode, tekst og analyse. Codex (OpenAI) er brukt sporadisk som supplement. Begge er kjørt i terminalbaserte agentmiljø (VS Code) med versjonskontroll i Git.

**Områder der KI er brukt.**

- *Idéutvikling og scope-justering.* KI har vært brukt som diskusjonspartner for problemformulering og avgrensning, blant annet ved omdefineringen av perspektivet fra butikk til leverandør 2026-04-24.
- *Python-kode.* Datarensing, ABC-klassifisering, LP-modellering i PuLP, sensitivitetsanalyse og visualiseringer er i hovedsak generert med KI-assistanse. Forfatterne har lest gjennom og kjørt all kode, kontrollert at output er rimelig, og verifisert mot rådata før resultater er overført til rapporten.
- *Figurer og tabeller.* Plotting-kode (matplotlib, seaborn, plotly) er KI-generert. Selve figurene er manuelt validert mot underliggende data.
- *Rapporttekst.* KI har bidratt med utkast, omformuleringer, struktur og språkvask. All faglig vurdering, modellantagelser, fortolkninger og endelige formuleringer er forfatternes egne valg.
- *Litteraturstøtte.* KI har foreslått søkeord, sammenfattet artikler og pekt på kilder. Hver enkelt referanse i §10 er deretter manuelt verifisert: forfatterne har lastet ned fulltekst og kontrollert at kilden faktisk eksisterer og er korrekt sitert.
- *Forelesningstranskripsjoner.* Auto-transkripsjoner av faglærers forelesninger er rensa med KI som kontekstgrunnlag for prosjektarbeidet, ikke for sitering.
- *Prosjektledelse.* MS Project-XML genereres fra JSON-kildefiler via en KI-assistert pipeline.

**Hva forfatterne står inne for.** All kode er kjørt og output er verifisert. Modellvalg, antagelser og fortolkninger er forfatternes egne. Alle referanser er fysisk lest og kontrollert.

**Hva KI ikke har gjort.** Ingen tall, datapunkter eller resultater er KI-generert uten kjøring av reell kode mot reelle data. Ingen referanser er beholdt uten manuell verifikasjon.

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

Rapporten undersøker hvordan en dagligvareleverandør kan bruke ukentlige sell-out-data fra en kjede-butikk som beslutningsstøtte i forhandlinger om hylleplass, og kvantifiserer reallokerings­gevinsten som kan dokumenteres overfor kjeden innen leverandørens egen portefølje hos Coop Extra X. Perspektivet er leverandørens; data på konkurrerende produkter inngår ikke, hvilket speiler den informasjons­asymmetri som kjennetegner reelle leverandør-kjede-forhandlinger. Basert på ukentlige sell-out-data for leverandørens 34 SKUer over ti uker (uke 06–15, 2026), formuleres en deterministisk lineær programmerings­modell (LP) implementert i Python med PuLP. Modellen omfordeler den kontraktuelle primær hylleallokeringen (1 079 frontfacings) og fordeler et begrenset antall sekundær­plasser med høyere salgsproduktivitet, slik at *margin-vektet* forventet sell-out maksimeres under produktspesifikke minimums­gulv som reflekterer sortiments­garantier. Analysen avdekker en gjennomgripende mismatch mellom hyllefordeling og etterspørsel: 24 av 34 SKUer er underkapasiterte mens 10 over­kapasiterte SKUer beslaglegger plass uten å fylles før neste etterfylling. Modellen kjøres i tre scenarier som spenner fra primær-omfordeling alene til konservativ omlegging. Hovedanbefalingen — som beholder alle 34 SKUer med et gulv på 1 kolli (3 frontfacings) og dirigerer 3 sekundær­plasser til de mest produktive A-SKUene — gir +49,8 % margin-vektet og +54,1 % i volum sammenlignet med observert baseline. En sensitivitets­analyse viser at gevinsten er robust mot de sentrale parameterantakelsene. Resultatet er operasjonelt meningsfullt i en forhandlings­kontekst siden det dokumenterer et kvantifisert reallokerings­potensial innen leverandørens egen portefølje — et utgangspunkt for kategoridialog med kjeden som krever verken investering eller utvidelse av leverandørens totale hylleallokering.

**Nøkkelord:** hylleallokering, space management, lineær programmering, retail, dagligvare, datadrevet beslutningsstøtte.

---

## Abstract

This report examines how a grocery supplier can use weekly sell-out data from a chain store as decision support in shelf-space negotiations, and quantifies the reallocation gain that can be documented towards the chain within the supplier's own portfolio at a Coop Extra store. The perspective is the supplier's; competing products are not included in the dataset — mirroring the information asymmetry typical of real supplier–retailer negotiations. Using ten weeks of weekly sell-out data for the supplier's 34 SKUs (weeks 06–15, 2026), a deterministic linear programming model (LP) implemented in Python with PuLP reallocates the supplier's contracted primary shelf space (1,079 frontfacings) and assigns a limited number of secondary-display slots with higher sales productivity so as to maximize expected *margin-weighted* sell-out, subject to minimum-floor constraints reflecting assortment commitments. The analysis surfaces a pervasive mismatch between shelf and demand: 24 of 34 SKUs are under-capacitated while 10 over-capacitated SKUs occupy shelf space that is not depleted before the next replenishment. The model is solved under three scenarios ranging from primary-only reallocation to conservative practice. The main recommendation — which preserves all 34 SKUs at a floor of one case (3 frontfacings) and assigns 3 secondary slots to the most productive A-class SKUs — yields +49.8 % margin-weighted and +54.1 % volume gain compared to the observed baseline. A sensitivity analysis shows the result is robust to the key parameter assumptions. The finding is operationally meaningful in a negotiation context because it documents a quantified reallocation potential within the supplier's own portfolio — a starting point for category dialogue with the chain that requires neither capital investment nor expansion of the supplier's total shelf allocation.

**Keywords:** shelf allocation, space management, linear programming, retail, grocery, data-driven decision support.

---

## Innhold

1. [Innledning](#1-innledning)
   1. [Problemstilling](#11-problemstilling)
   2. [Avgrensinger](#12-avgrensinger)
   3. [Antagelser](#13-antagelser)
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
- **Margin-vektet salg, ikke omsetning eller bunnlinje.** Målfunksjonen vekter forventet ukessalg med leverandørens *bruttomargin per enhet* slik den fremkommer av prislisten til Coop. Kostnader nedstrøms (logistikk, kampanjebidrag, hyllebetaling) inngår ikke. Pris- og volumdata på enkelttransaksjoner finnes ikke i datagrunnlaget.
- **Kvantitativ, ikke kvalitativ.** Prosjektet gjør ingen intervjuer med kategori­ansvarlige, butikk­sjefer eller forhandlings­parter. Alle tolkninger er basert på observerte sell-out- og kapasitets­data.

### 1.3 Antagelser

Analysen hviler på fire hovedantagelser som drøftes kritisk i §8:

1. **Observert ukentlig sell-out er representativt for den aktuelle periodens etterspørsel** for produkter som ikke går tomme. For produkter med utnyttelsesgrad ≥ 1 (hyllen tømmes før neste etterfylling) er observert salg et *nedre* anslag for reell etterspørsel.
2. **Hvert ekstra enhet hylleplass gir samme produktivitet (lineær space-elastisitet).** Reell elastisitet er sannsynligvis avtakende, noe som gjør modellens gevinst­anslag til et øvre estimat.
3. **Leverandørens minstekrav til hylleplass per SKU er ett kolli (3 frontfacings) i hovedscenariene og 50 % av dagens allokering i det konservative scenariet.** Eksplisitte kontraktsgulv per SKU er ikke tilgjengelige i dette prosjektet; ett kolli er valgt som operasjonelt minimum i tråd med kjedens påfyllingslogikk.
4. **Ingen kryssalgseffekter eller kannibalisering innen porteføljen.** Modellen behandler hvert produkt uavhengig. Mulige interaksjoner diskuteres i §8.
5. **Sekundæreksponering har høyere salgsproduktivitet enn primærhylle.** I hovedanbefalingen gis et lite antall ekstra plasser i kampanjeendene/skiveplasser med produktivitetsfaktor $k = 1{,}5$ relativt til primær­hyllen, i tråd med Chevalier (1975) og Nordfält & Ahlbom (2018). Effekten av å variere $k$ drøftes i §8.

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

Gholami & Bhakoo (2025) dokumenterer at den faktiske etterspørselen for OOS-rammede produkter kan være 1,5 til 3 ganger observert salg, avhengig av etterfyllingshyppighet og kundeatferd. Dette tallet er opprinnelsen til prosjektets `overserve_factor`-parameter (§6.4): for produkter med $u_i \ge 1$ antas den sanne etterspørselen å være en multippel av observert salg, der 2,0 brukes i hovedscenariene (S1, S2) og 1,5 i det konservative (S3). Sensitivitets­analysen (§7.3) varierer multiplikatoren fra 1,25 til 3,0 og viser at gevinsten holder seg positiv i hele intervallet.

Motstykket til OOS er *overkapasitet*: et produkt med $u_i < 1$ beslaglegger facings som aldri blir fylt før de etterfylles. Dette er "død hylle" som kunne vært omplassert til et produkt med høyere produktivitet per facing. Prosjektets utgangshypotese er at *begge fenomenene opptrer samtidig* i den observerte kategorien, og at reallokering fra overkapasiterte til underkapasiterte SKUer derfor gir netto gevinst.

### 3.4 ABC-klassifisering og Pareto-prinsippet

ABC-klassifisering er en praktisk anvendelse av Pareto-prinsippet (Pareto, 1896; videreført av Koch, 1997) på sortimentsstyring. Produkter sorteres etter deres bidrag til en valgt nøkkelindikator — her totalsalg i enheter — og deles inn i tre klasser basert på kumulativ andel:

- **A-produkter:** topp ≈ 80 % av kumulativt salg; typisk få SKUer
- **B-produkter:** neste ≈ 15 %
- **C-produkter:** de siste ≈ 5 %; typisk mange SKUer

Klassifiseringen brukes i praksis til å differensiere styringsregimer (hyppigere varetelling for A-produkter, bestemme hvilke produkter som fortjener egne kampanjer, osv.). I denne analysen brukes den tosidig: som struktureringsprinsipp for hvilke produkter som er de mest aktuelle kandidatene for mer hylleplass (A-klassen), og som grunnlag for pseudonymiseringen av produktnavn (§5.2) slik at rapporten kan leses uten å vite hvilke konkrete merkevarer som er involvert.

### 3.5 Sammenkobling — fra teori til modell

Sammen gir de fire teoretiske byggesteinene følgende operative narrativ: Hvis en butikk har et sortiment med både overkapasiterte og underkapasiterte SKUer (§3.3), og vi antar at hvert facing gir et målbart salgsbidrag (§3.1), så kan vi formulere et lineært optimeringsproblem (§3.2) som omfordeler den faste hyllekapasiteten slik at *forventet margin-vektet* salg maksimeres, hvor ABC-klassifiseringen (§3.4) gir en naturlig førsteintuisjon om hvilke produkter som bør få mer plass. Margin-vektingen — å gange hver SKUs forventede salg med leverandørens bruttomargin per enhet — kobler hylleallokerings­problemet til leverandørens reelle lønnsomhets­funksjon, ikke bare volum. Dette er nettopp det modellen i §6 gjør, og resultatene i §7 evaluerer.

---

## 4 Casebeskrivelse

Case-studien tar utgangspunkt i leverandørens perspektiv. Leverandøren er en stor, global produsent av kullsyreholdige leskedrikker med et bredt porteføljetilbud og en etablert kontraktuell hylleallokering hos Coop-kjeden i Norge. Analyse­enheten er leverandørens portefølje slik den er representert hos én konkret Coop Extra-butikk ("Coop Extra X"). Av hensyn til taushetserklæring inngått mellom prosjektgruppen og butikken/leverandøren er hverken butikkens geografiske lokasjon, leverandørens navn eller faktiske produktnavn gjengitt i rapporten; alle produkter er omtalt med pseudonymer (se §5.2).

### 4.1 Leverandørens portefølje som analyse-enhet

Case-studien ser på leverandørens SKU-portefølje slik den finnes i butikkens sortiment i observasjonsperioden. Porteføljen dekker kullsyreholdige leskedrikker i plastflasker (0.5 L og 1.5 L), energidrikk i boks, og en idrettsdrikk. Konkurrerende merkevarer fra andre leverandører er *ikke* inkludert — verken i sell-out-data eller i kapasitets­oversikten — i tråd med den informasjons­asymmetrien en leverandør realistisk arbeider under.

Porteføljen valg gjenspeiler den datatypen leverandøren disponerer i sin forhandlings­forberedelse: sell-out per uke for egne SKUer, samt nåværende kontraktuell hylleallokering per SKU hos butikken. Det leverandøren *ikke* har innsyn i — konkurrenters salg, konkurrenters hylleplass, kundesegmentering utover kjedens aggregater — er også det modellen ikke forutsetter å kjenne.

### 4.2 Hyllekontrakt og rammebetingelser

Leverandørens *hylle-allokering* hos butikken er et kontraktuelt tall: antall hylleenheter (frontfacings × dybde × antall hyller) fordelt mellom leverandørens SKUer i butikkens planogram. Analyseperioden har holdt denne fordelingen konstant, hvilket betyr at variasjon i salg ikke kan forklares av endringer i hylleplass. Reallokering innenfor leverandørens kontraktuelle ramme krever dialog med butikken/kjeden men vanligvis ikke reforhandling av kontrakten — og representerer derfor en relativt lav-friksjons endring sammenlignet med å argumentere for utvidelse av totalrammen.

**Samlet primær hylleallokering som leverandøren disponerer hos Coop Extra X i observasjons­perioden: 1 079 frontfacings fordelt på 34 SKUer.** I tillegg disponerer leverandøren *3 avtalte sekundærplasser* (kampanjeender og skiveplasser) hos butikken. Hovedanbefalingen i §6/§7 tildeler disse 3 plassene til de SKUene modellen identifiserer som mest produktive på sekundær­plass.

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

**Implementering og reproduserbarhet.** All analyse er implementert i Python 3.12. Modellene bruker biblioteket PuLP med CBC-solver for lineær programmering, pandas for datamanipulasjon, og matplotlib/seaborn/plotly for visualisering. Kode og genererte figurer/tabeller versjoneres i prosjektets Git-repository; pseudonymiserte versjoner av resultatene inngår i repoet, mens filer med ekte produktnavn holdes lokalt i en `intern/`-underfolder som er ekskludert fra versjonering. Hele kjøringen (datarensing → deskriptiv analyse → LP → sensitivitet → figurer) kan reproduseres med kommandoene som dokumenteres i `006 analysis/README.md`. Anonymiseringsmodulen `anonymisering.py` sikrer at produkter i alle genererte artefakter har samme pseudonymer på tvers av scripts.

**Figur 5.1.1** (`006 analysis/aktiviteter/3_5_analyse_og_resultater/figurer/analyse_pipeline.png`) gir en oversikt over hele pipelinen: rådata + planogram + margin-mapping inn til venstre, datarensing og deskriptiv analyse, LP-modell og sensitivitets­analyse, og figurer/rapport ut til høyre.

**Kvalitetssikring.** Intern kvalitetssikring skjer i henhold til prosjektplanen: hver analyse-artefakt genereres deterministisk fra rådata og sanity-sjekkes mot intuisjon (f.eks. at ABC-summen blir 100 %, at LP-status er "Optimal", og at summen av allokerte facings tilsvarer total kapasitet). Peer-to-peer review planlegges i henhold til slagplanen for fase 3. Formelle akademiske krav følger SKRIVING-kompendiet (Kap. 3), herunder APA 7-referansestil for bibliografien i §10.

**Etiske hensyn.** Studien behandler ikke personopplysninger og faller utenfor personopplysningsloven og helseforskningsloven (se egenerklæringen foran i rapporten). Konfidensialitet overfor Coop Extra X er ivaretatt gjennom taushetserklæring og pseudonymisering av produktnavn i alle offentlig tilgjengelige artefakter.

### 5.2 Data

Datagrunnlaget består av to sammenslåtte kilder: **ukentlig sell-out per SKU** (kundekjøp registrert i butikkens POS-system) og **kontraktuell hylleallokering per SKU** (antall enheter tildelt SKU i leverandørens del av planogrammet). Begge kilder dekker *leverandørens portefølje* hos Coop Extra X i observasjons­perioden; konkurrerende SKUer fra andre leverandører er ikke inkludert, i tråd med scope definert i §1.2.

Datasettet dekker hele leverandørens portefølje hos butikken i observasjons­perioden — 34 SKUer fordelt på flere drikkekategorier (kullsyreholdig leskedrikk, energi, idrettsdrikk, vann) og på tvers av størrelser og emballasje­typer. Konkrete merkenavn er holdt utenfor rapporten i tråd med taushetserklæringen.

**Omfang**

| Attributt | Verdi |
|---|---|
| Periode | Uke 06 – uke 15, 2026 (10 uker) |
| Kjede | Coop Extra |
| Butikk | Anonymisert enhet (Coop Extra X) |
| Antall SKUer | 34 |
| Observasjoner (SKU × uke) | 306 |
| Variabler | År, ukenummer, SKU, antall solgt, hyllekapasitet (frontfacings), brutto margin per enhet |

**Datakvalitet.** Ingen dubletter eller negative salgstall ble oppdaget i rådataene. Én SKU i den opprinnelige eksporten mangler kontraktuell hylleallokering og er forkastet i analysen (34 SKUer beholdt). Resterende rådata har varierende dekning per SKU — i gjennomsnitt 9 av 10 ukesobservasjoner per produkt, med 306 rader totalt. Manglende uker er utelatt for det aktuelle produktet; gjennomsnitt over de tilgjengelige ukene vurderes som akseptabel behandling. Alternative behandlinger (median-imputering, rullende gjennomsnitt) ga ikke materielle forskjeller og er ikke valgt for å unngå å introdusere artificial smoothing.

**Margindata.** Leverandørens bruttomargin per enhet er basert på leverandørens egen marginrapportering og varierer fra ca. 30 % til ca. 55 % på tvers av porteføljens produktgrupper, der energidrikks­segmentet typisk ligger lavt og leskedrikks-/idretts-/vann-SKUer typisk høyt. Marginprosenten brukes som vekt $m_i$ i målfunksjonen i §6 og er tilleggsvariabelen som skiller margin-vektet salg (baseline 846,9) fra rent enhets­salg (baseline 2 080,2 enheter/uke). Konkrete margin­tall per SKU er holdt utenfor rapporten i tråd med taushetserklæringen.

**Pseudonymisering.** For å ivareta taushetserklæringen omtaler rapporten produktene med pseudonymer på formen `{Klasse}{Nr}`, der klassen `A`/`B`/`C` tilsvarer ABC-klassifiseringen (se nedenfor) og nummeret rangerer produktet innen klassen etter totalsalg. Det resulterende navneregisteret lagres utenfor offentlig repository sammen med rådataene. Tabell 5.2.1 oppsummerer det anonymiserte datagrunnlaget.

**Tabell 5.2.1 Deskriptive nøkkeltall per produkt (uke 06–15, 2026)**

Tabellen er sortert etter utnyttelsesgrad (synkende). Verdier > 1 indikerer at ukesalget overstiger antallet frontfacings og at hyllen etterfylles mer enn én gang per uke.

| Produkt | Gj.snitt salg/uke | Std | Min | Maks | CoV | Hyllekap. | Utnyttelse |
|---|---:|---:|---:|---:|---:|---:|---:|
| A2 | 191,0 | 92,6 | 87 | 412 | 0,49 | 21 | 9,10 |
| A1 | 417,0 | 41,3 | 336 | 475 | 0,10 | 63 | 6,62 |
| A6 | 78,2 | 23,1 | 53 | 126 | 0,30 | 21 | 3,72 |
| A7 | 77,8 | 22,1 | 36 | 116 | 0,28 | 21 | 3,70 |
| A9 | 71,9 | 13,3 | 48 | 88 | 0,19 | 21 | 3,42 |
| A10 | 60,2 | 16,7 | 40 | 89 | 0,28 | 21 | 2,87 |
| A11 | 59,3 | 10,0 | 46 | 71 | 0,17 | 21 | 2,82 |
| A12 | 57,4 | 19,3 | 28 | 92 | 0,34 | 21 | 2,73 |
| A13 | 57,3 | 13,8 | 37 | 80 | 0,24 | 21 | 2,73 |
| A5 | 109,9 | 16,4 | 86 | 137 | 0,15 | 42 | 2,62 |
| A14 | 48,6 | 12,8 | 32 | 73 | 0,26 | 21 | 2,31 |
| B1 | 48,5 | 20,0 | 13 | 70 | 0,41 | 21 | 2,31 |
| B2 | 96,2 | 38,9 | 61 | 158 | 0,40 | 42 | 2,29 |
| B3 | 42,9 | 9,3 | 25 | 56 | 0,22 | 21 | 2,04 |
| C1 | 23,4 | 7,0 | 9 | 33 | 0,30 | 12 | 1,95 |
| B4 | 37,7 | 7,2 | 27 | 50 | 0,19 | 21 | 1,80 |
| A8 | 73,1 | 19,0 | 27 | 93 | 0,26 | 42 | 1,74 |
| B5 | 36,6 | 12,7 | 18 | 56 | 0,35 | 21 | 1,74 |
| B6 | 32,6 | 19,3 | 14 | 78 | 0,59 | 21 | 1,55 |
| C3 | 20,6 | 17,6 | 3 | 51 | 0,86 | 16 | 1,28 |
| B7 | 25,2 | 7,2 | 14 | 39 | 0,29 | 21 | 1,20 |
| B8 | 23,7 | 9,2 | 4 | 34 | 0,39 | 21 | 1,13 |
| B9 | 23,7 | 16,9 | 4 | 64 | 0,71 | 21 | 1,13 |
| A3 | 148,0 | 28,7 | 104 | 191 | 0,19 | 147 | 1,01 |
| A4 | 123,7 | 19,5 | 89 | 148 | 0,16 | 168 | 0,74 |
| C2 | 19,8 | 5,2 | 11 | 30 | 0,26 | 28 | 0,71 |
| C4 | 14,5 | 5,5 | 6 | 23 | 0,38 | 21 | 0,69 |
| C7 | 8,0 | 3,8 | 1 | 11 | 0,47 | 12 | 0,67 |
| C5 | 14,8 | 6,5 | 7 | 26 | 0,44 | 24 | 0,62 |
| C9 | 12,0 | 15,6 | 1 | 23 | 1,30 | 21 | 0,57 |
| C10 | 12,0 | 7,1 | 7 | 17 | 0,59 | 21 | 0,57 |
| C6 | 7,4 | 5,0 | 3 | 20 | 0,68 | 21 | 0,35 |
| C11 | 4,0 | — | 4 | 4 | — | 21 | 0,19 |
| C8 | 3,2 | 2,8 | 1 | 9 | 0,87 | 21 | 0,15 |

*Utnyttelse = gjennomsnittlig ukesalg / hyllekapasitet. CoV = variasjonskoeffisient (Std/Gj.snitt) og brukes som proxy for etterspørselens volatilitet. C11 har bare én observasjon i perioden og lar seg derfor ikke variasjonsmåle.*

**ABC-klassifisering.** Produkter er klassifisert i A/B/C basert på akkumulert andel av totalsalg over perioden, med de konvensjonelle tersklene 80 % og 95 %. Klassifiseringen gir 14 A-produkter (78,5 % av totalsalg, 826 av 1 079 frontfacings = 76,6 %), 9 B-produkter (16,0 % av salg) og 11 C-produkter (5,5 % av salg). 24 av 34 SKUer har utnyttelses­grad over 1,0 — den observerte mismatchen er gjennomgripende, ikke begrenset til enkeltprodukter. Denne fordelingen danner utgangspunktet for reallokerings­analysen i §7.

**Figur 5.2.1** (`006 analysis/aktiviteter/3_4_data_metode_og_modellering/figurer/salg_vs_kapasitet_tidsserie.png`) viser ukentlig salg mot kapasitet per SKU. **Figur 5.2.2** (`utnyttelse_mismatch.png`) viser gjennomsnittlig utnyttelsesgrad, og **Figur 5.2.3** (`abc_pareto.png`) viser Pareto-fordelingen av totalsalget.

---

## 6 Modellering

Reallokerings­problemet formuleres som en lineær programmerings­modell (LP) der målet er å fordele leverandørens *kontraktuelle hylleallokering* mellom egne SKUer slik at forventet samlet **margin-vektet** sell-out maksimeres innenfor produktspesifikke etterspørsels­grenser og sortiments­gulv. Modellen omfordeler utelukkende innen leverandørens portefølje; SKUer fra andre leverandører inngår hverken i målfunksjonen eller i kapasitets­restriksjonen. Formuleringen er deterministisk og periode­gjennomsnittlig: en enkelt «typisk uke» representerer perioden uke 06–15 2026. Modellen håndterer to hyllemiljøer — *primær* (ordinær hylleplass i leskedrikks­seksjonen) og *sekundær* (kampanjeender, skiveplasser ved kasse­område), der sistnevnte har høyere salgsproduktivitet per facing.

### 6.1 Mengder og indekser

| Symbol | Beskrivelse |
|---|---|
| $P$ | Mengde av leverandørens SKUer i butikkens sortiment, $i \in P$. Andre leverandørers SKUer inngår ikke i $P$. $\lvert P \rvert = 34$. |

### 6.2 Parametere

| Symbol | Enhet | Beskrivelse | Verdi / kilde |
|---|---|---|---|
| $T$ | frontfacings | Leverandørens samlede primær hylleallokering hos butikken, konstant i perioden. Dekker *ikke* kategoriens totale hylleplass. | 1 079 |
| $T^{\text{sek}}$ | sekundærplasser | Antall sekundær­eksponerings­plasser leverandøren disponerer i butikken (kampanjeende, skiveplass). | 3 (hovedscenario), 0 (S1, S3) |
| $c_i$ | frontfacings | Nåværende primær allokering av hylleplass til produkt $i$ | Tabell 5.2.1 |
| $\bar s_i$ | enheter/uke | Gjennomsnittlig observert ukesalg for produkt $i$ | Tabell 5.2.1 |
| $\rho_i$ | enheter/facing/uke | Primær produktivitet per frontfacing, $\rho_i = \bar s_i / c_i$ | Utledet |
| $k$ | — | Sekundær­eksponerings­faktor; salg per sekundær­plass = $k \cdot \rho_i$. | 1,5 (Chevalier 1975; Nordfält & Ahlbom 2018) |
| $m_i$ | NOK/enhet (relativ) | Leverandørens bruttomargin per enhet for produkt $i$ — fra prisliste til Coop, normalisert som andel. | 0,30–0,55 |
| $d_i$ | enheter/uke | Estimert øvre grense for ukentlig etterspørsel | §6.4 |
| $x_i^{\min}$ | frontfacings | Minimum antall frontfacings for å beholde produktet i sortimentet | 3 (1 kolli; hovedscenario) |

### 6.3 Beslutningsvariabler

$$
x_i \in \mathbb{Z}_{\ge 0}, \quad z_i \in \mathbb{Z}_{\ge 0}, \quad y_i \in \mathbb{R}_{\ge 0}, \quad \forall i \in P
$$

der $x_i$ er antall *primær* frontfacings og $z_i$ er antall *sekundær*­plasser tildelt produkt $i$. $y_i$ er forventet realisert salg i enheter per uke.

### 6.4 Etterspørselsantagelse

For SKUer med observert utnyttelse under 1,0 legges det til grunn at målt ukentlig sell-out svarer til etterspørselen ($d_i = \bar s_i$). For SKUer der observert sell-out overstiger hylleallokering, er salget begrenset av hylle og ikke av etterspørsel; den sanne etterspørselen er høyere enn observert sell-out men er ikke direkte målbar. I hovedscenariene brukes $d_i = 2\bar s_i$, en antakelse som reflekterer at out-of-stock-situasjoner er observert i flere uker for disse produktene. Det konservative scenariet (S3) bruker $d_i = 1{,}5 \bar s_i$. Alternative verdier prøves i sensitivitets­analysen (§7.3).

### 6.5 Målfunksjon

Modellen maksimerer forventet *margin-vektet* salg per uke:

$$
\max \sum_{i \in P} m_i \cdot y_i
$$

Vekten $m_i$ er leverandørens bruttomargin per enhet (uttrykt som andel av salgspris) og lar modellen prioritere produkter som er mer lønnsomme for leverandøren framfor produkter som bare er volumstore. Volum­tall (uveket sum av $y_i$) rapporteres parallelt i §7 for å vise at en margin-vektet anbefaling også gir betydelig volumvekst.

### 6.6 Restriksjoner

**R1 — Leverandørens kontraktuelle primær hylleramme.** Omfordelingen av primær hylleplass skjer innenfor den hylleallokering leverandøren allerede disponerer, uten netto endring mot resten av kategorien:

$$
\sum_{i \in P} x_i = T
$$

**R2 — Salgsrealisasjon begrenses av total kapasitet (primær + sekundær).** Forventet salg kan ikke overstige det antall enheter som tildelte facings kan omsette, der sekundærplasser har $k$ ganger primær­produktivitet:

$$
y_i \le \rho_i \, x_i + k \rho_i z_i, \quad \forall i \in P
$$

**R3 — Salgsrealisasjon begrenses av etterspørsel.** Forventet salg kan ikke overstige estimert etterspørsel:

$$
y_i \le d_i, \quad \forall i \in P
$$

**R4 — Minimum sortimentsgaranti.** Hvert produkt må ha minst $x_i^{\min}$ primær frontfacings:

$$
x_i \ge x_i^{\min}, \quad \forall i \in P
$$

**R5 — Sekundær­eksponerings­budsjett.** Antall sekundærplasser er begrenset av leverandørens totale sekundær­avtale med kjeden:

$$
\sum_{i \in P} z_i \le T^{\text{sek}}
$$

### 6.7 Oppsummering

Modellen har $2\lvert P \rvert = 68$ heltalls-beslutningsvariabler ($x_i, z_i$), $\lvert P \rvert = 34$ kontinuerlige variable ($y_i$), og $3\lvert P \rvert + 2 = 104$ lineære restriksjoner. Den lar seg løse med CBC-solveren som følger med PuLP, og optimum oppnås på under to sekunder for det aktuelle datasettet. Beregningene er implementert i `006 analysis/aktiviteter/3_4_data_metode_og_modellering/scripts/03_lp_modell.py`.

---

## 7 Analyse og resultater

Kapitlet presenterer resultatene av LP-modellen fra §6 anvendt på leverandørens samlede portefølje hos Coop Extra X — 34 SKUer med totalt 1 079 frontfacings i primær­hyllen og inntil 3 sekundær­plasser. Analysen er strukturert i tre deler: (i) en sammenligning av tre allokerings­scenarier som spenner fra primær-omfordeling alene til konservativ omlegging, (ii) en detaljert gjennomgang av hovedanbefalingen (S2) på produktnivå, og (iii) en sensitivitets­analyse av de to viktigste modell­parameterne.

Alle tall i §7 er for én typisk uke i observasjons­perioden. To resultatstørrelser rapporteres: **margin-vektet salg** ($\sum m_i y_i$, som er målfunksjonen) og **volum** ($\sum y_i$, antall enheter). Margin-baseline er 846,9; volum-baseline er 2 080,2 enheter/uke.

### 7.1 Scenariesammenligning

Tre scenarier ble kjørt mot samme LP-formulering, men med ulike verdier for sekundær­budsjett $T^{\text{sek}}$, etterspørsels­multiplikator $d_i / \bar s_i$ og minimums-sortimentet. Tabell 7.1 oppsummerer.

**Tabell 7.1 LP-scenarier og oppnådd margin-vektet salg per uke**

| Scenario | $x_i^{\min}$ | $d_i$ for underkap. | $T^{\text{sek}}$ | LP-margin | Gevinst | Gev % | Volum (enh.) | Volum-gev % |
|---|---|---|---:|---:|---:|---:|---:|---:|
| S1 Primær-omfordeling | 3 facings | $2\bar s_i$ | 0 | 1 265,9 | +419,0 | +49,5 % | 3 202 | +53,9 % |
| **S2 Primær + sekundær** | **3 facings** | **$2\bar s_i$** | **3** | **1 268,4** | **+421,5** | **+49,8 %** | **3 206** | **+54,1 %** |
| S3 Konservativ | 50 % av $c_i$ | $1{,}5\bar s_i$ | 0 | 1 060,0 | +213,0 | +25,2 % | 2 636 | +26,7 % |

Figur 7.1 (`006 analysis/aktiviteter/3_4_data_metode_og_modellering/figurer/lp_scenario_compare.png`) viser allokeringen per produkt på tvers av de tre scenariene sammen med nåværende allokering.

Tre observasjoner er sentrale:

1. **Primær­omfordeling alene gir +49,5 % margin-løft.** Modellen finner at A-klasse-SKUer med høy utnyttelses­grad og høy margin er underdimensjonerte; reallokering fra to bestselgere med lav margin (A4) og fra C-/B-klasse-SKUer med lav utnyttelse løfter margin­vektet salg fra 846,9 til 1 265,9.
2. **Sekundær­eksponering bidrar marginalt på toppen** av primær­omfordelingen — bare +2,5 margin­enheter ekstra (S2 vs. S1). De tre sekundærplassene tildeles A2 (2 plasser) og A3 (1 plass), de to A-produktene som mest aggressivt treffer etterspørsels­taket. Effekten i hovedanbefalingen er dermed liten i kroner og tjener mer som *forhandlings­argument* enn som hovedkilde til gevinst.
3. **S3 gir +25,2 % gevinst med halv-så-aggressiv omlegging.** Den er egnet som mellom­steg i en inkrementell utrulling. 20 av 34 SKUer får mer plass i S3, mot 19 i S2.

### 7.2 S2 Primær + sekundær — hovedanbefaling

Hovedanbefalingen omfordeler de 1 079 primær frontfacings og fordeler 3 sekundærplasser slik det fremgår av Tabell 7.2. Per-produkt-allokeringen er også vist i Figur 7.2 (`lp_allokering_S2_primaer_sek.png`).

**Tabell 7.2 S2 Primær + sekundær — allokering per produkt**

Margin-kolonne er ikke inkludert; SKUer på øvre del av margin­spennet (≈ 55 %) er markert med † for å vise at modellen prioriterer dem ved likevektige produktivitets­tilfeller.

| Produkt | Facings nå | Min | Primær ny | Sek. | Δ primær | Salg nå | Salg ny | Δ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | 63 | 3 | 126 | 0 | +63 | 417,0 | 834,0 | +417,0 |
| A2† | 21 | 3 | 39 | 2 | +18 | 191,0 | 382,0 | +191,0 |
| A3† | 147 | 3 | 102 | 1 | −45 | 148,0 | 104,2 | −43,8 |
| A4† | 168 | 3 | 3 | 0 | −165 | 123,7 | 2,2 | −121,5 |
| A5 | 42 | 3 | 84 | 0 | +42 | 109,9 | 219,8 | +109,9 |
| A6† | 21 | 3 | 42 | 0 | +21 | 78,2 | 156,4 | +78,2 |
| A7 | 21 | 3 | 42 | 0 | +21 | 77,8 | 155,6 | +77,8 |
| A8 | 42 | 3 | 3 | 0 | −39 | 73,1 | 5,2 | −67,9 |
| A9 | 21 | 3 | 42 | 0 | +21 | 71,9 | 143,8 | +71,9 |
| A10 | 21 | 3 | 42 | 0 | +21 | 60,2 | 120,4 | +60,2 |
| A11† | 21 | 3 | 42 | 0 | +21 | 59,3 | 118,6 | +59,3 |
| A12 | 21 | 3 | 42 | 0 | +21 | 57,4 | 114,8 | +57,4 |
| A13 | 21 | 3 | 42 | 0 | +21 | 57,3 | 114,6 | +57,3 |
| A14 | 21 | 3 | 42 | 0 | +21 | 48,6 | 97,2 | +48,6 |
| B1 | 21 | 3 | 42 | 0 | +21 | 48,5 | 97,0 | +48,5 |
| B2 | 42 | 3 | 84 | 0 | +42 | 96,2 | 192,4 | +96,2 |
| B3 | 21 | 3 | 42 | 0 | +21 | 42,9 | 85,8 | +42,9 |
| B4 | 21 | 3 | 3 | 0 | −18 | 37,7 | 5,4 | −32,3 |
| B5 | 21 | 3 | 3 | 0 | −18 | 36,6 | 5,2 | −31,4 |
| B6 | 21 | 3 | 3 | 0 | −18 | 32,6 | 4,7 | −27,9 |
| B7† | 21 | 3 | 42 | 0 | +21 | 25,2 | 50,4 | +25,2 |
| B8† | 21 | 3 | 42 | 0 | +21 | 23,7 | 47,4 | +23,7 |
| B9† | 21 | 3 | 42 | 0 | +21 | 23,7 | 47,4 | +23,7 |
| C1† | 12 | 3 | 24 | 0 | +12 | 23,4 | 46,8 | +23,4 |
| C3† | 16 | 3 | 32 | 0 | +16 | 20,6 | 41,1 | +20,5 |
| C2, C4–C11 | 14–28 | 3 | 3 | 0 | −11 til −25 | 3–20 | 0,5–2,1 | sterkt ned |

Omfordelingen følger fire mønstre:

- **A-klasse dobler primær­plassen.** 12 av 14 A-SKUer går opp til kapasitet hvor frontfacings akkurat matcher antatt etterspørsel ($x_i \approx d_i / \rho_i$), slik at hyllen ikke lenger er bindende.
- **To A-volum-SKUer reduseres mye.** A3 går fra 147 til 102 facings; A4 går fra 168 til minimums­gulvet på 3. Den observerte utnyttelses­graden var 0,74 for A4 og 1,01 for A3 — modellen flytter kapasiteten dit den gir mer salg.
- **B-klasse splittes etter produktivitet og margin.** B1, B2, B3, B7, B8, B9 (alle med høy utnyttelses­grad) vokser. B4–B6 har lavere produktivitet og margin og går til gulvet.
- **C-klasse gir fra seg alt over 1-kolli-gulvet.** C-produkter har samlet under 6 % av margin­basen og er enten over­dimensjonerte eller for små i absolutt volum til å konkurrere med A/B-alternativene per facing. Unntak: C1 og C3, som ligger på øvre del av margin­spennet og har høy observert utnyttelse, vokser.

**Sekundær­plassene** tildeles A2 (2 plasser) og A3 (1 plass). Begge ligger på øvre del av margin­spennet, og A2 er den mest underdimensjonerte SKUen i porteføljen (utnyttelses­grad 9,10). Sekundær­plassene flytter A2-salget videre opp utover hva primær­hyllen alene tillater i scenariet. Forhandlings­messig betyr dette at leverandøren kan be om sekundær­eksponering for de samme to SKUene som modellen anbefaler — et tallfestet underlag for hvor sekundær­plassen faktisk gir marginal lønnsomhet.

**Figur 7.2b** (`006 analysis/aktiviteter/3_5_analyse_og_resultater/figurer/sankey_omfordeling_S2.png`) visualiserer omfordelingen som et Sankey-diagram: 466 frontfacings flyttes fra 14 *over­dimensjonerte* SKUer (venstre) til 19 *underdimensjonerte* SKUer (høyre). Båndtykkelsen er proporsjonal med antall facings, og fargene markerer ABC-klasse (blå A, grønn B, oransje C). Diagrammet gjør det visuelt tydelig at gevinsten kommer fra omfordeling, ikke fra eliminering, og at hovedstrømmen går fra to A-volum-SKUer (A3, A4) til den brede A-klasse­fronten.

Det må bemerkes at A4-reduksjonen — fra 168 til 3 facings — er en *mekanisk* løsning gitt observert lav utnyttelses­grad. I praksis ville dette krevd egen dialog med kjeden om sortiments­bredden i den aktuelle produktundergruppen; punktet diskuteres i §8.

*†-merke:* SKU ligger på øvre del av margin­spennet (≈ 55 %).

### 7.3 Sensitivitetsanalyse

LP-resultatet hviler på to antakelser som er vanskelige å verifisere direkte: hvor mye høyere den sanne etterspørselen er enn observert salg for produkter som går tomme (`overserve_factor`), og hvor streng minimums-sortimentet binder (`x_min_fraction`). Tabell 7.3 og 7.4 viser hvordan total forventet ukesalg endrer seg når disse to parameterne varieres rundt S2-verdiene. *Merk:* sensitivitets­analysen rapporteres i volum-enheter (ikke margin) for å være sammenlignbar med litteraturens gevinst­anslag og fordi `overserve_factor` virker direkte på enheter.

**Tabell 7.3 Sensitivitet på etterspørsels­antakelse (x_min_fraction = 0,25)**

| overserve_factor | Volum (enh./uke) | Gevinst | Gevinst % |
|---:|---:|---:|---:|
| 1,25 | 2 438,4 | +358,2 | +17,2 % |
| 1,50 | 2 746,9 | +666,7 | +32,1 % |
| 1,75 | 3 025,6 | +945,4 | +45,5 % |
| **2,00** | **3 265,1** | **+1 184,9** | **+57,0 %** |
| 2,50 | 3 620,3 | +1 540,1 | +74,0 % |
| 3,00 | 3 905,9 | +1 825,7 | +87,8 % |

**Tabell 7.4 Sensitivitet på minimums-allokering (overserve_factor = 2,0)**

| x_min_fraction | Volum (enh./uke) | Gevinst | Gevinst % |
|---:|---:|---:|---:|
| 0,00 | 3 341,5 | +1 261,3 | +60,6 % |
| 0,10 | 3 326,3 | +1 246,1 | +59,9 % |
| **0,25** | **3 265,1** | **+1 184,9** | **+57,0 %** |
| 0,40 | 3 184,5 | +1 104,3 | +53,1 % |
| 0,50 | 3 115,4 | +1 035,2 | +49,8 % |
| 0,60 | 3 029,0 | +948,8 | +45,6 % |
| 0,80 | 2 806,0 | +725,8 | +34,9 % |

Resultatene gir to tydelige innsikter:

1. **Gevinsten er monotont økende i `overserve_factor`** (Figur 7.4a, `sensitivitet_overserve.png`), fordi høyere antatt etterspørsel hever taket $d_i$ for de underdimensjonerte A-produktene. Selv ved konservativ antakelse (1,25×) ligger volum­gevinsten på +17 %. Selv om den sanne etterspørselen er betydelig lavere enn antakelsen i hovedscenariet, kvalifiserer reallokering fortsatt som en forbedring.
2. **Gevinsten er nærmest flat i `x_min_fraction`** opp til omtrent 0,40, og faller deretter gradvis (Figur 7.4b, `sensitivitet_xmin.png`). Praktisk betyr dette at kjeden har betydelig operasjonelt spillerom: de kan binde minimums-sortimentet strammere enn S2 (3-facings-gulv) opp mot 40 % av nåværende allokering uten å miste vesentlig av gevinsten.

**Figur 7.5** (`006 analysis/aktiviteter/3_5_analyse_og_resultater/figurer/sensitivitet_2d_heatmap.png`) viser de to dimensjonene samlet i ett to-dimensjonalt rutenett — venstre panel for margin-vektet gevinst, høyre panel for volum­gevinst, begge i prosent over baseline. S2-punktet (overserve_factor = 2,0, x_min_fraction = 0,25) er markert med rød ring. Heatmappen synliggjør at gevinsten er positiv over hele det realistiske parameter­rommet og at de to parameterne påvirker resultatet i ulik retning og styrke: overserve_factor flytter gevinsten oppover (kolonner), mens et strengere x_min_fraction trekker gevinsten ned (rader nedover) først merkbart fra 0,40.

### 7.4 Sentrale funn

- Den observerte mismatchen mellom kapasitet og etterspørsel (§5.2) er gjennomgripende — 24 av 34 SKUer er underkapasiterte — og gir en LP-drevet reallokering rom til betydelig forbedring selv under konservative forutsetninger.
- **Gevinsten drives av at A-klassen får mer plass og at to over­dimensjonerte volum­varer (A3, A4) gir fra seg plass.** Reduksjon av lavt-presterende C-SKUer er nødvendig sortiments­hygiene, men ikke hovedmekanismen.
- Margin-vektingen flytter hovedanbefalingen mot SKUer på øvre del av margin­spennet (≈ 55 %) over rene volum-vinnere som ligger lavere i marginspennet. Volumet (+54 %) er likevel tett på margin-veksten (+50 %), fordi A-klassen domineres av høy-utnyttelse-SKUer på tvers av margin­spennet.
- Spredningen mellom S1, S2 og S3 (25–50 % margin-gevinst) angir båndet av rimelige estimater. Hovedanbefalingen er **S2**: +49,8 % margin-vektet salg med intakt sortiment (alle 34 SKUer beholdt på minst 3 facings) og 3 sekundær­plasser dirigert til de mest produktive A-SKUene.
- Sensitivitets­analysen viser at resultatet er robust mot den usikre etterspørsels­antakelsen — selv 1,25× multiplier gir +17 %.

---

## 8 Diskusjon

Dette kapitlet tolker funnene fra §7 mot det teoretiske rammeverket som introduseres i §3, vurderer styrker og svakheter ved modell og data, og drøfter praktiske implikasjoner for butikken. Vi presenterer ingen nye analyser her; alle tall er hentet fra §7.

### 8.1 Tolkning i lys av teori

**Reallokering følger space-elasticity-intuisjonen.** Det sentrale teoretiske bidraget fra Curhan og videre arbeid omkring space elasticity er at salg per produkt øker med tildelt hylleplass inntil etterspørselen er mettet, med avtakende marginalavkastning. Modellen vår antar en forenklet, lineær produktivitetsfunksjon $\rho_i \cdot x_i$, men lander likevel på en anbefaling som rimer med denne intuisjonen: A-produktene med høyest observert produktivitet per facing (§5.2, Tabell 5.2.1) er også de som tildeles mest ny plass. Resultatet er konsistent med det teoretisk forventede — hylleplass skal flyttes dit den marginale salgsavkastningen er høyest.

**Gevinsten kommer fra omfordeling, ikke fra eliminering.** Scenario­sammenlikningen (§7.1) viser at S1 (kun primær­omfordeling) henter +49,5 % margin-gevinst og S2 (med 3 sekundær­plasser) +49,8 % — sekundær­eksponeringen bidrar bare med en margin-prosent ekstra. Sortiments­hygienen — å redusere C-SKUer til 1 kolli — står for under 6 % av gevinsten. Hovedmekanismen er at to over­dimensjonerte A-SKUer (A3 og A4 med utnyttelse rundt 0,7–1,0) gir fra seg betydelig hylleplass til 12 underdimensjonerte A-SKUer. Det rimer med funn fra retail-litteraturen om at etablerte planogrammer ofte har inertia; frontfacings reflekterer historiske avtaler eller konvensjoner snarere enn aktuell etterspørsel.

**Margin-vektingen prioriterer riktig type produkt.** Sammenligning mellom margin-vektet og rent volum-basert målfunksjon viser at modellen velger samme generelle struktur (A-klasse vokser, C-klasse faller) — men SKUer på øvre del av margin­spennet (≈ 55 %) prioriteres marginalt høyere enn volum-vinnere på nedre del av spennet (≈ 30 %). For leverandøren er dette økonomisk meningsfullt: hyllen brukes for å maksimere bruttomargin, ikke bare antall enheter solgt.

**A-klasseproduktenes dobling av plass har en grense.** De fleste A-SKUene ender i S2 med presis det antall facings som metter deres antatte etterspørsel ($x_i = d_i / \rho_i$). Uten en `overserve_factor` som overstiger 1 ville de ikke fått økt plass. Det betyr at anbefalingen står og faller med at den observerte etterspørselen er undervurdert; dette adresseres eksplisitt i §8.2.

### 8.2 Begrensninger og usikkerhet

**B1. Deterministisk og periodegjennomsnittlig modell.** Modellen behandler uken som én beslutningsperiode og bruker gjennomsnittlig ukesalg som parameter. Reell drift er stokastisk: etterspørsel varierer fra uke til uke (Tabell 5.2.1 viser CoV mellom 0,10 og 0,49 per produkt) og innen uke mellom dager og tider. En stokastisk reformulering — med etterspørsel som tilfeldig variabel og service-level-restriksjoner i stedet for harde kapasitetsgrenser — ville gitt et mer realistisk bilde av sannsynligheten for at hyllen går tom. Denne forenklingen er akseptabel for et konseptbevis, men bør flagges før anbefalingen tas i bruk.

**B2. Lineær produktivitet.** Antagelsen $y_i \le \rho_i \, x_i$ sier at hver ekstra facing gir samme antall solgte enheter som den første. I praksis er det sannsynlig at space-elastisiteten er avtagende — den tiende facingen gir mindre salg enn den første. Uten eksperimentelle data (variasjon i kapasitet over tid) kan vi ikke estimere elastisiteten empirisk i dette prosjektet. Konsekvensen er at modellens gevinst antagelig er et *øvre* estimat; den reelle løftet fra doblet plass er trolig lavere enn 100 %.

**B3. Skjult etterspørsel og out-of-stock.** For produkter med observert utnyttelse > 1 er det sanne etterspørselsnivået ikke direkte målbart: ethvert salg som skulle skjedd etter at hyllen ble tom og før neste etterfylling er usynlig i dataene. I hovedscenariet antas etterspørselen å være 2× observert salg, en størrelsesorden som reflekterer erfaringstall fra retail, men som ikke er empirisk forankret i dette datasettet. Sensitivitetsanalysen (§7.3) demper risikoen noe ved å vise at selv 1,25× gir meningsfull gevinst, men tallet er fortsatt en antakelse.

**B4. Én butikk, 10 uker.** Datasettet omfatter én fysisk butikk og en periode på ti uker (uke 06–15 2026). Sesongvariasjoner, kampanjeuker eller eksterne hendelser kan ha påvirket datagrunnlaget uten at vi kan korrigere for det. Spesielt A2-observasjonen i uke 15 (412 enheter, mer enn dobbelt av gjennomsnittet for produktet) ble ikke fjernet som avviker fordi vi ikke har grunnlag for å hevde at den er en målefeil — det er sannsynligvis en kampanjeuke eller en uventet etterspørselspulje. En replikasjon på flere butikker og over lengre periode ville styrket grunnlaget for generalisering.

**B5. Margin er bruttomargin, ikke dekningsbidrag.** Vekten $m_i$ er leverandørens bruttomargin per enhet basert på leverandørens egen marginrapportering. Den fanger ikke leverandørens interne kostnader (logistikk, kampanjebidrag, hyllebetaling), markedsførings­tilskudd til kjeden, eller variabel pris­elastisitet på tvers av kampanjeperioder. En profitt­maksimerende variant med fullt dekningsbidrag per SKU ville gitt en mer økonomisk presis anbefaling — spesielt på tvers av margin­spennets ytterpunkter, der den faktiske dekningsbidrag­fordelingen kan være mer komprimert i praksis enn brutto­marginen antyder.

**B6. Ingen kryssalgseffekter eller kannibaliserings-modellering.** Modellen behandler hvert produkt uavhengig. I praksis kan en kraftig reduksjon av A4 flytte salg over til A3 (samme produktundergruppe) — kannibalisering som ikke er modellert. Tilsvarende kan en kraftig økning i A1 fortrenge salg i andre SKUer i samme drikke­kategori. Kvantifisering av slike effekter krever paneldata med eksponert kapasitets­variasjon og utgår for dette prosjektet.

**B7. Sekundær­eksponerings­faktoren $k = 1{,}5$ er hentet fra litteraturen, ikke estimert i caset.** Chevalier (1975) og Nordfält & Ahlbom (2018) finner sekundær­plassers løft i størrelses­orden 1,3–2,0× primær­produktivitet, men variasjonen mellom kategorier og butikk­typer er stor. I S2 dominerer primær­omfordelingen uansett, så $k$ påvirker resultatet bare marginalt. Ved utvidede sekundær­budsjett (for eksempel 10–15 plasser) ville $k$-valget hatt større betydning og burde estimeres empirisk gjennom et kontrollert forsøk.

### 8.3 Implikasjoner for leverandørens forhandlings­posisjon

Sett fra leverandørens perspektiv er hovedfunnet at egen portefølje sannsynligvis ikke står optimalt allokert innenfor den hyllerammen leverandøren allerede disponerer. S3 (konservativ) indikerer minst +25 % ukentlig margin-vektet sell-out bare ved intern omfordeling, og hovedanbefalingen S2 gir +50 % margin og +54 % i volum. Dette er tall leverandøren kan bringe med seg inn i neste kategori­besøk som dokumentert grunnlag for å endre planogrammet.

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

Svaret, basert på analyse av leverandørens samlede 34-SKU-portefølje hos Coop Extra X, er:

- **Under- og overallokerte SKUer kan identifiseres rutinemessig** gjennom et enkelt utnyttelsesmål (gjennomsnittlig ukentlig sell-out dividert på hylleallokering) kombinert med en ABC-klassifisering. I datasettet er 24 av 34 SKUer underdimensjonerte og 10 over­dimensjonerte; mismatchen er gjennomgripende, ikke begrenset til enkeltprodukter.
- **Reallokerings­potensialet innen leverandørens portefølje er betydelig.** En deterministisk margin-vektet LP-modell som omfordeler leverandørens kontraktuelle hylleramme gir mellom +25 % og +50 % i forventet ukentlig margin-vektet sell-out — avhengig av antagelser om skjult etterspørsel og sortiments­gulv. Hovedanbefalingen (S2 Primær + sekundær) gir +49,8 % margin-vekst og +54 % volumvekst med intakt sortiment (alle 34 SKUer beholder minst 3 facings).
- **Gevinsten er robust.** Sensitivitets­analysen viser at selv ved konservative antagelser (1,25× skjult etterspørsel) ligger volum­gevinsten på +17 % over observert baseline. Resultatet er også nærmest flatt mot minimums-sortimentsparameteren opp til 0,40, noe som gir leverandøren operasjonelt spillerom for å forhandle om strengere sortiments­gulv uten å miste vesentlig av argumentet.
- **Sekundær­eksponering bidrar marginalt på toppen av primær­omfordelingen** ved nåværende sekundær­budsjett (3 plasser), men gir et nyttig forhandlings­argument: modellen utpeker presist hvilke 2–3 SKUer som har høyest marginal lønnsomhet ved sekundær­plassering.
- **Scope gir metoden naturlig skalerbarhet.** Siden modellen bare krever data leverandøren allerede disponerer — sell-out per SKU, egen hylleallokering og brutto­margin per SKU — kan samme analyse kjøres på flere butikker, tidsperioder og porteføljer uten å forutsette kategoriovergripende informasjon.

**Praktiske implikasjoner.** Metoden gir leverandøren et kvantitativt argument som kan brukes direkte i JBP- og kategori­besøk. I stedet for å argumentere for "mer plass" generelt, dokumenterer leverandøren et konkret reallokerings­forslag innenfor eksisterende hylleramme. Siden forslaget ikke krever utvidet plass, senker det forhandlings­friksjonen og øker sannsynligheten for at kjeden aksepterer endringen — i det minste som en delvis utrulling med oppfølgende måling.

**Forslag til videre forskning.** Tre naturlige utvidelser er identifisert: (i) *stokastisk reformulering* som eksplisitt håndterer variasjon i sell-out og gir service-level-garantier i stedet for harde kapasitets­grenser; (ii) *økonomisk vekting* der målfunksjonen maksimerer dekningsbidrag fremfor enheter, betinget av at margintall kan innhentes fra leverandørens egne systemer; (iii) *empirisk estimering av space-elastisitet* gjennom et kontrollert forsøk hos leverandørens butikker, der forslag fra modellen implementeres på noen butikker og sell-out-responsen måles mot kontrollbutikker. Replikasjon på tvers av butikker og kategorier vil også styrke grunnlaget for generalisering.

Studien demonstrerer at en konseptuelt enkel margin-vektet LP-modell, matet med den datatypen en leverandør realistisk disponerer (sell-out, egen hylleallokering og bruttomargin per enhet), er tilstrekkelig for å identifisere kvantifiserbare reallokerings­potensialer. Modellens verdi ligger ikke i presisjonen av det estimerte prosent­løftet, men i at den gjør leverandørens kontraktuelle hylle­situasjon målbar mot egen sell-out og margin — et utgangspunkt for kategori­dialog som i dag ofte mangler tallfestet underlag.

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
- `aktiviteter/3_5_analyse_og_resultater/scripts/05_sensitivitet_heatmap.py` (2D rutenett)
- `aktiviteter/3_5_analyse_og_resultater/scripts/06_pipeline_diagram.py` (Graphviz)
- `aktiviteter/3_5_analyse_og_resultater/scripts/07_sankey_omfordeling.py` (Plotly Sankey)

Avhengigheter er definert i `006 analysis/pyproject.toml`. Hele pipelinen reproduseres med `uv sync` etterfulgt av de fire kommandolinjene dokumentert i `006 analysis/README.md`.

**Vedlegg B — Pseudonymregister.** Koblingen mellom pseudonymer (A1, A2, B1, B2, C1–C4) og reelle produktnavn er oppbevart lokalt i `006 analysis/aktiviteter/3_3_casebeskrivelse_og_datainnsamling/resultat/intern/navneregister.csv`. Denne filen er unntatt versjonering og deles ikke utenfor prosjektgruppen, i henhold til taushetserklæringen med Coop Extra X.

**Vedlegg C — Taushetserklæring.** Underskrevet taushetserklæring mellom prosjektgruppen og Coop Extra X er arkivert utenfor dette repoet i henhold til kjedens instruks. Mal er tilgjengelig i `000 templates/Taushetsærklæring.docx`.

**Vedlegg D — Rådata.** Rådata som ligger til grunn for analysen, `Data 10 uker.csv`, oppbevares lokalt i `004 data/` og er unntatt versjonering. Alle avledede datasett med reelle produktnavn oppbevares tilsvarende under `intern/`-underfoldere som er ekskludert i `.gitignore`.

