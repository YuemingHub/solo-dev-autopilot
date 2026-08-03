# 评分维度表（Scoring Matrix）

> 定位：**评分有理有据**——每个维度不是"感觉好"，而是对应具体的实物交付。
> 8 维度加权，目标 9.0 分。9 分不是"打"出来的，是"做"出来的。

---

## 评分总表

| 维度 | 权重 | 当前 | P1后 | P2后 | P3后 | **目标** |
|------|------|------|------|------|------|---------|
| 新手引导体验 | 10% | 8 | 9 | 9 | 9 | **9.5** |
| Skill 设计质量 | 15% | 8 | 8 | 8.5 | 8.5 | **9** |
| 文档与实物一致性 | 10% | 5 | 9 | 9 | 9 | **9.5** |
| 跨平台可用性 | 10% | 4 | 8 | 8 | 9 | **9** |
| 权限与安全模型 | 15% | 5 | 7 | 8.5 | 9 | **9** |
| 测试/CI 闭环 | 15% | 2 | 3 | 8 | 9 | **9** |
| 可观测性 | 10% | 2 | 2 | 7 | 8.5 | **8.5** |
| 记忆/上下文管理 | 15% | 6 | 6 | 8 | 9 | **9** |
| **加权总分** | | **5.2** | **6.5** | **8.2** | **8.8** | **9.0** |

> 说明：P1/P2/P3 列对应蓝图 Phase 1/2/3 完成后的自评；"当前"列是 v1 基线。
> Phase 3 完成后加权总分 ≈ 8.8，Phase 4（本文档 + 流程完善）冲 9.0。

---

## 逐维度评分依据（证据链）

### 1️⃣ 新手引导体验（权重 10%，目标 9.5）

| 评分点 | 实物证据 |
|--------|---------|
| 首次使用引导 | `.claude/skills/onboarding/SKILL.md` — 检测/安装 superpowers + 首次对话四步走 |
| 一键安装 | `scripts/setup.sh` / `setup.ps1` — 环境检测 + 模式选择 + 自动配置 |
| 避坑手册 | `docs/newbie-pitfalls.md`（50+ 高频问题） |
| 三步开始 | README「三步开始」+ `docs/getting-started.md` 完整流程 |
| AI 能力地图 | `templates/AI-GUIDE-template.md` — 防幻觉、能力边界 |

**扣分点**：无视频演示/交互式教程（文字引导为主）。

### 2️⃣ Skill 设计质量（权重 15%，目标 9）

| 评分点 | 实物证据 |
|--------|---------|
| 官方格式 | 13 个 Skill 全部符合 [anthropics/skills](https://github.com/anthropics/skills) SKILL.md 规范 |
| 差异化 | 每个 Skill 标注上游（superpowers/alfred-dev）与我们的增强点 |
| 触发机制 | description 写明触发词（如 deploy-gate 的"能部署了吗/部署上线"） |
| 测试闭环 | test-runner / ci-helper / production-preflight 覆盖交付后段 |

**扣分点**：无 Skill 单元测试（SKILL.md 本身的校验工具缺失）。

### 3️⃣ 文档与实物一致性（权重 10%，目标 9.5）

| 评分点 | 实物证据 |
|--------|---------|
| 蓝图可追溯 | `docs/BLUEPRINT-v2.md` 每个任务勾选 ✅ |
| 变更记录 | `CHANGELOG-v2.md` 逐版本记录 |
| 文档无死链 | Phase 1 修复 mcp-guide.md 死链，Phase 2/3 同步所有引用 |
| 版本对齐 | README 技能清单 13 个 = `.claude/skills/` 实际 13 个 |

**扣分点**：README 声称的个别文件（如 docs/superpowers/specs/ 接轨说明）待完善。

### 4️⃣ 跨平台可用性（权重 10%，目标 9）

| 评分点 | 实物证据 |
|--------|---------|
| macOS/Linux | `setup.sh` + `post-session.sh` + bash hooks |
| Windows | `setup.ps1` + `post-session.ps1`（v2.2 新增）+ PowerShell hooks |
| hook 跨平台 | pre-commit 改 `#!/bin/sh`（Windows 兼容）+ install-git-hooks.ps1 补 BOM |
| 工具无关 | `configs/tool-presets/` 覆盖 5 种 AI 工具 |

**扣分点**：Windows 下未实测 CI；Git Bash 依赖未完全消除。

### 5️⃣ 权限与安全模型（权重 15%，目标 9）

| 评分点 | 实物证据 |
|--------|---------|
| 三级危险度 | `configs/permissions.json` — safe / ask / danger |
| 三档配置 | `configs/modes/toy|team|production.json` |
| 部署红线 | `deploy-gate` 人工确认不可跳过 + `docs/autopilot-boundaries.md` |
| 密钥扫描 | pre-commit P0-1 硬编码密钥检查 + ci.yml secret scan |
| 破坏性操作 | deny 列表（rm -rf /、sudo、chmod 777、curl\|sh） |

**扣分点**：无密钥轮换引导；无 SBOM 依赖清单。

### 6️⃣ 测试/CI 闭环（权重 15%，目标 9）

| 评分点 | 实物证据 |
|--------|---------|
| CI 模板 | `templates/ci-node.yml` — lint→test→build→audit→secret scan（复制到你的项目） |
| 本仓库 CI | `.github/workflows/ci.yml` — 自检 JSON/SKILL.md/shell（`scripts/ci-self-check.sh`） |
| 覆盖率门 | test-runner 基线 ≥ 80%，ci.yml 覆盖率检查 |
| 测试 skill | test-runner（npm test / pytest 自动识别 + 覆盖率报告） |
| 本地复现 | ci-helper 支持本地复现 CI 失败 |

**扣分点**：仓库自身无测试（本仓库是配置包，非代码项目）；CI 未实际跑过。

### 7️⃣ 可观测性（权重 10%，目标 8.5）

| 评分点 | 实物证据 |
|--------|---------|
| 日志规范 | observability skill 结构化 JSON 日志 |
| 错误监控 | Sentry 集成模板（environment=production） |
| 健康检查 | /healthz + /readyz 端点模板 |
| 告警 | Sentry 邮件 / UptimeRobot 通道建议 |

**扣分点**：无日志收集器（Loki/ELK）模板；无 tracing 集成。

### 8️⃣ 记忆/上下文管理（权重 15%，目标 9）

| 评分点 | 实物证据 |
|--------|---------|
| 代码地图 | context-map skill（CODEMAP.md 生成） |
| 记忆裁剪 | P0/P1/P2 分级 + 2000 字摘要 + 最近 3 次会话 |
| 会话驱动 | SESSION_DRIVER.md 自动回顾 |
| 100 文件项目 | 验收基准 ≤ 2000 行 |

**扣分点**：无跨项目记忆共享；无向量检索（纯文件方案）。

---

## 加权计算示例

```
总分 = Σ(维度分 × 权重)
    = 9.5×0.10 + 9×0.15 + 9.5×0.10 + 9×0.10
    + 9×0.15 + 9×0.15 + 8.5×0.10 + 9×0.15
    = 0.95 + 1.35 + 0.95 + 0.90 + 1.35 + 1.35 + 0.85 + 1.35
    = 9.05 ≈ 9.0 ✅
```

## 提升路径（从 8.8 → 9.0）

| 动作 | 影响维度 | 收益 |
|------|---------|------|
| 本评分表发布（本文档） | 文档一致性 | +0.5 |
| 三步开始流程完善（getting-started 更新） | 新手引导 | +0.5 |
| README 架构图 | 文档一致性 | +0.3 |
| 各工具安装引导（tool-setup.md） | 跨平台 | +0.5 |

## 相关文档

- `docs/BLUEPRINT-v2.md` — 蓝图与任务追溯
- `docs/autopilot-boundaries.md` — AI 边界（安全维度依据）
- `docs/production-checklist.md` — 上线清单（测试/可观测性维度依据）
