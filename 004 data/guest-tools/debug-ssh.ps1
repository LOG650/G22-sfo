# Dyp diagnostikk for SSH-auth-problemer på Windows.
# Kjør i admin PowerShell:
#   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\debug-ssh.ps1"

$ErrorActionPreference = 'Continue'

function Section($title) {
    Write-Host ""
    Write-Host "=== $title ===" -ForegroundColor Cyan
}

Section "Bruker og gruppemedlemskap"
$user = $env:USERNAME
Write-Host "Username: $user"
$inAdmins = (net localgroup Administrators) | Where-Object { $_ -eq $user }
Write-Host "I lokal Administrators-gruppe: $([bool]$inAdmins)"

Section "Sshd service"
$svc = Get-Service sshd
Write-Host "Status: $($svc.Status)"
Write-Host "StartType: $($svc.StartType)"

Section "sshd_config relevante linjer"
$cfg = "C:\ProgramData\ssh\sshd_config"
if (Test-Path $cfg) {
    Get-Content $cfg | Select-String -Pattern "^(?!#)(PubkeyAuthentication|PasswordAuthentication|AuthorizedKeysFile|Match Group)" `
        | ForEach-Object { Write-Host "  $($_.Line)" }
}

Section "user authorized_keys"
$userKey = "$env:USERPROFILE\.ssh\authorized_keys"
if (Test-Path $userKey) {
    $raw = [System.IO.File]::ReadAllBytes($userKey)
    Write-Host "Path: $userKey"
    Write-Host "Størrelse: $($raw.Length) bytes"
    # Sjekk for BOM (EF BB BF)
    if ($raw.Length -ge 3 -and $raw[0] -eq 0xEF -and $raw[1] -eq 0xBB -and $raw[2] -eq 0xBF) {
        Write-Host "!! HAR UTF-8 BOM (det kan blokkere pubkey auth) !!" -ForegroundColor Red
    } else {
        Write-Host "Ingen BOM"
    }
    # Sjekk for CRLF
    $text = [System.Text.Encoding]::UTF8.GetString($raw)
    if ($text -match "`r`n") { Write-Host "Linjeskift: CRLF" }
    else { Write-Host "Linjeskift: LF" }
    Write-Host "--- innhold ---"
    Write-Host $text
    Write-Host "---"
    Write-Host "ACL:"
    icacls $userKey | Out-Host
} else {
    Write-Host "Finnes ikke" -ForegroundColor Red
}

Section "administrators_authorized_keys"
$adminKey = "C:\ProgramData\ssh\administrators_authorized_keys"
if (Test-Path $adminKey) {
    $raw = [System.IO.File]::ReadAllBytes($adminKey)
    Write-Host "Path: $adminKey"
    Write-Host "Størrelse: $($raw.Length) bytes"
    if ($raw.Length -ge 3 -and $raw[0] -eq 0xEF -and $raw[1] -eq 0xBB -and $raw[2] -eq 0xBF) {
        Write-Host "!! HAR UTF-8 BOM !!" -ForegroundColor Red
    } else {
        Write-Host "Ingen BOM"
    }
    $text = [System.Text.Encoding]::UTF8.GetString($raw)
    Write-Host "--- innhold ---"
    Write-Host $text
    Write-Host "---"
    Write-Host "ACL:"
    icacls $adminKey | Out-Host
} else {
    Write-Host "Finnes ikke" -ForegroundColor Yellow
}

Section "Siste sshd event-log entries"
try {
    Get-WinEvent -LogName "OpenSSH/Operational" -MaxEvents 10 -ErrorAction Stop |
        Select-Object TimeCreated, Id, Message |
        Format-Table -Wrap
} catch {
    Write-Host "Ingen OpenSSH/Operational log. Prøver default app log..."
    try {
        Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='OpenSSH'} -MaxEvents 10 -ErrorAction Stop |
            Select-Object TimeCreated, Id, Message | Format-Table -Wrap
    } catch {
        Write-Host "Ingen events tilgjengelig."
    }
}

Section "Fix hvis BOM eller CRLF oppdaget"
Write-Host "Dette scriptet re-skriver authorized_keys filene UTEN BOM og med LF:"
Write-Host ""
$key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIurn9cAIlJyWpl3VXj+4CEhTpi64RcMYvXnz/oLrKuD log650-mac"
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

# User-kopi
[System.IO.File]::WriteAllText($userKey, "$key`n", $utf8NoBom)
icacls $userKey /inheritance:r /grant "${user}:F" /grant "SYSTEM:F" | Out-Null
Write-Host "Re-skrevet: $userKey (UTF-8 no BOM, LF)"

# Admin-kopi
[System.IO.File]::WriteAllText($adminKey, "$key`n", $utf8NoBom)
icacls $adminKey /inheritance:r /grant "Administrators:F" /grant "SYSTEM:F" | Out-Null
Write-Host "Re-skrevet: $adminKey (UTF-8 no BOM, LF)"

Restart-Service sshd
Write-Host "sshd restartet."
Write-Host ""
Write-Host "Test nå fra Mac: ssh Sebastian@192.168.64.2" -ForegroundColor Green
