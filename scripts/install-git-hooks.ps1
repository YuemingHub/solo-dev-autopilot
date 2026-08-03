?# Solo Dev Autopilot - ?? Git Hooks (PowerShell)
# ??:powershell -ExecutionPolicy Bypass -File scripts\install-git-hooks.ps1

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$HooksDir = Join-Path $ProjectRoot ".git\hooks"
$TemplatesDir = Join-Path $ProjectRoot "templates"

function Info($msg)    { Write-Host "[git-hooks] $msg" -ForegroundColor Blue }
function Success($msg) { Write-Host "[git-hooks] $msg" -ForegroundColor Green }
function Warn($msg)    { Write-Host "[git-hooks] $msg" -ForegroundColor Yellow }
function ErrorMsg($msg){ Write-Host "[git-hooks] $msg" -ForegroundColor Red }

if (-not (Test-Path $HooksDir)) {
    ErrorMsg "?????? Git ??(??? .git\hooks\)"
    exit 1
}

Info "?? pre-commit hook..."
Copy-Item (Join-Path $TemplatesDir "pre-commit-hook") (Join-Path $HooksDir "pre-commit") -Force
Success "pre-commit hook ???"

Info "?? pre-push hook..."
Copy-Item (Join-Path $TemplatesDir "pre-push-hook") (Join-Path $HooksDir "pre-push") -Force
Success "pre-push hook ???"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host " Git Hooks ????!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host " ???:"
Write-Host "   ??? pre-commit  ? ??? P0 ??"
Write-Host "   ??? pre-push    ? ???????"
Write-Host ""
Write-Host " ??:Git Hooks ??? git ??,?????????" -ForegroundColor Yellow