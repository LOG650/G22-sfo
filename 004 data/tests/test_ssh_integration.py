"""
SSH-avhengige integrasjonstester. Kjører MS Project headless i Windows-VM
og verifiserer round-trip-fidelity mot JSON-kildene.

Disse testene SKIPPES automatisk hvis SSH-konfig mangler eller VMen ikke
er tilgjengelig. For å aktivere: følg oppsett i "004 data/msproject_ssh.py
setup-help".

Kjør:
  python3 -m pytest "004 data/tests/test_ssh_integration.py" -v
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = REPO_ROOT / "004 data"
GENERATOR = DATA_DIR / "generate_msproject_from_json.py"
DIFF_SCRIPT = DATA_DIR / "msproject_to_json_diff.py"
SSH_SCRIPT = DATA_DIR / "msproject_ssh.py"
DEFAULT_XML = DATA_DIR / "LOG650_G22_from_json.xml"


# Sjekk SSH-tilgjengelighet én gang
def _ssh_available() -> bool:
    try:
        r = subprocess.run(
            [sys.executable, str(SSH_SCRIPT), "check"],
            capture_output=True, text=True, timeout=15,
        )
        return r.returncode == 0
    except Exception:
        return False


SSH_OK = _ssh_available()
requires_ssh = pytest.mark.skipif(not SSH_OK,
                                    reason="SSH til Windows-VM ikke tilgjengelig")


@requires_ssh
def test_ms_project_can_open_generated_xml():
    """MS Project skal kunne åpne den genererte XML-filen uten feil."""
    # Sørg for at XML finnes
    subprocess.run([sys.executable, str(GENERATOR), "--quiet"],
                   check=True, cwd=str(REPO_ROOT))

    r = subprocess.run(
        [sys.executable, str(SSH_SCRIPT), "verify", str(DEFAULT_XML)],
        capture_output=True, text=True, timeout=120,
    )
    assert r.returncode == 0, \
        f"MS Project kunne ikke åpne filen:\n{r.stdout}\n{r.stderr}"
    assert "Tasks" in r.stdout or "Oppgaver" in r.stdout


@requires_ssh
@pytest.mark.xfail(
    reason="MS Project FileSaveAs-COM henger på ARM Windows 11 via emulator. "
           "Normalize er ikke-kritisk for kjerne-workflow. Verify dekker "
           "MS Project-validering.",
    run=False,
)
def test_ms_project_round_trip_preserves_activity_ids():
    """
    Etter at MS Project åpner og lagrer XML-en på nytt,
    skal diffen mot JSON fortsatt være clean. Deaktivert pga COM-hang.
    """
    pass


def test_ssh_config_or_skip_gracefully():
    """SSH-scriptet skal exit med kode 2 hvis config mangler."""
    import os
    env = os.environ.copy()
    for var in ("MSPROJECT_SSH_HOST", "MSPROJECT_SSH_USER",
                "MSPROJECT_SSH_PORT", "MSPROJECT_SSH_KEY"):
        env.pop(var, None)

    # Simuler manglende config-fil via tom HOME
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        env["HOME"] = tmp
        r = subprocess.run(
            [sys.executable, str(SSH_SCRIPT), "check"],
            capture_output=True, text=True, env=env, timeout=10,
        )
        # Uten config: exit 2 (graceful)
        assert r.returncode == 2, \
            f"Uten config bør exit=2, fikk {r.returncode}\n{r.stderr}"
