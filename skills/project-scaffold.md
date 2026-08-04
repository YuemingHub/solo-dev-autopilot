---
name: project-scaffold
description: >
  从零创建新项目脚手架。当用户说"新建一个项目/帮我开始写个 XX/初始化一个 Python 网站/从零开始开发"且目录为空或接近为空时使用:
  选定技术栈、生成推荐目录结构与核心配置文件、调 env-setup 搭好环境、冒烟验证 hello world。
  不适合已有代码的项目(用 env-detect + env-setup)。
license: MIT
---

# 项目脚手架(project-scaffold)

> 原则出处:《深入理解 AI Agent》(中文解析见 `references/book/`)第 5 章 5.1.5「项目文档化与任务理解」(先设计后实现)、5.1.8「实现技巧 · 即时代码反馈」。给新手一个「官方推荐的起跑姿势」,避免从乱糟糟的目录开始。

## 目标

把一个空目录变成「结构规范、环境已装好、能跑通最小示例」的项目起点,同时生成 AGENTS.md,让后续所有开发会话有据可依。

## 流程

### 1. 确认技术栈(必要询问点)

- 用户没指定时,问清楚:语言/框架(Python? Node? Go?…)、项目类型(CLI? Web 后端? Web 前端? 库? 数据脚本?)
- 新手没有偏好 → 推荐「最容易跑通的组合」:CLI 用 Python+uv;Web 后端用 Python+FastAPI+uv 或 Node+Express;Web 前端用 Node+Vite+React(TS)
- 确认版本策略:用当前 LTS / 稳定版,不要追最新大版本

### 2. 生成结构与核心文件(模板见下)

通用骨架(以 Python+uv 为例):

```
project/
├── src/<package>/            # 源码(包内 import 友好)
│   ├── __init__.py
│   └── main.py               # 入口
├── tests/
│   └── test_main.py          # 一个真实能跑的测试
├── pyproject.toml            # 元数据 + ruff/pytest 配置
├── uv.lock                   # (由 uv sync 生成)
├── README.md                 # 是什么、怎么装、怎么跑、怎么测
├── .gitignore                # .venv/.env/__pycache__/dist...
├── .env.example              # 环境变量模板(占位符)
└── AGENTS.md                 # 项目说明书(见 env-setup 第 7 步模板)
```

生成原则:一个能跑的 hello world 优先于「大而全但跑不动」——测试必须真实断言输出;配置即文档;README 写「新手能照抄的三条命令」:install / run / test。

### 3. 调 env-setup 搭环境

把脚手架变成「已安装、能冒烟」的活项目(依赖安装、.env、lint 配置、git init、AGENTS.md 全在 env-setup 里)。

### 4. 冒烟验证

跑测试 → 必须通过;能启动的服务启动一次再停。失败 → 走 env-setup 的「验证-纠正循环」,修复到冒烟通过为止。

### 5. 汇报与首次提交

汇报:目录结构、怎么跑、怎么测、下一步建议。如已 git init:提交脚手架(不含 .env),建议用户开第一个分支。

## 各技术栈模板(最小可运行)

### Python CLI(argparse,零依赖,最稳)

> 2026-07 实测:typer+click 在当前 Python 3.12 环境存在「子命令注册后不生效,`--help` 不显示命令,运行报 `Got unexpected extra argument`」的兼容问题(typer 0.25~0.27 均复现)。新手脚手架默认用标准库 `argparse`;要用 typer 时先确认 `uv run myproject hello` 能路由到子命令,不行就回到 argparse。

```toml
# pyproject.toml
[project]
name = "myproject"
version = "0.1.0"
description = "A tiny CLI scaffolded by the agent"
requires-python = ">=3.10"
dependencies = []

[project.scripts]
myproject = "myproject.main:main"

[dependency-groups]
dev = ["pytest", "ruff"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/myproject"]

[tool.ruff]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
```

```python
# src/myproject/__init__.py
__version__ = "0.1.0"

# src/myproject/main.py
import argparse

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="myproject", description="A tiny CLI.")
    p.add_argument("--name", default="world", help="who to greet")
    return p

def main() -> None:
    args = build_parser().parse_args()
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()
```

```python
# tests/test_main.py
from myproject.main import build_parser

def test_parser_default():
    assert build_parser().parse_args([]).name == "world"

def test_parser_name():
    assert build_parser().parse_args(["--name", "Bob"]).name == "Bob"
```

跑:uv sync → uv run myproject --name Bob → uv run pytest -q → uv run ruff check .

### Python Web 后端(FastAPI + uv)

- pyproject 同上(无 `[project.scripts]`),dependencies = ["fastapi", "uvicorn[standard]"]
- 入口 `src/myproject/main.py`:`app = FastAPI()` + 一个 `GET /health` 返回 `{"status":"ok"}`
- 测试用 `fastapi.testclient.TestClient`,断言 `GET /health` 200 且 body 正确

### Node CLI(tsx + vitest,零构建复杂度)

```json
// package.json
{
  "name": "myproject",
  "version": "0.1.0",
  "type": "module",
  "bin": {"myproject": "src/main.ts"},
  "scripts": {
    "dev": "tsx src/main.ts",
    "test": "vitest run",
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {"tsx": "^4", "typescript": "^5", "vitest": "^2"}
}
```

```ts
// src/main.ts
export function hello(name: string): string {
  return `Hello, ${name}!`;
}
console.log(hello("world"));
```

```ts
// tests/main.test.ts
import { describe, it, expect } from "vitest";
import { hello } from "../src/main";

describe("hello", () => {
  it("greets", () => expect(hello("world")).toBe("Hello, world!"));
});
```

### Node Web 前端(Vite + React + TS)

`pnpm create vite@latest . --template react-ts` 生成基础骨架(官方路径最稳,不要手写 Vite 配置);补 `pnpm add vitest @testing-library/react` 与 `"test": "vitest run"`;补一个真实测试:渲染 `<App />` 断言标题出现。

### Go 服务(cmd + internal 布局)

```
myproject/
├── go.mod
├── cmd/server/main.go          # 入口:http.ListenAndServe + /health
├── internal/handler/health.go   # handler 拆进 internal
└── internal/handler/health_test.go
```

```go
// internal/handler/health_test.go
package handler

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHealth(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/health", nil)
    rr := httptest.NewRecorder()
    Health(rr, req)
    if rr.Code != http.StatusOK {
        t.Fatalf("status = %d", rr.Code)
    }
}
```

### Rust CLI

```
myproject/
├── Cargo.toml    # [package] + [[bin]] src/main.rs
├── src/main.rs   # println!("Hello, world!");
└── tests/cli.rs
```

```rust
// tests/cli.rs
#[test]
fn prints_hello() {
    let out = std::process::Command::new(env!("CARGO_BIN_EXE_myproject"))
        .output().unwrap();
    assert!(String::from_utf8_lossy(&out.stdout).contains("Hello, world!"));
}
```

### Java(Spring Boot 最小版,Maven)

推荐用 Spring Initializr(https://start.spring.io)生成的骨架,而不是手写全部 XML;最小集 spring-boot-starter-web + spring-boot-starter-test;一个 `@RestController` 的 `/health` + `@SpringBootTest` 冒烟测试。

### 通用文件模板(所有项目)

```gitignore
# .gitignore(按语言裁剪)
.venv/
__pycache__/
*.pyc
node_modules/
dist/
.env
.env.local
target/
*.class
```

```markdown
# README.md
# <项目名>
一句话说明。
## 环境要求
<语言版本>
## 安装
<install 命令>
## 运行
<run 命令>
## 测试
<test 命令>
```

```markdown
# .env.example
# 每个变量的含义和获取方式写注释,值留空或占位
API_KEY=
DATABASE_URL=
```

AGENTS.md 模板见 env-setup 第 7 步。

## 边界

- 不要生成超出用户要求的框架代码(做 CLI 不要顺手塞数据库)
- 新手项目默认最小依赖集:先跑通,再按需加
- 目录已有少量文件(非空)→ 先 env-detect,不要覆盖
