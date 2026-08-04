# Creating Forward 任务图验证设计

## 1. 目标

为 Creating Forward 提供一个无第三方依赖、只读、确定性的任务图验证器，使 Governor 在执行前能够证明任务图节点结构完整、依赖引用有效且不存在有向环。

## 2. 选定方案

采用单一 JSON 图文件：

```json
{
  "version": "0.4.0-dev",
  "tasks": [
    {
      "id": "T-001",
      "title": "建立数据结构",
      "goal": "定义首版数据契约",
      "status": "ready",
      "dependencies": [],
      "completionCriteria": ["Schema 文件存在"],
      "verificationMethods": ["运行结构校验"],
      "allowedFiles": ["schemas/**"],
      "forbiddenActions": ["生产发布"],
      "assignedRole": "builder",
      "reviewRole": "verifier"
    }
  ]
}
```

JSON 是此验证器的公开输入契约。现有 YAML 任务模板保留为 Agent 可读写示例，但在没有受控 YAML 解析器前不作为确定性 CLI 输入。

## 3. 备选方案

### YAML 输入

与现有模板一致，但 Python 标准库不提供 YAML 解析。手写解析会重复上一迭代的契约风险，因此不采用。

### 通用图框架

可支持更多算法，但当前只需要引用检查和拓扑排序，引入框架会扩大依赖和接口面，因此不采用。

### 每任务一个文件

接近工作区实际形态，但需要额外处理目录枚举、文件格式和跨文件版本，当前先用单一图文件稳定契约。

## 4. CLI 接口

```powershell
python scripts/validate_task_graph.py <graph.json>
python scripts/validate_task_graph.py <graph.json> --format json
```

退出码：

- `0`：图有效。
- `1`：输入可读取，但图不符合契约。
- `2`：命令参数或文件读取错误。

文本成功输出：

```text
TASK GRAPH VALIDATION: PASSED
TOPOLOGICAL ORDER: T-001, T-002
```

JSON 成功输出：

```json
{"valid": true, "errors": [], "topologicalOrder": ["T-001", "T-002"]}
```

JSON 失败输出仍使用同一形状，`topologicalOrder` 为 `[]`。

## 5. 错误契约

每项错误包含：

```json
{"code": "DUPLICATE_TASK_ID", "taskId": "T-001", "message": "Duplicate task id: T-001"}
```

稳定错误码：

- `INVALID_GRAPH_SHAPE`
- `UNSUPPORTED_GRAPH_VERSION`
- `INVALID_TASK_SHAPE`
- `MISSING_TASK_FIELD`
- `INVALID_TASK_FIELD`
- `DUPLICATE_TASK_ID`
- `UNKNOWN_DEPENDENCY`
- `SELF_DEPENDENCY`
- `DUPLICATE_DEPENDENCY`
- `DEPENDENCY_CYCLE`

错误按任务输入顺序和检查顺序输出。消息用于人读，消费者只应依赖 `code`、`taskId` 和可选 `dependencyId`。

## 6. 验证规则

1. 根对象必须包含唯一版本和任务数组。
2. 版本必须为 `0.4.0-dev`。
3. 每个任务必须满足 `task.schema.json` 的当前确定性子集。
4. ID 必须为非空字符串且全图唯一。
5. 依赖必须是唯一字符串列表。
6. 依赖 ID 必须存在。
7. 任务不能依赖自己。
8. 图必须无环。
9. 成功时使用 Kahn 算法输出拓扑顺序；同层节点按原输入顺序处理。
10. 验证器不改变状态、任务或输入文件。

## 7. 符合性评估

新增机器可执行的结构评估清单，检查：

- Core 场景和 MingOS 场景具有稳定 ID。
- 每个场景声明层级、断言类型和证据要求。
- Core 场景不引用 MingOS 专属术语。
- MingOS 场景明确要求加载 `mingos` Adapter。

这些检查证明评估资产结构有效，不证明 Agent 行为已经通过。真实行为结果必须单独记录运行输入、输出和证据。

## 8. 非目标

- 不执行任务。
- 不计算任务是否应从 `pending` 变为 `ready`。
- 不自动修复图。
- 不解析 YAML。
- 不评估自然语言成果质量。
- 不启动 MingOS Phase 0。

## 9. 验收标准

- 有效 DAG 返回确定性拓扑顺序。
- 未知依赖、自依赖、重复依赖、重复 ID 和环均有稳定错误码。
- 无效 JSON 和文件不存在具有明确退出码。
- 现有 25 项测试不回归。
- 包校验将任务图验证器和评估资产列为必需文件。
- 独立审查无 Critical/Important 阻塞项。
