# Package Data and Result Model

## Purpose

Describe the structured data contracts and result objects needed for the MVP.

## `DataConfig`

`DataConfig` records the assumptions needed to turn a user dataset into binary model nodes:

- variable names and target name;
- threshold or binarization rule for each variable;
- missing-value strategy;
- optional sample-weight field;
- variable metadata and semantic descriptions;
- preprocessing version and review status.

## Model and Results

- `LearningModel`: model configuration, `h`, `J`, target node, backend, and serialization metadata.
- `FitResult`: convergence status, objective history, observed/model moments, sampler diagnostics, and warnings.
- `PredictionResult`: target probability, optional energy score, uncertainty interval, and preprocessing metadata.
- `AnalysisResult`: correlations, higher-order moments, node-freezing results, energy/entropy diagnostics, assumptions, and limitations.
- `model.sample(n_samples)`: draws binary states from the fitted joint distribution, using exact probabilities or Gibbs sampling according to model size.
- `FitResult`, `PredictionResult`, and `AnalysisResult` expose `to_dict()` and `to_json()` for dependency-light aggregate export, plus optional `to_dataframe()` when pandas is installed.

## Serialization Contract

Saved artifacts include parameters, variable names, preprocessing rules, package/model version, random seed, sampler state, training logs, and evaluation results. Raw user data is excluded by default.

## Review or Quality Status

If the project uses content, examples, generated outputs, or expert-reviewed material, define review status here.

Suggested review statuses:

- `placeholder`
- `needs_review`
- `reviewed`
