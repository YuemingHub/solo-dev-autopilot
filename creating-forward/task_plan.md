# Creating Forward 主开发库归一化计划

## 目标

将 `D:\LifeOs\Creating Forward` 建设为唯一主开发库，以 bootstrap v0.2 为经过验证的内容基线，保留历史来源，并把平台无关 Core 与 MingOS 项目 Adapter 分层。

## 阶段

- [x] 阶段 1：核对早期工作区、v0.1、v0.2 的来源关系和完整度
- [x] 阶段 2：批准“主库位置 + v0.2 内容基线 + 历史快照只读”设计
- [x] 阶段 3：迁入 v0.2 资产并初始化 Git 主库
- [x] 阶段 4：将顶层 Skill、入口和脚本通用化
- [x] 阶段 5：保留 MingOS Adapter、bootstrap 和验证计划的独立边界
- [x] 阶段 6：增加包级与工作区级自动验证
- [x] 阶段 7：执行自审、全量验证并固化下一迭代入口
- [ ] 阶段 8：定义任务图 JSON 契约与稳定错误语义
- [ ] 阶段 9：实现任务图引用、重复依赖与环检测
- [ ] 阶段 10：将符合性场景升级为可执行结构评估
- [ ] 阶段 11：独立审查、全量验证并准备 MingOS Phase 0

## 固定决策

- 唯一主开发目录：`D:\LifeOs\Creating Forward`
- 内容起点：`creating-forward-mingos-bootstrap-v0.2`
- `08_迭代日志` 下的 v0.1/v0.2 保持不可变历史快照
- 通用 Core 不绑定 MingOS、模型、厂商或特定工具
- MingOS 只通过 `adapters/mingos.md`、`bootstrap/` 和验证计划接入
- 项目工作状态使用 `.creating-forward/`，不依赖对话记忆
- 不在本轮引入 MCP、Web 应用、数据库或云同步
- 未经用户单独要求，不创建 Git commit、不发布、不部署
- 任务图验证器只读 JSON，不执行任务、不自动修复、不引入第三方依赖
- 符合性评估只验证确定性结构规则，不伪装成 LLM 行为已通过

## 验收标准

- 主目录包含可加载的通用 `SKILL.md`
- 早期 PRD 和工作记录有明确只读来源位置
- MingOS 专属规则不再出现在 Core 使命和通用入口中
- 初始化脚本可对任意项目建立 `.creating-forward/`
- 包结构、JSON Schema、初始化和工作区校验均有自动测试
- Git 已初始化，工作树内容可审查，未自动提交
- README 明确开发入口、架构边界和验证命令

## 最终验证

- `python -m unittest discover -s tests -v`：25/25 通过
- `python scripts/validate_package.py`：`PACKAGE VALIDATION: PASSED`
- 全部 `scripts/*.py` 与 `tests/*.py`：`py_compile` 通过
- 通用工作区初始化与校验：通过
- `mingos` Adapter 工作区初始化与校验：通过
- 最终独立代码审查：`APPROVE`，无 Critical/Important 阻塞项

## 错误记录

| 时间 | 错误 | 根因 | 处理 |
|---|---|---|---|
| 2026-07-28 | `validate_workspace.py --help` 报缺少文件 | 脚本只接受目标路径，把 `--help` 当目录 | 已读取脚本并按位置参数执行 |
| 2026-07-28 | Git 状态探测出现 PowerShell 空管道错误 | `foreach` 输出直接接管道的语法组合错误 | 改为先收集 `$rows` 再格式化 |
| 2026-07-28 | `coze code --help` 刷新令牌返回 `slow_down` | Coze OAuth 刷新限流 | 本地开发继续，Coze 通道延后重试 |
| 2026-07-28 | 单元素哈希比较被 PowerShell 展开为字符 | `@(@(...))` 在该表达式中被解包 | 改为两个显式路径直接比较，确认哈希一致 |
| 2026-07-28 | Coze message send 返回后触发 libuv assertion | Windows CLI 进程退出阶段断言；消息已返回 `sent` | 保留 project ID，稍后用单次 status 查询终态，本地主线继续 |
