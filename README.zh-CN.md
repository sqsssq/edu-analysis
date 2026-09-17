# Interpretable Learning Energy Model

一个可复用的 PyTorch package，用于拟合和分析可解释的二元成对最大熵能量模型。

## 安装

在项目目录中安装开发版本：

```bash
python -m pip install -e ".[dev]"
```

如果要读取本地 PISA 的 SAS、SPSS 或压缩文件，额外安装：

```bash
python -m pip install -e ".[pisa]"
```

如果需要严格复现项目开发环境，可以安装 [uv](https://docs.astral.sh/uv/)
并运行：

```bash
uv sync --locked --extra dev
```

这会使用仓库中的 `uv.lock`，而不是重新解析依赖版本。

## 用自己的数据训练

模型接受 `X`（行是样本、列是特征）和 `y`（每行一个目标值）。特征会按配置转换为二元节点；`h` 和对称的 `J` 参数可以直接检查和解释。

```python
from learnenergy import DataConfig, LearningModel

config = DataConfig(
    feature_names=("家庭资源", "教师支持"),
    target_name="学习结果",
    missing_strategy="median",
)
model = LearningModel(config, calculation="auto", seed=7)
fit = model.fit(X, y)
prediction = model.predict(X_new)
analysis = model.analyze()

model.save("learning-model.pt")
reloaded = LearningModel.load("learning-model.pt")
```

如果使用字典或 pandas DataFrame，可以让包按列名完成质量检查、列选择和训练：

```python
model = LearningModel(DataConfig(target_name="学习结果"))
fit = model.fit_table(
    table,
    feature_names=("家庭资源", "教师支持"),
    weight_name="样本权重",  # 可选；当前解释为普通行权重
)
print(model.last_quality_report.to_dict())
```

`calculation="auto"` 会在小模型上使用精确状态枚举，在较大模型上切换到多链 Gibbs 采样；也可以显式指定 `"exact"` 或 `"monte_carlo"`。采样结果应检查 R-hat、ESS、MCSE 和质量阈值。

## 论文复现协议

`examples/pisa_paper_reproduction.py` 固定了论文复现所需的实验口径：

- 每个经济体/学科组合无放回抽取 1,200 条，重复 16 次；
- 使用 `paper_std`，即严格按照 `f > population standard deviation` 二值化；
- 每个 1,200 条 repeat 独立计算标准差，范围记录为 `per_sample_repeat`；
- 19 节点使用 exact enumeration 和显式 KL-gradient，不使用 Adam；
- effective interaction 强制使用 Monte Carlo，并记录 chains、draws、R-hat、ESS、MCSE；
- critical-state 使用 exact covariance 导数。

从已经完成的聚合报告导出论文风格的 Figures 4–12（包括你提供的附录
Figure A.12）可以运行：

```bash
python examples/pisa_paper_figures_4_12.py \
  --report data/prepared/pisa2018-paper-reproduction-report.json \
  --output-dir data/prepared/pisa2018-paper-figures-4-12
```

脚本生成 9 张 PNG：Figure 4、5、6–10、11，以及 Appendix Figure A.12。
A.12 绘制阈值 `theta` 与原始/二值化数据 Pearson 相关系数的关系，只读取
聚合报告，不读取或导出 PISA 原始行数据。

复现脚本只输出聚合参数、矩、收敛信息、采样诊断和 provenance，不会把 PISA 原始行数据写入仓库。完整边界见 `docs/reproduction/PISA_BENCHMARK_CONTRACT.md`。
默认还会在 `data/prepared/pisa2018-paper-reproduction-models/` 保存 15 个
按经济体/学科选出的 PyTorch `.pt` 模型文件；每个文件都可以用
`LearningModel.load()` 重新加载。16 次重复结果仍会全部保留用于 validation。

无需 PISA 数据即可运行完整示例：

```bash
python -m examples.fit_synthetic
```

该示例会生成合成数据，执行 `fit -> analyze -> save`，不会写入任何受限研究数据。

## 项目背景

- 领域：`research Python package for educational and structured-data energy modeling`
- 主要用户：`researchers and machine-learning engineers`
- 当前 MVP 重点：`fit, inspect, and reproduce a binary maximum-entropy learning model`

## PISA 与数据边界

项目不打包或自动上传 PISA 原始数据。使用 PISA 时，应根据匹配的 OECD codebook 创建经过审核的 `PISAMapping`，把原始压缩文件保存在 Git 之外，并只导出聚合参数、诊断和 provenance。普通 `sample_weight` 不等于 PISA 的 replicate weights；复杂抽样方差、plausible values 和官方估计目前不在实现范围内。

从头运行合成示例：

```bash
python -m examples.fit_synthetic
```

更多 API、理论、复现和 HarnessWeaver 规则见 `docs/`。

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
