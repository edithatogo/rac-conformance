# Implementation Plan

GitHub issue: [#40](https://github.com/edithatogo/rac-conformance/issues/40). Depends on [#39](https://github.com/edithatogo/rac-conformance/issues/39) Phase 1.

## Phase 1 - Consumer and Semantic Inventory

- [ ] Task: Inventory process concepts from real consumers
    - [ ] Extract only consumed concepts from FOI-O, the existing Docassemble demo, harness traces, and approved health demonstrator requirements.
    - [ ] Record concept owner, consumer, cardinality, time semantics, and failure behavior.
    - [ ] Reject ontology, BPMN, and workflow-engine concepts with no current consumer.
    - **Acceptance:** every proposed field has a named consumer and evidence artifact.
- [ ] Task: Define authority and source-assertion model
    - [ ] Distinguish law, regulation, national policy, regional policy, guidance, interpretation, and runtime observation.
    - [ ] Define `agent-proposed`, `human-approved`, and official-primary assertion states.
    - [ ] Define fail-closed behavior for blocked, stale, conflicting, or missing-effective-date sources.
    - **Acceptance:** controlling assertions cannot be inferred from secondary-only evidence.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Consumer and Semantic Inventory' (Protocol in workflow.md)

## Phase 2 - Contract and Validator

- [ ] Task: Write process-profile schema and validator tests
    - [ ] Add at least two valid examples covering FOI-O and a synthetic human-review process.
    - [ ] Add invalid examples for authority, temporal, transition, task-kind, source-state, and trace-link failures.
    - [ ] Add compatibility tests for existing PIC identifiers.
    - **Acceptance:** tests fail for the intended unsupported contract before implementation.
- [ ] Task: Implement process-profile schemas and validator
    - [ ] Add versioned schemas, canonical examples, diagnostics, and CLI discovery.
    - [ ] Preserve all existing PIC validation behavior.
    - [ ] Produce deterministic normalized traces for comparison.
    - **Acceptance:** valid/invalid corpus and >=80% relevant coverage pass.
- [ ] Task: Document semantics and projection rules
    - [ ] Define normative lifecycle semantics and non-normative platform guidance.
    - [ ] Document representational loss and exception handling.
    - [ ] Add migration notes and changelog entries.
    - **Acceptance:** no platform-specific term is required to implement core semantics.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Contract and Validator' (Protocol in workflow.md)

## Phase 3 - FOI-O Baseline Validation

- [ ] Task: Build FOI-O compatibility profile and candidate corpus
    - [ ] Map state, event, statutory-clock, transfer, extension, refusal, and review traces by stable identifier.
    - [ ] Record unsupported or lossy mappings explicitly.
    - [ ] Keep AI-drafted mappings in candidates pending human review.
    - **Acceptance:** the corpus validates and does not alter FOI-O runtime authority.
- [ ] Task: [HUMAN] Certify controlling FOI-O mappings
    - [ ] Present only contested source assertions and mapping exceptions.
    - [ ] Record approval, rejection, or required changes per assertion.
    - **Acceptance:** certified fixtures contain no agent-only controlling assertion.
- [ ] Task: Run full compatibility and regression gates
    - [ ] Run `make check`, schema corpus checks, and FOI-O profile validation.
    - [ ] Update consumer and compatibility matrices.
    - **Acceptance:** all gates pass or exact external/human blockers are recorded.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - FOI-O Baseline Validation' (Protocol in workflow.md)
