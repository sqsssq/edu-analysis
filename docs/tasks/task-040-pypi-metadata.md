# Task 040: Add PyPI-ready project metadata

## Status

Review Ready

## Source PRD

- `docs/prd/06-acceptance-criteria.md`
- `docs/prd/DECISION_LOG.md`

## Goal

Make the installable package discoverable and accurately described in package
indexes without publishing it prematurely.

## Scope

- Add supported-version classifiers, keywords, and repository/documentation URLs.
- Keep the alpha development status and deferred final naming decision explicit.
- Verify the generated wheel metadata.

## Out of Scope

- Uploading to PyPI.
- Changing the package name or release version without a naming/release decision.

## Acceptance Criteria

- `pyproject.toml` parses with the intended project metadata.
- The built wheel carries the URLs, classifiers, and Apache-2.0 license metadata.
- Standard package verification passes.

## Done When

- PyPI metadata is aligned, verified, documented, committed, and pushed.
