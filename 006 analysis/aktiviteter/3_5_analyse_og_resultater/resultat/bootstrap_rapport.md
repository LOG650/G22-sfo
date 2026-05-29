# Bootstrap-KI på S2-gevinsten

Empirisk fordeling av margin- og volum-gevinst i S2 over **B = 1000 bootstrap-iterasjoner**. Hver iterasjon resampler de 10 ukene i observasjonsperioden med tilbakelegging og kjører LP S2 på det re-aggregerte datagrunnlaget.

Gjennomsnittlig antall *unike* uker per iterasjon: **6.48 av 10** (rest er duplikater).

## Margin-gevinst (%)

| Statistikk | Verdi |
|---|---:|
| Punkestimat (full data) | **+40.6%** |
| Mean (bootstrap) | +40.9% |
| Median (bootstrap) | +40.8% |
| Standardavvik | 1.53 pp |
| 95 % konfidensbånd | [+38.7%, +44.4%] |
| 90 % konfidensbånd | [+38.9%, +43.8%] |
| Interkvartil (p25–p75) | [+39.7%, +41.8%] |

## Volum-gevinst (%)

| Statistikk | Verdi |
|---|---:|
| Punkestimat (full data) | **+45.4%** |
| Median (bootstrap) | +45.5% |
| 95 % konfidensbånd | [+43.3%, +48.5%] |

## Absolutte tall — LP-margin per uke

| Statistikk | LP-margin |
|---|---:|
| Median | 1193.4 |
| 95 % bånd | [1088.0, 1310.7] |

## Tolkning

- Hovedfunnet (+40.6 %) ligger nær median (40.8 %). Punktestimatet er ikke et utfall i tail-en — det er en typisk realisering under resampling.
- 95 %-båndet på **[+38.7%, +44.4%]** sier at selv ved ugunstig sampling av ukene som inngår, ligger gevinsten godt over null.
- Nedre kant av 95 %-båndet er over +10 %. **Gevinsten er statistisk robust mot sampling-variasjonen i 10-ukers vinduet** — selv om absoluttverdien fortsatt avhenger av modellantagelsene (β = 1, skjult etterspørsel = 2× observert) som drøftes i §8.2.
- Bootstrap fanger kun usikkerhet *innenfor* den observerte perioden. Generaliserbarhet til andre butikker, kategorier eller sesonger er et separat spørsmål som adresseres i §8.4.