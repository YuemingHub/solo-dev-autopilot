# START HERE - Creating Forward Core

## 首次加载

1. 读取 `docs/PRODUCT_LINEAGE.md`，理解产品原意和不变边界。
2. 读取 `docs/PRODUCT_DECISION_BASELINE.md`，理解当前已固定决定。
3. 读取 `SKILL.md`，加载通用执行协议。
4. 检查目标项目是否有适用的 `adapters/` 文件；先确认它只会收紧 Core，没有则只使用 Core。
5. 读取目标项目自身的规则、文档、代码、测试和真实状态。
6. 读取 `docs/GOVERNED_EVOLUTION.md`，了解协议候选如何产生和审查。

## 初始化目标项目

在本仓库执行：

```powershell
python scripts/init_workspace.py <project-path> [adapter ...]
python scripts/validate_workspace.py <project-path>
```

初始化脚本只创建缺失的 `.creating-forward/` 文件，不覆盖已有状态。传入的 Adapter 名称会写入新状态的 `adapters` 列表。

## 开始任务

1. 从 `.creating-forward/state.yaml` 和事件记录恢复已有状态。
2. 核实目标项目的真实入口、能力、权限和上位约束。
3. 需求不清楚时，每次只问一个最影响方向的问题。
4. 需求确认后建立有依赖、完成标准和验证方法的任务图。
5. 正式执行前运行 `python scripts/validate_task_graph.py <graph.json>`；图无效时保持在 planning 或 blocked。
6. 执行低风险、可逆、已授权的工作，并在每次实质动作后更新状态。
7. 只有验证通过且证据已记录，任务才能完成。
8. 每次真实运行结束后完成 Run Review。
9. 协议问题只形成候选 Draft，不静默改写正式 Core。

## 项目 Adapter

Adapter 用于加入项目专属的上位原则、数据边界、分支策略和验证要求。Adapter 可以收紧 Core，但不能取消安全、证据、恢复和授权门禁。

## 最高规则

- 原始产品意图不能被当前技术实现覆盖。
- 用户离开不扩大授权。
- 能安全推进的，不等待。
- 不能代替用户的，不伪造。
- 没有证据的，不算完成。
- 可以迭代，但不能静默自我修改。
