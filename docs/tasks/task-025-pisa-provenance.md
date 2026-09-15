# Task 025: Record PISA run provenance

## Status

Review Ready

## Objective

Require the local PISA workflow to record assessment cycle, data scope, and codebook reference in the saved model metadata.

## Acceptance criteria

- The workflow requires explicit cycle, scope, and codebook arguments.
- Values are preserved in `DataConfig.metadata` and therefore in the model artifact.
- The PISA benchmark contract and local guide describe the requirement.
- Standard package verification passes.

## Handoff

These fields document provenance only; they do not validate the codebook or implement survey-design inference.
