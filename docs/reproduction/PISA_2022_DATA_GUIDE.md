# PISA 2022 local-data guide

## Official source

Use the [OECD PISA data files page](https://webfs.oecd.org/pisa2022/index.html).
For PISA 2022 it currently lists compressed SAS and SPSS files for the school,
student, and teacher questionnaires, cognitive item data, questionnaire timing,
creative thinking, and financial literacy. Select the file that contains the
respondent-level variables required by the reviewed mapping; do not download
every file by default.

## Local-only boundary

- Keep downloaded archives and extracted tables under `data/raw/` or another
  location outside Git.
- Do not commit row-level PISA data, derived row extracts, or model artifacts
  containing raw observations.
- Review the current OECD terms and the matching codebook before using or
  sharing any data or aggregate output.

## Recommended workflow

1. Select one PISA 2022 data file and its matching codebook from the OECD page.
2. Record the file version, country/economy scope, respondent level, and reader
   format (SAS or SPSS).
3. Create a reviewed `PISAMapping` JSON contract containing exact source column
   names, the target, ordinary student weight if applicable, missing-value codes,
   and provenance metadata.
4. Validate the mapping against the codebook. The package intentionally does
   not infer PISA variable names or missing codes.
5. Run the local workflow with the archive and mapping. It extracts a single
   supported member to a temporary location and writes aggregate results only.

Example mapping contract:

```python
from learning_energy_model import PISAMapping

mapping = PISAMapping(
    feature_names=("CODEBOOK_FEATURE_A", "CODEBOOK_FEATURE_B"),
    target_name="CODEBOOK_TARGET",
    weight_name="W_FSTUWT",
    missing_values=(-9999.0, -999.0),  # confirm against the matching codebook
    metadata={
        "cycle": "PISA 2022",
        "scope": "...",
        "respondent_level": "student",
        "codebook": "reviewed-codebook.pdf",
    },
)
mapping.save("data/mapping/pisa2022-reviewed.json")
```

Then use the saved mapping in Python:

```python
from learning_energy_model import LearningModel, PISAMapping, prepare_pisa_file

mapping = PISAMapping.load("data/mapping/pisa2022-reviewed.json")
prepared = prepare_pisa_file("data/raw/pisa2022-student.zip", mapping)
model = LearningModel(
    calculation="auto",
    # PISA-specific missing codes have already been converted by the mapping.
)
fit = model.fit(prepared.X, prepared.y, sample_weight=prepared.sample_weight)
model.save("data/prepared/pisa2022-model.pt")
```

The saved model and benchmark report must state that `sample_weight` is ordinary
row weighting. PISA replicate weights, plausible-value aggregation, and
complex-survey variance estimation are not implemented by this package, so the
result is a model estimate on the prepared sample, not an official PISA estimate.
