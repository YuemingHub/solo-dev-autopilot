---
name: env-detect
description: >
  项目环境侦测。当进入新项目/新工作目录、用户问"这是什么项目/怎么运行/需要什么环境/搭环境/配环境/环境有问题"、
  或任务涉及修改依赖清单(pyproject.toml、package.json、go.mod 等)时使用:扫描项目文件与技术栈,检查已安装工具链,
  输出结构化环境档案 .agentenv.json 和中文摘要。不适合已有档案且项目未变化时的纯编码任务。
license: MIT
---

# 项目环境侦测(env-detect)

> 原则出处:《深入理解 AI Agent》(github.com/bojieli/ai-agent-book,中文解析见 `references/book/`)第 5 章 5.1.5「项目文档化与任务理解」、5.1.8「实现技巧 · 环境信息动态注入」。检测在先、搭建在后,避免新手盲目装错环境。

## 目标

扫描当前工作目录,判定「这是什么项目、需要什么工具链、本机缺什么」,写出一份结构化环境档案供 env-setup / dev-loop / task-memory 消费,并给用户一段一眼看懂的中文摘要。

## 输入输出

- 输出文件:项目根目录 `.agentenv.json`(每次运行整体覆盖)
- 环境摘要写入 `.agent-memory/env.md`(若项目有 task-memory 目录)

## 步骤

### 1. 读项目指纹

用 Glob/Read 查看项目根目录(和常见子目录 `src/`、`app/`),按下方指纹表匹配技术栈。判定顺序:锁文件优先,再读清单文件,再看源码文件。

| 语言 | 指纹文件 | 包管理器优先级 |
| --- | --- | --- |
| Python | `pyproject.toml`、`requirements.txt`、`setup.py`、`Pipfile`、`uv.lock`、`*.py` | uv → pip → poetry |
| Node/前端 | `package.json`、`pnpm-lock.yaml`、`yarn.lock`、`package-lock.json`、`tsconfig.json`、`*.ts`/`*.js` | pnpm → npm → yarn |
| Go | `go.mod`、`*.go` | go mod |
| Rust | `Cargo.toml`、`*.rs` | cargo |
| Java/Kotlin | `pom.xml`、`build.gradle`、`build.gradle.kts`、`*.java` | Maven → Gradle |
| C/C++ | `CMakeLists.txt`、`Makefile`、`*.c`/`*.cpp`/`*.h` | cmake/make |
| .NET | `*.csproj`、`*.sln` | dotnet |
| PHP | `composer.json` | composer |
| Ruby | `Gemfile` | bundler |
| 多栈/部署 | `docker-compose.yml`、`Dockerfile`、`*.sql` + 任意后端指纹 | — |

框架识别:读 `package.json` 的 dependencies(react/vue/svelte/next/nuxt/express/nestjs)和 Python 入口文件的 import(fastapi/flask/django/click/typer)与 `pyproject.toml` 的 `[project.dependencies]`。

### 2. 检查工具链现状

对判定出的「必需工具链」逐个探测(用 Cmd 或 PowerShell),命令如下:

| 工具 | 探测命令(已有则输出版本) |
| --- | --- |
| Python | `py -0p`(列所有)、`python --version` |
| uv | `uv --version`;pip:`pip --version` |
| Node | `node --version`、`npm --version`、`pnpm --version`、`yarn --version` |
| Go | `go version` |
| Rust | `cargo --version`、`rustc --version` |
| Java | `java -version`、`mvn -version`、`gradle --version` |
| CMake/C++ | `cmake --version`、`cl` / `gcc --version` |
| .NET | `dotnet --version`;PHP:`php --version`;Ruby:`ruby --version` |
| Git | `git --version`(所有项目必备) |
| Docker | `docker --version`(docker-compose.yml 存在则必需) |

- 已有:记录真实版本号;缺失:标记 missing,交 env-setup 安装
- 探测失败不代表不存在,可交叉用 `where.exe <tool>` / `Get-Command` 复核

### 3. 读项目约定与凭据指引

- 是否存在 `.env.example`、README(提取"如何安装/如何运行/如何测试"段落)、`.gitignore`、CI 配置(`.github/workflows`、`.gitlab-ci.yml`)
- 是否存在 `AGENTS.md` / `CLAUDE.md`(项目给 Agent 的指令,优先遵守)
- 注意 `.env`、密钥类文件**只看有没有、不看内容**

### 4. 汇总为 .agentenv.json

按以下 schema 输出(缺省字段用 null,不要编造):

```json
{
  "detected_at": "2026-07-31T00:00:00Z",
  "project_type": "web-backend|web-frontend|cli|library|desktop|data|ml|game|multi-stack|unknown|empty",
  "stack": {
    "language": ["python"],
    "language_version_hint": ">=3.10",
    "framework": ["fastapi"],
    "package_manager": "uv",
    "lockfile": "uv.lock"
  },
  "runtimes": {
    "required": ["python", "uv", "git"],
    "installed": {"python": "3.12.8"},
    "missing": ["uv"]
  },
  "extras": {"docker": false, "database": "sqlite", "gpu": false, "browser": false},
  "commands": {
    "install": "uv sync --locked",
    "build": null,
    "test": "uv run pytest",
    "lint": "uv run ruff check .",
    "run": "uv run uvicorn app.main:app --reload"
  },
  "dotenv_example": true,
  "has_agents_md": false,
  "notes": ["README 要求 Python 3.11+ 和 Playwright 浏览器"]
}
```

`commands` 尽量从 README/CI/锁文件推导;推导不出就留 null 交给 env-setup 冒烟时确认。

### 5. 摘要与记忆

- 给用户中文摘要:项目类型 → 技术栈 → 本机已装/缺失 → 下一步(建议调用 env-setup)
- 若项目有 `.agent-memory/`,把档案摘要写入 `.agent-memory/env.md`(见 task-memory)

## 边界

- 只读操作,不安装、不修改任何文件(只写 `.agentenv.json` 和记忆文件)
- 目录为空 → `project_type: "empty"`,提示用户考虑 project-scaffold
- 多技术栈项目(monorepo)记录主栈,并在 notes 中列出所有检测到的栈
- 判定不了就如实写 `unknown`,不要猜
