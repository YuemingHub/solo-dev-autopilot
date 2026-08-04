# Creating Forward 主开发库设计

## 1. 目标

将早期产品工作区和后续 bootstrap 交付包归并为一个可持续开发、可验证、可发布的主库，同时保留全部产品来源和版本谱系。

## 2. 选定方案

采用“主库 + 通用 Core + Adapter + 只读历史”的结构：

```text
D:\LifeOs\Creating Forward
├── SKILL.md                 通用行为契约
├── protocol/               平台无关详细协议
├── schemas/                通用状态和任务契约
├── templates/              通用工作区模板
├── scripts/                初始化与验证工具
├── adapters/               项目或平台差异
│   └── mingos.md
├── bootstrap/              MingOS 首次运行入口
├── plans/                  真实验证计划
├── evals/                  协议符合性场景
├── tests/                  自动结构和脚本测试
├── docs/                   产品、架构、版本与治理文档
└── sources/                只读历史来源
```

## 3. 备选方案

### 方案 A：继续在 v0.2 快照目录开发

实现成本最低，但会把发布快照和开发工作树混在一起，后续 v0.3 无法清晰区分来源，因此不采用。

### 方案 B：保留早期工作区，只引用 v0.2

不会复制文件，但主库缺少完整可执行资产，跨 Agent 使用时依赖外部路径，不具备可移植性，因此不采用。

### 方案 C：归并到正式主库

将 v0.2 迁入正式目录，历史来源保留，顶层协议通用化，MingOS 作为 Adapter 和验证实例存在。该方案边界最清晰，采用此方案。

## 4. 组件边界

### Core

由 `SKILL.md`、`protocol/`、`schemas/`、`templates/` 和通用脚本组成。Core 只定义需求、上下文、任务图、执行循环、证据、授权、恢复和受治理演进，不出现 MingOS 专属使命或数据边界。

### Adapter

`adapters/mingos.md` 保存 Ming Foundation、家庭与儿童数据、生产分支和专业主观判断等专属约束。Adapter 可以收紧 Core，不得降低 Core 的安全和证据要求。

### Validation Program

`bootstrap/` 与 `plans/MINGOS_PHASE0_PLAN.md` 负责把 Core 应用于 MingOS。它们是首个真实验证项目的入口，不是通用安装入口。

### History

`sources/history-2026-07-27/` 保存早期 PRD、发现、进度和任务计划。历史材料不得作为当前执行状态，也不得覆盖当前产品决策基线。

## 5. 数据流

```text
用户目标
  -> 通用 Core 建立需求和授权基线
  -> 可选 Adapter 增加项目约束
  -> 初始化目标项目的 .creating-forward/
  -> 任务执行、证据验证、状态恢复
  -> Run Review
  -> 协议候选 Draft
  -> 人工审查后进入后续版本
```

## 6. 错误处理

- 目标项目路径不存在时，初始化脚本必须失败且不创建旁路目录。
- 工作区缺少必需文件、JSONL 损坏或出现疑似敏感文件时，校验必须失败。
- 包结构缺失、Schema 不是合法 JSON、顶层 Skill 仍绑定具体项目时，包级校验必须失败。
- 协议候选不得自动覆盖正式 Core。

## 7. 验证策略

- 包级静态校验：目录、必需文件、frontmatter、JSON Schema、Core/Adapter 边界。
- 工作区闭环测试：临时目录初始化后执行 validator。
- 幂等测试：重复初始化不覆盖已有状态。
- 迁移测试：v0.1 工作区升级时保留原状态并增加 v0.2 目录。
- Python 语法检查：所有脚本执行 `py_compile`。

## 8. 非目标

- 不实现 MCP 服务。
- 不实现 Web 管理台。
- 不实现云同步和账号体系。
- 不修改 MingOS 产品代码。
- 不发布或部署。

## 9. 成功标准

- 新 Agent 只读取主库入口即可理解通用协议和 Adapter 关系。
- 通用 Skill 可用于非 MingOS 项目。
- MingOS 仍可通过专属入口执行 Phase 0。
- 自动验证可证明包结构和工作区生命周期有效。
