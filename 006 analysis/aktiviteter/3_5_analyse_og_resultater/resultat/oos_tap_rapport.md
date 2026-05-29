# OOS-tap ex post — leverandørens portefølje hos Coop Extra X

Estimerer hvor mye margin-vektet salg leverandøren *taper hver uke* på grunn av out-of-stock (utnyttelse > 1,0) i dagens hyllekonfigurasjon. Beregnet før LP-omfordeling — dvs. tapet som *forsvinner* hvis anbefalingen i §7 implementeres.

**Baseline margin-vektet salg:** 846.9 per uke

## Oppsummering på tvers av antagelser

| Antagelse | overserve | OOS-SKUer | Tapt enh./uke | Tapt margin/uke | Andel av baseline |
|---|---:|---:|---:|---:|---:|
| hovedscenario | 2.00 | 24 | 1860.8 | 734.1 | 86.7% |
| konservativ | 1.50 | 24 | 930.4 | 367.0 | 43.3% |

**Tolkning:** OOS-tap-tallet er av samme størrelsesorden som LP-gevinsten (jf. §7). Det styrker E1 (mismatch er reell) med en *kostnadssize*: leverandøren mister allerede betydelig margin på dagens hylle.

## Per-SKU tap (hovedscenario, overserve = 2.0)

| SKU | Utnyttelse | Snittsalg | d_i | Tapt enh./uke | Margin | Tapt margin/uke |
|---|---:|---:|---:|---:|---:|---:|
| A1 | 6.62 | 417.0 | 834.0 | 417.0 | 30% | 125.10 |
| A2 | 9.10 | 191.0 | 382.0 | 191.0 | 55% | 105.05 |
| A3 | 1.01 | 148.0 | 296.0 | 148.0 | 55% | 81.40 |
| A6 | 3.72 | 78.2 | 156.4 | 78.2 | 55% | 43.01 |
| A7 | 3.70 | 77.8 | 155.6 | 77.8 | 50% | 38.90 |
| A5 | 2.62 | 109.9 | 219.8 | 109.9 | 30% | 32.97 |
| A11 | 2.82 | 59.3 | 118.6 | 59.3 | 55% | 32.62 |
| A10 | 2.87 | 60.2 | 120.4 | 60.2 | 50% | 30.10 |
| B2 | 2.29 | 96.2 | 192.4 | 96.2 | 30% | 28.86 |
| A8 | 1.74 | 73.1 | 146.2 | 73.1 | 30% | 21.93 |
| A9 | 3.42 | 71.9 | 143.8 | 71.9 | 30% | 21.57 |
| A12 | 2.73 | 57.4 | 114.8 | 57.4 | 30% | 17.22 |
| A13 | 2.73 | 57.3 | 114.6 | 57.3 | 30% | 17.19 |
| A14 | 2.31 | 48.6 | 97.2 | 48.6 | 30% | 14.58 |
| B1 | 2.31 | 48.5 | 97.0 | 48.5 | 30% | 14.55 |
| B7 | 1.20 | 25.2 | 50.4 | 25.2 | 55% | 13.86 |
| B8 | 1.13 | 23.7 | 47.4 | 23.7 | 55% | 13.04 |
| B9 | 1.13 | 23.7 | 47.4 | 23.7 | 55% | 13.04 |
| C1 | 1.95 | 23.4 | 46.8 | 23.4 | 55% | 12.87 |
| B3 | 2.04 | 42.9 | 85.8 | 42.9 | 30% | 12.87 |
| B4 | 1.80 | 37.7 | 75.4 | 37.7 | 30% | 11.31 |
| C3 | 1.28 | 20.6 | 41.1 | 20.6 | 55% | 11.31 |
| B5 | 1.74 | 36.6 | 73.2 | 36.6 | 30% | 10.98 |
| B6 | 1.55 | 32.6 | 65.2 | 32.6 | 30% | 9.78 |

**Topp 5 SKUer står for 54% av samlet OOS-tap** (A1, A2, A3, A6, A7).

## Tolkning i forhandlingsdialog

- Tallet er en *ex post*-kalkyle: hva mister leverandøren *i dag*, før noen omfordeling.
- Det er sammenlignbart med LP-gevinsten i §7 — begge er margin-enheter per uke.
- Antagelsen om skjult etterspørsel (overserve 1,5–2,0) er den samme som modellen bygger på; sensitiviteten her speiler §7.3.
- Hovedfunnet i §7.5 (mismatch er gjennomgripende) underbygges av at tapet er konsentrert hos få A-klasse-SKUer, ikke spredt utover porteføljen.