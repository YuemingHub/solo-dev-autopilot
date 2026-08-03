# Solo Dev Autopilot — 安装 Git Hooks (PowerShell)
# 用法：powershell -ExecutionPolicy Bypass -File scripts\install-git-hooks.ps1

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
    ErrorMsg "当前目录不是 Git 仓库（找不到 .git\hooks\）"
    exit 1
}

Info "安装 pre-commit hook..."
Copy-Item (Join-Path $TemplatesDir "pre-commit-hook") (Join-Path $HooksDir "pre-commit") -Force
Success "pre-commit hook 已安装"

Info "安装 pre-push hook..."
Copy-Item (Join-Path $TemplatesDir "pre-push-hook") (Join-Path $HooksDir "pre-push") -Force
Success "pre-push hook 已安装"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host " Git Hooks 安装完成！" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host " 已安装："
Write-Host "   ├── pre-commit  → 提交前 P0 检查"
Write-Host "   └── pre-push    → 推送前审查提醒"
Write-Host ""
Write-Host " 提示：Git Hooks 不会被 git 跟踪，换电脑后需重新安装" -ForegroundColor Yellow
