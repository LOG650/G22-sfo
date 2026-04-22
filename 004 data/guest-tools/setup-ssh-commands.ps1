# LOG650 — Setup OpenSSH Server + legg inn Mac public key
# Kjør i Windows PowerShell (som administrator):
#   powershell -ExecutionPolicy Bypass -File Z:\guest-tools\setup-ssh-commands.ps1

$ErrorActionPreference = 'Stop'

Write-Host "=== 1. Start OpenSSH Server-tjenesten ===" -ForegroundColor Cyan
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic

Write-Host ""
Write-Host "=== 2. Åpne port 22 i brannmur ===" -ForegroundColor Cyan
$existing = Get-NetFirewallRule -Name sshd -ErrorAction SilentlyContinue
if (-not $existing) {
    New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server' `
        -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 | Out-Null
    Write-Host "  Brannmurregel opprettet."
} else {
    Write-Host "  Brannmurregel finnes allerede."
}

Write-Host ""
Write-Host "=== 3. Legg Mac public key inn i authorized_keys ===" -ForegroundColor Cyan
$key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIurn9cAIlJyWpl3VXj+4CEhTpi64RcMYvXnz/oLrKuD log650-mac"

# Brukerens egen .ssh-mappe
$userSsh = "$env:USERPROFILE\.ssh"
New-Item -ItemType Directory -Force -Path $userSsh | Out-Null
$authFile = "$userSsh\authorized_keys"
if (-not (Test-Path $authFile) -or -not (Get-Content $authFile | Select-String -SimpleMatch $key)) {
    Add-Content -Path $authFile -Value $key
    Write-Host "  Nøkkel lagt til $authFile"
} else {
    Write-Host "  Nøkkel finnes allerede i $authFile"
}

# Sett riktige rettigheter
icacls $authFile /inheritance:r /grant "$($env:USERNAME):F" /grant "SYSTEM:F" | Out-Null

# Hvis brukeren er admin, MÅ nøkkelen også legges i administrators_authorized_keys
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole("Administrator")
if ($isAdmin) {
    $adminAuth = "C:\ProgramData\ssh\administrators_authorized_keys"
    if (-not (Test-Path $adminAuth) -or -not (Get-Content $adminAuth -ErrorAction SilentlyContinue | Select-String -SimpleMatch $key)) {
        Add-Content -Path $adminAuth -Value $key
        Write-Host "  Nøkkel lagt til $adminAuth (admin-path)"
    }
    icacls $adminAuth /inheritance:r /grant "Administrators:F" /grant "SYSTEM:F" | Out-Null
    Restart-Service sshd
    Write-Host "  sshd restartet."
}

Write-Host ""
Write-Host "=== 4. Tilkoblingsinfo ===" -ForegroundColor Green
Write-Host "Brukernavn:     $env:USERNAME"
Write-Host "Maskinnavn:     $env:COMPUTERNAME"
Write-Host "Admin-bruker:   $isAdmin"
Write-Host ""
Write-Host "IP-adresser:"
Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -notmatch '^169\.254\.' -and $_.IPAddress -ne '127.0.0.1' } |
    ForEach-Object {
        Write-Host ("  {0,-15}  ({1})" -f $_.IPAddress, $_.InterfaceAlias)
    }

Write-Host ""
Write-Host "sshd-status:" -NoNewline
$svc = Get-Service sshd
if ($svc.Status -eq 'Running') {
    Write-Host " Running" -ForegroundColor Green
} else {
    Write-Host " $($svc.Status)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Klart til å testes fra Mac med:" -ForegroundColor Cyan
Write-Host "  ssh $env:USERNAME@<IP fra listen over>"
