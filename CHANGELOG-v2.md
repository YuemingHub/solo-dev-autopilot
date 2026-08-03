# Changelog — v2.0

> **2026-08-03** — Phase 1 兼容性改造完成。重大版本升级，不兼容 v1.x。

## v2.1 — Phase 2 独有层（2026-08-03）

> Phase 2 完成：竞品没有的差异化能力就位。

### 新增

- `.claude/skills/onboarding/SKILL.md` — 首次使用引导：检测/安装 superpowers + 首次对话四步走
- `.claude/skills/deploy-gate/SKILL.md` — 部署门禁：P0-P3 检查 + CI 检查 + 密钥扫描 + **人工确认红线** + 回滚指南 + 中国部署场景
- `.claude/plugin/marketplace.json` + `.claude-plugin/marketplace.json` — 插件市场注册（schema 与 obra 官方市场一致）
- `.claude-plugin/plugin.json` — 仓库本身可作为 Claude Code 插件安装

### 增强

- context-map 增加**记忆裁剪策略**：CODEMAP 分级（P0 完整 / P1 接口签名 / P2 文件名）、PROJECT-MEMORY 2000 字自动摘要、SESSION_DRIVER 保留最近 3 次会话、手动全量刷新指令（100 文件项目 ≤ 2000 行）
- setup.sh / setup.ps1 — 改为安装官方文件夹式 SKILL.md；新增 superpowers 自动检测与安装引导；其他工具标注"社区适配中"（D4 决策）

### 变更

- deploy-check → **deploy-gate**（改名 + 增强），README/模板/文档引用全部同步
- 删除被 superpowers 覆盖的 git-workflow skill（using-git-worktrees + finishing-a-development-branch 已覆盖）

### 修复

- setup 脚本原按 v1 平铺 .md 复制到 .claude/skills/（Claude Code 无法识别）→ 改为文件夹式复制
- setup.sh 中 docs/mcp-guide.md 死链 → 改为 BLUEPRINT-v2.md

### 里程碑验收

- [x] 安装脚本能自动检测并引导安装 superpowers
- [x] 记忆文件在 100 文件项目下不超过 2000 行（context-map 裁剪策略）
- [x] deploy-gate 的部署确认不可被跳过（红线规则强制人工确认）

## 为什么是 v2.0

v1.x 是"新手引导模板"，目标是让 AI 帮你把想法变成能跑的东西。
v2.0 开始向"生产可用"转型——仍然对新手友好，但不再以牺牲模型能力为代价。

## Breaking Changes

| 变更 | v1.x | v2.0 |
|------|------|------|
| **Skill 格式** | 自定义 frontmatter（runAs/tools/priority/tags） | 官方 SKILL.md 标准（name/description/license） |
| **Skill 位置** | `skills/*.md` | `.claude/skills/<name>/SKILL.md` |
| **权限模型** | 窄白名单（10 个命令） | 三级危险度（auto-allow 60+ / ask 13 / deny 6） |
| **pre-commit any** | P0 阻止提交 | P1 警告不阻止 |
| **技术栈描述** | "预设最优全栈配置" | "预设默认全栈配置"（可替换） |

## 新增

- 9 个 Skill 迁移到 `.claude/skills/<name>/SKILL.md`，符合 [anthropics/skills](https://github.com/anthropics/skills) 官方规范
- `.claude/settings.json` — Claude Code 即用配置（三级权限 + skillsPath）
- `configs/tool-presets/reasonix.json` — 三级权限模型 + 保留 hooks
- `templates/pre-commit-hook` — any 降级 P1 + 新增 console.log 检查
- `scripts/install-git-hooks.sh/.ps1` — 安装前自动备份已有 hook
- `docs/BLUEPRINT-v2.md` — v2 完整开发蓝图（14 章 + 附录）
- `CHANGELOG-v2.md` — 本文件

## 修复

- README 移除 4 处死链（generate-code-map.py、mcp-guide.md、skill-writing.md、contributing.md）
- README 7 处"最优"改为"默认/推荐"
- README 目录树更新为 v2 实际结构

## 升级指南

```bash
git pull origin main

# 重新安装 Git Hooks（旧 hook 会自动备份）
bash scripts/install-git-hooks.sh        # macOS/Linux
powershell -ExecutionPolicy Bypass -File scripts\install-git-hooks.ps1  # Windows
```

`skills/` 目录保留作为源文件，所有 Skill 已迁移到 `.claude/skills/`。

## 下一步

- **v2.1**：superpowers 自动安装 + 中文增强层
- **v2.2**：测试闭环 + CI 集成
- **v2.3**：生产化配置档（toy/team/production）
- **v3.0**：评分 9.0 — 中文新手 + 完整交付闭环 + 生产可用

详见 [BLUEPRINT-v2.md](./docs/BLUEPRINT-v2.md)。