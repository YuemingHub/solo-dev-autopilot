#!/usr/bin/env bash
# Solo Dev Autopilot — 安装 Git Hooks
# 用法：bash scripts/install-git-hooks.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOKS_DIR="${PROJECT_ROOT}/.git/hooks"
TEMPLATES_DIR="${PROJECT_ROOT}/templates"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()   { echo -e "${GREEN}[git-hooks]${NC} $*"; }
warn()  { echo -e "${YELLOW}[git-hooks]${NC} $*"; }
error() { echo -e "${RED}[git-hooks]${NC} $*"; }

if [ ! -d "$HOOKS_DIR" ]; then
  error "当前目录不是 Git 仓库（找不到 .git/hooks/）"
  exit 1
fi

log "安装 pre-commit hook..."
cp "${TEMPLATES_DIR}/pre-commit-hook" "${HOOKS_DIR}/pre-commit"
chmod +x "${HOOKS_DIR}/pre-commit"
log "pre-commit hook 已安装"

log "安装 pre-push hook..."
cp "${TEMPLATES_DIR}/pre-push-hook" "${HOOKS_DIR}/pre-push"
chmod +x "${HOOKS_DIR}/pre-push"
log "pre-push hook 已安装"

log ""
log "========================================="
log " Git Hooks 安装完成！"
log "========================================="
log " 已安装："
log "   ├── pre-commit  → 提交前 P0 检查"
log "   └── pre-push    → 推送前审查提醒"
log ""
log " 提示：Git Hooks 不会被 git 跟踪，换电脑后需重新安装"
