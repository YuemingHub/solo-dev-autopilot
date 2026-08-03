# 生产上线检查清单（Production Checklist）

> 定位：上线前的**人工兜底清单**。AI 的 production-preflight skill 负责自动检查，
> 这份清单是给你（人类）在按下部署按钮前逐项过一遍的纸面清单。
> 配套 Skill：`/skill production-preflight`（自动版）、`/skill deploy-gate`（部署门禁）。

---

## 一、代码与测试

- [ ] 测试覆盖率 ≥ 80%（核心路径：认证/支付/数据写入必须有测试）
- [ ] 最近修复的 bug 都有回归测试
- [ ] CI 最近一次全绿（lint / test / build / audit / secret scan）
- [ ] main 分支受保护，直接 push 被禁止
- [ ] 无 `console.log` 裸日志残留（应使用结构化 JSON 日志）

## 二、配置与环境

- [ ] `.env.example` 完整（每个变量都有注释说明用途）
- [ ] 生产环境变量齐全且**不是占位符**
- [ ] 已切换生产模式配置（`configs/modes/production.json`）
- [ ] 日志级别为 info 起（不是 debug）
- [ ] CORS 只允许真实域名
- [ ] Rate limiting 已配置
- [ ] 时区/地区设置正确（国内部署注意备案与镜像源）

## 三、安全

- [ ] git 历史无硬编码密钥（历史和当前一样危险）
- [ ] `.env`、credentials 未被 git 跟踪
- [ ] 数据库密码强度足够
- [ ] 依赖审计无高危漏洞（`npm audit --audit-level=high`）
- [ ] 错误响应不泄露堆栈/内部路径

## 四、可观测性

- [ ] 结构化 JSON 日志已落地
- [ ] Sentry 已接入且 `environment=production`
- [ ] `/healthz`（存活）与 `/readyz`（就绪）存在并通过
- [ ] 至少一种告警通道（Sentry 邮件 / UptimeRobot）
- [ ] 已用真实流量测试过日志/报错能收到

## 五、备份与回滚

- [ ] 数据库有自动备份（平台自带或定时 pg_dump）
- [ ] 回滚路径明确：旧镜像 tag / 部署 tag 存在
- [ ] 迁移脚本可回滚（有 down 迁移）
- [ ] 回滚演练过至少一次（知道按钮在哪）

## 六、部署动作

- [ ] 部署目标确认（Vercel / Railway / 服务器 IP / 容器平台）
- [ ] 域名/SSL 证书就绪（国内需 ICP 备案）
- [ ] 部署后健康检查端点能访问
- [ ] 部署后立即查看日志确认无 error 潮

---

## 出问题时的顺序（先回滚，别在线上 debug）

1. **回滚**到上一个可用版本（比修复快）
2. 用 Sentry + 日志定位根因
3. 修 + 补回归测试
4. 重新部署
5. 复盘：为什么测试没拦住？加什么检查？

## 相关文件

- `docs/autopilot-boundaries.md` — AI 能做什么、不能做什么的边界
- `.claude/skills/production-preflight/SKILL.md` — 自动预检
- `.claude/skills/deploy-gate/SKILL.md` — 部署门禁（人工确认红线）
- `.claude/skills/observability/SKILL.md` — 可观测性接入
