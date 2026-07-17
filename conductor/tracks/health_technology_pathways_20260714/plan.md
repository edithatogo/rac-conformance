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
    - Evidence: `subrepos/process-mappings/profiles/health-technology/AUTHORITY_MATRIX.json` and `tools/tests/test_health_technology_matrix.py`.
- [x] Task: Build versioned primary-source manifests
    - [x] Store source ledgers under `subrepos/process-mappings/profiles/health-technology/sources/`.
    - [x] Pin current official process manuals, legislation or regulations where needed, application guidance, and public decision-record formats.
    - [x] Record effective date, retrieval time, version, supersession, rights, and digest.
    - [x] Record inaccessible confidential stages as unavailable rather than filling gaps.
    - **Acceptance:** every modeled stage has a source owner and authority classification.
    - Evidence: `subrepos/process-mappings/profiles/health-technology/sources/SOURCE_MANIFEST.json`. Blocked and UNVERIFIED sources are explicit and cannot control mappings.
- [x] Task: Define common lifecycle and variation model
    - [x] Define neutral concepts for authorisation, HTA, recommendation, funding decision, negotiation, listing, restriction, exception, implementation, and monitoring.
    - [x] Support parallel, iterative, terminated, resubmitted, and conditionally linked pathways.
    - [x] Document representational loss per jurisdiction.
    - **Acceptance:** common terms do not erase institutional decision ownership.
    - Evidence: `subrepos/process-mappings/profiles/health-technology/LIFECYCLE_MODEL.md`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Authority and Source Architecture' (Protocol in workflow.md)

> CHECKPOINT (2026-07-16): Authority roles, non-equivalence rules, source states,
> and neutral lifecycle vocabulary are implemented and covered by deterministic
> tests. Direct source capture, effective dates, and digests remain required
> before any candidate mapping can be controlling or promoted.
> REVIEW (2026-07-16): Phase diff reviewed; `make check` passed, including the
> health-technology validator. No high-confidence correctness findings remain.
> SOURCE REFRESH (2026-07-17): Direct HTTPS captures verified the selected
> Medsafe, Pharmac, MHRA, and NICE process sources. `candidates/SOURCE_SPINE.json`
> now records retrieval digests, explicit missing-effective-date gaps, and the
> boundary that direct capture does not certify authority or comparability.

## Phase 2 - Comparison Case Selection

- [x] Task: Produce comparison-case candidates
    - [x] Identify publicly documented medicines/indications with aligned regulator and funding records in at least two jurisdictions.
    - [x] Score source completeness, temporal comparability, indication alignment, public evidence, rights, and implementation value.
    - [x] Include a no-selection outcome if no candidate supports defensible comparison.
    - **Acceptance:** each candidate has a source manifest and stated comparability limitations.
    - Evidence: `candidates/COMPARISON_CASE_CANDIDATES.json` and `candidates/SOURCE_SPINE.json`; the selected candidate remains unpromoted and source-verification-gated.
- [x] Task: [HUMAN] Approve one comparison case and jurisdiction pair
    - [x] Present ranked candidates, source gaps, sensitivity, and expected process coverage.
    - [x] Dylan selects, defers, or rejects the case; no fixture promotion occurs here.
    - **Acceptance:** selection and reasons are recorded without implying clinical endorsement.
    > HUMAN DECISION (2026-07-17): Dylan approved
    > `pembrolizumab-adjuvant-stage-iii-melanoma` for NZ Medsafe/Pharmac versus
    > UK MHRA/NICE. Approval authorizes source verification and candidate-profile
    > implementation only; no fixture promotion or clinical/funding conclusion
    > is authorized.
    > CHECKPOINT (2026-07-17): Reconciled `comparison-candidates.json` with the
    > human decision. The machine-readable ledger now records the NZ/UK case as
    > selected for source verification only; no executable profile or fixture is
    > promoted.
- [x] Task: Define independent-oracle and adjudication protocol
    - [x] Separate official process facts, public decision facts, project mappings, and unavailable deliberative evidence.
    - [x] Define deterministic triangulation and focused analyst exception review.
    - **Acceptance:** agent-authored mappings cannot self-certify.
    - Evidence: `ADJUDICATION_PROTOCOL.md` and `ADJUDICATION_RULES.json`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Comparison Case Selection' (Protocol in workflow.md)
    - **CHECKPOINT (2026-07-17):** The approved NZ/UK case, source-spine limitations, independent-oracle boundary, and candidate-only authorization were reviewed and retained.

## Phase 3 - Executable Comparative Profiles

- [x] Task: Write jurisdiction-profile and trace tests
    - [x] Cover source-supported standard and held-for-review paths for the selected case.
    - [x] Add negative tests for controlling agent assertions and non-none trace equivalence.
    - **Acceptance:** tests fail before profile implementation.
- [x] Task: Implement two regulator-to-funder jurisdiction profiles
    - [x] Store candidate mappings and scenarios under `subrepos/process-mappings/profiles/health-technology/candidates/` until certification.
    - [x] Use the shared process profile with jurisdiction-owned actors and source links.
    - [x] Generate deterministic normalized traces with an explicit `none` equivalence claim.
    - [x] Keep all proposed outcomes in candidates pending certification.
    - **Acceptance:** both profiles run without shared code encoding one jurisdiction's substantive decision as the other's oracle.
    - Evidence: `candidates/nz-pembrolizumab-pathway.json`, `candidates/uk-pembrolizumab-pathway.json`, `contracts/tools/tests/test_health_technology_profiles.py`, and `tools/validate_health_technology_profiles.py`.
- [ ] Task: Implement optional Australian codependent-technology branch
    - [ ] Model PBAC/PBS and MSAC/MBS coordination only if the approved case requires it.
    - [ ] Otherwise record `not_applicable` with evidence and do not create speculative mappings.
    - **Acceptance:** MBS work has a concrete consumer and case or remains absent.
- [ ] Task: Implement optional post-market safety handoff consumer
    - [ ] Accept only the validated public or appropriately de-identified aggregate signal contract from the adverse-incident track.
    - [ ] Route to monitoring, evidence review, or human reassessment only where a controlling official source supports that route.
    - [ ] Preserve uncertainty and prohibit causal, regulatory, funding, restriction, and patient-access outcome inference.
    - **Acceptance:** negative tests reject patient-level data, purpose mismatch, wrong jurisdiction, stale authority, and deterministic outcome inference.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Executable Comparative Profiles' (Protocol in workflow.md)
    - **CHECKPOINT (2026-07-17):** The mandatory NZ/UK candidate-profile slice is implemented and reviewed. The optional Australian codependent-technology branch is deferred because the approved case does not require it. The optional post-market consumer is deferred pending a named consumer and controlling source. Certification, promotion, comparative publication, and Phase 4 remain pending.

> CHECKPOINT (2026-07-17): Candidate NZ and UK profiles validate against
> `pic-process-profile/0.1.0`, preserve jurisdiction-owned actors and source
> assertions, and normalize deterministic candidate traces. All assertions are
> `agent-proposed` and non-controlling; both traces assert no equivalence and
> terminate in source review exceptions. No clinical, funding, access, or
> authorisation outcome is represented.

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
