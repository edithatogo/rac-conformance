# Implementation Plan

GitHub issue: [#41](https://github.com/edithatogo/rac-conformance/issues/41). Depends on [#40](https://github.com/edithatogo/rac-conformance/issues/40) Phase 2.

Implementation home: `subrepos/process-mappings/profiles/adverse-incidents/`
during the repository incubation governed by
[#50](https://github.com/edithatogo/rac-conformance/issues/50).

## Phase 1 - Source and Authority Spine

> CHECKPOINT (2026-07-15): The adverse-incident profile now has a versioned
> primary-source ledger and an authority/variation matrix covering NZ, Australia,
> and NSW. The matrix distinguishes regulation, national policy, national
> framework, national standard, state directive, regional implementation, and
> hypothetical local procedure. Two NSW official policy downloads remain blocked
> and are recorded as exceptions; no secondary substitute, legal conclusion, or
> clinical judgement has been encoded.

- [x] Task: Build versioned primary-source manifest
    - [x] Store the profile source ledger under `subrepos/process-mappings/profiles/adverse-incidents/sources/`.
    - [x] Pin current NZ national policy, HDC guidance/Code basis, Australian national framework/standard, and NSW directives/guidance.
    - [x] Record issuer, jurisdiction, authority type, applicability, effective date, supersession, retrieval time, rights, and digest.
    - [x] Mark blocked or ambiguous documents explicitly; do not substitute secondary summaries.
    - Evidence: `subrepos/process-mappings/profiles/adverse-incidents/sources/SOURCE_MANIFEST.json`.
    - **Acceptance:** every modeled obligation resolves to a controlling or explicitly non-controlling primary source.
- [x] Task: Build authority and variation matrix
    - [x] Separate national consistency layer, jurisdictional requirements, regional implementation, and hypothetical local procedure.
    - [x] Record actor authority, discretion, required human judgement, and escalation owner.
    - [x] Identify common core and intentional variation without premature crosswalk claims.
    - Evidence: `subrepos/process-mappings/profiles/adverse-incidents/AUTHORITY_VARIATION_MATRIX.json`.
    - **Acceptance:** no national framework is mislabeled as legislation and no local policy is generalized nationally.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Source and Authority Spine' (Protocol in workflow.md)

## Phase 2 - Process Mapping and Triangulation

> CHECKPOINT (2026-07-15): Phase 2 now contains agent-proposed process
> candidates, a deterministic field-driven source triangulation resolver, and
> a generated result packet. The resolver emits one disposition per mapping,
> fails closed for blocked, conflicting, undated, underspecified, and
> secondary-only evidence, and never certifies an obligation. Review found no
> actionable defects; human certification and synthetic fixture work remain
> deferred to Phase 3.

- [x] Task: Draft process-profile candidates
    - [x] Store candidate mappings under `subrepos/process-mappings/profiles/adverse-incidents/candidates/`.
    - [x] Model detection through closure with stable IDs and explicit human tasks.
    - [x] Model open communication as a continuing relational process, not a one-time notification flag.
    - [x] Link reporting, complaints, review, disclosure, and improvement as related but distinct processes.
    - **Acceptance:** all mappings are `agent-proposed` until source and human review gates pass.
    - Evidence: `subrepos/process-mappings/profiles/adverse-incidents/candidates/CANDIDATE_MAPPINGS.json` and `SOURCE_ASSERTIONS.json`.
- [x] Task: Implement deterministic source triangulation
    - [x] Require controlling primary-source support for normative obligation labels.
    - [x] Resolve national/regional overlays by jurisdiction, authority, effective date, and applicability.
    - [x] Emit exception reasons for blocked source, conflict, missing date, underspecified local procedure, and secondary-only evidence.
    - **Acceptance:** every mapping receives a proposed disposition or explicit exception without case-name-coded rules.
    - Evidence: `tools/adverse_incident_triangulation.py`.
- [x] Task: Write mapping and resolver tests
    - [x] Cover harm, near miss, delayed recognition, disputed facts, parallel complaint, and blocked-source cases.
    - [x] Verify agent-only assertions cannot become certified obligations.
    - [x] Verify jurisdiction and effective-date leakage fails.
    - **Acceptance:** tests fail before implementation and pass after deterministic resolver work.
    - Evidence: `contracts/tools/tests/test_adverse_incident_triangulation.py` and `results/triangulated-candidates.json`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Process Mapping and Triangulation' (Protocol in workflow.md)
    - Review: spec/plan/workflow/diff reviewed; no actionable defects found.
    - Validation: `FOI_PROGRAMME_REPO_ROOT=/tmp/rac-process-consumption make check` passed.

## Phase 3 - Synthetic Demonstrator and Review

- [x] Task: Build synthetic candidate fixture corpus
    - [x] Include culturally responsive participation and support options without asserting substantive adequacy automatically.
    - [x] Include expected parallel pathways and explicit unresolved questions.
    - [x] Run process-profile validation and trace generation.
    - **Acceptance:** no fixture contains real or plausibly re-identifiable event data.
    - Evidence: `candidates/process-profiles/`, `tools/generate_adverse_incident_fixtures.py`, and `contracts/tools/tests/test_adverse_incident_fixtures.py`.
- [x] Task: [HUMAN] Certify contested assertions and interpretation boundaries
    - [x] Present resolver exceptions, controlling-source assertions, and proposed process differences only.
    - [x] Record approval, rejection, limits, or further-source requirements.
    - **Acceptance:** human review is focused and every promoted assertion has an auditable decision.
    - Prepared artifacts: `subrepos/process-mappings/profiles/adverse-incidents/HUMAN_REVIEW_PACKET.md` and `HUMAN_REVIEW_DECISIONS.template.json`.
    - **HUMAN GATE COMPLETE:** all six queued decisions are recorded; local escalation remains explicitly unresolved and no local obligation is promoted.
    - Human decisions recorded in `HUMAN_REVIEW_DECISIONS.json`: four limited approvals, one explicit rejection, and one approved-unresolved boundary.
    - Process improvement recorded: source discovery is the first human-controlled step for every pathway; see `SOURCE_DISCOVERY_PROTOCOL.md`.
    - Process architecture recorded: all decisions sit within the project-level linked-process model in `PROCESS_PROJECT_MODEL.md`.
- [x] Task: Publish comparative findings and limitations
    - [x] Distinguish source fact, interpretation, executable behavior, variation, and unresolved exception.
    - [x] Document portability implications for the process profile and Camunda study.
    - **Acceptance:** findings make no organisational-compliance, legal-advice, or clinical-safety claim.
    - Evidence: `subrepos/process-mappings/profiles/adverse-incidents/COMPARATIVE_FINDINGS.md`.
- [x] Task: Define privacy-preserving post-market safety handoff
    - [x] Specify the minimum public or appropriately de-identified aggregate event, provenance, authority, jurisdiction, permitted-purpose, and review fields.
    - [x] Reject patient-level content, inferred causation, and uncertified downstream action.
    - [x] Add valid and negative examples without making the handoff mandatory for incident workflows.
    - **Acceptance:** the handoff schema and examples validate and strictly exclude patient-level data, causal inference, and uncertified downstream action.
    - Evidence: `safety-handoff/schema.json`, `safety-handoff/examples/`, and `contracts/tools/tests/test_adverse_incident_safety_handoff.py`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Synthetic Demonstrator and Review' (Protocol in workflow.md)
    - Review: spec/plan/workflow/diff reviewed; one safety-handoff consumption gate and one stale source-blocker statement fixed.
    - Validation: `FOI_PROGRAMME_REPO_ROOT=/tmp/rac-process-consumption make check` passed.

> CHECKPOINT (2026-07-15): Phase 3 is complete. Human review decisions are
> auditable, the six synthetic pathways remain non-identifying, comparative
> findings preserve source and interpretation boundaries, and the optional
> safety handoff fails closed before human review. Remaining source exceptions
> are explicit: two blocked NSW policy downloads, the Australian framework's
> unstated effective date, and unresolved local escalation ownership. No legal,
> clinical, organisational, or compliance claim has been automated.
