# AGENTS.md — Solo Dev Autopilot 统一运行契约（三合一）

> 本文件是三合一后的**全局规则入口**：任何 AI 工具（Claude Code / Codex / Cursor / Cline / ohmyagent 等）进入本仓库或把它作为项目根目录时，先读本文件。
> 三层架构一句话：**协议层定纪律（creating-forward 技能）、harness 层管环境与验证、交付层完成产品闭环**。

## 三层架构

| 层 | 位置 | 职责 | 入口 |
|---|---|---|---|
| ① 协议层 | `.claude/skills/creating-forward/SKILL.md` | 需求基线、上下文包、任务图、执行循环、证据验证、授权边界、中断恢复 | 技能文件本身 + `scripts/cf_*.py` 校验链 |
| ② Harness 层 | 7 个环境/验证 Skill | 侦测 → 搭建 → 脚手架 → 开发循环 → 记忆 → 护栏 | `.claude/skills/` 中的 env-* / dev-loop / task-memory / harness-guard / project-scaffold / book-experiments |
| ③ 交付层 | 13 个交付 Skill + templates/ + configs/ | 规划 → 审查 → 测试 → 提交 → 部署门禁 → 上线预检 → 9 步闭环 | `.claude/skills/` 其余 Skill + `docs/closed-loop.md` |

共 **21 个官方 SKILL.md**（`.claude/skills/`，唯一事实源）；平铺兼容层 `skills/*.md` 由 `scripts/sync-skills.py` 单向同步，不要手改。
辅助资产统一归位：协议状态契约 `configs/schemas/`、模板 `templates/creating-forward/`、场景目录 `evals/`、适配器 `adapters/`、单测 `tests/`、自定义 agent `configs/agents/`。

## 触发时序（按会话阶段）

### 会话开始 / 进入新项目目录
1. 若项目有 `.agent-memory/memory.md` 或 `PROJECT-MEMORY.md` → 读摘要注入上下文
2. 若 `.agentenv.json` 不存在或项目结构变化 → env-detect
3. 若是全新/空目录 → 询问是否 project-scaffold
4. 若环境缺运行时（runtimes.missing 非空）→ env-setup 补齐
5. 正式任务开始前按 creating-forward 协议形成**需求基线**（problem / deliverables / successCriteria / outOfScope / approvalStatus），不清楚时每次只问一个最影响方向的问题

### 用户发起开发任务（写代码/加功能/修 bug）
1. 确认环境就绪（读 .agentenv.json；未就绪先 env-setup）
2. task-planner 拆解（防漂移）；复杂任务按 creating-forward 建任务图（有依赖、有完成标准、有验证方法）
3. 代码改动后 → dev-loop 验证；**测试通过前不得声称任务完成**
4. 提交前 → code-review（P0-P3）+ commit-helper；发布类操作过 deploy-gate
5. 任务结束 → task-memory 沉淀 + context-map 更新

### 危险操作前
- 删除、覆盖未读文件、全局安装、force push、`DROP`、改 PATH/注册表 → harness-guard 分级，高风险先按「做什么 / 影响范围 / 可逆性」三要素询问用户
- 权限唯一事实源：`configs/permissions.json`（safe 自动放行 / ask 确认 / danger 拒绝+确认）；档位随 `.autopilot-mode`（toy / team / production）

### 失败处理（全局熔断）
- 同一命令连续失败 3 次或累计 5 次 → 停止自动重试，汇报「目标 / 做了什么 / 失败输出 / 建议路径」，写入 `.agent-memory/troubleshooting.md`
- 环境类失败转 env-setup，不当代码 bug 修
- 连续两次同类失败 → 阻塞或改路，不空转

## 红线（任何时候不得违反）

1. **未执行不得声称执行；未验证不得声称完成**（证据：命令+退出码、测试/构建结果、文件结构校验、用户验收；"应该可以"不算证据）
2. 发布类操作必须用户拍板：合并 production、部署服务器、改密钥/环境/真实数据、创建 release
3. 密钥不进代码、不进日志、不进记忆、不进 git（只进 .env，且 .env 不入库）
4. 用户离开不扩大授权；"你先做"不等于无限授权
5. 不伪造文件、测试、截图或外部结果；不隐藏失败与风险
6. 中文 commit 用 `git commit -F <UTF-8无BOM文件>`（Windows PowerShell 5.1 的 -m 中文会变 ?，见 docs/newbie-pitfalls.md 坑 20）

## 9 步闭环（三仓联动 / 单项目同样适用）

进度 → 地图(context-map) → 规划(task-planner) → 开发 → 验证(test-runner/dev-loop) → 审查(code-review) → 提交(commit-helper + Draft PR) → 记录(状态快照) → 回响(缺口回灌方法论)。
详见 `docs/closed-loop.md`；一个 issue = 一轮闭环。

## 汇报风格

- 面向新手、全程中文、不堆术语；不堆 emoji，关键结论给短列表
- 只在有意义变化时汇报：`已完成：一句话 / 现在：一句话 / 需要你：仅在确有关键决定时出现`
- 每次汇报包含：做了什么 / 结果（验证输出）/ 下一步建议

## 仓库自身维护

- 修改 Skill 只改 `.claude/skills/`，然后 `python scripts/sync-skills.py` 重新生成平铺层
- 仓库自检：`bash scripts/ci-self-check.sh`（JSON / SKILL.md frontmatter / shell 语法 / 平铺层一致性 / creating-forward 包校验）
- creating-forward 协议验证：`python scripts/cf_validate_package.py` 与 `python -m unittest discover -s tests -v`
- 不改锁文件做版本升级（除非用户要求）；不猜测项目类型，判定不了就如实报告
