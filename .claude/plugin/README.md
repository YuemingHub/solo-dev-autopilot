# Claude Code 插件市场注册

本目录（`.claude/plugin/marketplace.json`）与仓库根目录的 `.claude-plugin/marketplace.json` 是同一份市场清单，格式与 [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) 官方市场一致。

## 用法

仓库推送到 GitHub 后，在 Claude Code 中注册并安装：

```text
/plugin marketplace add YuemingHub/solo-dev-autopilot
/plugin install solo-dev-autopilot@YuemingHub/solo-dev-autopilot
```

> 也可以把本仓库作为插件直接安装（仓库根目录的 `.claude-plugin/plugin.json` 声明了 skills 位置）。

## 发布前需要修改

- `owner.email`：替换为你的真实邮箱（`replace-me@example.com`）
- `plugins[].source.url`：替换为你的仓库实际地址（已预填 YuemingHub/solo-dev-autopilot）

## 手动安装（不依赖市场）

```text
/plugin install YuemingHub/solo-dev-autopilot
```

或直接把本仓库 clone 后，把 `.claude/skills/` 复制到你的项目 `.claude/skills/`。
