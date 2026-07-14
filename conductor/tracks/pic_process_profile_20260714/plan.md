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
    - **Evidence:** `contracts/process-profile/CONSUMER_INVENTORY.md` records six current consumers, evidence paths, field cardinality/time/failure semantics, and explicit exclusions.
- [x] Task: Define authority and source-assertion model
    - [x] Distinguish law, regulation, national policy, regional policy, guidance, interpretation, and runtime observation.
    - [x] Define `agent-proposed`, `human-approved`, and official-primary assertion states.
    - [x] Define fail-closed behavior for blocked, stale, conflicting, or missing-effective-date sources.
    - **Acceptance:** controlling assertions cannot be inferred from secondary-only evidence.
    - **Evidence:** `contracts/process-profile/AUTHORITY_MODEL.md` defines authority classes, required assertion fields, controlling eligibility, and explicit fail-closed dispositions.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Consumer and Semantic Inventory' (Protocol in workflow.md)
    - **Review:** Phase 1 review found no consumerless normative field or authority-state gap; exclusions explicitly reject ontology, BPMN, platform, and runtime-AI expansion.

> CHECKPOINT (2026-07-15): `contracts/process-profile/CONSUMER_INVENTORY.md` limits the profile to concepts consumed by FOI-O, the Docassemble demo, service examples, harnesses, and the health pathway requirements. `contracts/process-profile/AUTHORITY_MODEL.md` separates authority classes, effective dates, retrieval dates, reviewer states, and fail-closed dispositions. Full `make check` passed after both tasks. Schema implementation remains next; no legal, clinical, funding, or platform authority is claimed.

## Phase 2 - Contract and Validator

- [x] Task: Write process-profile schema and validator tests
    - [x] Add at least two valid examples covering FOI-O and a synthetic human-review process.
    - [x] Add invalid examples for authority, temporal, transition, task-kind, source-state, and trace-link failures.
    - [x] Add compatibility tests for existing PIC identifiers.
    - **Acceptance:** tests fail for the intended unsupported contract before implementation.
    - **Evidence:** `contracts/tools/tests/test_process_profile_schema.py` and the valid/invalid corpus define the intended red/green behavior; targeted collection fails until `process-profile/0.1.0` and validator discovery are implemented.
- [ ] Task: Implement process-profile schemas and validator
    - [ ] Add versioned schemas, canonical examples, diagnostics, and CLI discovery.
    - [ ] Preserve all existing PIC validation behavior.
    - [ ] Produce deterministic normalized traces for comparison.
    - **Acceptance:** valid/invalid corpus and >=80% relevant coverage pass.
- [x] Task: Document semantics and projection rules
    - [x] Define normative lifecycle semantics and non-normative platform guidance.
    - [x] Document representational loss and exception handling.
    - [x] Add migration notes and changelog entries.
    - **Acceptance:** no platform-specific term is required to implement core semantics.
    - **Evidence:** `contracts/process-profile/0.1.0/SPEC.md`, `README.md`, and `CHANGELOG.md` define lifecycle semantics, non-normative projection loss, safety boundaries, and migration posture.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Contract and Validator' (Protocol in workflow.md)
    - **Review:** Phase 2 review fixed identifier compatibility, semantic reference validation, schema discovery, and lint issues; no platform-specific term is required by the normative contract.

> CHECKPOINT (2026-07-15): `process-profile/0.1.0` now has a versioned JSON Schema, valid/invalid corpus, deterministic semantic checks, PIC identifier compatibility coverage, lifecycle specification, projection-loss rules, and changelog. Full `make check` passes with 57 contract-tool tests. FOI-O remains a semantic consumer and external engines remain adapters.

## Phase 3 - FOI-O Baseline Validation

- [x] Task: Build FOI-O compatibility profile and candidate corpus
    - [x] Map state, event, statutory-clock, transfer, extension, refusal, and review traces by stable identifier.
    - [x] Record unsupported or lossy mappings explicitly.
    - [x] Keep AI-drafted mappings in candidates pending human review.
    - [x] Implement profile data under `subrepos/process-mappings/profiles/foi/` and consume pinned foi-process exports only as execution evidence.
    - **Acceptance:** the corpus validates and does not alter FOI-O runtime authority.
    - **Evidence:** `subrepos/process-mappings/profiles/foi/PROFILE_CANDIDATES.json` and `SOURCE_MANIFEST.json` contain candidate-only mappings, explicit loss, unsupported cases, and pinned contract provenance.
- [ ] Task: [HUMAN] Certify controlling FOI-O mappings
    - [ ] Present only contested source assertions and mapping exceptions.
    - [ ] Record approval, rejection, or required changes per assertion.
    - **Acceptance:** certified fixtures contain no agent-only controlling assertion.
- [ ] Task: Run full compatibility and regression gates
    - [ ] Run `make check`, schema corpus checks, and FOI-O profile validation.
    - [ ] Update consumer and compatibility matrices.
    - **Acceptance:** all gates pass or exact external/human blockers are recorded.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - FOI-O Baseline Validation' (Protocol in workflow.md)
