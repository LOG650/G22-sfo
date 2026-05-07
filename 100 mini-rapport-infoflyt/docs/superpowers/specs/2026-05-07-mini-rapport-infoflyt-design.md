# Design-spec: Mini-rapport om informasjonsflyt i en FMCG-salgsorganisasjon

**Forfatter:** Sebastian V. Thunestvedt
**Dato:** 2026-05-07
**Status:** Spec — venter brukergodkjenning før implementasjonsplan
**Type:** Internt arbeidsdokument (utenfor LOG650)

---

## 1. Bakgrunn og problemstilling

Selger i en FMCG-/dagligvarekontekst forvalter en kundeportefølje som
besøkes gjentatte ganger. Kundebesøkene styrkes av oppdatert
informasjon — pris, kampanjer, listinger, lager, kundespesifikke
beslutninger. I dagens organisasjon flyter denne informasjonen
hovedsakelig fra **KAM-team** (~90 % av selgerens inngående info)
gjennom kaskaden:

```
KAM → Direktør → Regionssjef → Salgssjef → Selger
```

Resultatet er at kritisk informasjon ofte ankommer *etter* at kunden er
besøkt. Selgeren må enten besøke kunden på nytt (operativ kostnad) eller
tape troverdighet i relasjonen (relasjonell kostnad). Den siste
kostnaden er compound: hver gang en selger besøker samme A-kunde med
utdatert informasjon, eroderer det tilliten i en relasjon som er bygget
opp over år.

Mini-rapporten skal:

1. Dokumentere problemet sterkt og visuelt.
2. Forankre diagnosen i etablert litteratur (akademisk + praktiker).
3. Foreslå en alternativ informasjonsflyt-modell, porteføljebevisst og
   kundesentrisk.

## 2. Scope og avgrensning

**Inn:**

- Generisk B2B-FMCG-salgsorganisasjon i Norge / Norden.
- Selgerperspektivet (forfatterens egen rolle).
- Informasjon som flyter fra interne kilder (KAM, kategori, marketing,
  supply, execution-team) til selger.
- Både operativ pris (ekstra besøk) og relasjonell pris (tillit) som
  konsekvenser.

**Ut:**

- Ingen merkenavn eller selskapsnavn — generisk fremstilling.
- Ingen ekstern info-flyt (kunde → leverandør) utover det som er
  nødvendig for å motivere intern flyt.
- Ingen detaljert verktøy-evaluering (f.eks. Salesforce vs. Repsly).
  Kun referanse til at slike verktøy *eksisterer*.
- Ikke akademisk publisering — dette er et internt forslag, ikke en
  fagartikkel.

## 3. Målgruppe og tone

**Primær målgruppe:** Egen ledelse — salgssjef, regionssjef, eller
direktør i selgerens organisasjon.

**Tone:**

- Saklig, datadrevet, men personlig forankret.
- Selger-perspektivet i førsteperson i innledning og konklusjon.
- Akademisk forankring i midtkapitlene (litteratur + diagnose).
- *Modellen feiler, ikke menneskene.* Ingen anklager mot enkeltledere
  eller -funksjoner. KAM, salgssjef og direktør gjør jobben sin —
  systemet er underdimensjonert for hverdagen.
- Bruk litteraturens språk (bullwhip, anti-Challenger,
  customer-centric) for å gi leserne et felles vokabular.

## 4. Tese (hovedbudskap)

> Dagens kaskademodell (KAM → 4 ledd → selger) ble bygget for en stabil
> hverdag. I FMCG i 2026 er hverdagen for hektisk og kunderelasjonene
> for porteføljebaserte til at modellen leverer. Resultatet er ikke
> bare ekstra besøk — det er compound erosjon av tilliten i porteføljen.
> Løsningen finnes i etablert litteratur og modne verktøy, og kan
> innføres med differensierte tiltak per porteføljesegment.

## 5. Narrativ-bue (5 trekk)

1. **Smerten er konkret** — selger besøker kunde, KAM-info kommer
   dagen etter, ekstra besøk må til. Eksempelhistorie i innledningen.
2. **Smerten er ikke individuell, men strukturell** — bullwhip-
   analogien (Lee, Padmanabhan & Whang, 1997) viser at
   info-forvrengning gjennom ledd er en *forutsigbar* dynamikk.
3. **Smerten har en relasjonell pris** — Morgan & Hunt (1994) og
   Challenger-data (Dixon & Adamson, 2011): utdatert info bryter ned
   tillit, som er beholdningsverdien i porteføljen.
4. **Modellen er for smal til oppgaven** — Galbraith (1974, 2005) og
   Shah et al. (2006): hierarkiet leverer ikke nok båndbredde mot
   hektisk hverdag og krever lateral kobling + IT.
5. **Det finnes en alternativ modell** — porteføljebevisst,
   hub-and-spoke, differensiert push/pull. Modne verktøy finnes
   (TELUS, retail execution-segmentet, 18–25 % gevinst dokumentert).

## 6. Disposisjon

| § | Kapittel | Innhold | Figur | Sider |
|---|---|---|---|---|
| 1 | Innledning | Selger-perspektiv i 1. person; konkret smerte-anekdote; tese | — | 0,75 |
| 2 | Dagens modell (as-is) | Kaskaden KAM → 4 ledd → selger; mange kokker; tidsforsinkelse pr ledd | Fig. 1 swimlane | 1,25 |
| 3 | Litteraturramme | Bullwhip + boundary spanner + Galbraith + commitment-trust + Challenger | Fig. 2 bullwhip-analogi | 1,25 |
| 4 | Diagnose | Operativ pris (ekstra besøk, timer/uke) + relasjonell pris (tillit-erosjon) | Fig. 3 tillitskurve | 1,25 |
| 5 | Alternativ modell (to-be) | Porteføljedifferensiert info-flyt; hub-and-spoke; routing-logikk | Fig. 4 A/B/C-matrise + Fig. 5 to-be hub | 2 |
| 6 | Implementasjon + risiko | Skritt 1–3, raske gevinster, det vi *ikke* foreslår | — | 0,5 |
| 7 | Kilder | APA 7-referanseliste | — | 0,5 |

**Total:** 6–8 sider (avhengig av tetthet).

## 7. Visuell strategi (5 figurer)

| # | Figur | Hva den viser | Implementasjon |
|---|---|---|---|
| 1 | **Swimlane med tidsstempler** | Kaskaden KAM → 4 ledd → selger; piler med timer/dager forsinkelse | matplotlib + manuelle bokser/piler, eller graphviz → PNG |
| 2 | **Bullwhip-analogi** | Ren signal hos KAM, forvrengt hos selger gjennom ledd | matplotlib (linjer/kurver, syntetiske data) |
| 3 | **Tillits-/relasjonskurve** | Compound erosjon av tillit over n uoppdaterte besøk hos samme A-kunde | matplotlib (eksponensielt fall) |
| 4 | **Porteføljematrise** | A/B/C-segment × info-type; hva krever direkte ruting vs. push | matplotlib heatmap eller seaborn |
| 5 | **To-be info-arkitektur** | Hub-and-spoke — KAM som hub, selger med direkte tilgang via verktøy | matplotlib + bokser/piler, eller graphviz |

**Stil:**

- Norsk tekst i figurer.
- Kursiv figurtekst i markdown (`*Figur X. Beskrivelse.*`).
- 80 % sidebredde (samme konvensjon som LOG650-rapporten).
- Konsistent fargebruk: f.eks. matplotlib `tab10` eller en redusert
  palett (3–4 farger) for hele rapporten.

## 8. Tall og forankring

Hypotetiske kostnadstall brukes for å gjøre saken konkret. Modelleres
eksplisitt i rapporten med transparente forutsetninger:

- Antall selgere i orgen: f.eks. 50.
- Ekstra besøk pr. selger pr. uke pga. utdatert info: f.eks. 2.
- Tid pr. besøk inkl. reise: f.eks. 1,5 t.
- ⇒ 150 t/uke = 1 årsverk × 4 (eller tilsvarende kr-tall ved typisk
  timekost).
- Tillit-erosjon: konseptuell kurve, ikke empirisk; merkes tydelig som
  illustrativ.

Tallene brukes for å demonstrere størrelsesorden, ikke for å påstå
nøyaktighet.

## 9. Filstruktur

```
100 mini-rapport-infoflyt/
├── research/
│   └── kildekartlegging.md         (ferdig — 14 kilder, 7 narrativer)
├── docs/superpowers/specs/
│   └── 2026-05-07-mini-rapport-infoflyt-design.md   (denne spec)
├── rapport.md                       (hovedfil — markdown)
├── figurer/
│   ├── fig1_swimlane.py
│   ├── fig1_swimlane.png
│   ├── fig2_bullwhip.py
│   ├── fig2_bullwhip.png
│   ├── fig3_tillitskurve.py
│   ├── fig3_tillitskurve.png
│   ├── fig4_portefoljematrise.py
│   ├── fig4_portefoljematrise.png
│   ├── fig5_to_be_hub.py
│   └── fig5_to_be_hub.png
├── refs.bib                         (APA 7 BibTeX, 14 kilder)
├── output/
│   └── rapport.pdf                  (build-output, gitignored)
└── Makefile                         (make pdf — gjenbruker Eisvogel)
```

## 10. Verktøykjede

- **Python 3.12 + uv** (samme som LOG650-pipeline) for figurer
  (matplotlib, seaborn).
- **Pandoc** med Eisvogel-mal og APA 7 CSL — gjenbruker oppsettet i
  `000 templates/pandoc/eisvogel.latex` og `make pdf`-target som
  brukeren konfigurerte 2026-05-07.
- **TeX Live 2026** på `/Volumes/DevSSD/texlive/2026/` (xelatex, babel
  norsk).
- **Git** for versjonskontroll. Ingen sensitive data — kan committes
  fritt.

## 11. Litteraturgrunnlag

Kildekartlegging i `100 mini-rapport-infoflyt/research/kildekartlegging.md`
(utkast 2 — 14 kilder gruppert i 5 temaer):

1. Informasjonsforvrengning gjennom ledd
2. Selgeren som grenserolle
3. Organisasjonens informasjonsbehandling og KAM-koordinering
4. Sales enablement og retail execution i praksis
5. Kundesentrisitet, relasjonskvalitet og porteføljeperspektiv

Alle 14 kildene er DOI/URL-verifisert. APA 7-referanseliste i § 7 av
kildekartleggingen overføres til `refs.bib`.

## 12. Suksesskriterier

Mini-rapporten vurderes som vellykket om:

1. **En leser i ledelsen kan på 10 minutter:** forstå problemet,
   forstå hvorfor det oppstår strukturelt, og se hovedforslaget til
   løsning.
2. **Litteraturforankringen** er tydelig og APA 7-korrekt — leseren
   kan etterprøve hver påstand.
3. **Figurene står på egne ben** — en leser som blar gjennom figurene
   uten å lese teksten skjønner narrativ-buen.
4. **Forslagene er konkrete nok** til at neste skritt er åpenbart
   (hvem gjør hva, hva krever pilot, hva er rask gevinst).
5. **Tonen er ikke anklagende** — ledelsen får et språk og en
   diagnose, ikke en kritikk.

## 13. Begrensninger og det rapporten *ikke* gjør

- Ingen empirisk datainnsamling (ikke spørreundersøkelse, ikke
  intervju). Tall er hypotetiske og merkes som sådan.
- Ingen verktøy-shortlist eller leverandør-sammenligning.
- Ingen fullstendig endringsledelses-plan — bare hovedskritt og
  risikobetraktninger.
- Ingen organisatorisk redesign-anbefaling utover info-flyten —
  kaskaden er ikke nødvendigvis feil for *alle* prosesser, bare for
  hektisk markedsinformasjon.

## 14. Risiko og mitigering

| Risiko | Mitigering |
|---|---|
| Ledelsen leser dette som kritikk av KAM eller mellomledere | Eksplisitt ramme: "modellen, ikke menneskene". Honor mellom-leddenes funksjon i andre prosesser. |
| Tallene oppfattes som påstander om eksakt størrelse | Tydelig "modell-tall" / "illustrative" merking i alle kostnadsfigurer. |
| Bullwhip-analogien strekker seg for langt (forsyningskjede ≠ intern info) | Eksplisitt diskusjon av analogiens grenser i § 3. |
| Forslaget oppfattes som "kjøp et nytt verktøy" | Strukturér to-be-modellen som *organisatorisk + teknologisk* — verktøy er hjelp, ikke svar. |
| Rapporten blir for lang og mister fokus | Hard sidegrense 8 sider. Hvis innhold sprenger rammen → kutt heller eksempler enn poenger. |

## 15. Implementasjonsskritt (overordnet)

1. **Makefile + pandoc-oppsett** for `100 mini-rapport-infoflyt/` —
   gjenbruker Eisvogel-mal og CSL fra LOG650.
2. **`refs.bib`** — APA 7 BibTeX-poster for de 14 kildene.
3. **5 figurer** — Python-script + PNG-generering. Anbefalt rekkefølge:
   fig 2 (bullwhip, enklest), fig 3 (tillitskurve), fig 4 (matrise),
   fig 1 (swimlane), fig 5 (to-be hub).
4. **Skriv kapitler i denne rekkefølgen:** §3 litteratur (ankres mot
   ferdig kildekartlegging), §2 as-is, §4 diagnose, §5 to-be, §6
   implementasjon, §1 innledning, §7 kilder. (Innledning sist når man
   vet hva man har skrevet.)
5. **Bygg PDF** med `make pdf` og iterer.
6. **Sluttpolering** — språk, figurkonsistens, APA-sjekk, sidebryting.

Detaljert implementasjonsplan utarbeides i neste skritt
(`writing-plans`-skill).
