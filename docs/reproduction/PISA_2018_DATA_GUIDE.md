# PISA 2018 local-data guide

## Official source

Use the [OECD PISA 2018 Database](https://www.oecd.org/en/data/datasets/pisa-2018-database.html). The page provides questionnaires, codebooks, compendia, and Public Use Files (PUFs) in SAS and SPSS formats for participating countries.

The PUF download link leads to the [OECD PISA PUF user registration form](https://survey.oecd.org/index.php?lang=en&r=survey/index&sid=197663). Access requires the requestor to identify an institution and contact details and to describe the research project.

## Data-use boundary

- Do not commit PISA files, extracted rows, or model artifacts containing PISA-derived raw records.
- Do not redistribute the PUF or make it available to third parties.
- Do not attempt to re-identify students or schools or link records to identifying information.
- Report only aggregated results that cannot reveal individual or school responses.
- Acknowledge the source as: “Programme for International Student Assessment (PISA) Organisation for Economic Co-operation and Development (OECD), Paris”.

These are operational project rules based on the OECD access terms; users must review the current terms before downloading or sharing results.

## Recommended local layout

Keep the downloaded files outside Git, for example:

```text
data/
  raw/                 # local-only PISA files; never commit
  prepared/            # local derived tables; never commit by default
  README.local.md      # optional local notes, no raw values
```

The repository should contain only scripts, field mappings, synthetic fixtures, and documentation. A local workflow can load an OECD CSV/SAS/SPSS file—or a ZIP containing exactly one such data file—select the documented columns, and pass a table-like object to `prepare_tabular_data`.

## Preparation checklist

1. Download the country or multi-country PUF and the matching codebook from the OECD page.
2. Confirm the file version, country/economy code, respondent level, and questionnaire year.
3. Map each model node to a documented PISA variable; record recodes and response-value handling.
4. Select one target and the feature columns. Keep plausible values and replicate-weight decisions explicit.
5. Validate missing-value codes before applying `DataConfig` thresholds. PISA-specific nonresponse codes are not automatically ordinary numeric values.
6. Pass the final table and optional student weight column through `PISAMapping` and `prepare_pisa_file` (or `prepare_tabular_data` for an already-loaded table).
7. Fit locally and export only aggregate parameters, diagnostics, and reproducible mapping metadata.

Example after installing the optional reader dependencies:

```python
from learning_energy_model import DataConfig, LearningModel, PISAMapping, prepare_pisa_file

mapping = PISAMapping(
    feature_names=("FEATURE_A", "FEATURE_B"),
    target_name="TARGET",
    weight_name="W_FSTUWT",
    missing_values=(-9999.0, -999.0),  # confirm against the matching codebook
)
prepared = prepare_pisa_file("data/raw/pisa2018.zip", mapping)
model = LearningModel(DataConfig(feature_names=prepared.feature_names, target_name=prepared.target_name, sample_weight_name=mapping.weight_name, missing_strategy="median"))
result = model.fit(prepared.X, prepared.y, sample_weight=prepared.sample_weight)
model.save("data/prepared/local-model.pt")
```

For a complete local workflow that also writes an aggregate JSON report, use
`python examples/pisa_local_workflow.py --input ... --features ... --target ...`.
The variable names and missing codes must come from the matching codebook; the
script does not infer them.

## Current project limitation

The package currently supports ordinary row weights as `sample_weight`; it does not yet implement PISA’s full complex-survey variance estimation, replicate-weight procedure, plausible-value aggregation, or country-specific field mapping. Until those components are added, results should be described as model estimates on the prepared sample, not official PISA estimates.
