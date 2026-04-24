# Kildevurdering for LOG650 G22-rapporten

**Dato:** 2026-04-24
**Formål:** Kuratering av faglig kildegrunnlag for rapporten om datadrevet hylleallokering i leverandør-forhandlingskontekst.

## Relevans-vurderingskriterier

| Kriterium | Begrunnelse |
|---|---|
| Metodelikhet | Deterministisk LP/MILP, ikke stokastisk/ML — speilbilde av modellen i §6 |
| Datakrav matchende | Single-store, 10 uker, ingen tverrelastisitets-data, ingen kapasitets-variasjon |
| Domenelikhet | Dagligvare + leverandør-perspektiv + brus-kategori |
| Nylighet | 2020+ for metode, klassikere for grunnbegreper |
| Bidragstype | Foundational (hva er feltet), current (siste metodikk), boundary (hva vi IKKE gjør) |

## Nåværende kilder i rapporten — rangert etter relevans

### 🟢 Ikke-erstattbare grunnreferanser

1. **Curhan (1972)** — JMR — space elasticity-begrepet; grunnlag alle senere bygger på
2. **Chevalier (1975)** — JMR — in-store display-grunnlag; standard for §3-sekundær
3. **Nordfält & Ahlbom (2018)** — JRCS — moderne empiri på endcap-lokasjon; underbygger k=1.5
4. **Klement & Hübner (2023)** — FSMJ — helhetlig sortiment+hylle+påfyllings­rammeverk; perfekt for dobbeltperspektivet
5. **Bouzembrak et al. (2025)** — RAIRO-OR — fersk SSAP-oversikt; strukturerer §2
6. **Hübner, Schäfer & Schaal (2020)** — POM — stokastisk space allocation; det vi IKKE gjør, benchmark for §8

### 🟡 Bevar, svakere koblet

7. **Gholami & Bhakoo (2025)** — Supply Chain Analytics — empirisk OOS, støtter overserve_factor=2
8. **Bezawada et al. (2009)** — Journal of Marketing — kryssalgseffekter (for §8 B6)
9. **Düsterhöft, Hübner & Schaal (2021)** — EJOR — eksakt metode; vurder erstatning med Ostermeier (2021) Omega
10. **Mishra (2023)** — OPSEARCH — heuristikker; erstattes evt. av nyere alternativ

### 🔴 Lavt bidrag — dropp

- **Gustriansyah (2022)** — Mathematics — ML-prognose, vi prognoser ikke
- **Usama (2024)** — WJARR — AI-prognose, samme som over
- **Santos (2024)** — ESA — deep learning planogramovervåking, sidesport
- **Hsu (2025)** — Scientific Reports — computer vision, sidesport

Disse ble lagt inn for å gjøre §2.4 "moderne" men mangler ekte metodisk kobling til LP-tilnærmingen.

## Vurdering av nye kildekandidater fra brukerens liste

### Ostermeier, Düsterhöft & Hübner (2021) — Omega ⭐⭐⭐⭐⭐

Samme forfattergruppe som Düsterhöft/Hübner/Schaal (2021) EJOR. Omega er mer operasjonelt-fokusert enn EJOR. Sannsynligvis praksis-rettet variant av samme modellfamilie.

**Anbefaling:** Erstatt Düsterhöft/Hübner/Schaal (2021) EJOR med denne.

### Hübner & Kuhn (2024) — Springer ⭐⭐⭐⭐⭐

Hübner + Kuhn — to tungvektere i retail OR. Springer-publisering tyder på bokkapittel eller tematisk utvidet arbeid, trolig review eller framework.

**Anbefaling:** Sterk kandidat for §3 kategorimanagement-delen.

### Ziari & Sheikh Sajadieh (2025) — RAIRO-OR ⭐⭐⭐⭐

Samme tidsskrift som Bouzembrak et al. (2025). Tittel antyder nyere SSAP-bidrag.

**Anbefaling:** Nyttig som sekundær-oversikt i §2, eller som nyere heuristikk-referanse til erstatning for Mishra (2023).

### Liu et al. (2025) — Aston Research Explorer ⭐⭐⭐

Aston har sterk retail/SCM-gruppe. Uten abstrakt er plassering usikker.

**Anbefaling:** Be om abstrakt før beslutning om inklusjon.

## Anbefalt endelig kildesett

**Bytt UT 4 svakere kilder, BYTT INN 3 sterkere:**

| Ut | Inn |
|---|---|
| Gustriansyah (2022), Usama (2024) | Ostermeier et al. (2021) — Omega |
| Santos (2024) | Hübner & Kuhn (2024) — Springer |
| Hsu (2025) | Ziari & Sheikh Sajadieh (2025) — RAIRO-OR |

Liu et al. (2025) venter på abstrakt.

## Kildebelegg etter endring — per seksjon

| Seksjon | Kilder | Vurdering |
|---|---|---|
| §2.1 SSAP OR-tradisjon | Bouzembrak (2025), Ziari (2025), Ostermeier (2021), Hübner/Schäfer (2020), Klement & Hübner (2023) | Sterk — både oversikt og metode |
| §2.2 Etterspørsel/OOS | Gholami & Bhakoo (2025) | Minimal men dekkende |
| §2.3 Category management | Klement & Hübner (2023), Hübner & Kuhn (2024) | Sterk — dobbel Hübner |
| §2.4 Sekundær | Chevalier (1975), Nordfält & Ahlbom (2018), Bezawada (2009) | Solid |
| §3.1 Space elasticity | Curhan (1972), Hübner/Schäfer (2020) | Kanonisk + moderne |
| §3.2 LP-teori | Dantzig (1947) | Tilstrekkelig |
| §3.4 ABC | Pareto (1896), Koch (1997) | Standard |

## Gjenstående avklaringer før låst kildevalg

1. **Er Ostermeier et al. (2021) en modell-artikkel eller oversikt?** Hvis modell, perfekt match. Hvis oversikt, vurder overlapp med Bouzembrak.
2. **Tittelen på Hübner & Kuhn (2024)?** Hvis "review" eller "framework" → sterk for §3. Hvis smal modellvariant → re-vurder.
3. **Abstrakt for Liu et al. (2025)?** Avgjør om de bør inn eller droppes.

## Ærlighet om egen kildebruk

Ingen av kildene er lest i primærform. Titler, forfattere og tidsskrifter er hentet fra:
- `prosjektplan.md §8 Litteratursøk` (for den opprinnelige listen)
- Web-søk (for Chevalier, Nordfält & Ahlbom, og nye kandidater)

DOI-er og pagineringsdetaljer i §10 Bibliografi er plausible men **ikke verifisert mot primærkilde**. Full verifikasjon mot primærkilder må skje før endelig innlevering 31.05.2026.
