---
name: ci-helper
description: >
  CI 助手：配置 GitHub Actions CI 流水线（lint → test → build → 依赖审计 →
  密钥扫描），本地模拟 CI 检查序列，读取/诊断 CI 失败。当用户说"配置 CI"
  / "CI 挂了" / "为什么 CI 失败" / "加个自动化检查" 时触发。
license: MIT
---

# CI Helper — 持续集成助手

## 目标

让"CI 一键配置、失败可诊断、通过率 > 95%"成为常态。CI 是 solo 开发者的
**免费质量门**——GitHub 免费额度够个人项目用，配置一次长期受益。

## 工作流程

### Step 1：检查现状

```bash
ls .github/workflows/ 2>/dev/null
```

- 已有 ci.yml → 直接进入 Step 3（诊断或增强）
- 没有 → 进入 Step 2（生成）

### Step 2：生成 CI 模板

将 `templates/ci-node.yml`（Node 项目 CI 模板）复制到目标项目的 `.github/workflows/ci.yml`，并按技术栈调整：

| 技术栈 | 关键改动 |
|--------|---------|
| Node/pnpm | 包管理器用 pnpm，加 `--frozen-lockfile` |
| Python | 用 `actions/setup-python` + `pip install -e .[dev]` |
| Go | `actions/setup-go` + `go test ./...` |
| 前端 | 构建步骤换成 `npm run build` |

生成后必须检查 `.gitignore` 是否忽略 `node_modules` / `dist` / `.env`——
CI 拉取的是仓库内容，忽略错了会导致缓存污染或密钥泄露。

### Step 3：本地模拟 CI 序列（CI 挂了先本地复现）

按 CI 顺序在本地执行同一套命令，用二分法定位失败步骤：

```bash
# 1. lint
pnpm lint          # 或 npm run lint
# 2. test（含覆盖率）
pnpm test
# 3. build
pnpm build
# 4. 依赖审计（仅高危）
npm audit --audit-level=high
# 5. 密钥扫描
git diff HEAD | grep -iE "(api[_-]?key|secret|password|token)[[:space:]]*[:=][[:space:]]*['\"][A-Za-z0-9]{16,}"
```

哪一步失败，CI 就在哪一步失败——本地和 CI 的差异通常来自：
- 环境变量缺失（最常见）
- lock 文件与 package.json 不一致（`--frozen-lockfile` 报错）
- 平台差异（Windows 路径 / bash 命令）
- 未提交文件（CI 只看到已 push 的内容）

### Step 4：读取/诊断远程 CI 状态

```bash
# GitHub CLI（优先）
gh run list --limit 5
gh run view <run-id> --log-failed
# 无 gh CLI：让用户贴 CI 日志链接，或提示安装 gh
```

诊断输出格式：

```markdown
## 🔧 CI 诊断 — <workflow> #<run-id>

- 状态：❌ failed（第 3/5 步 build 失败）
- 失败日志摘要：<关键错误行>
- 本地复现：<在本地复现的步骤>
- 根因：<原因>
- 修复：<具体修改>
- 防再犯：<加什么检查/规则防止同类问题>
```

### Step 5：增强建议（可选）

按需建议，不强行堆配置：
- **依赖审计**：`npm audit` / `pip-audit` / `govulncheck`
- **密钥扫描**：`gitleaks`（GitHub 官方也有 secret scanning，可二选一）
- **覆盖率门槛**：Codecov / 简单的阈值脚本
- **自动格式化检查**：prettier --check / biome ci

## 规则

1. **本地优先**：CI 失败先本地复现，不要在 CI 上盲试。
2. **最小化**：CI 配置保持 5 步以内，每步一个明确职责，别堆 20 个 step。
3. **失败要可读**：日志摘要只保留关键行，不要贴整段原始日志。
4. **防再犯**：每个修复都附带"如何防止同类问题再次出现"。
5. **CI 是门不是墙**：`main` 分支保护用 CI 检查，但别让格式强迫症阻塞交付。

## 触发方式

- 手动：说"配置 CI" / "CI 挂了帮我看看" / `/skill ci-helper`
- 自动：deploy-gate 检查 CI 状态时，失败项引导到这里修复
