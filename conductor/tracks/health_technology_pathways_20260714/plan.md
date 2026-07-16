# Implementation Plan

GitHub issue: [#42](https://github.com/edithatogo/rac-conformance/issues/42). Depends on [#40](https://github.com/edithatogo/rac-conformance/issues/40) Phase 2.

Implementation home: `subrepos/process-mappings/profiles/health-technology/`
during the repository incubation governed by
[#50](https://github.com/edithatogo/rac-conformance/issues/50).

## Phase 1 - Authority and Source Architecture

- [x] Task: Build regulator, HTA, payer, and service-funding authority matrix
    - [x] Cover Medsafe/Pharmac, TGA/PBAC-PBS/MSAC-MBS, MHRA/NICE, and FDA/explicitly payer-specific US follow-on.
    - [x] Record statutory or policy function, decision owner, advice owner, applicant, output, review route, and post-market owner.
    - [x] Mark non-equivalent and absent functions explicitly.
    - **Acceptance:** automated checks reject FDA-as-payer, MBS-as-medicine-regulator, and other false-equivalence assertions.
    - **Evidence:** `subrepos/process-mappings/profiles/health-technology/AUTHORITY_MATRIX.json`, `LIFECYCLE_MODEL.md`, `sources/SOURCE_MANIFEST.json`, and `contracts/tools/tests/test_health_technology_profile.py`; 83 contract tests and full `make check` pass.
- [x] Task: Build versioned primary-source manifests
    - [x] Store source ledgers under `subrepos/process-mappings/profiles/health-technology/sources/`.
    - [x] Pin current official process manuals, legislation or regulations where needed, application guidance, and public decision-record formats.
    - [x] Record effective date, retrieval time, version, supersession, rights, and digest.
    - [x] Record inaccessible confidential stages as unavailable rather than filling gaps.
    - **Acceptance:** every modeled stage has a source owner and authority classification.
    - **Evidence:** `subrepos/process-mappings/profiles/health-technology/sources/SOURCE_MANIFEST.json` records 13 official source references, retrieval time, digests, authority classes, unresolved effective/supersession fields, rights, and unavailable confidential evidence; manifest regression tests pass.
- [x] Task: Define common lifecycle and variation model
    - [x] Define neutral concepts for authorisation, HTA, recommendation, funding decision, negotiation, listing, restriction, exception, implementation, and monitoring.
    - [x] Support parallel, iterative, terminated, resubmitted, and conditionally linked pathways.
    - [x] Document representational loss per jurisdiction.
    - **Acceptance:** common terms do not erase institutional decision ownership.
    - **Evidence:** `subrepos/process-mappings/profiles/health-technology/LIFECYCLE_MODEL.md` defines neutral stages, variation rules, unavailable evidence, representational loss, and authority boundaries; lifecycle regression tests pass.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Authority and Source Architecture' (Protocol in workflow.md)
    - **Review:** Automated review found and fixed two regression-test brittleness issues; the final matrix, source manifest, lifecycle model, and tests preserve authority boundaries and unavailable evidence without asserting clinical or funding outcomes.
    - **Verification:** `FOI_PROGRAMME_REPO_ROOT=/tmp/rac-process-consumption make check` passed with 84 contract tests and 83.46% contract coverage.

> CHECKPOINT (2026-07-15): Phase 1 is complete. The candidate authority matrix covers Medsafe/Pharmac, TGA/PBAC/PBS/MSAC/MBS, MHRA/NICE, FDA, CMS, and explicitly unspecified commercial payers. The source ledger pins 13 official references and records unavailable confidential evidence. The lifecycle model supports branching and iteration without treating unlike authorities as equivalent. No comparison case, jurisdiction profile, or source assertion has been human-certified.

## Phase 2 - Comparison Case Selection

- [x] Task: Produce comparison-case candidates
    - [x] Identify publicly documented medicines/indications with aligned regulator and funding records in at least two jurisdictions.
    - [x] Score source completeness, temporal comparability, indication alignment, public evidence, rights, and implementation value.
    - [x] Include a no-selection outcome if no candidate supports defensible comparison.
    - **Acceptance:** each candidate has a source manifest and stated comparability limitations.
    - **Evidence:** `subrepos/process-mappings/profiles/health-technology/candidates/COMPARISON_CASE_CANDIDATES.json` ranks three pembrolizumab candidates; `SOURCE_SPINE.json` records official discovery sources, effective dates, gaps, and unavailable evidence. No candidate is selected or promoted.
- [ ] Task: [HUMAN] Approve one comparison case and jurisdiction pair
    - [ ] Present ranked candidates, source gaps, sensitivity, and expected process coverage.
    - [ ] Dylan selects, defers, or rejects the case; no fixture promotion occurs here.
    - **Acceptance:** selection and reasons are recorded without implying clinical endorsement.
    - **Packet:** `CASE_SELECTION_PACKET.md` presents the ranked candidates, recommendation, limitations, and explicit defer/no-selection outcomes.
- [ ] Task: Define independent-oracle and adjudication protocol
    - [x] Separate official process facts, public decision facts, project mappings, and unavailable deliberative evidence.
    - [x] Define deterministic triangulation and focused human exception review.
    - **Acceptance:** agent-authored mappings cannot self-certify.
    - **Evidence:** `ADJUDICATION_PROTOCOL.md` and `ADJUDICATION_RULES.json` define evidence classes, resolution precedence, stable exception reasons, proposed dispositions, and the independent-oracle boundary. Regression coverage is in `contracts/tools/tests/test_health_technology_profile.py`; no candidate is selected or promoted.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Comparison Case Selection' (Protocol in workflow.md)

## Phase 3 - Executable Comparative Profiles

- [ ] Task: Write jurisdiction-profile and trace tests
    - [ ] Cover standard, additional-information, parallel review, negative/reconsideration, positive-not-yet-listed, restriction, exception, and post-market paths as sources permit.
    - [ ] Add negative tests for jurisdiction, authority, indication, date, confidentiality, and causal-claim leakage.
    - **Acceptance:** tests fail before profile implementation.
- [ ] Task: Implement two regulator-to-funder jurisdiction profiles
    - [ ] Store candidate mappings and scenarios under `subrepos/process-mappings/profiles/health-technology/candidates/` until certification.
    - [ ] Use the shared process profile with jurisdiction-owned extensions only where consumed.
    - [ ] Generate deterministic normalized traces and a documented difference report.
    - [ ] Keep all proposed outcomes in candidates pending certification.
    - **Acceptance:** both profiles run without shared code encoding one jurisdiction's substantive decision as the other's oracle.
- [ ] Task: Implement optional Australian codependent-technology branch
    - [ ] Model PBAC/PBS and MSAC/MBS coordination only if the approved case requires it.
    - [ ] Otherwise record `not_applicable` with evidence and do not create speculative mappings.
    - **Acceptance:** MBS work has a concrete consumer and case or remains absent.
- [ ] Task: Implement optional post-market safety handoff consumer
    - [ ] Accept only the validated public or appropriately de-identified aggregate signal contract from the adverse-incident track.
    - [ ] Route to monitoring, evidence review, or human reassessment only where a controlling official source supports that route.
    - [ ] Preserve uncertainty and prohibit causal, regulatory, funding, restriction, and patient-access outcome inference.
    - **Acceptance:** negative tests reject patient-level data, purpose mismatch, wrong jurisdiction, stale authority, and deterministic outcome inference.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Executable Comparative Profiles' (Protocol in workflow.md)

## Phase 4 - Certification and Findings

- [ ] Task: Run deterministic triangulation and generate exception packet
    - [ ] Resolve assertions by authority, jurisdiction, indication, effective date, and source status.
    - [ ] Emit explicit exceptions for conflicts, missing dates, unavailable confidential evidence, and non-comparable decisions.
    - **Acceptance:** every held assertion has a proposed disposition or explicit exception.
- [ ] Task: [HUMAN] Certify controlling assertions and comparison limits
    - [ ] Review only contested controlling assertions, fixture interpretations, and exception cases.
    - [ ] Record approvals and rejected or unresolved claims.
    - **Acceptance:** promoted fixtures have independent certification and no inferred confidential facts.
- [ ] Task: Publish comparative report and reusable source pack
    - [ ] Lead with observed pathway differences, then method and caveats.
    - [ ] Separate process portability findings from policy or outcome judgements.
    - **Acceptance:** report is reproducible and makes no clinical or funding recommendation.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Certification and Findings' (Protocol in workflow.md)
