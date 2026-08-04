---
name: dev-loop
description: >
  开发循环质量门禁与自动修复。每次修改代码之后、任务声称"做完了"之前、提交代码之前,或构建/测试/lint 失败时使用:
  自动跑格式检查→lint→类型检查→构建→测试,失败则诊断分类并自动修复,通过后做提交前审查。
  让新手不用手动敲一条验证命令。不适合环境搭建(用 env-setup)和写文档等无代码变更任务。
license: MIT
---

# 开发循环(dev-loop)

> 原则出处:《深入理解 AI Agent》(中文解析见 `references/book/`)第 1 章 1.2「Harness 工程」(验证、纠正、熔断、静默重试、约束优先于指导)、第 5 章 5.1.5「测试驱动与验收标准」(测试通过才算完成)、5.1.6「故障恢复」(错误分类→重试→降级→熔断→人工升级)、5.1.8「实现技巧 · 状态栏与上下文管理」。

## 核心原则

1. **测试通过才算完成**——代码"写完"不是完成,验证通过才是
2. **反馈越快越好**——改一个文件先跑单文件 lint/类型检查,别等全量
3. **约束优先于指导**——用工具和门禁兜底,而不是靠"记得检查"
4. **静默重试,定向修复,熔断升级**——同一错误不无限重试

## 触发时机

- 每完成一个功能/修复,在汇报"完成"前
- 用户说"测试一下/跑一下/为什么报错/帮我修"
- 提交/推送前(强制走一次)
- 依赖或配置变更后(install 之后先验证再继续写)

## 执行流程

### 1. 注入状态栏(上下文管理)

开始前向对话注入一行摘要:`目录=<path> | 分支=<git branch> | 变更=<n> 文件(+a/-b) | 最近提交=<msg> | 环境=.agentenv.json 已/未就绪`

### 2. 按技术栈跑验证序列

序列统一为 `format → lint → typecheck → build → test`(不需要的环节跳过)。已配置的项目直接用 AGENTS.md 里声明的命令。各技术栈命令:

| 技术栈 | format | lint | typecheck | build | test |
| --- | --- | --- | --- | --- | --- |
| Python(uv) | `uv run ruff format --check .` | `uv run ruff check .` | `uv run mypy src`(配了才有) | `uv build`(库项目) | `uv run pytest` |
| Node/TS | `prettier --check .` | `eslint .` | `tsc --noEmit` / `vue-tsc --noEmit` | `npm run build` | `npm test` / `vitest run` |
| Go | `gofmt -l .` | `go vet ./...` | `go build ./...` | `go build ./...` | `go test ./...` |
| Rust | `cargo fmt --check` | `cargo clippy -- -D warnings` | `cargo build`(有锁用 --locked) | `cargo build` | `cargo test` |
| Java(Maven) | — | `mvn checkstyle:check`(有则) | `mvn -q compile` | `mvn -q compile` | `mvn -q test` |

pip 项目:`python -m ruff` / `python -m pytest`;Django:`python manage.py check` 加进序列。

### 3. 失败 → 诊断分类 → 自动修复

读完整错误输出,按类别处理:

| 类别 | 特征 | 修复策略 |
| --- | --- | --- |
| 语法 | ParseError/SyntaxError/TS1005 | 直接修对应代码,重跑单文件检查 |
| 类型 | type mismatch 等 | 读报错位置,修正类型标注/调用方式 |
| 逻辑 | 测试断言失败 | 读测试与实现,判断是改代码还是改测试(改测试要谨慎,优先改实现) |
| 依赖 | ModuleNotFound/No module/缺少依赖 | 按 env-setup 配方装依赖或调整版本,不要手改锁文件 |
| 环境 | PATH/端口占用/命令不存在 | 环境类问题转 env-setup,别在代码里打补丁 |
| 已存在 | 改动前就有的存量问题 | 记录不阻塞,除非影响本次改动 |

修复后从对应步骤重跑(单文件优先),通过再跑全量。lint 类的机械问题(import 排序、未用变量、格式)优先用 `ruff check --fix` / `eslint --fix` / `prettier --write` 自动修。

### 4. 熔断与升级(Harness)

- 同一错误连续 3 次修复失败,或全量验证累计 5 次失败 → **停止自动重试**
- 汇报:目标、做了什么、失败输出摘要、你的假设、建议的两条路径(继续修 vs 简化需求)
- 写入 `.agent-memory/troubleshooting.md` 踩坑记录(见 task-memory)

### 5. 提交前审查

全部通过后,`git diff` 检查:
- 调试残留(console.log/print/debugger/TODO 无关代码)
- 硬编码密钥(见 harness-guard;密钥必须走 .env)
- 注释/文档与代码不一致(同步更新)
- 意外改动(只提交本次任务相关文件,`git add` 要精确)

### 6. 汇报

- 验证结果(哪些过了、用了什么命令)、改了哪些文件、为什么、遗留问题与建议
- 更新 `.agent-memory/`(命令、约定、踩坑)

## 常见错误速查(2026-07 实测补充)

- `ModuleNotFoundError`:装依赖(env-setup 配方),或检查是否在 `.venv` 内运行
- `ImportError` 相对导入:检查包结构 `__init__.py` 与运行位置
- pytest collection error:检查 `testpaths` 与文件名 `test_*.py`
- **typer/click 兼容坑**:`app.registered_commands` 有命令但 `--help` 不显示、运行报 `Got unexpected extra argument` → 是 typer+click 版本组合问题,换用标准库 `argparse`(见 project-scaffold 模板)
- `Cannot find module 'x'`(Node):缺依赖 `pnpm add x` 或版本不兼容
- TS 报错优先按报错行修类型,不要 `@ts-ignore`(除非有明确理由并注释)
- 端口占用 `EADDRINUSE`:换端口或杀进程,别改代码
- Go `import cycle not allowed`:抽公共包;`go.sum` 不一致:`go mod tidy` 后重跑
- 命令报"不是内部或外部命令":PATH 问题 → 环境类,转 env-setup
- 长命令加超时(安装类 600s、构建/测试 300s、普通 120s)
- 测试随机失败(flaky):重跑一次区分;连续两次失败才当真实 bug
- 一次只修一类错误,修完重跑,别同时改多处

## 完成标准

`format/lint/typecheck/build/test` 全部通过(未配置环节跳过),或剩余失败均为「已存在的存量问题」并已记录。

## 高风险动作(询问后执行)

- `git push` / `git reset --hard` / 删除文件 / 覆盖未读文件 / 全局安装
- 大量代码的自动批量重写(先给用户看 diff 计划)
