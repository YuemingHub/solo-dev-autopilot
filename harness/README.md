# Harness 层（原 agent-tool · 新手自动驾驶环境合集）

> 依据《深入理解 AI Agent》(李博杰,github.com/bojieli/ai-agent-book):**Agent = 模型(大脑) + 上下文(眼睛) + 工具(手脚)**,竞争力在模型之外的 Harness 工程。
> 本层让新手打开任何项目,由 Agent 自动完成「侦测 → 搭建 → 开发 → 验证 → 记忆」闭环,零手工配置。
> **2026-08-05 已并入 solo-dev-autopilot 三合一仓库**,成为统一架构的第 ② 层（见根目录 `AGENTS.md`）。

## 合并后的位置

| 原 agent-tool | 合并后位置 | 说明 |
| --- | --- | --- |
| `skills/*.md`（7 个） | `.claude/skills/<name>/SKILL.md` | 升级为官方 SKILL.md 格式（含 license 字段），与 13 个交付 Skill 并列,共 **20 个**；平铺兼容层 `skills/*.md` 由 `scripts/sync-skills.py` 单向同步 |
| `agents/*.json`（2 个） | `harness/agents/` | env-agent / dev-agent,供支持自定义 agent 的工具使用 |
| `AGENTS.md` | `harness/AGENTS.md` | harness 层全局触发规则（ohmyagent 等工具的全局安装用） |
| `docs/book/` | `references/book/` | 书解析 Markdown + 中文 PDF（资料库） |
| `tools/` | `harness/tools/` | validate.py（结构校验）、e2e_demo.py（端到端演示） |
| `install.ps1` | `harness/install.ps1` | 重写为相对路径版,一键同步到 ohmyagent 全局配置目录 |

## 7 个 Harness Skill

| Skill | 职责 |
| --- | --- |
| env-detect | 侦测技术栈与工具链 → 写 `.agentenv.json` |
| env-setup | 补运行时/装依赖/.env/lint/git/AGENTS.md → 冒烟 |
| project-scaffold | 从零建项目(6 套模板) |
| dev-loop | 质量门禁+自动修复+熔断(自动驾驶核心) |
| task-memory | 跨会话项目记忆(`.agent-memory/`) |
| harness-guard | 危险操作/密钥/覆盖护栏 |
| book-experiments | 克隆书仓库、按章装依赖、跑 94 个实验 |

## 怎么安装 / 生效（ohmyagent 用户）

1. 在仓库根目录运行 `powershell -ExecutionPolicy Bypass -File harness\install.ps1`：把平铺层 `skills/*.md`、`harness/agents/*.json`、`harness/AGENTS.md` 同步到全局配置目录 `%APPDATA%\com.chaitin.baizhi.monkeycode\ohmyagent\`
2. **新开一个 ohmyagent 会话**——skill 扫描发生在会话启动时,新会话自动加载
3. 验证:对话里让 Agent「列出可用 skill」,或看日志 `[skills] scanned 7 skills`

Claude Code / Codex 用户无需此步：20 个 Skill 以官方格式直接在 `.claude/skills/` 被加载。

## 怎么用(新手视角,全自动)

| 你说 | Agent 自动做什么 |
| --- | --- |
| 「帮我看看这个项目」 | env-detect:判定技术栈、检查工具链、写 .agentenv.json |
| 「搭好环境」/ 打开缺环境项目 | env-setup:装运行时→装依赖→.env→lint→git→冒烟验证 |
| 「帮我新建一个 Python 项目」 | project-scaffold:生成骨架→env-setup→测试通过 |
| 「加个功能/修个 bug」 | dev-loop:改完自动 format→lint→typecheck→build→test,失败自修 |
| 新会话继续开发 | task-memory:自动加载项目记忆,不用重新摸索 |
| 「我想跑这本书的实验」 | book-experiments:克隆仓库、`uv sync --extra chN`、跑通 |

## 自动驾驶程度(已确认的设定)

- 低风险全自动(装依赖、配置、构建测试、自动修复)
- 高危先询问(删除、覆盖未读文件、全局安装、force push)
- 运行时缺失允许 winget 自动安装;语言覆盖 Python/Node/Go/Rust/Java 全栈

## 已验证(2026-07-31,Windows 真机 · agent-tool 原仓库时期)

- `[skills] scanned 7 skills`、2 个 agent 进注册表(registry: 10 definitions)
- 全局 AGENTS.md 规则功能实测生效(注入规则,模型遵守)
- 端到端:脚手架→uv sync→pytest 通过→ruff 报错→`ruff --fix` 自动修复→冒烟 `Hello, Bob!`
- 真实踩坑已沉淀:typer+click 在 Python 3.12 上子命令失效 → 脚手架默认用标准库 argparse

## 注意事项

- ohmyagent 只扫描**单文件 .md skill**(带 YAML frontmatter),不支持目录+SKILL.md 的 Claude Code 格式(已实测确认)——所以 ohmyagent 安装用平铺层 `skills/*.md`
- 修改 skill 内容只改 `.claude/skills/`,再 `python scripts/sync-skills.py` 重新生成平铺层
- `.env` 只存占位符,真实密钥永不入库、不入记忆
