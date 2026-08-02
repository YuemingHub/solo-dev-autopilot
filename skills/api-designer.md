---
name: api-designer
description: >
  API 接口设计与文档生成器。根据业务需求自动设计 RESTful API，
  生成 OpenAPI/Swagger 规范、请求/响应类型定义、Zod 验证 schema。
  新手最容易把 API 设计得混乱——这个 Skill 确保接口规范一致。
runAs: subagent
tools: [write_file, read_file, list_directory]
tags: [api, design, restful, openapi, documentation]
priority: medium
---

# API Designer — 接口设计与文档生成器

## 目标

根据用户描述的业务需求，设计一套**规范、完整、可扩展**的 RESTful API，并生成对应的代码实现。

## 执行流程

### Step 1: 收集需求

向用户确认：
1. **核心资源有哪些？**（User, Post, Order, Product...）
2. **每个资源需要哪些操作？**（CRUD + 自定义操作）
3. **需要认证吗？**（默认 JWT Bearer Token）
4. **需要分页/搜索/过滤吗？**
5. **有特殊的业务规则吗？**

### Step 2: 设计 API 规范

按 RESTful 最佳实践设计：

#### URL 设计规范
```
GET    /api/<resource>              列表（支持分页、过滤、排序）
GET    /api/<resource>/:id          详情
POST   /api/<resource>              创建
PUT    /api/<resource>/:id          全量更新
PATCH  /api/<resource>/:id          部分更新
DELETE /api/<resource>/:id          删除

# 嵌套资源
GET    /api/users/:userId/posts     某用户的文章列表
POST   /api/users/:userId/posts     为某用户创建文章

# 自定义动作
POST   /api/posts/:id/publish       发布文章
POST   /api/posts/:id/archive       归档文章
```

#### 统一响应格式
```typescript
// 成功
{
  "success": true,
  "data": <T>,
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 100
  }
}

// 错误
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在",
    "details": { ... }
  }
}
```

### Step 3: 输出产物

#### 产物 1：API 文档 (Markdown)
```markdown
# API Reference — <project-name>

## Base URL
- 开发环境: http://localhost:3000/api
- 生产环境: https://api.example.com/v1

## 认证方式
- Bearer Token (JWT)
- Header: `Authorization: Bearer <token>`

## 错误码
| Code | HTTP Status | 说明 |
|------|-------------|------|
| VALIDATION_ERROR | 400 | 请求参数验证失败 |
| UNAUTHORIZED | 401 | 未认证 |
| FORBIDDEN | 403 | 无权限 |
| NOT_FOUND | 404 | 资源不存在 |
| CONFLICT | 409 | 资源冲突 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |

## 接口列表

### Users
...

### Posts
...
```

#### 产物 2：路由文件 (Hono 示例)
```typescript
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zodiac'

const app = new Hono()

// Schema definitions
const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  name: z.string().min(1).max(50),
})

const UpdateUserSchema = CreateUserSchema.partial()

const PaginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  pageSize: z.coerce.number().int().positive().max(100).default(20),
  search: z.string().optional(),
  sortBy: z.enum(['createdAt', 'name']).optional('createdAt'),
  sortOrder: z.enum(['asc', 'desc']).optional('desc'),
})

// Routes
app.get('/', zValidator('query', PaginationSchema), async (c) => {
  const { page, pageSize, search, sortBy, sortOrder } = c.req.valid('query')
  // ...
})

app.post('/', zValidator('json', CreateUserSchema), async (c) => {
  const data = c.req.valid('json')
  // ...
})

app.get('/:id', async (c) => {
  const id = c.req.param('id')
  // ...
})

// ... 其他路由

export default app
```

#### 产物 3：TypeScript 类型定义
```typescript
// types/api.ts

export interface PaginatedResponse<T> {
  success: true
  data: T[]
  meta: PaginationMeta
}

export interface SingleResponse<T> {
  success: true
  data: T
}

export interface ErrorResponse {
  success: false
  error: ApiError
}

export interface ApiError {
  code: string
  message: string
  details?: Record<string, unknown>
}

export interface PaginationMeta {
  page: number
  pageSize: number
  total: number
  totalPages: number
  hasNext: boolean
  hasPrev: boolean
}

// Resource types
export interface User {
  id: string
  email: string
  name: string
  avatarUrl?: string
  role: UserRole
  createdAt: string
  updatedAt: string
}

export type UserRole = 'admin' | 'user'

export interface CreateUserInput {
  email: string
  password: string
  name: string
}

export interface UpdateUserInput extends Partial<CreateUserInput> {}
```

## 使用方式

在对话中说：
- "帮我设计一个博客系统的 API"
- "设计用户模块的接口"
- "/skill api-designer"
- "生成 CRUD 接口"

## 注意事项

1. **版本化从第一天开始**：URL 用 `/v1/` 前缀，即使现在只有一个版本
2. **统一命名约定**：用 camelCase 字段名，kebab-case URL 路径
3. **每个接口都要有验证**：用 Zod schema 定义输入，不要手动验证
4. **错误信息要具体**：不要返回 "Bad request"，要返回 "email 格式不正确"
5. **分页是默认行为**：列表接口必须支持分页，不要返回全部数据
