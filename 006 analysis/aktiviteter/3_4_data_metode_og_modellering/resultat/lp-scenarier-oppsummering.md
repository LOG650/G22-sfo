# LP-scenarier — oppsummering (margin-vektet) (anonymisert)

Baseline margin-vektet salg: **846.9**.
Målfunksjon = Σ (margin_i × forventet_salg_i). Marginprosent = leverandørens brutto margin per enhet fra prislisten til Coop.

| Scenario | Beskrivelse | LP-margin | Gevinst | Gev % |
|---|---|---:|---:|---:|
| S1 Primær-omfordeling | Reallokering kun innen primær hylle, x_min = 1 kolli per SKU (3 facings × Dybde_i), 2× etterspørsel, ingen sekundæreksponering. | 1187.8 | +340.9 | +40.3% |
| S2 Primær + sekundær | Hovedanbefaling: primær-omfordeling pluss 3 sekundærplasser som tildeles mest effektive SKUer. k = 1.5× primær-effektivitet. x_min = 1 kolli per SKU. | 1190.9 | +344.0 | +40.6% |
| S3 Konservativ | Konservativ: x_min = max(50 % av dagens allokering, 1 kolli), 1.5× etterspørsel, ingen sekundæreksponering. | 1020.2 | +173.3 | +20.5% |
| S4 Implementerbar | Som S2, men hver SKU er begrenset til ±50 % av dagens hyllekapasitet. Speiler hva som er praktisk gjennomførbart i én forhandlingsrunde uten store omstillinger i butikkdriften. | 1039.9 | +193.0 | +22.8% |