# 🚀 一键启动提示词

> 打开 AI IDE → 打开本仓库文件夹 → 把下面这段话原样粘贴发给 AI → 它自己跑完全部初始化 → 回复你"可以开始了"

---

## 使用方法

1. 打开你的 AI IDE（TRAE / Cursor / Claude Code / Cline 等）
2. 打开这个仓库文件夹作为工作目录
3. 把下面「复制这段」里的内容原样粘贴发送
4. AI 会自主完成：认识项目 → 检测环境 → 建立记忆 → 告诉你可以开始了 → 引导你开发

---

## 复制这段

```
你是我的 AI 开发伙伴。我现在把 solo-dev-autopilot 仓库交给你，请你按下面的步骤自主完成初始化准备，每完成一个大阶段向我汇报一次结果，全部完成后引导我开始开发。

【阶段 1：认识项目】
1. 阅读 README.md，了解这个仓库是干什么的
2. 阅读 docs/getting-started.md，了解完整使用流程
3. 阅读 docs/newbie-pitfalls.md，了解新手最容易踩的坑（你要在后续开发中主动帮我避开）
4. 阅读 skills/ 下所有 skill 文件，总结每个 skill 的用途，告诉我你有哪些能力

【阶段 2：环境检测】
1. 检测我的开发环境：Node.js / Bun / pnpm / Git 是否已安装，版本是多少
2. 如果缺少某个工具，明确告诉我"需要安装 XX，命令是：..."，但不要擅自安装
3. 检查 .gitignore 和 .env.example 是否就位

【阶段 3：建立项目记忆】
1. 检查 PROJECT-MEMORY.md 是否存在；不存在就用 templates/PROJECT-MEMORY-template.md 生成，并引导我填写技术栈等关键信息
2. 检查 SESSION_DRIVER.md 是否存在；不存在就用 templates/SESSION_DRIVER-template.md 生成
3. 生成 CODEMAP.md 项目代码地图
4. 阅读 templates/ONBOARDING-template.md 和 templates/AI-GUIDE-template.md，确认你理解"启动咒语"和记忆系统的工作方式

【阶段 4：准备开发引导】
1. 确认你已经掌握了 task-planner skill 的用法（把模糊想法拆成 MVP + 可执行任务）
2. 准备好后，告诉我："我们已经可以开始开发了"
3. 然后引导我说出第一个想法，用这句话开头：
   "你想做什么？不用想清楚，把你脑子里冒出来的想法都告诉我，我来帮你整理成可执行的任务。"

【重要规则】
- 每个阶段完成都要向我汇报结果，不要一口气闷头跑完
- 遇到问题先解释，再给方案；不要自作主张做超出我要求的事
- 一切以"让我这个新手能顺利开始写代码"为目标
- 全程用中文回复
```

---

## 之后每次开会话（启动咒语）

```
读取 PROJECT-MEMORY.md、CODEMAP.md 和 SESSION_DRIVER.md，了解项目当前状态，然后告诉我今天可以做什么。
```

## 结束会话时

```
结束会话，生成会话回顾
```

> 详见 templates/ONBOARDING-template.md 里的完整说明