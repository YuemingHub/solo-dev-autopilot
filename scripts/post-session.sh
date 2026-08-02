#!/usr/bin/env bash
# ============================================
# Solo Dev Autopilot — 会话结束后的自动化脚本
# 功能：
#   1. 生成/更新代码地图 (CODEMAP.md)
#   2. 更新项目记忆 (PROJECT-MEMORY.md)
#   3. 记录本次会话的变更摘要
#   4. 生成"上次会话回顾"写入 SESSION_DRIVER.md
#   5. 检查是否有新的待办事项
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
  log "建议：下次开会话时说以下命令来恢复上下文："
  echo ""
  echo "  读取 PROJECT-MEMORY.md、CODEMAP.md 和 SESSION_DRIVER.md"
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

# ---- Step 4: 生成上次会话回顾写入 SESSION_DRIVER.md ----
generate_session_review() {
  local session_driver="${PROJECT_ROOT}/SESSION_DRIVER.md"

  cd "$PROJECT_ROOT"

  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  local branch=$(git branch --show-current 2>/dev/null || echo "unknown")

  # 收集本次会话的 commit 信息
  local recent_commits=""
  local commit_hashes=$(git log --oneline -10 2>/dev/null | head -10)
  if [ -n "$commit_hashes" ]; then
    while IFS= read -r line; do
      recent_commits="${recent_commits}- ${line}"$'\n'
    done <<< "$commit_hashes"
  else
    recent_commits="- （无提交记录）"$'\n'
  fi

  # 收集变更的文件列表（带简要说明）
  local changed_file_list=""
  local changed_files=$(git diff --name-only HEAD~5 HEAD 2>/dev/null || git diff --name-only HEAD 2>/dev/null || echo "")
  if [ -n "$changed_files" ]; then
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      local status="M"
      if [ ! -f "$f" ]; then status="D"; fi
      changed_file_list="${changed_file_list}- [${status}] \`${f}\`"$'\n'
    done <<< "$changed_files"
  else
    changed_file_list="- （无文件变更）"$'\n'
  fi

  # 收集未完成的 TODO（从代码中扫描）
  local todo_list=""
  local todos=$(grep -rn "TODO\|FIXME\|HACK" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" --include="*.go" --include="*.rs" "$PROJECT_ROOT/src" "$PROJECT_ROOT/app" "$PROJECT_ROOT/apps" 2>/dev/null | head -10 || echo "")
  if [ -n "$todos" ]; then
    while IFS= read -r line; do
      [ -z "$line" ] && continue
      todo_list="${todo_list}- ${line}"$'\n'
    done <<< "$todos"
  else
    todo_list="- （无未完成 TODO）"$'\n'
  fi

  # 构建回顾区块内容
  local review_block="**时间**：${timestamp} | **分支**：${branch}

**本次提交记录**：
${recent_commits}
**变更文件**：
${changed_file_list}
**未完成 TODO**：
${todo_list}"

  # 如果 SESSION_DRIVER.md 不存在，创建一个空白骨架
  if [ ! -f "$session_driver" ]; then
    log "SESSION_DRIVER.md 不存在，创建空白骨架"
    cat > "$session_driver" << 'DRIVER_EOF'
# Session Driver

## 本轮目标

- [ ] （填写本轮目标）

## 上次会话回顾

*（等待自动填充）*

## 当前进度

### 已完成
- [x] （示例）项目初始化

### 进行中
- [ ] （示例）用户认证模块

### 待开始
- [ ] （示例）文章管理

## 已知阻塞项

- （无）

## 备注

- （无）
DRIVER_EOF
  fi

  # 用 sed 替换"上次会话回顾"区块
  # 策略：找到 "## 上次会话回顾" 和下一个 "## " 之间的内容，替换掉
  local temp_file=$(mktemp)

  # 用 awk 替换区块内容
  awk -v review="$review_block" '
    /^## 上次会话回顾/ { in_block=1; print; print ""; print review; next }
    /^## / && in_block { in_block=0 }
    !in_block { print }
    in_block && /^\*（等待自动填充）\*/ { next }
  ' "$session_driver" > "$temp_file"

  # 如果 awk 没有正确处理（文件格式不同），用更简单的方式追加
  if [ ! -s "$temp_file" ]; then
    cp "$session_driver" "$temp_file"
  fi

  mv "$temp_file" "$session_driver"
  log "上次会话回顾已写入 SESSION_DRIVER.md"
}

# ---- Step 5: 检查健康状态 ----
health_check() {
  local warnings=0

  # 检查是否有 .env 文件但它在 .gitignore 里没有
  if [ -f "${PROJECT_ROOT}/.env" ] && grep -q "^\.env$" "${PROJECT_ROOT}/.gitignore" 2>/dev/null; then
    : # 正常情况
  elif [ -f "${PROJECT_ROOT}/.env" ]; then
    warn " ..env 文件存在但可能未被 gitignore 忽略！"
    ((warnings++))
  fi

  # 检查 node_modules 是否意外被跟踪
  if git ls-files --error-unmatch "${PROJECT_ROOT}/node_modules" &>/dev/null 2>&1; then
    warn " node_modules 被 git 跟踪了！应该加入 .gitignore"
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
    warn "发现大文件（>10MB），可能不应该提交："
    echo "$large_files" | while read -r f; do
      warn "   $(basename "$f") ($(du -h "$f" | cut -f1))"
    done
    ((warnings++))
  fi

  if [ "$warnings" -gt 0 ]; then
    warn "发现 ${warnings} 个潜在问题，建议修复"
  else
    log "健康检查通过"
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
  generate_session_review
  health_check

  log "会话后处理完成"
  log "下次启动时说：读取 PROJECT-MEMORY.md、CODEMAP.md 和 SESSION_DRIVER.md"
}

main "$@"