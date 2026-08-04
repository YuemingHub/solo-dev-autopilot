---
name: env-setup
description: >
  项目环境自动搭建。在 env-detect 之后、或用户要求"搭环境/装依赖/装工具/初始化环境/环境跑不起来/缺 python/node/go"时使用:
  自动补齐运行时、安装依赖、生成 .env、配置代码检查、初始化 git、写 AGENTS.md,最后冒烟验证并汇报。
  适合从零初始化项目或修复环境。不适合改业务代码。
license: MIT
---

# 环境自动搭建(env-setup)

> 原则出处:《深入理解 AI Agent》(中文解析见 `references/book/`)第 1 章 1.2「Harness 工程」(约束、验证、纠正——熔断与静默重试)、第 5 章 5.1.5「项目文档化」、5.1.8「实现技巧 · 命令执行状态持久化、环境信息动态注入」。目标:让新手一条命令都不用手敲,环境直接可用、可复现。

## 目标

把当前项目从「缺环境」变成「可运行」:补齐运行时与包管理器 → 装依赖 → 配 .env → 配检查工具 → 建 AGENTS.md → 冒烟验证。全程自动,只有高风险动作才询问用户。

## 前置

1. 若没有 `.agentenv.json`,先调用 env-detect
2. 确认网络可用(下载需要);确认用户已同意自动安装(全局 AGENTS.md 默认允许)

## 执行流程(每步都遵守「验证-纠正」循环)

### 1. 补齐运行时(按 .agentenv.json 的 runtimes.missing)

优先「已有则复用,缺失才安装」,安装用 winget 或官方安装器(配方见下表);**装完必须重新探测验证版本**(新开 shell 再 `--version`),并注意 PATH 持久化。

| 运行时 | 验证命令 | 缺失时安装命令 |
| --- | --- | --- |
| Python | `py --version` / `py -0p` | `winget install --id Python.Python.3.12 -e --source winget` |
| uv | `uv --version` | `py -m pip install --user uv` 或 `winget install --id astral-sh.uv -e` |
| Node LTS | `node --version` | `winget install --id OpenJS.NodeJS.LTS -e --source winget`(corepack enable 启用 pnpm/yarn) |
| Go | `go version` | `winget install --id GoLang.Go -e --source winget` |
| Rust | `rustc --version`、`cargo --version` | 运行 https://win.rustup.rs(rustup-init,需 MSVC Build Tools) |
| Java JDK21 | `java -version` | `winget install --id EclipseAdoptium.Temurin.21.JDK -e --source winget` |
| Maven/Gradle | `mvn -version` / `gradle --version` | `winget install --id Apache.Maven -e` / `winget install --id Gradle.Gradle -e` |
| C++/CMake | `cl` 或 `gcc --version` | `winget install --id Microsoft.VisualStudio.2022.BuildTools -e`(勾 C++ 工作负载)+ `winget install --id Kitware.CMake -e` |
| .NET SDK | `dotnet --version` | `winget install --id Microsoft.DotNet.SDK.8 -e` |
| PHP | `php --version` | `winget install --id PHP.PHP.8.3 -e` |
| Ruby | `ruby --version` | `winget install --id RubyInstallerTeam.RubyWithDevKit.3.2 -e` |
| Git | `git --version` | `winget install --id Git.Git -e --source winget`(所有项目必备) |
| Docker Desktop | `docker --version` | `winget install --id Docker.DockerDesktop -e`(docker-compose.yml 存在时) |

镜像(网络受限时按需设置,并在汇报中明示):pip `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`;npm `npm config set registry https://registry.npmmirror.com`;uv 用 `UV_DEFAULT_INDEX` 环境变量。

### 2. 创建虚拟环境(解释型语言)

- Python:已有 `uv.lock` → `uv sync --locked`;否则 `uv venv` 或 `py -m venv .venv`。激活规则写进 README/AGENTS.md
- Node:依赖装在本地 node_modules,无需全局

### 3. 安装依赖(锁文件优先,保证可复现)

| 包管理器 | 有锁文件 | 无锁文件 |
| --- | --- | --- |
| uv | `uv sync --locked` | `uv sync`(生成锁) |
| pip | — | `python -m pip install -e .` 或按 requirements.txt |
| pnpm | `pnpm install --frozen-lockfile` | `pnpm install` |
| npm | `npm ci` | `npm install` |
| yarn | `yarn install --frozen-lockfile` | `yarn install` |
| go | `go mod download`(go.sum 校验) | `go mod tidy` |
| cargo | `cargo build --locked` | `cargo build` |
| maven/gradle | — | `mvn -q package -DskipTests` / `gradle build -x test` |

失败 → 走下方「验证-纠正循环」。**安装类命令默认超时 600s**,不要手改锁文件。

### 4. 生成 .env

- 有 `.env.example`:复制为 `.env`,值为空或占位符,**绝不写真实密钥**
- 无 `.env.example`:根据代码里引用的环境变量生成模板 `.env.example` + `.env`,注释说明每个变量的含义和获取方式
- 检查 `.gitignore` 是否包含 `.env`、`.env.local`、`.venv`、`node_modules`、`__pycache__`、`target/`、`dist/` 等,没有就补上

### 5. 配置代码检查与格式化

按技术栈配好(默认推荐,用户可后改),配完跑一遍确认零错误(存量问题记录到 notes,不强制全修):

- Python:ruff(格式+lint)+ pytest,在 pyproject.toml 配 `[tool.ruff]` 与 `[tool.pytest.ini_options]`
- Node/TS:eslint + prettier(或统一 biome),vitest/jest
- Go:gofmt/go vet 开箱即用;Rust:rustfmt/clippy 开箱即用

### 6. git 初始化 + 首次提交

- 无 `.git` → `git init -b main`;确认用户级 `user.name`/`user.email` 已配,未配则询问用户(不要自作主张)
- 首次提交:包含脚手架与配置,**不含 .env 与依赖产物**

### 7. 生成 AGENTS.md(项目指令文件,按书 5.1.5「项目文档化」)

```markdown
# 项目说明(由 env-setup 自动生成,可修改)
## 技术栈
- 语言/框架:<...>(来自 .agentenv.json)
## 常用命令
- 安装依赖: <install>   运行: <run>   测试: <test>   代码检查: <lint>   构建: <build>
## 环境变量
见 .env.example;真实密钥绝不写入任何代码文件。
## 代码约定
- <语言惯例、命名、模块边界;按技术栈给默认值>
- 修改代码后必须通过测试与 lint(见 dev-loop)
## 禁区
- 不要删除 .git 历史;不要提交 .env;不要升级锁文件之外的依赖大版本
```

### 8. 冒烟验证(完成标准 = 能跑通)

- 执行最小可运行命令:优先 run(有服务器就启动再关掉)、否则 build、再否则 test
- 冒烟通过 → 汇报完成;失败 → 进入「验证-纠正循环」

## 验证-纠正循环(Harness: 重试 → 修复 → 熔断)

每一步(安装/冒烟)失败时:

1. **分类**:读错误输出,判定类型——网络(超时/镜像)、权限(拒绝访问/UAC)、依赖冲突(版本/平台)、配置(路径/PATH/环境变量)、语法(代码本身)
2. **静默重试**:网络类错误指数退避重试(2s→4s→8s,最多 3 次),不重复打印同一错误
3. **定向修复**:依赖冲突→按错误信息调整版本或换镜像;配置类→检查 PATH、.env、工作目录;语法类→修复配置/入口文件
4. **熔断**:同一命令连续失败 3 次或累计 5 次 → 停止,把「做了什么、失败输出、你的判断、建议下一步」汇报给用户,并写入 `.agent-memory/troubleshooting.md`,不再盲目重试

## 高风险动作(先询问,再执行)

- 安装系统级软件(winget 安装、下载运行时可执行文件)
- `pip install` 全局(-g)/`npm install -g`
- 覆盖用户已有的未读文件(如已有 .env、已有 AGENTS.md 内容冲突)
- 修改 PATH/环境变量注册表、系统级配置

## 汇报格式

装了什么(版本)、激活了什么、怎么跑/怎么测(命令)、改动/生成的文件清单、遗留问题(存量 lint、未配的密钥)。用中文、面向新手。
