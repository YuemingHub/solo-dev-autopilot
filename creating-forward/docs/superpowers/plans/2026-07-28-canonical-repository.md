# Creating Forward Canonical Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `D:\LifeOs\Creating Forward` 建设为以 v0.2 为基线、Core 与 MingOS Adapter 分离的唯一主开发库。

**Architecture:** 迁入 v0.2 的协议、Schema、模板、脚本和历史来源；将顶层入口通用化；MingOS 专属内容保留在 Adapter、bootstrap 和验证计划中。使用 Python 标准库提供包级和工作区级验证，不新增第三方依赖。

**Tech Stack:** Markdown、YAML、JSON Schema、Python 3 标准库、Git

## Global Constraints

- 不修改 `D:\LifeOs\个人引擎室\08_迭代日志\creating-forward` 中的历史快照。
- 不引入 MCP、Web 应用、数据库或云端服务。
- 不自动发布、部署、合并或创建 Git commit。
- Core 不得绑定 MingOS、模型、厂商或具体工具名称。
- Adapter 只能收紧 Core，不能降低证据、安全和授权门禁。

---

### Task 1: 迁入经过验证的 v0.2 资产

**Files:**
- Create: `README.md`, `SKILL.md`, `START_HERE.md`, `CHANGELOG.md`
- Create: `protocol/**`, `schemas/**`, `templates/**`, `scripts/**`, `adapters/**`, `bootstrap/**`, `evals/**`, `plans/**`, `sources/**`
- Preserve: `docs/superpowers/specs/2026-07-27-creating-forward-skill-design.md`

- [x] 机械复制 v0.2 文件，排除 `__pycache__` 和 `.pyc`。
- [x] 比较历史来源哈希，确认早期 PRD 和记录未丢失。
- [x] 初始化 Git 仓库并添加标准 `.gitignore`，但不创建 commit。
- [x] 检查主库文件清单和 Git 工作树。

### Task 2: 将顶层协议通用化

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `START_HERE.md`
- Modify: `scripts/init_workspace.py`
- Modify: `scripts/validate_workspace.py`

**Interfaces:**
- Produces: `python scripts/init_workspace.py <project-path>`
- Produces: `python scripts/validate_workspace.py <project-path>`

- [x] 将 Skill 名称改为 `creating-forward`，使命改为任意复杂项目的可靠推进。
- [x] 保留七类工程、角色分工、证据门禁、授权和演进规则。
- [x] 从 Core 删除 MingOS 专属 Foundation、家庭数据和生产分支表述，以 Adapter 引用代替。
- [x] 重写 README 和 START_HERE，说明通用加载流程和可选 Adapter。
- [x] 将脚本参数和错误信息从 `mingos-repo-path` 改为 `project-path`。

### Task 3: 固化 MingOS Adapter 边界

**Files:**
- Modify: `adapters/mingos.md`
- Modify: `bootstrap/MINGOS_LOCAL_AGENT_PROMPT.md`
- Modify: `bootstrap/FIRST_RUN_CHECKLIST.md`
- Preserve: `plans/MINGOS_PHASE0_PLAN.md`

**Interfaces:**
- Consumes: 通用 `SKILL.md`
- Produces: MingOS 专属约束和 Phase 0 入口

- [x] 声明 Adapter 依赖的 Core 版本和优先级。
- [x] 明确专属授权边界只适用于 MingOS。
- [x] 确保 bootstrap 先加载 Core，再加载 Adapter 和验证计划。
- [x] 检查 MingOS 规则没有泄漏回 Core。

### Task 4: 增加包级自动验证

**Files:**
- Create: `scripts/validate_package.py`
- Create: `tests/test_package.py`
- Modify: `.gitignore`

**Interfaces:**
- Produces: `python scripts/validate_package.py`
- Produces: `python -m unittest discover -s tests -v`

- [x] 写测试，断言必需结构、合法 Schema、通用 Skill 身份和初始化闭环。
- [x] 先运行测试，确认缺少 package validator 时失败。
- [x] 实现最小 package validator。
- [x] 运行测试并修复失败。
- [x] 运行所有脚本的 `py_compile`。

### Task 5: 更新版本、清单和开发入口

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `docs/VERSIONING_AND_MIGRATION.md`
- Modify: `docs/PRODUCT_DECISION_BASELINE.md`
- Modify: `task_plan.md`, `findings.md`, `progress.md`
- Remove: `MANIFEST.json` from the mutable development root

- [x] 将当前开发版本标记为 `0.4.0-dev`，不伪装成已发布版本。
- [x] 记录从 MingOS bootstrap 到通用主库的迁移决定。
- [x] 将发布清单定义为打包时生成的不可变资产。
- [x] 更新计划和进度，记录验证证据和剩余风险。
- [x] 检查 Git diff、敏感文件形状和未跟踪文件。

### Task 6: 最终验证

**Files:**
- Verify only

- [x] 运行 `python scripts/validate_package.py`，预期 `PACKAGE VALIDATION: PASSED`。
- [x] 运行 `python -m unittest discover -s tests -v`，预期全部通过。
- [x] 运行 `python -m py_compile scripts/*.py tests/*.py` 的 PowerShell 等价命令，预期退出码 0。
- [x] 在临时目录执行初始化和工作区校验，预期 `VALIDATION: PASSED`。
- [x] 搜索 Core 中的 MingOS 专属词，确认只存在解释 Adapter 边界所需的引用。
- [x] 输出主库状态、未提交变化和下一迭代建议。
