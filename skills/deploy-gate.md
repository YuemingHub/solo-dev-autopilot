---
name: deploy-gate
description: >
  部署门禁：自动执行部署前安全检查和 CI 检查，输出部署确认单，并强制人工确认。
  红线：生产部署永远要人工确认，AI 不能自动跳过确认步骤。
  当用户说"能部署了吗" / "部署上线" / "发布到生产" / "deploy" 时触发。
license: MIT
---

# Deploy Gate — 部署门禁（自动检查 + 人工确认红线）

## 目标

在每次部署前执行全面的安全检查，并**强制人工确认**。

> 🚦 **红线（不可绕过）**：生产部署永远要人工确认。AI 可以建议、检查、准备，
> 但"上线"这个动作必须由人按下。这条红线参考 alfred-dev 的质量门原则，
> 也是本项目的 autopilot 边界之一：**开发阶段可自动推进，生产部署永远人工确认。**

## 红线规则

1. 任何生产部署，必须先输出**部署确认单**，等用户明确回复"确认部署"后才能继续
2. 用户说"你看着办""直接部署"**不算确认**——必须复述确认单并让用户逐项确认
3. 确认单中任一 ❌ 默认阻止部署；用户仍要部署时，必须复述已知风险
4. 不允许 AI 以"时间紧""小改动不用查"等理由跳过任何检查项

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

### 🔵 CI 检查（新增）

如果项目配置了 CI（GitHub Actions 等），检查最近一次运行结果：

```bash
# GitHub CLI
gh run list --limit 3
gh run view <run-id> --log-failed
```

- [ ] CI 最近一次运行通过？（lint / test / build / audit / secret scan）
- [ ] 本地检查项与 CI 是否一致？（不一致说明有遗漏）

### 🔵 密钥扫描（新增）

```bash
# 扫描最近改动是否混入密钥
git diff HEAD | grep -iE "(api[_-]?key|secret|password|token)[[:space:]]*[:=][[:space:]]*['\"][A-Za-z0-9]{16,}"
# 或使用专用工具
gitleaks detect 2>/dev/null || trufflehog git --since-commit HEAD~5 2>/dev/null || true
```

- [ ] 无硬编码密钥？
- [ ] 无意外提交的 .env / credentials 文件？

## 输出部署确认单（强制人工确认）

```markdown
## 🚦 部署确认单 — <project> → <environment>

### 检查结果

| 检查项 | 结果 |
|--------|------|
| 环境变量完整性 | ✅ / ❌ |
| 依赖一致性 | ✅ / ❌ |
| 构建成功 | ✅ / ❌ |
| 数据库迁移 | ✅ / ⏭️ |
| 测试通过率 | ✅ / ❌ |
| CI 最近运行 | ✅ / ⏭️ |
| 密钥扫描 | ✅ / ❌ |
| Git 状态清洁 | ✅ / ⚠️ |

### 本次部署内容
- 部署目标：<Vercel / Railway / Supabase / 服务器 IP>
- 涉及变更：<commit 范围 / 功能描述>
- 回滚方案：<见回滚指南>

### 需要你确认
> 我已检查以上所有项目。**请逐项确认后回复"确认部署"。**
> ⚠️ 任何一项为 ❌ 时默认阻止部署；如仍要部署，请说明已知风险。
```

**在用户回复"确认部署"之前，不得执行任何部署命令。确认单无论部署与否都留给用户存档。**

## 回滚指南（部署前必须备好）

| 平台 | 回滚方式 |
|------|---------|
| Vercel | `vercel rollback <deployment-url>` 或 Dashboard → Deployments → Rollback |
| Railway | Dashboard → Deployments → 选择上一个成功版本 → Redeploy |
| Supabase | 迁移前先备份：`pg_dump`；回滚用 `supabase db reset --no-seed`（谨慎） |
| Docker | 保留上一个镜像 tag，`docker compose up -d <旧镜像>` 切回 |
| 通用 | 部署前打 tag：`git tag deploy-<日期>`；回滚 = checkout 旧 tag 重新部署 |

**回滚三原则**：
1. 部署前先确认回滚路径可用（数据库备份、旧镜像存在）
2. 回滚比修复快 → 出问题先回滚，别在生产上 debug
3. 回滚后立即复盘：什么导致的？怎么防止再发生？

## 中国部署场景（国内环境特供）

- [ ] 域名是否完成 ICP 备案？（未备案域名无法绑定国内服务器/CDN）
- [ ] 国内服务器 → 确认镜像源（npm/pnpm 用 npmmirror，Docker 用国内镜像加速）
- [ ] 海外服务（Vercel/Cloudflare）在国内可能不稳定 → 确认是否需要国内替代（阿里云/腾讯云）
- [ ] 微信小程序/公众号 → 需要 HTTPS + 备案域名 + 服务器在国内

## 使用方式

### 手动触发
在对话中说：
- "帮我做一下部署检查"
- "能部署了吗"
- "发布到生产"
- "/skill deploy-gate"

### 自动触发（推荐）
配置在 CI/CD pipeline 的 deploy step 之前：

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    steps:
      - name: Deploy Gate 检查
        run: npx solo-dev-autopilot skill deploy-gate
      - name: 等待人工确认（手动批准）
        uses: trstringer/manual-approval@v1
        with:
          secret: ${{ secrets.GITHUB_TOKEN }}
          approvers: <你的 GitHub 用户名>
      - name: Deploy
        if: success()
        run: ...
```

或作为 git pre-push hook（推送 main 分支时自动触发检查）。

## 注意事项

1. **P0 是硬性门槛**：任何一项 P0 失败都必须阻止部署
2. **给出修复方案而不只是报错**：每条失败都要有具体的修复步骤
3. **考虑环境差异**：本地能跑不代表线上能跑，特别关注环境变量和依赖版本
4. **保留检查日志**：每次部署检查的结果都应该被记录，方便事后排查
5. **渐进式严格**：开发阶段可以放宽 P2，上线前必须全部通过
6. **红线优先于一切**：即使所有检查通过，缺少人工确认也绝不部署
