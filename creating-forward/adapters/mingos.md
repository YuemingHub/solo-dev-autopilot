# MingOS 专属适配协议

Adapter 版本：`mingos-0.4.0-dev`  
依赖 Core：`creating-forward 0.4.0-dev`

本文件只对 MingOS 生效。加载顺序是先加载通用 `SKILL.md`，再加载本 Adapter；冲突时采用更严格的安全、证据和授权要求。本 Adapter 不得降低 Core 门禁。

## 1. 上下位关系

```text
Ming Foundation
  Charter / Kernel / RFC / Governance
              ↓
Co‑Visionary
  开发工作协议与 Agent 编排
              ↓
Ming-os
  Family Space / 家庭空间应用实现
```

Ming Foundation 决定不可违背的上位约束。
Co‑Visionary 决定开发过程怎样推进。
Ming-os 是被实现和验证的产品。

## 2. 启动前首读顺序

Agent 必须在仓库中查找并读取实际存在的文件，不得假设路径一定有效。

优先顺序：
1. README.md
2. AGENTS.md
3. 当前可信运行手册
4. Foundation 对齐或 implementation mapping 文档
5. Git、PR、部署和回滚安全文档
6. 当前状态与开放 PR
7. 当前任务相关代码和测试
8. Ming Foundation 对应上游条款

如 README 指向的文件不存在，记录为事实漂移，不自行伪造内容。

## 3. MingOS 不可丢失边界

- 生命先于系统。
- 理解先于建议。
- 关系先于方法。
- 观察与事实先于推断。
- 事实、观察、假设、模式、判断和决定必须可区分。
- AI 不替代人的决定与关系。
- 家长和孩子都拥有确认、修正、拒绝与退出的权利。
- 安全升级必须可追溯。
- 失败、未知、争议和风险不得被隐藏。
- 真实家庭数据不得进入开发 Agent 普通上下文。

## 4. 当前默认开发边界

本节的“默认允许”不是独立授权来源。每个动作仍必须同时满足 Core 的 `authorizationProfile`、当前 `delegationMode` 和目标工作区范围；本 Adapter 只能进一步收紧，不能扩大已有授权。

默认禁止：
- 部署 production。
- 修改 production 分支指针。
- 自动合并 PR。
- 连接或修改真实家庭数据库。
- 读取真实家庭日志、备份、会话和密钥。
- 修改 ymai.me 独立企微渠道。
- 将开发 Skill、Agent 状态或工作台脚本打入产品运行时。
- 将当前实验 UI、画像或分类误称为最终标准。

默认允许：
- 读取仓库。
- 读取上游规范。
- 创建独立开发分支。
- 修改开发文档、测试和授权范围内代码。
- 使用合成数据。
- 运行本地测试和构建。
- 创建 Draft PR 或补丁。
- 记录决策和证据。

## 5. 分支策略

首次运行必须核实实际分支策略。
在未完成事实核查前，不得假设 master、production 或某个 codex 分支是唯一可信基线。

默认做法：
- 从核实后的开发基线派生 `codex/creating-forward-<task>`。
- 不直接推送 master 或 production。
- 不自动合并。
- PR 默认 Draft。
- 提交必须按明确文件清单处理，禁止无审查的全量 stage。

## 6. 测试策略

优先使用仓库已有测试。
Agent 必须从 package.json、运行手册和任务相关测试中确定真实命令。

至少分为：
- 结构与边界测试。
- Foundation / governance 契约测试。
- 安全门测试。
- 数据权利与记忆测试。
- 前后端构建。
- 双端口和部署边界。
- 任务新增的窄回归测试。

实时模型测试不得作为唯一发布证据。
涉及真实外部模型时，必须说明不确定性和可重复性边界。

## 7. 首次适配任务

第一轮只做 Phase 0：
- 当前事实核查。
- 文档入口核查。
- 分支与 PR 图谱。
- 运行和部署基线。
- 已知债务与冲突。
- 自主开发边界。
- `.creating-forward/` 初始化。
- 恢复测试。

不得顺手开发新产品功能。


## 8. 运行后必须反向校准

每一个 MingOS 开发运行结束后：

1. 填写 `templates/run-review.md`。
2. 将代码问题与协议问题分开。
3. 项目特有问题优先修复 MingOS 或 Adapter。
4. 只有可复现的通用问题才能进入 `protocol-candidates/`。
5. Agent 可以创建 Core 候选 Draft，但不得自行发布。
6. 所有候选必须追溯到 `docs/PRODUCT_LINEAGE.md` 和 `docs/TRACEABILITY_MATRIX.md`。
