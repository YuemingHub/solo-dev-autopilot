# Changelog

## 0.4.0-dev - 2026-07-28

### Added
- 项目更名为 Creating Forward（向未来去创造）。
- 根目录 MIT LICENSE。

### Changed
- 英文主名 `Creating Forward` → `Creating Forward`；中文口号「向未来去创造」。
- 工作区目录 `.creating-forward/` → `.creating-forward/`。
- Skill 名称 `creating-forward` → `creating-forward`。
- 版本线从 `0.4.0-dev` 演进到 `0.4.0-dev`。

### Preserved
- 产品原始意图、“我在 / 你先做”、证据门禁和状态恢复。
- Governor / Builder / Verifier 分工。
- MingOS 作为首个正式验证环境。

## 0.4.0-dev - 2026-07-28

### Added
- 唯一主开发库和 Git 安全边界。
- 通用包结构验证器与标准库测试套件。
- v0.2 工作区到 v0.3 开发契约的迁移脚本。
- 独立的 MingOS 符合性场景。
- 只读 JSON 任务图验证器、稳定错误码和确定性拓扑顺序。
- Core 与 MingOS 的结构化符合性场景目录及校验器。

### Changed
- 顶层 Skill 从 `creating-forward-mingos` 通用化为 `creating-forward`。
- 默认状态使用动态项目 ID、Adapter 列表和通用敏感数据授权字段。
- MingOS 专属事实、数据和 Foundation 约束收敛到 Adapter 与 bootstrap。
- 初始化和校验脚本接受任意项目路径。

### Removed
- 从可变主库移除旧 v0.2 发布清单；清单只在不可变发布包中生成。

### Preserved
- 产品原始意图、“我在 / 你先做”、证据门禁和状态恢复。
- Governor / Builder / Verifier 分工。
- MingOS 作为首个正式验证环境。

## 0.2.0 — 2026-07-27

### Added
- 正式产品谱系。
- 产品决策基线。
- 原意—协议—验证可追溯矩阵。
- 受治理的协议演进机制。
- Evolution Engineering。
- 运行观察、协议候选和 Run Review 模板。
- 成熟度模型。
- MingOS 真实验证计划。
- v0.1 工作区迁移脚本。
- 历史材料只读来源快照。

### Changed
- 核心 Skill 升级为 0.2.0。
- 工作区增加 observations、protocol-candidates、reviews、metrics。
- MingOS Adapter 增加运行后反向校准。
- Phase 0 增加运行复盘和协议候选提取。
- 强化 Core、Adapter、实现三层分流。

### Preserved
- “我在 / 你先做”。
- Requirement / Context / Prompt / Graph / Loop / Evidence / Authority。
- Governor / Builder / Verifier。
- 证据门禁和恢复机制。
- 生产、真实家庭数据、合并和外部操作的人工授权边界。
