---
name: context-map
description: >
  扫描整个项目，生成结构化的"代码地图"。这是会话恢复的核心机制。
  每次会话结束时自动触发，下次启动时 AI 加载代码地图即可瞬间恢复全部上下文。
  解决新手最大的隐性成本：每次重新开会话后 AI 不记得之前做了什么。
runAs: subagent
tools: [read_file, list_directory, search_content, glob]
tags: [context, memory, session-recovery, codebase-understanding]
priority: critical
---

# Context Map — 项目代码地图生成器

## 目标

为当前项目生成一份**结构化的、可被 AI 快速加载的代码地图**。这份地图是 AI 跨会话记忆的载体。

## 执行步骤

### Step 1: 收集项目元信息

读取以下文件（如果存在）：
- `package.json` 或 `pyproject.toml` 或 `Cargo.toml` 或 `go.mod` → 提取项目名、依赖、脚本
- `README.md` → 提取项目描述
- `.gitignore` → 了解项目类型
- 任何已有的 `CODEMAP.md` 或 `PROJECT-MEMORY.md` → 增量更新

### Step 2: 构建目录结构树

```
执行：list_directory(root_path, recursive=true, max_depth=4)
```

过滤掉以下目录/文件（不纳入地图）：
- `node_modules/`, `.next/`, `dist/`, `build/`, `__pycache__/`, `.cache/`
- `.git/`, `.DS_Store`
- `*.lock`, `package-lock.json`, `yarn.lock`（除非需要分析依赖）

### Step 3: 分析每个核心模块

对每个顶层源码目录（如 `src/`, `app/`, `lib/`, `components/` 等）：

1. **识别模块职责**：通过阅读入口文件（index.ts, main.py, mod.rs 等）判断
2. **记录关键文件**：列出该模块中最重要的 3-5 个文件
3. **追踪依赖关系**：该模块 import/require 了哪些其他模块
4. **标记当前状态**：
   - 🟢 稳定可用
   - 🟡 开发中 / 有已知问题
   - 🔴 需要重构 / 有严重问题
   - ⚪ 计划中 / 尚未开始

### Step 4: 分析数据流

追踪项目的数据流向：
```
用户请求 → 入口 → [中间件/路由] → [业务逻辑] → [数据层] → 数据库
                                    ↘ [响应] → 用户
```

特别关注：
- API 端点列表（路由定义）
- 数据库模型/Schema 定义
- 认证/授权流程
- 外部服务集成

### Step 5: 输出代码地图

将结果写入 `<project-root>/CODEMAP.md`，格式如下：

```markdown
# 🗺️ Code Map — <project-name>

> 最后更新：<timestamp>
> 由 Solo Dev Autopilot 自动生成

## 项目概览

| 属性 | 值 |
|------|-----|
| 名称 | <project-name> |
| 技术栈 | <language> + <framework> + <database> |
| 当前阶段 | <development/testing/production> |
| 核心功能描述 | <一句话>

## 目录结构

<精简的树形结构，只显示到 2-3 层深度>

## 核心模块

### <module-name>
- **职责**：<一句话>
- **关键文件**：
  - `path/to/file1.ts` — <作用>
  - `path/to/file2.ts` — <作用>
- **依赖**：<list of modules it depends on>
- **状态**：🟢🟡🔴⚪
- **备注**：<重要注意事项>

（重复每个模块）

## 数据流图

<ASCII 或 Mermaid 格式的数据流>

## API 端点

| 方法 | 路径 | 功能 | 状态 |
|------|------|------|------|
| GET | `/api/users` | 获取用户列表 | 🟢 |

（重复每个端点）

## 数据模型

| 模型 | 表/集合 | 关键字段 | 备注 |
|------|---------|---------|------|
| User | users | id, email, name | |

## 待办事项 & 已知问题

- [ ] <待办项>
- [x] <已完成>
- ⚠️ <已知问题及影响>

## 最近变更

<最近 3-5 次有意义的改动，从 git log 或记忆中提取>
```

## 使用方式

### 自动触发（推荐）
配置在工具的 Stop hook 中，每次会话结束时自动执行。

### 手动触发
在对话中说：
- "生成代码地图"
- "更新代码地图"
- "帮我梳理一下项目现状"
- "/skill context-map"

### 加载已有地图
新会话开始时说：
- "加载 CODEMAP.md"
- "根据代码地图恢复上下文"
- "先读一下项目代码地图"

## 注意事项

1. **增量更新优先**：如果已存在 CODEMAP.md，在其基础上更新而非全量重写
2. **保持简洁**：地图的目标是让 AI 在 10 秒内理解项目全貌，不是写文档
3. **状态标记最重要**：🟢🟡🔴⚪ 让 AI 瞬间知道哪里可以动、哪里要小心
4. **避免冗余**：不要把每个文件都列出来，只列关键的
5. **与 PROJECT-MEMORY.md 配合**：代码地图是结构快照，项目记忆是约定/偏好，两者互补
