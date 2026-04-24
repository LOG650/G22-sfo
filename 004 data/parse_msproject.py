#!/usr/bin/env python3
"""
Parser for MS Project XML-eksport.
Leser prosjektplanen og genererer fremdriftsoversikt.

Bruk:
    python parse_msproject.py                  # Full oversikt
    python parse_msproject.py --status         # Kun statusrapport (hva er forsinket?)
    python parse_msproject.py --critical       # Kun kritisk linje
    python parse_msproject.py --upcoming 14    # Oppgaver neste 14 dager
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import re

XML_FILE = Path(__file__).parent / "LOG650 - G22 Prosjektplan.xml"
NS = {"ms": "http://schemas.microsoft.com/project"}
TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def parse_duration_hours(duration_str: str) -> float:
    """Konverter MS Project PT-duration (e.g. PT40H0M0S) til timer."""
    if not duration_str:
        return 0
    m = re.match(r"PT(\d+)H(\d+)M(\d+)S", duration_str)
    if m:
        return int(m.group(1)) + int(m.group(2)) / 60
    return 0


def parse_date(date_str: str) -> datetime | None:
    """Parse ISO-dato fra XML."""
    if not date_str:
        return None
    return datetime.fromisoformat(date_str)


def load_tasks(xml_path: Path) -> list[dict]:
    """Les alle oppgaver fra MS Project XML."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    tasks = []

    for task_el in root.findall(".//ms:Tasks/ms:Task", NS):
        uid = task_el.findtext("ms:UID", "", NS)
        name = task_el.findtext("ms:Name", "", NS)
        wbs = task_el.findtext("ms:WBS", "", NS)
        outline_level = int(task_el.findtext("ms:OutlineLevel", "0", NS))
        start = parse_date(task_el.findtext("ms:Start", "", NS))
        finish = parse_date(task_el.findtext("ms:Finish", "", NS))
        duration_str = task_el.findtext("ms:Duration", "", NS)
        duration_h = parse_duration_hours(duration_str)
        pct_complete = int(task_el.findtext("ms:PercentComplete", "0", NS))
        critical = task_el.findtext("ms:Critical", "0", NS) == "1"
        milestone = task_el.findtext("ms:Milestone", "0", NS) == "1"

        # Hent predecessors
        predecessors = []
        for pred in task_el.findall("ms:PredecessorLink", NS):
            pred_uid = pred.findtext("ms:PredecessorUID", "", NS)
            pred_type = pred.findtext("ms:Type", "1", NS)  # 1=FS, 0=FF, 2=SS, 3=SF
            predecessors.append({"uid": pred_uid, "type": pred_type})

        # Baseline-data (hvis satt)
        bl_start = parse_date(
            task_el.findtext("ms:BaselineStart", "", NS)
            or task_el.findtext("ms:b298000", "", NS)
        )
        bl_finish = parse_date(
            task_el.findtext("ms:BaselineFinish", "", NS)
            or task_el.findtext("ms:b299000", "", NS)
        )

        if outline_level == 0 and wbs == "0":
            continue  # Skip prosjekt-summary

        tasks.append({
            "uid": uid,
            "name": name,
            "wbs": wbs,
            "level": outline_level,
            "start": start,
            "finish": finish,
            "duration_h": duration_h,
            "duration_days": duration_h / 8 if duration_h else 0,
            "pct_complete": pct_complete,
            "critical": critical,
            "milestone": milestone,
            "predecessors": predecessors,
            "bl_start": bl_start,
            "bl_finish": bl_finish,
        })

    return tasks


def status_icon(task: dict) -> str:
    """Returner statusikon basert på fremdrift vs. tid."""
    if task["pct_complete"] == 100:
        return "done"
    if not task["finish"]:
        return "  ? "
    if task["finish"] < TODAY and task["pct_complete"] < 100:
        return "LATE"
    if task["start"] and task["start"] <= TODAY:
        # Beregn forventet % basert på tid
        total = (task["finish"] - task["start"]).days
        elapsed = (TODAY - task["start"]).days
        if total > 0:
            expected_pct = min(100, int(elapsed / total * 100))
            if task["pct_complete"] < expected_pct - 20:
                return "RISK"
            elif task["pct_complete"] >= expected_pct:
                return " ok "
            else:
                return "slow"
        return " ok "
    return "    "


def print_all_tasks(tasks: list[dict]):
    """Skriv ut full oppgaveliste med status."""
    print(f"\n{'='*90}")
    print(f"  PROSJEKTOVERSIKT — {TODAY.strftime('%d. %B %Y')}")
    print(f"{'='*90}")
    print(f"{'WBS':<8} {'Status':<6} {'%':>4} {'Oppgave':<40} {'Start':<12} {'Slutt':<12} {'Dager':>5}")
    print(f"{'-'*8} {'-'*6} {'-'*4} {'-'*40} {'-'*12} {'-'*12} {'-'*5}")

    for t in tasks:
        indent = "  " * (t["level"] - 1) if t["level"] > 0 else ""
        name = indent + t["name"]
        if len(name) > 40:
            name = name[:37] + "..."

        icon = status_icon(t)
        start_str = t["start"].strftime("%d.%m") if t["start"] else ""
        finish_str = t["finish"].strftime("%d.%m") if t["finish"] else ""
        crit = "*" if t["critical"] else " "
        mile = "<<M>>" if t["milestone"] else ""

        if t["milestone"]:
            print(f"{t['wbs']:<8} {icon:<6} {t['pct_complete']:>3}% {'  ' + mile + ' ' + t['name']:<40} {start_str:<12} {finish_str:<12}")
        elif t["level"] == 1:
            print(f"\n{t['wbs']:<8} {icon:<6} {t['pct_complete']:>3}% {name:<40} {start_str:<12} {finish_str:<12} {t['duration_days']:>5.0f}")
        else:
            print(f"{t['wbs']:<8} {icon:<6} {t['pct_complete']:>3}%{crit}{name:<40} {start_str:<12} {finish_str:<12} {t['duration_days']:>5.0f}")


def print_status_report(tasks: list[dict]):
    """Skriv ut statusrapport: forsinkede, pågående, kommende."""
    print(f"\n{'='*70}")
    print(f"  STATUSRAPPORT — {TODAY.strftime('%d. %B %Y')}")
    print(f"{'='*70}")

    # Forsinkede oppgaver
    late = [t for t in tasks if status_icon(t) in ("LATE", "RISK") and t["level"] > 1]
    if late:
        print(f"\n  FORSINKEDE / I RISIKO ({len(late)} oppgaver):")
        print(f"  {'-'*60}")
        for t in late:
            days_late = (TODAY - t["finish"]).days if t["finish"] and t["finish"] < TODAY else 0
            status = f"FORSINKET {days_late}d" if days_late > 0 else "I RISIKO"
            print(f"  [{status}] {t['wbs']} {t['name']} ({t['pct_complete']}% ferdig, frist: {t['finish'].strftime('%d.%m') if t['finish'] else '?'})")
    else:
        print("\n  Ingen forsinkede oppgaver!")

    # Pågående
    active = [t for t in tasks
              if t["level"] > 1
              and t["start"] and t["start"] <= TODAY
              and t["finish"] and t["finish"] >= TODAY
              and t["pct_complete"] < 100]
    if active:
        print(f"\n  PÅGÅENDE ({len(active)} oppgaver):")
        print(f"  {'-'*60}")
        for t in active:
            remaining = (t["finish"] - TODAY).days
            print(f"  {t['wbs']:<8} {t['name']:<40} {t['pct_complete']:>3}% ferdig, {remaining}d igjen")

    # Neste opp
    upcoming = [t for t in tasks
                if t["level"] > 1
                and t["start"] and t["start"] > TODAY
                and t["start"] <= TODAY + timedelta(days=14)]
    if upcoming:
        print(f"\n  KOMMENDE (neste 14 dager, {len(upcoming)} oppgaver):")
        print(f"  {'-'*60}")
        for t in upcoming:
            print(f"  {t['wbs']:<8} {t['name']:<40} starter {t['start'].strftime('%d.%m')}")

    # Prosjektfremdrift
    all_leaf = [t for t in tasks if t["level"] > 1 and not t["milestone"]]
    if all_leaf:
        total_days = sum(t["duration_days"] for t in all_leaf)
        completed_days = sum(t["duration_days"] * t["pct_complete"] / 100 for t in all_leaf)
        overall_pct = (completed_days / total_days * 100) if total_days > 0 else 0
        print(f"\n  TOTALFREMDRIFT: {overall_pct:.1f}%")
        bar_len = 40
        filled = int(bar_len * overall_pct / 100)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"  [{bar}] {overall_pct:.1f}%")


def print_critical_path(tasks: list[dict]):
    """Skriv ut oppgaver på kritisk linje."""
    critical = [t for t in tasks if t["critical"] and t["level"] > 1]
    print(f"\n{'='*70}")
    print(f"  KRITISK LINJE")
    print(f"{'='*70}")
    if not critical:
        print("  Ingen oppgaver markert som kritiske i MS Project.")
        return
    for t in critical:
        icon = status_icon(t)
        start_str = t["start"].strftime("%d.%m") if t["start"] else ""
        finish_str = t["finish"].strftime("%d.%m") if t["finish"] else ""
        print(f"  [{icon}] {t['wbs']:<8} {t['name']:<40} {start_str}-{finish_str}  {t['pct_complete']}%")


def print_upcoming(tasks: list[dict], days: int = 14):
    """Skriv ut oppgaver som starter/slutter innen N dager."""
    cutoff = TODAY + timedelta(days=days)
    relevant = [t for t in tasks
                if t["level"] > 1
                and not t["milestone"]
                and ((t["start"] and TODAY <= t["start"] <= cutoff)
                     or (t["finish"] and TODAY <= t["finish"] <= cutoff)
                     or (t["start"] and t["finish"] and t["start"] <= TODAY and t["finish"] >= TODAY))]
    print(f"\n{'='*70}")
    print(f"  OPPGAVER NESTE {days} DAGER (fra {TODAY.strftime('%d.%m')})")
    print(f"{'='*70}")
    for t in sorted(relevant, key=lambda x: x["start"] or TODAY):
        icon = status_icon(t)
        start_str = t["start"].strftime("%d.%m") if t["start"] else ""
        finish_str = t["finish"].strftime("%d.%m") if t["finish"] else ""
        print(f"  [{icon}] {t['wbs']:<8} {t['name']:<35} {start_str}-{finish_str}  {t['pct_complete']}%")


def main():
    parser = argparse.ArgumentParser(description="MS Project fremdriftsoversikt for LOG650-G22")
    parser.add_argument("--status", action="store_true", help="Kun statusrapport")
    parser.add_argument("--critical", action="store_true", help="Kun kritisk linje")
    parser.add_argument("--upcoming", type=int, metavar="DAYS", help="Oppgaver neste N dager")
    parser.add_argument("--file", type=str, default=str(XML_FILE), help="Sti til XML-fil")
    args = parser.parse_args()

    tasks = load_tasks(Path(args.file))
    print(f"  Lastet {len(tasks)} oppgaver fra MS Project")

    if args.status:
        print_status_report(tasks)
    elif args.critical:
        print_critical_path(tasks)
    elif args.upcoming is not None:
        print_upcoming(tasks, args.upcoming)
    else:
        print_all_tasks(tasks)
        print()
        print_critical_path(tasks)
        print()
        print_status_report(tasks)


if __name__ == "__main__":
    main()
