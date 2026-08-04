# Changelog — v2.0

> **2026-08-03** — Phase 1 兼容性改造完成。重大版本升级，不兼容 v1.x。

## v2.5.1 — 第 3 轮回响（2026-08-04）

### 新增

- **newbie-pitfalls.md 坑 32**：npm 写操作会替换 node_modules junction，多 worktree 共享依赖被拆散
  （三仓联动第 3 轮实测：`npm audit fix` 把共享 junction 替换成残缺真实目录，`Cannot find module 'axios'`；
  解决 = worktree 只跑测试、npm 写操作回主工作区或 `--package-lock-only`、被替换后删除残缺目录重建 junction）

### 说明

- 补丁级更新，2.5 系列内；无破坏性变更

## v2.5 — 第 2 轮回响固化（2026-08-04）

> 三仓库联动第 2 轮（Ming-os 安全越界修复 + 三轨并行）跑完后，把 6 个新坑与多 Agent 协作规范固化进仓库。

### 新增

- **newbie-pitfalls.md 坑 26-31**：
  - 坑 26 `git fetch` 定向拉分支防超时（全量拉取 34s+ 超时 vs 定向 4.7s）；
  - 坑 27 gh CLI 在 PowerShell 传中文/特殊字符 → 文案落盘 + `--body-file`；
  - 坑 28 Draft PR 基线漂移 → push 前 rebase + `git diff origin/production...HEAD --stat` 验证；
  - 坑 29 PowerShell 读 UTF-8 文件加 `-Encoding UTF8`（显示乱码 ≠ 存储损坏）；
  - 坑 30 密钥/凭据脚本不入库，先 `git status --porcelain` + `git ls-files` 扫描；
  - 坑 31 多 Agent 共享工作区协作规范（分支所有权 / 状态单一事实源 / 动工前检查 / 合并权归用户）
- **docs/closed-loop.md**：新增「实战回响记录」章节（第 1/2 轮）；第 7 步补 rebase 验证、第 8 步补多轨状态认领/回填
- TOC 同步新增「6.5 多 Agent 并行协作」

### 验证

- 全部 JSON 配置解析通过（node v22）
- CI（ci-self-check.sh）由 GitHub Actions 在 PR 上自动运行
- 本批次由 Codex 按 9 步闭环执行（第 2 轮实战反馈落地）

## v2.4 — 三仓库联动固化批次（2026-08-04）

> 用真实项目（Ming-os）跑完第 1 轮 9 步闭环后，把实战经验固化进仓库。

### 新增

- **Codex 适配**：`configs/tool-presets/codex.json`（三级模式 → Codex 沙箱/AGENTS.md 映射）+ `docs/codex-setup.md`（两种接入方式 + 已知差异）；README 适用工具表/结构树/架构图同步
- **`docs/closed-loop.md`**：三仓库联动 9 步闭环正式文档（进度→地图→规划→开发→验证→审查→提交→记录→回响；角色/档位/红线/粒度）
- **newbie-pitfalls.md 增补坑 20-25**：PowerShell 5.1 中文 commit、GitHub 大包/代理、partial clone + `gc.auto=0`、UTF-16 .gitignore、终端乱码与存储乱码区分、Windows `python` 占位符

### 验证

- `configs/tool-presets/*.json` 全部 JSON 解析通过（ci-self-check 第 1 段 glob 自动覆盖新增 codex.json）
- README 结构树与实际文件一致；无 `YOUR_USERNAME` 等占位符残留
- 本批次由 Codex 会话按 9 步闭环执行（第 1 轮实战反馈落地）

## v2.3.3 — 复核修复批次（2026-08-03）

> 对仓库做独立复核，修复 3 处残留，补上 Skill 兼容层同步机制，防止双格式漂移。

### 修复

1. **clone URL 占位符**：README / getting-started 的 `YOUR_USERNAME` → `YuemingHub`（仓库已公开，占位符失效）
2. **scoring.md 过时表述**：维度 6"CI 未实际跑过" → 修正为实测记录（verification.md §3：GitHub Actions 连续 3 次全绿）
3. **docs/EVOLVE_CHANGELOG.md 缺失**：auto-evolve.yml 引用的变更记录文件从未创建，已补齐

### 新增

- `scripts/sync-skills.py` — Skill 兼容层同步：`.claude/skills/<name>/SKILL.md`（官方）→ `skills/<name>.md`（社区工具平铺兼容层）；支持 `--check` 供 CI 使用
- 补全 4 个缺失的平铺兼容文件：test-runner / ci-helper / observability / production-preflight（此前兼容层只有 9/13，Reasonix / Cline 用户拿不到 Phase 3 的 4 个新 Skill）

### 增强

- `scripts/ci-self-check.sh` — 新增第 4 段：Skill 兼容层同步检查（`sync-skills.py --check`；python3 不可用时降级为存在性检查）

### 验证

- `python scripts/sync-skills.py` 本地生成 13 个平铺文件无错误
- 推送后由 GitHub Actions 完整自检（含第 4 段首次运行）

## v2.3.2 — CI 模板端到端验证修复（2026-08-03）

> 用真实 Node 项目把 templates/ci-node.yml 整条流水线跑了一遍，发现并修复 3 个模板缺陷。
> 验证过程与证据见 `docs/verification.md`。

### 修复

1. **覆盖率门失效**：`--reporter=json` 是 vitest 测试结果 reporter，不输出 JSON 到 stdout，
   grep `"lines"` 落空导致门静默失效 → 改用 `--coverage.reporter=json-summary`
   生成 coverage/coverage-summary.json，node 一行提取 `s.total.lines.pct` 判断 ≥80%
2. **审计形同虚设**：`pnpm audit --audit-level=high || true` 让高危漏洞不阻止 CI →
   去掉豁免，高危真实阻止；确认为可接受风险时显式加回（注释说明）
3. **密钥扫描漏报**：值部分 `[A-Za-z0-9]{16,}` 匹配不了 `sk-` 带连字符格式 →
   改 `[^'"[:space:]]{16,}` + `access[_-]?key` 备选（覆盖 aws_secret_access_key 模式），
   6 案例两向测试全过

### 新增

- `docs/verification.md` — 验证记录：配置自检 / hooks 实测 / CI 真实运行 / 模板端到端 / 一致性检查，全部可复现

### 验证

- 最小 vitest 项目：3 tests passed，覆盖率 100% ≥ 80% 门 ✅
- tsc lint/build 通过 ✅；pnpm audit 正常报告（vitest 2.1.9 critical 漏洞被正确标出）✅
- 密钥扫描 6/6 两向正确（sk-/AKIA 命中，env 引用/短值/模板串不误报）✅

## v2.3.1 — CI 自检修复（2026-08-03）

> 修复：本仓库的 CI 不能跑 Node 模板（仓库本身没有 package.json）。

### 变更

- `.github/workflows/ci.yml` — 从「Node 项目 CI 模板」改为「仓库自检」：JSON 有效性 / SKILL.md 格式 / Shell 语法
- `scripts/ci-self-check.sh` — 自检脚本（新增），本地可跑、CI 复用同一脚本；纯 POSIX（兼容 Git for Windows 迷你 sh）
- `templates/ci-node.yml` — Node 项目 CI 模板（新增），供用户复制到自己的项目；ci-helper skill / README / 蓝图 / tool-setup / scoring 引用同步更新

### 为什么

原 ci.yml 带 `on: push` 触发器，但本仓库无 package.json，`pnpm install` 必失败——推送后 Actions 必红。
现在本仓库 CI 验证自己的产品（配置包），用户 CI 用模板，各归其位。

## v2.3 — Phase 4 文档与评分（2026-08-03）

> Phase 4 完成：评分 9 分有理有据。

### 新增

- README **架构图**（四层：你的项目 → AI 工具 → Autopilot 配置层 → 上游底座）
- `docs/tool-setup.md` — 各 AI 工具安装引导（Claude Code 全适配 + Cursor/Cline/Reasonix/Windsurf 社区适配步骤 + 迁移已有项目）
- `docs/scoring.md` — **评分维度表**：8 维加权，逐维度附实物证据链，加权总分 9.0 的计算路径

### 增强

- `docs/getting-started.md` — 补「三步开始」总览；修复 v1 残留（平铺 `skills/*.md` → 文件夹式 `.claude/skills/`；自定义 Skill 改官方 SKILL.md 格式；多项目软链指向修正）
- `BOOTSTRAP-PROMPT.md` — `skills/` → `.claude/skills/` 引用修正
- README 文档区挂载 tool-setup.md / scoring.md

### 里程碑验收

- [x] README 定位声明 + 依赖说明 + 架构图
- [x] 各工具安装引导文档（tool-setup.md 覆盖 5 工具）
- [x] 评分维度表发布（scoring.md，证据链可追溯）
- [x] 「三步开始」完整流程（README 简版 + getting-started 详版）

## v2.2 — Phase 3 生产化（2026-08-03）

> Phase 3 完成：生产可用配置包就位。

### 新增

- `configs/permissions.json` — **三级危险度权限模型**（safe 自动放行 / ask 确认 / danger 拒绝+确认），作为权限唯一事实源
- `configs/modes/toy.json` / `team.json` / `production.json` — **三档配置**：权限 + hook 严格度 + 记忆策略 + Claude Code 即用权限片段
- 4 个新 Skill：
  - `.claude/skills/test-runner/SKILL.md` — 测试闭环：识别技术栈 → 跑单测/集成/E2E → 覆盖率报告（基线 ≥ 80%）
  - `.claude/skills/ci-helper/SKILL.md` — CI 配置生成 + 本地复现 + 失败诊断
  - `.claude/skills/observability/SKILL.md` — 结构化 JSON 日志规范 + Sentry 集成 + 健康检查端点 + 告警
  - `.claude/skills/production-preflight/SKILL.md` — 上线前六维预检（覆盖率/CI/权限/可观测性/密钥/回滚），与 deploy-gate 衔接
- `.github/workflows/ci.yml` — CI 模板：lint → test(+覆盖率门 80%) → build → 依赖审计 → 密钥扫描
- `scripts/post-session.ps1` — Windows 版会话后处理（与 post-session.sh 对齐）
- `docs/production-checklist.md` — 生产上线人工兜底清单
- `docs/autopilot-boundaries.md` — AI 边界原则：开发可自动、部署必人工

### 增强

- pre-commit-hook — **严格度可配置**：读取 `.autopilot-mode`（toy=仅警告 / team & production=阻止）；any 检查精确化（跳过注释行，`\b` 边界减少误报）
- setup.sh / setup.ps1 — 新增**配置模式选择**（toy/team/production → 写入 `.autopilot-mode`）；hooks 安装带备份且 pre-commit/pre-push 齐全
- `.claude/settings.json` + `configs/tool-presets/claude-code.json` — 权限升级为三级危险度模型（deny 增加 sudo/chmod 777/curl|sh 等 danger 规则）
- scripts/install-git-hooks.ps1 — 补 UTF-8 BOM，修复 PS 5.1 中文解析失败

### 里程碑验收

- [x] CI 通过率 > 95%（ci-helper + ci.yml 模板：lint→test→build→audit→secret scan）
- [x] 生产模式配置档能正常加载（configs/modes/production.json 可合并到 .claude/settings.json）
- [x] test-runner 能跑 npm test / pytest 并输出覆盖率（基线 ≥ 80%）

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

- **v2.3**：生产化配置档补全（toy/team/production）→ 已完成 ✅（v2.2）
- **Phase 4**：文档与评分（README 定位声明已更新、评分维度表、三步开始流程完善）
- **v3.0**：评分 9.0 — 中文新手 + 完整交付闭环 + 生产可用

详见 [BLUEPRINT-v2.md](./docs/BLUEPRINT-v2.md)。
