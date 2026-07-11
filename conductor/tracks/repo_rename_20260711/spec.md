# Repository rename and identity migration

## Objective

Rename `edithatogo/rulesandprocesses` to `edithatogo/rac-conformance` and make the new identity canonical while preserving historical, versioned identifiers.

## Requirements

- Rename the GitHub repository and update the local `origin` remote.
- Update current documentation, citation metadata, security links, project text, and operational ledgers to the new URL.
- Keep published v0.1/v0.2 JSON Schema `$id` values unchanged; they are persistent identifiers and resolve through GitHub redirects.
- Retain RaCX only as historical context and explicitly avoid reviving the superseded “Exchange Superset” claim.
- Verify redirects, cloning, Actions, issues, Projects, and external links after migration.

## Acceptance

- The canonical remote is `https://github.com/edithatogo/rac-conformance`.
- `git remote get-url origin` uses the new URL and `main` is synchronized.
- Current metadata and documentation use the new URL, with historical schema identifiers documented as intentionally stable.
- `make check` and GitHub Actions pass after the rename.
