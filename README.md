 🚀 Solo Dev Autopilot

> **一个人，一个 AI，一个完整产品。**  
> 通用 Solo 开发自动驾驶环境 —— Clone、配置一次、永久自动驾驶。

## ✨ 核心价值

| 新手痛点 | 我们的解法 |
|---------|-----------|
| 不知道选什么技术栈 | 预设默认全栈配置 |
| 每次开会话 AI 不记得上下文 | 自动代码地图 + 持久化记忆 |
| 写完代码不知道对不对 | 自动 P0-P3 分级审查 |
| 不知道怎么提交/部署 | 一键 commit + 部署前检查 |
| 不知道怎么排错 | 新手问题自动排查 Skill |
| 不知道 AI 能帮我什么 | AI 协作指南（能力地图 + 防幻觉） |
| 想法混乱不会拆任务 | task-planner Skill（目标拆解 + 防漂移） |
| 会话结束忘了做到哪 | SESSION_DRIVER 自动回顾 + 进度跟踪 |
| 工具换了要重新配 | 工具无关设计，一套配置通用 |

## 🎯 适用工具

本仓库**不绑定任何特定工具**，只要支持 MCP + Skill 的环境都能用：

- **Claude Code** (`.claude/skills/`)
- **Cursor** (`.cursor/rules/`)
- **Cline** (`.cline/`)
- **Reasonix** (`.reasonix/skills/`)
- **Windsurf** (`.windsurf/rules/`)
- **任何支持 MCP 协议的 IDE / 本地工作台**

## ⚡ 三步开始

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USERNAME/solo-dev-autopilot.git
cd solo-dev-autopilot

# 2. 运行一键安装（检测你的环境并自动配置）
# macOS / Linux / Git Bash:
bash scripts/setup.sh

# Windows PowerShell:
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1

# 3. 把这个目录作为你的项目根目录开始开发
# 或者把 skills/ 和 templates/ 复制到已有项目中
```

## 📂 仓库结构

```
solo-dev-autopilot/
├── README.md
├── LICENSE                            ← MIT
├── CHANGELOG-v2.md                    ← v2 更新日志
├── BOOTSTRAP-PROMPT.md                ← 首次启动引导
│
├── .claude/                           ← 🧠 Claude Code 原生适配（v2 新增）
│   ├── settings.json                  │   三级权限模型（auto-allow / ask / deny）
│   └── skills/                        │   官方 SKILL.md 格式技能（Claude Code 自动识别）
│       ├── api-designer/SKILL.md      │   API 接口设计
│       ├── code-review/SKILL.md       │   P0-P3 分级代码审查
│       ├── commit-helper/SKILL.md     │   智能 Commit 信息
│       ├── context-map/SKILL.md       │   代码地图（会话恢复核心）
│       ├── deploy-check/SKILL.md      │   部署前安全检查
│       ├── fullstack-scaffold/SKILL.md│   全栈脚手架生成
│       ├── git-workflow/SKILL.md      │   Git 工作流引导
│       ├── task-planner/SKILL.md      │   目标拆解与防漂移
│       └── troubleshoot/SKILL.md      │   新手问题排查
│
├── skills/                            ← ⚠️ v1 源文件（已迁移至 .claude/skills/）
│
├── configs/                           ← ⚙️ 各工具的预设配置
│   ├── mcp-servers.json              │   MCP 服务器推荐配置
│   └── tool-presets/                  │   各工具适配配置
│       ├── claude-code.json          │   三级权限 + MCP + skillsPath
│       ├── cursor.json               │
│       ├── cline.json                │
│       └── reasonix.json             │   三级权限 + hooks
│
├── scripts/                           ← 🔧 自动化脚本
│   ├── setup.sh / setup.ps1          │   一键安装（macOS/Linux/Windows）
│   ├── post-session.sh               │   会话结束自动化（代码地图+记忆更新）
│   ├── install-git-hooks.sh          │   Git Hooks 安装（带备份）
│   ├── install-git-hooks.ps1         │   Git Hooks 安装（Windows）
│   └── auto-evolve.sh                │   社区方案搜索
│
├── templates/                         ← 📝 项目模板
│   ├── AI-GUIDE-template.md          │   AI 协作指南（防幻觉）
│   ├── ONBOARDING-template.md        │   新人引导模板
│   ├── PROJECT-MEMORY-template.md    │   项目记忆模板
│   ├── SESSION_DRIVER-template.md    │   会话驱动模板
│   ├── pre-commit-hook               │   P0 阻止 + P1 警告
│   ├── pre-push-hook                 │   推送前审查提醒
│   ├── gitignore                     │   推荐 .gitignore
│   └── env-example.env               │   环境变量模板
│
├── docs/                              ← 📚 文档
│   ├── BLUEPRINT-v2.md               │   v2 开发蓝图（14 章 + 附录）
│   ├── getting-started.md            │   详细入门指南
│   └── newbie-pitfalls.md            │   新手避坑手册
│
└── .github/workflows/                ← ⚡ GitHub Actions
    └── auto-evolve.yml               │   每周自动搜索社区方案
```
## 🔧 核心 Skill 说明

### 1️⃣ context-map — 代码地图（最重要）

**解决什么问题**：新手最大的隐性成本不是写代码，而是每次重新开会话后 AI 不记得之前做了什么。

**做什么**：
- 扫描整个项目，生成结构化的"代码地图"
- 记录每个模块的职责、依赖关系、当前状态
- 下次开会话时 AI 加载代码地图 → 瞬间恢复全部上下文
- 每次会话结束自动更新

**什么时候用**：
- 每次会话结束时自动触发（通过 hook）
- 手动调用：`/skill context-map` 或在对话中说"生成代码地图"

### 2️⃣ fullstack-scaffold — 全栈脚手架

**做什么**：一句话描述需求 → 生成完整的前后端项目骨架。

**支持的技术栈组合**（默认选型如下（均可替换））：

| 后端 | 前端 | 数据库 | 部署 |
|------|------|--------|------|
| Node.js + Hono | React + Tailwind + shadcn/ui | PostgreSQL (Supabase) | Vercel |
| Node.js + Hono | Vue 3 + Tailwind | SQLite (Turso) | Cloudflare |
| Python + FastAPI | React + Next.js | PostgreSQL | Railway |
| Bun + Elysia | SvelteKit | Turso | Deno Deploy |

**为什么选这些作为默认解**：详见 `docs/getting-started.md` 技术选型章节。

### 3️⃣ code-review — 代码审查

**做什么**：对当前改动做 P0-P3 分级审查。

- **[P0] 严重**：安全漏洞、逻辑错误、数据丢失风险 → 必须修
- **[P1] 重要**：性能问题、错误处理缺失 → 强烈建议修
- **[P2] 一般**：代码质量、可读性 → 建议修
- **[P3] 改进**：最佳实践、未来优化 → 可选

### 4️⃣ 其他 Skill

| Skill | 用途 | 触发方式 |
|-------|------|---------|
| commit-helper | 分析改动生成 Conventional Commits | `/skill commit-helper` |
| deploy-check | 部署前检查环境变量、依赖、构建 | `/skill deploy-check` |
| troubleshoot | 根据错误信息自动排查原因 | `/skill troubleshoot <错误信息>` |
| api-designer | 设计 API 接口并生成文档 | `/skill api-designer` |

## 🔌 推荐 MCP 配置

从后端到前端，按需启用：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": { "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}" }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "--allowedPaths", "${PROJECT_ROOT}"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

完整配置见 `configs/mcp-servers.json`，包含每个 MCP 的用途说明和可选替代方案。

## 🔄 自动进化机制

**不是堆砌，是精选替换。**

每周自动执行：
1. 搜索 GitHub 上新出现的优秀 MCP Server / Skill / 工具配置
2. 与现有方案对比（质量、活跃度、社区反馈）
3. 如果更好 → 替换现有配置，记录变更理由
4. 提交 PR 通知你审查

手动触发：`bash scripts/auto-evolve.sh`

## 🛡️ 新手防护网

我们预埋了以下保护机制：

- ✅ **编辑门控**：默认 auto 模式（5秒撤销窗口），防止误操作
- ✅ **权限白名单**：只允许安全的 shell 命令，危险操作需要确认
- ✅ **自动格式化**：每次保存文件后自动 format/lint
- ✅ **部署检查**：部署前自动检查环境变量、依赖完整性、构建状态
- ✅ **常见问题库**：`troubleshoot.md` 覆盖 50+ 新手高频问题

## 📊 设计原则

1. **决策最小化**：所有选项都有默认值，新手不需要做选择
2. **渐进式复杂度**：从最简单的路径开始，需要时再深入
3. **失败友好**：每一步都有回退方案和错误提示
4. **上下文持久化**：代码地图 + 项目记忆 = 无缝续接
5. **工具无关**：不绑定任何特定工具或模型提供商
6. **进化而非膨胀**：发现更好的就替换，不叠加

## 🤝 贡献指南

欢迎贡献！特别是：
- 新的 Skill（解决你遇到的重复性问题）
- 更优的 MCP 配置方案
- 新手避坑案例（你踩过的坑）
- 技术栈模板（其他语言/框架组合）

详见 [getting-started.md](docs/getting-started.md)

## 📄 License

MIT License - 自由使用、修改、分发。

---

<p align="center">
<strong>让一个人也能像团队一样高效开发。</strong><br>
Made with ❤️ for Solo Developers
</p>
