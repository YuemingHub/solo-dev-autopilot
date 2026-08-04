# 各 AI 工具安装引导（Tool Setup Guide）

> 定位：按工具给出安装 Solo Dev Autopilot 的完整步骤。
> 兼容性声明：**Claude Code 全适配**（官方 SKILL.md + 插件市场原生支持），
> 其余工具为**社区适配中**（能读配置和规则，但 Skill 触发方式可能不同）。

---

## 兼容性总览

| 工具 | 状态 | Skill 支持 | 配置文件 | 安装方式 |
|------|------|-----------|---------|---------|
| **Claude Code** | ✅ 全适配 | 官方 SKILL.md 自动识别 | `.claude/settings.json` | 推荐 |
| **Cursor** | 🟡 社区适配中 | 通过 rules 引用 | `.cursor/rules/` | 可用 |
| **Cline** | 🟡 社区适配中 | 通过规则文件引用 | `.cline/` | 可用 |
| **Reasonix** | 🟡 社区适配中 | 通过 skills 目录引用 | `.reasonix/skills/` | 可用 |
| **Windsurf** | 🟡 社区适配中 | 通过 rules 引用 | `.windsurf/rules/` | 可用 |

> 判断标准：能否**原生自动加载** 20 个 SKILL.md。Claude Code 官方格式全兼容，
> 其他工具需要手动把 skill 内容转为自己的规则格式（转换器见各工具小节）。

---

## 0. 通用准备（所有工具）

```bash
# 1. 克隆仓库
git clone https://github.com/YuemingHub/solo-dev-autopilot.git
cd solo-dev-autopilot

# 2. 一键安装（检测环境、装 Skill、引导装 superpowers）
# macOS / Linux / Git Bash:
bash scripts/setup.sh
# Windows PowerShell:
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

安装时选择配置模式（toy / team / production），写入 `.autopilot-mode`。

---

## 1. Claude Code（✅ 全适配，推荐）

### 安装

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 进入项目后确认 Skill 被识别
claude
# 输入 /skill 应看到 20 个 Skill（api-designer ~ troubleshoot + env-detect ~ book-experiments）
```

### 权限合并（关键）

`.claude/settings.json` 已随仓库带上三级权限模型，开箱即用。
如果你之前有个人配置，合并（**不要覆盖**）：

```bash
# 查看现有配置
cat ~/.claude/settings.json
# 将本项目 configs/tool-presets/claude-code.json 的 permissions 合并进去
```

### 插件市场注册（可选，一键安装）

```bash
# 在 Claude Code 中执行
/plugin marketplace add YuemingHub/solo-dev-autopilot
/plugin install solo-dev-autopilot@YuemingHub/solo-dev-autopilot
```

### 安装 superpowers（方法论底座）

```bash
# 在 Claude Code 中执行（官方市场）
/plugin install superpowers@claude-plugins-official
# 或 SP 市场
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### 验证

```bash
# 1. /skill 能看到 20 个 Skill
# 2. 说"生成代码地图" → context-map 运行
# 3. 说"能部署了吗" → deploy-gate 输出部署确认单（人工确认红线）
```

---

## 1.5 Codex（✅ 全适配）

见 [codex-setup.md](codex-setup.md)：用 AGENTS.md 指令承载三级权限模型，`.codex/skills/` 加载 20 个 Skill；无需插件市场，不强制安装 superpowers（由 20 个 Skill + 9 步闭环承担方法论）。

---

## 2. Cursor（🟡 社区适配中）

### 安装

1. 下载 [cursor.com](https://cursor.com)
2. 用 Cursor 打开 `solo-dev-autopilot` 目录
3. 手动把 skill 内容转为 rules：`Settings → Rules → User Rules` 粘贴
   `skills/` 下的内容（或参考 `.cursor/rules/` 的转换示例）

### 注意

- Cursor 的 Rules 是**全局生效**的，不适合塞 20 个完整 Skill
- 建议只转 2-3 个核心：context-map（代码地图）、troubleshoot（排错）、commit-helper（提交）
- 权限模型（permissions.json）在 Cursor 中需手动在 Settings → Security 配置

---

## 3. Cline（🟡 社区适配中）

### 安装

1. VS Code 扩展市场搜索 "Cline" 安装
2. 在 Cline 设置中启用自定义指令，粘贴 `AI-GUIDE.md` 的关键内容
3. 手动把需要的 Skill 转成 Cline 的 `.clinerules/` 格式

### 注意

- Cline 偏重"工具调用"，Skill 的对话式引导能力弱于 Claude Code
- 建议核心使用 context-map + troubleshoot
- MCP 配置：`configs/mcp-servers.json` 可直接用

---

## 4. Reasonix（🟡 社区适配中）

### 安装

```bash
npm install -g reasonix
cd solo-dev-autopilot
reasonix code
```

### Skill 引用

Reasonix 支持 `skills/` 目录引用（v1 平铺格式），把需要的 `.md` 复制过去：

```bash
mkdir -p ~/.reasonix/skills/
cp .claude/skills/*/SKILL.md ~/.reasonix/skills/
```

### 注意

- Reasonix 的 Skill 触发用 `/skill <name>`（与 Claude Code 类似）
- 权限模型在 `configs/tool-presets/reasonix.json`（hooks + 权限）

---

## 5. Windsurf（🟡 社区适配中）

### 安装

1. 下载 [windsurf.com](https://windsurf.com)
2. 打开项目目录
3. 把 skill 核心内容转成 `.windsurf/rules/` 规则文件

### 注意

- Windsurf 的 Cascade 是对话式，规则文件支持有限
- 建议：直接用 AI-GUIDE.md 作为系统提示词的一部分

---

## 6. 迁移到已有项目（不克隆本仓库）

如果你已有项目，只需复制关键部分：

```bash
# 最小可用集（推荐）
cp -r .claude/ your-project/          # Claude Code 全适配
cp -r configs/permissions.json your-project/.claude/
cp -r templates/AI-GUIDE-template.md your-project/AI-GUIDE.md
cp -r templates/PROJECT-MEMORY-template.md your-project/PROJECT-MEMORY.md

# 完整集（含 hooks + CI）
cp -r templates/ your-project/
cp -r templates/ci-node.yml your-project/.github/workflows/ci.yml
bash scripts/install-git-hooks.sh      # 或 install-git-hooks.ps1
```

---

## 常见问题

| 问题 | 解决 |
|------|------|
| 其他工具能自动加载 20 个 Skill 吗？ | 不能。只有 Claude Code 原生支持官方 SKILL.md，其他工具需手动转换 |
| 权限模型在其他工具生效吗？ | 不完全。Claude Code 原生支持 permissions.json，其他工具需在各自设置里配置 |
| 一定要用 Claude Code 吗？ | 不用。工具无关设计，但体验最佳的是 Claude Code（全适配） |
| superpowers 是必须的吗？ | 建议装（方法论底座），不装也能用我们的 Skill，只是少了 brainstorm/plan/TDD 流程 |

## 相关文档

- `docs/getting-started.md` — 详细入门（含技术选型）
- `docs/scoring.md` — 评分维度表（为什么这么设计）
- `configs/tool-presets/` — 各工具配置预设
