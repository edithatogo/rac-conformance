# Implementation Plan

Depends on: `repo_boundaries_20260706` Phase 1.

## Phase 1 - Coverage Selection

- [x] Task: Audit RuleSpec NZ candidate modules
    - [x] Inspect local and upstream `rulespec-nz` for modules with companion tests.
    - [x] Rank candidates by source clarity, overlap with PIC concepts, and non-trivial output behavior.
    - [x] Record selection in `external/axiom/COVERAGE_PLAN.md`.
    - **Acceptance:** coverage plan names selected and rejected modules with reasons.
- [x] Task: Source assertion check
    - [x] For selected modules, identify source assertions or companion oracle tests.
    - [x] Mark any case without source support as smoke-only, not golden.
    - **Acceptance:** no case is promoted as validation without source/oracle evidence.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Coverage Selection' (Protocol in workflow.md)

> CHECKPOINT (2026-07-06): Phase 1 now has a locked coverage plan and explicit source-assertion ledger for the first Axiom validation slices.
> Confirmed-validation candidates are KiwiSaver contributions and NZ Superannuation, both backed by primary-source anchors plus companion evidence.
> GST, ACC earners levy, and individual income tax remain smoke-only baselines and are not promoted as goldens.
> Reserve social-security coverage is staged as a follow-on slice; broader deferred social-security surfaces remain out of scope until their source support improves.
> `make check` passed across contracts, converters, harness, and snap-divergence runner tests.

## Phase 2 - Fixture And Adapter Expansion

- [x] Task: Write adapter tests first
    - [x] Add failing tests for each new PIC-to-RuleSpec ID mapping.
    - [x] Add failure tests for unmapped IDs and bad value states.
    - **Acceptance:** tests fail before implementation and pass after mappings are added.
- [x] Task: Add PIC fixture documents
    - [x] Add source-backed fixture files under `external/axiom/fixtures/`.
    - [x] Validate with `pic-validate`.
    - **Acceptance:** fixtures validate and preserve oracle independence metadata.

> NOTE (2026-07-06): `pic-validate --no-references external/axiom/fixtures` passes for the new source-backed fixtures; full directory reference checking is blocked by pre-existing smoke fixtures in the same folder that still point at unresolved crosswalk IDs.
- [ ] Task: Implement deterministic mappings
    - [ ] Extend `harness/axiom` only with explicit mappings.
    - [ ] Update runbook with compile/run commands for each slice.
    - **Acceptance:** unit tests and fixture validation pass.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Fixture And Adapter Expansion' (Protocol in workflow.md)

## Phase 3 - Live Runs And CI Integration

- [ ] Task: Run live RuleSpec validation suite
    - [ ] Pin `rulespec-nz` and `axiom-rules-engine` SHAs.
    - [ ] Run the suite locally.
    - [ ] Store reports under `external/axiom/results/`.
    - **Acceptance:** at least 10 cases run or blocker is documented.
- [ ] Task: Add CI-compatible check
    - [ ] Add a smoke CI check that self-skips when external engine artifacts are unavailable.
    - [ ] Keep deterministic unit tests mandatory.
    - **Acceptance:** CI does not require network-only artifacts but verifies mappings and report code.
- [ ] Task: Prepare upstream Axiom feedback
    - [ ] Draft issue/PR text for any discovered integration gap.
    - [ ] Mark submission as `[HUMAN]` unless authenticated approval is explicit.
    - **Acceptance:** feedback artifact is complete or explicitly unnecessary.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Live Runs And CI Integration' (Protocol in workflow.md)

## Phase 4 - External Review Closure

- [ ] Task: Push branch and monitor Actions
    - [ ] Push only after local `make check` passes.
    - [ ] Monitor GitHub Actions until green or blocked.
    - [ ] Apply fixes for agent-addressable failures.
    - **Acceptance:** branch has green Actions or exact blocker.
- [ ] Task: [HUMAN] Submit or merge upstream Axiom work
    - [ ] Present report, branch, and feedback text to Dylan.
    - [ ] Record submitted/merged URLs or blocker in `external/ADOPTION_STATUS.md`.
    - **Acceptance:** external state is not ambiguous.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - External Review Closure' (Protocol in workflow.md)
