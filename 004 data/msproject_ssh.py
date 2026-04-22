#!/usr/bin/env python3
"""
SSH-bro til Windows-VM med MS Project (kjører i UTM).

Gir macOS-siden mulighet til å:
  - Starte MS Project headless og åpne en XML-fil (COM automation via PowerShell)
  - Be MS Project re-lagre filen som normalisert MSPDI XML
  - Lukke MS Project (frigjøre fillås) før videre diff/apply
  - Verifisere at MS Project kan åpne en fil uten feilmeldinger

Konfigurasjon (ett av to):
  1. Environment-variabler:
       MSPROJECT_SSH_HOST=192.168.64.10
       MSPROJECT_SSH_USER=sebastian
       MSPROJECT_SSH_PORT=22          (valgfri, default 22)
       MSPROJECT_SSH_KEY=~/.ssh/id_ed25519  (valgfri)
       MSPROJECT_WIN_SHARE=Z:         (drive-bokstav hvor 004 data er mounted)
  2. Fil ~/.config/log650/msproject-ssh.json:
       {
         "host": "192.168.64.10",
         "user": "sebastian",
         "port": 22,
         "key": "~/.ssh/id_ed25519",
         "winShare": "Z:"
       }

Kjør:
  python3 "004 data/msproject_ssh.py" check          # kobler, sjekker Windows-siden
  python3 "004 data/msproject_ssh.py" normalize FIL  # åpner+lagrer XML i MS Project
  python3 "004 data/msproject_ssh.py" verify FIL     # bekrefter at MS Project kan åpne
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = Path.home() / ".config" / "log650" / "msproject-ssh.json"


@dataclass
class SSHConfig:
    host: str
    user: str
    port: int = 22
    key: str | None = None
    win_share: str = "Z:"   # Windows drive-bokstav hvor shared folder er mounted

    @classmethod
    def load(cls) -> "SSHConfig | None":
        # 1. Env vars
        host = os.environ.get("MSPROJECT_SSH_HOST")
        user = os.environ.get("MSPROJECT_SSH_USER")
        if host and user:
            return cls(
                host=host,
                user=user,
                port=int(os.environ.get("MSPROJECT_SSH_PORT", "22")),
                key=os.environ.get("MSPROJECT_SSH_KEY"),
                win_share=os.environ.get("MSPROJECT_WIN_SHARE", "Z:"),
            )
        # 2. Config-fil
        if CONFIG_FILE.exists():
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return cls(
                host=data["host"],
                user=data["user"],
                port=int(data.get("port", 22)),
                key=data.get("key"),
                win_share=data.get("winShare", "Z:"),
            )
        return None

    def ssh_args(self) -> list[str]:
        args = ["ssh", "-p", str(self.port),
                "-o", "ConnectTimeout=5",
                "-o", "StrictHostKeyChecking=accept-new",
                "-o", "BatchMode=yes"]
        if self.key:
            args += ["-i", os.path.expanduser(self.key)]
        args.append(f"{self.user}@{self.host}")
        return args


def run_ssh(cfg: SSHConfig, remote_cmd: str, timeout: int = 60) -> subprocess.CompletedProcess:
    """Kjør en kommando via SSH mot Windows-VMen."""
    cmd = cfg.ssh_args() + [remote_cmd]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def run_powershell(cfg: SSHConfig, ps_script: str, timeout: int = 120) -> subprocess.CompletedProcess:
    """Kjør et PowerShell-script på Windows-siden."""
    # Encode som base64 for å unngå quoting-helvete
    import base64
    encoded = base64.b64encode(ps_script.encode("utf-16-le")).decode("ascii")
    return run_ssh(cfg, f"powershell -EncodedCommand {encoded}", timeout=timeout)


# =====================================================================
# POWERSHELL-SCRIPTS
# =====================================================================
PS_CHECK = r"""
$ErrorActionPreference = 'Stop'
$result = @{}
$result['host'] = $env:COMPUTERNAME
$result['user'] = $env:USERNAME
$result['osVersion'] = (Get-CimInstance Win32_OperatingSystem).Version
$result['powerShellVersion'] = $PSVersionTable.PSVersion.ToString()

# Sjekk shared folder
$share = 'Z:\'
if (Test-Path $share) {
    $result['shareAccessible'] = $true
    $result['shareFiles'] = (Get-ChildItem $share -Filter '*.xml' -ErrorAction SilentlyContinue |
                             Select-Object -ExpandProperty Name) -join ','
} else {
    $result['shareAccessible'] = $false
}

# Sjekk MS Project
try {
    $app = New-Object -ComObject MSProject.Application
    $result['msProjectAvailable'] = $true
    $result['msProjectVersion'] = $app.Version
    $result['msProjectBuild'] = $app.Build
    $app.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
    [GC]::Collect()
} catch {
    $result['msProjectAvailable'] = $false
    $result['msProjectError'] = $_.Exception.Message
}

$result | ConvertTo-Json
"""

PS_NORMALIZE = r"""
param(
    [Parameter(Mandatory=$true)][string]$FilePath
)
$ErrorActionPreference = 'Stop'
$result = @{}

if (-not (Test-Path $FilePath)) {
    $result['success'] = $false
    $result['error'] = "Fil finnes ikke: $FilePath"
    $result | ConvertTo-Json
    exit 1
}

try {
    $app = New-Object -ComObject MSProject.Application
    $app.Visible = $false
    $app.DisplayAlerts = $false

    # Åpne fila
    $app.FileOpenEx($FilePath, $false)
    $proj = $app.ActiveProject
    $result['tasksLoaded'] = $proj.Tasks.Count
    $result['projectName'] = $proj.Name

    # Lagre som MSPDI XML (overskriver)
    $app.FileSaveAs($FilePath, 'xml')

    # Lukk uten ytterligere prompts
    $proj.ClearBaseline()  # no-op, bare for å unngå dialog
    $app.FileClose(0)  # 0 = pjDoNotSave (vi har allerede lagret)
    $app.Quit()

    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()

    $result['success'] = $true
} catch {
    $result['success'] = $false
    $result['error'] = $_.Exception.Message
    try { $app.Quit() } catch {}
}

$result | ConvertTo-Json
"""

PS_VERIFY = r"""
param(
    [Parameter(Mandatory=$true)][string]$FilePath
)
$ErrorActionPreference = 'Stop'
$result = @{}

if (-not (Test-Path $FilePath)) {
    $result['success'] = $false
    $result['error'] = "Fil finnes ikke: $FilePath"
    $result | ConvertTo-Json
    exit 1
}

try {
    $app = New-Object -ComObject MSProject.Application
    $app.Visible = $false
    $app.DisplayAlerts = $false

    $app.FileOpenEx($FilePath, $true)  # read-only
    $proj = $app.ActiveProject
    $result['tasks'] = $proj.Tasks.Count
    $result['resources'] = $proj.Resources.Count
    $result['projectName'] = $proj.Name
    $result['startDate'] = $proj.ProjectStart.ToString('yyyy-MM-dd')
    $result['finishDate'] = $proj.ProjectFinish.ToString('yyyy-MM-dd')

    $app.FileClose(0)
    $app.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
    [GC]::Collect()

    $result['success'] = $true
} catch {
    $result['success'] = $false
    $result['error'] = $_.Exception.Message
    try { $app.Quit() } catch {}
}

$result | ConvertTo-Json
"""


# =====================================================================
# STI-KONVERTERING
# =====================================================================
def to_windows_path(cfg: SSHConfig, mac_path: Path) -> str:
    """
    Konverter mac-sti (f.eks. /Volumes/.../004 data/foo.xml) til Windows-sti
    relativt til shared folder (f.eks. Z:\\foo.xml).
    """
    mac_path = mac_path.resolve()
    share_root = REPO_ROOT / "004 data"
    try:
        rel = mac_path.relative_to(share_root)
    except ValueError:
        raise ValueError(
            f"Filen må ligge under {share_root} for at VirtioFS-mappingen skal gjelde. "
            f"Fikk: {mac_path}"
        )
    return cfg.win_share + "\\" + str(rel).replace("/", "\\")


# =====================================================================
# HØYNIVÅ API
# =====================================================================
def check(cfg: SSHConfig) -> dict:
    result = run_powershell(cfg, PS_CHECK, timeout=30)
    if result.returncode != 0:
        return {"error": f"SSH/PowerShell feilet: {result.stderr.strip()}"}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "Kunne ikke parse PowerShell-output", "raw": result.stdout}


def normalize(cfg: SSHConfig, xml_path: Path) -> dict:
    win_path = to_windows_path(cfg, xml_path)
    script = f"{PS_NORMALIZE}\n\n. {{ param($p) Invoke-Expression ... }}"
    # Enklere: interpolér param direkte
    wrapped = PS_NORMALIZE.replace(
        "param(\n    [Parameter(Mandatory=$true)][string]$FilePath\n)",
        f'$FilePath = "{win_path}"'
    )
    result = run_powershell(cfg, wrapped, timeout=120)
    if result.returncode != 0:
        return {"success": False, "error": result.stderr.strip()}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"success": False, "error": "JSON-parse feilet", "raw": result.stdout}


def verify(cfg: SSHConfig, xml_path: Path) -> dict:
    win_path = to_windows_path(cfg, xml_path)
    wrapped = PS_VERIFY.replace(
        "param(\n    [Parameter(Mandatory=$true)][string]$FilePath\n)",
        f'$FilePath = "{win_path}"'
    )
    result = run_powershell(cfg, wrapped, timeout=60)
    if result.returncode != 0:
        return {"success": False, "error": result.stderr.strip()}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"success": False, "error": "JSON-parse feilet", "raw": result.stdout}


# =====================================================================
# CLI
# =====================================================================
def cmd_check(args) -> int:
    cfg = SSHConfig.load()
    if not cfg:
        print("Ingen SSH-konfig. Se --help for hvordan sette den opp.", file=sys.stderr)
        return 2
    print(f"SSH-config: {cfg.user}@{cfg.host}:{cfg.port} (winShare={cfg.win_share})")
    info = check(cfg)
    if "error" in info:
        print(f"✗ {info['error']}", file=sys.stderr)
        return 1
    print(f"✓ Tilkobling OK — Windows {info.get('osVersion')} som {info.get('user')}")
    print(f"  Shared folder {cfg.win_share} tilgjengelig: {info.get('shareAccessible')}")
    print(f"  MS Project: {info.get('msProjectAvailable')} "
          f"(versjon {info.get('msProjectVersion', '?')})")
    if info.get("shareFiles"):
        print(f"  XML-filer i share: {info['shareFiles']}")
    return 0


def cmd_normalize(args) -> int:
    cfg = SSHConfig.load()
    if not cfg:
        print("Ingen SSH-konfig.", file=sys.stderr)
        return 2
    print(f"Normaliserer {args.path} via MS Project på {cfg.host}...")
    info = normalize(cfg, args.path)
    if info.get("success"):
        print(f"✓ Normalisert — {info.get('tasksLoaded')} oppgaver, "
              f"prosjekt: {info.get('projectName')}")
        return 0
    print(f"✗ {info.get('error', 'ukjent feil')}", file=sys.stderr)
    return 1


def cmd_verify(args) -> int:
    cfg = SSHConfig.load()
    if not cfg:
        print("Ingen SSH-konfig.", file=sys.stderr)
        return 2
    info = verify(cfg, args.path)
    if info.get("success"):
        print(f"✓ MS Project kan åpne {args.path.name}")
        print(f"  Navn: {info.get('projectName')}")
        print(f"  Oppgaver: {info.get('tasks')}  Ressurser: {info.get('resources')}")
        print(f"  Periode: {info.get('startDate')} → {info.get('finishDate')}")
        return 0
    print(f"✗ MS Project kunne ikke åpne filen: {info.get('error')}", file=sys.stderr)
    return 1


def cmd_setup_help(args) -> int:
    print("""
Oppsett av SSH-tilgang til Windows-VMen med MS Project:

1. I Windows (PowerShell som admin):
   Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
   Start-Service sshd
   Set-Service -Name sshd -StartupType Automatic
   New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server' `
     -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22

2. Kopiér din Mac-public-key til Windows:
   cat ~/.ssh/id_ed25519.pub
   # Lim innholdet inn i C:\\Users\\<brukernavn>\\.ssh\\authorized_keys på Windows

3. Finn VM-IP på Windows:
   ipconfig

4. Lag config-fil på Mac:
   mkdir -p ~/.config/log650
   cat > ~/.config/log650/msproject-ssh.json <<EOF
   {
     "host": "192.168.64.10",
     "user": "sebastian",
     "port": 22,
     "key": "~/.ssh/id_ed25519",
     "winShare": "Z:"
   }
   EOF

5. Test:
   python3 "004 data/msproject_ssh.py" check
""")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(
        description="SSH-bro til Windows-VM for MS Project-automasjon"
    )
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="Sjekk SSH-tilkobling og Windows-tilstand")

    p_norm = sub.add_parser("normalize",
                             help="Åpne XML i MS Project og lagre tilbake (normalisering)")
    p_norm.add_argument("path", type=Path)

    p_ver = sub.add_parser("verify", help="Bekreft at MS Project kan åpne filen")
    p_ver.add_argument("path", type=Path)

    sub.add_parser("setup-help", help="Vis oppsett-instruksjoner")

    args = p.parse_args()

    handler = {
        "check": cmd_check,
        "normalize": cmd_normalize,
        "verify": cmd_verify,
        "setup-help": cmd_setup_help,
    }[args.command]
    sys.exit(handler(args))


if __name__ == "__main__":
    main()
