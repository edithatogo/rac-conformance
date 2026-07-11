# Reliability, upstream governance, and publication refinement

## Objective

Bring every open upstream contribution to a consistent, reviewable standard; make this repository's validation and automation fail closed; and align paper claims with reproducible repository evidence.

## Requirements

1. Every upstream PR has a corresponding actionable issue, explicit scope, verification, limitations, and closing linkage where appropriate.
2. Every upstream issue and PR is represented in GitHub Project 19 without claiming maintainer acceptance.
3. Repository CI covers every executable surface, manuscript integrity, workflow hygiene, dependency review, and static security analysis with least-privilege permissions.
4. Contributor templates, ownership, security reporting, dependency updates, and deterministic local audit commands are present.
5. Manuscripts distinguish approved agreements, held divergences, candidate evidence, external gates, and limitations. Claims must be traceable to committed artifacts.

## Constraints

- Do not merge upstream PRs or bypass maintainer review.
- Do not manufacture signing credentials or approve first-time-contributor workflows.
- Do not promote candidate fixtures or legal interpretations.
- No runtime AI decisions.

## Acceptance

- All seven upstream PR/issue pairs pass the governance audit or have an explicit external blocker.
- `make check` and deterministic repository/manuscript audits pass locally and in GitHub Actions.
- Both paper drafts contain reproducibility, limitations, artifact availability, and evidence-calibrated conclusions.
