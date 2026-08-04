# 全局规则:新手自动驾驶开发流程(AGENTS.md)

> 本文件让 Agent 在**任何项目**里自动走「侦测 → 搭建 → 开发 → 验证 → 记忆」闭环,新手零手工配置。
> 依据:《深入理解 AI Agent》(github.com/bojieli/ai-agent-book)第 1/2/3/5 章实践原则。
> 配套 skill 合集(全局,已扫描加载):env-detect、env-setup、project-scaffold、dev-loop、task-memory、harness-guard、book-experiments。

## 触发规则(按会话阶段)

### 会话开始 / 进入新项目目录
1. 若 `.agent-memory/memory.md` 存在 → 读摘要注入上下文
2. 若 `.agentenv.json` 不存在或项目结构变化 → 自动调用 Skill(env-detect)
3. 若项目是全新/空目录 → 提示用户是否走 Skill(project-scaffold)
4. 若 `.agentenv.json` 显示 `runtimes.missing` 非空 → 自动调用 Skill(env-setup)补齐

### 用户发起开发任务(写代码/加功能/修 bug)
1. 确认环境就绪(读 .agentenv.json;未就绪先 env-setup)
2. 遵循项目 AGENTS.md(项目级指令优先于本文件)
3. 代码改动后 → 自动调用 Skill(dev-loop)验证;测试通过前**不得**声称任务完成
4. 任务结束 → 自动调用 Skill(task-memory)沉淀

### 任务声称完成 / 提交前
- 强制 Skill(dev-loop)完整验证;未通过不许报告"完成"

### 执行任何 shell 命令 / 写文件前
- 危险操作(删除、覆盖未读、全局安装、force push 等)→ 先按 harness-guard 分级,高风险询问用户

### 失败处理(全局熔断)
- 同一命令连续失败 3 次 → 停止自动重试,汇报用户 + 写入 `.agent-memory/troubleshooting.md`
- 不要把「环境类失败」当代码 bug 修;转 Skill(env-setup)

### 用户提到《深入理解 AI Agent》或想跑书中实验
- 自动调用 Skill(book-experiments):克隆仓库、按章装依赖、跑通实验

## 自动化程度(用户已确认)

- **低风险操作:全自动**(依赖安装、配置生成、构建测试、自动修复、提交)
- **高风险操作:先询问**(删除、覆盖未读文件、全局安装、git 历史改写、推送远程)
- 系统级运行时(Python/Node/Go 等)缺失时**允许自动安装**(winget/官方安装器),装完重新验证
- 语言覆盖:Python / Node.js(前端) / Go / Rust / Java 常用全栈

## 汇报风格

- 面向新手,中文,不用术语堆砌
- 每次汇报包含:做了什么 / 结果(验证输出)/ 下一步建议
- 不用 emoji 堆砌;关键结论给短列表

## 禁止事项

- 不把真实密钥写入代码、日志、记忆(只能进 .env 且 .env 不入库)
- 不猜测项目类型;判定不了就如实报告并询问
- 不修改锁文件版本升级依赖(除非用户要求)
- 不在未验证时宣称任务完成
