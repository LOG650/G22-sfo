"""
Tester for JSON ↔ MS Project-integrasjonen.

Kjør (fra repo-root):
  python3 -m pytest "004 data/tests/"            # hele suiten
  python3 -m pytest "004 data/tests/" -v         # verbose
  python3 -m pytest "004 data/tests/" -k uid     # bare UID-tester

Krever pytest: pip install pytest
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = REPO_ROOT / "004 data"
PLAN_DIR = REPO_ROOT / "012 fase 2 - plan"
GENERATOR = DATA_DIR / "generate_msproject_from_json.py"
DIFF_SCRIPT = DATA_DIR / "msproject_to_json_diff.py"
VALIDATOR = DATA_DIR / "validate_msproject_xml.py"
APPLY_SCRIPT = DATA_DIR / "apply_diff.py"

NS = {"m": "http://schemas.microsoft.com/project"}


# =====================================================================
# FIXTURES
# =====================================================================
@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    """Kopi av JSON-kilder + tom output-mappe. Gir isolasjon per test."""
    ws = tmp_path / "ws"
    plan_dst = ws / "plan"
    data_dst = ws / "data"
    plan_dst.mkdir(parents=True)
    data_dst.mkdir(parents=True)
    # Kopier bare JSON-filene vi trenger
    for name in ("core.json", "wbs.json", "schedule.json"):
        shutil.copy(PLAN_DIR / name, plan_dst / name)
    return ws


def run_generator(ws: Path, extra: list[str] | None = None) -> subprocess.CompletedProcess:
    """Kjør generator med custom output/mapping under ws/."""
    xml_out = ws / "data" / "out.xml"
    mapping = ws / "plan" / "msproject-mapping.json"
    cmd = [
        sys.executable, str(GENERATOR),
        "--output", str(xml_out),
        "--mapping-file", str(mapping),
        "--quiet",
    ]
    if extra:
        cmd += extra
    # Patch env slik at generator leser fra ws/plan/ i stedet for repo
    # Enkleste: symlink 012-mappen midlertidig. Siden generator bruker
    # REPO_ROOT-relative stier, kjører vi den som normalt og sjekker
    # mot default mappings etter. For isolasjon bruker vi separate
    # mapping/output-stier.
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))


def load_xml(path: Path) -> ET.ElementTree:
    return ET.parse(path)


def all_task_uids(tree: ET.ElementTree) -> list[int]:
    return [
        int(t.findtext("m:UID", default="0", namespaces=NS))
        for t in tree.findall("m:Tasks/m:Task", NS)
    ]


def task_uid_by_activity_id(tree: ET.ElementTree) -> dict[str, int]:
    """Map ExtendedAttribute Text1 (activity ID) → Task UID."""
    result = {}
    for t in tree.findall("m:Tasks/m:Task", NS):
        uid = int(t.findtext("m:UID", default="0", namespaces=NS))
        for ext in t.findall("m:ExtendedAttribute", NS):
            fid = ext.findtext("m:FieldID", default="", namespaces=NS)
            val = ext.findtext("m:Value", default="", namespaces=NS)
            if fid == "188743731" and val:  # Text1
                result[val] = uid
    return result


# =====================================================================
# TESTER
# =====================================================================
def test_generator_runs_cleanly(workspace: Path):
    """Generatoren kjører og produserer valid XML."""
    r = run_generator(workspace)
    assert r.returncode == 0, f"stderr: {r.stderr}"
    xml_out = workspace / "data" / "out.xml"
    assert xml_out.exists()
    tree = load_xml(xml_out)
    assert tree.getroot().tag.endswith("Project")


def test_structural_validation_passes(workspace: Path):
    """Den genererte XML-en består strukturell validering."""
    run_generator(workspace)
    xml_out = workspace / "data" / "out.xml"
    r = subprocess.run(
        [sys.executable, str(VALIDATOR), "--xml", str(xml_out)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, f"Validator feilet:\n{r.stdout}\n{r.stderr}"


def test_uid_stability_across_runs(workspace: Path):
    """UIDs skal være stabile når JSON ikke endres."""
    run_generator(workspace)
    tree1 = load_xml(workspace / "data" / "out.xml")
    map1 = task_uid_by_activity_id(tree1)

    run_generator(workspace)  # andre kjøring, samme mapping
    tree2 = load_xml(workspace / "data" / "out.xml")
    map2 = task_uid_by_activity_id(tree2)

    assert map1 == map2, "UIDs endret seg mellom to kjøringer"
    assert len(map1) > 10, "For få aktiviteter med ExtendedAttribute"


def test_no_mapping_gives_sequential_uids(workspace: Path):
    """--no-mapping skal gi UIDs 1, 2, 3, ... uten å bruke eksisterende mapping."""
    # Kjør først med mapping for å etablere basis
    run_generator(workspace)

    # Så uten mapping
    r = run_generator(workspace, extra=["--no-mapping"])
    assert r.returncode == 0
    tree = load_xml(workspace / "data" / "out.xml")
    uids = sorted(all_task_uids(tree))
    # UIDs bør være 1..N (evt. med 0 for project)
    non_zero = [u for u in uids if u > 0]
    assert non_zero == list(range(1, len(non_zero) + 1)), \
        f"UIDs er ikke sekvensielle: {non_zero[:10]}..."


def test_dry_run_writes_nothing(workspace: Path):
    """--dry-run skal ikke skape filer."""
    xml_out = workspace / "data" / "out.xml"
    mapping = workspace / "plan" / "msproject-mapping.json"
    r = run_generator(workspace, extra=["--dry-run"])
    assert r.returncode == 0
    assert not xml_out.exists(), "Dry-run skrev likevel XML"
    assert not mapping.exists(), "Dry-run skrev likevel mapping"


def test_predecessor_uids_all_exist(workspace: Path):
    """Alle PredecessorUID-referanser skal peke på eksisterende Task UIDs."""
    run_generator(workspace)
    tree = load_xml(workspace / "data" / "out.xml")
    uids = set(all_task_uids(tree))
    for t in tree.findall("m:Tasks/m:Task", NS):
        for pl in t.findall("m:PredecessorLink", NS):
            pre_uid = int(pl.findtext("m:PredecessorUID", default="0", namespaces=NS))
            assert pre_uid in uids, \
                f"PredecessorUID={pre_uid} peker på ikke-eksisterende task"


def test_extended_attributes_present(workspace: Path):
    """Alle ikke-root-tasks bør ha minst én ExtendedAttribute for identitet."""
    run_generator(workspace)
    tree = load_xml(workspace / "data" / "out.xml")
    tasks = tree.findall("m:Tasks/m:Task", NS)
    # UID 0 er prosjekt-summary og har ikke ExtendedAttribute
    non_project = [
        t for t in tasks
        if int(t.findtext("m:UID", default="0", namespaces=NS)) != 0
    ]
    with_ext = [t for t in non_project if t.find("m:ExtendedAttribute", NS) is not None]
    assert len(with_ext) == len(non_project), \
        f"Fant {len(non_project) - len(with_ext)} tasks uten ExtendedAttribute"


def test_round_trip_diff_clean(workspace: Path):
    """Generer → diff mot samme XML → 0 endringer."""
    run_generator(workspace)
    xml_out = workspace / "data" / "out.xml"
    r = subprocess.run(
        [sys.executable, str(DIFF_SCRIPT),
         "--xml", str(xml_out),
         "--quiet"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    # Exit 0 = ingen endringer (diff-scriptet bruker REPO_ROOT-JSON-kildene)
    assert r.returncode == 0, f"Round-trip diff fant endringer:\n{r.stdout}"


def test_new_activity_gets_new_uid(workspace: Path, monkeypatch):
    """Hvis en ny aktivitet legges til i schedule.json, får den en ny UID
    og eksisterende UIDs endres ikke."""
    # Første kjøring med original schedule
    run_generator(workspace)
    tree1 = load_xml(workspace / "data" / "out.xml")
    map1 = task_uid_by_activity_id(tree1)
    original_uids = set(map1.values())
    existing_max = max(original_uids)

    # Midlertidig modifisere schedule.json i repoet og restaurere etterpå
    schedule_path = PLAN_DIR / "schedule.json"
    backup = schedule_path.read_bytes()
    try:
        schedule = json.loads(backup.decode("utf-8"))
        # Dupliser en aktivitet med ny ID
        new_act = dict(schedule["schedule"]["activities"][-1])
        new_act["activityId"] = "ACT-TEST-NEW"
        new_act["taskId"] = "TEST.NEW"
        new_act["name"] = "TEST NY AKTIVITET"
        schedule["schedule"]["activities"].append(new_act)
        # Legg aktiviteten til en eksisterende WBS (siste)
        wbs_path = PLAN_DIR / "wbs.json"
        wbs_backup = wbs_path.read_bytes()
        try:
            wbs = json.loads(wbs_backup.decode("utf-8"))
            # Finn en work-package for siste fase
            for item in wbs["wbs"]["items"]:
                if item.get("level") == 3 and item.get("parentId") == "WBS-1.4":
                    item.setdefault("activityIds", []).append("ACT-TEST-NEW")
                    break
            wbs_path.write_text(json.dumps(wbs, indent=4, ensure_ascii=False),
                                encoding="utf-8")
            schedule_path.write_text(json.dumps(schedule, indent=4, ensure_ascii=False),
                                     encoding="utf-8")

            # Andre kjøring — den nye aktiviteten skal få ny UID,
            # og de eksisterende UIDs skal være uendret
            run_generator(workspace)
            tree2 = load_xml(workspace / "data" / "out.xml")
            map2 = task_uid_by_activity_id(tree2)

            assert "ACT-TEST-NEW" in map2, "Ny aktivitet fikk ikke UID"
            new_uid = map2["ACT-TEST-NEW"]
            assert new_uid > existing_max, \
                f"Ny UID {new_uid} skal være > eksisterende max {existing_max}"

            # Alle gamle IDs må ha samme UID som før
            for aid, uid in map1.items():
                assert map2.get(aid) == uid, \
                    f"UID for {aid} endret seg: {uid} → {map2.get(aid)}"
        finally:
            wbs_path.write_bytes(wbs_backup)
    finally:
        schedule_path.write_bytes(backup)


def test_all_milestones_have_zero_duration(workspace: Path):
    """Milepæler skal ha Duration=PT0H0M0S og Milestone=1."""
    run_generator(workspace)
    tree = load_xml(workspace / "data" / "out.xml")
    for t in tree.findall("m:Tasks/m:Task", NS):
        if (t.findtext("m:Milestone", default="0", namespaces=NS) or "0") == "1":
            dur = t.findtext("m:Duration", default="", namespaces=NS)
            assert dur == "PT0H0M0S", f"Milepæl har non-zero duration: {dur}"


def test_resources_match_core_json(workspace: Path):
    """Antall ressurser i XML = antall team-medlemmer i core.json (+ UID 0)."""
    core = json.loads((PLAN_DIR / "core.json").read_text(encoding="utf-8"))
    team_size = len(core["project"].get("team", []))

    run_generator(workspace)
    tree = load_xml(workspace / "data" / "out.xml")
    resources = tree.findall("m:Resources/m:Resource", NS)
    # +1 for obligatorisk "Unassigned" UID=0
    assert len(resources) == team_size + 1, \
        f"Forventet {team_size + 1} ressurser, fant {len(resources)}"
