# Changelog — v2.0

> **2026-08-03** — Phase 1 兼容性改造完成。重大版本升级，不兼容 v1.x。

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