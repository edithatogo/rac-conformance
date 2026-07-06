# Implementation Plan

Depends on: `adoption_closure_20260706` Phase 1. Do not start schema edits until consumer feedback is inventoried.

## Phase 1 - Feedback Ledger

- [ ] Task: Create `contracts/FEEDBACK.md`
    - [ ] Inventory feedback from `external/ADOPTION_STATUS.md`, issue/PR comments, DBN responses, and local implementation pain.
    - [ ] Classify each request by source, urgency, consumer, and evidence.
    - [ ] Mark speculative ideas as rejected or deferred.
    - **Acceptance:** every proposed v0.2 change has a named consumer or is deferred.
- [ ] Task: Define v0.2 scope
    - [ ] Draft `contracts/VERSIONING.md` or update `contracts/README.md` with v0.2 scope rules.
    - [ ] Decide which contract packages, if any, require v0.2 directories.
    - **Acceptance:** scope has no unbacked ontology/JSON-LD/expression-language additions.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Feedback Ledger' (Protocol in workflow.md)

## Phase 2 - Contract Changes

- [ ] Task: Write tests for selected v0.2 changes
    - [ ] Add failing schema/validator tests first.
    - [ ] Add valid and invalid examples for each changed contract.
    - **Acceptance:** tests fail for the intended missing v0.2 behavior before implementation.
- [ ] Task: Implement v0.2 schemas and validator support
    - [ ] Add new version directories only for changed contracts.
    - [ ] Preserve v0.1 validation behavior.
    - [ ] Update `pic-validate` discovery as needed.
    - **Acceptance:** all contract examples validate or fail as expected.
- [ ] Task: Write migration notes
    - [ ] Add changelog entries for each changed contract.
    - [ ] Add migration examples for breaking changes.
    - **Acceptance:** a consumer can tell whether they need to migrate.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Contract Changes' (Protocol in workflow.md)

## Phase 3 - Consumer Validation

- [ ] Task: Validate active consumers
    - [ ] Run `pic-validate` over `contracts/examples`, `external/foi-o/rules`, `studies/snap-divergence`, and Axiom fixtures.
    - [ ] Update consumer artifacts only where required.
    - **Acceptance:** active consumers validate cleanly or have explicit migration blockers.
- [ ] Task: GitHub Actions and PR readiness
    - [ ] Run `make check`.
    - [ ] Push branch when authorized.
    - [ ] Monitor GitHub Actions after push.
    - [ ] Apply fixes until checks pass or blocker is documented.
    - **Acceptance:** branch has green Actions or exact external blocker.
- [ ] Task: [HUMAN] Approve v0.2 publication posture
    - [ ] Present feedback ledger, diff, consumer validation, and migration notes.
    - [ ] Dylan decides whether v0.2 is published, deferred, or kept experimental.
    - **Acceptance:** publication status is recorded.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Consumer Validation' (Protocol in workflow.md)
