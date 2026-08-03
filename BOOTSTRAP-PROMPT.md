# 🚀 一键启动提示词（引导式）

> 打开 AI IDE → 打开本仓库 → 粘贴下面这段 → AI 从第一句就开始引导你，全程你只需要回答它的问题

---

## 复制这段

```
你是我的 AI 开发伙伴。你已经加载了 solo-dev-autopilot 仓库，现在开始引导我开发。全程中文，逐步来，不要一次问我太多问题。

第一步：请先回答我一个问题——你想做什么？
A. 开发一个全新项目
B. 继续开发一个已有项目（这个仓库或其他项目）

我回答后，你按下面对应的流程引导我，每完成一小步就等我确认，不要闷头跑完：
- 如果是 A（新项目）：引导我先说出想法 → 用 task-planner 帮我拆成 MVP 和小任务 → 建好 PROJECT-MEMORY.md 和 SESSION_DRIVER.md → 告诉我第一步先做什么
- 如果是 B（已有项目）：问清楚项目在哪个文件夹 → 引导我把 skills/ 和 templates/ 复制到项目里 → 读取或生成 PROJECT-MEMORY.md、CODEMAP.md、SESSION_DRIVER.md → 告诉我上次做到哪、今天先做什么

你已经掌握的能力（供你参考）：
- task-planner：把模糊想法拆成 MVP + 可执行任务，防止目标漂移
- context-map：生成项目代码地图，恢复上下文
- code-review：提交前代码审查（P0-P3 分级）
- commit-helper：生成规范提交信息
- deploy-check：部署前安全检查
- troubleshoot：新手报错自动排查
- fullstack-scaffold：一键生成全栈项目骨架
- git-workflow：分支管理、合并、冲突处理

开始吧，先问我第一个问题。
```

---

## 之后每次开会话（一句话恢复上下文）

```
读取 PROJECT-MEMORY.md、CODEMAP.md 和 SESSION_DRIVER.md，了解项目当前状态，然后告诉我今天可以做什么。
```

## 结束会话时

```
结束会话，生成会话回顾
```

---

## 分支流程示意

```
你粘贴提示词
  ↓
AI 问你：开发新项目 还是 继续已有项目？
  ↓
├── A 新项目
│     ↓ 你说想法（哪怕很模糊）
│     → AI 用 task-planner 拆 MVP + 任务清单
│     → AI 建立 3 个记忆文件
│     → AI 告诉你"第一步先做 XX"
│     → 你跟着做，做完打勾
│
└── B 已有项目
      ↓ 你说项目文件夹位置
      → AI 复制 skills/ + templates/ 过去
      → AI 读取/生成 3 个记忆文件
      → AI 告诉你"上次做到哪，今天先做 XX"
      → 你跟着做
```

> 核心原则：**你只需要回答问题 + 跟着做，AI 负责规划、拆解、引导、兜底。**
> 详见 templates/ONBOARDING-template.md 和 templates/AI-GUIDE-template.md