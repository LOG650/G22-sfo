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
    # Staging-mappe på Windows hvor XML-filer lastes opp for MS Project-operasjoner.
    # Opprettes automatisk. Default: C:\Users\<user>\Documents\log650-staging
    win_staging: str | None = None

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
                win_staging=os.environ.get("MSPROJECT_WIN_STAGING"),
            )
        # 2. Config-fil
        if CONFIG_FILE.exists():
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return cls(
                host=data["host"],
                user=data["user"],
                port=int(data.get("port", 22)),
                key=data.get("key"),
                win_staging=data.get("winStaging"),
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

    def scp_args(self) -> list[str]:
        args = ["scp", "-P", str(self.port),
                "-o", "ConnectTimeout=5",
                "-o", "StrictHostKeyChecking=accept-new",
                "-o", "BatchMode=yes"]
        if self.key:
            args += ["-i", os.path.expanduser(self.key)]
        return args

    def staging_path(self) -> str:
        """Returnér Windows staging-mappen (default under Documents)."""
        return self.win_staging or f"C:\\Users\\{self.user}\\Documents\\log650-staging"


def run_ssh(cfg: SSHConfig, remote_cmd: str, timeout: int = 60) -> subprocess.CompletedProcess:
    """Kjør en kommando via SSH mot Windows-VMen."""
    cmd = cfg.ssh_args() + [remote_cmd]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def run_powershell(cfg: SSHConfig, ps_script: str, timeout: int = 120) -> subprocess.CompletedProcess:
    """Kjør et PowerShell-script på Windows-siden."""
    # Prepend: silence progress, stop on error, og rydd eventuelle zombie MS Project-prosesser
    prefix = (
        "$ProgressPreference='SilentlyContinue'; "
        "$ErrorActionPreference='Stop'; "
        "Get-Process WINPROJ -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue; "
        "Start-Sleep -Milliseconds 200; "
    )
    full = prefix + ps_script
    # Encode som base64 for å unngå quoting-helvete
    import base64
    encoded = base64.b64encode(full.encode("utf-16-le")).decode("ascii")
    # -NonInteractive + -NoProfile + -OutputFormat Text gir ren JSON uten CLIXML
    remote = (f"powershell.exe -NonInteractive -NoProfile -OutputFormat Text "
              f"-ExecutionPolicy Bypass -EncodedCommand {encoded}")
    return run_ssh(cfg, remote, timeout=timeout)


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

# Sørg for at staging-mappen finnes
$staging = '__STAGING__'
if (-not (Test-Path $staging)) {
    New-Item -ItemType Directory -Force -Path $staging | Out-Null
}
$result['stagingDir'] = $staging
$result['stagingExists'] = (Test-Path $staging)
$result['stagingFiles'] = (Get-ChildItem $staging -Filter '*.xml' -ErrorAction SilentlyContinue |
                           Select-Object -ExpandProperty Name) -join ','

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

# Lagre til midlertidig fil for å unngå overskrive-dialog
$tmpPath = $FilePath + '.normalized.xml'
if (Test-Path $tmpPath) { Remove-Item $tmpPath -Force }

$app = $null
try {
    $app = New-Object -ComObject MSProject.Application
    $app.Visible = $false
    $app.DisplayAlerts = $false
    # pjDoNotSaveChanges = 0
    # pjXML = 12 (MSPDI XML format)

    $app.FileOpenEx($FilePath, $false) | Out-Null
    $proj = $app.ActiveProject
    $result['tasksLoaded'] = $proj.Tasks.Count
    $result['projectName'] = $proj.Name

    # FileSaveAs med pjXML (12) til ny sti — ingen overskrivings-prompt
    $app.FileSaveAs($tmpPath, 12) | Out-Null

    $app.FileCloseEx(0) | Out-Null
    $app.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
    $app = $null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()

    # Bytt ut original med normalisert
    if (Test-Path $tmpPath) {
        Move-Item -Path $tmpPath -Destination $FilePath -Force
        $result['success'] = $true
    } else {
        $result['success'] = $false
        $result['error'] = "Normalisert fil ble ikke skrevet"
    }
} catch {
    $result['success'] = $false
    $result['error'] = $_.Exception.Message
    if ($app) { try { $app.Quit() } catch {} }
    # Hvis hengt, drep WINPROJ
    Get-Process WINPROJ -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
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

    $app.FileOpenEx($FilePath, $true) | Out-Null  # read-only
    $proj = $app.ActiveProject
    $result['tasks'] = $proj.Tasks.Count
    $result['resources'] = $proj.Resources.Count
    $result['projectName'] = $proj.Name
    $result['startDate'] = $proj.ProjectStart.ToString('yyyy-MM-dd')
    $result['finishDate'] = $proj.ProjectFinish.ToString('yyyy-MM-dd')

    $app.FileClose(0) | Out-Null
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


def _parse_json_tolerant(text: str) -> dict:
    """Finn JSON-objekt i output som kan ha støy før/etter (PowerShell bool-output etc)."""
    text = text.strip()
    if not text:
        return {"success": False, "error": "Tom output fra PowerShell"}
    # Finn første '{' og siste '}' for å ekstrahere JSON-blokken
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    return {"success": False, "error": "JSON-parse feilet", "raw": text[:500]}


# =====================================================================
# SCP FILOVERFØRING
# =====================================================================
def upload(cfg: SSHConfig, local_path: Path, remote_name: str | None = None) -> str:
    """
    Last opp en lokal fil til staging-mappen på Windows. Returnerer Windows-stien.
    Oppretter staging-mappen hvis den ikke finnes.
    """
    local_path = local_path.resolve()
    if not local_path.exists():
        raise FileNotFoundError(local_path)
    staging = cfg.staging_path()
    name = remote_name or local_path.name
    win_path = f"{staging}\\{name}"

    # Sørg for at staging-mappen finnes
    mk = run_ssh(cfg, f'if not exist "{staging}" mkdir "{staging}"', timeout=10)
    # Bruk PowerShell for robusthet (default shell er PowerShell)
    mk_ps = run_powershell(
        cfg,
        f"if (-not (Test-Path '{staging}')) {{ New-Item -ItemType Directory -Force -Path '{staging}' | Out-Null }}",
        timeout=10,
    )

    # Windows-sti med framslash er OK i scp-destinasjonen, men bruk SCP-kompatibel form
    # Vi bruker POSIX-lignende sti i scp-kommandoen og PowerShell konverterer
    scp_dest = f"{cfg.user}@{cfg.host}:"
    # Bruk en remote filnavn som er enklere for scp — skriv til Documents-området
    # Formatet for scp til Windows OpenSSH: user@host:'C:/Users/foo/file.xml'
    remote_scp_path = win_path.replace("\\", "/")
    cmd = cfg.scp_args() + [str(local_path), f"{scp_dest}{remote_scp_path}"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"SCP upload feilet: {r.stderr.strip()}")
    return win_path


def download(cfg: SSHConfig, remote_win_path: str, local_path: Path) -> None:
    """Last ned en fil fra Windows til Mac."""
    local_path = local_path.resolve()
    remote_scp_path = remote_win_path.replace("\\", "/")
    cmd = cfg.scp_args() + [
        f"{cfg.user}@{cfg.host}:{remote_scp_path}",
        str(local_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"SCP download feilet: {r.stderr.strip()}")


# =====================================================================
# HØYNIVÅ API
# =====================================================================
def check(cfg: SSHConfig) -> dict:
    # Interpolér staging-path i scriptet
    script = PS_CHECK.replace("__STAGING__", cfg.staging_path())
    result = run_powershell(cfg, script, timeout=30)
    if result.returncode != 0:
        return {"error": f"SSH/PowerShell feilet: {result.stderr.strip()}"}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "Kunne ikke parse PowerShell-output", "raw": result.stdout}


def _wrap_with_filepath(ps: str, win_path: str) -> str:
    """Bytt param-blokken i PS_VERIFY/PS_NORMALIZE med eksplisitt $FilePath-tilordning."""
    return ps.replace(
        "param(\n    [Parameter(Mandatory=$true)][string]$FilePath\n)",
        f'$FilePath = "{win_path}"'
    )


def normalize(cfg: SSHConfig, xml_path: Path) -> dict:
    """
    Last opp XML til Windows, la MS Project åpne og re-lagre den,
    og last resultatet tilbake til samme lokale fil.
    """
    # 1. Last opp til staging
    win_path = upload(cfg, xml_path)

    # 2. Kjør MS Project normalize på staging-fila
    wrapped = _wrap_with_filepath(PS_NORMALIZE, win_path)
    result = run_powershell(cfg, wrapped, timeout=180)
    if result.returncode != 0:
        return {"success": False, "error": result.stderr.strip() or result.stdout.strip()}

    try:
        info = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"success": False, "error": "JSON-parse feilet", "raw": result.stdout}

    if not info.get("success"):
        return info

    # 3. Last ned normalisert fil tilbake
    try:
        download(cfg, win_path, xml_path)
        info["downloadedTo"] = str(xml_path)
    except Exception as e:
        info["downloadError"] = str(e)
        info["success"] = False
    return info


def verify(cfg: SSHConfig, xml_path: Path) -> dict:
    """Last opp XML og bekreft at MS Project kan åpne den (read-only)."""
    win_path = upload(cfg, xml_path)
    wrapped = _wrap_with_filepath(PS_VERIFY, win_path)
    result = run_powershell(cfg, wrapped, timeout=120)
    if result.returncode != 0:
        return {"success": False, "error": result.stderr.strip() or result.stdout.strip()}
    return _parse_json_tolerant(result.stdout)


def fetch(cfg: SSHConfig, remote_name: str, local_path: Path) -> None:
    """
    Hent en fil fra Windows-staging til lokal sti. Nyttig når PM har lagret
    XML i staging-mappa og du vil diffe den.
    """
    staging = cfg.staging_path()
    download(cfg, f"{staging}\\{remote_name}", local_path)


# =====================================================================
# CLI
# =====================================================================
def cmd_check(args) -> int:
    cfg = SSHConfig.load()
    if not cfg:
        print("Ingen SSH-konfig. Se --help for hvordan sette den opp.", file=sys.stderr)
        return 2
    print(f"SSH-config: {cfg.user}@{cfg.host}:{cfg.port}")
    print(f"Staging:    {cfg.staging_path()}")
    info = check(cfg)
    if "error" in info:
        print(f"✗ {info['error']}", file=sys.stderr)
        return 1
    print(f"✓ Tilkobling OK — Windows {info.get('osVersion')} som {info.get('user')}")
    print(f"  Staging-mappe klar: {info.get('stagingExists')}")
    print(f"  MS Project: {info.get('msProjectAvailable')} "
          f"(versjon {info.get('msProjectVersion', '?')})")
    if info.get("stagingFiles"):
        print(f"  XML-filer i staging: {info['stagingFiles']}")
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
