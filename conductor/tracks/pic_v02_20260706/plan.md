# Implementation Plan

Depends on: `adoption_closure_20260706` Phase 3. Do not start schema edits until consumer feedback includes real external status, PR/issue responses, or explicitly recorded local implementation friction. Inventory alone is insufficient for v0.2 schema changes.

## Phase 1 - Feedback Ledger

- [x] Task: Create `contracts/FEEDBACK.md`
    - [x] Inventory feedback from `external/ADOPTION_STATUS.md`, issue/PR comments, DBN responses, and local implementation pain.
    - [x] Classify each request by source, urgency, consumer, and evidence.
    - [x] Mark speculative ideas as rejected or deferred.
    - **Acceptance:** every proposed v0.2 change has a named consumer or is deferred.
- [x] Task: Define v0.2 scope
    - [x] Draft `contracts/VERSIONING.md` or update `contracts/README.md` with v0.2 scope rules.
    - [x] Decide which contract packages, if any, require v0.2 directories.
    - **Acceptance:** scope has no unbacked ontology/JSON-LD/expression-language additions.

> CHECKPOINT (2026-07-07): The feedback ledger now separates active from potential consumers, and the Alaveteli request-state proposal is recorded as deferred evidence rather than v0.2 scope.
> `contracts/VERSIONING.md` still limits v0.2 upgrades to `pic-traces` and `pic-parameters`; the contract set does not expand into JSON-LD, ontologies, or expression DSLs.
> `make check` passed at the phase boundary, so the remaining phase work is documentation review and checkpointing only.

- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Feedback Ledger' (Protocol in workflow.md)

## Phase 2 - Contract Changes

- [x] Task: Write tests for selected v0.2 changes (SHA: dce43f8)
    - [x] Add failing schema/validator tests first.
    - [x] Add valid and invalid examples for each changed contract.
    - **Acceptance:** tests fail for the intended missing v0.2 behavior before implementation.
- [x] Task: Implement v0.2 schemas and validator support
    - [x] Add new version directories only for changed contracts.
    - [x] Preserve v0.1 validation behavior.
    - [x] Update `pic-validate` discovery as needed.
    - **Acceptance:** all contract examples validate or fail as expected.
- [x] Task: Write migration notes
    - [x] Add changelog entries for each changed contract.
    - [x] Add migration examples for breaking changes.
    - **Acceptance:** a consumer can tell whether they need to migrate.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Contract Changes' (Protocol in workflow.md)

## Phase 3 - Consumer Validation

- [x] Task: Validate active consumers
    - [x] Run `pic-validate` over `contracts/examples`, `external/foi-o/rules`, `studies/snap-divergence`, and Axiom fixtures.
    - [x] Update consumer artifacts only where required.
    - **Acceptance:** active consumers validate cleanly or have explicit migration blockers.
- [x] Task: GitHub Actions and PR readiness
    - [x] Run `make check`.
    - [x] Push branch when authorized.
    - [x] Monitor GitHub Actions after push.
    - [x] Apply fixes until checks pass or blocker is documented.
    - **Acceptance:** branch has green Actions or exact external blocker.
- [x] Task: [HUMAN] Approve v0.2 publication posture
    - [x] Present feedback ledger, diff, consumer validation, and migration notes.
    - [x] Dylan decides whether v0.2 is published, deferred, or kept experimental.
    - **Acceptance:** publication status is recorded.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Consumer Validation' (Protocol in workflow.md)
