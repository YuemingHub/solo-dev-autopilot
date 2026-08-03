---
name: commit-helper
description: 分析当前所有改动，自动生成符合 Conventional Commits 规范的提交信息。 新手最纠结"commit message 怎么写"——这个 Skill 彻底消除这个决策点。
license: MIT
---

# Commit Helper — 智能 Commit 信息生成器

## 目标

分析 `git diff` / `git status` 的改动内容，生成**符合 Conventional Commits 规范**、信息完整、中英文皆可的高质量 commit message。

## Conventional Commits 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 列表

| Type | 描述 | 何时使用 |
|------|------|---------|
| `feat` | 新功能 | 添加新特性、新页面、新 API |
| `fix` | Bug 修复 | 修复错误、异常、崩溃 |
| `docs` | 文档变更 | 只改了 README、注释、文档 |
| `style` | 代码格式 | 空格、分号、格式化（不影响逻辑） |
| `refactor` | 重构 | 既不是 feat 也不是 fix 的代码变更 |
| `perf` | 性能优化 | 提升性能的代码变更 |
| `test` | 测试相关 | 添加/修改测试用例 |
| `chore` | 构建/工具 | 构建配置、依赖更新、脚本变更 |
| `ci` | CI/CD | 工作流配置变更 |
| `revert` | 回滚 | 回退之前的 commit |

### Scope 常见值

`auth`, `db`, `api`, `ui`, `components`, `server`, `client`, `config`, `deps`, `readme`

## 执行步骤

### Step 1: 收集改动信息

```bash
# 获取改动的文件列表和状态
git status --short

# 获取详细的 diff 内容
git diff HEAD          # 未暂存的改动
git diff --cached      # 已暂存的改动

# 如果是 amend 或 merge，获取最近几次 commit
git log --oneline -5
```

### Step 2: 分析改动类型

对每个改动的文件/目录进行分类：

1. **识别主要 type**：看改动最多的是哪类文件
   - 新增组件/页面 → `feat`
   - 修复报错 → `fix`
   - 改变量名/结构 → `refactor`
   - 只改格式 → `style`
   - 更新依赖版本 → `chore`

2. **识别 scope**：根据改动的目录判断
   - `src/routes/auth.ts` → scope = `auth`
   - `components/Button.tsx` → scope = `ui`
   - `package.json` → scope = `deps`

3. **识别 subject**：一句话概括改动目的（不超过 50 字符，中文不超过 20 字）

### Step 3: 生成 commit message

#### 格式 A：简单改动（<5 个文件，单一类型）

```
<type>(<scope>): <subject>
```

示例：
- `feat(auth): 添加邮箱密码登录功能`
- `fix(api): 修复用户列表查询分页参数错误`
- `chore(deps): 升级 react 到 19.0.0`
- `style(ui): 统一按钮间距为 4px 倍数`

#### 格式 B：复杂改动（多文件、多类型）

```
<type>(<scope>): <subject>

- 详细描述改动了什么
- 为什么这样改
- 有哪些影响
- 影响模块：<本次改动影响的模块列表>

Closes #<issue-number>
```

示例：
```
feat(api): 实现用户 CRUD 接口

- 添加 GET /api/users 用户列表（支持分页、搜索）
- 添加 GET /api/users/:id 用户详情
- 添加 POST /api/users 创建用户（含验证）
- 添加 PUT /api/users/:id 更新用户
- 添加 DELETE /api/users/:id 删除用户（软删除）
- 集成权限中间件，仅管理员可访问

使用 Drizzle ORM + Zod schema 验证
Closes #12
```

### Step 4: 输出建议

向用户展示：

```markdown
## 📝 建议 Commit Message

\`\`\`
<生成的 commit message>
\`\`\`

---
**改动统计**：
- 修改文件：<N> 个
- 新增行数：+<added>
- 删除行数：-<deleted>
- 主要类型：<type>
- 影响 scope：<list>

确认后执行：`git add -A && git commit -m "<message>"`
或直接说"确认提交"
```

## 使用方式

### 手动触发
在对话中说：
- "帮我写个 commit message"
- "提交一下"
- "commit"
- "/skill commit-helper"

### 自动触发（推荐）
在 git 操作流程中作为最后一步：
1. 完成 code review ✅
2. 执行 commit-helper 📝
3. 确认并提交 ✅

## 注意事项

1. **subject 不要以句号结尾**
2. **subject 使用祈使语气**："添加xxx" 而不是 "添加了xxx" 或 "添加 xxx"
3. **body 与 subject 之间空一行**
4. **中文项目用中文 commit message**，国际项目用英文。根据项目现有 commit 风格决定
5. **如果改动太大，建议拆分成多个 commit**：每个 commit 只做一件事
6. **不要在 commit message 中放敏感信息**：API Key、密码、Token 等
7. **body 必须包含影响模块**：列出本次改动影响了哪些模块，让新人一眼看懂改了啥
