#!/usr/bin/env sh
# ============================================
# Solo Dev Autopilot — 仓库自检
# 本地可跑：bash scripts/ci-self-check.sh
# CI 调用：.github/workflows/ci.yml 执行同一脚本
# 检查：JSON 有效性 / SKILL.md 格式 / Shell 语法
# 纯 POSIX，不依赖 dirname/basename（Git for Windows 的迷你 sh 也能跑）
# ============================================

set -u

case "$0" in
  */*) SCRIPT_DIR=${0%/*} ;;
  *)   SCRIPT_DIR=. ;;
esac
ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$ROOT"

pass=0
fail=0

ok()   { pass=$((pass + 1)); echo "  [PASS] $1"; }
bad()  { fail=$((fail + 1)); echo "  [FAIL] $1"; }

echo "=== 1. JSON 有效性 ==="
json_files="configs/permissions.json configs/modes/toy.json configs/modes/team.json configs/modes/production.json configs/mcp-servers.json .claude/settings.json"
for f in $json_files; do
  if [ ! -f "$f" ]; then
    bad "JSON 缺失: $f"; continue
  fi
  if python3 -c "import json,sys; json.load(open('$f', encoding='utf-8-sig'))" 2>/dev/null; then
    ok "JSON: $f"
  else
    bad "JSON 解析失败: $f"
  fi
done
for f in configs/tool-presets/*.json; do
  [ -f "$f" ] || continue
  if python3 -c "import json,sys; json.load(open('$f', encoding='utf-8-sig'))" 2>/dev/null; then
    ok "JSON: $f"
  else
    bad "JSON 解析失败: $f"
  fi
done

echo "=== 2. SKILL.md 格式（frontmatter: name/description/license） ==="
skill_count=0
for dir in .claude/skills/*/; do
  [ -d "$dir" ] || continue
  skill_count=$((skill_count + 1))
  skill=${dir%/}
  skill=${skill##*/}
  f="${dir}SKILL.md"
  if [ ! -f "$f" ]; then
    bad "SKILL: $skill 缺 SKILL.md"; continue
  fi
  ok=1
  head -1 "$f" | grep -q '^---$'    || ok=0
  grep -q '^name:' "$f"             || ok=0
  grep -q '^description:' "$f"      || ok=0
  grep -q '^license:' "$f"          || ok=0
  if [ "$ok" -eq 1 ]; then
    ok "SKILL: $skill"
  else
    bad "SKILL: $skill frontmatter 缺 name/description/license 之一"
  fi
done
[ "$skill_count" -gt 0 ] || bad "未发现任何 skill（.claude/skills/ 为空？）"

echo "=== 3. Shell 语法（strip BOM 后 sh -n） ==="
for f in scripts/*.sh templates/pre-commit-hook templates/pre-push-hook; do
  [ -f "$f" ] || continue
  tmp=$(mktemp 2>/dev/null || echo "/tmp/sdap-check.$$")
  sed '1s/^\xEF\xBB\xBF//' "$f" > "$tmp"
  if sh -n "$tmp" 2>/dev/null; then
    ok "SH: $f"
  else
    bad "SH 语法错误: $f"
  fi
  rm -f "$tmp"
done

echo ""
echo "结果: $pass 通过 / $fail 失败"
[ "$fail" -eq 0 ] || exit 1
