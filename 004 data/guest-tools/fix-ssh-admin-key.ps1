# Legg Mac public key i administrators_authorized_keys og verifisér oppsett.
# Kjør i admin PowerShell:
#   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\fix-ssh-admin-key.ps1"

$ErrorActionPreference = 'Continue'
$key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIurn9cAIlJyWpl3VXj+4CEhTpi64RcMYvXnz/oLrKuD log650-mac"

Write-Host "=== Sjekk gruppemedlemskap ===" -ForegroundColor Cyan
$user = $env:USERNAME
$isInAdmins = (net localgroup Administrators) -match "^$user$"
Write-Host "Brukeren '$user' i lokal Administrators-gruppe: $isInAdmins"

Write-Host ""
Write-Host "=== Legg nøkkel i admin-authorized_keys ===" -ForegroundColor Cyan
$adminAuth = "C:\ProgramData\ssh\administrators_authorized_keys"
if (-not (Test-Path "C:\ProgramData\ssh")) {
    New-Item -ItemType Directory -Force -Path "C:\ProgramData\ssh" | Out-Null
}

# Les eksisterende innhold (hvis finnes) og sjekk om nøkkelen er der
$existing = ""
if (Test-Path $adminAuth) {
    $existing = Get-Content $adminAuth -Raw -ErrorAction SilentlyContinue
}
if ($existing -notmatch [regex]::Escape("oLrKuD")) {
    Add-Content -Path $adminAuth -Value $key
    Write-Host "  Nøkkel lagt til." -ForegroundColor Green
} else {
    Write-Host "  Nøkkel fantes allerede." -ForegroundColor Yellow
}

# Windows OpenSSH krever strict ACL på administrators_authorized_keys
icacls $adminAuth /inheritance:r /grant "Administrators:F" /grant "SYSTEM:F" | Out-Null
Write-Host "  ACL satt: Administrators + SYSTEM (inheritance fjernet)"

Write-Host ""
Write-Host "=== Sjekk sshd_config ===" -ForegroundColor Cyan
$config = "C:\ProgramData\ssh\sshd_config"
if (Test-Path $config) {
    $content = Get-Content $config
    $matchLine = $content | Select-String "Match Group administrators"
    if ($matchLine) {
        Write-Host "  'Match Group administrators' er aktivert (default på Windows Server OpenSSH)."
        $authLine = $content | Select-String "administrators_authorized_keys"
        if ($authLine) {
            Write-Host "  → bruker $($authLine.Line.Trim())"
        }
    }
}

Write-Host ""
Write-Host "=== Restart sshd ===" -ForegroundColor Cyan
Restart-Service sshd
Start-Sleep -Seconds 1
$svc = Get-Service sshd
Write-Host "  sshd: $($svc.Status)"

Write-Host ""
Write-Host "=== Innholdet i nøkkelfilene (for sanity check) ===" -ForegroundColor Cyan
Write-Host "-- $env:USERPROFILE\.ssh\authorized_keys --"
if (Test-Path "$env:USERPROFILE\.ssh\authorized_keys") {
    Get-Content "$env:USERPROFILE\.ssh\authorized_keys"
}
Write-Host ""
Write-Host "-- $adminAuth --"
Get-Content $adminAuth

Write-Host ""
Write-Host "Ferdig. Test fra Mac med: ssh $env:USERNAME@192.168.64.2" -ForegroundColor Green
