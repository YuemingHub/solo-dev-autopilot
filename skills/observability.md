---
name: observability
description: >
  可观测性：结构化 JSON 日志规范、Sentry 错误监控集成、健康检查端点、基础告警。
  让上线后的应用"出了问题能看见、能定位、能告警"。当用户说"加日志"
  / "接入 Sentry" / "健康检查" / "监控告警" / "线上报错了怎么查" 时触发。
license: MIT
---

# Observability — 可观测性（日志 + Sentry + 健康检查 + 告警）

## 目标

新手项目最大的隐患不是功能 bug，而是**上线后瞎了**——出问题不知道、
知道了不知道在哪、找到了不知道原因。本 Skill 建立最薄但够用的可观测性层。

## 一、结构化 JSON 日志规范

### 为什么 JSON

- 机器可解析：可被日志平台/`jq` 直接查询
- 字段统一：跨服务排查时字段名一致
- 未来可迁移：换日志平台零成本

### 最小字段集（每个应用日志必须包含）

```json
{
  "ts": "2026-08-03T13:52:00.000Z",
  "level": "info",
  "msg": "user logged in",
  "service": "api",
  "request_id": "req_9f3a2b",
  "user_id": "u_123"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `ts` | ✅ | ISO 8601 UTC 时间 |
| `level` | ✅ | debug / info / warn / error |
| `msg` | ✅ | 人类可读的一句话 |
| `service` | ✅ | 服务名（如 api / worker） |
| `request_id` | ✅ | 一次请求的追踪 ID（透传） |
| 业务字段 | 按需 | user_id / order_id 等，便于检索 |

### 日志级别规范

| 级别 | 用途 | 生产环境 |
|------|------|---------|
| debug | 开发细节 | ❌ 关闭（性能 + 噪音） |
| info | 正常业务事件（登录、下单） | ✅ |
| warn | 可恢复的异常（重试、限流） | ✅ |
| error | 请求失败、异常 | ✅（必须带堆栈/上下文） |

### 代码模板

```ts
// Node/TS 最小示例（无第三方库，JSON.stringify 即可）
function log(level: 'debug'|'info'|'warn'|'error', msg: string, fields: Record<string, unknown> = {}) {
  if (level === 'debug' && process.env.NODE_ENV === 'production') return;
  console.log(JSON.stringify({ ts: new Date().toISOString(), level, msg, service: 'api', ...fields }));
}
```

```python
# Python 最小示例
import json, logging, time

def log(level, msg, **fields):
    record = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "level": level, "msg": msg, "service": "api", **fields}
    print(json.dumps(record, ensure_ascii=False))
```

**红线**：禁止 `console.log("用户登录了")` 这类裸文本日志——没有时间戳、
没有级别、无法检索，等于没记。

## 二、Sentry 错误监控集成

### 什么时候需要

- 应用有后端 API（Node/Python/Go）
- 有前端页面（JS/TS）
- 想要"线上报错主动通知我"

### 集成步骤

```bash
# Node 后端
pnpm add @sentry/node
# 或前端
pnpm add @sentry/browser
# Python
pip install sentry-sdk
```

```ts
// Node 初始化（入口文件最顶部）
import * as Sentry from '@sentry/node';
Sentry.init({
  dsn: process.env.SENTRY_DSN,        // 从环境变量读，绝不硬编码
  environment: process.env.NODE_ENV,  // production / staging
  tracesSampleRate: 0.1,              // 性能采样 10%，省钱够用
});
```

```python
import sentry_sdk
sentry_sdk.init(dsn=os.environ["SENTRY_DSN"], environment=os.environ.get("NODE_ENV", "dev"))
```

### 配置检查清单

- [ ] DSN 从环境变量读取，`.env.example` 里有 `SENTRY_DSN=` 占位
- [ ] `environment` 正确标注（区分 production/staging 才好过滤）
- [ ] 明确哪些错误**不**上报（如 4xx 业务错误可降噪，只上报 5xx/未捕获异常）

## 三、健康检查端点

给部署平台（Render/Railway/Docker healthcheck）用的标准端点：

| 端点 | 用途 | 返回 |
|------|------|------|
| `/healthz` | 存活检查（进程活着） | `200 {"status":"ok"}` |
| `/readyz` | 就绪检查（依赖可用） | `200` 或 `503`（含各依赖状态） |

```ts
// Node 最小实现（Express/Fastify 等价写法）
app.get('/healthz', (_req, res) => res.json({ status: 'ok' }));
app.get('/readyz', async (_req, res) => {
  try {
    await db.$queryRaw`SELECT 1`;   // 检查数据库
    res.json({ status: 'ready', deps: { db: 'ok' } });
  } catch (e) {
    res.status(503).json({ status: 'not-ready', deps: { db: 'down' } });
  }
});
```

**红线**：健康检查端点不得打印敏感信息（数据库连接串、内部 IP）。

## 四、基础告警

Solo 开发者不需要完整监控平台，先做这三件事：

1. **Sentry 错误告警**：Sentry 项目设置里配邮箱/Webhook，error 级别即通知
2. **部署失败告警**：CI（GitHub Actions）失败时发邮件——Actions 自带通知
3. **可用性探测**：UptimeRobot（免费 50 个监控）每 5 分钟探测 `/healthz`，挂了发邮件

## 五、事故排查流程（线上报错了怎么查）

```
1. 看 Sentry 最近 error → 拿到 request_id / 堆栈
2. 查日志：grep request_id → 看该请求完整链路
3. 定位：哪一步抛错 → 环境变量？依赖？数据？
4. 修复 → 补一条回归测试 → 部署
5. 复盘：为什么没被测试拦住？加什么检查？
```

## 触发方式

- 手动：说"加日志" / "接入 Sentry" / "健康检查" / "监控告警" / `/skill observability`
- 自动：production-preflight 检查可观测性项时调用
