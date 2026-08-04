# 可追溯矩阵

每一条核心协议规则必须能够回答三个问题：

1. 它来自哪一个原始产品需要？
2. 它在当前协议中如何实现？
3. 它在 MingOS 中用什么证据验证？

| 原始意图 | 协议实现 | MingOS 验证证据 |
|---|---|---|
| 用户不应先学会全部 AI 工具 | Governor 负责任务路由和能力检查 | 用户只给目标，Agent 能选择现有测试、文件和角色 |
| 模糊想法不能直接执行 | Requirement baseline + confirming gate | 新需求未确认时不进入业务实现 |
| 少人为干预 | delegated 默认处理低风险决定 | 记录用户被询问次数及其必要性 |
| 用户仍保留方向决定权 | paused_for_human + decision record | 核心目标、伦理、生产动作均有人工决定 |
| AI 不得假装完成 | evidence gate | 任务 completed 必须关联测试或审查证据 |
| 长任务可恢复 | state snapshot + event log | 新会话只读工作区即可准确续接 |
| 多 Agent 不应失控 | Governor/Builder/Verifier 分工 | 独立 Verifier 能发现越界和假完成 |
| 不绑定单一平台 | Core + Adapter | 至少两个本地 Agent 环境完成同一场景 |
| 技术不能覆盖生命逻辑 | MingOS Adapter + Foundation constraints | 实现审查包含主体性、安全和数据权利边界 |
| 系统能够学习 | governed evolution loop | 真实失败形成候选补丁和回归测试，而非直接改规则 |

## 使用规则

- 新增核心规则时必须增加一行。
- 如果找不到原始意图来源，规则不得进入 Core，只能作为项目 Adapter 或实验规则。
- 如果没有可验证方式，规则只能标记为 aspirational，不得称为已实现。
