# Setter default SSH-shell til PowerShell og lukker evt. kjørende MS Project.
# Kjør i admin PowerShell:
#   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\set-default-shell.ps1"

$psPath = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value $psPath -PropertyType String -Force | Out-Null
Write-Host "DefaultShell satt til: $psPath" -ForegroundColor Green

$proj = Get-Process WINPROJ -ErrorAction SilentlyContinue
if ($proj) {
    $proj | Stop-Process -Force
    Write-Host "MS Project lukket." -ForegroundColor Yellow
} else {
    Write-Host "MS Project kjører ikke." -ForegroundColor Green
}

# Verify
Get-ItemProperty HKLM:\SOFTWARE\OpenSSH | Select-Object DefaultShell
Write-Host ""
Write-Host "Ferdig. Tester kan kjøres fra Mac nå." -ForegroundColor Cyan
