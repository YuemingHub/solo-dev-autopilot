---
name: troubleshoot
description: 新手问题自动排查器。覆盖 50+ 新手高频问题：依赖冲突、端口占用、环境变量缺失、 构建失败、数据库连接错误等。输入错误信息，输出结构化的排查步骤和修复方案。
license: MIT
---

# Troubleshoot — 新手问题自动排查器

## 目标

根据用户提供的**错误信息或异常现象**，自动分析原因并给出结构化的排查步骤和修复方案。

## 支持的问题类别

### 类别 1：依赖与包管理
- `npm install` 失败 / 卡住
- `ENOTFOUND` / `ECONNREFUSED` 网络错误
- `peer dependency` 冲突
- `node_modules` 损坏
- pnpm/yarn/npm 混用导致问题
- lock 文件不一致

### 类别 2：运行时错误
- `EADDRINUSE` 端口被占用
- `ENOENT` 文件找不到
- `Cannot find module`
- `TypeError: Cannot read properties of undefined`
- `SyntaxError` / 解析错误
- 内存溢出（OOM）

### 类别 3：构建错误
- TypeScript 编译错误
- Webpack/Vite/Rollup 构建失败
- CSS/SCSS 编译错误
- 资源文件找不到
- 环境变量未定义导致构建失败

### 类别 4：数据库问题
- 连接拒绝 (`ECONNREFUSED`)
- 认证失败 (`password authentication failed`)
- 表/列不存在
- 迁移失败
- 连接池耗尽
- 字符集/编码问题

### 类别 5：API / 网络问题
- CORS 错误
- 401/403/404/500 错误
- 请求超时
- SSL/TLS 证书问题
- WebSocket 连接失败

### 类别 6：Git 问题
- 合并冲突
- 权限问题（Permission denied）
- 大文件提交失败
- 分支混乱
- `.gitignore` 不生效

## 执行流程

### Step 1: 收集错误信息

向用户确认：
1. **完整的错误输出**（不是截图，是文字）
2. **什么时候发生的？**（安装/启动/构建/运行/部署）
3. **之前做了什么？**（刚改了什么 / 刚装了什么 / 第一次跑）
4. **环境信息**（OS、Node 版本、包管理器）

如果用户只给了部分信息，先问清楚再继续。

### Step 2: 错误模式匹配

将错误信息与已知问题库进行匹配。以下是高频问题的快速诊断表：

#### 🔥 Top 20 高频问题速查

| 错误关键词 | 可能原因 | 首选修复方案 |
|-----------|---------|-------------|
| `EADDRINUSE: address already in use :::3000` | 端口被占用 | `lsof -ti:3000 \| xargs kill -9` 或换端口 |
| `ERR_MODULE_NOT_FOUND` | 包没装或路径错 | 重装依赖 `rm -rf node_modules && pnpm install` |
| `Cannot find module 'xxx'` | 缺少依赖 | `pnpm add xxx` |
| `peer dep @x.y.z not found` | peer dependency 冲突 | `--legacy-peer-deps` 或 `--force`（临时）|
| `ENOSPC` / `no space left` | 磁盘满了 | 清理缓存 `pnpm store prune` / 清理 Docker |
| `ETIMEDOUT` / `ECONNREFUSED` | 网络不通 | 检查代理/VPN/DNS |
| `permission denied` | 权限不足 | `sudo`（Node 相关不推荐）或修复文件权限 |
| `cross-env not found` | devDependency 未装 | `pnpm add -D cross-env` |
| `Unexpected token` | TS/JSX 未正确编译 | 检查 tsconfig / babel 配置 |
| `Failed to parse source map` | source map 损坏 | 删除 node_modules 重建 |
| `password authentication failed for user` | 数据库密码错 | 检查 .env 中的 DATABASE_URL |
| `relation "xxx" does not exist` | 表不存在 | 运行迁移 `pnpm db:push` |
| `FATAL: database "xxx" does not exist` | 数据库没创建 | 先创建数据库 `createdb xxx` |
| `CORS policy blocked` | 前后端跨域 | 后端配置 CORS 中间件 |
| `env variable undefined` | 环境变量缺失 | 复制 .env.example 为 .env 并填值 |
| `git push rejected (non fast-forward)` | 远程有新提交 | 先 pull 再 push |
| `SSL certificate problem` | 证书问题 | 设置 `NODE_TLS_REJECT_UNAUTHORIZED=0`（仅开发）|
| `Maximum call stack size exceeded` | 无限递归/循环引用 | 检查递归调用和循环 import |
| `heap out of memory` | 内存不够 | 增加 `NODE_OPTIONS=--max-old-space-size=4096` |
| `zsh: command not found: xxx` | 命令不在 PATH 中 | 用 npx 运行或全局安装 |

### Step 3: 输出结构化排查报告

```markdown
# 🔧 Troubleshooting Report

> 问题：<用户描述的错误>
> 时间：<timestamp>

## 🎯 诊断结果

**问题类型**：<类别>
**可能原因**：<1-3 个按可能性排序的原因>
**置信度**：高/中/低

## 📋 排查步骤（按顺序执行）

### Step 1: <最可能的修复> ✅ 首试
```bash
<命令>
```
预期结果：<成功后应该看到什么>

### Step 2: <如果 Step 1 不行>
```bash
<命令>
```

### Step 3: <如果 Step 2 还不行>
```bash
<命令>
```

## 💡 根本原因解释

<用新手能懂的话解释为什么会出这个问题，不要用术语堆砌>

## 🛡️ 防止再次发生

<1-2 条预防措施>
```

### Step 4: 如果问题不在已知库中

如果错误信息没有匹配到任何已知问题：

1. **提取关键错误词**：从错误信息中找出最重要的关键词
2. **搜索解决方案**：使用 web_search 工具搜索该错误
3. **整理成新条目**：找到解决方案后，将其添加到项目记忆中供后续参考
4. **反馈给仓库**：建议用户将此问题贡献回 solo-dev-autopilot 仓库

## 使用方式

### 手动触发
在对话中说：
- "帮我看看这个报错" + 粘贴错误信息
- "为什么报这个错"
- "troubleshoot <错误信息>"
- "/skill troubleshoot"
- "救命，我的代码跑不起来了"

### 自动触发（推荐）
配置在工具的 error handler 中——当 shell 命令返回非零退出码时，自动调用此 skill 分析。

## 注意事项

1. **先问后查**：如果错误信息不完整，先问清楚再猜测。不要凭半句话下结论
2. **由简到繁**：排查步骤从最简单/最常见的开始，逐步深入
3. **给具体命令**：每一步都要给可以直接复制粘贴执行的完整命令
4. **解释原因**：不只是给修复方案，还要解释"为什么会这样"，帮助新手理解
5. **记录经验**：每次解决一个问题后，建议用 `/remember` 记录下来，避免下次再踩
