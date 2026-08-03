#!/usr/bin/env bash
# ============================================
# Solo Dev Autopilot — 一键安装与环境检测
# 用法: bash scripts/setup.sh [项目路径]
# ============================================

set -euo pipefail

# ---- 颜色输出 ----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}   $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; }

# ---- 路径配置 ----
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${1:-$(pwd)}"

# ---- 检测工具环境 ----
detect_environment() {
  info "正在检测你的开发环境..."
  
  local detected_tools=()
  
  # 检测 Node.js / Bun
  if command -v node &>/dev/null; then
    NODE_VERSION=$(node --version)
    success "Node.js: ${NODE_VERSION}"
    detected_tools+=("node")
  else
    warn "未检测到 Node.js"
  fi
  
  if command -v bun &>/dev/null; then
    BUN_VERSION=$(bun --version)
    success "Bun: ${BUN_VERSION}"
    detected_tools+=("bun")
  fi
  
  # 检测包管理器
  if command -v pnpm &>/dev/null; then
    PNPM_VERSION=$(pnpm --version)
    success "pnpm: ${PNPM_VERSION}"
    detected_tools+=("pnpm")
  elif command -v npm &>/dev/null; then
    NPM_VERSION=$(npm --version)
    success "npm: ${NPM_VERSION}"
    detected_tools+=("npm")
  fi
  
  # 检测 Git
  if command -v git &>/dev/null; then
    GIT_VERSION=$(git --version)
    success "Git: ${GIT_VERSION}"
  else
    error "未检测到 Git！请先安装 Git"
    exit 1
  fi
  
  # 检测 AI 编程工具
  info ""
  info "检测 AI 编程工具..."
  
  local ai_tool=""
  if command -v claude &>/dev/null || npx claude --version &>/dev/null 2>&1; then
    success "检测到 Claude Code ✅"
    ai_tool="claude-code"
  fi
  
  if [ -d "${HOME}/.cursor" ] 2>/dev/null || command -v cursor &>/dev/null 2>&1; then
    success "检测到 Cursor ✅"
    ai_tool="${ai_tool:+${ai_tool} }cursor"
  fi
  
  if [ -d "${HOME}/.reasonix" ] 2>/dev/null || command -v reasonix &>/dev/null 2>&1; then
    success "检测到 Reasonix ✅"
    ai_tool="${ai_tool:+${ai_tool} }reasonix"
  fi
  
  if [ -z "$ai_tool" ]; then
    warn "未检测到已安装的 AI 编程工具"
    warn "支持的工具：Claude Code, Cursor, Reasonix, Cline, Windsurf"
    info "你可以继续安装，稍后手动配置 MCP 和 Skill"
  fi
  
  export DETECTED_TOOLS="${detected_tools[*]}"
  export AI_TOOL="$ai_tool"
}

# ---- 复制 Skill 文件 ----
install_skills() {
  info ""
  info "安装 Skill 文件..."
  
  # v2: 官方 SKILL.md 文件夹格式 → .claude/skills/（Claude Code 原生识别）
  local skills_src="${REPO_ROOT}/.claude/skills"
  local skills_dest="${TARGET_DIR}/.claude/skills"
  
  if [ ! -d "$skills_src" ]; then
    error "源目录不存在: ${skills_src}"
    exit 1
  fi
  
  mkdir -p "$skills_dest"
  cp -r "${skills_src}/"* "${skills_dest}/"
  
  # 统计复制的 skill 数量
  local skill_count=$(find "$skills_dest" -name "SKILL.md" | wc -l | tr -d ' ')
  success "已复制 ${skill_count} 个官方格式 Skill 到 ${skills_dest}/"
  
  # 兼容层：v1 平铺 .md 源文件保留到 skills/（社区工具适配参考，v2 主推 Claude Code）
  local legacy_src="${REPO_ROOT}/skills"
  if [ -d "$legacy_src" ]; then
    mkdir -p "${TARGET_DIR}/skills"
    cp -r "${legacy_src}/"*.md "${TARGET_DIR}/skills/" 2>/dev/null || true
    success "已复制 v1 平铺源文件到 ${TARGET_DIR}/skills/（仅作参考）"
  fi
  
  # 为各工具配置 Skill 路径
  setup_tool_skills
}

setup_tool_skills() {
  info ""
  info "为各工具配置 Skill 路径..."
  
  # Claude Code: .claude/skills/ 已在上一步完成（官方 SKILL.md 文件夹格式，自动识别）
  if [ -d "${TARGET_DIR}/.claude/skills" ]; then
    success "Claude Code 已就绪 → .claude/skills/（官方格式，自动识别）"
  fi
  
  # 其他工具：v2 优先 Claude Code 全适配，其余标注"社区适配中"（D4 决策）
  for tool in cursor reasonix cline; do
    if [ -d "${TARGET_DIR}/.${tool}" ] || echo "$AI_TOOL" | grep -q "$tool"; then
      warn "${tool}: 社区适配中（v2 优先 Claude Code），配置文件保留在 configs/tool-presets/"
    fi
  done
}

# ---- superpowers 上游方法论：检测与安装引导 ----
install_superpowers() {
  info ""
  info "检测 superpowers 上游方法论..."
  info "（superpowers 是我们的方法论底座：brainstorm → plan → TDD → review → finish）"
  
  local sp_detected=""
  if [ -d "${HOME}/.claude/plugins" ]; then
    if ls "${HOME}/.claude/plugins/installed" 2>/dev/null | grep -qi superpowers; then
      sp_detected="installed"
    elif ls "${HOME}/.claude/plugins/marketplaces" 2>/dev/null | grep -qi superpowers; then
      sp_detected="marketplace"
    fi
  fi
  
  if [ -n "$sp_detected" ]; then
    success "已检测到 superpowers（$sp_detected）✅"
    return
  fi
  
  warn "未检测到 superpowers"
  info "我们的 Skill 是 superpowers 的中文新手增强层，建议安装："
  
  case "$AI_TOOL" in
    *claude*)
      info "Claude Code 安装（二选一）："
      info "  官方市场: /plugin install superpowers@claude-plugins-official"
      info "  SP 市场:  /plugin marketplace add obra/superpowers-marketplace"
      info "            /plugin install superpowers@superpowers-marketplace"
      ;;
    *cursor*)
      info "Cursor 安装：在 Agent 对话框输入 /add-plugin superpowers"
      ;;
    *)
      info "其他工具：参考 https://github.com/obra/superpowers 官方安装文档"
      ;;
  esac
  
  read -rp "是否打开 superpowers 官方文档？(y/n) [默认: n] " open_sp_docs
  if [[ "${open_sp_docs:-n}" =~ ^[Yy] ]]; then
    if command -v open >/dev/null 2>&1; then
      open https://github.com/obra/superpowers
    elif command -v xdg-open >/dev/null 2>&1; then
      xdg-open https://github.com/obra/superpowers
    else
      info "请手动打开: https://github.com/obra/superpowers"
    fi
  fi
}

# ---- 安装模板文件 ----
install_templates() {
  info ""
  info "安装项目模板..."
  
  # .gitignore
  if [ ! -f "${TARGET_DIR}/.gitignore" ]; then
    cp "${REPO_ROOT}/templates/gitignore" "${TARGET_DIR}/.gitignore"
    success ".gitignore 已创建"
  else
    warn ".gitignore 已存在，跳过（手动合并请参考 templates/gitignore）"
  fi
  
  # 环境变量模板
  if [ ! -f "${TARGET_DIR}/.env.example" ] && [ ! -f "${TARGET_DIR}/.env.example.env" ]; then
    cp "${REPO_ROOT}/templates/env-example.env" "${TARGET_DIR}/.env.example"
    success ".env.example 已创建"
  else
    warn ".env.example 已存在，跳过"
  fi
  
  # 项目记忆模板
  if [ ! -f "${TARGET_DIR}/PROJECT-MEMORY.md" ]; then
    cp "${REPO_ROOT}/templates/PROJECT-MEMORY-template.md" "${TARGET_DIR}/PROJECT-MEMORY.md"
    success "PROJECT-MEMORY.md 已创建（请编辑填写你的项目信息）"
  else
    warn "PROJECT-MEMORY.md 已存在，跳过"
  fi

  # 新手启动指南
  if [ ! -f "${TARGET_DIR}/ONBOARDING.md" ]; then
    cp "${REPO_ROOT}/templates/ONBOARDING-template.md" "${TARGET_DIR}/ONBOARDING.md"
    success "ONBOARDING.md 已创建（新手必读！）"
  else
    warn "ONBOARDING.md 已存在，跳过"
  fi

  # 会话方向盘
  if [ ! -f "${TARGET_DIR}/SESSION_DRIVER.md" ]; then
    cp "${REPO_ROOT}/templates/SESSION_DRIVER-template.md" "${TARGET_DIR}/SESSION_DRIVER.md"
    success "SESSION_DRIVER.md 已创建（每次会话开始时填写）"
  else
    warn "SESSION_DRIVER.md 已存在，跳过"
  fi

  # AI 协作指南
  if [ ! -f "${TARGET_DIR}/AI-GUIDE.md" ]; then
    cp "${REPO_ROOT}/templates/AI-GUIDE-template.md" "${TARGET_DIR}/AI-GUIDE.md"
    success "AI-GUIDE.md 已创建（新手必读！了解 AI 能做什么、怎么防幻觉）"
  else
    warn "AI-GUIDE.md 已存在，跳过"
  fi
}

# ---- 配置 MCP（交互式）---- 
configure_mcp() {
  info ""
  info "MCP 服务器配置"
  info "─────────────────────────────"
  info "推荐的最小配置："
  info "  1. github        — GitHub 操作（需要 GITHUB_TOKEN）"
  info "  2. filesystem     — 文件系统访问"
  info "  3. sequential-thinking — 结构化思维引擎"
  info ""
  read -rp "是否现在配置 MCP？(y/n) [默认: y] " configure_mcp_now
  configure_mcp_now=${configure_mcp_now:-y}
  
  if [[ "$configure_mcp_now" =~ ^[Yy] ]]; then
    read -rp "输入你的 GitHub Personal Access Token (留空跳过): " github_token
    
    if [ -n "$github_token" ]; then
      # 根据检测到的工具写入对应配置
      if echo "$AI_TOOL" | grep -q "reasonix"; then
        configure_mcp_reasonix "$github_token"
      elif echo "$AI_TOOL" | grep -q "claude"; then
        configure_mcp_claude "$github_token"
      elif echo "$AI_TOOL" | grep -q "cursor"; then
        configure_mcp_cursor "$github_token"
      else
        warn "未检测到支持的 AI 工具，MCP 配置文件已生成在 configs/mcp-servers.json"
        info "请手动将配置复制到你的工具配置中"
      fi
    else
      info "跳过 GitHub Token 配置，可稍后手动设置"
      info "完整 MCP 配置参考: ${REPO_ROOT}/configs/mcp-servers.json"
    fi
  fi
}

configure_mcp_reasonix() {
  local token="$1"
  local config_file="${HOME}/.reasonix/config.json"
  
  info "写入 Reasonix MCP 配置 → ${config_file}"
  
  if [ ! -f "$config_file" ]; then
    echo '{}' > "$config_file"
  fi
  
  # 使用 Node.js 合并 JSON（如果可用）
  if command -v node &>/dev/null; then
    node -e "
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('${config_file}', 'utf8'));
config.mcp = config.mcp || {};
config.mcp.servers = config.mcp.servers || {};
config.mcp.servers.github = {
  transport: 'stdio',
  command: 'npx',
  args: ['-y', '@modelcontextprotocol/server-github'],
  env: { GITHUB_PERSONAL_ACCESS_TOKEN: '${token}' }
};
config.mcp.servers.filesystem = {
  transport: 'stdio',
  command: 'npx',
  args: ['-y', '@modelcontextprotocol/server-filesystem', '${TARGET_DIR}']
};
config.mcp.servers['sequential-thinking'] = {
  transport: 'stdio',
  command: 'npx',
  args: ['-y', '@modelcontextprotocol/server-sequential-thinking']
};
fs.writeFileSync('${config_file}', JSON.stringify(config, null, 2));
console.log('OK');
" 2>/dev/null && success "Reasonix MCP 配置完成" || warn "手动配置见 configs/tool-presets/reasonix.json"
  else
    warn "需要 Node.js 来自动配置，请手动复制配置"
  fi
}

configure_mcp_claude() {
  local token="$1"
  warn "Claude Code MCP 配置请参考: ${REPO_ROOT}/configs/tool-presets/claude-code.json"
  info "运行: cat configs/tool-presets/claude-code.json >> ~/.claude/settings.json"
}

configure_mcp_cursor() {
  local token="$1"
  warn "Cursor MCP 配置请参考: ${REPO_ROOT}/configs/tool-presets/cursor.json"
  info "在 Cursor Settings → MCP 中添加服务器"
}

# ---- 设置 Git Hooks ----
setup_git_hooks() {
  info ""
  info "配置 Git Hooks（可选）..."
  read -rp "是否启用自动代码地图更新 hook？(y/n) [默认: y] " enable_hooks
  enable_hooks=${enable_hooks:-y}
  
  if [[ "$enable_hooks" =~ ^[Yy] ]]; then
    local hooks_dir="${TARGET_DIR}/.git/hooks"
    mkdir -p "$hooks_dir"
    
    # Post-commit hook: 更新代码地图
    cat > "${hooks_dir}/post-commit" << 'HOOK'
#!/bin/bash
# Solo Dev Autopilot: 提交后提示更新代码地图
echo "🗺️  提示：运行 '/skill context-map' 更新代码地图以保持上下文同步"
HOOK
    chmod +x "${hooks_dir}/post-commit"
    success "Git post-commit hook 已安装"
  fi
}

# ---- 初始化 Git ----
init_git() {
  if [ -d "${TARGET_DIR}/.git" ]; then
    warn "Git 仓库已存在，跳过初始化"
    return
  fi
  
  info ""
  info "初始化 Git 仓库..."
  cd "$TARGET_DIR"
  git init
  git add -A
  git commit -m "chore: initialize with Solo Dev Autopilot" 2>/dev/null || true
  success "Git 仓库已初始化并提交"
}

# ---- 最终检查与总结 ----
print_summary() {
  echo ""
  echo "============================================="
  echo -e "${GREEN}✅ Solo Dev Autopilot 安装完成！${NC}"
  echo "============================================="
  echo ""
  echo "📁 目标目录: ${TARGET_DIR}"
  echo "🔧 已安装:"
  echo "   ├── .claude/skills/  $(find "${TARGET_DIR}/.claude/skills" -name 'SKILL.md' 2>/dev/null | wc -l | tr -d ' ') 个 Skill（官方格式）"
  echo "   ├── superpowers       已装=$(ls "${HOME}/.claude/plugins/installed" 2>/dev/null | grep -ci superpowers)（0=未装，按引导安装）"
  echo "   ├── .gitignore        ✅"
  echo "   ├── .env.example      ✅"
  echo "   ├── PROJECT-MEMORY.md ✅"
  echo "   ├── ONBOARDING.md     ✅"
  echo "   ├── AI-GUIDE.md       ✅"
  echo "   └── SESSION_DRIVER.md ✅"
  echo ""
  echo "🚀 下一步操作:"
  echo "   1. 阅读 AI-GUIDE.md（了解 AI 能做什么、怎么防幻觉）"
  echo "   2. 阅读 ONBOARDING.md（了解记忆文件和启动咒语）"
  echo "   3. 编辑 PROJECT-MEMORY.md 填写项目信息"
  echo "   4. 复制 .env.example 为 .env 并填入实际值"
  echo "   5. 如未装 superpowers，在 Claude Code 里执行: /plugin install superpowers@claude-plugins-official"
  echo "   6. 启动你的 AI 编程工具"
  echo "   7. 说: '读取 PROJECT-MEMORY.md、CODEMAP.md 和 SESSION_DRIVER.md'"
  echo ""
  echo "📖 文档:"
  echo "   完整入门指南 → ${REPO_ROOT}/docs/getting-started.md"
  echo "   新手避坑手册 → ${REPO_ROOT}/docs/newbie-pitfalls.md"
  echo "   v2 开发蓝图   → ${REPO_ROOT}/docs/BLUEPRINT-v2.md"
  echo ""
  echo "💡 常用命令:"
  echo "   /skill onboarding        — 首次使用引导（装 superpowers）"
  echo "   /skill context-map       — 生成/更新代码地图"
  echo "   /skill fullstack-scaffold— 创建新项目"
  echo "   /skill code-review       — 代码审查"
  echo "   /skill commit-helper     — 生成提交信息"
  echo "   /skill deploy-gate       — 部署门禁（人工确认红线）"
  echo "   /skill troubleshoot      — 问题排查"
  echo ""
}

# ---- 主流程 ----
main() {
  echo ""
  echo "╔══════════════════════════════════════════╗"
  echo "║   🚀 Solo Dev Autopilot Installer        ║"
  echo "║   一个人，一个 AI，一个完整产品           ║"
  echo "╚══════════════════════════════════════════╝"
  echo ""
  
  detect_environment
  install_skills
  install_superpowers
  install_templates
  configure_mcp
  setup_git_hooks
  init_git
  print_summary
}

main "$@"
