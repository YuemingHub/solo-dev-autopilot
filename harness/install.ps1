# 一键同步 harness 层（原 agent-tool 的 7 skill + 2 agent + 全局规则）到 ohmyagent 全局配置目录
# 用法:在仓库任意位置执行  powershell -ExecutionPolicy Bypass -File harness\install.ps1
# 幂等:重复执行安全。源 = 本仓库(可 git 管理),目标 = %APPDATA%\com.chaitin.baizhi.monkeycode\ohmyagent\

$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot            # 仓库根目录
$cfg = Join-Path $env:APPDATA 'com.chaitin.baizhi.monkeycode\ohmyagent'

if (-not (Test-Path $cfg)) {
    Write-Host "全局配置目录不存在:$cfg(未安装 ohmyagent?Claude Code/Codex 用户无需此脚本)" -ForegroundColor Red
    exit 1
}

# 1. skills:用平铺兼容层 skills/*.md(ohmyagent 只认单文件 .md,由 sync-skills.py 从 .claude/skills/ 生成)
$flat = Join-Path $repo 'skills'
if (-not (Test-Path $flat)) {
    Write-Host "平铺层 $flat 不存在,请先运行 python scripts/sync-skills.py" -ForegroundColor Red
    exit 1
}
$dstSkills = Join-Path $cfg 'skills'
New-Item -ItemType Directory -Force -Path $dstSkills | Out-Null
$n = 0
Get-ChildItem "$flat\*.md" -File | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $dstSkills $_.Name) -Force
    $n++
}

# 2. agents(2 个:env-agent / dev-agent)
$agents = Join-Path $repo 'harness\agents'
$dstAgents = Join-Path $cfg 'agents'
New-Item -ItemType Directory -Force -Path $dstAgents | Out-Null
Get-ChildItem "$agents\*.json" -File | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $dstAgents $_.Name) -Force
}

# 3. 全局规则(harness 层触发时序)
Copy-Item (Join-Path $repo 'harness\AGENTS.md') (Join-Path $cfg 'AGENTS.md') -Force

Write-Host "同步完成:${n} 个 skill + $(@(Get-ChildItem "$agents\*.json").Count) 个 agent + AGENTS.md"
Write-Host "安装位置:$cfg"
Write-Host "注意:新开 ohmyagent 会话后生效(扫描发生在会话启动时)。"
