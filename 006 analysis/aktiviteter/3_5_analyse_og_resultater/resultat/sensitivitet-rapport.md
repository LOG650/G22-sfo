# Sensitivitetsanalyse (anonymisert)

Baseline observert total: **946.0** enheter/uke.

## Etterspørselsantakelse — overserve_factor

Hvor mye høyere antas ukentlig etterspørsel å være enn observert salg for produkter der hyllen tømmes? x_min_fraction holdes på 0.25 (S2).

| overserve_factor | LP-salg | Gevinst | Gev % |
|---:|---:|---:|---:|
| 1.25 | 1098.0 | +152.0 | +16.1% |
| 1.50 | 1245.8 | +299.8 | +31.7% |
| 1.75 | 1391.7 | +445.7 | +47.1% |
| 2.00 | 1524.1 | +578.1 | +61.1% |
| 2.50 | 1783.9 | +837.9 | +88.6% |
| 3.00 | 2045.8 | +1099.8 | +116.3% |

## Minimums-allokering — x_min_fraction

Hvor streng er sortimentsgarantien? overserve_factor holdes på 2.0 (S2).

| x_min_fraction | LP-salg | Gevinst | Gev % |
|---:|---:|---:|---:|
| 0.00 | 1541.0 | +595.0 | +62.9% |
| 0.10 | 1536.0 | +590.0 | +62.4% |
| 0.25 | 1524.1 | +578.1 | +61.1% |
| 0.40 | 1513.1 | +567.1 | +59.9% |
| 0.50 | 1505.3 | +559.3 | +59.1% |
| 0.60 | 1498.5 | +552.5 | +58.4% |
| 0.80 | 1477.6 | +531.6 | +56.2% |

## Tolkning

- Gevinsten vokser monotont med overserve_factor fordi høyere antatt etterspørsel hever taket d_i for de underkapasiterte A-produktene. Selv ved konservativ antakelse (1.25×) gir modellen betydelig forbedring.
- Minimums-allokering har liten effekt inntil den begynner å binde B2 (≈ 0.30–0.40). Over dette tvinges modellen til å beholde overkapasitert hylleplass og mister gevinst.
- S2 Realistisk (0.25, 2.0) ligger i det monotone området der hovedparten av gevinsten er realisert uten å kutte sortimentet.