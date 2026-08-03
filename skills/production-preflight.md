---
name: production-preflight
description: >
  生产上线预检：上线前最后一公里检查——测试覆盖率、CI 状态、权限配置、
  可观测性、密钥扫描、备份与回滚。输出上线检查单，与 deploy-gate 衔接。
  当用户说"可以上线了吗" / "上线前检查" / "production preflight" 时触发。
license: MIT
---

# Production Preflight — 生产上线预检

## 目标

在 deploy-gate（部署门禁）之前做**最后一公里**检查：deploy-gate 负责"能不能部署"，
本 Skill 负责"上线后会不会出事"——把覆盖率、CI、可观测性、密钥、回滚这五件事
一次性查清楚，输出一份可存档的上线检查单。

> 与 deploy-gate 的关系：**先跑 production-preflight（上线预检），再跑 deploy-gate（部署门禁）**。
> preflight 查出"上线风险"，deploy-gate 守着"上线动作"。两者都通过 + 人工确认，才允许部署。

## 检查维度（六项）

### 1. 测试覆盖率（P0）

```bash
# 运行测试并输出覆盖率（复用 test-runner 的数据）
pnpm vitest run --coverage   # 或 pytest --cov=.
```

- [ ] 覆盖率 >= 80%（蓝图基线）
- [ ] 核心路径（认证、支付、数据写入）有测试覆盖
- [ ] 最近修复的 bug 有对应回归测试

### 2. CI 状态（P0）

```bash
gh run list --limit 3
```

- [ ] 最近一次 CI 全绿（lint / test / build / audit / secret scan）
- [ ] main 分支受保护（直接 push 被禁止，走 PR）

### 3. 权限与配置（P0）

- [ ] 生产环境变量齐全且非占位符（对照 `.env.example`）
- [ ] 生产模式配置已加载（`configs/modes/production.json` 对应规则）
- [ ] 日志级别不是 debug（生产用 info 起）
- [ ] CORS 只允许真实域名，不是 `*`
- [ ] Rate limiting 已配置（防刷）

### 4. 可观测性（P1）

- [ ] 结构化 JSON 日志已落地（无裸 console.log）
- [ ] Sentry 已接入且 `environment=production`
- [ ] `/healthz` `/readyz` 存在且通过
- [ ] 至少一种告警通道已配置（Sentry 邮件 / UptimeRobot）

### 5. 密钥与敏感数据（P0）

```bash
git log --all --oneline | head -20   # 检查历史
gitleaks detect 2>/dev/null || git diff HEAD | grep -iE "(api[_-]?key|secret|password|token)[[:space:]]*[:=][[:space:]]*['\"][A-Za-z0-9]{16,}"
```

- [ ] 无硬编码密钥（含 git 历史！历史泄露和当前泄露一样危险）
- [ ] `.env` / `credentials` 未被跟踪
- [ ] 数据库密码强度足够且不在代码中

### 6. 备份与回滚（P0）

- [ ] 数据库有自动备份（Supabase/Railway 自带或定时 pg_dump）
- [ ] 回滚路径明确：上一个可用镜像 tag / 部署 tag 存在
- [ ] 迁移脚本可回滚（down 迁移已写）

## 输出上线检查单

```markdown
## 📋 上线检查单 — <项目> → production

| # | 检查项 | 结果 | 备注 |
|---|--------|------|------|
| 1 | 测试覆盖率 >= 80% | ✅ 86.4% | |
| 2 | CI 最近全绿 | ✅ | main 受保护 |
| 3 | 权限与配置 | ⚠️ | CORS 待收紧 |
| 4 | 可观测性 | ✅ | Sentry + healthz |
| 5 | 密钥扫描 | ✅ | 历史干净 |
| 6 | 备份与回滚 | ✅ | 每日备份 + tag |

### 结论
- ✅ 可以进入 deploy-gate（部署门禁）
- ⚠️ 有风险项（见备注），建议先处理：<具体项>
- ❌ 有 P0 未过，禁止部署：<具体项>

### 修复建议
- <每项失败给出具体改法，不只报问题>
```

## 规则

1. **P0 不过 = 禁止部署**：任何 P0 项 ❌，直接阻止，不进入 deploy-gate。
2. **实测数据**：覆盖率/CI 状态必须来自实际运行，禁止猜测。
3. **检查单必须存档**：无论是否上线，检查单写入 `.solo-dev-autopilot/preflight-<日期>.md`。
4. **与 deploy-gate 无缝衔接**：本 Skill 检查完输出结论，deploy-gate 接手做部署确认。
5. **渐进严格**：P2 项（性能基线等）可以标 ⏭️，但 P0/P1 不打折。

## 触发方式

- 手动：说"可以上线了吗" / "上线前检查" / "/skill production-preflight"
- 自动：deploy-gate 的"配置检查"步骤之前推荐先跑本 Skill
