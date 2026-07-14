# Implementation Plan

GitHub issue: [#41](https://github.com/edithatogo/rac-conformance/issues/41). Depends on [#40](https://github.com/edithatogo/rac-conformance/issues/40) Phase 2.

## Phase 1 - Source and Authority Spine

- [ ] Task: Build versioned primary-source manifest
    - [ ] Pin current NZ national policy, HDC guidance/Code basis, Australian national framework/standard, and NSW directives/guidance.
    - [ ] Record issuer, jurisdiction, authority type, applicability, effective date, supersession, retrieval time, rights, and digest.
    - [ ] Mark blocked or ambiguous documents explicitly; do not substitute secondary summaries.
    - **Acceptance:** every modeled obligation resolves to a controlling or explicitly non-controlling primary source.
- [ ] Task: Build authority and variation matrix
    - [ ] Separate national consistency layer, jurisdictional requirements, regional implementation, and hypothetical local procedure.
    - [ ] Record actor authority, discretion, required human judgement, and escalation owner.
    - [ ] Identify common core and intentional variation without premature crosswalk claims.
    - **Acceptance:** no national framework is mislabeled as legislation and no local policy is generalized nationally.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Source and Authority Spine' (Protocol in workflow.md)

## Phase 2 - Process Mapping and Triangulation

- [ ] Task: Draft process-profile candidates
    - [ ] Model detection through closure with stable IDs and explicit human tasks.
    - [ ] Model open communication as a continuing relational process, not a one-time notification flag.
    - [ ] Link reporting, complaints, review, disclosure, and improvement as related but distinct processes.
    - **Acceptance:** all mappings are `agent-proposed` until source and human review gates pass.
- [ ] Task: Implement deterministic source triangulation
    - [ ] Require controlling primary-source support for normative obligation labels.
    - [ ] Resolve national/regional overlays by jurisdiction, authority, effective date, and applicability.
    - [ ] Emit exception reasons for blocked source, conflict, missing date, underspecified local procedure, and secondary-only evidence.
    - **Acceptance:** every mapping receives a proposed disposition or explicit exception without case-name-coded rules.
- [ ] Task: Write mapping and resolver tests
    - [ ] Cover harm, near miss, delayed recognition, disputed facts, parallel complaint, and blocked-source cases.
    - [ ] Verify agent-only assertions cannot become certified obligations.
    - [ ] Verify jurisdiction and effective-date leakage fails.
    - **Acceptance:** tests fail before implementation and pass after deterministic resolver work.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Process Mapping and Triangulation' (Protocol in workflow.md)

## Phase 3 - Synthetic Demonstrator and Review

- [ ] Task: Build synthetic candidate fixture corpus
    - [ ] Include culturally responsive participation and support options without asserting substantive adequacy automatically.
    - [ ] Include expected parallel pathways and explicit unresolved questions.
    - [ ] Run process-profile validation and trace generation.
    - **Acceptance:** no fixture contains real or plausibly re-identifiable event data.
- [ ] Task: [HUMAN] Certify contested assertions and interpretation boundaries
    - [ ] Present resolver exceptions, controlling-source assertions, and proposed process differences only.
    - [ ] Record approval, rejection, limits, or further-source requirements.
    - **Acceptance:** human review is focused and every promoted assertion has an auditable decision.
- [ ] Task: Publish comparative findings and limitations
    - [ ] Distinguish source fact, interpretation, executable behavior, variation, and unresolved exception.
    - [ ] Document portability implications for the process profile and Camunda study.
    - **Acceptance:** findings make no organisational-compliance, legal-advice, or clinical-safety claim.
- [ ] Task: Define privacy-preserving post-market safety handoff
    - [ ] Specify the minimum public or appropriately de-identified aggregate event, provenance, authority, jurisdiction, permitted-purpose, and review fields.
    - [ ] Reject patient-level content, inferred causation, and uncertified downstream action.
    - [ ] Add valid and negative examples without making the handoff mandatory for incident workflows.
    - **Acceptance:** the handoff schema and examples validate and strictly exclude patient-level data, causal inference, and uncertified downstream action.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Synthetic Demonstrator and Review' (Protocol in workflow.md)
