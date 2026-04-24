# Rydder opp gamle mappinger og lagrer SMB-creds til Windows Credential Manager
# slik at SSH-sesjoner kan nå Mac-sharen.
#
# Kjør i admin PowerShell:
#   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\setup-smb-cred.ps1"

$macHost = "192.168.64.1"
$macUser = "sebastianthunestveit"
$shareName = "G22-sfo"
$driveLetter = "Y"

Write-Host "=== 1. Fjern gamle credentials for $macHost ==="
cmdkey /list:$macHost 2>&1 | Out-Host
cmdkey /delete:$macHost 2>&1 | Out-Null
Write-Host "Gamle fjernet."

Write-Host ""
Write-Host "=== 2. Spør om Mac-passord (vises ikke) ==="
$securePass = Read-Host -AsSecureString "Mac-passord for $macUser"
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePass)
$plainPass = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)

Write-Host ""
Write-Host "=== 3. Lagre credential i Windows Credential Manager ==="
cmdkey /add:$macHost /user:$macUser /pass:$plainPass | Out-Host

Write-Host ""
Write-Host "=== 4. Fjern gammel drive-mapping hvis den finnes ==="
net use ${driveLetter}: /delete /yes 2>&1 | Out-Null

Write-Host ""
Write-Host "=== 5. Mount Mac SMB-share ==="
net use "${driveLetter}:" "\\$macHost\$shareName" /persistent:yes /user:$macUser $plainPass 2>&1 | Out-Host

# Slett passord fra variabel
$plainPass = $null
Remove-Variable plainPass -ErrorAction SilentlyContinue
[GC]::Collect()

Write-Host ""
Write-Host "=== 6. Verifiser ==="
if (Test-Path "${driveLetter}:\004 data") {
    Write-Host "OK: ${driveLetter}:\004 data er tilgjengelig" -ForegroundColor Green
    Get-ChildItem "${driveLetter}:\004 data\" -Filter "*.xml" | Select-Object Name, Length | Format-Table
} else {
    Write-Host "FEIL: ${driveLetter}: ikke tilgjengelig" -ForegroundColor Red
}

Write-Host ""
Write-Host "Credentials er lagret. SSH-sesjoner kan nå bruke UNC-sti:"
Write-Host "  \\$macHost\$shareName\004 data\" -ForegroundColor Cyan
