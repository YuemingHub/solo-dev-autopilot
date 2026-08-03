#!/usr/bin/env bash
# Solo Dev Autopilot — 安装 Git Hooks（带备份）
# 用法：bash scripts/install-git-hooks.sh
# 安全特性：安装前自动备份已有 hook 到 .git/hooks-backup/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOKS_DIR="${PROJECT_ROOT}/.git/hooks"
TEMPLATES_DIR="${PROJECT_ROOT}/templates"
BACKUP_DIR="${PROJECT_ROOT}/.git/hooks-backup"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()    { echo -e "${GREEN}[git-hooks]${NC} $*"; }
warn()   { echo -e "${YELLOW}[git-hooks]${NC} $*"; }
error()  { echo -e "${RED}[git-hooks]${NC} $*" >&2; exit 1; }

# 验证 Git 仓库
if [ ! -d "$HOOKS_DIR" ]; then
  error "当前目录不是 Git 仓库（找不到 .git/hooks/）"
fi

# 验证模板文件存在
template_precommit="${TEMPLATES_DIR}/pre-commit-hook"
template_prepush="${TEMPLATES_DIR}/pre-push-hook"
if [ ! -f "$template_precommit" ]; then
  error "找不到模板文件：$template_precommit"
fi
if [ ! -f "$template_prepush" ]; then
  error "找不到模板文件：$template_prepush"
fi

# 备份已有 hooks
mkdir -p "$BACKUP_DIR"
for hook_name in pre-commit pre-push; do
  existing="${HOOKS_DIR}/${hook_name}"
  if [ -f "$existing" ]; then
    # 检查是否已经是我们的（避免重复备份）
    if head -1 "$existing" | grep -q "Solo Dev Autopilot" 2>/dev/null; then
      log "${hook_name} 已是本仓库安装，跳过备份"
    else
      backup_file="${BACKUP_DIR}/${hook_name}.$(date +%Y%m%d%H%M%S)"
      cp "$existing" "$backup_file"
      warn "已有 ${hook_name} 已备份到 ${backup_file}"
    fi
  fi
done

# 安装 hooks
cp "$template_precommit" "${HOOKS_DIR}/pre-commit"
chmod +x "${HOOKS_DIR}/pre-commit"
log "已安装：pre-commit (P0 阻止 + P1 警告)"

cp "$template_prepush" "${HOOKS_DIR}/pre-push"
chmod +x "${HOOKS_DIR}/pre-push"
log "已安装：pre-push (推送前审查提醒)"

log ""
log "========================================="
log " Git Hooks 安装完成！"
log "========================================="
log " 原有 hook 备份在：${BACKUP_DIR}"
log ""
log " 提示：Git Hooks 不会被 git 跟踪，换电脑后需重新安装"