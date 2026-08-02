---
name: fullstack-scaffold
description: >
  一句话描述需求 → 生成完整的前后端项目骨架。
  所有技术选型已预设为最优解，新手不需要做任何决策。
  支持 Node.js/Bun/Python 后端 + React/Vue/Svelte 前端的多种组合。
runAs: subagent
tools: [write_file, create_directory, list_directory, run_command]
tags: [scaffold, project-creation, fullstack, bootstrap]
priority: high
---

# Fullstack Scaffold — 全栈项目脚手架生成器

## 目标

根据用户的一句话描述，生成一个**开箱即用、结构清晰、配置完备**的全栈项目骨架。

## 支持的技术栈组合（已选最优解）

### 推荐组合 A：现代全栈（默认）
| 层 | 技术 | 为什么选它 |
|---|------|-----------|
| 运行时 | **Bun** | 比 Node 快 3x，内置 TS 支持，包管理+运行时一体 |
| 后端框架 | **Hono** | 轻量、快、边缘兼容、TypeScript-first |
| 前端框架 | **React 19 + Vite** | 生态最大、就业最广、学习资源最多 |
| UI 库 | **shadcn/ui + Tailwind CSS v4** | 可定制、不打包、Tree-shakable 组件 |
| 数据库 | **PostgreSQL (via Supabase)** | 免费额度够用、自带 Auth/Storage/Realtime |
| 部署 | **Vercel (前端) + Supabase (后端)** | 免费额度、自动 CI/CD、零配置部署 |
| 包管理 | **pnpm** | 节省磁盘、快速、严格依赖管理 |

### 推荐组合 B：轻量极速
| 层 | 技术 |
|---|------|
| 运行时 | **Bun** |
| 后端框架 | **Elysia** (更快但生态小) 或 **Hono** |
| 前端框架 | **SvelteKit + Svelte 5** |
| UI 库 | **Tailwind CSS v4 + shadcn-svelte** |
| 数据库 | **Turso (libSQL)** | 边缘原生、免费额度大 |
| 部署 | **Cloudflare Workers/Pages** |

### 推荐组合 C：Python 全栈
| 层 | 技术 |
|---|------|
| 后端框架 | **FastAPI** + **SQLAlchemy 2.0** |
| 前端框架 | **Next.js (App Router)** 或 **Vue 3 + Vite** |
| 数据库 | **PostgreSQL (via Neon)** |
| 部署 | **Railway** 或 **Vercel** |

## 执行流程

### Step 1: 理解需求

向用户确认以下信息（如果用户没说清楚）：
1. **做什么产品？** — 一句话描述功能
2. **有偏好吗？** — 如果没有，使用推荐组合 A
3. **需要认证吗？** — 默认包含邮箱+密码登录
4. **需要数据库吗？** — 大多数情况需要，默认 PostgreSQL

### Step 2: 生成项目结构

```
<project-root>/
├── package.json              # pnpm monorepo (workspace: *)
├── pnpm-workspace.yaml
├── turbo.json                # Turborepo 配置
├── .env.example              # 环境变量模板
├── .gitignore                # 最优 gitignore
│
├── apps/
│   ├── web/                  # 前端应用 (React + Vite)
│   │   ├── src/
│   │   │   ├── components/   # 可复用组件
│   │   │   │   └── ui/       # shadcn/ui 组件
│   │   │   ├── pages/        # 页面路由
│   │   │   ├── lib/          # 工具函数、API 客户端
│   │   │   ├── hooks/        # 自定义 Hooks
│   │   │   ├── stores/       # 状态管理 (zustand)
│   │   │   ├── types/        # TypeScript 类型定义
│   │   │   └── main.tsx      # 入口
│   │   ├── public/
│   │   ├── index.html
│   │   ├── vite.config.ts
│   │   ├── tailwind.config.ts
│   │   ├── tsconfig.json
│   │   └── components.json   # shadcn/ui 配置
│   │
│   └── server/               # 后端应用 (Hono + Bun)
│       ├── src/
│       │   ├── routes/       # 路由模块
│       │   │   ├── index.ts
│       │   │   ├── auth.ts
│       │   │   ├── users.ts
│       │   │   └── ...       # 按业务域拆分
│       │   ├── middleware/    # 中间件
│       │   │   ├── auth.ts
│       │   │   ├── error.ts
│       │   │   └── logger.ts
│       │   ├── services/     # 业务逻辑层
│       │   ├── db/           # 数据库相关
│       │   │   ├── schema.ts  # Drizzle ORM schema
│       │   │   ├── connect.ts # 连接配置
│       │   │   └── seed.ts    # 种子数据
│       │   ├── lib/          # 工具函数
│       │   └── index.ts      # 入口
│       ├── drizzle.config.ts
│       └── tsconfig.json
│
├── packages/
│   ├── shared/               # 共享代码
│   │   ├── src/
│   │   │   ├── types.ts      # 共享类型
│   │   │   ├── constants.ts  # 共享常量
│   │   │   └── utils.ts      # 共享工具函数
│   │   └── tsconfig.json
│   └── ui/                   # 共享 UI 组件 (如需多前端)
│
├── scripts/
│   ├── dev.sh                # 一键启动开发环境
│   ├── db-push.sh            # 推送数据库变更
│   └── seed.sh               # 填充种子数据
│
└── tests/
    ├── e2e/                  # 端到端测试 (Playwright)
    └── unit/                 # 单元测试 (vitest)
```

### Step 3: 生成关键文件内容

#### package.json (monorepo root)
```json
{
  "name": "my-project",
  "private": true,
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "lint": "turbo lint",
    "db:generate": "cd apps/server && drizzle-kit generate",
    "db:push": "cd apps/server && drizzle-kit push",
    "db:studio": "cd apps/server && drizzle-kit studio",
    "seed": "bun apps/server/src/db/seed.ts"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.5.0"
  },
  "packageManager": "pnpm@9.15.0",
  "engines": {
    "node": ">=20"
  }
}
```

#### .env.example
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Auth (Supabase)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx
SUPABASE_SERVICE_ROLE_KEY=eyJxxx

# App
APP_URL=http://localhost:5173
PORT=3000
NODE_ENV=development
```

#### apps/server/src/index.ts (Hono 入口示例)
```typescript
import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { logger } from 'hono/logger'
import { routes } from './routes'

const app = new Hono()

// Middleware
app.use('*', cors())
app.use('*', logger())

// Health check
app.get('/health', (c) => c.json({ status: 'ok', timestamp: new Date().toISOString() }))

// Routes
app.route('/', routes)

// Error handling
app.onError((err, c) => {
  console.error('❌ Error:', err.message)
  return c.json({ error: 'Internal Server Error', message: err.message }, 500)
})

export default app
```

#### apps/web/src/lib/api-client.ts (前端 API 客户端)
```typescript
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3000'

export async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: res.statusText }))
    throw new Error(error.message || `API Error: ${res.status}`)
  }

  return res.json()
}

// Typed convenience methods
export const apiClient = {
  get: <T>(path: string) => api<T>(path),
  post: <T>(path: string, body?: unknown) => api<T>(path, { method: 'POST', body: JSON.stringify(body) }),
  put: <T>(path: string, body?: unknown) => api<T>(path, { method: 'PUT', body: JSON.stringify(body) }),
  del: <T>(path: string) => api<T>(path, { method: 'DELETE' }),
}
```

### Step 4: 初始化项目

执行以下命令：
```bash
# 安装依赖
pnpm install

# 初始化数据库
pnpm db:push

# 启动开发
pnpm dev
```

### Step 5: 生成 CODEMAP.md 和 PROJECT-MEMORY.md

调用 context-map skill 生成初始代码地图。

## 输出清单

生成完成后，向用户展示：

1. ✅ 项目结构树
2. ✅ 已生成的关键文件列表
3. ✅ 下一步操作指南：
   - 复制 `.env.example` 为 `.env` 并填入值
   - 运行 `pnpm install`
   - 运行 `pnpm dev` 启动开发服务器
   - 访问 http://localhost:5173 (前端) 和 http://localhost:3000 (后端健康检查)
4. ⚠️ 需要手动做的事（如注册 Supabase、获取 API Key）

## 注意事项

1. **不要过度工程化**：只生成当前需要的结构，不要预先做抽象
2. **每个文件都要有实际内容**：不要生成空文件或只有注释的占位文件
3. **TypeScript 优先**：所有 JS 文件都应该是 .ts/.tsx，开启 strict 模式
4. **错误处理从第一天就有**：全局错误边界、API 错误处理、表单验证
5. **环境变量从第一天就规范**：用 .env.example，不要硬编码
