?#!/usr/bin/env bash
# Solo Dev Autopilot - ?? Git Hooks
# ??:bash scripts/install-git-hooks.sh

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
  error "?????? Git ??(??? .git/hooks/)"
  exit 1
fi

log "?? pre-commit hook..."
cp "${TEMPLATES_DIR}/pre-commit-hook" "${HOOKS_DIR}/pre-commit"
chmod +x "${HOOKS_DIR}/pre-commit"
log "pre-commit hook ???"

log "?? pre-push hook..."
cp "${TEMPLATES_DIR}/pre-push-hook" "${HOOKS_DIR}/pre-push"
chmod +x "${HOOKS_DIR}/pre-push"
log "pre-push hook ???"

log ""
log "========================================="
log " Git Hooks ????!"
log "========================================="
log " ???:"
log "   ??? pre-commit  ? ??? P0 ??"
log "   ??? pre-push    ? ???????"
log ""
log " ??:Git Hooks ??? git ??,?????????"