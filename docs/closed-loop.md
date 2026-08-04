# 三仓库联动 · 9 步闭环（v2.4 固化为产品文档）

> 2026-08-03 起，本仓库（方法论）与真实项目、理解仓库三仓联动验证：
> 方法论仓库定义流程 → 真实项目按流程开发 → 理解仓库记录状态与产物 → 实战缺口回灌方法论。
> 本文档把这套实践固化为正式流程。

## 角色

| 角色 | 仓库 | 职责 |
|---|---|---|
| ① 方法论 | solo-dev-autopilot（本仓库） | 流程、Skill、模板、评分、CI 模板 |
| ② 真实项目 | 你的项目（如 Ming-os-production） | 实际开发对象，走 `codex/<task>` 分支 |
| ③ 理解仓库 | 你的理解仓库（如 Ming-os-understanding） | 状态快照、架构地图、UA 产物、交接入口 |

## 9 步闭环

| 步 | 名称 | 做什么 | 产出 | 责任人 |
|---|---|---|---|---|
| 1 | 进度 | 读 CURRENT_STATE / PROJECT-MEMORY / SESSION_DRIVER / issue | 本轮目标（1-3 件） | agent |
| 2 | 地图 | context-map / understand 工具生成或刷新代码地图 | CODEMAP / knowledge-graph | agent |
| 3 | 规划 | task-planner 拆 MVP + 小任务，防漂移 | 任务清单 | agent + 用户确认 |
| 4 | 开发 | 一次一个小任务，最小改动 | 代码改动 | agent |
| 5 | 验证 | test-runner + CI 门禁（覆盖率基线） | 测试通过记录 | agent |
| 6 | 审查 | code-review P0-P3 + 安全审查 | 审查结论 | agent |
| 7 | 提交 | commit-helper + `codex/<task>` 分支 + Draft PR | Draft PR | agent（合入 = 用户） |
| 8 | 记录 | 更新理解仓库状态/产物 | 状态快照 | agent |
| 9 | 回响 | 把实战缺口反馈给方法论仓库 | 下一轮改进项 | agent + 用户 |

## 档位与红线

- 档位：`toy`（学习）/ `team`（正常开发）/ `production`（发布级），严格度随 `.autopilot-mode` 调整。
- 红线（示例，按真实项目 AGENTS.md 落地）：
  - 发布类操作（合并 production、部署服务器、改密钥/环境/真实数据）必须用户拍板；
  - 测试通过 ≠ 可以放行；真实发布状态以项目状态卡（如 `CURRENT_RELEASE_STATUS.md`）为准；
  - 理解仓库严禁放真实数据/密钥/聊天记录；
  - 中文 commit 用 `git commit -F <UTF-8无BOM文件>`（Windows PowerShell 5.1）。

## 粒度：一个 issue 一轮

一个 issue / 一个明确任务 = 一轮闭环。完成后回到第 1 步选择下一轮。
第 9 步「回响」是闭环的价值所在：方法论仓库必须从真实项目中长出下一轮改进，而不是闭门造车。
