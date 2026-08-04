# Evidence Engineering

## 证据记录最小字段

- evidenceId
- taskId
- type
- commandOrMethod
- observedResult
- exitCode
- artifactPaths
- timestamp
- verifier
- limitations

## 强证据顺序

1. 机器可重复验证。
2. 独立 Agent 检查。
3. 外部服务明确确认。
4. 人类主观验收。

不同类型成果使用不同证据：
- 代码：测试、构建、静态检查、运行。
- 页面：真实构建、浏览器检查、控制台与关键状态。
- 文档：存在性、结构、引用、事实核查。
- 研究：来源、引用映射和交叉核验。
- 专业回复：安全门、契约测试、真实样本与专业人员验收。
