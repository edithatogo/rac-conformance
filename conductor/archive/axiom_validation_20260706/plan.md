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
- [x] Task: Implement deterministic mappings
    - [x] Extend `harness/axiom` only with explicit mappings.
    - [x] Update runbook with compile/run commands for each slice.
    - **Acceptance:** unit tests and fixture validation pass.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Fixture And Adapter Expansion' (Protocol in workflow.md)

> CHECKPOINT (2026-07-06): Phase 2 now has explicit KiwiSaver and NZ Superannuation adapters, source-backed candidate fixture files, and slice-specific runbook commands.
> The new adapter tests pass, including bad value-state rejection and unmapped-ID failures.
> `pic-validate --no-references external/axiom/fixtures` passes for the new fixture documents; full directory reference validation is still blocked by the pre-existing smoke fixtures in the same folder.
> `make check` passed at the phase boundary.

## Phase 3 - Live Runs And CI Integration

- [x] Task: Run live RuleSpec validation suite
    - [x] Pin `rulespec-nz` and `axiom-rules-engine` SHAs.
    - [x] Run the suite locally.
    - [x] Store reports under `external/axiom/results/`.
    - **Acceptance:** at least 10 cases run or blocker is documented.

> NOTE (2026-07-06): The live suite ran 10 cases with 10 exact matches and stored reports under `external/axiom/results/rulespec-nz-live-suite/`. KiwiSaver compilation from `.external-repos/rulespec-nz` still fails with a YAML parse error at `rules[1].versions[0].values`, so that slice remains blocked separately from the successful live set.
- [x] Task: Add CI-compatible check
    - [x] Add a smoke CI check that self-skips when external engine artifacts are unavailable.
    - [x] Keep deterministic unit tests mandatory.
    - **Acceptance:** CI does not require network-only artifacts but verifies mappings and report code.

> NOTE (2026-07-06): The CI workflow now runs harness tests and a smoke check that exits cleanly when the external Axiom engine artifacts are absent. Locally, the smoke check reuses the compiled artifacts and live-suite runner.
- [x] Task: Prepare upstream Axiom feedback
    - [x] Draft issue/PR text for any discovered integration gap.
    - [x] Mark submission as `[HUMAN]` unless authenticated approval is explicit.
    - **Acceptance:** feedback artifact is complete or explicitly unnecessary.

> NOTE (2026-07-06): The staged feedback draft covers the KiwiSaver compile blocker observed under the pinned engine/repo pair. The rest of the live suite remains green.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Live Runs And CI Integration' (Protocol in workflow.md)

> CHECKPOINT (2026-07-06): The live Axiom suite ran 10 cases with 10 exact matches and wrote the report packet under `external/axiom/results/rulespec-nz-live-suite/`.
> The CI workflow now runs harness tests plus a skip-aware smoke check, so repository CI does not require external engine artifacts.
> The upstream feedback draft is staged for the KiwiSaver compile blocker, which still fails under the pinned engine/repo pair.
> `make check` was green at the phase boundary.

## Phase 4 - External Review Closure

- [x] Task: Push branch and monitor Actions
    - [x] Push only after local `make check` passes.
    - [x] Monitor GitHub Actions until green or blocked.
    - [x] Apply fixes for agent-addressable failures.
    - **Acceptance:** branch has green Actions or exact blocker.
- [x] Task: [HUMAN] Submit or merge upstream Axiom work
    - [x] Present report, branch, and feedback text to Dylan.
    - [x] Record submitted/merged URLs or blocker in `external/ADOPTION_STATUS.md`.
    - **Acceptance:** external state is not ambiguous.

> NOTE (2026-07-06): Branch `main` is pushed and GitHub Actions run `28796868138` completed successfully after the local harness fixes.
>
> CHECKPOINT (2026-07-09): Upstream KiwiSaver compile feedback submitted as [TheAxiomFoundation/rulespec-nz#79](https://github.com/TheAxiomFoundation/rulespec-nz/issues/79). Ledger and `UPSTREAM_FEEDBACK.md` updated. Maintainer response / module fix remains external; agent submission gate is closed.

- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - External Review Closure' (Protocol in workflow.md)

> CHECKPOINT (2026-07-09): Phase 4 closed for agent purposes. External Axiom KiwiSaver compile issue is filed with a durable URL; live suite remains green for non-KiwiSaver slices.
