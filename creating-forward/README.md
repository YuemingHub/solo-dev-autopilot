# Creating Forward 向未来去创造

Creating Forward 是一套可被 AI Agent 加载的平台无关工作协议。用户负责表达目标、确认方向和保留必要的人类决定；Agent 负责澄清、规划、执行、验证、记录、恢复和交付。

当前主库版本为 `0.4.0-dev`。它由 bootstrap v0.2 演进而来，正在把通用 Core 与首个真实验证项目 MingOS 完全分层。

## 架构

```text
通用 Core
  SKILL.md + protocol/ + schemas/ + templates/
        ↓ 可选加载
项目或平台 Adapter
  adapters/
        ↓ 应用与验证
目标项目的 .creating-forward/ 工作区
```

- `SKILL.md`：平台无关行为契约。
- `protocol/`：需求、上下文、任务图、循环、证据、授权与演进规则。
- `schemas/`、`templates/`：状态和记录契约。
- `adapters/`：项目或平台专属约束；只能收紧 Core。
- `bootstrap/`、`plans/`：真实验证项目的启动入口和计划。
- `sources/`：只读历史来源，不是当前执行状态。

## 开始使用

1. 让 Agent 从 `START_HERE.md` 开始。
2. 在目标项目运行：

```powershell
python scripts/init_workspace.py <project-path> [adapter ...]
python scripts/validate_workspace.py <project-path>
```

3. 若目标项目有 Adapter，先读取并确认它只会收紧 Core，再将 Adapter 名称作为初始化参数写入状态。例如：`python scripts/init_workspace.py <mingos-path> mingos`。
4. 需求确认后执行任务；没有证据的任务不得标记完成。

## 开发验证

```powershell
python scripts/validate_package.py
python scripts/validate_evals.py
python scripts/validate_task_graph.py <graph.json>
python -m unittest discover -s tests -v
```

任务图 CLI 只读取 `0.4.0-dev` JSON 图文件，验证任务字段、依赖引用、重复依赖和有向环，成功时输出确定性拓扑顺序。结构化评估校验只证明场景目录有效，不代表 Agent 行为已经执行或通过。

本项目不要求 MCP、Web 应用、数据库或特定模型。Skill 定义工作方法，外部工具只提供能力。

## MingOS 验证

MingOS 是第一个正式验证环境，不是通用 Core 的组成部分。相关入口：

- `adapters/mingos.md`
- `bootstrap/MINGOS_LOCAL_AGENT_PROMPT.md`
- `plans/MINGOS_PHASE0_PLAN.md`
- `docs/MINGOS_VALIDATION_PROGRAM.md`

## 历史

- 早期 PRD：`sources/history-2026-07-27/creating-forward-prd-v0.1.md`
- v0.2 产品谱系：`docs/PRODUCT_LINEAGE.md`
- 当前决策基线：`docs/PRODUCT_DECISION_BASELINE.md`
- 版本和迁移：`docs/VERSIONING_AND_MIGRATION.md`

发布快照保存在迭代日志目录；本目录是唯一持续开发主库。
