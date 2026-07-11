# Plan: reliability_publication_20260711

## Phase 1 - Upstream contribution governance

- [x] Task: Audit and normalize all open PR and issue pairs
    - [x] Confirm seven PRs have corresponding upstream issues
    - [x] Add all issue and PR URLs to GitHub Project 19
    - [x] Normalize closing links, summaries, verification, risks, and reviewer asks
    - [x] Record CI, conflict, signing, and maintainer-only gates
- [x] Task: Conductor - Automated Review and Checkpoint 'Upstream contribution governance' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): Seven upstream PR/issue pairs were audited and normalized. All 14 URLs are individual Project 19 items marked In Progress. PR #200 now formally closes #199. RuleSpec NZ #80 was merged with current upstream, its conflict resolved, and its compile/Ruff/270-test surface verified; signed-manifest regeneration remains a maintainer-only gate. Empty upstream check rollups remain explicitly unverified.

## Phase 2 - Harness engineering and automation

- [x] Task: Add deterministic repository and manuscript audits with tests
- [x] Task: Harden CI, dependency, security, ownership, and contribution workflows
- [x] Task: Conductor - Automated Review and Checkpoint 'Harness engineering and automation' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): `make check` now includes deterministic governance/manuscript audits and tests. Full-surface Quality CI, CodeQL, dependency review, Dependabot, issue/PR templates, CODEOWNERS, and SECURITY policy were added. Every action is SHA-pinned, checkout credentials are disabled, workflows have least-privilege permissions/timeouts/concurrency, and `zizmor` reports zero findings.

## Phase 3 - Paper refinement

- [x] Task: Refine coupling paper against current evidence
- [x] Task: Refine SNAP paper against current evidence
- [x] Task: Conductor - Automated Review and Checkpoint 'Paper refinement' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): Both manuscripts now distinguish approved comparisons from held cases, avoid unsupported universal-reliability and no-bug claims, and include data/code availability and limitations. The repository audit rejects recurrence of the identified overclaims and broken local manuscript links.
