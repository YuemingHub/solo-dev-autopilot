# 会话衔接与记忆系统设计

> 日期：2026-08-03
> 维度：新手踩坑全景图 - 维度 2（会话衔接与记忆）
> 状态：已批准，实施中

## 问题陈述

新人在使用 AI 编程工具时，最大的隐性成本不是写代码本身，而是：
1. 不知道"上下文"是什么，从不主动给 AI 上下文
2. 以为 AI 记得昨天的对话，关窗口再开就失忆
3. 记忆文件（PROJECT-MEMORY.md）从初始化后从不更新
4. 会话结束直接关窗口，不触发 post-session
5. AI 改了什么新人完全不知道，失控感强
6. 不知道何时该更新记忆

## 设计目标

让新人"不需要理解上下文概念"也能正确使用记忆系统——通过模板文件、AI 主动提醒、自动化脚本的组合，把"维护记忆"从"新人需要记住的事"变成"系统自动做的事"。

## 产出物

### 新增文件

1. `templates/ONBOARDING-template.md` — 新手入口文件
   - 用人话解释 3 个记忆文件是什么、什么时候被读、什么时候要更新
   - 内置"启动咒语"（复制即用的会话开场白）
   - 会话节奏建议（别超过 1-2 小时）
   - "结束会话前"检查清单

2. `templates/SESSION_DRIVER-template.md` — 会话方向盘
   - 本轮目标（1-3 件具体的事）
   - 上次会话回顾（自动填充）
   - 当前进度 checklist
   - 已知阻塞项

### 修改文件

3. `skills/context-map.md` — 加 Step 0 记忆健康检查 + 触发时机清单
4. `scripts/post-session.sh` — 生成"上次会话回顾"区块
5. `skills/commit-helper.md` — body 必须带"影响模块"
6. `scripts/setup.sh` — 生成 ONBOARDING + SESSION_DRIVER 到目标项目

## 坑 → 机制映射

| 坑 | 机制 | 落地 |
|---|---|---|
| #6 不知道有记忆文件 | ONBOARDING 第一屏解释 | ONBOARDING-template.md |
| #7 以为 AI 记得昨天 | 启动咒语模板 | ONBOARDING-template.md |
| #8 不知道上下文有上限 | 会话节奏建议 + SESSION_DRIVER 本轮目标 | 两个模板 |
| #9 记忆从不更新 | context-map Step 0 健康检查，AI 主动问 | context-map.md |
| #10 直接关窗口 | post-session 自动回顾 + ONBOARDING 提醒 | post-session.sh + ONBOARDING |
| #11 不知何时更新 | context-map 触发时机清单 | context-map.md |
| #12 AI 改了啥不知道 | post-session 逐文件回顾 + commit body 带模块 | post-session.sh + commit-helper.md |

## 非目标

- 不做 Git Hooks 硬约束（方案 B，留到后续轮次）
- 不做路线图/进度看板（方案 C，留到 v2）
- 不改现有 skills 的核心逻辑，只加前置步骤