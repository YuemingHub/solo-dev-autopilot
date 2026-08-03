---
name: test-runner
description: >
  测试闭环：识别项目技术栈，一键运行单元/集成/E2E 测试，输出覆盖率报告，
  失败时给出具体修复建议。当用户说"跑一下测试" / "测试通过了吗" / "覆盖率多少"
  / "帮我写测试" 时触发。
license: MIT
---

# Test Runner — 测试闭环

## 目标

让"写测试 → 跑测试 → 看覆盖率 → 修复"成为一条顺畅的流水线，消除新手
"不知道测什么、不知道怎么跑、不知道覆盖够不够"的决策负担。

## 工作流程

### Step 1：识别项目技术栈

按优先级探测（只探测一次，不要反复猜）：

| 文件/特征 | 技术栈 | 测试命令 |
|-----------|--------|---------|
| `package.json` + `vitest` 依赖 | Node/Vite | `npm test` 或 `pnpm test` |
| `package.json` + `jest` 依赖 | Node/Jest | `npm test` 或 `pnpm test` |
| `package.json` + `playwright` | E2E | `npm run test:e2e` |
| `pyproject.toml` / `pytest.ini` | Python | `pytest` 或 `uv run pytest` |
| `go.mod` | Go | `go test ./...` |
| `Cargo.toml` | Rust | `cargo test` |
| 无任何测试框架 | 未配置 | 进入 Step 5 引导搭建 |

> ⚠️ 先运行 `ls` / 读取 `package.json` 确认，不要凭目录名猜测。

### Step 2：运行单元测试 + 覆盖率

```bash
# Node (vitest)
pnpm vitest run --coverage
# Node (jest)
npx jest --coverage
# Python
pytest --cov=. --cov-report=term-missing
# Go
go test -cover ./...
# Rust
cargo test
```

**覆盖率基线：>= 80%**（蓝图 7.1 要求）。
- 低于 80%：不阻止，但必须报告差距并给出"补哪些测试提分最快"的建议。
- 高于 90%：表扬并说明保持策略。

### Step 3：运行集成/E2E（如果存在）

- 集成测试：`npm run test:integration`（或等价命令）
- E2E：`npm run test:e2e`（Playwright 等）

E2E 如果依赖外部服务，先检查 `.env` 是否就绪，缺失时提示而不是硬跑。

### Step 4：输出测试报告

按以下格式汇总（必须是工具实测数据，不许编造）：

```markdown
## 🧪 测试报告 — <项目名>

| 项目 | 结果 |
|------|------|
| 单元测试 | ✅ 24 passed / 0 failed（3.2s） |
| 覆盖率 | 86.4%（基线 80%）✅ |
| 集成测试 | ✅ 5 passed |
| E2E | ⏭️ 未配置 |

### 失败项与修复建议
- ❌ <测试名>：<错误摘要>
  - 原因：<推断>
  - 修复：<具体改法>
```

### Step 5：没有测试框架？引导搭建（不替用户做决定）

| 技术栈 | 推荐方案 | 一句话引导 |
|--------|---------|-----------|
| Node/TS | vitest | `pnpm add -D vitest @vitest/coverage-v8` |
| Python | pytest | `pip install pytest pytest-cov` |
| Go | 内置 | `go test ./...` 开箱即用 |
| E2E | Playwright | `npm init playwright@latest` |

先给出最小可跑示例（一个真测试文件），让用户看到绿色通过，再谈覆盖率。

## 规则

1. **实测数据**：所有结果必须来自实际运行输出，禁止编造通过数/覆盖率。
2. **失败必须给修复路径**：只报"测试失败"不给修复建议 = 失职。
3. **先跑单测再跑集成**：单测失败时集成测试大概率也失败，先修底层。
4. **不自动改代码**：测试失败时给出修复建议，等用户确认后再改。
5. **覆盖率看趋势**：单次 100% 不如从 60% 稳步上升到 85% 有价值，关注变化方向。

## 触发方式

- 手动：说"跑一下测试" / "帮我写测试" / "覆盖率多少" / `/skill test-runner`
- 自动：commit 前、deploy-gate 检查前（作为 P1 检查项的数据来源）
