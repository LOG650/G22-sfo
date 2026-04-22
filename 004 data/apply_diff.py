#!/usr/bin/env python3
"""
Apply-sync: Oppdater schedule.json automatisk med PM-eide datoendringer
fra en diff-rapport (fra msproject_to_json_diff.py).

Field ownership:
  - PM-eide felt (plannedStart, plannedFinish, date) oppdateres automatisk
  - Dev-eide felt (name, percentComplete) kan ikke auto-oppdateres
    (konflikter krever manuell beslutning; de flagges bare)

Kjør:
  python3 "004 data/msproject_to_json_diff.py" --xml path.xml --report /tmp/d.json --quiet
  python3 "004 data/apply_diff.py" --report /tmp/d.json
  python3 "004 data/apply_diff.py" --report /tmp/d.json --dry-run

Eller i en kommando (kjører diff først):
  python3 "004 data/apply_diff.py" --xml "path/to/pm-edited.xml"
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLAN_DIR = REPO_ROOT / "012 fase 2 - plan"
SCHEDULE_JSON = PLAN_DIR / "schedule.json"
DIFF_SCRIPT = Path(__file__).parent / "msproject_to_json_diff.py"
DEFAULT_XML = REPO_ROOT / "004 data" / "LOG650_G22_from_json.xml"


def run_diff(xml_path: Path, report_path: Path) -> int:
    """Kjør diff-scriptet og lagre rapport."""
    result = subprocess.run(
        [sys.executable, str(DIFF_SCRIPT),
         "--xml", str(xml_path),
         "--report", str(report_path),
         "--quiet"],
        capture_output=True, text=True,
    )
    return result.returncode


def apply_to_schedule(schedule: dict, diff_report: dict,
                      dry_run: bool) -> tuple[list[str], list[str]]:
    """
    Påfør PM-eide endringer på schedule-dict.
    Returnerer (applied: list, skipped_conflicts: list) med beskrivelser.
    """
    activities = {a["activityId"]: a for a in schedule["schedule"]["activities"]}
    milestones = {m["milestoneId"]: m for m in schedule["schedule"]["milestones"]}

    applied: list[str] = []
    skipped: list[str] = []

    for d in diff_report.get("diffs", []):
        owner = d.get("owner")
        field = d.get("field")
        key = d.get("key", "")
        xml_val = d.get("xmlValue")
        json_val = d.get("jsonValue")

        if owner != "pm":
            # Konflikt eller dev-eid — kan ikke auto-oppdatere
            skipped.append(f"{key}: {field} ({owner}-eid, severity={d.get('severity')}): "
                           f"{json_val!r} vs {xml_val!r}")
            continue

        # PM-eid endring — anvend
        if key.startswith("activity:"):
            aid = key.split(":", 1)[1]
            act = activities.get(aid)
            if not act:
                skipped.append(f"{key}: aktivitet ikke funnet i schedule.json")
                continue
            if field in ("plannedStart", "plannedFinish"):
                act[field] = xml_val
                applied.append(f"{key}: {field} {json_val} → {xml_val}")
        elif key.startswith("milestone:"):
            mid = key.split(":", 1)[1]
            ms = milestones.get(mid)
            if not ms:
                skipped.append(f"{key}: milepæl ikke funnet i schedule.json")
                continue
            if field == "date":
                ms["date"] = xml_val
                applied.append(f"{key}: date {json_val} → {xml_val}")

    # Oppdater audit hvis noe ble endret
    if applied and not dry_run:
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        schedule["schedule"].setdefault("audit", {})["updatedAt"] = now
        schedule["schedule"]["audit"]["updatedBy"] = "apply_diff.py (PM reverse sync)"

    return applied, skipped


def main() -> None:
    p = argparse.ArgumentParser(description="Auto-oppdater schedule.json fra diff-rapport")
    p.add_argument("--report", type=Path,
                   help="Forhåndsgenerert diff-rapport. Hvis utelatt, kjøres diff mot --xml først.")
    p.add_argument("--xml", type=Path, default=DEFAULT_XML,
                   help=f"MSPDI XML å diffe mot (default: {DEFAULT_XML.name})")
    p.add_argument("--schedule", type=Path, default=SCHEDULE_JSON,
                   help="schedule.json å oppdatere")
    p.add_argument("--dry-run", action="store_true",
                   help="Vis hva som ville blitt endret, ikke skriv")
    p.add_argument("--no-backup", action="store_true",
                   help="Ikke lag .bak backup av schedule.json")
    args = p.parse_args()

    # 1. Hent diff-rapport
    if args.report:
        report = json.loads(args.report.read_text(encoding="utf-8"))
    else:
        import tempfile
        tmp = Path(tempfile.gettempdir()) / f"msproj-diff-{datetime.now().timestamp()}.json"
        print(f"Kjører diff mot {args.xml}...")
        rc = run_diff(args.xml, tmp)
        if rc not in (0, 1, 2):
            print(f"FEIL: diff-script returnerte {rc}", file=sys.stderr)
            sys.exit(rc)
        report = json.loads(tmp.read_text(encoding="utf-8"))
        tmp.unlink(missing_ok=True)

    # 2. Last schedule.json
    schedule = json.loads(args.schedule.read_text(encoding="utf-8"))

    # 3. Anvend
    applied, skipped = apply_to_schedule(schedule, report, args.dry_run)

    # 4. Rapportér
    print(f"\nApply-sync fra: {report.get('xmlPath', '?')}")
    print("-" * 72)
    print(f"  Anvendte endringer: {len(applied)}")
    for line in applied:
        print(f"    ✓ {line}")
    print(f"\n  Hoppet over (konflikter/dev-eid): {len(skipped)}")
    for line in skipped:
        print(f"    ⚠ {line}")

    pm_added = report.get("pmAddedTasks", [])
    if pm_added:
        print(f"\n  PM-lagt til oppgaver (manuell håndtering kreves): {len(pm_added)}")
        for t in pm_added:
            print(f"    + UID={t.get('uid')}: {t.get('name')}")

    # 5. Skriv tilbake
    if applied and not args.dry_run:
        if not args.no_backup:
            backup = args.schedule.with_suffix(args.schedule.suffix + ".bak")
            shutil.copy(args.schedule, backup)
            print(f"\n  Backup: {backup}")
        args.schedule.write_text(
            json.dumps(schedule, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"  Oppdatert: {args.schedule}")
    elif args.dry_run:
        print(f"\n  [DRY-RUN] Ingen filer skrevet.")
    else:
        print(f"\n  Ingen PM-eide endringer å anvende.")

    # Exit codes
    if skipped:
        sys.exit(2)
    if not applied and not pm_added:
        sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    main()
