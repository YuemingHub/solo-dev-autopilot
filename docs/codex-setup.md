# Codex 接入指南（v2.4 新增）

> 本仓库的方法论与 Skill 是工具无关的（官方 SKILL.md 格式），Codex（OpenAI 桌面版 / CLI）可以直接使用。
> 与 Claude Code 全适配不同，Codex 没有「插件市场 + 按命令权限表」，因此用 **AGENTS.md 指令 + 沙箱模式**承载三级危险度权限模型（唯一事实源：`configs/permissions.json`）。

## 1. 两种接入方式

### 方式 A：以本仓库为项目根目录（推荐）

```bash
git clone https://github.com/YuemingHub/solo-dev-autopilot.git
cd solo-dev-autopilot
```

1. 把 `configs/tool-presets/codex.json` 里的 `agentsMd` 片段合入仓库根 `AGENTS.md`（Codex 自动读取）。
2. 加载 skills：把 `.claude/skills/` 复制到 `.codex/skills/`（Codex 的 skills 目录约定，20 个 SKILL.md 均为官方格式）。
3. 安装 git hooks：`bash scripts/install-git-hooks.sh`（或 Windows 版 `scripts/install-git-hooks.ps1`）。

### 方式 B：接入已有项目

1. 把 `.claude/skills/` 复制到项目的 `.codex/skills/`；
2. 把 `templates/` 中的记忆/指南模板复制进项目并填写；
3. 把 `agentsMd` 片段合入项目 `AGENTS.md`。

## 2. 三级模式 → Codex 沙箱映射

| 档位 | Codex 沙箱/权限 | 行为 |
|---|---|---|
| toy | workspace-write | 学习档：项目内读写自动放行；pre-commit 只警告 |
| team | workspace-write | 正常开发档：P0 阻止提交、pre-push 提醒 |
| production | workspace-write + 发布类操作人工确认（AGENTS.md 红线） | 部署/密钥/真实数据/合并 production 一律先问用户 |

> 不要复制 Claude Code 的权限表；Codex 侧以 AGENTS.md 指令表达同样语义。

## 3. 推荐流程：9 步闭环

见 `docs/closed-loop.md`：进度 → 地图 → 规划 → 开发 → 验证 → 审查 → 提交 → 记录 → 回响。

## 4. 已知差异与注意

- superpowers 是 Claude Code 插件市场的方法论底座；Codex 侧的方法论由 20 个 Skill + 9 步闭环 + creating-forward 协议层承担，不强制安装 superpowers。
- 中文 commit 消息用 `git commit -F <UTF-8无BOM文件>`（PowerShell 5.1 的 `-m` 中文会变 `?`，见 `newbie-pitfalls.md` 坑 20）。
- GitHub 大包传输失败时用代理（见 `newbie-pitfalls.md` 坑 21）。
- 修改 skill 内容只改 `.claude/skills/`，平铺兼容层由 `scripts/sync-skills.py` 单向同步。
