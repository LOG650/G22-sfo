#!/usr/bin/env python3
"""
Reverse sync: Les PM-modifisert MSPDI XML og sammenlign mot JSON-kildene.

Rapporterer hva som har endret seg og hvem som eier feltene iht. field-ownership
fra integrasjonsforskningen:
  - Dev (JSON) eier:  navn, percentComplete, identitet (ExtendedAttribute), struktur
  - PM (MS Project) eier:  plannedStart, plannedFinish, varighet, ressurser

Kjør:
  python3 "004 data/msproject_to_json_diff.py"
  python3 "004 data/msproject_to_json_diff.py" --xml "path/to/other.xml"
  python3 "004 data/msproject_to_json_diff.py" --report diff-report.json
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLAN_DIR = REPO_ROOT / "012 fase 2 - plan"
DEFAULT_XML = REPO_ROOT / "004 data" / "LOG650_G22_from_json.xml"

CORE_JSON = PLAN_DIR / "core.json"
WBS_JSON = PLAN_DIR / "wbs.json"
SCHEDULE_JSON = PLAN_DIR / "schedule.json"
MAPPING_JSON = PLAN_DIR / "msproject-mapping.json"

NS = {"m": "http://schemas.microsoft.com/project"}

FIELD_TEXT1 = "188743731"  # Activity ID
FIELD_TEXT2 = "188743734"  # Task ID
FIELD_TEXT3 = "188743737"  # WBS Item ID

DEV_OWNED = {"name", "percentComplete"}
PM_OWNED = {"plannedStart", "plannedFinish", "duration", "resources"}


# =====================================================================
# DATAKLASSER
# =====================================================================
@dataclass
class XmlTask:
    uid: int
    xml_id: int
    name: str
    start: str          # 'YYYY-MM-DD'
    finish: str         # 'YYYY-MM-DD'
    pct_complete: int
    milestone: bool
    summary: bool
    outline_level: int
    activity_id: str | None
    task_id: str | None
    wbs_item_id: str | None


@dataclass
class Diff:
    key: str
    entity_type: str         # 'activity', 'milestone', 'wbs'
    field: str
    owner: str               # 'dev', 'pm'
    json_value: object
    xml_value: object
    severity: str            # 'info', 'warn', 'conflict'

    def as_dict(self) -> dict:
        return {
            "key": self.key,
            "entityType": self.entity_type,
            "field": self.field,
            "owner": self.owner,
            "jsonValue": self.json_value,
            "xmlValue": self.xml_value,
            "severity": self.severity,
        }


@dataclass
class DiffReport:
    xmlPath: str
    generatedAt: str
    diffs: list[Diff] = field(default_factory=list)
    pmAdded: list[dict] = field(default_factory=list)   # i XML, ikke i JSON
    dvDeleted: list[dict] = field(default_factory=list)  # i mapping, ikke i XML
    summary: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "xmlPath": self.xmlPath,
            "generatedAt": self.generatedAt,
            "summary": self.summary,
            "diffs": [d.as_dict() for d in self.diffs],
            "pmAddedTasks": self.pmAdded,
            "devDeletedKeys": self.dvDeleted,
        }


# =====================================================================
# XML-PARSING
# =====================================================================
def iso_date(s: str | None) -> str:
    if not s:
        return ""
    return s[:10]


def parse_xml_tasks(xml_path: Path) -> list[XmlTask]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    tasks: list[XmlTask] = []

    for t in root.findall("m:Tasks/m:Task", NS):
        uid = int((t.findtext("m:UID", default="0", namespaces=NS) or "0"))
        if uid == 0:
            continue  # prosjekt-summary

        xid = int((t.findtext("m:ID", default="0", namespaces=NS) or "0"))
        name = t.findtext("m:Name", default="", namespaces=NS) or ""
        start = iso_date(t.findtext("m:Start", default="", namespaces=NS))
        finish = iso_date(t.findtext("m:Finish", default="", namespaces=NS))
        pct = int((t.findtext("m:PercentComplete", default="0", namespaces=NS) or "0"))
        milestone = (t.findtext("m:Milestone", default="0", namespaces=NS) or "0") == "1"
        summary = (t.findtext("m:Summary", default="0", namespaces=NS) or "0") == "1"
        level = int((t.findtext("m:OutlineLevel", default="0", namespaces=NS) or "0"))

        act_id: str | None = None
        task_id: str | None = None
        wbs_id: str | None = None
        for ext in t.findall("m:ExtendedAttribute", NS):
            fid = ext.findtext("m:FieldID", default="", namespaces=NS)
            val = ext.findtext("m:Value", default="", namespaces=NS)
            if fid == FIELD_TEXT1:
                act_id = val
            elif fid == FIELD_TEXT2:
                task_id = val
            elif fid == FIELD_TEXT3:
                wbs_id = val

        tasks.append(XmlTask(
            uid=uid, xml_id=xid, name=name, start=start, finish=finish,
            pct_complete=pct, milestone=milestone, summary=summary,
            outline_level=level, activity_id=act_id, task_id=task_id,
            wbs_item_id=wbs_id,
        ))
    return tasks


# =====================================================================
# MAPPING-NØKKEL FRA XML-TASK
# =====================================================================
def mapping_key_for_xml_task(xt: XmlTask) -> str | None:
    """Bestem stabil mapping-nøkkel for en XML-task."""
    if xt.milestone and xt.activity_id and xt.activity_id.startswith("M"):
        return f"milestone:{xt.activity_id}"
    if xt.summary and xt.wbs_item_id:
        return f"wbs:{xt.wbs_item_id}"
    if xt.activity_id and xt.activity_id.startswith("ACT-"):
        return f"activity:{xt.activity_id}"
    return None


# =====================================================================
# SAMMENLIGNING
# =====================================================================
def compare_activity(xt: XmlTask, act: dict, diffs: list[Diff]) -> None:
    key = f"activity:{act['activityId']}"
    json_name = act.get("name", "")
    json_start = act.get("plannedStart", "")
    json_finish = act.get("plannedFinish", "")
    json_pct = int(act.get("percentComplete", 0) or 0)

    if xt.name != json_name:
        diffs.append(Diff(
            key=key, entity_type="activity", field="name", owner="dev",
            json_value=json_name, xml_value=xt.name,
            severity="conflict",  # PM skrev over dev-eid felt
        ))
    if xt.start and xt.start != json_start:
        diffs.append(Diff(
            key=key, entity_type="activity", field="plannedStart", owner="pm",
            json_value=json_start, xml_value=xt.start,
            severity="info",  # PM eier; foreslå oppdatering av JSON
        ))
    if xt.finish and xt.finish != json_finish:
        diffs.append(Diff(
            key=key, entity_type="activity", field="plannedFinish", owner="pm",
            json_value=json_finish, xml_value=xt.finish,
            severity="info",
        ))
    if xt.pct_complete != json_pct:
        diffs.append(Diff(
            key=key, entity_type="activity", field="percentComplete", owner="dev",
            json_value=json_pct, xml_value=xt.pct_complete,
            severity="conflict",
        ))


def compare_milestone(xt: XmlTask, ms: dict, diffs: list[Diff]) -> None:
    key = f"milestone:{ms['milestoneId']}"
    expected_name = f"{ms['milestoneId']}: {ms.get('name', '')}"
    json_date = ms.get("date", "")

    if xt.name != expected_name:
        diffs.append(Diff(
            key=key, entity_type="milestone", field="name", owner="dev",
            json_value=expected_name, xml_value=xt.name,
            severity="conflict",
        ))
    if xt.start and xt.start != json_date:
        diffs.append(Diff(
            key=key, entity_type="milestone", field="date", owner="pm",
            json_value=json_date, xml_value=xt.start,
            severity="info",
        ))


def compare_wbs(xt: XmlTask, wbs_item: dict, diffs: list[Diff]) -> None:
    key = f"wbs:{wbs_item['wbsItemId']}"
    json_name = wbs_item.get("name", "")
    if xt.name != json_name:
        diffs.append(Diff(
            key=key, entity_type="wbs", field="name", owner="dev",
            json_value=json_name, xml_value=xt.name,
            severity="warn",
        ))


# =====================================================================
# HOVEDLOGIKK
# =====================================================================
def run_diff(xml_path: Path) -> DiffReport:
    if not xml_path.exists():
        print(f"FEIL: XML-fil finnes ikke: {xml_path}", file=sys.stderr)
        sys.exit(1)

    schedule = json.loads(SCHEDULE_JSON.read_text(encoding="utf-8"))["schedule"]
    wbs = json.loads(WBS_JSON.read_text(encoding="utf-8"))["wbs"]
    mapping = {}
    if MAPPING_JSON.exists():
        mapping = json.loads(MAPPING_JSON.read_text(encoding="utf-8")).get("entries", {})

    activities = {a["activityId"]: a for a in schedule.get("activities", [])}
    milestones = {m["milestoneId"]: m for m in schedule.get("milestones", [])}
    wbs_items = {w["wbsItemId"]: w for w in wbs.get("items", [])}

    xml_tasks = parse_xml_tasks(xml_path)

    report = DiffReport(
        xmlPath=str(xml_path),
        generatedAt=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    xml_keys: set[str] = set()
    for xt in xml_tasks:
        key = mapping_key_for_xml_task(xt)
        if key is None:
            # PM-lagt task uten ExtendedAttribute
            report.pmAdded.append({
                "uid": xt.uid,
                "xmlId": xt.xml_id,
                "name": xt.name,
                "start": xt.start,
                "finish": xt.finish,
                "milestone": xt.milestone,
                "summary": xt.summary,
            })
            continue

        xml_keys.add(key)

        if key.startswith("activity:"):
            aid = key.split(":", 1)[1]
            if aid in activities:
                compare_activity(xt, activities[aid], report.diffs)
        elif key.startswith("milestone:"):
            mid = key.split(":", 1)[1]
            if mid in milestones:
                compare_milestone(xt, milestones[mid], report.diffs)
        elif key.startswith("wbs:"):
            wid = key.split(":", 1)[1]
            if wid in wbs_items:
                compare_wbs(xt, wbs_items[wid], report.diffs)

    # Dev slettet: finnes i mapping men ikke i XML
    for k, uid in mapping.items():
        if k not in xml_keys:
            report.dvDeleted.append({"key": k, "lastUid": uid})

    report.summary = {
        "xmlTasks": len(xml_tasks),
        "matched": len(xml_keys),
        "pmAdded": len(report.pmAdded),
        "devDeletedFromMapping": len(report.dvDeleted),
        "diffs": len(report.diffs),
        "conflicts": sum(1 for d in report.diffs if d.severity == "conflict"),
        "pmDateChanges": sum(
            1 for d in report.diffs
            if d.owner == "pm" and d.field in ("plannedStart", "plannedFinish", "date")
        ),
    }
    return report


# =====================================================================
# RAPPORTERING
# =====================================================================
def color(txt: str, code: str) -> str:
    return f"\033[{code}m{txt}\033[0m" if sys.stdout.isatty() else txt


def print_report(report: DiffReport) -> None:
    s = report.summary
    print(f"\nReverse-sync diff: {report.xmlPath}")
    print(f"Genererert: {report.generatedAt}")
    print("-" * 72)
    print(f"  XML-tasks:              {s['xmlTasks']}")
    print(f"  Matchet mot JSON:       {s['matched']}")
    print(f"  PM-lagt til (nye):      {s['pmAdded']}")
    print(f"  Slettet fra JSON:       {s['devDeletedFromMapping']}")
    print(f"  Totalt diffs:           {s['diffs']}")
    print(f"    Konflikter (dev-eid): {s['conflicts']}")
    print(f"    PM datoendringer:     {s['pmDateChanges']}")

    if report.diffs:
        print("\nEndringer:")
        # Grupper per entitet
        by_key: dict[str, list[Diff]] = {}
        for d in report.diffs:
            by_key.setdefault(d.key, []).append(d)
        for key in sorted(by_key):
            print(f"\n  {key}")
            for d in by_key[key]:
                arrow = "→"
                marker = {
                    "info": color("[PM endret]", "36"),
                    "warn": color("[Avvik]", "33"),
                    "conflict": color("[KONFLIKT]", "31"),
                }.get(d.severity, d.severity)
                suggestion = ""
                if d.owner == "pm":
                    suggestion = "  (foreslått: oppdater JSON)"
                elif d.owner == "dev":
                    suggestion = "  (foreslått: gjenopprett JSON-verdi i MS Project)"
                print(f"    {marker} {d.field}: "
                      f"{d.json_value!r} {arrow} {d.xml_value!r}{suggestion}")

    if report.pmAdded:
        print(f"\nPM-lagt til oppgaver (mangler ExtendedAttribute):")
        for t in report.pmAdded:
            kind = "milepæl" if t["milestone"] else ("summary" if t["summary"] else "oppgave")
            print(f"  + UID={t['uid']} ({kind}): {t['name']} [{t['start']} → {t['finish']}]")
        print(f"  Foreslått: legg inn i JSON og kjør generator for å tildele stabil UID.")

    if report.dvDeleted:
        print(f"\nForeldreløse i mapping (ikke i XML lenger):")
        for x in report.dvDeleted[:10]:
            print(f"  - {x['key']} (siste UID={x['lastUid']})")
        if len(report.dvDeleted) > 10:
            print(f"  ... og {len(report.dvDeleted) - 10} flere")

    if not report.diffs and not report.pmAdded and not report.dvDeleted:
        print("\n✓ Ingen endringer. XML og JSON er i sync.")


# =====================================================================
# MAIN
# =====================================================================
def main() -> None:
    p = argparse.ArgumentParser(description="Reverse sync: MS Project XML → JSON diff")
    p.add_argument("--xml", type=Path, default=DEFAULT_XML,
                   help=f"Sti til MSPDI XML (default: {DEFAULT_XML.name})")
    p.add_argument("--report", type=Path, default=None,
                   help="Skriv maskinlesbar JSON-rapport til denne stien")
    p.add_argument("--quiet", action="store_true",
                   help="Skriv bare JSON-rapport, ikke konsolltekst")
    args = p.parse_args()

    report = run_diff(args.xml)

    if not args.quiet:
        print_report(report)

    if args.report:
        args.report.write_text(
            json.dumps(report.as_dict(), indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        if not args.quiet:
            print(f"\nRapport lagret: {args.report}")

    # Exit-kode: 0 hvis ingen endringer, 1 hvis konflikter, 2 hvis bare info/warn
    if report.summary.get("conflicts", 0) > 0:
        sys.exit(1)
    if report.diffs or report.pmAdded or report.dvDeleted:
        sys.exit(2)


if __name__ == "__main__":
    main()
