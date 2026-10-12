# Zhihu Operations Skill Installer for Windows PowerShell
$ErrorActionPreference = "Stop"

$SkillName = "zhihu-operations"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceDir = Join-Path $ScriptDir $SkillName

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Zhihu Operations Skill Installer (PowerShell)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

if (-not (Test-Path $SourceDir)) {
    Write-Error "[-] Error: Source directory '$SourceDir' not found!"
    exit 1
}

$TargetDir = if ($args.Count -gt 0) { $args[0] } else { Join-Path $HOME ".hermes\skills\social-media\$SkillName" }

Write-Host "[*] Source: $SourceDir"
Write-Host "[*] Target: $TargetDir"

$ParentDir = Split-Path -Parent $TargetDir
if (-not (Test-Path $ParentDir)) {
    New-Item -ItemType Directory -Path $ParentDir -Force | Out-Null
}

if (Test-Path $TargetDir) {
    Write-Host "[!] Updating existing installation..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $TargetDir
}

Copy-Item -Recurse -Path $SourceDir -Destination $TargetDir

Write-Host "[+] Successfully installed $SkillName to $TargetDir" -ForegroundColor Green
Write-Host ""
Write-Host "Verify installation:"
Write-Host "  python `"$TargetDir\scripts\lint.py`" --help"
Write-Host "  python `"$TargetDir\scripts\guard.py`" check"
