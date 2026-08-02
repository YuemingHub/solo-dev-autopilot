# 🛡️ 新手避坑手册

> 我们收集了 Solo 开发者最容易踩的 50+ 个坑，每个都给出原因、现象、解决方案和预防措施。

## 目录

- [认知与心智模型](#0-认知与心智模型)
- [依赖与包管理](#1-依赖与包管理)
- [目标与任务管理](#05-目标与任务管理)
- [运行时错误](#2-运行时错误)
- [构建与部署](#3-构建与部署)
- [选型与初始化](#35-选型与初始化)
- [编码与代码质量](#45-编码与代码质量)
- [数据库](#4-数据库)
- [Git 与版本控制](#5-git-与版本控制)
- [AI 协作常见问题](#6-ai-协作常见问题)
- [心态与方法论](#7-心态与方法论)

---

## 0. 认知与心智模型

> 新手最大的坑不是技术问题，而是对 AI 的认知错误。这些坑会导致你用错方式跟 AI 协作，事倍功半。

### 坑 0.1：不知道 AI 能帮我什么

**现象**：装了 AI 编程工具，但面对空白对话框发呆，不知道能让它做什么

**原因**：新手以为 AI 只是"更聪明的搜索引擎"或"自动补全"，不知道它能建项目、设计 API、审查代码、排查错误

**解决**：
读项目根目录的 `AI-GUIDE.md`，里面有完整的"AI 能帮你做什么"场景清单。或者直接对 AI 说"你能帮我做什么"

**预防**：第一次使用前，花 3 分钟读 AI-GUIDE.md

---

### 坑 0.2：不知道 AI 有什么能力

**现象**：只用 AI 来"写代码"，不知道它还能审查代码、设计 API、检查部署、生成测试

**原因**：不知道项目里装了 8 个 Skill，每个都是一个"专业助手"

**解决**：
对 AI 说"读 AI-GUIDE.md，告诉我你有哪些 Skill"或者在 AI-GUIDE.md 里查"能力地图"表格

**预防**：把 AI-GUIDE.md 的"能力地图"表格当作速查表，随时翻

---

### 坑 0.3：知道 AI 会幻觉，但不知道怎么办

**现象**：听说 AI 会"一本正经地胡说"，所以不敢用，或者用了但被编造的 API 坑了

**原因**：知道"有幻觉"这个概念，但不知道具体怎么防

**解决**：
记住 3 条规则：
1. AI 给的 API/函数名，先验证再使用（问"这个 API 是真的吗"）
2. 每写一步就跑一下，不要一口气写完再测
3. 看不懂的代码不要直接用，先让 AI 解释

**预防**：每次 AI 给出代码，心里问一句"这个我真的能验证吗"

---

### 坑 0.4：把 AI 当搜索引擎用

**现象**：提问像搜索关键词——"React 怎么写表单"，得到泛泛的回答

**原因**：习惯了搜索引擎的用法，不知道 AI 需要上下文才能精准回答

**解决**：
用"协作式提问"，包含 4 要素：背景 + 目标 + 约束 + 当前状态。
详见 AI-GUIDE.md 的"搜索引擎式提问 vs 协作式提问"

**预防**：每次提问前问自己"AI 知道我的项目背景吗？"，不知道就先念启动咒语

---

### 坑 0.5：不敢质疑 AI

**现象**：AI 给了方案，自己觉得不对劲但不敢说，直接用了

**原因**：觉得 AI "更专业"，怕自己说错

**解决**：
记住：**你是 driver，AI 是副驾**。你觉得不对就直接说：
- "这个是不是太复杂了？"
- "我想要的是 xxx，你这个偏了"
- "换一个思路"

**预防**：每次 AI 给方案，先问自己"这个方案我看得懂吗？合理吗？"

---
## 0.5. 目标与任务管理

> 新手最大的效率杀手不是写错代码，而是不知道该写什么。这些坑会导致你一整天下来什么都没做出来。

### 坑 0.5.1：不会拆任务

**现象**：对 AI 说"帮我做个博客"，AI 一口气写一堆，中间出错不知道卡在哪步

**原因**：把大目标直接扔给 AI，没有拆成小任务。大目标 = 大代码量 = 大概率出错

**解决**：
对 AI 说"我想做个博客，帮我拆解任务"或"/skill task-planner"。
AI 会把"做个博客"拆成：建表→写API→写页面→联调，每步 30 分钟能完成。

**预防**：每次开始新功能前，先用 task-planner 拆解，再动手

---

### 坑 0.5.2：想法混乱零散，不知道从哪开始

**现象**：脑子里有很多想法，但一团乱麻，不知道先做哪个

**原因**：想法都在脑子里转，没有倒出来整理

**解决**：
打开 SESSION_DRIVER.md 的"想法收集区"，把所有想法倒进去，不用整理。
然后对 AI 说"读想法收集区，帮我整理成任务清单"。

**预防**：想到什么就写进想法收集区，别让想法在脑子里转

---

### 坑 0.5.3：AI 越聊越加功能

**现象**：本来说做登录，聊着聊着 AI 加了 OAuth+2FA+权限系统

**原因**：AI 倾向于给"最完整"的方案，新手不知道该拒绝

**解决**：
明确说"MVP 阶段不需要这些，只做最简单的版本"。
task-planner skill 会强制砍到 MVP，防止功能蔓延。
新想法会被记到"想法收集区"，不丢但也不打断当前目标。

**预防**：在 PROJECT-MEMORY.md 里注明"MVP 阶段，优先简洁"

---

### 坑 0.5.4：目标漂移自己没发现

**现象**：本来做 A，聊到一半变成 B，一整天白干

**原因**：没有明确记录当前目标，聊着聊着就偏了

**解决**：
每次开会话先在 SESSION_DRIVER.md 写"本轮目标"（1-3 件事）。
AI 会在做每个任务前检查是否在目标范围内，偏离了会主动提醒你。

**预防**：task-planner 的防漂移机制会帮你盯着目标

---

### 坑 0.5.5：不知道做到哪了，接下来该干什么

**现象**：做了半天，不知道完成了多少，不知道下一步做什么

**原因**：没有进度跟踪，做完就忘了做了啥

**解决**：
对 AI 说"读 SESSION_DRIVER.md，告诉我做到哪了，下一步做什么"。
SESSION_DRIVER.md 的"当前进度"区块记录了所有任务和完成状态。

**预防**：每完成一个任务就打勾，会话结束时 post-session 自动更新进度

---

### 坑 0.5.6：完美主义瘫痪

**现象**：花了两周纠结技术选型和项目结构，一行代码都没写

**原因**：想要"最好"的方案，害怕以后要重构

**解决**：
对 AI 说"帮我用 MVP 方式拆解任务"。
task-planner 会强制你只做最小可用版本，先跑起来再优化。

记住：**先让它跑起来，再让它变好。**

**预防**：用 fullstack-scaffold 生成项目骨架，5 分钟开始写业务代码

---
## 1. 依赖与包管理

### 坑 1：npm 和 pnpm/yarn 混用

**现象**：`node_modules` 里出现奇怪的依赖冲突，删除重装也没用

**原因**：不同包管理器的 lock 文件格式不同，`node_modules` 结构也不同。混用会导致幽灵依赖或缺失依赖。

**解决**：
```bash
# 选一个，只用一个！
rm -rf node_modules package-lock.json yarn.lock pnpm-lock.yaml
# 然后只用 pnpm install 或 npm install，不要混用
```

**预防**：在 PROJECT-MEMORY.md 中记录使用哪个包管理器，让 AI 始终遵守。

---

### 坑 2：忘记安装 devDependencies

**现象**：`Cannot find module 'xxx'`，但明明 `package.json` 里有

**原因**：有些包是 devDependency（如 typescript, @types/*, vite, tailwindcss），`npm install --production` 或某些环境下不会安装。

**解决**：
```bash
pnpm add -D xxx  # 明确加为 devDependency
```

**预防**：AI 生成的 package.json 应该正确区分 dependencies 和 devDependencies。

---

### 坑 3：lock 文件不提交

**现象**：同事/部署环境安装的依赖版本和你不一样，出 bug

**原因**：没有 lock 文件，每次 `install` 可能解析出不同版本的依赖。

**解决**：
```bash
# 确保 .gitignore 没有排除 lock 文件
git add pnpm-lock.yaml  # 或 package-lock.json / yarn.lock
git commit -m "chore: add lock file"
```

**预防**：我们的 .gitignore 模板已经排除了 lock 文件的忽略规则。

---

### 坑 4：全局安装 vs 本地安装混淆

**现象**：脚本里直接 `tsc` 或 `eslint` 报 command not found

**原因**：这些工具安装在本地 node_modules/.bin 但没有通过 npx 调用。

**解决**：
```bash
# ❌ 错误
tsc --noEmit
eslint src/

# ✅ 正确
npx tsc --noEmit
npx eslint src/

# 或者在 package.json scripts 中（推荐）
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "lint": "eslint src/"
  }
}
# 然后 pnpm typecheck
```

---

## 2. 运行时错误

### 坑 5：端口被占用 EADDRINUSE

**现象**：
```
Error: listen EADDRINUSE: address already in use :::3000
```

**原因**：上次的进程没关掉，或者其他程序用了这个端口。

**解决**：
```bash
# 方法 1：找到并杀掉占用端口的进程
lsof -ti:3000 | xargs kill -9

# 方法 2：换一个端口
PORT=3001 pnpm dev

# 方法 3：一键杀掉所有 Node 进程（慎用）
killall node  # macOS/Linux
```

**预防**：使用 `--port` 参数或环境变量指定端口，开发时固定用一个端口范围如 3000-3010。

---

### 坑 6：环境变量未定义

**现象**：
```
TypeError: Cannot read properties of undefined (reading 'DATABASE_URL')
```
或者启动后功能异常但没有明显报错。

**原因**：`.env` 文件不存在，或者变量名拼写错误，或者没有重启服务。

**解决**：
```bash
# 1. 确认 .env 存在
ls -la .env

# 2. 确认变量名正确（注意不要有多余空格）
cat .env | grep DATABASE

# 3. 重启服务（环境变量只在启动时读取）
# Ctrl+C 然后 pnpm dev
```

**预防**：使用 deploy-check skill 在每次部署前检查环境变量完整性。

---

### 坑 7：async/await 未处理 rejection

**现象**：进程静默退出，没有任何错误日志

**原因**：某个 Promise 被 reject 但没有被 catch，Node.js 默认行为是静默退出。

**解决**：
```javascript
// 在入口文件最顶部添加
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // 不要 process.exit()，让日志先输出完
});

// 所有 async 函数都要 try-catch
app.get('/api/users', async (req, res) => {
  try {
    const users = await db.users.findMany();
    res.json(users);
  } catch (error) {
    console.error('Failed to fetch users:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

**预防**：code-review skill 会检查是否有未处理的 async 错误。

---

### 坑 8：CORS 跨域错误

**现象**：
前端控制台报错：
```
Access to XMLHttpRequest at 'http://localhost:3000/api' from origin 
'http://localhost:5173' has been blocked by CORS policy
```

**原因**：前端（:5173）和后端（:3000）端口不同，浏览器同源策略阻止请求。

**解决**：
```typescript
// 后端添加 CORS 中间件
import { cors } from 'hono/cors'

const app = new Hono()
app.use('*', cors({
  origin: ['http://localhost:5173', 'https://your-production-domain.com'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization'],
}))
```

**预防**：fullstack-scaffold 生成的脚手架已经包含 CORS 配置。

---

## 3. 构建与部署

### 坑 9：构建本地通过但线上失败

**现象**：`pnpm build` 本地成功，部署后报错

**原因**：
- 本地有 `.env` 但线上没有配环境变量
- 本地装的依赖和 lock file 不一致
- 大小写敏感（Linux 区分大小写，macOS 不区分）

**解决**：
```bash
# 1. 确保线上环境变量已配置
# 2. 用 ci 模式安装依赖（严格按 lock file）
pnpm install --frozen-lockfile
# 3. 检查 import 路径的大小写
```

**预防**：deploy-check skill 会在部署前检查这些问题。

---

### 坑 10：.env 被意外提交到 Git

**现象**：GitHub 仓库里出现了包含密钥的 .env 文件

**原因**：忘记把 .env 加入 .gitignore，或者在 .gitignore 之前就 git add 了。

**解决**：
```bash
# 1. 立即撤销提交（如果刚提交）
git reset HEAD~1
echo ".env" >> .gitignore
git add .gitignore
git commit -m "chore: add .env to gitignore"

# 2. 如果已经推送到远程
# 立即轮换所有暴露的密钥（API Key、密码等）
# 然后用 BFG Repo Cleaner 或 git filter-repo 清除历史
```

**预防**：我们的 .gitignore 模板默认忽略 .env，post-session hook 也会检查。

---

## 4. 数据库

### 坑 11：迁移未执行导致表不存在

**现象**：
```
relation "users" does not exist
```

**原因**：代码里有 schema 定义但没有执行过迁移/建表命令。

**解决**：
```bash
# Drizzle ORM
pnpm db:push   # 推送 schema 变更到数据库

# Prisma
npx prisma migrate dev

# 或者首次初始化
pnpm db:push  # 创建所有表
```

**预防**：在 README 或启动脚本中加入数据库初始化步骤。

---

### 坑 12：并发写入冲突

**现象**：偶尔出现 "database is locked" 或死锁错误

**原因**：SQLite 并发写入限制（同一时间只能有一个写操作）。PostgreSQL 也有类似问题但更少见。

**解决**：
```typescript
// SQLite/Turso：加互斥锁
import { Database } from 'bun:sqlite'
// 或使用连接池 + 排队机制

// PostgreSQL：使用事务 + 合理的超时
await db.transaction(async (tx) => {
  await tx.users.update(...)
})
```

**预防**：在 PROJECT-MEMORY.md 中记录数据库特性和已知陷阱。

---

## 3.5. 选型与初始化

> 新手在"还没开始写代码"的阶段就会踩很多坑。这些坑会导致你从一开始就走错方向。

### 坑 3.5.1：不知道该选什么技术

**现象**：在 100 个框架里纠结，花了一周还没开始写代码

**原因**：选择太多，不知道哪个适合自己

**解决**：
直接用 fullstack-scaffold skill 的推荐组合 A（Bun+Hono+React+Tailwind+PostgreSQL），这是已经帮你选好的"最优解"。不需要纠结。

**预防**：技术选型用社区验证过的"最优解"，把决策精力留给业务逻辑

---

### 坑 3.5.2：照搬教程的旧技术栈

**现象**：用了 Express + EJS + jQuery，上来就过时

**原因**：照搬了 3 年前的教程

**解决**：
检查你的技术栈是否还在维护。对 AI 说"检查我的技术栈是否过时，有没有更好的替代"。

**预防**：用 fullstack-scaffold 生成项目骨架，技术栈永远是当前最优

---

### 坑 3.5.3：配置文件看不懂就改

**现象**：改了 tsconfig 或 vite.config 后项目跑不起来

**原因**：不理解配置文件的作用，照着教程乱改

**解决**：
改配置前先问 AI"这个配置文件每一项是干什么的"。改完跑一次确认没报错。

**预防**：不要手动改配置文件，让 AI 帮你改并解释

---

### 坑 3.5.4：环境没装对就开写

**现象**：Node 版本不对，报一堆莫名其妙的错

**原因**：没检查环境就开始写代码

**解决**：
运行 setup.ps1 / setup.sh，它会自动检测你的环境。
确认 Node.js >= 18、Git 已安装。

**预防**：每次开新项目先跑 setup 脚本检测环境

---

## 4.5. 编码与代码质量

> 新手写代码时最容易犯的错，不是逻辑错，而是"习惯错"——养成了坏习惯却不自知。

### 坑 4.5.1：用 any 不写类型

**现象**：TypeScript 项目里到处是 any，等于用 JS 写代码

**原因**：觉得写类型太麻烦，或者不知道怎么写类型

**解决**：
对 AI 说"帮我把这个函数加上类型"。code-review skill 会标记所有 any 使用。

**预防**：在 PROJECT-MEMORY.md 的编码规范里写"禁止 any"

---

### 坑 4.5.2：错误处理缺失

**现象**：程序静默崩溃，没有错误日志

**原因**：空 catch 块、async 没 try-catch

**解决**：
对 AI 说"检查这个文件有没有未处理的错误"。code-review skill 的 P1 检查会覆盖这个。

**预防**：每个 async 函数都要 try-catch，catch 里至少 console.error

---

### 坑 4.5.3：复制粘贴不懂就改

**现象**：从网上复制的代码改了关键行，报神秘错误

**原因**：不理解代码逻辑就改

**解决**：
粘贴前先对 AI 说"解释一下这段代码在干什么"。看懂了再改。

**预防**：看不懂的代码不要用

---

### 坑 4.5.4：不验证就往下写

**现象**：AI 写了一堆功能，最后一起跑，发现全错

**原因**：写完一个功能没测就继续写下一个

**解决**：
每写完一个功能就跑一次。对 AI 说"写完这个功能后先跑一下测试"。

**预防**：养成"写一步测一步"的习惯

---

### 坑 4.5.5：一次性写太多再测

**现象**：让 AI 一次写 5 个功能，最后一起跑，不知道哪步错了

**原因**：贪多，想一次搞定

**解决**：
用 task-planner 拆成小任务，每次只做 1-2 个。
对 AI 说"一次只做一个功能，做完就测"。

**预防**：一个会话最多完成 2-3 个小任务

---
## 5. Git 与版本控制

### 坑 13：一次提交太多东西

**现象**：一个 commit 改了 20 个文件，涵盖 3 个不同的功能

**原因**：写了很久代码后才提交，没有分批。

**解决**：
```bash
# 用 git stash 暂存，然后分批提交
git stash
# 功能 1 的改动
git add src/auth/*
git commit -m "feat(auth): add login"

git stash pop
# 功能 2 的改动
git add src/posts/*
git commit -m "feat(posts): create post CRUD"
```

**预防**：养成"完成一个小功能就提交"的习惯。commit-helper skill 会帮你规范 message。

---

### 坑 14：直接 push 到 main 分支

**现象**：main 分支上有未测试的代码，导致生产故障

**原因**：没有分支保护意识。

**解决**：
```bash
# 始终从 main 创建 feature 分支
git checkout -b feat/user-auth
# 开发...
git add .
git commit -m "feat(auth): add user authentication"
git push origin feat/user-auth
# 然后在 GitHub 上创建 PR，通过 CI 检查后再合并
```

**预防**：即使一个人开发也要用 feature branch + PR 流程，这是最好的代码审查习惯。

---

### 坑 5.5：不敢用 Git

**现象**：怕弄坏代码不敢操作 Git，全靠手动备份文件夹

**原因**：不理解 Git 的概念，怕出错不可逆

**解决**：
Git 的好处就是可以回退。对 AI 说"帮我提交，生成 commit message"。
commit-helper skill 会帮你写规范的 commit message。

**预防**：用 commit-helper skill，让 AI 帮你处理 Git 操作

---

### 坑 5.6：合并冲突不会处理

**现象**：看到 conflict 提示就慌了，不知道怎么解决

**原因**：不理解合并冲突是什么

**解决**：
把冲突信息粘贴给 AI，说"帮我解决合并冲突"。
AI 会分析冲突并给出合并方案。

**预防**：经常提交和拉取，减少大冲突的概率

---
## 6. AI 协作常见问题

### 坑 15：AI 不知道项目上下文

**现象**：每次新开会话都要重新解释项目结构和技术栈

**原因**：没有维护代码地图和项目记忆文件。

**解决**：
```bash
# 每次结束会话前
/skill context-map  # 更新代码地图

# 每次开始新会话
"加载 CODEMAP.md 和 PROJECT-MEMORY.md"
```

**预防**：post-session hook 会提醒你更新代码地图。

---

### 坑 16：AI 生成的代码不能跑

**现象**：AI 说代码写好了，但一运行就报错

**原因**：
- AI 没有实际执行能力，只能预测代码是否正确
- 缺少依赖但 AI 不知道
- 环境差异（AI 假设的环境和你实际的不一样）

**解决**：
```bash
# 1. 先看报错信息
# 2. 把完整报错发给 AI
# 3. 让 AI 逐步修复，而不是一次性重写
"报错了，错误信息是：[粘贴]"
```

**预防**：让 AI 每改一步就跑一下测试，而不是写完一大堆再验证。

---

### 坑 17：AI 过度工程化

**现象**：一个简单的 TODO 应用被 AI 设计成了微服务架构

**原因**：AI 倾向于给出"最完整"的方案，但新手项目需要的是"最简单可用"的方案。

**解决**：
明确告诉 AI：
```
保持简单。MVP 阶段不需要：
- 微服务
- 复杂的设计模式
- 过度的抽象层
- 还没用到的功能预留

当前只需要：能跑的最简实现。
```

**预防**：在 PROJECT-MEMORY.md 中注明"MVP 阶段，优先简洁"。

---

## 7. 心态与方法论

### 坑 18：完美主义瘫痪

**现象**：花了两周时间纠结技术选型和项目结构，一行代码都没写

**原因**：想要"最好"的方案，害怕以后要重构。

**解决**：
```
先让它跑起来，再让它变好。
— Kent Beck (Extreme Programming 之父)

MVP 原则：
1. 能用 > 完美
2. 今天能跑 > 明天更优雅
3. 先解决核心问题，再优化
```

**我们的建议**：直接用 fullstack-scaffold 生成项目骨架，5 分钟内开始写业务代码。

---

### 坑 19：不敢问 / 不敢试 / 不敢试

**现象**：遇到错误就卡住，不知道怎么办

**原因**：怕暴露自己不懂，或者觉得问题太蠢不该问。

**解决**：
```
1. 把错误信息原封不动发给 AI
2. 用 troubleshoot skill
3. 搜索引擎搜错误信息（大概率别人也遇到过）
4. 社区提问（Stack Overflow, GitHub Issues, Discord）

没有蠢问题，只有不问的问题。
```

---

### 坑 8.5：不知道部署前查什么

**现象**：直接 push 到生产，结果环境变量没配、依赖没装

**原因**：不知道部署前有检查清单

**解决**：
对 AI 说"能部署了吗"，deploy-check skill 会自动检查所有关键项。

**预防**：每次部署前必跑 deploy-check

---

### 坑 8.6：域名/HTTPS 不会配

**现象**：部署成功但访问不了，或者浏览器提示不安全

**原因**：DNS 没配、HTTPS 证书没设置

**解决**：
对 AI 说"帮我配置域名和 HTTPS"。Vercel 等平台通常自动配 HTTPS。

**预防**：用 Vercel 部署前端，自动配 HTTPS

---
## 📊 坑频统计

基于社区反馈的高频 TOP 10：

| 排名 | 问题 | 出现频率 | 影响程度 | 解决难度 |
|------|------|---------|---------|---------|
| 1 | 端口被占用 | ★★★★★ | ★★☆☆☆ | ★☆☆☆☆ |
| 2 | 环境变量缺失 | ★★★★★ | ★★★★☆ | ★★☆☆☆ |
| 3 | 依赖混用 | ★★★★☆ | ★★★★☆ | ★★☆☆☆ |
| 4 | CORS 跨域 | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ |
| 5 | .env 泄露 | ★★★☆☆ | ★★★★★ | ★★☆☆☆ |
| 6 | AI 上下文丢失 | ★★★★★ | ★★★★☆ | ★☆☆☆☆ |
| 7 | 构建不一致 | ★★★☆☆ | ★★★★☆ | ★★★☆☆ |
| 8 | async 错误吞掉 | ★★★★☆ | ★★★★☆ | ★★☆☆☆ |
| 9 | 迁移未执行 | ★★★☆☆ | ★★★★☆ | ★★☆☆☆ |
| 10 | 过度工程化 | ★★★★☆ | ★★★☆☆ | ★☆☆☆☆ |

---

> 💡 如果你踩了一个这里没有记录的坑，欢迎贡献回仓库！
> 这就是"持续进化"的意义——每个人的经验都能帮助后来者。
