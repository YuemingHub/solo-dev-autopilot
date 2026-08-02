# ============================================
# Solo Dev Autopilot — 一键安装与环境检测 (Windows PowerShell 版)
# 用法: powershell -ExecutionPolicy Bypass -File scripts\setup.ps1 [项目路径]
# ============================================

param(
    [string]$TargetDir = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

# ---- 路径配置 ----
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

# ---- 辅助函数 ----
function Info($msg)    { Write-Host "[INFO]  $msg" -ForegroundColor Blue }
function Success($msg) { Write-Host "[OK]   $msg" -ForegroundColor Green }
function Warn($msg)    { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function ErrorMsg($msg){ Write-Host "[ERROR] $msg" -ForegroundColor Red }

# ---- 检测工具环境 ----
function Detect-Environment {
    Info "正在检测你的开发环境..."

    $detectedTools = @()

    # Node.js
    $nodeVersion = try { (node --version 2>$null) } catch { $null }
    if ($nodeVersion) { Success "Node.js: $nodeVersion"; $detectedTools += "node" }
    else { Warn "未检测到 Node.js" }

    # Bun
    $bunVersion = try { (bun --version 2>$null) } catch { $null }
    if ($bunVersion) { Success "Bun: $bunVersion"; $detectedTools += "bun" }

    # pnpm / npm
    $pnpmVersion = try { (pnpm --version 2>$null) } catch { $null }
    if ($pnpmVersion) { Success "pnpm: $pnpmVersion"; $detectedTools += "pnpm" }
    else {
        $npmVersion = try { (npm --version 2>$null) } catch { $null }
        if ($npmVersion) { Success "npm: $npmVersion"; $detectedTools += "npm" }
    }

    # Git
    $gitVersion = try { (git --version 2>$null) } catch { $null }
    if ($gitVersion) { Success "Git: $gitVersion" }
    else { ErrorMsg "未检测到 Git！请先安装 Git"; exit 1 }

    # AI 编程工具
    Info ""
    Info "检测 AI 编程工具..."

    $aiTool = @()
    if (Get-Command claude -ErrorAction SilentlyContinue) { Success "检测到 Claude Code"; $aiTool += "claude-code" }
    if (Test-Path "$env:USERPROFILE\.cursor" -ErrorAction SilentlyContinue) { Success "检测到 Cursor"; $aiTool += "cursor" }

    if ($aiTool.Count -eq 0) {
        Warn "未检测到已安装的 AI 编程工具"
        Warn "支持的工具：Claude Code, Cursor, Cline, Windsurf"
        Info "你可以继续安装，稍后手动配置 MCP 和 Skill"
    }

    return $detectedTools
}

# ---- 复制 Skill 文件 ----
function Install-Skills {
    Info ""
    Info "安装 Skill 文件..."

    $skillsSrc = Join-Path $RepoRoot "skills"
    $skillsDest = Join-Path $TargetDir "skills"

    if (-not (Test-Path $skillsSrc)) { ErrorMsg "源目录不存在: $skillsSrc"; exit 1 }

    New-Item -ItemType Directory -Force -Path $skillsDest | Out-Null
    Copy-Item -Path "$skillsSrc\*" -Destination $skillsDest -Recurse -Force

    $skillCount = (Get-ChildItem $skillsDest -Filter "*.md").Count
    Success "已复制 $skillCount 个 Skill 到 $skillsDest\"
}

# ---- 安装模板文件 ----
function Install-Templates {
    Info ""
    Info "安装项目模板..."

    # .gitignore
    $gitignorePath = Join-Path $TargetDir ".gitignore"
    if (-not (Test-Path $gitignorePath)) {
        Copy-Item (Join-Path $RepoRoot "templates\gitignore") $gitignorePath
        Success ".gitignore 已创建"
    } else { Warn ".gitignore 已存在，跳过" }

    # .env.example
    $envPath = Join-Path $TargetDir ".env.example"
    if (-not (Test-Path $envPath)) {
        Copy-Item (Join-Path $RepoRoot "templates\env-example.env") $envPath
        Success ".env.example 已创建"
    } else { Warn ".env.example 已存在，跳过" }

    # PROJECT-MEMORY.md
    $memPath = Join-Path $TargetDir "PROJECT-MEMORY.md"
    if (-not (Test-Path $memPath)) {
        Copy-Item (Join-Path $RepoRoot "templates\PROJECT-MEMORY-template.md") $memPath
        Success "PROJECT-MEMORY.md 已创建（请编辑填写你的项目信息）"
    } else { Warn "PROJECT-MEMORY.md 已存在，跳过" }

    # ONBOARDING.md
    $obPath = Join-Path $TargetDir "ONBOARDING.md"
    if (-not (Test-Path $obPath)) {
        Copy-Item (Join-Path $RepoRoot "templates\ONBOARDING-template.md") $obPath
        Success "ONBOARDING.md 已创建（新手必读！）"
    } else { Warn "ONBOARDING.md 已存在，跳过" }

    # AI-GUIDE.md
    $guidePath = Join-Path $TargetDir "AI-GUIDE.md"
    if (-not (Test-Path $guidePath)) {
        Copy-Item (Join-Path $RepoRoot "templates\AI-GUIDE-template.md") $guidePath
        Success "AI-GUIDE.md 已创建（新手必读！了解 AI 能做什么、怎么防幻觉）"
    } else { Warn "AI-GUIDE.md 已存在，跳过" }

    # SESSION_DRIVER.md
    $sdPath = Join-Path $TargetDir "SESSION_DRIVER.md"
    if (-not (Test-Path $sdPath)) {
        Copy-Item (Join-Path $RepoRoot "templates\SESSION_DRIVER-template.md") $sdPath
        Success "SESSION_DRIVER.md 已创建（每次会话开始时填写）"
    } else { Warn "SESSION_DRIVER.md 已存在，跳过" }
}

# ---- 初始化 Git ----
function Init-Git {
    if (Test-Path (Join-Path $TargetDir ".git")) {
        Warn "Git 仓库已存在，跳过初始化"
        return
    }

    Info ""
    Info "初始化 Git 仓库..."
    Push-Location $TargetDir
    git init
    git add -A
    git commit -m "chore: initialize with Solo Dev Autopilot" 2>$null
    Pop-Location
    Success "Git 仓库已初始化并提交"
}

# ---- 最终检查与总结 ----
function Print-Summary {
    Write-Host ""
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host " Solo Dev Autopilot 安装完成！" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host " 目标目录: $TargetDir"
    Write-Host " 已安装:"
    Write-Host "   ├── skills/          $((Get-ChildItem (Join-Path $TargetDir 'skills') -Filter '*.md' -ErrorAction SilentlyContinue).Count) 个 Skill"
    Write-Host "   ├── .gitignore       OK"
    Write-Host "   ├── .env.example     OK"
    Write-Host "   ├── PROJECT-MEMORY.md OK"
    Write-Host "   ├── ONBOARDING.md    OK"
    Write-Host "   ├── AI-GUIDE.md      OK"
    Write-Host "   └── SESSION_DRIVER.md OK"
    Write-Host ""
    Write-Host " 下一步操作:"
    Write-Host "   1. 阅读 AI-GUIDE.md（了解 AI 能做什么、怎么防幻觉）"
    Write-Host "   2. 阅读 ONBOARDING.md（了解记忆文件和启动咒语）"
    Write-Host "   3. 编辑 PROJECT-MEMORY.md 填写项目信息"
    Write-Host "   4. 复制 .env.example 为 .env 并填入实际值"
    Write-Host "   5. 启动你的 AI 编程工具"
    Write-Host "   6. 说: '读取 PROJECT-MEMORY.md、CODEMAP.md 和 SESSION_DRIVER.md'"
    Write-Host ""
    Write-Host " 常用命令:"
    Write-Host "   /skill task-planner     — 拆解任务、设定目标"
    Write-Host "   /skill context-map      — 生成/更新代码地图"
    Write-Host "   /skill fullstack-scaffold — 创建新项目"
    Write-Host "   /skill code-review      — 代码审查"
    Write-Host "   /skill commit-helper    — 生成提交信息"
    Write-Host "   /skill deploy-check     — 部署前检查"
    Write-Host "   /skill troubleshoot     — 问题排查"
    Write-Host ""
}

# ---- 主流程 ----
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Solo Dev Autopilot Installer (PowerShell)" -ForegroundColor Cyan
Write-Host "  一个人，一个 AI，一个完整产品" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

Detect-Environment
Install-Skills
Install-Templates
Init-Git
Print-Summary