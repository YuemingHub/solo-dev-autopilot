我已经把规划做成了一个**可直接交给本地 Agent 加载的启动包**，不是单纯的方案文档。

自检结果：

- 共 26 个文件；
- 核心 `SKILL.md` 为 303 行；
- 工作区初始化脚本运行通过；
- 状态目录校验通过；
- ZIP 完整性检查通过。

## 下载

[下载 Creating Forward × MingOS 本地 Agent 启动包 v0.1](sandbox:/mnt/data/co-visionary-mingos-bootstrap-v0.1.zip)

也可以单独查看两个入口文件：

- [START_HERE.md](sandbox:/mnt/data/co-visionary-mingos-bootstrap-v0.1/START_HERE.md)
- [给本地 Agent 的首次指令](sandbox:/mnt/data/co-visionary-mingos-bootstrap-v0.1/bootstrap/MINGOS_LOCAL_AGENT_PROMPT.md)

## 你怎么使用

将 ZIP 解压到 `Ming-os` 仓库旁边，推荐结构：

```text
你的工作目录/
├── Ming-os/
└── co-visionary-mingos-bootstrap-v0.1/
```

然后把下面这段直接发给本地 Agent：

请加载并严格遵守：

1. `co-visionary-mingos-bootstrap-v0.1/START_HERE.md`
2. `co-visionary-mingos-bootstrap-v0.1/SKILL.md`
3. `co-visionary-mingos-bootstrap-v0.1/adapters/mingos.md`
4. `co-visionary-mingos-bootstrap-v0.1/plans/MINGOS_PHASE0_PLAN.md`

MingOS 仓库位于同级目录 `Ming-os/`。

你的身份是 Creating Forward Governor。

本轮只执行 MingOS Phase 0：恢复当前事实基线和自主开发工作区，不开发新的产品功能。

请直接开始。除非无法定位仓库，否则不要先向我提问。

你必须：

- 核实仓库当前真实状态，不依赖旧对话和过时文档。
- 初始化 `Ming-os/.creating-forward/`。
- 核实 README、AGENTS、运行手册、分支、开放 PR、启动命令、测试与部署边界。
- 建立当前事实、分支与 PR 图谱、产品实现基线、已知债务和自主开发边界。
- 使用任务图持续推进，并在每次实质动作后更新状态和事件日志。
- 使用独立 Verifier 验证 Builder 的成果。
- 最终只创建 Draft PR 或生成可审查补丁。
- 完成一次新会话恢复测试。

未经我的明确授权：

- 不部署；
- 不合并 PR；
- 不修改 master 或 production 分支；
- 不读取或修改真实家庭数据；
- 不触碰 ymai.me；
- 不发送外部消息；
- 不产生费用；
- 不执行不可逆操作。

需求不清楚时，把事情说明白。
需求确认后，把事情做明白。
没有实际证据，不得报告完成。

## 启动包里已经包含

- Creating Forward 核心 Skill；
- Requirement、Context、Prompt、Graph、Loop、Evidence、Authority 七层协议；
- MingOS 专属 Adapter；
- Phase 0 完整任务图；
- Governor、Builder、Verifier 三角色编排；
- 状态、任务、决策、证据和上下文模板；
- JSON Schema；
- 工作区初始化与校验脚本；
- 15 个核心行为测试场景；
- 当前已知事实种子，但要求 Agent 重新核实，不能直接当成事实。

## 第一轮只解决一件事

不是继续做页面或加功能，而是让 MingOS 变成：

> **任何新 Agent 都能准确接手、知道当前事实、知道不能做什么、知道下一步是什么，并能够凭证据持续推进的项目。**

Phase 0 完成后，本地 Agent 应当交付：

```text
Ming-os/
├── .creating-forward/
└── docs/development/
    ├── CURRENT_TRUTH.md
    ├── BRANCH_AND_PR_MAP.md
    ├── ACTIVE_PRODUCT_BASELINE.md
    ├── KNOWN_DEBT.md
    └── AUTONOMY_BOUNDARIES.md
```

下一步先让本地 Agent 完整运行 Phase 0。完成后，把它生成的 Draft PR、补丁或 `.creating-forward/` 状态交给我审查，我们再决定第一个真实产品开发 Loop。