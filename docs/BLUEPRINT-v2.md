# Solo Dev Autopilot v2 开发蓝图

> 定位：**中文新手 + 完整交付闭环 + 生产可用** 三合一
> 原则：不重新造轮子。GitHub 已有的直接用，我们只做差异化。
> 创建日期：2026-08-03 | 状态：待执行

---

## 〇、需要你拍板的 6 个决策

| # | 决策项 | 我的建议 | 需要你定 |
|---|--------|---------|---------|
| D1 | **和 superpowers 的关系** | 硬依赖——安装脚本自动装 superpowers，我们的 skill 是它的中文增强层 | 接受"用户需先装 superpowers"这个前提吗？ |
| D2 | **默认技术栈** | 保留 Bun+Hono+React+Supabase 作为"默认解"（不是"最优解"），加"可替换"出口；第二期加国内生态栈 | 第一期就要加小程序/国内栈？还是先做好 Web 全栈？ |
| D3 | **autopilot 边界** | 参照 alfred-dev：开发阶段可自动推进，**生产部署永远要人工确认** | 同意"部署不自动"这条红线吗？ |
| D4 | **工具适配优先级** | v2 先做 Claude Code 全适配（plugin marketplace 原生支持），其他工具标注"社区适配中" | 只用 Claude Code？还是必须同时支持多个？ |
| D5 | **版本策略** | v2.0 breaking change——旧的自定义 frontmatter 和 SKILL.md 不兼容，并存只会让用户困惑，一次性切干净 | 同意 breaking change？还是要渐进式？ |
| D6 | **ZWNJ 路径** | 当前目录名是零宽字符包着的 project，所有文件工具失效。你在 Windows 上手动改名为 project，或我们另建一个正常路径的 clone | 你来改目录名？还是我们另起？ |

---

## 一、战略定位

| 维度 | 我们的占位 | 竞品现状 |
|---|---|---|
| **中文新手** | 第一次用 AI 编程的人，需要被引导、被保护 | superpowers-zh 只翻译技能不做引导；superpowers 是英文开发者向 |
| **完整交付闭环** | 想法→拆解→开发→审查→部署→运维，全程不断链 | alfred-dev 有质量门但偏工程向，superpowers 偏方法论不做部署 |
| **生产可用** | 测试/CI/权限/可观测性/记忆裁剪，不是玩具 | 没有任何竞品同时做"新手友好"和"生产可用" |

**一句话定位**：让第一次用 AI 写代码的中文用户，能交付一个真正能上线、能维护、能排查问题的产品。

---

## 二、核心原则

1. **不造轮子**：官方标准、成熟方法论、现成工具，直接用，不重写
2. **接标准**：skill 格式用 Anthropic 官方 SKILL.md schema，让 Claude Code 原生可安装
3. **生产化优先**：每个新功能先问"生产环境里怎么跑"，再问"新手怎么用"
4. **薄封装**：superpowers 方法论作为上游依赖，我们的 skill 是薄封装 + 中文新手场景适配
5. **可验证**：每个改动有测试、有质量门、有回滚路径

---

## 三、架构分层

### 层 1：直接用（不写代码，只配置引用）

| 组件 | 来源 | Stars | 用途 |
|---|---|---|---|
| skill 格式标准 | anthropics/skills | 165k | 所有 skill 必须用官方 SKILL.md schema |
| 开发方法论 | obra/superpowers | 265k | brainstorm→plan→TDD→review→finish 全流程 |
| MCP 服务器清单 | punkpeye/awesome-mcp-servers | 91k | 替换手写的 4 个 server 配置 |
| 多工具适配模式 | wshobson/agents | 38k | 参考其 marketplace 安装模式 |

### 层 2：薄封装（基于上游 + 场景适配）

| 组件 | 上游 | 我们的封装 |
|---|---|---|
| task-planner | superpowers brainstorming | 加中文新手引导问题、30分钟任务拆解、防漂移 |
| code-review | alfred-dev evidence guard | 加 P0-P3 分级、中文解释、新手友好输出 |
| deploy-check | alfred-dev quality gate | 加中国部署场景 + 人工确认红线 |
| SESSION_DRIVER | 原创 | 加摘要裁剪策略，防止上下文膨胀 |

### 层 3：原创（竞品没有，我们的护城河）

| 组件 | 用途 |
|---|---|
| AI-GUIDE 防幻觉指南 | 教新手怎么和 AI 协作，什么时候该打断 |
| 新手问题排查 troubleshoot | 常见错误模式 + 中文解释 + 一键修复 |
| 生产化配置档 | toy / team / production 三档权限/hook/记忆策略 |
| 完整交付管线 | commit→review→deploy→进度跟踪 串联成闭环 |

---

## 四、Skill 迁移方案

### 4.1 官方 SKILL.md 格式

```markdown
---
name: skill-name
description: 完整描述这个 skill 做什么、什么时候触发
---

# Skill Title

[指令正文]
```

- 只有 **name** 和 **description** 两个必填字段
- 一个 skill = 一个文件夹，文件夹里是 SKILL.md
- 不支持 tools/runAs/priority 等自定义字段——这些移入正文作为自约束规则

### 4.2 迁移对照表

| 现有文件 | 迁移后路径 | 处理方式 |
|---------|-----------|---------|
| skills/task-planner.md | skills/task-planner/SKILL.md | 迁移格式，简化为"接收 superpowers brainstorming 输出，拆成30分钟中文任务" |
| skills/code-review.md | skills/code-review/SKILL.md | 薄封装 + 中文 P0-P3 分级 |
| skills/commit-helper.md | skills/commit-helper/SKILL.md | 迁移格式 |
| skills/deploy-check.md | skills/deploy-gate/SKILL.md | 改名+增强（加人工确认红线+CI检查+回滚指南） |
| skills/troubleshoot.md | skills/troubleshoot/SKILL.md | 迁移 + 加常见错误模式库 |
| skills/fullstack-scaffold.md | skills/fullstack-scaffold/SKILL.md | 加"可替换"出口，去掉"最优解"措辞 |
| skills/context-map.md | skills/context-map/SKILL.md | 加摘要/裁剪策略 |
| skills/api-designer.md | skills/api-designer/SKILL.md | 迁移格式 |
| skills/git-workflow.md | **删除** | superpowers 的 using-git-worktrees + finishing-branch 已覆盖 |

### 4.3 新增 skill

| 新增 skill | 用途 |
|-----------|------|
| skills/onboarding/SKILL.md | 首次使用引导：装 superpowers + 首次对话 |
| skills/test-runner/SKILL.md | 测试闭环：检测框架→跑测试→失败回滚→覆盖率 |
| skills/ci-helper/SKILL.md | CI 配置生成：lint→test→build→审计→密钥扫描 |
| skills/observability/SKILL.md | 日志规范 + Sentry 接入 + 告警配置 |
| skills/production-preflight/SKILL.md | 生产化检查：覆盖率/CI/权限/可观测性/密钥 |

---

## 五、权限模型：窄白名单 → 三级危险度

### 当前问题

claude-code.json 白名单只有 npm/pnpm/bun/git/cat/ls/grep 等，python/node/curl/docker 全部被封，模型连跑测试都被拦。

### 改造方案

| 级别 | 命令 | 策略 |
|------|------|------|
| safe | Read Write Edit, git/npm/pnpm/bun/node/python/pytest/cat/ls/grep/find/head/tail/wc/jq/curl/docker/sqlite3/npx/tsc/eslint/biome | 自动放行 |
| ask | rm mv cp, git push/merge/rebase, npm publish, docker push, psql/mysql | 首次提示确认 |
| danger | rm -rf /, sudo, chmod 777, curl|sh | 每次都确认 + 摘要预览 |

参考 alfred-dev 原则：自动批准用户级 gate，生产部署永远人工确认。

---

## 六、配置分档

| 档位 | 权限 | hook 严格度 | 记忆策略 | 受众 |
|------|------|-----------|---------|------|
| toy | 宽松白名单 | pre-commit: warning only | 全量加载 | 第一次用 AI 编程的人 |
| team | 危险度分级 | pre-commit: P0 阻止提交 | 摘要 + 按需加载 | 小团队协作 |
| production | 危险度分级 + 生产库二次确认 | pre-commit: P0 阻止 + pre-push: 全量检查 | 摘要 + 裁剪 + 归档 | 上线项目 |

---

## 七、生产化配置包

### 7.1 测试模板
- 单元测试模板（vitest / jest）
- 集成测试模板（API 测试）
- E2E 测试模板（playwright）
- 覆盖率基线（>=80%）

### 7.2 CI 模板
- GitHub Actions：lint → test → build → 依赖审计 → 密钥扫描
- 部署前检查清单（整合进 deploy-gate skill）

### 7.3 可观测性
- 结构化 JSON 日志规范
- Sentry 错误监控集成模板
- 健康检查端点模板

### 7.4 记忆裁剪策略
- CODEMAP 按模块分级：P0 核心完整结构 / P1 次要接口签名 / P2 边缘仅文件名
- PROJECT-MEMORY 超 2000 字自动摘要
- SESSION_DRIVER 只保留最近 3 次会话
- 提供手动触发"全量刷新"指令

---

## 八、修复清单（当前仓库硬伤）

| # | 问题 | 修复 |
|---|------|------|
| 1 | ZWNJ 路径（零宽字符包着的 project） | 重命名目录为普通 project |
| 2 | README 声称的 generate-code-map.py / mcp-guide.md / skill-writing.md 不存在 | 补齐或删掉声明 |
| 3 | pre-commit 的 any 检查误报（P0 阻止提交） | 降级为 warning |
| 4 | hooks 安装直接覆盖已有 hook 不备份 | 安装前备份为 .bak |
| 5 | post-session.sh 纯 bash，Windows 不可用 | 提供 PowerShell 版本 |
| 6 | docs/superpowers/specs/ 目录存在但未接轨 | 明确引用 superpowers 作为上游 |
| 7 | auto-evolve.yml 引用不存在的 EVOLVE_CHANGELOG.md | 修复或删除 |

---

## 九、仓库结构（改造后）

```
solo-dev-autopilot/
├── README.md                          ← 重写（定位声明 + 安装引导）
├── LICENSE                            ← MIT（不变）
├── BOOTSTRAP-PROMPT.md                ← 保留（改引用 superpowers）
├── .claude/
│   └── plugin/
│       └── marketplace.json           ← 新增：插件市场注册
├── skills/                            ← 改为文件夹式 SKILL.md
│   ├── onboarding/SKILL.md            ← 新增
│   ├── task-planner/SKILL.md          ← 迁移
│   ├── fullstack-scaffold/SKILL.md    ← 迁移 + 加可替换出口
│   ├── code-review/SKILL.md           ← 迁移
│   ├── commit-helper/SKILL.md         ← 迁移
│   ├── deploy-gate/SKILL.md           ← 新增（替代 deploy-check）
│   ├── test-runner/SKILL.md           ← 新增
│   ├── ci-helper/SKILL.md             ← 新增
│   ├── observability/SKILL.md         ← 新增
│   ├── production-preflight/SKILL.md  ← 新增
│   ├── troubleshoot/SKILL.md          ← 迁移 + 增强
│   ├── context-map/SKILL.md           ← 迁移 + 加裁剪
│   └── api-designer/SKILL.md          ← 迁移
├── configs/
│   ├── permissions.json               ← 新增：三级权限模型
│   ├── mcp-servers.json               ← 重写：引用 awesome-mcp-servers
│   ├── modes/                         ← 新增：三档配置
│   │   ├── toy.json
│   │   ├── team.json
│   │   └── production.json
│   └── tool-presets/                  ← 保留，权限部分改用 permissions.json
├── templates/
│   ├── AI-GUIDE-template.md           ← 保留 + 加 superpowers 速览
│   ├── PROJECT-MEMORY-template.md     ← 保留 + 加摘要标记
│   ├── SESSION_DRIVER-template.md     ← 保留
│   ├── pre-commit-hook                ← 改：any 降级 + 备份
│   └── pre-push-hook                  ← 保留
├── scripts/
│   ├── setup.sh                       ← 改：加 superpowers 检测
│   ├── setup.ps1                      ← 改：同上 + Windows 补全
│   ├── post-session.sh                ← 保留
│   ├── post-session.ps1               ← 新增：Windows 版
│   ├── auto-evolve.sh                 ← 保留
│   └── install-git-hooks.sh           ← 改：加备份
├── .github/
│   └── workflows/
│       ├── ci.yml                     ← 新增：CI 模板
│       └── auto-evolve.yml            ← 保留
└── docs/
    ├── BLUEPRINT-v2.md                ← 本文件
    ├── getting-started.md             ← 保留
    ├── newbie-pitfalls.md             ← 保留
    ├── competitive-analysis.md        ← 新增：竞品分析存档
    ├── production-checklist.md        ← 新增：生产上线清单
    └── autopilot-boundaries.md        ← 新增：autopilot 边界原则
```

---

## 十、开发阶段

### Phase 1：兼容性改造（2-3 天）

**目标**：让仓库接上 superpowers 和 SKILL.md 标准，不破坏现有结构。

- [ ] 修复 ZWNJ 路径问题
- [ ] 所有 skills/ 迁移为官方 SKILL.md 格式（文件夹式）
- [ ] 删除被 superpowers 覆盖的 git-workflow skill
- [ ] 整理 docs/ 目录，删除不存在文件的声明
- [ ] 将 superpowers 和 awesome-mcp-servers 写入 README 依赖声明
- [ ] 修复 auto-evolve.yml 的缺失引用
- [ ] 放宽权限白名单（python/node/curl/docker 解禁）

**里程碑验收**：
- 所有 skill 能被 Claude Code 原生识别
- README 里没有 404 链接
- pre-commit 不会误报 any[]

### Phase 2：独有层开发（3-5 天）

**目标**：竞品没有的差异化能力就位。

- [x] onboarding skill（引导装 superpowers + 首次使用）
- [x] context-map 增强（记忆裁剪策略）
- [x] deploy-gate skill（自动检查 + 人工确认红线）
- [x] 更新安装脚本，加入 superpowers 自动安装步骤
- [x] 插件市场注册（.claude/plugin/marketplace.json）

**里程碑验收**：
- [x] 安装脚本能自动检测并引导安装 superpowers
- [x] 记忆文件在 100 文件项目下不超过 2000 行
- [x] deploy-gate 的部署确认不可被跳过

### Phase 3：生产化（3-5 天）

**目标**：生产可用配置包就位。

- [ ] 权限模型：窄白名单 → 三级危险度分级（permissions.json）
- [ ] 配置分档：toy / team / production
- [ ] test-runner skill（测试闭环）
- [ ] ci-helper skill + GitHub Actions CI 模板
- [ ] observability skill（日志 + Sentry + 告警）
- [ ] production-preflight skill
- [ ] pre-commit 优化：any 降级、备份已有 hook
- [ ] setup.ps1 补全 Windows 支持

**里程碑验收**：
- CI 通过率 > 95%
- 生产模式配置档能正常加载
- test-runner 能跑 npm test / pytest 并输出覆盖率

### Phase 4：文档与评分（1-2 天）

**目标**：评分 9 分有理有据。

- [ ] 更新 README（定位声明 + 依赖说明 + 架构图）
- [ ] 补充各工具的安装引导文档
- [ ] 发布评分维度表
- [ ] 撰写"三步开始"完整流程

---

## 十一、评分体系（8 维度加权）

| 维度 | 权重 | 当前 | P1后 | P2后 | P3后(目标) |
|------|------|------|------|------|-----------|
| 新手引导体验 | 10% | 8 | 9 | 9 | 9.5 |
| Skill 设计质量 | 15% | 8 | 8 | 8.5 | 9 |
| 文档与实物一致性 | 10% | 5 | 9 | 9 | 9.5 |
| 跨平台可用性 | 10% | 4 | 8 | 8 | 9 |
| 权限与安全模型 | 15% | 5 | 7 | 8.5 | 9 |
| 测试/CI 闭环 | 15% | 2 | 3 | 8 | 9 |
| 可观测性 | 10% | 2 | 2 | 7 | 8.5 |
| 记忆/上下文管理 | 15% | 6 | 6 | 8 | 9 |
| **加权总分** | | **5.2** | **6.5** | **8.2** | **9.0** |

9 分不是"打"出来的，是"做"出来的。每个维度的分数都对应具体的改造任务。

---

## 十二、不做什么（防范围蔓延）

| 不做 | 原因 |
|------|------|
| 不自己写 TDD 方法论 | superpowers 已有 265k stars 的实现 |
| 不自己写 brainstorm/plan 流程 | 同上 |
| 不做多 agent 编排系统 | alfred-dev 在做，我们不竞争这个方向 |
| 不做 IDE 插件 | 我们是 skill + 配置层，不是 IDE 层 |
| 不做模型路由/训练 | 我们是工具无关的配置层 |
| 不做付费功能 | MIT 开源，保持纯粹 |

---

## 十三、风险与缓解

| 风险 | 影响 | 缓解措施 |
|---|---|---|
| superpowers 方法论变更 | 薄封装失效 | 锁定版本，定期同步 |
| 技术栈预设过时 | 脚手架跑不起来 | 每季度更新，声明支持版本号 |
| 新手不会用 skill | 装了不知道什么时候触发 | AI-GUIDE 强制阅读 + skill 自动提示 |
| 生产模式配置太复杂 | 用户不敢切 | 提供 setup-production 一键配置 |

---

## 附录：关键依赖项目

| 项目 | Stars | 用途 |
|---|---|---|
| anthropics/skills | 165,839 | 官方 SKILL.md 标准 |
| obra/superpowers | 265,204 | 方法论 + 技能框架 |
| 686f6c61/alfred-dev | 112 | 质量门 + 角色化 agent 参考 |
| punkpeye/awesome-mcp-servers | 91,742 | MCP 服务器大全 |
| wshobson/agents | 38,437 | 多工具插件市场模式 |
| jnMetaCode/superpowers-zh | 7,415 | superpowers 中文汉化（参考） |