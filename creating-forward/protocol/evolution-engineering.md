# Evolution Engineering

Evolution Engineering 负责让协议从真实运行中学习，但不允许运行实例直接改写正式协议。

## 输入

- 运行复盘。
- 失败和阻塞。
- 用户不必要干预。
- 验证漏检。
- 权限误判。
- 上下文错误。
- 任务图返工。
- 跨 Agent 恢复偏差。

## 输出

- observation record。
- attribution。
- protocol candidate。
- regression scenario。
- impact analysis。
- migration note。
- Draft change。

## 决策

候选状态：
- observed
- reproduced
- diagnosed
- proposed
- tested
- independently_reviewed
- human_approved
- released
- rejected

不得从 `observed` 直接进入 `released`。
