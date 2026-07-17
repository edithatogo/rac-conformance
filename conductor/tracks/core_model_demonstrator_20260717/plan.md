# Implementation Plan

GitHub programme issue: [#38](https://github.com/edithatogo/rac-conformance/issues/38).
Consumes completed work from [#39](https://github.com/edithatogo/rac-conformance/issues/39),
[#40](https://github.com/edithatogo/rac-conformance/issues/40), and
[#41](https://github.com/edithatogo/rac-conformance/issues/41).

## Phase 1 - Core contract audit

- [x] Task: Audit the released PIC contracts and validator corpus
    - [x] Confirm every core schema has valid and invalid examples.
    - [x] Confirm deterministic validation, diff, compatibility, and example commands pass.
    - [x] Confirm money remains decimal-string and no runtime AI dependency exists.
    - **Acceptance:** a clean checkout reproduces the core contract evidence without external repositories.
    - **Evidence:** `CORE_CONTRACT_AUDIT.md`; `make check` passed on 2026-07-17.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Core contract audit'

> CHECKPOINT (2026-07-17): Phase 1 audit was reviewed through PR #120; hosted
> checks passed and review comments were fixed before merge.

## Phase 2 - Process-profile closure

- [x] Task: Audit `pic-process-profile/0.1.0` against its consumer inventory
    - [x] Confirm states, events, actors, timers, tasks, source assertions, exceptions, and traces have named consumers.
    - [x] Confirm controlling assertions fail closed on ineligible review state or missing effective date.
    - [x] Confirm normalized trace projection is deterministic and platform-neutral.
    - **Acceptance:** the profile contract is implementable without FOI-O, BPMN, or a workflow engine.
    - **Evidence:** `PROCESS_PROFILE_CLOSURE_AUDIT.md`; `contracts/tools/tests/test_process_profile_schema.py`; `make check` passed on 2026-07-17.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Process-profile closure'

> CHECKPOINT (2026-07-17): Phase 2 closure audit was reviewed through PR #121;
> the determinism regression was strengthened and all hosted checks passed.

## Phase 3 - FOI demonstrator certification

- [x] Task: Reconcile FOI-O candidate, foi-process execution, and PIC trace evidence
    - [x] Validate the candidate profile and deterministic execution trace together.
    - [x] Record representational loss, unavailable source material, and non-claims.
    - [x] Ensure no candidate fixture is promoted by the implementing agent.
    - **Acceptance:** the demonstrator has a reproducible source-to-profile-to-trace evidence chain.
    - **Evidence:** `FOI_DEMONSTRATOR_CHAIN.json`, `FOI_DEMONSTRATOR_CERTIFICATION_PACKET.md`, `external/foi-process/SUBMISSION.md`; `make check` passed on 2026-07-17.
- [ ] Task: [HUMAN] Certify the FOI-O demonstrator boundary
    - [ ] Review only the combined execution evidence, shared-concept boundary, representational losses, and non-claims; the exact profile's prior compatibility certification is not reopened.
    - [ ] Record certification or required changes against immutable digests.
    - **Acceptance:** certification is explicit and does not claim legal authority or universal portability.
    > BLOCKED (2026-07-17): Dylan must review `FOI_DEMONSTRATOR_CERTIFICATION_PACKET.md` and record the bounded certification decision. The implementing agent cannot certify the chain or promote the candidate.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - FOI demonstrator certification'

## Phase 4 - Local hardening and core readiness

- [x] Task: Run local hardening and reproducibility qualification
    - [x] Run hostile-input, property, mutation, SBOM, reproducibility, and rollback-tabletop evidence.
    - [x] Re-run `make check` from a clean worktree and record exact commit/digests.
    - [x] Keep hosted attestations, signing, live rollback, and external evidence explicitly deferred.
    - **Acceptance:** local core evidence is reproducible and residual external gates are named rather than hidden.
    - **Evidence:** `CORE_HARDENING_EVIDENCE.md`; existing `security/`, `docs/V1_REPRODUCIBILITY.json`, `docs/V1_MUTATION_GATE.json`; `make check` passed on 2026-07-17.
- [x] Task: Prepare core demonstrator readiness packet
    - [x] State the core claims supported by each evidence level.
    - [x] Link the FOI-O certification, normalized trace, validator corpus, and hardening evidence.
    - [x] Link [DEFERRED_ROADMAP.md](../../DEFERRED_ROADMAP.md) for all excluded work.
    - **Acceptance:** a reviewer can distinguish model completeness, demonstration evidence, and deferred programme work.
    - **Evidence:** [CORE_READINESS_PACKET.md](CORE_READINESS_PACKET.md); human certification remains the explicit Phase 3 gate.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Local hardening and core readiness'

> CHECKPOINT (2026-07-17): Phase 4 evidence and readiness packet were reviewed
> through PRs #123 and #124; hosted checks passed. Hosted attestations, signing,
> live rollback, and human certification remain explicitly outside this local
> checkpoint.
