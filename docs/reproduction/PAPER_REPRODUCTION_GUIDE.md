# 用 `learnenergy` 复现论文

本文说明如何使用本项目的 Python package 复现论文 *A Neural Network Model
for Learning - Application to PISA 2018 Data*。文档给出两条路径：

1. **调用公开 API**：适合把同一套模型用于自己的数据，或逐步控制每个训练环节。
2. **运行论文协议脚本**：适合按照论文的 PISA 2018 设置批量完成 15 个“经济体 × 学科”组合。

这里的模型是二值 pairwise maximum-entropy energy model，不是普通的前馈神经网络。
模型约定为：

```text
E(s) = h·s + Σ(i<j) J[i,j] s[i]s[j]
p(s) ∝ exp(-E(s))
```

`h` 是节点场，`J` 是对称的两两相互作用矩阵。节点冻结和有效相互作用是模型内部的结构分析，不能解释为因果效应或个体干预建议。

## 1. 安装

在项目根目录创建并激活虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install -U pip
python -m pip install -e '.[pisa,visualization]'
```

如果只使用自己的 CSV/NumPy 数据，不需要 PISA reader，可以安装：

```bash
python -m pip install -e .
```

## 2. 数据准备原则

论文复现需要自己从 OECD 获得并审核数据文件和 codebook。原始 PISA 文件、抽样行、训练产生的 `.pt` 模型和本地报告都应保留在本机，不要提交到 GitHub。

建议的本地目录：

```text
data/
  raw/        # 本地 PISA SAS/SPSS/CSV/ZIP 文件，不提交
  prepared/   # 本地报告、图和模型，不提交
```

在训练之前必须确认：

- 每个模型节点对应的 OECD 变量名和 respondent level；
- 源文件版本、经济体代码和学科 plausible value；
- PISA 缺失值代码及其 recode 规则；
- 特征顺序、目标变量、权重字段和抽样范围；
- 是否使用普通 row weight。当前包尚未实现 PISA replicate weights、plausible-value aggregation 或官方复杂抽样方差估计，因此结果不能称为官方 PISA 估计。

变量映射应保存为不含数据行的 JSON：

```python
from learnenergy import PISAMapping

mapping = PISAMapping(
    feature_names=("HOMEPOS", "CULTPOSS", "HEDRES"),
    target_name="PV1MATH",
    weight_name="W_FSTUWT",
    missing_values=(-9999.0, -999.0),  # 必须按匹配 codebook 审核
    metadata={
        "cycle": "PISA 2018",
        "scope": "TAP",
        "respondent_level": "student",
        "codebook": "local reference",
    },
)
mapping.save("data/prepared/pisa-mapping.json")
```

## 3. 用公开 API 训练一个自己的模型

下面的例子展示完整的 package 调用方式。它读取一个本地表格，按显式映射取列，训练 19 个二值节点，并保存可重新加载的 PyTorch `.pt` 文件。

```python
from pathlib import Path

import numpy as np

from learnenergy import DataConfig, LearningModel, PISAMapping, read_pisa_file

FEATURES = (
    "HOMEPOS", "CULTPOSS", "HEDRES", "WEALTH", "ICTRES",
    "DISCLIMA", "TEACHSUP", "DIRINS", "PERFEED", "STIMREAD",
    "COMPETE", "WORKMAST", "EUDMO", "BEINGBULLIED", "ENTUSE",
    "SOIAICT", "ICTCLASS", "ICTOUTSIDE",
)

mapping = PISAMapping(
    feature_names=FEATURES,
    target_name="PV1MATH",
    missing_values=(),  # 用实际 codebook 审核后的代码替换
    metadata={"cycle": "PISA 2018", "scope": "TAP"},
)

table = read_pisa_file("data/raw/pisa2018.sas7bdat")

# 只保留已审核的一个经济体；不要把原始 table 写进模型文件。
table = table.loc[table["CNT"] == "TAP", [*FEATURES, "PV1MATH"]]
table = table.dropna().sample(n=1200, random_state=7)

config = DataConfig(
    feature_names=FEATURES,
    target_name="PV1MATH",
    threshold_method="paper_std",
    normalization="zscore",
    missing_strategy="error",
    metadata={
        "cycle": "PISA 2018",
        "scope": "TAP",
        "sampling": "1200 rows without replacement",
        "threshold_scope": "per_sample_repeat",
    },
)

model = LearningModel(
    config,
    calculation="exact",
    max_exact_nodes=19,
    learning_rate=0.5,
    max_epochs=1500,
    tolerance=1e-3,
    seed=7,
)

fit = model.fit(
    table.loc[:, FEATURES].to_numpy(),
    table["PV1MATH"].to_numpy(),
    method="kl",  # 论文协议使用显式 KL-gradient 迭代
)

analysis = model.analyze()
effective = model.effective_interaction_report(calculation="monte_carlo")
temperature = model.temperature_response(np.linspace(0.05, 4.0, 160))

print("converged:", fit.converged)
print("epochs:", fit.epochs)
print("h:", analysis.h)
print("J shape:", analysis.J.shape)
print("MC diagnostics:", effective.diagnostics)

model.save("data/prepared/TAP-PV1MATH.pt")
```

说明：`normalization="zscore"` 和 `threshold_method="paper_std"` 是论文复现设置。对经过 z-score 的变量，严格规则 `f > population standard deviation` 等价于 `z > 1`。如果训练自己的数据而不是复现论文，可以根据研究问题改用默认的 median threshold，但必须把配置写进报告。

如果要运行原始仓库风格的近似训练路径，可以改用：

```python
model = LearningModel(
    config,
    calculation="monte_carlo",
    learning_rate=0.001,
    mc_samples=2**20,
    mc_burn_in=1024,
    seed=7,
)
fit = model.fit(X, y, method="adam")
```

这与原始仓库的“Monte Carlo 估计 moments，再用 Adam 更新”流程相近，但当前包仍使用 `{0, 1}` 状态和 Gibbs sampler；原仓库使用 `{-1, +1}` spin、C++ Metropolis 和 HDF5，因此两条路径的参数不能直接逐项比较。

## 4. 直接运行论文协议

如果目标是复现论文的批量结果，推荐直接使用项目内 runner。它会：

- 对每个经济体和 outcome 重复抽取 1,200 行，共 16 次；
- 每个 repeat 独立进行 z-score 和严格标准差二值化；
- 使用 19 节点 exact enumeration 和显式 KL-gradient 训练；
- 使用 Monte Carlo 计算 effective interaction，并保存 R-hat、ESS、MCSE 等诊断；
- 保留 16 次 repeat 用于验证，并为每个经济体/outcome 选择一个 `.pt` 模型。

```bash
python -u examples/pisa_paper_reproduction.py \
  --input data/raw/pisa2018.sas7bdat \
  --economy-column CNT \
  --output data/prepared/pisa2018-paper-reproduction-report.json \
  --status-file data/prepared/pisa2018-paper-reproduction-status.json \
  --model-dir data/prepared/pisa2018-paper-reproduction-models \
  --sample-size 1200 \
  --repeats 16 \
  --seed 0 \
  --learning-rate 0.5 \
  --max-epochs 1500 \
  --tolerance 1e-3
```

默认输出均为本地生成物：

```text
data/prepared/
  pisa2018-paper-reproduction-report.json
  pisa2018-paper-reproduction-status.json
  pisa2018-paper-reproduction-models/
    TAP-PV1MATH.pt
    ...
```

模型 `.pt` 是 PyTorch 序列化 artifact，包含参数、特征顺序、阈值、归一化统计量和聚合质量信息，不包含原始输入行。可以这样重新加载：

```python
from learnenergy import LearningModel

model = LearningModel.load("data/prepared/pisa2018-paper-reproduction-models/TAP-PV1MATH.pt")
print(model.analyze().to_dict())
```

## 5. 验证结果

对批量报告运行验证：

```bash
python examples/validate_pisa_paper_reproduction.py \
  --report data/prepared/pisa2018-paper-reproduction-report.json \
  --model-dir data/prepared/pisa2018-paper-reproduction-models \
  --output data/prepared/pisa2018-paper-reproduction-validation.json
```

至少检查以下项目：

1. 15 个经济体/outcome 组合是否全部完成；
2. 每个组合是否有 16 个 repeat；
3. target 是否退化为全 0 或全 1；
4. `fit.converged`、最终 KL divergence 和迭代上限；
5. 一阶到四阶 moments 的最大/平均绝对误差；
6. Monte Carlo effective interaction 的 chain、draw、R-hat、ESS、MCSE；
7. 节点顺序、`h`、`J` 的维度和 provenance 是否一致。

验证报告中的 `all_checks_passed` 为 `false` 时，不应直接宣称“完全复现”。需要查看具体失败的是收敛、higher-order moment 误差，还是 Monte Carlo 诊断。

## 6. 生成论文风格图

从 aggregate report 和选定的 `.pt` 文件生成 Figures 3–11：

```bash
python examples/pisa_paper_figures_4_12.py \
  --report data/prepared/pisa2018-paper-reproduction-report.json \
  --output-dir data/prepared/pisa2018-paper-figures-4-12
```

脚本不会再次读取原始 PISA 行，而是使用报告中的聚合字段和模型 artifact。Figure 11 的温度轴使用 `0–4` 的显示范围，并从选定模型重新计算 `T=0.05–4.0` 的 exact-covariance response。Figure A.12 不属于当前输出集合。

## 7. 使用自己的数据

只要数据可以转换为数值特征矩阵和二值目标，就不需要 PISA adapter：

```python
from learnenergy import DataConfig, LearningModel

config = DataConfig(
    feature_names=("feature_a", "feature_b", "feature_c"),
    target_name="outcome",
    threshold_method="median",
    missing_strategy="median",
)
model = LearningModel(config, calculation="auto", seed=7)
fit = model.fit_table(table)
report = model.analyze()
probabilities = model.predict(new_table)
model.save("my-learning-energy-model.pt")
```

`calculation="auto"` 会在节点数不超过 `max_exact_nodes` 时使用 exact enumeration，节点更多时切换到 Gibbs/Monte Carlo。需要论文级可追溯性时，应显式设置 `calculation`、随机种子、预处理、采样诊断和报告版本。

## 关于不二值化的数据

当前 `LearningModel` 的数学对象是二值 pairwise model，不能只删除二值化步骤后继续使用相同的条件概率、节点冻结和参数解释。连续变量需要新的状态空间、能量函数、采样器和归一化约定。

后续可以增加独立的 continuous 或 mixed-node 模型 API，并保留当前 binary API 的兼容性。例如连续节点可以使用 Gaussian/quadratic energy，混合数据则需要定义离散-连续交互项和相应的 sampler。这个方向应作为独立任务设计和验证，而不是悄悄改变当前包的默认语义。

## 8. 复现边界

本项目可以复现论文所需的二值化、19 节点 exact training、显式 KL-gradient、Monte Carlo effective interaction、温度响应和 moment comparison 流程；但数值结果仍取决于数据文件版本、codebook 映射、缺失值处理、抽样种子和运行配置。

因此正确的报告表述应是“在指定数据和协议下的 prepared-sample reproduction”，而不是“官方 PISA 估计”或“教育因果机制”。

更多细节：

- [PISA 2018 数据指南](PISA_2018_DATA_GUIDE.md)
- [PISA benchmark contract](PISA_BENCHMARK_CONTRACT.md)
- [Methods](../guide/methods.md)
- [Parameters](../guide/parameters.md)
- [Fit and inspect](../guide/fit-and-inspect.md)
- [Save and reload](../guide/save-and-reload.md)
