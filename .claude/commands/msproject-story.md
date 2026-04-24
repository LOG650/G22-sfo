---
description: Generer MS Project XML med løpende fremdrift opp til i dag (for faglærer-innlevering)
argument-hint: [YYYY-MM-DD eller "today"]
allowed-tools: Bash
---

Regenerer MSPDI XML med progressiv "løpende" fremdrift opp til en valgt dato (default: i dag). Dette gir MS Project-bildet faglærer forventer: aktiviteter er gjort etter hvert som tiden går, i stedet for alt-eller-ingenting status-hoppene i `schedule.json`.

Hva skjer:
- Aktiviteter som skulle vært ferdige før status-datoen: 100% med ActualStart + ActualFinish
- Aktiviteter som pågår (krysser status-datoen): lineær %-progresjon basert på arbeidsdager
- Fremtidige aktiviteter: 0% uten actuals
- StatusDate settes i XML så MS Project tegner "today"-linjen riktig

JSON-kildene (`core.json`, `wbs.json`, `schedule.json`) røres ikke — dette er kun render-tid-visning.

Eventuelle argumenter fra brukeren: $ARGUMENTS

Utfør (default: today hvis ingen argumenter):

```
python3 "004 data/generate_msproject_from_json.py" --status-date ${ARGUMENTS:-today}
```

Etter kjøring:
1. Verifiser at XML-filen er skrevet og last den i MS Project
2. Påpek at PM må lukke + åpne igjen i MS Project hvis filen allerede er åpen
3. Anbefal "Tracking Gantt"-visning for å se fremdriftsindikatorene tydelig
4. Minn brukeren om at senere `/msproject-test` eller `/msproject-generate` uten --status-date vil overskrive denne progressive versjonen — kjør `/msproject-story` på nytt hvis det skjer.
