# Loop Engineering

## 标准循环

1. Observe：读取任务、状态、工作区真实情况。
2. Plan：选择本轮最小必要动作。
3. Act：执行。
4. Verify：收集证据并对照完成标准。
5. Checkpoint：更新任务、证据、事件和状态。
6. Continue：继续、修复、阻塞或暂停。

## 默认预算

```yaml
maxAttemptsPerTask: 3
maxConsecutiveSameFailure: 2
maxDerivedRepairTasks: 2
maxParallelBuilders: 2
externalCostBudgetCny: 0
stopWhenNoReadyTask: true
```

## 防空转

以下情况必须停止：
- 没有 ready 任务。
- 权限不足。
- 超过重试上限。
- 需要不可逆决定。
- 发现生产或敏感数据风险。
- 成果需要主观验收。
