# 🛡️ 新手避坑手册

> 我们收集了 Solo 开发者最容易踩的 50+ 个坑，每个都给出原因、现象、解决方案和预防措施。

## 目录

- [依赖与包管理](#1-依赖与包管理)
- [运行时错误](#2-运行时错误)
- [构建与部署](#3-构建与部署)
- [数据库](#4-数据库)
- [Git 与版本控制](#5-git-与版本控制)
- [AI 协作常见问题](#6-ai-协作常见问题)
- [心态与方法论](#7-心态与方法论)

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

### 坑 18：不敢问 / 不敢试

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
