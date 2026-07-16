# Implementation Plan

GitHub issue: [#40](https://github.com/edithatogo/rac-conformance/issues/40). Depends on [#39](https://github.com/edithatogo/rac-conformance/issues/39) Phase 1.

Repository home: normative contract work remains in
`contracts/process-profile/` and `contracts/tools/`; source-backed profile data
is implemented under `subrepos/process-mappings/profiles/` during incubation
under [#50](https://github.com/edithatogo/rac-conformance/issues/50).

## Phase 1 - Consumer and Semantic Inventory

- [x] Task: Inventory process concepts from real consumers
    - [x] Extract only consumed concepts from FOI-O, the existing Docassemble demo, harness traces, and approved health demonstrator requirements.
    - [x] Record concept owner, consumer, cardinality, time semantics, and failure behavior.
    - [x] Reject ontology, BPMN, and workflow-engine concepts with no current consumer.
    - **Acceptance:** every proposed field has a named consumer and evidence artifact.
    - Evidence: `contracts/process-profile/CONSUMER_INVENTORY.md`.
- [x] Task: Define authority and source-assertion model
    - [x] Distinguish law, regulation, national policy, regional policy, guidance, interpretation, and runtime observation.
    - [x] Define `agent-proposed`, `human-approved`, and official-primary assertion states.
    - [x] Define fail-closed behavior for blocked, stale, conflicting, or missing-effective-date sources.
    - **Acceptance:** controlling assertions cannot be inferred from secondary-only evidence.
    - Evidence: `contracts/process-profile/DESIGN.md`, schema semantics, and negative examples.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Consumer and Semantic Inventory' (Protocol in workflow.md)

> CHECKPOINT (2026-07-16): Phase 1 is complete. The consumer inventory names
> the FOI-O, foi-process, health-profile, and optional Camunda consumers for
> each field. Authority, review, effective-date, and fail-closed semantics are
> documented and exercised by the process-profile corpus. No ontology or
> platform runtime was added.

> COMPLETION AUDIT (2026-07-16): The profile schema explicitly includes
> actors/authority links and timers/deadline declarations, in addition to the
> original state, event, transition, task, rule, evidence, exception, and
> trace records. Timer arithmetic remains in PIC parameters/rules. Required
> source, actor, timer, and trace links fail closed when omitted or unknown.

## Phase 2 - Contract and Validator

- [x] Task: Write process-profile schema and validator tests
    - [x] Add at least two valid examples covering FOI-O and a synthetic human-review process.
    - [x] Add invalid examples for authority, temporal, transition, task-kind, source-state, and trace-link failures.
    - [x] Add compatibility tests for existing PIC identifiers.
    - **Acceptance:** tests fail for the intended unsupported contract before implementation.
    - Evidence: `contracts/process-profile/0.1.0/examples/` and `contracts/tools/tests/test_process_profile_schema.py`.
- [x] Task: Implement process-profile schemas and validator
    - [x] Add versioned schemas, canonical examples, diagnostics, and CLI discovery.
    - [x] Preserve all existing PIC validation behavior.
    - [x] Produce deterministic normalized traces for comparison.
    - **Acceptance:** valid/invalid corpus and >=80% relevant coverage pass.
    - Evidence: schema, `pic_contracts.validation`, and deterministic `normalize_trace` projection.
- [x] Task: Document semantics and projection rules
    - [x] Define normative lifecycle semantics and non-normative platform guidance.
    - [x] Document representational loss and exception handling.
    - [x] Add migration notes and changelog entries.
    - **Acceptance:** no platform-specific term is required to implement core semantics.
    - Evidence: `SPEC.md`, `DESIGN.md`, and `CHANGELOG.md`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Contract and Validator' (Protocol in workflow.md)

> CHECKPOINT (2026-07-16): Phase 2 is complete. The versioned schema has two
> valid examples and three invalid examples, semantic validation covers source
> authority, time ordering, references, task kinds, and deterministic rule
> links, and normalized traces are sorted deterministically. The full contract
> corpus passes; repository-wide coverage is verified by the full `make check`
> gate rather than the focused test invocation.

## Phase 3 - FOI-O Baseline Validation

> CHECKPOINT (2026-07-16): The engineering portion of Phase 3 is complete.
> The candidate profile, pinned contract-consumption manifest, source/loss
> packet, candidate validator, standalone incubator check, and full `make
> check` all pass. The only remaining task is the explicit human certification
> of the candidate mapping; no agent has promoted it.

- [x] Task: Build FOI-O compatibility profile and candidate corpus
    - [x] Map state, event, statutory-clock, transfer, extension, refusal, and review traces by stable identifier.
    - [x] Record unsupported or lossy mappings explicitly.
    - [x] Keep AI-drafted mappings in candidates pending human review.
    - [x] Implement profile data under `subrepos/process-mappings/profiles/foi/` and consume pinned foi-process exports only as execution evidence.
    - **Acceptance:** the corpus validates and does not alter FOI-O runtime authority.
    - Evidence: `subrepos/process-mappings/profiles/foi/candidates/` and `CANDIDATE_REVIEW.md`.
- [x] Task: [HUMAN] Certify controlling FOI-O mappings
    - [x] Present only contested source assertions and mapping exceptions.
    - [x] Record approval, rejection, or required changes per assertion.
    - **Acceptance:** certified fixtures contain no agent-only controlling assertion.
    - Packet: `HUMAN_CERTIFICATION_PACKET.md`.
    - Evidence: `CERTIFICATION_RECORD.json` records Dylan's certification of the PIC compatibility projection; canonical repository promotion remains deferred to #50.
- [x] Task: Run full compatibility and regression gates
    - [x] Run `make check`, schema corpus checks, and FOI-O profile validation.
    - [x] Update consumer and compatibility matrices.
    - **Acceptance:** all gates pass or exact external/human blockers are recorded.
    - Evidence: `make check` passed on 2026-07-16; focused process-profile suite passed with 8 tests; the pinned process-mappings manifest and standalone check validate the candidate.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - FOI-O Baseline Validation' (Protocol in workflow.md)

> REVIEW (2026-07-17): The revised candidate validates through the parent
> process-profile contract, the pinned incubator manifest, and standalone
> checks. `make check` passes. Dylan certified the PIC compatibility projection;
> no canonical candidate promotion occurred.
> REVIEW UPDATE (2026-07-17): The candidate was revised to preserve staged
> FOI-O CoreEvent vocabulary and remove the unsupported terminal reviewability
> implication. The certification packet now asks questions against revision
> `7990b4f`; the human gate was subsequently certified by Dylan, while
> canonical promotion remains deferred to #50.
> REVIEW AID (2026-07-17): Added `MAPPING_REVIEW_MATRIX.md` with row-level
> source vocabulary, PIC representation, and explicit non-claims.
> HUMAN DECISION (2026-07-16): Dylan approved Decision 1, covering the revised
> event vocabulary and non-terminal reviewability semantics.
> HUMAN DECISION (2026-07-16): Dylan approved Decision 2, covering the
> distinction between observed events, executed actions, and derived signals.
> HUMAN DECISION (2026-07-16): Dylan approved Decision 3, confirming that
> reviewability remains a non-terminal derived signal and not a legal or
> Ombudsman outcome.
> HUMAN DECISION (2026-07-16): Dylan approved Decision 4, confirming the
> official source spine, effective date, explicit actors, and timer declaration.
> HUMAN DECISION (2026-07-16): Dylan approved Decision 5, confirming the loss
> notes and explicit non-claims.
> HUMAN CERTIFICATION (2026-07-16): Dylan certified the candidate for PIC
> compatibility. It remains in the incubator candidate directory pending #50.
