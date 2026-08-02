#!/usr/bin/env bash
# ============================================
# Solo Dev Autopilot — 会话结束后的自动化脚本
# 功能：
#   1. 生成/更新代码地图 (CODEMAP.md)
#   2. 更新项目记忆 (PROJECT-MEMORY.md)
#   3. 记录本次会话的变更摘要
#   4. 检查是否有新的待办事项
#
# 使用方式：
#   - 通过工具的 Stop hook 自动触发
#   - 手动执行: bash scripts/post-session.sh
# ============================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ---- 颜色 ----
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[post-session]${NC} $*"; }
warn() { echo -e "${YELLOW}[post-session]${NC} $*"; }

# ---- Step 1: 检测变更 ----
detect_changes() {
  log "检测本次会话的变更..."
  
  cd "$PROJECT_ROOT"
  
  # 检查是否有未提交的变更
  if git diff --quiet HEAD 2>/dev/null && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    warn "没有检测到变更，跳过代码地图更新"
    return 1
  fi
  
  # 获取变更统计
  CHANGED_FILES=$(git diff --stat HEAD 2>/dev/null | tail -1)
  log "变更: ${CHANGED_FILES}"
  
  return 0
}

# ---- Step 2: 更新代码地图提示 ----
update_codemap_hint() {
  log "💡 建议：下次开会话时说以下任一命令来恢复上下文："
  echo ""
  echo "  📖 '加载 CODEMAP.md'"
  echo "  📖 '读取项目代码地图'"
  echo "  📖 '根据代码地图继续工作'"
  echo "  📖 '/skill context-map'"
  echo ""
  echo "  📖 '加载 PROJECT-MEMORY.md'"
  echo "  📖 '读取项目记忆'"
  echo ""
}

# ---- Step 3: 记录会话摘要 ----
record_session_summary() {
  local session_log_dir="${PROJECT_ROOT}/.solo-dev-autopilot"
  local session_log="${session_log_dir}/sessions.log"
  
  mkdir -p "$session_log_dir"
  
  cd "$PROJECT_ROOT"
  
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  local commit_count=$(git rev-list --count HEAD 2>/dev/null || echo "?")
  local changed_files=$(git diff --name-only HEAD 2>/dev/null | wc -l | tr -d ' ')
  local branch=$(git branch --show-current 2>/dev/null || echo "unknown")
  
  cat >> "$session_log" << EOF
[${timestamp}] branch=${branch} commits=${commit_count} changed_files=${changed_files}
EOF
  
  log "会话记录已追加到 ${session_log}"
}

# ---- Step 4: 检查健康状态 ----
health_check() {
  local warnings=0
  
  # 检查是否有 .env 文件但它在 .gitignore 里没有
  if [ -f "${PROJECT_ROOT}/.env" ] && grep -q "^\.env$" "${PROJECT_ROOT}/.gitignore" 2>/dev/null; then
    : # 正常情况
  elif [ -f "${PROJECT_ROOT}/.env" ]; then
    warn "⚠️  .env 文件存在但可能未被 gitignore 忽略！"
    ((warnings++))
  fi
  
  # 检查 node_modules 是否意外被跟踪
  if git ls-files --error-unmatch "${PROJECT_ROOT}/node_modules" &>/dev/null 2>&1; then
    warn "⚠️  node_modules 被 git 跟踪了！应该加入 .gitignore"
    ((warnings++))
  fi
  
  # 检查大文件
  local large_files=$(find "${PROJECT_ROOT}" -type f -size +10M \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/dist/*" \
    -not -path "*/build/*" \
    2>/dev/null | head -5)
  
  if [ -n "$large_files" ]; then
    warn "⚠️  发现大文件（>10MB），可能不应该提交："
    echo "$large_files" | while read -r f; do
      warn "   $(basename "$f") ($(du -h "$f" | cut -f1))"
    done
    ((warnings++))
  fi
  
  if [ "$warnings" -gt 0 ]; then
    warn "发现 ${warnings} 个潜在问题，建议修复"
  else
    log "健康检查通过 ✅"
  fi
}

# ---- 主流程 ----
main() {
  log "========================================="
  log "Solo Dev Autopilot — 会话后自动化"
  log "时间: $(date '+%Y-%m-%d %H:%M:%S')"
  log "========================================="
  
  if detect_changes; then
    update_codemap_hint
  fi
  
  record_session_summary
  health_check
  
  log "✅ 会话后处理完成"
  log "下次启动时记得让 AI 加载 CODEMAP.md 和 PROJECT-MEMORY.md"
}

main "$@"
