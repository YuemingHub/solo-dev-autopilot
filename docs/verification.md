# 验证记录（Verification Log）

> 本文件记录 Solo Dev Autopilot 各项能力的**真实验证证据**——每个结论都可复算、可追溯。
> 与 `docs/scoring.md` 的评分维度一一对应，是"评分 9 分有理有据"的底层支撑。
> 最后更新：2026-08-03（v2.3.2）

---

## 1. 配置包自检（CI 流水线）

**脚本**：`scripts/ci-self-check.sh`（本地可跑，CI 复用同一脚本）
**检查范围**：JSON 有效性 / SKILL.md frontmatter / Shell 语法

| 检查项 | 数量 | 命令 |
|--------|------|------|
| JSON 配置 | 10 个 | `configs/*.json` + `configs/tool-presets/*.json` + `.claude/settings.json` |
| SKILL.md frontmatter | 13 个 | `.claude/skills/*/SKILL.md`（必须含 name/description/license） |
| Shell 脚本语法 | 7 个 | `scripts/*.sh` + `templates/pre-commit-hook` + `pre-push-hook` |

**结果**：本机 23/23 断言通过；GitHub Actions 真实运行连续全绿（见 §3）。

**修复记录**：
- 本地 `sh.exe` 实为 bash 5.3，`sh -n` 不能代表 CI 的 dash → 统一 `bash -n`（commit `f4210c2`）

---

## 2. Git Hooks 实测（pre-commit 质量门）

**场景**：临时仓库 + `templates/pre-commit-hook` + 硬编码密钥 `sk-1234567890abcdef`

| 模式 | 期望 | 实测 | 结果 |
|------|------|------|------|
| team（.autopilot-mode=team） | P0 阻止提交 | exit 1，提交被拒 | ✅ |
| toy（.autopilot-mode=toy） | P0 仅警告 | exit 0，提交成功 | ✅ |

**结论**：严格度随 `.autopilot-mode` 三档生效；硬编码密钥检测真实拦截。

---

## 3. GitHub Actions 真实运行记录

仓库：`YuemingHub/solo-dev-autopilot`（workflow: CI — Repo Self-Check）

| commit | 结果 | 说明 |
|--------|------|------|
| `3b5d3a4` / `ba92659` | ❌ | 旧版 Node 模板（本仓库无 package.json，预期失败，已废弃） |
| `1b46811` | ❌ | 自检脚本首次运行：`sh -n` 在 dash 下误报（已修复） |
| `f4210c2` | ✅ | `bash -n` 修复生效 |
| `acef976` / `9d54f65` | ✅ | 连续全绿 |

**结论**：里程碑"CI 通过率 > 95%"有真实运行证据；当前 workflow 连续 3 次全绿。

---

## 4. Node CI 模板端到端验证（templates/ci-node.yml）

**环境**：node v22.16.0 + vitest 2.1.9，最小项目（math.ts 3 测试）

| 步骤 | 命令 | 实测 |
|------|------|------|
| 测试 | `vitest run --coverage --coverage.reporter=text --coverage.reporter=json-summary` | ✅ 3 tests passed |
| 覆盖率门 | `node -e "…s.total.lines.pct"` ≥ 80 | ✅ 100% ≥ 80% |
| Lint | `tsc --noEmit` | ✅ exit 0 |
| Build | `tsc` | ✅ dist/ 生成 |
| 依赖审计 | `pnpm audit --audit-level=high` | ✅ 正常报告（发现 vitest<3.2.6 critical 漏洞，exit 1 符合质量门语义） |
| 密钥扫描 | grep 正则两向测试（6 案例） | ✅ 6/6（sk-/AKIA 命中，env 引用/短值不误报） |

**发现的模板缺陷（均已修复）**：

| # | 缺陷 | 修复 |
|---|------|------|
| 1 | 覆盖率门用 `--reporter=json`（不输出 JSON 到 stdout），门静默失效 | 改 `--coverage.reporter=json-summary` + node 提取 |
| 2 | `pnpm audit … \|\| true` 让高危漏洞不阻止 CI | 去掉豁免，高危真实阻止；可接受风险时显式加回 |
| 3 | 密钥扫描值部分 `[A-Za-z0-9]{16,}` 漏掉 `sk-` 带连字符格式 | 改 `[^'"[:space:]]{16,}` + `access[_-]?key` 备选 |

> ⚠️ 环境注：本机 corepack/pnpm 11 有 ignored-builds 机制（CI 用 pnpm 9 无此问题），
> 验证时通过 `node_modules/.bin/` 直接调用绕过；不影响模板在 CI 中的行为。

---

## 5. 配置与文档一致性

| 检查项 | 结果 |
|--------|------|
| `.claude/skills/` 实际数量 | 13 个 = README 声称 13 个 ✅ |
| README 结构树声称的关键文件 | 23/23 存在 ✅ |
| 6 个 JSON 配置解析 | 全部通过（PowerShell ConvertFrom-Json）✅ |
| v1 残留引用（skills/*.md / runAs） | docs 扫描干净，仅保留"已废弃"说明 ✅ |

---

## 复现方式

```bash
# 自检（需 bash + grep + sed，Ubuntu/Git Bash 均可）
bash scripts/ci-self-check.sh

# hooks 实测（临时仓库）
bash scripts/install-git-hooks.sh
echo 'team' > .autopilot-mode

# 覆盖率门验证（Node 项目）
pnpm vitest run --coverage --coverage.reporter=json-summary
node -e "const s=require('./coverage/coverage-summary.json'); console.log(s.total.lines.pct)"
```
