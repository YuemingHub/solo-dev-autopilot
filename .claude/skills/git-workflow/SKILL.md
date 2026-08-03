---
name: git-workflow
description: 新手不知道什么时候该开分支、怎么命名、怎么合并——这个 Skill 帮你管理 Git 工作流。 分支命名规范、提交频率建议、合并冲突处理、PR 流程引导。
license: MIT
---

# Git Workflow — 分支管理与 PR 流程引导器

## 目标

让新手不用理解 Git 的复杂概念，也能正确地：
1. 开分支 → 2. 提交代码 → 3. 合并回主干 → 4. 处理冲突

## 分支策略

### 简化版 Git Flow（新手专用）

```
main          ← 稳定代码，随时可部署
  └── feat/xxx   ← 功能分支，开发完合并回 main
  └── fix/xxx    ← 修复分支，修完合并回 main
```

> 新手不需要 develop 分支、release 分支、hotfix 分支。
> 只用 main + 功能分支就够了。

### 分支命名规范

| 类型 | 格式 | 例子 |
|------|------|------|
| 新功能 | `feat/<简短描述>` | `feat/user-auth` |
| 修复 bug | `fix/<简短描述>` | `fix/login-redirect` |
| 改样式 | `style/<简短描述>` | `style/dark-mode` |
| 重构 | `refactor/<简短描述>` | `refactor/api-client` |
| 文档 | `docs/<简短描述>` | `docs/api-readme` |

> 命名用英文小写 + 连字符，不要用中文或下划线。

## 执行流程

### 场景 1：开始做新功能

当用户说"我要开始做 xxx 功能"时：

1. 确认当前在 main 分支且工作区干净
2. 拉取最新代码：`git pull origin main`
3. 创建功能分支：`git checkout -b feat/<描述>`
4. 告诉用户："已创建分支 `feat/xxx`，现在可以开始写代码了"

### 场景 2：提交代码

当用户说"帮我提交"或"提交代码"时：

1. 检查改动：`git status` + `git diff`
2. 调用 commit-helper skill 生成 commit message
3. 暂存相关文件（不要 `git add -A`，只加相关的）
4. 提交：`git commit -m "<message>"`
5. 告诉用户："已提交！commit: `<hash>`"

**提交频率建议**：
- 每完成一个小功能就提交一次
- 不要攒一天的工作量再提交
- 每次提交应该是"可独立运行"的状态

### 场景 3：合并回 main

当用户说"做完了，合并"或"合并到 main"时：

1. 确保当前分支的所有改动已提交
2. 切回 main：`git checkout main`
3. 拉取最新：`git pull origin main`
4. 合并功能分支：`git merge feat/xxx`
5. 如果有冲突 → 进入冲突处理流程
6. 推送：`git push origin main`
7. 删除功能分支（可选）：`git branch -d feat/xxx`
8. 告诉用户："已合并到 main 并推送！"

### 场景 4：处理合并冲突

当合并出现冲突时：

1. 列出所有冲突文件
2. 对每个冲突文件：
   - 读取冲突内容
   - 分析两边的改动
   - 给出合并建议（展示冲突区域 + 建议的合并结果）
   - 等用户确认后修改
3. 标记已解决：`git add <file>`
4. 继续合并：`git commit`（或 `git merge --continue`）

**冲突处理原则**：
- 不要自动选择一边，要给用户看两边的差异
- 如果是同一逻辑的不同写法，问用户要哪个
- 如果是不冲突的不同部分，两边都保留

### 场景 5：撤销操作

当用户说"我搞砸了"或"回退"时：

| 场景 | 命令 | 说明 |
|------|------|------|
| 撤销未暂存的改动 | `git checkout -- <file>` | 文件回到上次提交的状态 |
| 撤销已暂存的改动 | `git reset HEAD <file>` | 取消暂存，改动还在 |
| 撤销最近一次提交（保留改动） | `git reset --soft HEAD~1` | 提交撤销，代码改动保留 |
| 撤销最近一次提交（丢弃改动） | `git reset --hard HEAD~1` | ⚠️ 危险！改动会丢失 |

> ⚠️ 永远不要在没有确认的情况下执行 `git reset --hard`。

## 常见错误处理

### 错误：提交到了错误的分支

```
你在 feat/xxx 分支开发，但忘了切分支，代码提交到了 main
```

**修复**：
```bash
git checkout feat/xxx          # 切到正确的分支
git merge main                  # 把误提交的代码带过来
git checkout main               # 切回 main
git reset --hard HEAD~1         # 撤销 main 上的误提交
git checkout feat/xxx           # 切回功能分支继续
```

### 错误：推送被拒绝（non-fast-forward）

```
! [rejected] main -> main (non-fast-forward)
```

**原因**：远程有别人推送的新提交，你本地没有

**修复**：
```bash
git pull --rebase origin main   # 先拉取并 rebase
git push origin main             # 再推送
```

### 错误：不小心 git add -A 把不该加的文件加进去了

**修复**：
```bash
git reset HEAD <文件名>          # 取消暂存该文件
```

## 使用方式

在对话中说：
- "我要开始做 xxx 功能" → 自动创建分支
- "帮我提交" → 调用 commit-helper 提交
- "合并到 main" → 合并流程
- "有冲突，帮我解决" → 冲突处理
- "我搞砸了，帮我回退" → 撤销操作
- "/skill git-workflow" → 手动触发

## 注意事项

1. **main 分支要随时可部署**：不要在 main 上直接开发，永远开分支
2. **提交粒度要小**：一个小功能一次提交，不要攒一堆
3. **合并前先拉取**：`git pull origin main` 避免大冲突
4. **不要 force push 到 main**：除非是个人项目且只有你一个人
5. **冲突不可怕**：AI 会帮你分析两边的改动，给出合并建议
