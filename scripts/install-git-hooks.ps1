param(
    [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot/..").Path
)

# Solo Dev Autopilot — 安装 Git Hooks（Windows / 带备份）
# 用法：powershell -ExecutionPolicy Bypass -File scripts\install-git-hooks.ps1

$hooksDir = Join-Path $ProjectRoot '.git\hooks'
$templatesDir = Join-Path $ProjectRoot 'templates'
$backupDir = Join-Path $ProjectRoot '.git\hooks-backup'

function Write-Info($msg) { Write-Host "[git-hooks] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "[git-hooks] $msg" -ForegroundColor Yellow }
function Write-ErrorExit($msg) { Write-Host "[git-hooks] $msg" -ForegroundColor Red; exit 1 }

if (!(Test-Path $hooksDir)) { Write-ErrorExit "找不到 .git/hooks/（当前目录不是 Git 仓库）" }

$templatePrecommit = Join-Path $templatesDir 'pre-commit-hook'
$templatePrepush = Join-Path $templatesDir 'pre-push-hook'
if (!(Test-Path $templatePrecommit)) { Write-ErrorExit "找不到模板文件：$templatePrecommit" }
if (!(Test-Path $templatePrepush)) { Write-ErrorExit "找不到模板文件：$templatePrepush" }

# 备份已有 hooks
New-Item -Path $backupDir -ItemType Directory -Force | Out-Null
foreach ($hook in @('pre-commit', 'pre-push')) {
    $existing = Join-Path $hooksDir $hook
    if (Test-Path $existing) {
        $firstLine = Get-Content $existing -TotalCount 1 -ErrorAction SilentlyContinue
        if ($firstLine -match 'Solo Dev Autopilot') {
            Write-Info "$hook 已是本仓库安装，跳过备份"
        } else {
            $backup = Join-Path $backupDir "$hook-$(Get-Date -Format 'yyyyMMddHHmmss')"
            Copy-Item $existing $backup -Force
            Write-Warn "已有 $hook 已备份到 $backup"
        }
    }
    $template = if ($hook -eq 'pre-commit') { $templatePrecommit } else { $templatePrepush }
    Copy-Item $template $existing -Force
    Write-Info "已安装：$hook"
}

Write-Info ""
Write-Info "Git Hooks 安装完成！"
Write-Info "原有 hook 备份在：$backupDir"
Write-Info "提示：Git Hooks 不会被 git 跟踪，换电脑后需重新安装"