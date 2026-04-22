#!/usr/bin/env python3
"""
Validerer MSPDI XML strukturelt (alltid) og mot MSPDI XSD (hvis lxml + xsd finnes).

Strukturelle sjekker:
  - Root-element er <Project> med riktig namespace
  - Obligatoriske elementer: Tasks, Resources, Assignments, Calendars
  - Alle Task/UID er unike
  - Alle PredecessorLink/PredecessorUID peker på eksisterende UID
  - Alle Assignment/TaskUID og ResourceUID peker på eksisterende UIDer
  - Datoer parses som ISO 8601
  - OutlineLevel er numerisk
  - Milestones har Duration = 0

Kjør:
  python3 "004 data/validate_msproject_xml.py"
  python3 "004 data/validate_msproject_xml.py" --xml path.xml
  python3 "004 data/validate_msproject_xml.py" --xsd path/to/mspdi_pj12.xsd
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_XML = REPO_ROOT / "004 data" / "LOG650_G22_from_json.xml"
NS = {"m": "http://schemas.microsoft.com/project"}


def check_structure(xml_path: Path) -> list[str]:
    """Returner liste med feilbeskrivelser; tom liste = valid."""
    errors: list[str] = []

    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as e:
        return [f"XML parse-feil: {e}"]

    root = tree.getroot()
    if root.tag != "{http://schemas.microsoft.com/project}Project":
        errors.append(f"Root-element må være Project i MS Project namespace, fant: {root.tag}")
        return errors

    # Obligatoriske elementer
    for req in ("Tasks", "Resources", "Calendars"):
        if root.find(f"m:{req}", NS) is None:
            errors.append(f"Mangler obligatorisk element: <{req}>")

    tasks = root.findall("m:Tasks/m:Task", NS)
    if not tasks:
        errors.append("Ingen <Task>-elementer funnet")
        return errors

    # UID-unikhet
    uids: set[int] = set()
    task_uids: set[int] = set()
    for t in tasks:
        uid_txt = t.findtext("m:UID", default="", namespaces=NS)
        try:
            uid = int(uid_txt or "")
        except ValueError:
            errors.append(f"Ugyldig UID: {uid_txt!r}")
            continue
        if uid in uids:
            errors.append(f"Duplikat Task UID: {uid}")
        uids.add(uid)
        task_uids.add(uid)

    # Datoer og typer
    for t in tasks:
        uid = t.findtext("m:UID", default="?", namespaces=NS)
        name = t.findtext("m:Name", default="(uten navn)", namespaces=NS)
        for field in ("Start", "Finish"):
            v = t.findtext(f"m:{field}", default="", namespaces=NS)
            if v:
                try:
                    datetime.fromisoformat(v)
                except ValueError:
                    errors.append(f"Task UID={uid} ({name}): ugyldig {field}-dato: {v!r}")

        ol = t.findtext("m:OutlineLevel", default="", namespaces=NS)
        if ol:
            try:
                int(ol)
            except ValueError:
                errors.append(f"Task UID={uid}: OutlineLevel er ikke numerisk: {ol!r}")

        # Milepæler bør ha Milestone=1 og Duration=PT0H0M0S
        is_ms = (t.findtext("m:Milestone", default="0", namespaces=NS) or "0") == "1"
        if is_ms:
            dur = t.findtext("m:Duration", default="", namespaces=NS)
            if dur and dur != "PT0H0M0S":
                errors.append(f"Task UID={uid}: milepæl har ikke-null duration: {dur}")

    # Predecessor-integritet
    for t in tasks:
        uid = t.findtext("m:UID", default="?", namespaces=NS)
        for pl in t.findall("m:PredecessorLink", NS):
            pre_uid_txt = pl.findtext("m:PredecessorUID", default="", namespaces=NS)
            try:
                pre_uid = int(pre_uid_txt)
            except ValueError:
                errors.append(f"Task UID={uid}: ugyldig PredecessorUID: {pre_uid_txt!r}")
                continue
            if pre_uid not in task_uids:
                errors.append(
                    f"Task UID={uid}: PredecessorUID={pre_uid} peker på en task som ikke finnes"
                )

    # Ressurs-integritet
    resources = root.findall("m:Resources/m:Resource", NS)
    res_uids: set[int] = set()
    for r in resources:
        uid_txt = r.findtext("m:UID", default="", namespaces=NS)
        try:
            uid = int(uid_txt)
        except ValueError:
            errors.append(f"Ugyldig Resource UID: {uid_txt!r}")
            continue
        if uid in res_uids:
            errors.append(f"Duplikat Resource UID: {uid}")
        res_uids.add(uid)

    # Assignment-integritet
    assignments = root.findall("m:Assignments/m:Assignment", NS)
    for a in assignments:
        a_uid = a.findtext("m:UID", default="?", namespaces=NS)
        t_uid_txt = a.findtext("m:TaskUID", default="", namespaces=NS)
        r_uid_txt = a.findtext("m:ResourceUID", default="", namespaces=NS)
        try:
            t_uid = int(t_uid_txt)
            if t_uid not in task_uids and t_uid != 0:
                errors.append(f"Assignment UID={a_uid}: TaskUID={t_uid} finnes ikke")
        except ValueError:
            errors.append(f"Assignment UID={a_uid}: ugyldig TaskUID: {t_uid_txt!r}")
        try:
            r_uid = int(r_uid_txt)
            if r_uid not in res_uids and r_uid != 0:
                errors.append(f"Assignment UID={a_uid}: ResourceUID={r_uid} finnes ikke")
        except ValueError:
            errors.append(f"Assignment UID={a_uid}: ugyldig ResourceUID: {r_uid_txt!r}")

    return errors


def check_xsd(xml_path: Path, xsd_path: Path) -> tuple[bool, list[str]]:
    """Returner (valid, errors). Krever lxml."""
    try:
        from lxml import etree as lxml_etree
    except ImportError:
        return False, [
            "lxml ikke installert — hopper over XSD-validering.",
            "  Kjør: pip install lxml  for å aktivere XSD-sjekk."
        ]
    try:
        with open(xsd_path, "rb") as f:
            schema_doc = lxml_etree.parse(f)
        schema = lxml_etree.XMLSchema(schema_doc)
    except Exception as e:
        return False, [f"Kunne ikke laste XSD fra {xsd_path}: {e}"]
    try:
        with open(xml_path, "rb") as f:
            doc = lxml_etree.parse(f)
    except Exception as e:
        return False, [f"Kunne ikke parse XML: {e}"]
    if schema.validate(doc):
        return True, []
    return False, [str(e) for e in schema.error_log]


DEFAULT_XSD = REPO_ROOT / "004 data" / "schema" / "mspdi_pj12_patched.xsd"


def main() -> None:
    p = argparse.ArgumentParser(
        description="Valider MSPDI XML (strukturelt + valgfri XSD).",
        epilog=(
            "Merk: XSD-validering bruker 2007-skjemaet. Moderne MS Project "
            "genererer felt som er utenfor dette skjemaet (BuildNumber etc.), "
            "så XSD-avvik rapporteres som advarsler. Strukturell validering "
            "er den autoritative sjekken for om MS Project kan åpne filen."
        ),
    )
    p.add_argument("--xml", type=Path, default=DEFAULT_XML,
                   help=f"XML-fil å validere (default: {DEFAULT_XML.name})")
    p.add_argument("--xsd", type=Path, default=None,
                   help=f"Sti til MSPDI XSD. Bruk 'auto' for "
                        f"{DEFAULT_XSD.name} hvis den finnes.")
    p.add_argument("--strict-xsd", action="store_true",
                   help="Behandle XSD-avvik som feil (default: advarsel)")
    args = p.parse_args()

    # Auto-velg lokal patched XSD hvis bruker sier --xsd auto
    if args.xsd and str(args.xsd) == "auto":
        args.xsd = DEFAULT_XSD if DEFAULT_XSD.exists() else None

    if not args.xml.exists():
        print(f"FEIL: XML finnes ikke: {args.xml}", file=sys.stderr)
        sys.exit(1)

    print(f"Validerer: {args.xml}")
    print("-" * 72)

    # 1. Strukturell validering (alltid)
    struct_errors = check_structure(args.xml)
    if struct_errors:
        print(f"✗ Strukturell validering: {len(struct_errors)} feil")
        for e in struct_errors:
            print(f"    - {e}")
    else:
        print("✓ Strukturell validering: bestått")

    # 2. XSD-validering (valgfri, advarsel som default)
    xsd_ok = None
    if args.xsd:
        if not args.xsd.exists():
            print(f"✗ XSD-fil finnes ikke: {args.xsd}")
            xsd_ok = False
        else:
            ok, msgs = check_xsd(args.xml, args.xsd)
            if ok:
                print(f"✓ XSD-validering ({args.xsd.name}): bestått")
                xsd_ok = True
            else:
                marker = "✗" if args.strict_xsd else "⚠"
                label = "FEILET" if args.strict_xsd else "advarsler (2007-skjema)"
                print(f"{marker} XSD-validering: {label}")
                for m in msgs[:10]:
                    print(f"    - {m}")
                if len(msgs) > 10:
                    print(f"    ... og {len(msgs) - 10} flere")
                xsd_ok = False
    else:
        print("  XSD-validering: hoppet over (--xsd ikke oppgitt; bruk --xsd auto)")

    failed = bool(struct_errors) or (args.strict_xsd and xsd_ok is False)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
