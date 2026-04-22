#!/usr/bin/env python3
"""
Les .mpp (binær MS Project)-fil via MPXJ og konverter til MSPDI XML.

Dette er den anbefalte "Option A" fra integrasjonsforskningen:
  - MPXJ = LGPL, 13+ år moden, Java/Python/.NET-bridge
  - Kan lese .mpp direkte (noe pure Python ikke kan)
  - Skriver til MSPDI XML som vi deretter kan diffe mot JSON-kildene

Krav:
  1. Java JDK 11+
     macOS:    brew install openjdk@17
               sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk \\
                           /Library/Java/JavaVirtualMachines/openjdk-17.jdk
     Ubuntu:   sudo apt-get install openjdk-17-jdk
     Windows:  https://adoptium.net/
  2. Sett JAVA_HOME i miljøet (hvis ikke auto-detektert)
  3. pip install mpxj  (pulls JPype1 som avhengighet)

Kjør (eksempel):
  python3 "004 data/read_mpp_mpxj.py" --mpp "plan.mpp" --output "plan_converted.xml"

Integrasjon med resten av pipelinen:
  .mpp → [read_mpp_mpxj.py] → MSPDI XML → [msproject_to_json_diff.py] → diff
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def check_mpxj_available() -> tuple[bool, str]:
    """Returner (ok, melding). ok=True hvis MPXJ kan brukes."""
    try:
        import jpype  # noqa: F401
    except ImportError:
        return False, (
            "JPype er ikke installert.\n"
            "  Kjør: pip install mpxj\n"
            "  (pip installerer både mpxj og JPype1 automatisk)"
        )
    try:
        import mpxj  # noqa: F401
    except ImportError:
        return False, (
            "MPXJ er ikke installert.\n"
            "  Kjør: pip install mpxj"
        )
    import os
    java_home = os.environ.get("JAVA_HOME")
    if not java_home:
        return False, (
            "JAVA_HOME er ikke satt. MPXJ trenger Java JDK 11+.\n"
            "  macOS:  brew install openjdk@17 && "
            "export JAVA_HOME=$(/usr/libexec/java_home -v17)\n"
            "  Ubuntu: sudo apt-get install openjdk-17-jdk && "
            "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64"
        )
    java_exe = Path(java_home) / "bin" / "java"
    if not java_exe.exists():
        return False, f"JAVA_HOME={java_home} peker ikke på en gyldig JDK."
    return True, f"MPXJ klar. JAVA_HOME={java_home}"


def convert_mpp_to_mspdi(mpp_path: Path, output_path: Path) -> None:
    """Les .mpp og skriv MSPDI XML."""
    import jpype
    import jpype.imports

    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[str(Path(__file__).parent)])

    from net.sf.mpxj.reader import UniversalProjectReader
    from net.sf.mpxj.writer import UniversalProjectWriter
    from net.sf.mpxj import FileFormat

    print(f"Leser: {mpp_path}")
    reader = UniversalProjectReader()
    project_file = reader.read(str(mpp_path))

    print(f"Skriver MSPDI XML: {output_path}")
    writer = UniversalProjectWriter(FileFormat.MSPDI)
    writer.write(project_file, str(output_path))
    print("Ferdig.")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Konverter .mpp (binær) til MSPDI XML via MPXJ.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--mpp", type=Path, required=False,
                   help="Sti til .mpp-fil som skal leses")
    p.add_argument("--output", "-o", type=Path, default=None,
                   help="Sti til MSPDI XML-output")
    p.add_argument("--check", action="store_true",
                   help="Bare sjekk at MPXJ-oppsett fungerer, ikke konverter")
    args = p.parse_args()

    ok, msg = check_mpxj_available()
    print(msg)
    if args.check:
        sys.exit(0 if ok else 1)

    if not ok:
        print("\nMPXJ-oppsett mangler. Se melding over. Installasjonsguide:", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    if not args.mpp:
        print("FEIL: --mpp er påkrevd når du vil konvertere.", file=sys.stderr)
        sys.exit(2)
    if not args.mpp.exists():
        print(f"FEIL: MPP-fil finnes ikke: {args.mpp}", file=sys.stderr)
        sys.exit(1)

    output = args.output or args.mpp.with_suffix(".xml")
    try:
        convert_mpp_to_mspdi(args.mpp, output)
    except Exception as e:
        print(f"FEIL under MPXJ-konvertering: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
