# 1. Introduksjon

I moderne dagligvarehandel er hylleplass en av de mest begrensede og kostbare ressursene. Effektiv forvaltning av denne plassen, ofte referert til som *space management*, er avgjørende for butikkens lønnsomhet og kundeopplevelse. Tradisjonelt baseres hylleallokering (planogrammer) på overordnede kategoristrategier og avtaler med leverandører. Imidlertid viser praksis ofte et misforhold mellom den tildelte plassen og den faktiske etterspørselen i den enkelte butikk.

Når produkter med høy omløpshastighet har for liten hyllekapasitet, øker risikoen for tomme hyller (*out-of-stock*), noe som fører til tapt salg og redusert kundetilfredshet. Samtidig beslaglegges verdifull plass av produkter med lavere etterspørsel. Ved å ta i bruk datadrevne metoder og kvantitativ optimalisering, kan detaljister bevege seg fra generiske planogrammer til butikkspesifikke løsninger som reflekterer lokalt salgsmønster. Dette prosjektet utforsker hvordan lineær programmering kan benyttes for å identifisere og utbedre slike skjevfordelinger i en operasjonell kontekst.

## 1.1 Problemstilling og forskningsmål

Hovedformålet med dette prosjektet er å utvikle en kvantitativ modell som kan evaluere og optimalisere hylleallokering basert på faktiske salgsdata. Med utgangspunkt i Coop Extra X som caseselskap, skal prosjektet besvare følgende problemstilling:

> *Hvordan kan en datadrevet tilnærming identifisere produkter som er underallokert i hylleplass relativt til observerte salgsdata, og hva er det estimerte potensialet for forbedring ved reallokering av eksisterende hyllekapasitet innen en avgrenset varekategori i Coop Extra X?*

For å besvare problemstillingen er det definert følgende forskningsmål:
1. Kartlegge nåværende hyllekapasitet mot faktisk etterspørsel for å identifisere kapasitetsavvik.
2. Formulere og implementere en optimaliseringsmodell i Python som maksimerer forventet omsetning gitt fysiske kapasitetsbegrensninger.
3. Kvantifisere det økonomiske og operasjonelle forbedringspotensialet ved en foreslått reallokering sammenlignet med dagens situasjon.

## 1.2 Avgrensninger

For å sikre tilstrekkelig dybde i den kvantitative analysen innenfor prosjektets tidsrammer, er det gjort følgende faglige avgrensninger:

*   **Kontekstuell avgrensning:** Studien er begrenset til én spesifikk butikk (Coop Extra X) og én utvalgt varekategori. Dette muliggjør en detaljert analyse av lokale etterspørselsmønstre fremfor aggregerte nasjonale trender.
*   **Omfang av analyseobjekter:** Modellen inkluderer maksimalt 10 representative produkter (SKU-er) innen den valgte kategorien. Dette utvalget er tilstrekkelig for å demonstrere modellens logikk og interaksjonen mellom ulike produkter under felles kapasitetsbegrensninger.
*   **Modelltekniske forenklinger:** Faktorer som kampanjeaktivitet, sesongvariasjoner og prisendringer modelleres ikke eksplisitt. Studien fokuserer på den fundamentale sammenhengen mellom hylleplass (facings) og stabilt salg over tid.
*   **Operasjonell rekkevidde:** Prosjektet begrenser seg til å levere en teoretisk analyse og forslag til optimalisering. Fysisk implementering i butikk eller longitudinell testing av resultatene faller utenfor oppgavens omfang.

## 1.3 Oppgavens oppbygning

Rapporten er strukturert for å lede leseren gjennom hele den kvantitative forskningsprosessen. Etter introduksjonen presenterer kapittel 2 det teoretiske rammeverket knyttet til *space elasticity* og lineær programmering. Kapittel 3 gir en beskrivelse av caseselskapet og de relevante driftsprosessene. I kapittel 4 og 5 redegjøres det for datagrunnlaget og den matematiske formuleringen av optimaliseringsmodellen. Kapittel 6 presenterer resultatene fra modellkjøringene og sensitivitetsanalysen, etterfulgt av en diskusjon i kapittel 7 hvor funnene tolkes i lys av teori og praktiske implikasjoner. Oppgaven avsluttes med en konklusjon i kapittel 8 som besvarer problemstillingen direkte.
