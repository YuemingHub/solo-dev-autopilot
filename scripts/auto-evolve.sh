#!/usr/bin/env bash
# ============================================
# Solo Dev AutoPilot — 自动进化脚本
# 
# 功能：搜索 GitHub 上最新的优秀 MCP Server、Skill、工具配置，
#       与现有方案对比，如果发现更优方案则替换。
#       
# 策略：精选替换式，非堆叠式。发现更好的就替换，不叠加。
#
# 使用方式：
#   手动: bash scripts/auto-evolve.sh [--dry-run]
#   自动: GitHub Actions 每周运行 (.github/workflows/auto-evolve.yml)
# ============================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EVOLVE_LOG="${REPO_ROOT}/.solo-dev-autopilot/evolve.log"
CHANGELOG="${REPO_ROOT}/docs/EVOLVE_CHANGELOG.md"

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

# ---- 颜色 ----
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${CYAN}[evolve]${NC}  $*"; }
ok()    { echo -e "${GREEN}[evolve]${NC}  ✅ $*"; }
warn()  { echo -e "${YELLOW}[evolve]${NC}  ⚠️  $*"; }
err()   { echo -e "${RED}[evolve]${NC}  ❌ $*"; }

mkdir -p "$(dirname "$EVOLVE_LOG")"

log_evolve() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$EVOLVE_LOG"
}

# ---- 搜索函数 ----
search_github() {
  local query="$1"
  local sort="${2:-stars}"
  local per_page="${3:-10}"
  
  # 使用 curl 调用 GitHub Search API（无需认证即可使用，有速率限制）
  local url="https://api.github.com/search/repositories?q=${query}&sort=${sort}&order=desc&per_page=${per_page}"
  
  local response
  response=$(curl -sf "$url" 2>/dev/null || echo '{"items":[]}')
  
  echo "$response"
}

extract_repo_info() {
  local json="$1"
  # 提取 repo 名称、star 数、描述、最近更新时间
  echo "$json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data.get('items', [])[:5]:
    print(f\"{item['full_name']}|{item['stargazers_count']}|{item.get('description','')[:80]}|{item.get('updated_at','')[:10]}|{item['html_url']}\")
" 2>/dev/null || echo "解析失败"
}

# ---- 对比逻辑 ----
check_category() {
  local category_name="$1"
  local search_query="$2"
  local current_best="$3"
  local criteria="$4"
  
  info "━━━ 检查: ${category_name} ━━━"
  info "当前最优: ${current_best}"
  info "搜索条件: ${search_query}"
  info "评估标准: ${criteria}"
  
  local results
  results=$(search_github "$search_query" stars 5)
  
  local top_repos
  top_repos=$(extract_repo_info "$results")
  
  if [ -z "$top_repos" ] || [[ "$top_repos" == *"解析失败"* ]]; then
    warn "搜索失败，跳过 ${category_name}"
    return
  fi
  
  info "GitHub Top 结果:"
  echo "$top_repos" | while IFS='|' read -r name stars desc updated url; do
    info "  ⭐${stars}  ${name} — ${desc} (${updated})"
  done
  
  # TODO: 这里可以添加更智能的对比逻辑
  # 目前输出结果供人工审核
  local top_repo
  top_repo=$(echo "$top_repos" | head -1 | cut -d'|' -f1)
  
  if [ "$top_repo" != "$current_best" ]; then
    warn "发现不同的热门仓库: ${top_repo}"
    warn "当前: ${current_best}"
    warn "这不一定意味着更好，请根据以下标准判断："
    info "  ${criteria}"
    echo ""
    
    if [ "$DRY_RUN" = true ]; then
      info "[DRY RUN] 不会修改任何文件"
    else
      # 记录为候选替换项
      echo "## $(date '+%Y-%m-%d') ${category_name}" >> "${CHANGELOG}.tmp"
      echo "- **候选**: ${top_repo}" >> "${CHANGELOG}.tmp"
      echo "- **当前**: ${current_best}" >> "${CHANGELOG}.tmp"
      echo "- **Top 结果**:" >> "${CHANGELOG}.tmp"
      echo "$top_repos" | while IFS='|' read -r name stars desc updated url; do
        echo "  - ⭐${stars} [\`${name}\`](${url}) — ${desc}" >> "${CHANGELOG}.tmp"
      done
      echo "" >> "${CHANGELOG}.tmp"
    fi
  else
    ok "${category_name}: 当前选择仍是 GitHub 最热 👍"
  fi
}

# ---- 主流程 ----
main() {
  echo ""
  echo "╔══════════════════════════════════════════╗"
  echo "║   🔄 Solo Dev Autopilot — 自动进化       ║"
  echo "║   搜索最优解 · 精选替换 · 拒绝臃肿       ║"
  echo "╚══════════════════════════════════════════╝"
  echo ""
  
  if [ "$DRY_RUN" = true ]; then
    info "🔍 DRY RUN 模式 — 只搜索不修改"
  fi
  
  log_evolve "开始进化扫描"
  
  # ---- 类别 1: MCP Server — GitHub 操作 ----
  check_category \
    "GitHub MCP Server" \
    "mcp-server-github topic:mcp" \
    "modelcontextprotocol/server-github" \
    "Stars 数、活跃度（最近更新）、官方维护优先"
  
  # ---- 类别 2: MCP Server — 数据库 ----
  check_category \
    "PostgreSQL MCP Server" \
    "mcp-server-postgres topic:mcp" \
    "modelcontextprotocol/server-postgres" \
    "Stars 数、维护状态、功能完整性"
  
  # ---- 类别 3: MCP Server — 浏览器自动化 ----
  check_category \
    "Browser Automation MCP" \
    "mcp-server-puppeteer OR mcp-server-playwright topic:mcp" \
    "@anthropic-ai/mcp-server-puppeteer" \
    "稳定性、社区活跃度、文档质量"
  
  # ---- 类别 4: MCP Server — 结构化思维 ----
  check_category \
    "Sequential Thinking MCP" \
    "mcp-sequential-thinking topic:mcp" \
    "modelcontextprotocol/server-sequential-thinking" \
    "实用性、集成便利性"
  
  # ---- 类别 5: 全栈框架趋势 ----
  check_category \
    "全栈框架 (Bun+Hono)" \
    "hono bun framework" \
    "honojs/hono" \
    "Stars 增长速度、下载量、社区讨论热度"
  
  # ---- 类别 6: UI 组件库趋势 ----
  check_category \
    "React UI 组件库 (shadcn/ui)" \
    "shadcn-ui react components" \
    "shadcn-ui/shadcn-ui" \
    "Stars 数、更新频率、采用率"
  
  # ---- 类别 7: ORM 趋势 ----
  check_category \
    "TypeScript ORM (Drizzle)" \
    "drizzle-orm typescript orm" \
    "drizzle-team/drizzle-orm" \
    "性能、TypeScript 集成度、文档质量"
  
  # ---- 类别 8: 新兴 MCP Server 发现 ----
  info "━━━ 搜索: 新兴 MCP Server ━━━"
  local new_servers
  new_servers=$(search_github "mcp-server created:>2025-06-01" updated sort=stars 10)
  local new_top
  new_top=$(extract_repo_info "$new_servers")
  
  if [ -n "$new_top" ] && [[ "$new_top" != *"解析失败"* ]]; then
    info "近期新出的 MCP Server："
    echo "$new_top" | head -5 | while IFS='|' read -r name stars desc updated url; do
      info "  🆕 ⭐${stars}  ${name} — ${desc}"
    done
  fi
  
  # ---- 总结 ----
  echo ""
  echo "========================================="
  ok "进化扫描完成"
  echo ""
  
  if [ -f "${CHANGELOG}.tmp" ]; then
    info "发现候选替换项，详情见 ${CHANGELOG}.tmp"
    info "审核后可合并到 ${CHANGELOG}"
    
    if [ "$DRY_RUN" = false ]; then
      warn "请在确认后将 ${CHANGELOG}.tmp 内容合并到 docs/EVOLVE_CHANGELOG.md"
    fi
  else
    info "所有类别均保持当前选择，无需变更"
  fi
  
  log_evolve "进化扫描完成"
  
  echo ""
  info "💡 提示：定期运行此脚本保持技术栈最新"
  info "   bash scripts/auto-evolve.sh          # 正常模式"
  info "   bash scripts/auto-evolve.sh --dry-run  # 仅查看不修改"
}

main "$@"
