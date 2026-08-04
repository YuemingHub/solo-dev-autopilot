# MEMORY.md — 长期记忆

## 三仓库联动项目（2026-08-03 启动）

目标：solo-dev-autopilot（方法论）↔ Ming-os-production（真实项目）↔ Ming-os-understanding（理解地图）三者循环验证、一起迭代。

| 角色 | 路径 | 远程 |
| --- | --- | --- |
| ① 方法论引擎 | `F:\project\solo-dev-autopilot` | https://github.com/YuemingHub/solo-dev-autopilot |
| ② 真实项目 | `F:\Program\Ming-os-production` | git@github.com:YuemingHub/Ming-os.git（私有） |
| ③ 理解地图 | `F:\Program\Ming-os-understanding` | git@github.com:YuemingHub/Ming-os-understanding.git |

- 备份：`F:\Program\Ming-os-production - 副本`（git 操作前已有，可放心改动主目录）

## 联动规则（已与用户确认）

- **9 步闭环**：进场 → 地图(context-map) → 规划(task-planner) → 开发 → 验证(test-runner+CI) → 审查(code-review) → 提交(commit-helper+PR) → 记录(更新 understanding) → 回馈(autopilot 缺口清单)
- **档位**：production 档（P0 门禁 + 全量预检），红线不松
- **粒度**：一个 issue 一轮循环
- **地图生成**：用 OpenSquilla 自己的工具自动生成/刷新，不等 Trae
- **执行分工**：agent 自主执行到"开发分支提交 / 提 PR"；**发布类操作必须用户拍板**（production 分支合并、部署服务器、碰 ymai.me、改变 NO-GO 状态）

## Ming-os 红线（任何时候不得违反）

1. 正式启动只用 `npm run start:dual`（单进程双端口，sql.js 整库单进程）
2. 不碰 ymai.me 渠道（企微真实家长独立后端）
3. 不公开收费；`CURRENT_RELEASE_STATUS.md` 为 NO-GO 时不得绕过
4. understanding 仓库严禁放真实家庭数据、密钥、.env、聊天记录
5. 开发走 `codex/<task>` 分支；正式发布只走 production 分支或 release-* 标签

## 当前进度（2026-08-04）

- **试点第 1 轮完成（2026-08-04）**：Mingos 运行态产物解除跟踪收尾。
  - 候选任务大部分已在 ad17094 完成（agent/chats/jobs 解除跟踪）；
  - 本轮补齐剩余：`reports/flywheel/` 53 个 session JSON `git rm --cached`，分支 `codex/fix-flywheel-untrack-v2`，Draft PR #110；
  - 发现旧分支 #109 混删活源码 `test-llm-fallback.js`（被 `test:llm-fallback` 引用），未沿用，建议关闭 #109；
  - understanding 仓库已记录（PROJECT_STATE.md 决策表），方法教训沉淀至 `memory/2026-08-04.md`。

## 当前进度（2026-08-03）

- **Step 0（git 打通）✅ 完成**：
  - `F:\Program\Ming-os-production` 已 init + 关联远程 `https://github.com/YuemingHub/Ming-os.git`（SSH 大包传输卡死，改 HTTPS；网络对 GitHub 大传输不稳定，需重试或代理）
  - 本地分支 `production` @ `1500317`（本地快照 commit，父节点 = 远程 production `55802b8`），工作区干净
  - 因网络只能浅拉取（depth=1）+ 曾触发 partial clone（blob:none），已设 `gc.auto=0` 避免 repack 读缺 blob 失败；本地 blob 由 `git add -A` 从磁盘重建，日常开发/提交/推送新分支可用
  - 本地 git 身份临时设为 `ming-os-local <ming-os-local@localhost>`（repo-local），可改
- **对齐状态（本地 vs 远程 production@55802b8）**：本地多 `UNDERSTANDING_INDEX.md`；远程多 63 个误提交的运行时文件（chats.json/agent.json/jobs.json/reports/flywheel/*/knowledge/fki/compiled/* 等）；`.gitignore` 有差异
- **发现 1（根因）**：远程 `.gitignore` 是 **UTF-16 LE（103 行旧版）**，git 读不懂 → 忽略规则失效 → 63 个运行时文件被误提交。本地是 UTF-8 117 行新版（含 chats.json/agent.json/jobs.json/.understand-anything 规则），领先远程且从未推送
- **发现 2（缺口）**：`UNDERSTANDING_INDEX.md` 不在远程 production 树里（理解仓库 README 声称主项目有该索引）
- **发现 3**：production 自带 17 个 .claude/skills + 2 个 CI workflow + AGENTS.md 自主契约（可自主做到 Draft PR）；autopilot 安装应以流程整合为主，避免整包复制冲突

## 候选首个试点任务（已完成，2026-08-04）

「修复 .gitignore 编码为 UTF-8 + 采用本地 117 行新版 + `git rm --cached` 解除 63 个误跟踪运行时文件」——已大部分完成：agent/chats/jobs 已解除（ad17094），flywheel 53 个已解除（PR #110）；剩余 knowledge/fki/compiled 是否入库需按知识治理决策，不沿用 #109 一并删除。

---

## 2026-08-03 补充：方法论仓库复核（v2.3.3）

- 独立复核确认：Phase 1-4 全部完成；CI 实测连续 3 次全绿（docs/verification.md §3）；评分 9.0 有据可查
- 修复 3 处残留：README/getting-started 的 `YOUR_USERNAME` 占位符 → YuemingHub；scoring.md "CI 未实际跑过" 过时表述；docs/EVOLVE_CHANGELOG.md 缺失
- 新增 `scripts/sync-skills.py`：官方 `.claude/skills/` → 平铺 `skills/` 兼容层单向同步（`--check` 供 CI），ci-self-check.sh 增加第 4 段
- 兼容层归一化：7 个 v1 格式平铺文件升级为官方内容，补齐 4 个缺失文件，13/13 与官方一致
- ⚠️ 路径注意：`F:\<ZWNJ>project<ZWNJ>\solo-dev-autopilot` 是过时副本（停在 d34e445，Phase 2 之前），勿再使用，可删除；规范路径 = `F:\project\solo-dev-autopilot`
