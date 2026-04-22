#!/usr/bin/env python3
"""
Genererer MS Project MSPDI XML fra JSON-kildefilene i '012 fase 2 - plan/'.

Kilder (source of truth):
  - 012 fase 2 - plan/core.json      → prosjektnavn, team (ressurser)
  - 012 fase 2 - plan/wbs.json       → hierarki (summary-oppgaver)
  - 012 fase 2 - plan/schedule.json  → aktiviteter, milepæler, datoer, avhengigheter

Produserer:
  - 004 data/LOG650_G22_from_json.xml  (åpnes direkte i MS Project)

Kjør:
  python3 "004 data/generate_msproject_from_json.py"
"""

from __future__ import annotations

import argparse
import json
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from xml.dom import minidom

# =====================================================================
# STIER
# =====================================================================
REPO_ROOT = Path(__file__).resolve().parent.parent
PLAN_DIR = REPO_ROOT / "012 fase 2 - plan"
OUTPUT = REPO_ROOT / "004 data" / "LOG650_G22_from_json.xml"

CORE_JSON = PLAN_DIR / "core.json"
WBS_JSON = PLAN_DIR / "wbs.json"
SCHEDULE_JSON = PLAN_DIR / "schedule.json"
MAPPING_JSON = PLAN_DIR / "msproject-mapping.json"

# =====================================================================
# KALENDER
# =====================================================================
HOURS_PER_DAY = 8
MINS_PER_DAY = HOURS_PER_DAY * 60  # 480

# MS Project ExtendedAttribute FieldIDs (MSPDI-standard)
FIELD_TEXT1 = "188743731"
FIELD_TEXT2 = "188743734"
FIELD_TEXT3 = "188743737"
FIELD_TEXT4 = "188743740"

# Predecessor-typer (MSPDI)
PRED_TYPE = {
    "finish-to-finish": "0",
    "finish-to-start": "1",
    "start-to-finish": "2",
    "start-to-start": "3",
}

# Milepæl → fase (WBS level 2) mapping. Bestemmer hvor milepælen plasseres
# i hierarkiet. Rekkefølgen speiler prosjektplanen.
MILESTONE_TO_WBS = {
    "M0": "WBS-1.1",
    "M1": "WBS-1.2",
    "M2": "WBS-1.3",
    "M3": "WBS-1.4",
}


# =====================================================================
# HJELPEFUNKSJONER
# =====================================================================
def parse_date(s: str, end_of_day: bool = False) -> datetime:
    """Parse 'YYYY-MM-DD' til datetime kl 08:00 eller 17:00."""
    d = datetime.strptime(s[:10], "%Y-%m-%d")
    return d.replace(hour=17, minute=0) if end_of_day else d.replace(hour=8, minute=0)


def workdays_between(start: datetime, finish: datetime) -> int:
    """Antall arbeidsdager (man-fre) mellom to datoer, inklusivt."""
    if finish < start:
        return 0
    days = 0
    cur = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = finish.replace(hour=0, minute=0, second=0, microsecond=0)
    while cur <= end:
        if cur.weekday() < 5:
            days += 1
        cur += timedelta(days=1)
    return max(days, 1)


def duration_pt(days: int) -> str:
    """Konverter arbeidsdager til PT-format (PT40H0M0S = 5 dager)."""
    return f"PT{days * HOURS_PER_DAY}H0M0S"


def add(parent: ET.Element, tag: str, text) -> ET.Element:
    el = ET.SubElement(parent, tag)
    el.text = str(text)
    return el


def add_extended_attr(parent: ET.Element, field_id: str, value: str) -> None:
    """Legg til ExtendedAttribute på en oppgave."""
    ext = ET.SubElement(parent, "ExtendedAttribute")
    add(ext, "FieldID", field_id)
    add(ext, "Value", value)


# =====================================================================
# UID MAPPING (stabil identitet på tvers av syncs)
# =====================================================================
class UIDAllocator:
    """
    Tildeler og bevarer stabile MS Project UIDs på tvers av genereringer.

    Nøkler er stabile ID-er fra JSON-kildene:
      - activity:<activityId>   for aktiviteter (f.eks. 'activity:ACT-2.1')
      - milestone:<milestoneId> for milepæler  (f.eks. 'milestone:M1')
      - wbs:<wbsItemId>         for summary-oppgaver (f.eks. 'wbs:WBS-1.2')

    Mapping-fil lagres i PLAN_DIR/msproject-mapping.json.
    """

    def __init__(self, mapping_file: Path = MAPPING_JSON,
                 load_existing: bool = True) -> None:
        self.mapping_file = mapping_file
        self.mapping: dict = self._load() if load_existing else {
            "entries": {}, "nextUid": 1, "history": []
        }
        self.entries: dict[str, int] = dict(self.mapping.get("entries", {}))
        self.used: set[int] = set(self.entries.values())
        self.next_uid: int = max(self.mapping.get("nextUid", 1),
                                 max(self.used, default=0) + 1)
        self.hits: set[str] = set()
        self.new_keys: list[str] = []

    def _load(self) -> dict:
        if self.mapping_file.exists():
            try:
                return json.loads(self.mapping_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        return {"entries": {}, "nextUid": 1, "history": []}

    def get(self, key: str) -> int:
        if key in self.entries:
            self.hits.add(key)
            return self.entries[key]
        while self.next_uid in self.used:
            self.next_uid += 1
        uid = self.next_uid
        self.entries[key] = uid
        self.used.add(uid)
        self.new_keys.append(key)
        self.next_uid += 1
        return uid

    def orphans(self) -> list[str]:
        """Nøkler i eksisterende mapping som ikke ble brukt i denne runden."""
        return [k for k in self.mapping.get("entries", {}) if k not in self.hits]

    def save(self, active_keys: set[str]) -> None:
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        orphans = [k for k in self.entries if k not in active_keys]
        payload = {
            "schema": {
                "name": "msproject.uid.mapping",
                "version": "1.0.0",
                "description": ("Stabil mapping fra JSON-ID-er til MS Project UIDs. "
                                "Oppdateres av generate_msproject_from_json.py."),
            },
            "lastSync": now,
            "nextUid": self.next_uid,
            "stats": {
                "total": len(self.entries),
                "reused": len(self.hits),
                "new": len(self.new_keys),
                "orphans": len(orphans),
            },
            "entries": dict(sorted(self.entries.items())),
            "orphans": orphans,
            "history": (self.mapping.get("history", []) + [{
                "syncedAt": now,
                "reused": len(self.hits),
                "new": len(self.new_keys),
                "orphans": len(orphans),
                "newKeys": self.new_keys,
            }])[-10:],  # behold siste 10 runs
        }
        self.mapping_file.write_text(
            json.dumps(payload, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


# =====================================================================
# DATAMODELLER
# =====================================================================
def load_sources() -> tuple[dict, dict, dict]:
    core = json.loads(CORE_JSON.read_text(encoding="utf-8"))
    wbs = json.loads(WBS_JSON.read_text(encoding="utf-8"))
    schedule = json.loads(SCHEDULE_JSON.read_text(encoding="utf-8"))
    return core, wbs, schedule


def build_resources(core: dict) -> list[dict]:
    """Bygg ressursliste fra core.json team. UIDs er 1-basert."""
    team = core["project"].get("team", [])
    resources = []
    for idx, member in enumerate(team, start=1):
        name = member["name"]
        parts = name.split()
        initials = "".join(p[0] for p in parts if p).upper()[:3]
        resources.append({
            "uid": idx,
            "id": idx,
            "name": name,
            "initials": initials,
            "party_id": member.get("partyId", ""),
        })
    return resources


def resolve_resources_for_run_by(run_by: str | None, resources: list[dict]) -> list[int]:
    """Map 'runBy'-streng fra schedule.json til liste av ressurs-UIDs."""
    if not run_by:
        return []
    run_by = run_by.strip()
    if run_by.lower() in ("alle", "studentgruppe", "prosjektgruppe g22"):
        return [r["uid"] for r in resources]
    uids = []
    for part in (p.strip() for p in run_by.split(",")):
        for r in resources:
            if part and (part == r["name"] or part in r["name"]):
                uids.append(r["uid"])
                break
    return uids


def assemble_tasks(
    wbs: dict,
    schedule: dict,
    resources: list[dict],
    allocator: UIDAllocator,
) -> tuple[list[dict], set[str]]:
    """
    Bygg flat, ordnet liste av oppgaver med OutlineLevel, klar for XML-eksport.

    Bruker UIDAllocator for å gjenbruke stabile UIDs på tvers av kjøringer.
    Returnerer også settet av mapping-nøkler som er aktive i denne runden.

    Struktur:
      - Level 1: Fase (WBS level 2)
      - Level 2: Arbeidspakke/deliverable (WBS level 3)
      - Level 3: Aktivitet eller milepæl
    """
    wbs_items = wbs["wbs"]["items"]
    activities = schedule["schedule"]["activities"]
    milestones = schedule["schedule"]["milestones"]

    activity_by_id = {a["activityId"]: a for a in activities}

    # Milepæler per fase-WBS
    milestone_by_phase: dict[str, list[dict]] = {}
    for ms in milestones:
        phase_wbs = MILESTONE_TO_WBS.get(ms["milestoneId"])
        if phase_wbs:
            milestone_by_phase.setdefault(phase_wbs, []).append(ms)

    tasks: list[dict] = []
    active_keys: set[str] = set()

    # Walk WBS-hierarki: phases (level 2 under WBS-1) → deliverables (level 3)
    phases = [w for w in wbs_items if w["level"] == 2 and w["parentId"] == "WBS-1"]
    phases.sort(key=lambda w: w["code"])

    for phase in phases:
        phase_key = f"wbs:{phase['wbsItemId']}"
        active_keys.add(phase_key)
        tasks.append({
            "uid": allocator.get(phase_key),
            "mapping_key": phase_key,
            "name": phase["name"],
            "level": 1,
            "summary": True,
            "wbs_code": phase["code"],
            "wbs_item_id": phase["wbsItemId"],
            "activity_id": None,
            "task_id": None,
            "milestone": False,
            "predecessors": [],
            "resources": [],
            "pct": 0,
        })

        # Deliverables under fase
        deliverables = [
            w for w in wbs_items
            if w["level"] == 3 and w["parentId"] == phase["wbsItemId"]
        ]
        deliverables.sort(key=lambda w: w["code"])

        for deliv in deliverables:
            deliv_key = f"wbs:{deliv['wbsItemId']}"
            active_keys.add(deliv_key)
            deliv_activities = [
                activity_by_id[aid]
                for aid in deliv.get("activityIds", [])
                if aid in activity_by_id
            ]
            deliv_activities.sort(key=lambda a: a["plannedStart"])

            tasks.append({
                "uid": allocator.get(deliv_key),
                "mapping_key": deliv_key,
                "name": deliv["name"],
                "level": 2,
                "summary": True,
                "wbs_code": deliv["code"],
                "wbs_item_id": deliv["wbsItemId"],
                "activity_id": None,
                "task_id": None,
                "milestone": False,
                "predecessors": [],
                "resources": [],
                "pct": 0,
            })

            # Aktiviteter (level 3, blad)
            for act in deliv_activities:
                act_key = f"activity:{act['activityId']}"
                active_keys.add(act_key)
                start_dt = parse_date(act["plannedStart"])
                finish_dt = parse_date(act["plannedFinish"], end_of_day=True)
                duration = workdays_between(start_dt, finish_dt)

                run_by = (act.get("execution") or {}).get("runBy")
                res_uids = resolve_resources_for_run_by(run_by, resources)

                tasks.append({
                    "uid": allocator.get(act_key),
                    "mapping_key": act_key,
                    "name": act["name"],
                    "level": 3,
                    "summary": False,
                    "wbs_code": deliv["code"],
                    "wbs_item_id": deliv["wbsItemId"],
                    "activity_id": act["activityId"],
                    "task_id": act.get("taskId"),
                    "milestone": False,
                    "start": start_dt,
                    "finish": finish_dt,
                    "duration_days": duration,
                    "predecessors": act.get("predecessors", []),
                    "resources": res_uids,
                    "pct": int(act.get("percentComplete", 0) or 0),
                    "is_critical": bool(act.get("isCriticalPath", False)),
                    "milestone_ref": act.get("milestoneId"),
                })

        # Milepæler for denne fasen — plasseres sist i fasen
        for ms in milestone_by_phase.get(phase["wbsItemId"], []):
            ms_key = f"milestone:{ms['milestoneId']}"
            active_keys.add(ms_key)
            ms_date = parse_date(ms["date"])
            ms_preds = [
                {"activityId": a["activityId"], "type": "finish-to-start", "lagDays": 0}
                for a in activities
                if a.get("milestoneId") == ms["milestoneId"]
            ]
            pct = 100 if ms.get("status") == "reached" else 0
            tasks.append({
                "uid": allocator.get(ms_key),
                "mapping_key": ms_key,
                "name": f"{ms['milestoneId']}: {ms['name']}",
                "level": 2,
                "summary": False,
                "wbs_code": phase["code"],
                "wbs_item_id": phase["wbsItemId"],
                "activity_id": ms["milestoneId"],
                "task_id": None,
                "milestone": True,
                "start": ms_date,
                "finish": ms_date,
                "duration_days": 0,
                "predecessors": ms_preds,
                "resources": [],
                "pct": pct,
                "is_critical": True,
                "milestone_ref": None,
            })

    return tasks, active_keys


def compute_summary_dates(tasks: list[dict]) -> None:
    """Sett start/finish/duration på summary-oppgaver fra underliggende blader."""
    # Bygg indeks av 'children' per summary
    n = len(tasks)
    for i, t in enumerate(tasks):
        if not t.get("summary"):
            continue
        children = []
        for j in range(i + 1, n):
            c = tasks[j]
            if c["level"] <= t["level"]:
                break
            if not c.get("summary"):
                children.append(c)
        if not children:
            continue
        start = min(c["start"] for c in children if c.get("start"))
        finish = max(c["finish"] for c in children if c.get("finish"))
        t["start"] = start
        t["finish"] = finish
        t["duration_days"] = workdays_between(start, finish)
        # Summary pct = vektet snitt av barn (på arbeidsdager)
        total_days = sum(c.get("duration_days", 1) for c in children) or 1
        weighted_pct = sum(
            c.get("pct", 0) * c.get("duration_days", 1) for c in children
        ) / total_days
        t["pct"] = int(round(weighted_pct))


def resolve_predecessors(tasks: list[dict]) -> None:
    """Bytt ut predecessor activityId med tilsvarende task-UID."""
    uid_by_activity = {
        t["activity_id"]: t["uid"]
        for t in tasks
        if t.get("activity_id")
    }
    for t in tasks:
        resolved = []
        for p in t.get("predecessors", []):
            aid = p.get("activityId")
            if not aid or aid not in uid_by_activity:
                continue
            resolved.append({
                "uid": uid_by_activity[aid],
                "type": PRED_TYPE.get(p.get("type", "finish-to-start"), "1"),
                "lag_days": int(p.get("lagDays", 0) or 0),
            })
        t["predecessors_resolved"] = resolved


# =====================================================================
# XML-BYGGING
# =====================================================================
def build_xml(core: dict, tasks: list[dict], resources: list[dict]) -> ET.Element:
    project = core["project"]
    project_name = project.get("name", "Prosjekt")
    project_code = project.get("code", "PRJ")

    root = ET.Element("Project")
    root.set("xmlns", "http://schemas.microsoft.com/project")

    # --- Metadata ---
    leaves = [t for t in tasks if not t.get("summary")]
    project_start = min(t["start"] for t in leaves if t.get("start"))
    project_finish = max(t["finish"] for t in leaves if t.get("finish"))
    now = datetime.now()

    add(root, "SaveVersion", "14")
    add(root, "BuildNumber", "16.0.19725.20152")
    add(root, "Name", OUTPUT.name)
    add(root, "GUID", str(uuid.uuid4()).upper())
    add(root, "Title", project_name)
    add(root, "Subject", project_code)
    add(root, "Author", "LOG650 G22 (generert fra JSON)")
    add(root, "CreationDate", now.strftime("%Y-%m-%dT%H:%M:00"))
    add(root, "LastSaved", now.strftime("%Y-%m-%dT%H:%M:00"))
    add(root, "ScheduleFromStart", "1")
    add(root, "StartDate", project_start.strftime("%Y-%m-%dT08:00:00"))
    add(root, "FinishDate", project_finish.strftime("%Y-%m-%dT17:00:00"))
    add(root, "FYStartDate", "1")
    add(root, "CriticalSlackLimit", "0")
    add(root, "CurrencyDigits", "2")
    add(root, "CurrencySymbol", "kr")
    add(root, "CurrencyCode", "NOK")
    add(root, "CurrencySymbolPosition", "3")
    add(root, "CalendarUID", "1")
    add(root, "DefaultStartTime", "08:00:00")
    add(root, "DefaultFinishTime", "17:00:00")
    add(root, "MinutesPerDay", str(MINS_PER_DAY))
    add(root, "MinutesPerWeek", str(MINS_PER_DAY * 5))
    add(root, "DaysPerMonth", "20")
    add(root, "DefaultTaskType", "0")
    add(root, "DefaultFixedCostAccrual", "3")
    add(root, "DefaultStandardRate", "0")
    add(root, "DefaultOvertimeRate", "0")
    add(root, "DurationFormat", "7")
    add(root, "WorkFormat", "2")
    add(root, "EditableActualCosts", "0")
    add(root, "HonorConstraints", "0")
    add(root, "InsertedProjectsLikeSummary", "0")
    add(root, "MultipleCriticalPaths", "0")
    add(root, "NewTasksEffortDriven", "0")
    add(root, "NewTasksEstimated", "1")
    add(root, "SplitsInProgressTasks", "1")
    add(root, "SpreadActualCost", "0")
    add(root, "SpreadPercentComplete", "0")
    add(root, "TaskUpdatesResource", "1")
    add(root, "FiscalYearStart", "0")
    add(root, "WeekStartDay", "1")
    add(root, "MoveCompletedEndsBack", "0")
    add(root, "MoveRemainingStartsBack", "0")
    add(root, "MoveRemainingStartsForward", "0")
    add(root, "MoveCompletedEndsForward", "0")
    add(root, "BaselineForEarnedValue", "0")
    add(root, "AutoAddNewResourcesAndTasks", "1")
    add(root, "CurrentDate", now.strftime("%Y-%m-%dT08:00:00"))
    add(root, "MicrosoftProjectServerURL", "1")
    add(root, "Autolink", "1")
    add(root, "NewTaskStartDate", "0")
    add(root, "NewTasksAreManual", "0")
    add(root, "DefaultTaskEVMethod", "0")
    add(root, "ProjectExternallyEdited", "0")
    add(root, "ActualsInSync", "0")
    add(root, "RemoveFileProperties", "0")
    add(root, "AdminProject", "0")

    ET.SubElement(root, "OutlineCodes")
    ET.SubElement(root, "WBSMasks")

    # --- Custom fields (ExtendedAttributes) for agent-metadata ---
    ext_attrs = ET.SubElement(root, "ExtendedAttributes")

    def declare_field(field_id: str, name: str, alias: str) -> None:
        ea = ET.SubElement(ext_attrs, "ExtendedAttribute")
        add(ea, "FieldID", field_id)
        add(ea, "FieldName", name)
        add(ea, "Alias", alias)

    declare_field(FIELD_TEXT1, "Text1", "Activity ID")
    declare_field(FIELD_TEXT2, "Text2", "Task ID")
    declare_field(FIELD_TEXT3, "Text3", "WBS Item ID")
    declare_field(FIELD_TEXT4, "Text4", "Source")

    # --- Kalender ---
    calendars = ET.SubElement(root, "Calendars")
    cal = ET.SubElement(calendars, "Calendar")
    add(cal, "UID", "1")
    add(cal, "Name", "Standard")
    add(cal, "IsBaseCalendar", "1")
    add(cal, "IsBaselineCalendar", "0")
    add(cal, "BaseCalendarUID", "-1")
    weekdays = ET.SubElement(cal, "WeekDays")
    for day_type in range(1, 8):
        wd = ET.SubElement(weekdays, "WeekDay")
        add(wd, "DayType", str(day_type))
        if day_type in (1, 7):  # søndag, lørdag
            add(wd, "DayWorking", "0")
        else:
            add(wd, "DayWorking", "1")
            wts = ET.SubElement(wd, "WorkingTimes")
            wt1 = ET.SubElement(wts, "WorkingTime")
            add(wt1, "FromTime", "08:00:00")
            add(wt1, "ToTime", "12:00:00")
            wt2 = ET.SubElement(wts, "WorkingTime")
            add(wt2, "FromTime", "13:00:00")
            add(wt2, "ToTime", "17:00:00")

    # --- Tasks ---
    tasks_el = ET.SubElement(root, "Tasks")

    # UID 0: Project summary
    total_days = workdays_between(project_start, project_finish)
    total_leaf_work = sum(
        (t.get("duration_days") or 0) * max(len(t.get("resources") or []), 1)
        for t in leaves if not t.get("milestone")
    )

    proj = ET.SubElement(tasks_el, "Task")
    add(proj, "UID", "0")
    add(proj, "ID", "0")
    add(proj, "Name", project_name)
    add(proj, "Active", "1")
    add(proj, "Manual", "0")
    add(proj, "Type", "1")
    add(proj, "IsNull", "0")
    add(proj, "CreateDate", now.strftime("%Y-%m-%dT%H:%M:00"))
    add(proj, "WBS", "0")
    add(proj, "OutlineNumber", "0")
    add(proj, "OutlineLevel", "0")
    add(proj, "Priority", "500")
    add(proj, "Start", project_start.strftime("%Y-%m-%dT08:00:00"))
    add(proj, "Finish", project_finish.strftime("%Y-%m-%dT17:00:00"))
    add(proj, "Duration", duration_pt(total_days))
    add(proj, "DurationFormat", "7")
    add(proj, "Work", f"PT{total_leaf_work * HOURS_PER_DAY}H0M0S")
    add(proj, "ResumeValid", "0")
    add(proj, "EffortDriven", "0")
    add(proj, "Recurring", "0")
    add(proj, "OverAllocated", "0")
    add(proj, "Estimated", "0")
    add(proj, "Milestone", "0")
    add(proj, "Summary", "1")
    add(proj, "DisplayAsSummary", "0")
    add(proj, "Critical", "0")
    add(proj, "IsSubproject", "0")
    add(proj, "IsSubprojectReadOnly", "0")
    add(proj, "ExternalTask", "0")
    add(proj, "FixedCostAccrual", "3")
    add(proj, "RemainingDuration", duration_pt(total_days))
    add(proj, "ConstraintType", "0")
    add(proj, "CalendarUID", "-1")
    add(proj, "LevelAssignments", "1")
    add(proj, "LevelingCanSplit", "1")
    add(proj, "IgnoreResourceCalendar", "0")
    add(proj, "HideBar", "0")
    add(proj, "Rollup", "0")
    add(proj, "PercentComplete", "0")
    add(proj, "PercentWorkComplete", "0")
    add(proj, "EarnedValueMethod", "0")

    # Faktiske tasks
    for idx, t in enumerate(tasks, start=1):
        te = ET.SubElement(tasks_el, "Task")
        add(te, "UID", str(t["uid"]))
        add(te, "ID", str(idx))
        add(te, "Name", t["name"])
        add(te, "Active", "1")
        add(te, "Manual", "0")
        add(te, "Type", "0")
        add(te, "IsNull", "0")
        add(te, "CreateDate", now.strftime("%Y-%m-%dT%H:%M:00"))
        add(te, "WBS", t.get("wbs_code", ""))
        add(te, "OutlineNumber", t.get("wbs_code", ""))
        add(te, "OutlineLevel", str(t["level"]))
        add(te, "Priority", "500")

        start_str = t["start"].strftime("%Y-%m-%dT08:00:00")
        if t.get("milestone"):
            finish_str = t["finish"].strftime("%Y-%m-%dT08:00:00")
        else:
            finish_str = t["finish"].strftime("%Y-%m-%dT17:00:00")
        add(te, "Start", start_str)
        add(te, "Finish", finish_str)

        duration_days = int(t.get("duration_days") or 0)
        add(te, "Duration", duration_pt(duration_days))
        add(te, "DurationFormat", "7")

        if t.get("summary") or t.get("milestone"):
            work_hours = 0
        else:
            num_res = max(len(t.get("resources") or []), 1)
            work_hours = duration_days * HOURS_PER_DAY * num_res
        add(te, "Work", f"PT{work_hours}H0M0S")

        add(te, "ResumeValid", "0")
        add(te, "EffortDriven", "0")
        add(te, "Recurring", "0")
        add(te, "OverAllocated", "0")
        add(te, "Estimated", "0")
        add(te, "Milestone", "1" if t.get("milestone") else "0")
        add(te, "Summary", "1" if t.get("summary") else "0")
        add(te, "DisplayAsSummary", "0")
        add(te, "Critical", "1" if t.get("is_critical") else "0")
        add(te, "IsSubproject", "0")
        add(te, "IsSubprojectReadOnly", "0")
        add(te, "ExternalTask", "0")
        add(te, "FixedCostAccrual", "3")

        pct = int(t.get("pct", 0) or 0)
        remaining_days = int(round(duration_days * (100 - pct) / 100))
        actual_days = duration_days - remaining_days
        add(te, "ActualDuration", duration_pt(actual_days))
        add(te, "RemainingDuration", duration_pt(remaining_days))

        if pct > 0 and not t.get("summary"):
            add(te, "ActualStart", start_str)
        if pct == 100 and not t.get("summary"):
            add(te, "ActualFinish", finish_str)

        add(te, "ConstraintType", "0")
        add(te, "CalendarUID", "-1")
        add(te, "LevelAssignments", "1")
        add(te, "LevelingCanSplit", "1")
        add(te, "IgnoreResourceCalendar", "0")
        add(te, "HideBar", "0")
        add(te, "Rollup", "0")
        add(te, "PercentComplete", str(pct))
        add(te, "PercentWorkComplete", str(pct))

        actual_work = int(work_hours * pct / 100)
        remaining_work = work_hours - actual_work
        add(te, "ActualWork", f"PT{actual_work}H0M0S")
        add(te, "RemainingWork", f"PT{remaining_work}H0M0S")
        add(te, "EarnedValueMethod", "0")

        # Predecessors (bare på ikke-summary)
        if not t.get("summary"):
            for pred in t.get("predecessors_resolved", []):
                pl = ET.SubElement(te, "PredecessorLink")
                add(pl, "PredecessorUID", str(pred["uid"]))
                add(pl, "Type", pred["type"])
                add(pl, "CrossProject", "0")
                # Vi stoler på plannedStart/Finish i JSON; sett lag=0 for å unngå
                # at MS Project overstyrer datoer basert på lag.
                add(pl, "LinkLag", "0")
                add(pl, "LagFormat", "7")

        # ExtendedAttributes (identitet + metadata)
        if t.get("activity_id"):
            add_extended_attr(te, FIELD_TEXT1, t["activity_id"])
        if t.get("task_id"):
            add_extended_attr(te, FIELD_TEXT2, t["task_id"])
        if t.get("wbs_item_id"):
            add_extended_attr(te, FIELD_TEXT3, t["wbs_item_id"])
        add_extended_attr(te, FIELD_TEXT4, "generate_msproject_from_json.py")

    # --- Ressurser ---
    resources_el = ET.SubElement(root, "Resources")

    # UID 0: Unassigned (obligatorisk)
    r0 = ET.SubElement(resources_el, "Resource")
    add(r0, "UID", "0")
    add(r0, "ID", "0")
    add(r0, "Type", "1")
    add(r0, "IsNull", "0")
    add(r0, "MaxUnits", "1.00")
    add(r0, "PeakUnits", "0.00")
    add(r0, "OverAllocated", "0")
    add(r0, "CanLevel", "1")
    add(r0, "AccrueAt", "3")

    for r in resources:
        re_el = ET.SubElement(resources_el, "Resource")
        add(re_el, "UID", str(r["uid"]))
        add(re_el, "ID", str(r["id"]))
        add(re_el, "Name", r["name"])
        add(re_el, "Initials", r["initials"])
        add(re_el, "Type", "1")
        add(re_el, "IsNull", "0")
        add(re_el, "MaxUnits", "1.00")
        add(re_el, "PeakUnits", "1.00")
        add(re_el, "OverAllocated", "0")
        add(re_el, "CanLevel", "1")
        add(re_el, "AccrueAt", "3")
        add(re_el, "StandardRate", "0")
        add(re_el, "StandardRateFormat", "2")
        add(re_el, "OvertimeRate", "0")
        add(re_el, "OvertimeRateFormat", "2")
        add(re_el, "IsGeneric", "0")
        add(re_el, "IsInactive", "0")
        add(re_el, "IsEnterprise", "0")
        add(re_el, "BookingType", "0")
        add(re_el, "IsCostResource", "0")
        add(re_el, "IsBudget", "0")

    # --- Assignments ---
    assignments_el = ET.SubElement(root, "Assignments")
    assignment_uid = 1
    for t in tasks:
        if t.get("summary") or t.get("milestone"):
            continue
        res_uids = t.get("resources") or []
        if not res_uids:
            continue
        units_each = 1.0 / len(res_uids) if len(res_uids) > 1 else 1.0
        duration_days = int(t.get("duration_days") or 0)
        work_hours = duration_days * HOURS_PER_DAY
        pct = int(t.get("pct", 0) or 0)
        for res_uid in res_uids:
            asgn = ET.SubElement(assignments_el, "Assignment")
            add(asgn, "UID", str(assignment_uid))
            add(asgn, "TaskUID", str(t["uid"]))
            add(asgn, "ResourceUID", str(res_uid))
            add(asgn, "PercentWorkComplete", str(pct))
            add(asgn, "Units", f"{units_each:.2f}")
            add(asgn, "Work", f"PT{work_hours}H0M0S")
            add(asgn, "RegularWork", f"PT{work_hours}H0M0S")
            remaining = int(work_hours * (100 - pct) / 100)
            add(asgn, "RemainingWork", f"PT{remaining}H0M0S")
            add(asgn, "Start", t["start"].strftime("%Y-%m-%dT08:00:00"))
            add(asgn, "Finish", t["finish"].strftime("%Y-%m-%dT17:00:00"))
            assignment_uid += 1

    return root


def prettify(element: ET.Element) -> str:
    rough = ET.tostring(element, encoding="unicode", xml_declaration=False)
    parsed = minidom.parseString(rough)
    pretty = parsed.toprettyxml(indent="\t", encoding=None)
    lines = pretty.split("\n")
    lines[0] = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    return "\n".join(line for line in lines if line.strip())


# =====================================================================
# MAIN
# =====================================================================
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generer MSPDI XML fra JSON-kildene i '012 fase 2 - plan/'."
    )
    p.add_argument("--output", "-o", type=Path, default=OUTPUT,
                   help=f"Sti til XML-output (default: {OUTPUT.name})")
    p.add_argument("--mapping-file", type=Path, default=MAPPING_JSON,
                   help=f"Sti til UID-mapping (default: {MAPPING_JSON.name})")
    p.add_argument("--no-mapping", action="store_true",
                   help="Ikke bruk/oppdater mapping-fil (alle UIDs tildeles fra 1)")
    p.add_argument("--dry-run", action="store_true",
                   help="Ikke skriv filer til disk; bare vis hva som ville skjedd")
    p.add_argument("--quiet", "-q", action="store_true",
                   help="Ikke skriv oppgaveliste til konsoll")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    if not args.quiet:
        print(f"Leser JSON-kilder fra: {PLAN_DIR}")
    core, wbs, schedule = load_sources()

    resources = build_resources(core)
    if not args.quiet:
        print(f"  Ressurser: {len(resources)}")

    allocator = UIDAllocator(
        mapping_file=args.mapping_file,
        load_existing=not args.no_mapping,
    )
    existing_before = len(allocator.mapping.get("entries", {}))
    if not args.quiet:
        if args.no_mapping:
            print(f"  UID-mapping: DEAKTIVERT (--no-mapping)")
        else:
            print(f"  Eksisterende UID-mapping: {existing_before} nøkler "
                  f"(fra {args.mapping_file.name})")

    tasks, active_keys = assemble_tasks(wbs, schedule, resources, allocator)
    resolve_predecessors(tasks)
    compute_summary_dates(tasks)

    orphans = [k for k in allocator.mapping.get("entries", {}) if k not in active_keys]
    if orphans and not args.quiet:
        print(f"\n⚠  {len(orphans)} foreldreløs(e) mapping-nøkler "
              f"(finnes ikke lenger i JSON):")
        for k in orphans[:10]:
            print(f"     - {k} (UID={allocator.mapping['entries'][k]})")
        if len(orphans) > 10:
            print(f"     ... og {len(orphans) - 10} flere")

    if allocator.new_keys and not args.quiet:
        print(f"\n+ {len(allocator.new_keys)} ny(e) mapping-nøkler tildelt:")
        for k in allocator.new_keys[:10]:
            print(f"     + {k} (UID={allocator.entries[k]})")
        if len(allocator.new_keys) > 10:
            print(f"     ... og {len(allocator.new_keys) - 10} flere")

    if not args.quiet:
        print("\nOppgaveoversikt:")
        print(f"{'UID':<4} {'WBS':<8} {'Lv':<3} {'Navn':<55} "
              f"{'Start':<12} {'Slutt':<12} {'Dager':>5} {'%':>4}")
        print("-" * 110)
        for t in tasks:
            indent = "  " * (t["level"] - 1)
            flag = " [M]" if t.get("milestone") else (" [S]" if t.get("summary") else "")
            name = (indent + t["name"] + flag)[:55]
            start_str = t["start"].strftime("%d.%m.%Y") if t.get("start") else ""
            finish_str = t["finish"].strftime("%d.%m.%Y") if t.get("finish") else ""
            print(f"{t['uid']:<4} {t.get('wbs_code', ''):<8} {t['level']:<3} "
                  f"{name:<55} {start_str:<12} {finish_str:<12} "
                  f"{t.get('duration_days', 0):>5} {t.get('pct', 0):>3}%")

    if not args.quiet:
        print("\nBygger MSPDI XML...")
    root = build_xml(core, tasks, resources)
    xml_str = prettify(root)

    if args.dry_run:
        if not args.quiet:
            print(f"\n[DRY-RUN] Ville skrevet {len(xml_str)} tegn til: {args.output}")
            print(f"[DRY-RUN] Ville skrevet mapping til: {args.mapping_file}")
    else:
        args.output.write_text(xml_str, encoding="utf-8")
        if not args.no_mapping:
            allocator.save(active_keys)
            if not args.quiet:
                print(f"Mapping oppdatert: {args.mapping_file}")
                print(f"  Gjenbrukt: {len(allocator.hits)}  "
                      f"Ny: {len(allocator.new_keys)}  "
                      f"Foreldreløse: {len(orphans)}")

    leaves = [t for t in tasks if not t.get("summary")]
    project_start = min(t["start"] for t in leaves if t.get("start"))
    project_finish = max(t["finish"] for t in leaves if t.get("finish"))

    if not args.quiet:
        prefix = "[DRY-RUN] " if args.dry_run else ""
        print(f"\n{prefix}Ferdig! Fil: {args.output}")
        print(f"  Totalt:         {len(tasks)} oppgaver (inkl. summaries & milepæler)")
        print(f"  Aktiviteter:    {sum(1 for t in tasks if not t.get('summary') and not t.get('milestone'))}")
        print(f"  Milepæler:      {sum(1 for t in tasks if t.get('milestone'))}")
        print(f"  Ressurser:      {len(resources)}")
        print(f"  Prosjektstart:  {project_start.strftime('%d.%m.%Y')}")
        print(f"  Prosjektslutt:  {project_finish.strftime('%d.%m.%Y')}")
        if not args.dry_run:
            print(f"\nÅpne i MS Project: Fil → Åpne → velg '{args.output.name}'")


if __name__ == "__main__":
    main()
