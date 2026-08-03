---
name: onboarding
description: >
  首次使用引导：检测并安装 superpowers 上游方法论，完成首次对话设置。
  当用户是第一次打开这个仓库 / 说"我不会用" / "怎么开始" / "这是什么" / "帮我初始化" 时触发。
  目标：10 分钟内让新手进入"能自己推进开发"的状态。
license: MIT
---

# Onboarding — 首次使用引导

## 目标

新手第一次接触 Solo Dev Autopilot 时，通常卡在两个地方：

1. **不知道要装什么** —— superpowers 是上游方法论底座，不装的话我们的 Skill 是"半成品"
2. **不知道第一句说什么** —— 面对 AI 编程工具，脑子一片空白

这个 Skill 把这两件事变成 10 分钟的傻瓜流程。

## Step 1: 检测 superpowers 是否已安装

### Claude Code

在对话中输入：

```text
/plugin
```

看列表里有没有 `superpowers`。也可以直接问 AI："我装 superpowers 了吗？"

命令行检测：

```bash
# 已安装的插件
ls ~/.claude/plugins/installed 2>/dev/null | grep -i superpowers
# 已注册的市场
ls ~/.claude/plugins/marketplaces 2>/dev/null | grep -i superpowers
```

### Cursor

在 Agent 对话框输入 `/add-plugin superpowers`，能搜到就是能用。

### 其他工具（Codex / Gemini CLI / OpenCode 等）

目前标注"社区适配中"，参考 superpowers 官方 README 的安装章节：
<https://github.com/obra/superpowers>

## Step 2: 未安装 → 按工具引导安装

### Claude Code（推荐路径）

```text
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

或从 Anthropic 官方市场安装：

```text
/plugin install superpowers@claude-plugins-official
```

### Cursor

```text
/add-plugin superpowers
```

### 安装后验证

```bash
ls ~/.claude/plugins/installed | grep superpowers
```

出现 `superpowers` 目录 = 安装成功。

> ⚠️ **不要跳过这一步。** 我们的 Skill 是 superpowers 的**中文新手增强层**。
> 上游的 brainstorm → plan → TDD → review → finish 流程是底座，底座不装，增强层没有意义。

## Step 3: 首次对话四步走

按顺序引导用户，每步等 AI 回应后再继续：

1. **念启动咒语**（恢复上下文）

   ```text
   读取 PROJECT-MEMORY.md、CODEMAP.md 和 SESSION_DRIVER.md，了解项目当前状态，然后告诉我今天可以做什么。
   ```

   首次使用没有这些文件 → 让 AI 从 `templates/` 复制并初始化。

2. **说出想法**（不用想清楚）

   ```text
   我想做一个 xxx
   ```

   → 触发 task-planner 拆 MVP 和任务清单。

3. **确认本轮目标**（1-3 件事）

   AI 会问"这次先做哪几个"，别贪多，做完一件打一个勾。

4. **开始干活**（写一步跑一步）

   每完成一小步 → 提交一次 → 继续下一步。

## Step 4: 明确分工（我们的 Skill vs superpowers）

| 场景 | 用谁 | 说明 |
|------|------|------|
| 想法打磨 / 出设计方案 | superpowers brainstorming | 上游做 |
| 拆实现计划 / TDD | superpowers writing-plans / test-driven-development | 上游做 |
| Git worktree / 合并分支 | superpowers using-git-worktrees / finishing-a-development-branch | 上游做（我们的 git-workflow 已移除，避免重复） |
| 中文新手任务拆解 | task-planner | 我们做 |
| 代码审查（P0-P3 中文分级） | code-review | 我们做 |
| 部署门禁 + 人工确认红线 | deploy-gate | 我们做 |
| 上下文恢复 + 记忆裁剪 | context-map | 我们做 |

> 简单记忆法：**上游管"怎么把活干对"，我们管"新手怎么上手、怎么上线、怎么不迷路"。**

## 检查清单（完成标准）

- [ ] superpowers 已安装（`ls ~/.claude/plugins/installed | grep superpowers` 有输出）
- [ ] PROJECT-MEMORY.md / CODEMAP.md / SESSION_DRIVER.md 三个记忆文件已就位
- [ ] 用户说出了第一个想法，且已拆出 MVP
- [ ] 用户知道"每写一步跑一次、每完成一块提交一次"
- [ ] 用户知道部署前必须走 deploy-gate，且不能跳过人工确认

## 常见问题

**Q: 我不用 Claude Code，用 Cursor，能用吗？**
A: 能。superpowers 支持 Cursor 的 `/add-plugin superpowers`。其余工具按 superpowers 官方 README 安装，我们目前标注"社区适配中"（v2 优先 Claude Code 全适配）。

**Q: superpowers 是英文的，我看不懂怎么办？**
A: 我们的 Skill 全部是中文的，覆盖新手最常用的场景。superpowers 的英文 Skill 由 AI 自动翻译执行，你不需要直接读它。
