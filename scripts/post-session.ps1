# ============================================
# Solo Dev Autopilot - Post-session automation (Windows PowerShell)
# Features:
#   1. Detect changes
#   2. Record session summary to .solo-dev-autopilot/sessions.log
#   3. Generate "last session review" into SESSION_DRIVER.md
#   4. Health check
#
# Usage:
#   - Hook from AI tool Stop event (Windows)
#   - Manual: powershell -ExecutionPolicy Bypass -File scripts\post-session.ps1
#
# Note: keep this file ASCII-only for PowerShell 5.1 compatibility.
# ============================================

param(
    [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot/..").Path
)

$ErrorActionPreference = "SilentlyContinue"

function Info($msg)  { Write-Host "[post-session] $msg" -ForegroundColor Green }
function Warn($msg)  { Write-Host "[post-session] $msg" -ForegroundColor Yellow }

# ---- Step 1: detect changes ----
$hasChanges = $false
Push-Location $ProjectRoot
$status = git status --porcelain 2>$null
Pop-Location
if ($status) {
    $hasChanges = $true
    Info "Changes detected: $($status.Count) file(s)"
} else {
    Warn "No changes detected, skip codemap hint"
}

# ---- Step 2: record session summary ----
function Record-SessionSummary {
    $logDir = Join-Path $ProjectRoot ".solo-dev-autopilot"
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    $logFile = Join-Path $logDir "sessions.log"

    Push-Location $ProjectRoot
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $branch = git branch --show-current 2>$null
    if (-not $branch) { $branch = "unknown" }
    $commitCount = git rev-list --count HEAD 2>$null
    if (-not $commitCount) { $commitCount = "?" }
    $changedCount = (git diff --name-only HEAD 2>$null | Measure-Object).Count
    Pop-Location

    Add-Content -Path $logFile -Value "[$timestamp] branch=$branch commits=$commitCount changed_files=$changedCount"
    Info "Session log appended to $logFile"
}

# ---- Step 3: generate last-session review into SESSION_DRIVER.md ----
function Generate-SessionReview {
    $driver = Join-Path $ProjectRoot "SESSION_DRIVER.md"

    Push-Location $ProjectRoot
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $branch = git branch --show-current 2>$null
    if (-not $branch) { $branch = "unknown" }

    $commits = git log --oneline -10 2>$null
    if (-not $commits) { $commits = "- (no commits)" }
    $files = git diff --name-only "HEAD~5" HEAD 2>$null
    if (-not $files) { $files = git diff --name-only HEAD 2>$null }
    if (-not $files) { $files = @("- (no file changes)") }
    Pop-Location

    $commitLines = ($commits | ForEach-Object { "- $_" }) -join "`n"
    $fileLines = ($files | ForEach-Object { "- [M] ``$_``" }) -join "`n"

    $reviewBlock = @"
**Time**: $timestamp | **Branch**: $branch

**Recent commits**:
$commitLines

**Changed files**:
$fileLines
"@

    # Create skeleton if missing
    if (-not (Test-Path $driver)) {
        Info "SESSION_DRIVER.md not found, creating skeleton"
        @"
# Session Driver

## Goal

- [ ] (fill in this session goal)

## Last Session Review

* (waiting for auto-fill) *

## Progress

- (none)

## Known blockers

- (none)
"@ | Set-Content -Path $driver -Encoding UTF8
    }

    # Replace "## Last Session Review" section
    $content = Get-Content $driver -Raw -Encoding UTF8
    $pattern = "(?s)## Last Session Review.*?(?=## |\z)"
    if ($content -match $pattern) {
        $updated = $content -replace $pattern, "## Last Session Review`n`n$reviewBlock`n`n"
        Set-Content -Path $driver -Value $updated -Encoding UTF8
        Info "Last session review written to SESSION_DRIVER.md"
    } else {
        Warn "Could not locate '## Last Session Review' section, skipped"
    }
}

# ---- Step 4: health check ----
function Health-Check {
    $warnings = 0

    # .env tracked?
    Push-Location $ProjectRoot
    $envTracked = git ls-files --error-unmatch .env 2>$null
    Pop-Location
    if ($envTracked) {
        Warn ".env is tracked by git! Add it to .gitignore"
        $warnings++
    }

    # node_modules tracked?
    Push-Location $ProjectRoot
    $nmTracked = git ls-files --error-unmatch node_modules 2>$null
    Pop-Location
    if ($nmTracked) {
        Warn "node_modules is tracked by git! Add it to .gitignore"
        $warnings++
    }

    # large files (>10MB)
    $large = Get-ChildItem -Path $ProjectRoot -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Length -gt 10MB -and $_.FullName -notmatch 'node_modules|\\.git\\|\\dist\\|\\build\\' } |
        Select-Object -First 5
    if ($large) {
        Warn "Large files (>10MB) found:"
        $large | ForEach-Object { Warn "  $($_.Name) ($([math]::Round($_.Length / 1MB, 1)) MB)" }
        $warnings++
    }

    if ($warnings -eq 0) { Info "Health check passed" }
    else { Warn "Health check found $warnings potential issue(s)" }
}

# ---- main ----
Info "========================================="
Info "Solo Dev Autopilot - post-session automation"
Info "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Info "========================================="

Record-SessionSummary
Generate-SessionReview
Health-Check

Info "Post-session done."
Info "Next session: read PROJECT-MEMORY.md, CODEMAP.md and SESSION_DRIVER.md"
