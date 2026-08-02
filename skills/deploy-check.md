---
name: deploy-check
description: >
  部署前的安全检查清单。新手最容易在部署时踩坑——环境变量缺失、依赖不一致、构建失败。
  这个 Skill 在部署前自动检查所有关键项，防止低级错误带到线上。
runAs: subagent
tools: [read_file, run_command, list_directory, glob]
tags: [deploy, safety-check, pre-deploy, ci-cd]
priority: high
---

# Deploy Check — 部署前安全检查器

## 目标

在每次部署前执行全面的安全检查，确保不会因为低级错误导致线上故障。

## 检查项目（按优先级排序）

### 🔴 P0 — 必须通过（任一失败则阻止部署）

#### 1. 环境变量完整性
```bash
# 读取 .env.example 获取所有必需变量
# 对比当前 .env 或部署环境的实际值
```

检查项：
- [ ] `.env.example` 中列出的所有变量是否都有值？
- [ ] 敏感变量（API_KEY, SECRET, PASSWORD, TOKEN）是否有值且不是占位符？
- [ ] URL 类变量格式是否正确？（http:// 或 https:// 开头）
- [ ] 端口号是否正确？
- [ ] 数据库连接字符串是否完整？

**如果缺失**：列出所有缺失的变量，给出示例值格式。

#### 2. 依赖一致性
```bash
# 检查 lock 文件是否存在且与 package.json 一致
pnpm install --frozen-lockfile  # 或对应工具的等价命令
# 或者
npm ci
```

检查项：
- [ ] `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` 是否存在？
- [ ] lock 文件与 `package.json` 是否一致？
- [ ] 所有依赖能否正常安装？
- [ ] 是否有 `npm audit` 报告的高危漏洞？（可选阻止）

#### 3. 构建成功
```bash
# 执行构建命令
pnpm build
# 或
npm run build
```

检查项：
- [ ] 构建命令是否能成功完成？
- [ ] 构建产物是否生成到预期目录？
- [ ] 构建是否有 warning？（不阻止但需提醒）

### 🟠 P1 — 强烈建议通过

#### 4. 数据库迁移状态
```bash
# 检查待执行的迁移
pnpm db:push --dry-run
# 或
npx prisma migrate status
# 或
npx drizzle-kit push --dry
```

检查项：
- [ ] 是否有未执行的数据库迁移？
- [ ] 迁移是否可能破坏现有数据？
- [ ] 是否有需要备份的数据？

#### 5. 测试通过率
```bash
# 运行测试套件
pnpm test
# 或
pnpm test:e2e
```

检查项：
- [ ] 单元测试通过率 >= 80%？
- [ ] 关键路径的 E2E 测试是否通过？
- [ ] 是否有跳过的测试（skip）？

#### 6. Git 状态清洁
```bash
git status
git log --oneline -5
```

检查项：
- [ ] 所有改动是否已 commit？
- [ ] 当前分支是否正确？（main / develop / feature 分支）
- [ ] 最近一次 commit message 是否规范？
- [ ] 是否有敏感文件被意外提交？（.env, credentials 等）

### 🟡 P2 — 建议检查

#### 7. 性能基线
- [ ] 构建产物大小是否合理？（前端 bundle < 500KB gzipped）
- [ ] Lighthouse 分数是否可接受？（Performance > 80）
- [ ] 是否有明显的性能回归？

#### 8. 安全扫描
```bash
npm audit
# 或
snyk test
# 或
pip check
```
- [ ] 无已知的高危 CVE？
- [ ] 依赖是否来自可信源？

#### 9. 配置检查
- [ ] 生产环境的 CORS 设置是否正确？
- [ ] Rate limiting 是否配置？
- [ ] 日志级别是否适合生产？（不要 debug 级别）
- [ ] 错误信息是否会泄露堆栈信息给用户？

## 输出报告格式

```markdown
# ✈️ Deploy Check Report

> 项目：<project-name>
> 目标环境：<production | staging | development>
> 检查时间：<timestamp>

## 结果总览

| 级别 | 通过 | 失败 | 跳过 |
|------|------|------|------|
| P0 🔴 | N/N | N | N |
| P1 🟠 | N/N | N | N |
| P2 🟡 | N/N | N | N |

**结论：** ✅ **可以部署** / ⚠️ **建议修复后部署** / ❌ **不能部署**

## 详细结果

### P0 — 必须通过

| # | 检查项 | 状态 | 详情 |
|---|--------|------|------|
| 1 | 环境变量完整性 | ✅/❌ | ... |
| 2 | 依赖一致性 | ✅/❌ | ... |
| 3 | 构建成功 | ✅/⚠️/❌ | ... |

### P1 — 强烈建议

| # | 检查项 | 状态 | 详情 |
|---|--------|------|------|
| 4 | 数据库迁移 | ✅/❌/⏭️ | ... |
| 5 | 测试通过率 | ✅/❌/⏭️ | ... |
| 6 | Git 状态 | ✅/⚠️ | ... |

## ⚠️ 问题列表（如有）

### <问题标题>
- **严重度**：P0/P1/P2
- **影响**：<如果不修会怎样>
- **修复建议**：<具体步骤>

## 📋 部署前确认清单

- [ ] 已阅读上述所有检查结果
- [ ] P0 问题已全部修复
- [ ] 已通知团队成员（如适用）
- [ ] 回滚方案已准备就绪
- [ ] 部署窗口已确认（如适用）
```

## 使用方式

### 手动触发
在对话中说：
- "帮我做一下部署检查"
- "能部署了吗"
- "deploy check"
- "/skill deploy-check"

### 自动触发（推荐）
配置在 CI/CD pipeline 的 deploy step 之前：
```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    steps:
      - name: Deploy Check
        run: npx solo-dev-autopilot skill deploy-check
      - name: Deploy
        if: success()
        run: ...
```

或作为 git pre-push hook：
```bash
# 当尝试 push 到 main 分支时自动触发
```

## 注意事项

1. **P0 是硬性门槛**：任何一项 P0 失败都必须阻止部署
2. **给出修复方案而不只是报错**：每条失败都要有具体的修复步骤
3. **考虑环境差异**：本地能跑不代表线上能跑，特别关注环境变量和依赖版本
4. **保留检查日志**：每次部署检查的结果都应该被记录，方便事后排查
5. **渐进式严格**：开发阶段可以放宽 P2，上线前必须全部通过
