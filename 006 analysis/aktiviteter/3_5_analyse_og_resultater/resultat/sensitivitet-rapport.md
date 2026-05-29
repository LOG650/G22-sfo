# Sensitivitetsanalyse (anonymisert)

Baseline observert total: **2080.2** enheter/uke.

## Etterspørselsantakelse — overserve_factor

Hvor mye høyere antas ukentlig etterspørsel å være enn observert salg for produkter der hyllen tømmes? x_min_fraction holdes på 0.25 (S2).

| overserve_factor | LP-salg | Gevinst | Gev % |
|---:|---:|---:|---:|
| 1.25 | 2379.3 | +299.1 | +14.4% |
| 1.50 | 2655.1 | +574.9 | +27.6% |
| 1.75 | 2828.9 | +748.7 | +36.0% |
| 2.00 | 2969.7 | +889.5 | +42.8% |
| 2.50 | 3191.5 | +1111.3 | +53.4% |
| 3.00 | 3400.9 | +1320.7 | +63.5% |

## Minimums-allokering — x_min_fraction

Hvor streng er sortimentsgarantien? overserve_factor holdes på 2.0 (S2).

| x_min_fraction | LP-salg | Gevinst | Gev % |
|---:|---:|---:|---:|
| 0.00 | 3024.5 | +944.3 | +45.4% |
| 0.10 | 3024.5 | +944.3 | +45.4% |
| 0.25 | 2969.7 | +889.5 | +42.8% |
| 0.40 | 2887.3 | +807.1 | +38.8% |
| 0.50 | 2828.6 | +748.4 | +36.0% |
| 0.60 | 2762.2 | +682.0 | +32.8% |
| 0.80 | 2544.5 | +464.3 | +22.3% |

## Tolkning

- Gevinsten vokser monotont med overserve_factor fordi høyere antatt etterspørsel hever taket d_i for de underkapasiterte A-produktene. Selv ved konservativ antakelse (1.25×) gir modellen betydelig forbedring.
- Minimums-allokering har liten effekt inntil den begynner å binde B2 (≈ 0.30–0.40). Over dette tvinges modellen til å beholde overkapasitert hylleplass og mister gevinst.
- S2 Realistisk (0.25, 2.0) ligger i det monotone området der hovedparten av gevinsten er realisert uten å kutte sortimentet.