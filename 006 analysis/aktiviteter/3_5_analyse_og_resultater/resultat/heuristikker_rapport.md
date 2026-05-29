# Heuristikk-benchmark mot LP S2

Fire enkle allokeringsregler sammenlignet med LP-hovedanbefalingen (S2). Formålet er å kvantifisere hva LP-optimeringen *legger til* utover sunn fornuft.

- **Baseline (dagens hyllekonfigurasjon)**: margin 846.9, volum 2080
- **LP S2 (hovedanbefaling)**: margin 1190.9, volum 3024 (+40.6% margin)

## Sammenligning

| Regel | Margin | Δ vs baseline | Volum | LP-gap (pp) |
|---|---:|---:|---:|---:|
| H1 Prop-salg | 1065.7 | +25.8% | 2650 | +14.8 |
| H2 Prop-margin×salg | 1043.0 | +23.2% | 2515 | +17.5 |
| H3 ABC-flatt 80/15/5 | 1045.8 | +23.5% | 2503 | +17.1 |
| H4 Behold dagens | 846.9 | +0.0% | 2080 | +40.6 |
| **LP S2** | **1190.9** | **+40.6%** | **3024** | **0** |

**LP-gap** = avstand fra heuristikken til LP-optimum i prosentpoeng på margin-gevinsten. Lavt gap betyr at heuristikken er nesten like god som LP.

## Tolkning

- **Beste heuristikk**: *H1 Prop-salg* med +25.8% margin-gevinst. LP-gap: 14.8 prosentpoeng.
- LP-løftet utover beste heuristikk er **betydelig** (14.8 pp). Optimeringen henter ut gevinst som enkle regler ikke fanger — særlig håndtering av minimumssortiment, sekundærplasser og demand-cap simultant.
- Behold-dagens (H4) representerer baseline; differansen til H1–H3 viser hva *enkel omfordeling* alene gir.

## Allokering per SKU (alle regler + LP)

| SKU | Dagens | H1 Prop-salg | H2 Prop-margin×salg | H3 ABC-flatt 80/15/5 | H4 Behold dagens | LP S2 |
|---|---:|---:|---:|---:|---:|---:|
| A1 | 63 | 94 | 75 | 42 | 63 | 126 |
| A10 | 21 | 32 | 34 | 43 | 21 | 42 |
| A11 | 21 | 31 | 35 | 42 | 21 | 42 |
| A12 | 21 | 31 | 28 | 42 | 21 | 42 |
| A13 | 21 | 31 | 28 | 42 | 21 | 42 |
| A14 | 21 | 30 | 27 | 26 | 21 | 39 |
| A2 | 21 | 54 | 66 | 42 | 21 | 42 |
| A3 | 147 | 47 | 56 | 42 | 147 | 21 |
| A4 | 168 | 43 | 50 | 42 | 168 | 21 |
| A5 | 42 | 40 | 35 | 42 | 42 | 84 |
| A6 | 21 | 35 | 40 | 42 | 21 | 42 |
| A7 | 21 | 35 | 38 | 42 | 21 | 42 |
| A8 | 42 | 34 | 30 | 42 | 42 | 21 |
| A9 | 21 | 34 | 30 | 42 | 21 | 42 |
| B1 | 21 | 29 | 27 | 26 | 21 | 21 |
| B2 | 42 | 38 | 33 | 42 | 42 | 21 |
| B3 | 21 | 28 | 27 | 26 | 21 | 21 |
| B4 | 21 | 28 | 26 | 26 | 21 | 21 |
| B5 | 21 | 27 | 26 | 26 | 21 | 21 |
| B6 | 21 | 27 | 25 | 26 | 21 | 21 |
| B7 | 21 | 25 | 27 | 26 | 21 | 21 |
| B8 | 21 | 25 | 27 | 26 | 21 | 21 |
| B9 | 21 | 25 | 27 | 26 | 21 | 21 |
| C1 | 12 | 22 | 24 | 23 | 12 | 21 |
| C10 | 21 | 23 | 23 | 23 | 21 | 21 |
| C11 | 21 | 22 | 22 | 23 | 21 | 21 |
| C2 | 28 | 24 | 26 | 23 | 28 | 21 |
| C3 | 16 | 28 | 29 | 26 | 16 | 32 |
| C4 | 21 | 24 | 24 | 23 | 21 | 21 |
| C5 | 24 | 27 | 27 | 26 | 24 | 24 |
| C6 | 21 | 22 | 22 | 23 | 21 | 21 |
| C7 | 12 | 19 | 20 | 20 | 12 | 18 |
| C8 | 21 | 22 | 22 | 23 | 21 | 21 |
| C9 | 21 | 23 | 23 | 23 | 21 | 21 |