---
name: harness-guard
description: >
  安全护栏。执行 shell 命令前、写文件/删除/覆盖前自动做安全检查:识别破坏性命令、禁止硬编码密钥、防止覆盖未读文件,
  高风险动作先询问用户。任何涉及 rm -rf/删除/drop/force push/全局安装/写敏感信息的操作前使用。
  不适合普通代码编辑(用 dev-loop)。
license: MIT
---

# 安全护栏(harness-guard)

> 原则出处:《深入理解 AI Agent》(中文解析见 `references/book/`)第 1 章 1.2.6「护栏」(输入侧护栏、执行侧护栏、输出侧护栏;人工干预:失败阈值与高风险操作升级)、5.1.6「故障恢复」(降级与人工升级)。目标:自动驾驶可以快,但不能翻车。

## 核心规则

1. **低风险操作全自动;高风险操作先说明影响再询问**
2. **密钥不进代码、不进日志、不进记忆**——只进 .env(且 .env 不入库)
3. **破坏性动作要可逆**:先备份/先确认,再执行

## 执行流程(在危险动作前调用)

### 1. 命令风险分级

| 等级 | 例子 | 处理 |
| --- | --- | --- |
| 安全 | 读文件、查询版本、git status/diff、项目内安装依赖 | 直接执行 |
| 需确认 | `rm -rf`/`del /s`、`git reset --hard`/`push --force`、删文件、覆盖未读文件、全局装包、`pip uninstall`、`DROP TABLE`、改 PATH/系统配置、`taskkill /f`、`aws configure` 等凭据操作 | 向用户说明**影响范围+可逆性+是否有备份**,确认再执行 |
| 禁止(除非用户明确要求) | 清空磁盘、删除 .git、提交/暴露密钥、向远程仓库推密钥 | 拒绝并说明 |

关键词表(大小写不敏感,执行前把命令拆 token 扫描):`rm -rf`、`del /s`、`rmdir /s`、`Remove-Item -Recurse -Force`、`shutil.rmtree`、`DROP DATABASE`、`DROP TABLE`、`TRUNCATE`、`git reset --hard`、`git push --force`/`-f`、`git clean -f`、`git filter-branch`、`pip install -g`、`npm install -g`、`yarn global add`、`winget install`、`choco install`、`pip uninstall`、`npm uninstall`、删锁文件(lockfile)、删 `.git`、`setx`、注册表、防火墙、`taskkill /f`、`Stop-Process -Force`、`kill -9`。

### 2. 写文件敏感信息检查

写入/修改任何代码文件前,检查内容是否含:

- 常见密钥格式:`sk-[A-Za-z0-9]{16,}`、`AKIA[0-9A-Z]{16}`(AWS)、`AIza[0-9A-Za-z_-]{30,}`(Google)、`ghp_[0-9A-Za-z]{30,}`(GitHub PAT)、`-----BEGIN [A-Z ]*PRIVATE KEY-----`(私钥)、`postgres://user:pass@` / `mongodb://user:pass@`(明文密码 URL)
- 发现 → 改为引用环境变量(如 `os.environ["API_KEY"]`),值写入 `.env`,并确认 `.env` 在 .gitignore 中
- 检查已有仓库历史:不小心提交过密钥时,提示用户用 `git filter-repo`/BFG 清理(询问后执行,不建议新手直接操作历史)

### 3. 覆盖与删除保护

- 覆盖已存在文件前,先 Read 该文件(未读不算数);用户项目里的文件修改前先备份到 `.agent-memory/backups/` 或用 git
- 删除文件前先 `git ls-files` 确认是否被跟踪;被跟踪且未提交 → 视为需确认操作

### 4. 超时与卡死检测

所有长命令设置超时(安装/下载 600s、构建/测试 300s、普通 120s、网络探测 30s);命令疑似卡死(长时间无输出)或等待交互输入时,终止并报告,不要无限等。

### 5. 失败升级路径(Harness)

危险动作失败 → 不自动换更暴力方案(比如 rm -rf 失败不要换管理员删除),停下来报告:失败原因、已尝试、建议的人工步骤。

## 需确认场景的提问模板

向用户说明三件事,缺一不可:
1. **要做什么**(一句话 + 命令)
2. **影响范围**(哪些文件/数据/系统)
3. **可逆性**(有备份?git 可恢复?删了能否重建)

```
⚠️ 需要确认:我将执行 <命令>,它会 <影响>。
- 影响范围:<...>
- 可逆性:<已 git 提交可回滚 / 我会先备份到 .agent-memory/backups / 不可逆>
是否继续?(y=执行 / n=跳过 / 有修改意见请直接说)
```

## 与三级权限模型的关系

- 本 skill 的命令分级与 `configs/permissions.json`(safe/ask/danger)语义一致:safe=直接执行、ask/danger=先确认
- production 档位下,发布类操作(合并 production、部署、改真实数据)一律先问用户(见 docs/autopilot-boundaries.md)

## 汇报格式

发现的风险、你做了什么防护、需要用户确认的点(一条条列清楚)。面向新手,说明「为什么要确认」而不是只抛命令。
