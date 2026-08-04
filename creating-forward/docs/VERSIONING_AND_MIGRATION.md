# 版本与迁移策略

## 版本格式

使用语义化版本：

- MAJOR：改变核心责任、授权或状态契约，可能不兼容。
- MINOR：增加向后兼容能力、协议层或 Adapter。
- PATCH：修正文案、测试、脚本和不改变语义的错误。

## 资产版本

以下资产分别记录版本：
- protocolVersion
- adapters（名称列表；各 Adapter 在自身文件中记录版本）
- schemaVersion
- workspaceVersion
- conformanceSuiteVersion

不得只用一个产品版本掩盖数据契约变化。

## v0.1 → v0.2 变化

新增：
- 产品谱系。
- 产品决策基线。
- 可追溯矩阵。
- 受治理演进循环。
- 摩擦与协议候选记录。
- 运行复盘模板。
- 版本和迁移规则。
- MingOS 验证计划。
- Core 与 Adapter 变更分流。

保持：
- “我在 / 你先做”用户语言。
- 七层工程结构。
- Governor / Builder / Verifier。
- 证据门禁。
- 生产与真实家庭数据禁区。

## 工作区迁移

v0.1 工作区增加：

```text
.creating-forward/
├── observations/
├── protocol-candidates/
├── reviews/
└── metrics/
```

已有 `state.yaml` 不删除。
迁移脚本只创建缺失目录和字段，不覆盖现有状态。

## v0.2 -> v0.4.0-dev

主库从 MingOS bootstrap 归一化为通用 Core：

- 顶层 Skill 名称改为 `creating-forward`。
- `projectId` 在初始化时根据目标目录生成。
- 单一 `adapterVersion` 改为 `adapters` 列表。
- `realFamilyDataAccess` 通用化为 `sensitiveDataAccess`。
- MingOS 专属规则只存在于 Adapter、bootstrap 和验证资产。
- 可变主库不保存发布 `MANIFEST.json`；发布时从已验证版本重新生成。

已有 v0.2 工作区运行：

```powershell
python scripts/migrate_workspace_v02_to_v03.py <project-path>
python scripts/validate_workspace.py <project-path>
```

迁移保留 `projectId`、历史事件和已有任务，只更新可观察的状态契约字段。
