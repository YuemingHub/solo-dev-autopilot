---
name: task-memory
description: >
  项目记忆读写。会话开始时读取项目记忆摘要注入上下文;环境变化(依赖/配置/命令变更)、任务完成、踩坑解决后写入记忆。
  让新会话不用重新摸索,自动获得"这个项目怎么跑、哪些坑踩过"。适合所有项目;不适合无状态的一次性问答。
license: MIT
---

# 项目记忆(task-memory)

> 原则出处:《深入理解 AI Agent》(中文解析见 `references/book/`)第 3 章「用户记忆和知识库」(跨会话记忆、记忆的存储格式与压缩、隐私保护)、第 2 章「上下文工程」(按需加载,避免上下文膨胀)。

## 目标

项目级「第二大脑」:`.agent-memory/` 目录下持续沉淀,新会话自动加载,新手重复踩过的坑只踩一次。

## 目录结构

```
.agent-memory/
├── memory.md            # 主记忆(必读):项目事实、命令、约定、决策
├── env.md               # 环境档案摘要(env-detect/env-setup 维护)
├── troubleshooting.md   # 踩坑记录(问题→原因→解法,按时间倒序)
└── decisions.md         # 架构/技术选型决策记录(可选,项目大时用)
```

## 读写规则

### 会话开始(读)

1. 存在 `.agent-memory/memory.md` → 把**摘要**(不是全文)注入上下文:项目类型、三命令、约定、最新踩坑
2. 结合 `.agentenv.json` 使用;两者缺一就提示跑 env-detect

### 任务过程中/结束时(写)

记录时遵循「精简、可执行、脱敏」:

| 类别 | 写什么 | 例子 |
| --- | --- | --- |
| 命令 | 本项目特有的构建/测试/运行命令 | `uv run pytest tests/api` |
| 约定 | 命名、目录、错误处理惯例 | 服务入口在 src/app/main.py |
| 踩坑 | 问题→原因→解法(带复现命令) | `ImportError` → 需在 .venv 内运行 |
| 决策 | 选型与理由(反悔也有依据) | 用 uv 而非 pip:锁文件可复现 |
| 依赖 | 重要依赖及用途 | playwright 用于 UI 测试 |

更新时机:env-setup 完成、依赖变更 → 更新 env.md 与 memory.md 命令段;dev-loop 熔断或修复成功 → 更新 troubleshooting.md;用户明确告知的偏好/约定 → 立即记录。每次更新控制在 3-5 条以内,避免记忆膨胀。

## 格式规范

### memory.md 主记忆(推荐模板)

```markdown
# 项目记忆
> 自动维护,新会话必读。更新原则:精简、可执行、脱敏。

## 项目事实
- 类型:FastAPI 后端(web-backend);Python 3.12 + uv
- 结构:src/app/main.py 为入口;tests/ 用 pytest

## 常用命令
- 安装: uv sync --locked
- 运行: uv run uvicorn app.main:app --reload --port 8000
- 测试: uv run pytest -q
- 检查: uv run ruff check . && uv run ruff format --check .

## 约定
- 所有配置走环境变量,密钥放 .env(不入库)
- 新增路由必须先写测试
- 命名:模块小写下划线

## 重要依赖
- fastapi、uvicorn:Web 框架
- pytest:测试

## 待办/遗留
- [ ] README 还缺部署一节
```

### env.md 环境档案摘要

```markdown
# 环境档案(由 env-detect/env-setup 维护)
- 检测时间:2026-07-31
- 运行时:python 3.12.8(已装)、uv 0.7(已装)、git 2.4x(已装)
- 缺失:无
- 备注:README 要求 Playwright 浏览器(未装,做 UI 测试前再装)
```

### troubleshooting.md 踩坑记录(倒序)

```markdown
# 踩坑记录
## 2026-07-31 uv sync 报 "failed to resolve"
- 现象:uv sync --locked 失败
- 原因:pyproject.toml 依赖版本与锁文件不一致
- 解法:改依赖后用 uv lock 重新生成锁文件,再 uv sync
- 复现:uv sync --locked
```

每条四要素:**现象 / 原因 / 解法 / 复现命令**。超过 20 条就把最老的 5 条归档或删除。

### decisions.md 决策记录(可选)

```markdown
# 决策记录
## 2026-07-31 选 uv 作为包管理器
- 背景:需要锁文件保证可复现
- 备选:pip + requirements.txt
- 决定:uv,理由:锁文件 + 速度快
- 状态:已采用
```

## 隐私与安全(第 3 章:脱敏)

- **绝不记录**真实 API Key、密码、令牌、Cookie(一律写 `<env:XXX>` 引用)
- 不记录用户不愿公开的个人信息;记录前如不确定,先问
- 记忆文件可以进 git(不含密钥),但建议在 README 说明用途

## 维护纪律

1. 更新别贪多:每次 3-5 条
2. 写完必读一遍:「新会话只看 memory.md 能跑起来吗?」
3. 密钥类信息一律写 `<env:变量名>`,不写值
4. 与 .agentenv.json 信息重复时,以 .agentenv.json 为准,memory.md 只写「差异和备注」
