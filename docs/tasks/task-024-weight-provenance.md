# Task 024: Preserve sample-weight provenance

## Status

Review Ready

## Objective

Record the ordinary row-weight field name alongside model configuration and artifacts.

## Acceptance criteria

- `DataConfig.sample_weight_name` is optional and validated as a separate non-empty column.
- CLI and local PISA workflows populate the field when a weight is supplied.
- Save/load preserves the field name.
- Standard package verification passes.

## Handoff

The field records provenance only; it does not imply PISA replicate-weight or complex-survey inference support.
