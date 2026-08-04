---
name: book-experiments
description: >
  运行《深入理解 AI Agent》(李博杰,github.com/bojieli/ai-agent-book)的配套实验。当用户想跑书中实验、克隆 ai-agent-book、
  安装某章依赖(uv sync --extra chN)、复现实验、或问这本书怎么用/学习路径时使用。
  自动克隆仓库、按章安装依赖、跑通实验并汇报。不适合普通业务开发(用 env-setup/dev-loop)。
license: MIT
---

# 书的配套实验运行(book-experiments)

> 仓库:github.com/bojieli/ai-agent-book(Apache-2.0)。全书主线:**Agent = 模型(大脑) + 上下文(眼睛) + 工具(手脚)**,竞争力在模型之外的 Harness 工程。本 skill 把「读这本书 + 跑它的实验」变成自动流程。
> 本书中文解析 Markdown 已随仓库保存在 `references/book/`(book_part1.md / book_part2.md),只读正文不必克隆仓库。

## 全书速览(章节地图)

| 章节 | 主题 | 与本 skill 合集的关系 |
| --- | --- | --- |
| 第 1 章 | Agent 基础与 Harness 工程 | dev-loop/harness-guard 取材 |
| 第 2 章 | 上下文工程(系统提示、KV Cache、Agent Skills、状态栏) | env-setup 生成 AGENTS.md;dev-loop 状态栏 |
| 第 3 章 | 用户记忆与知识库(记忆格式、RAG、隐私) | task-memory 取材 |
| 第 4 章 | 工具与 MCP(感知/执行/协作三类工具) | 脚手架「命令即工具」思想 |
| 第 5 章 | 生产级 Coding Agent(文档化、测试驱动、故障恢复) | env-detect/env-setup/dev-loop 取材 |
| 第 6 章 | 评估体系(SWE-bench 等基准、LLM-as-a-Judge) | dev-loop 验证序列的进阶版 |
| 第 7 章 | 模型后训练(SFT vs RL) | 新手一般不需要 |
| 第 8 章 | Agent 自我进化(经验学习) | task-memory 踩坑=轻量经验沉淀 |
| 第 9 章 | 多模态与实时交互(语音、GUI、机器人) | 需 Playwright/浏览器 |
| 第 10 章 | 多 Agent 协作 | 进阶 |

仓库结构:`book/chapter1.md ~ chapter10.md`(正文 Markdown)、`chapter1/ ~ chapter10/`(实验代码)、`docs/zh-CN/LEARNING.md`(官方学习路径)、`agentbook/`(本书自研 Agent 辅助包)。

## 流程

### 1. 克隆仓库(一次性)

```
git clone https://github.com/bojieli/ai-agent-book.git
cd ai-agent-book
```

> 先跑 env-detect 确认本机有 Python 3.10+、uv、git;缺失按 env-setup 配方安装(仓库统一要求 Python 3.10+)。

### 2. 按章安装依赖(锁文件优先,可复现)

仓库根目录执行,`ch1` 换成 `ch2`~`ch10` 即可:

```
uv sync --locked --extra ch1          # 推荐:使用仓库 uv.lock,可复现
# 未装 uv 时:
python -m pip install -e ".[ch1]"     # pip 解析,不用锁文件
```

注意:
- 多个 extra 合并到同一条命令:`uv sync --locked --extra ch2 --extra vllm`
- `all` 是不含本地训练栈的 CPU 友好组合,不代表每个实验
- 需要 API Key 的实验:复制根目录 `.env.example` 为 `.env` 填至少一个提供商 Key(Kimi/智谱/Siliconflow/DeepSeek/OpenRouter 任选);有些实验要自己在实验目录放 `.env` 或导出环境变量
- 只有实验 README/CLI 明确列出 `ollama` 时才用本地 Ollama

### 3. 运行实验

从仓库根目录运行(示例):

```
uv run python chapter1/context/main.py
# pip 安装时:python chapter1/context/main.py
```

- 每个实验看自身 README 了解预期输出;验证以「能跑通、输出符合 README 描述」为准,不要自创结论
- 第 6/7/9/10 章共 22 个外部仓库(评测基准/训练框架)不在仓库内,README「附录 · 外部仓库获取」有一键克隆脚本(固定 SHA 的 detached checkout,带 `rev-parse HEAD` 校验)

### 4. 汇报

- 克隆/安装/运行结果(命令 + 输出摘要)
- 环境依赖(哪些章需要 GPU/浏览器/外部仓库/实机硬件)
- 建议的下一步实验;把跑通/踩坑记入 `.agent-memory/troubleshooting.md`(见 task-memory)

## 已知坑(2026-07)

- 第 7 章训练类实验需要 GPU 与显存,CPU 机器不要硬跑,README 有明确硬件要求
- 第 9 章 GUI 实验需要 Playwright 浏览器(`npx playwright install chromium`)与 FFmpeg(`winget install --id Gyan.FFmpeg -e`)
- 部分实验要求 Python 3.11+(浏览器/记忆)、3.12+(第 8 章部分组件)

## 边界

- 只读正文不需要克隆完整仓库:直接读本仓库 `references/book/` 的解析 Markdown,或 GitHub 网页 `book/chapterN.md` 的 raw 链接
- 克隆 + 装全部 10 章依赖体积很大;按用户当前学习章节按需安装,别一次装完
