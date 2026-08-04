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

v2 优先 **Claude Code 全适配**（官方 SKILL.md + 插件市场原生支持）与 **Codex 全适配**（AGENTS.md + `.codex/skills/`，见 [docs/codex-setup.md](docs/codex-setup.md)），其他工具标注"社区适配中"：

- **Claude Code** ✅ 全适配 (`.claude/skills/` + 插件市场注册)
- **Codex** ✅ 全适配（AGENTS.md + `.codex/skills/`，[docs/codex-setup.md](docs/codex-setup.md)）
- **Cursor** 🟡 社区适配中 (`.cursor/rules/`)
- **Cline** 🟡 社区适配中 (`.cline/`)
- **Reasonix** 🟡 社区适配中 (`.reasonix/skills/`)
- **Windsurf** 🟡 社区适配中 (`.windsurf/rules/`)
- **任何支持 MCP 协议的 IDE / 本地工作台**

> 与 superpowers 的关系：**硬依赖 + 中文增强层**——superpowers 是方法论底座（brainstorm → plan → TDD → review → finish），我们的 Skill 是它的中文新手场景适配层。安装引导见 `onboarding` Skill 和 `scripts/setup.sh`。

## ⚡ 三步开始

```bash
# 1. 克隆仓库
git clone https://github.com/YuemingHub/solo-dev-autopilot.git
cd solo-dev-autopilot

# 2. 运行一键安装（检测环境、安装 Skill、引导安装 superpowers）
# macOS / Linux / Git Bash:
bash scripts/setup.sh

# Windows PowerShell:
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1

# 3. 在 Claude Code 里安装上游方法论（脚本会引导你，或手动执行）：
#    /plugin install superpowers@claude-plugins-official
#    Codex 用户跳过本步，按 docs/codex-setup.md 接入；三仓库 9 步闭环见 docs/closed-loop.md

# 4. 把这个目录作为你的项目根目录开始开发
# 或者把 .claude/skills/ 和 templates/ 复制到已有项目中
```

> 🔗 **依赖声明**：本仓库站在三个开源项目之上，不重复造轮子——
> [anthropics/skills](https://github.com/anthropics/skills)（官方 SKILL.md 标准）、
> [obra/superpowers](https://github.com/obra/superpowers)（开发方法论底座）、
> [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)（MCP 服务器清单）。

## 🏗️ 架构图

```
┌──────────────────────────────────────────────────────────────────────┐
│                          你的项目 (Your Project)                     │
│   CODEMAP.md · PROJECT-MEMORY.md · SESSION_DRIVER.md · .env.example   │
│   pre-commit / pre-push hooks · CI · 部署目标                        │
└───────────────┬──────────────────────────────────┬──────────────────┘
                │ 注入上下文（记忆/代码地图）        │ 自动化执行（质量门）
┌───────────────▼──────────────────┐   ┌───────────▼──────────────────┐
│      AI 编程工具（任选其一）       │   │     Git Hooks + CI           │
│  Claude Code · Codex · Cursor    │   │  pre-commit：P0 阻止提交      │
│  Cline · Reasonix · Windsurf     │   │  pre-push：推送前审查提醒     │
└───────────────┬──────────────────┘   │  GitHub Actions：lint→test    │
                │ 读取                    │  →build→审计→密钥扫描        │
                │                       └──────────────────────────────┘
┌───────────────▼─────────────────────────────────────────────────────┐
│              🦐 Solo Dev Autopilot 配置层（本仓库）                   │
│  ├─ 13 个 SKILL.md —— 中文新手场景增强（官方格式）                    │
│  ├─ configs/permissions.json —— 三级危险度权限模型（唯一事实源）       │
│  ├─ configs/modes/ —— toy / team / production 三档配置               │
│  ├─ configs/tool-presets/ —— 各工具适配（Claude 全适配，其他社区适配）│
│  └─ configs/mcp-servers.json —— MCP 服务器推荐                       │
└───────────────┬─────────────────────────────────────────────────────┘
                │ 基于（不重复造轮子）
┌───────────────▼─────────────────────────────────────────────────────┐
│                           上游开源底座                                │
│  anthropics/skills（SKILL.md 标准）· obra/superpowers（开发方法论）    │
│  punkpeye/awesome-mcp-servers（MCP 清单）                             │
└──────────────────────────────────────────────────────────────────────┘
```

**读法**：你的项目在最上层（产物），AI 工具在中间（执行者），本仓库是配置层（规则与技能），
最下面是上游底座（我们不重造的部分）。Solo 开发者只需关心最上层——其余由 autopilot 自动推进。

## 📂 仓库结构

```
solo-dev-autopilot/
├── README.md
├── LICENSE                            ← MIT
├── CHANGELOG-v2.md                    ← v2 更新日志
├── BOOTSTRAP-PROMPT.md                ← 首次启动引导
│
├── .claude/                           ← 🧠 Claude Code 原生适配（v2 新增）
│   ├── settings.json                  │   三级危险度权限模型（auto-allow / ask / deny）
│   ├── plugin/marketplace.json        │   插件市场注册（v2 新增）
│   └── skills/                        │   官方 SKILL.md 格式技能（Claude Code 自动识别）
│       ├── api-designer/SKILL.md      │   API 接口设计
│       ├── ci-helper/SKILL.md         │   CI 配置与排障（v2.1 新增）
│       ├── code-review/SKILL.md       │   P0-P3 分级代码审查
│       ├── commit-helper/SKILL.md     │   智能 Commit 信息
│       ├── context-map/SKILL.md       │   代码地图（会话恢复核心）
│       ├── deploy-gate/SKILL.md       │   部署门禁（人工确认红线）
│       ├── fullstack-scaffold/SKILL.md│   全栈脚手架生成
│       ├── observability/SKILL.md     │   日志/Sentry/健康检查（v2.1 新增）
│       ├── onboarding/SKILL.md        │   首次使用引导（装 superpowers）
│       ├── production-preflight/SKILL.md │ 上线前预检（v2.1 新增）
│       ├── task-planner/SKILL.md      │   目标拆解与防漂移
│       ├── test-runner/SKILL.md       │   测试闭环 + 覆盖率（v2.1 新增）
│       └── troubleshoot/SKILL.md      │   新手问题排查
│
├── skills/                            ← 🔗 社区工具兼容层（平铺 .md，由 sync-skills.py 从 .claude/skills/ 同步）
│
├── configs/                           ← ⚙️ 各工具的预设配置
│   ├── permissions.json               │   三级危险度权限模型（唯一事实源，v2.1 新增）
│   ├── modes/                         │   三档配置：toy / team / production（v2.1 新增）
│   ├── mcp-servers.json              │   MCP 服务器推荐配置
│   └── tool-presets/                  │   各工具适配配置
│       ├── claude-code.json          │   三级权限 + MCP + skillsPath
│       ├── cursor.json               │
│       ├── cline.json                │
│       ├── reasonix.json             │   三级权限 + hooks
│       └── codex.json                │   Codex 适配（AGENTS.md + 沙箱映射，v2.4 新增）
│
├── scripts/                           ← 🔧 自动化脚本
│   ├── setup.sh / setup.ps1          │   一键安装（macOS/Linux/Windows + 模式选择）
│   ├── post-session.sh / post-session.ps1 │ 会话结束自动化（v2.1 新增 Windows 版）
│   ├── install-git-hooks.sh / .ps1   │   Git Hooks 安装（带备份）
│   ├── sync-skills.py                │   Skill 兼容层同步（v2.3.3 新增）
│   └── auto-evolve.sh                │   社区方案搜索
│
├── templates/                         ← 📝 项目模板
│   ├── AI-GUIDE-template.md          │   AI 协作指南（防幻觉）
│   ├── ONBOARDING-template.md        │   新人引导模板
│   ├── PROJECT-MEMORY-template.md    │   项目记忆模板
│   ├── SESSION_DRIVER-template.md    │   会话驱动模板
│   ├── pre-commit-hook               │   P0 检查（严格度随模式调整，v2.1 优化）
│   ├── pre-push-hook                 │   推送前审查提醒
│   ├── gitignore                     │   推荐 .gitignore
│   └── env-example.env               │   环境变量模板
│
├── docs/                              ← 📚 文档
│   ├── BLUEPRINT-v2.md               │   v2 开发蓝图（14 章 + 附录）
│   ├── getting-started.md            │   详细入门指南（三步开始）
│   ├── tool-setup.md                 │   各 AI 工具安装引导（v2.3 新增）
│   ├── codex-setup.md                │   Codex 接入指南（v2.4 新增）
│   ├── closed-loop.md                │   三仓库联动 9 步闭环（v2.4 新增）
│   ├── scoring.md                    │   评分维度表 8 维加权（v2.3 新增）
│   ├── verification.md              │   验证记录：所有实测证据可复现（v2.3.2 新增）
│   ├── EVOLVE_CHANGELOG.md          │   自动进化变更记录（v2.3.3 补齐）
│   ├── newbie-pitfalls.md            │   新手避坑手册
│   ├── production-checklist.md       │   生产上线清单（v2.1 新增）
│   └── autopilot-boundaries.md       │   AI 边界原则（v2.1 新增）
│
└── .github/workflows/                ← ⚡ GitHub Actions
    ├── ci.yml                        │   仓库自检：JSON/SKILL.md/shell（scripts/ci-self-check.sh）
    └── auto-evolve.yml               │   每周自动搜索社区方案
```
> 你的项目的 CI 模板见 `templates/ci-node.yml`（lint→test→build→审计→密钥扫描）。
## 🔧 核心 Skill 说明

> 💡 第一次用？先让 AI 触发 `onboarding`（或说"怎么开始"），它会引导你安装 superpowers 并完成首次设置。

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
| onboarding | 首次使用引导（装 superpowers） | `/skill onboarding` |
| deploy-gate | 部署门禁：检查 + 人工确认红线 | `/skill deploy-gate` |
| test-runner | 测试闭环：跑单测/集成/E2E + 覆盖率 | `/skill test-runner` |
| ci-helper | CI 配置生成与失败诊断 | `/skill ci-helper` |
| observability | 结构化日志 + Sentry + 健康检查 + 告警 | `/skill observability` |
| production-preflight | 上线前预检：覆盖率/CI/权限/可观测性/密钥/回滚 | `/skill production-preflight` |
| troubleshoot | 根据错误信息自动排查原因 | `/skill troubleshoot <错误信息>` |
| api-designer | 设计 API 接口并生成文档 | `/skill api-designer` |

## ⚙️ 配置模式（toy / team / production）

安装时（`setup.sh` / `setup.ps1`）选择模式，写入 `.autopilot-mode`，决定权限严格度与 hook 行为：

| 档位 | 权限 | hook 严格度 | 记忆策略 | 适合谁 |
|------|------|-----------|---------|--------|
| toy | 宽松白名单，几乎不确认 | pre-commit: 仅警告 | 全量加载 | 第一次用 AI 编程的人 |
| team | 三级危险度分级 | pre-commit: P0 阻止提交 | 摘要 + 按需加载 | 小团队协作 |
| production | 分级 + 生产库二次确认 | P0 阻止 + pre-push 全量检查 | 摘要 + 裁剪 + 归档 | 上线项目 |

切换模式：`echo 'production' > .autopilot-mode`（hook 下次运行时生效）。
完整权限定义见 `configs/permissions.json` 与 `configs/modes/`。

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
- ✅ **三级危险度权限**：safe 自动放行 / ask 确认 / danger 拒绝+确认（`configs/permissions.json`）
- ✅ **自动格式化**：每次保存文件后自动 format/lint
- ✅ **部署门禁**：部署前自动检查（环境变量/依赖/构建/CI/密钥扫描）+ **人工确认红线**（生产部署不可自动跳过）
- ✅ **上线预检**：production-preflight 检查覆盖率/CI/权限/可观测性/密钥/回滚（`docs/production-checklist.md`）
- ✅ **AI 边界明确**：开发可自动、部署必人工（`docs/autopilot-boundaries.md`）
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

详见 [getting-started.md](docs/getting-started.md)、[codex-setup.md](docs/codex-setup.md)、[closed-loop.md](docs/closed-loop.md)

## 📄 License

MIT License - 自由使用、修改、分发。

---

<p align="center">
<strong>让一个人也能像团队一样高效开发。</strong><br>
Made with ❤️ for Solo Developers
</p>
