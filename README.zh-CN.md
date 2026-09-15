# Interpretable Learning Energy Model

a reusable PyTorch package for fitting and analyzing an interpretable pairwise maximum-entropy energy model。

无需 PISA 数据即可运行完整示例：

```bash
python -m examples.fit_synthetic
```

该示例会生成合成数据，执行 `fit -> analyze -> save`，不会写入任何受限研究数据。

## 项目背景

- 领域：`research Python package for educational and structured-data energy modeling`
- 主要用户：`researchers and machine-learning engineers`
- 当前 MVP 重点：`fit, inspect, and reproduce a binary maximum-entropy learning model`

## 开发流程

本项目采用 PRD 优先、基于小任务的 AI 辅助开发流程。

1. 阅读 `AGENTS.md` 和相关项目规则。
2. 确认 PRD 与任务范围。
3. 一次完成一个小而完整的任务。
4. 运行验证。
5. 审查差异并准备人工交接。

## 验证

```bash
bash scripts/verify.sh --instance
bash scripts/verify.sh --strict-instance
```

就绪检查请参考 `docs/harness/06-strict-readiness.md`。
