# Sensitivitetsanalyse (anonymisert)

Baseline observert total: **2080.2** enheter/uke.

## Etterspørselsantakelse — overserve_factor

Hvor mye høyere antas ukentlig etterspørsel å være enn observert salg for produkter der hyllen tømmes? x_min_fraction holdes på 0.25 (S2).

| overserve_factor | LP-salg | Gevinst | Gev % |
|---:|---:|---:|---:|
| 1.25 | 2438.4 | +358.2 | +17.2% |
| 1.50 | 2746.9 | +666.7 | +32.1% |
| 1.75 | 3025.6 | +945.4 | +45.5% |
| 2.00 | 3265.1 | +1184.9 | +57.0% |
| 2.50 | 3620.3 | +1540.1 | +74.0% |
| 3.00 | 3905.9 | +1825.7 | +87.8% |

## Minimums-allokering — x_min_fraction

Hvor streng er sortimentsgarantien? overserve_factor holdes på 2.0 (S2).

| x_min_fraction | LP-salg | Gevinst | Gev % |
|---:|---:|---:|---:|
| 0.00 | 3341.5 | +1261.3 | +60.6% |
| 0.10 | 3326.3 | +1246.1 | +59.9% |
| 0.25 | 3265.1 | +1184.9 | +57.0% |
| 0.40 | 3184.5 | +1104.3 | +53.1% |
| 0.50 | 3115.4 | +1035.2 | +49.8% |
| 0.60 | 3029.0 | +948.8 | +45.6% |
| 0.80 | 2806.0 | +725.8 | +34.9% |

## Tolkning

- Gevinsten vokser monotont med overserve_factor fordi høyere antatt etterspørsel hever taket d_i for de underkapasiterte A-produktene. Selv ved konservativ antakelse (1.25×) gir modellen betydelig forbedring.
- Minimums-allokering har liten effekt inntil den begynner å binde B2 (≈ 0.30–0.40). Over dette tvinges modellen til å beholde overkapasitert hylleplass og mister gevinst.
- S2 Realistisk (0.25, 2.0) ligger i det monotone området der hovedparten av gevinsten er realisert uten å kutte sortimentet.