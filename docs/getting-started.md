# 🚀 详细入门指南 — Solo Dev Autopilot

> 从零到自动驾驶的完整路径。按顺序阅读，每一步都有明确的操作指令。

## ⚡ 三步开始（30 秒看完）

```bash
# ① 克隆 + 一键安装（选配置模式：toy/team/production）
bash scripts/setup.sh          # macOS/Linux/Git Bash
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1   # Windows

# ② 在 Claude Code 里装方法论底座
/plugin install superpowers@claude-plugins-official

# ③ 开始开发（AI 自动加载记忆 + 代码地图）
claude
# 第一句话：读取 PROJECT-MEMORY.md 和 CODEMAP.md，帮我生成代码地图
```

> 三步的含义：**① 装好环境** → **② 接上方法论** → **③ 交给 autopilot**。
> 之后的日常开发（写代码→测试→审查→提交→部署检查）全部由 21 个 Skill 自动推进，
> 你只需在关键节点（合并、部署）做人工确认。

## 目录

1. [前置要求](#1-前置要求)
2. [安装步骤](#2-安装步骤)
3. [第一次启动](#3-第一次启动)
4. [技术选型说明](#4-技术选型说明)
5. [日常使用流程](#5-日常使用流程)
6. [进阶配置](#6-进阶配置)

---

## 1. 前置要求

### 必须有

| 工具 | 最低版本 | 用途 | 安装方式 |
|------|---------|------|---------|
| **Git** | 2.x | 版本控制 | [git-scm.com](https://git-scm.com) |
| **Node.js** | ≥20 或 **Bun** | 运行时 + 包管理 | [nodejs.org](https://nodejs.org) / [bun.sh](https://bun.sh) |
| **AI 编程工具**（任选一个） | 最新版 | 与 AI 协作开发 | 见下方 |

### AI 编程工具选择指南

| 工具 | 适合场景 | 安装方式 |
|------|---------|---------|
| **Claude Code** | 终端用户、深度编程任务 | `npm install -g @anthropic-ai/claude-code` |
| **Cursor** | VS Code 用户、IDE 偏好 | [cursor.com](https://cursor.com) |
| **Cline** | VS Code 免费替代品 | VS Code 扩展市场搜索 "Cline" |
| **Reasonix** | DeepSeek 用户、成本敏感 | `npm install -g reasonix` |
| **Windsurf** | Codeium 用户 | [windsurf.com](https://windsurf.com) |

> 💡 **新手推荐**: 如果不知道选哪个，先用 **Claude Code**（最成熟）或 **Cursor**（最易上手）。

### 可选但推荐

| 工具 | 用途 | 为什么推荐 |
|------|------|-----------|
| **pnpm** | 包管理器 | 比 npm 快 2-3x，节省磁盘，严格依赖管理 |
| **GitHub 账号** | 代码托管 + MCP 操作 | 免费，必备 |

---

## 2. 安装步骤

### Step 1: 克隆仓库

```bash
git clone https://github.com/YuemingHub/solo-dev-autopilot.git
cd solo-dev-autopilot
```

### Step 2: 一键安装

> **Windows 用户注意**：如果你用的是 Windows，请运行 PowerShell 版本：
> ```powershell
> powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
> ```
> 如果你安装了 Git for Windows（自带 Git Bash），也可以运行 bash 版本：
> ```bash
> bash scripts/setup.sh
> ```

```bash
# macOS / Linux / Git Bash
bash scripts/setup.sh
```

```bash
# 自动检测环境并配置所有文件
bash scripts/setup.sh
```

这个脚本会自动：
1. ✅ 检测你的操作系统和已安装的工具
2. ✅ 复制 Skill 文件到你的项目目录
3. ✅ 为各工具创建符号链接或副本
4. ✅ 安装模板文件（.gitignore、.env.example、PROJECT-MEMORY.md）
5. ✅ 引导你配置 MCP 服务器
6. ✅ 设置 Git Hooks
7. ✅ 初始化 Git 仓库

### Step 3: 手动安装（如果脚本失败）

如果 `setup.sh` 因环境问题无法运行，手动执行以下操作：

#### 3a. 复制 Skill 文件（官方文件夹式 SKILL.md）

```bash
# 复制到目标项目的 .claude/skills/（Claude Code 原生识别）
mkdir -p your-project/.claude/skills/
cp -r .claude/skills/* your-project/.claude/skills/

# 其他工具（社区适配）：见 docs/tool-setup.md 对应小节
# Cursor  → .cursor/rules/（需手动转换）
# Cline   → .clinerules/
# Reasonix → ~/.reasonix/skills/
# Windsurf → .windsurf/rules/
```

> ⚠️ v1 的平铺 `skills/*.md` 已废弃——Claude Code 只认
> `.claude/skills/<name>/SKILL.md` 文件夹格式。

#### 3b. 复制模板文件

```bash
cp templates/gitignore your-project/.gitignore
cp templates/env-example.env your-project/.env.example
cp templates/PROJECT-MEMORY-template.md your-project/PROJECT-MEMORY.md
```

#### 3c. 配置 MCP

参考 `configs/mcp-servers.json` 和 `configs/tool-presets/` 下的对应文件。

---

## 3. 第一次启动

### 3.1 编辑项目记忆文件

打开 `PROJECT-MEMORY.md`，填写你的项目信息：

```markdown
## 项目概览
名称：我的第一个全栈应用
一句话描述：一个用户可以发布文章和评论的博客平台
当前阶段：mvp

## 技术栈
后端：Bun + Hono
前端：React + Vite + Tailwind CSS
数据库：PostgreSQL (Supabase)
```

> ⚠️ 这一步很重要！AI 每次开会话都会读取这个文件来理解你的项目。

### 3.2 配置环境变量

```bash
# 复制模板为实际配置
cp .env.example .env

# 编辑填入实际值
nano .env  # 或用任何编辑器
```

至少需要配置：
- `DATABASE_URL` — 数据库连接字符串
- `GITHUB_TOKEN` — GitHub Personal Access Token（用于 MCP）

### 3.3 启动 AI 编程工具

根据你选择的工具：

```bash
# Claude Code
claude

# Reasonix
reasonix code

# Cursor / Cline
# 在 IDE 中打开项目即可
```

### 3.4 第一句话

启动后，对 AI 说：

```
读取 PROJECT-MEMORY.md 和 CODEMAP.md，了解这个项目。
然后帮我生成代码地图。
```

这会让 AI 瞬间恢复全部上下文。

---

## 4. 技术选型说明

为什么我们选择了这些"最优解"？每个选择都有明确理由。

### 后端：Bun + Hono

| 选择 | 理由 |
|------|------|
| **Bun 而非 Node.js** | 快 3x，内置 TypeScript 支持，内置包管理器，内置 test runner |
| **Hono 而非 Express** | 更轻量（14KB vs 700KB+），TypeScript-first，边缘兼容（Cloudflare Workers/Deno），更快的路由匹配 |
| **Drizzle ORM 而非 Prisma** | 类型安全但不生成臃肿的 runtime，SQL-like API 学习成本低，轻量（<10KB） |

### 前端：React + Vite + Tailwind + shadcn/ui

| 选择 | 理由 |
|------|------|
| **React** | 生态最大、就业最广、学习资源最多、社区活跃 |
| **Vite** | 开发服务器启动 <100ms，HMR 毫秒级，构建用 Rollup 生产优化 |
| **Tailwind CSS v4** | 不离开 HTML/JSX 写样式，原子化避免样式冲突，CSS-first 配置 |
| **shadcn/ui** | 不是组件库而是可复制的组件代码，完全可定制，不引入额外依赖，Tree-shakable |

### 数据库：PostgreSQL (Supabase)

| 选择 | 理由 |
|------|------|
| **PostgreSQL** | 最强大的开源关系数据库，JSON 支持，全文搜索，地理数据类型 |
| **Supabase** | PostgreSQL 的 Firebase 替代品，免费额度够用，自带 Auth + Storage + Realtime + Edge Functions |
| **备选 Turso** | 边缘原生 SQLite，全球分布，免费额度大，适合读多写少的应用 |

### 部署：Vercel + Supabase

| 选择 | 理由 |
|------|------|
| **Vercel** | 零配置部署，自动 CI/CD，免费额度充足，边缘网络快 |
| **Supabase 托管** | 免费层够 MVP 使用，按需付费扩展简单 |

### 包管理器：pnpm

| 选择 | 理由 |
|------|------|
| **pnpm** | 节省磁盘空间（内容寻址存储），安装速度快，严格依赖管理（避免 phantom dependencies） |

---

## 5. 日常使用流程

### 一个典型的开发会话

```
1. 启动工具 → AI 自动加载 PROJECT-MEMORY.md
2. 你说："加载 CODEMAP.md"
3. AI 恢复上下文 → 你说需求
4. AI 写代码 → review 模式预览 → 你确认
5. 你说："review 一下" → code-review skill 运行
6. 你说："提交" → commit-helper 生成 commit message
7. 你确认 → git commit
8. 结束会话 → post-session hook 自动触发
9. 下次回来 → 回到第 1 步
```

### 常用命令速查表

| 你想做什么 | 对 AI 说 | 触发的 Skill |
|-----------|---------|-------------|
| 新建项目 | "帮我创建一个 xxx 项目" | fullstack-scaffold |
| 了解项目现状 | "生成代码地图" | context-map |
| 审查代码 | "review 一下" | code-review |
| 提交代码 | "帮我提交" | commit-helper |
| 能否部署 | "能部署了吗" | deploy-gate |
| 排查错误 | "报错了：[粘贴错误]" | troubleshoot |
| 设计接口 | "设计 xxx 的 API" | api-designer |
| 记住偏好 | "记住我们用 pnpm" | 内置 memory |

---

## 6. 进阶配置

### 6.1 自定义 Skill（官方 SKILL.md 格式）

在 `.claude/skills/` 下新建文件夹 + SKILL.md（Claude Code 自动识别）：

```markdown
---
name: my-custom-skill
description: >
  我的自定义技能：一句话描述用途 + 触发时机。
  当用户说"xxx"时触发。
license: MIT
---

# My Custom Skill

## 目标
...

## 执行步骤
...
```

```bash
# 文件位置：
# .claude/skills/my-custom-skill/SKILL.md
```

然后在对话中触发：`/skill my-custom-skill` 或说触发词。

> ⚠️ 官方格式只有 name / description / license 三个字段（无 runAs/tools 等 v1 字段）。
> description 写清楚触发词，AI 才能自动识别何时调用。

### 6.2 添加更多 MCP Server

编辑 `configs/mcp-servers.json` 或工具对应的配置文件：

```json
{
  "mcpServers": {
    "my-new-server": {
      "command": "npx",
      "args": ["-y", "@some/mcp-server"],
      "env": { "API_KEY": "${YOUR_KEY}" }
    }
  }
}
```

### 6.3 配置自动进化

编辑 `.github/workflows/auto-evolve.yml` 中的搜索条件，或直接运行：

```bash
bash scripts/auto-evolve.sh          # 正常模式
bash scripts/auto-evolve.sh --dry-run # 仅查看不修改
```

### 6.4 多项目管理

如果你同时开发多个项目：

```bash
# 方案 A：每个项目独立一份
cd project-a && bash /path/to/solo-dev-autopilot/scripts/setup.sh
cd project-b && bash /path/to/solo-dev-autopilot/scripts/setup.sh

# 方案 B：全局共享 Skill（推荐，软链到 Claude Code 用户目录）
ln -s /path/to/solo-dev-autopilot/.claude/skills ~/.claude/skills
```

---

## 下一步

- 📖 阅读 [新手避坑手册](newbie-pitfalls.md)
- 🔧 查看 `configs/mcp-servers.json` 了解 MCP 配置
- 🤝 贡献你的 Skill 到仓库
