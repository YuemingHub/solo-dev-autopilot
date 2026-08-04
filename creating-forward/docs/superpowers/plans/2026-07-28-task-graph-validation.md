# Task Graph Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 提供只读 JSON 任务图验证器和可机器检查的符合性场景结构。

**Architecture:** `scripts/task_graph.py` 承担纯验证逻辑，`scripts/validate_task_graph.py` 只承担 CLI 和序列化；`schemas/task-graph.schema.json` 记录公开结构；`evals/*.json` 提供结构化场景定义，`scripts/validate_evals.py` 检查评估资产边界。全部使用 Python 3 标准库。

**Tech Stack:** Python 3 标准库、JSON、JSON Schema 文档、unittest

## Global Constraints

- 输入只支持 JSON。
- 验证器只读，不执行、不修改、不修复任务图。
- 不增加第三方依赖。
- 错误码是公开稳定接口，消息不是机器契约。
- 场景结构通过不等于 Agent 行为通过。
- 不创建 commit、不发布、不部署。

---

### Task 1: Task Graph Core Validator

**Files:**
- Create: `scripts/task_graph.py`
- Create: `schemas/task-graph.schema.json`
- Create: `tests/test_task_graph.py`
- Modify: `schemas/task.schema.json`

**Interfaces:**
- Produces: `validate_task_graph(graph: object) -> dict`
- Result: `{ "valid": bool, "errors": list[dict], "topologicalOrder": list[str] }`

- [ ] 写有效 DAG、重复 ID、未知依赖、自依赖、重复依赖和环检测失败测试。
- [ ] 运行 `python -m unittest tests.test_task_graph -v`，确认因模块不存在而失败。
- [ ] 实现字段验证、引用检查和 Kahn 拓扑排序。
- [ ] 运行窄测试，确认全部通过。

### Task 2: Stable CLI Contract

**Files:**
- Create: `scripts/validate_task_graph.py`
- Modify: `tests/test_task_graph.py`

**Interfaces:**
- Produces: `python scripts/validate_task_graph.py <graph.json> [--format json]`
- Exit codes: `0` valid, `1` invalid graph, `2` usage/read error

- [ ] 写文本输出、JSON 输出、无效 JSON和缺失文件测试。
- [ ] 运行窄测试，确认 CLI 测试失败。
- [ ] 实现参数解析、读取和稳定输出。
- [ ] 运行窄测试，确认全部通过。

### Task 3: Executable Evaluation Structure

**Files:**
- Create: `evals/core-scenarios.json`
- Create: `evals/mingos-scenarios.json`
- Create: `scripts/validate_evals.py`
- Create: `tests/test_evals.py`
- Modify: `evals/SCENARIOS.md`
- Modify: `evals/MINGOS_SCENARIOS.md`

**Interfaces:**
- Produces: `python scripts/validate_evals.py`

- [ ] 写场景 ID、层级、Adapter、断言类型和证据字段测试。
- [ ] 运行 `python -m unittest tests.test_evals -v`，确认缺少资产而失败。
- [ ] 创建结构化场景并实现边界校验器。
- [ ] 运行窄测试，确认全部通过。

### Task 4: Integration and Documentation

**Files:**
- Modify: `scripts/validate_package.py`
- Modify: `tests/test_package.py`
- Modify: `README.md`
- Modify: `START_HERE.md`
- Modify: `AGENTS.md`
- Modify: `protocol/graph-engineering.md`
- Modify: `CHANGELOG.md`
- Modify: `task_plan.md`, `progress.md`, `findings.md`

- [ ] 将新脚本、Schema 和评估 JSON 加入包级必需结构。
- [ ] 文档记录 CLI、错误语义和“结构通过不等于行为通过”。
- [ ] 运行所有 unittest、包校验、评估校验和 py_compile。
- [ ] 运行独立代码审查并修复 Critical/Important 问题。
