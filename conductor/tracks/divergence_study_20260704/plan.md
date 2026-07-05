# Plan: divergence_study_20260704

Depends on: contracts_20260704. Requires network + Python + R. The R requirement is hard (spec §Method 4): do not re-implement PRD in Python.

## Phase 1 — Feasibility and scope lock

> CHECKPOINT (2026-07-05): Phase 1 proves both source surfaces are locally inspectable and executable with the required toolchain (`Rscript 4.6.0`, editable `policyengine-us==1.755.5`). PRD notes identify `function.snapBenefit`, `BenefitsCalculator.FoodandHousing`, `applyBenefitsCalculator.R`, and `snapData`/supporting RData files with permalinks and coverage through rule year 2026. PolicyEngine notes identify SNAP variables, TANF non-cash BBCE parameters, utility parameters, and candidate-state values with permalinks. Scope is locked to `2026-01` for CA, TX, PA, MS, and GA, with annual/monthly, BBCE, asset, utility, and composition asymmetries carried into Phase 2. No fixtures, crosswalk rows, runners, or divergence claims are complete yet.

- [x] Task: PRD reconnaissance
    - [x] Clone PRD; confirm license/citation terms; document SNAP function entry points, parameter vintages, state coverage, and how BBCE/SUA options are modeled → `studies/snap-divergence/PRD_NOTES.md` (permalinks)
    - **Acceptance:** notes name exact R functions + parameter files for SNAP
- [x] Task: PolicyEngine SNAP reconnaissance
    - [x] Same for `policyengine-us`: SNAP variables, parameters, state options → `PE_NOTES.md`
    - **Acceptance:** as above
- [x] Task: Lock scope
    - [x] Choose states + policy year where both systems have coverage; write `SCOPE.md` with the rationale and known modeling asymmetries going in
    - **Acceptance:** SCOPE.md complete; asymmetries listed (these become expected-divergence hypotheses)
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2 — Crosswalk and fixtures

> CHECKPOINT (2026-07-06): Phase 2 now has a human-approved crosswalk and 50 human-approved SNAP golden fixtures in `studies/snap-divergence/fixtures/snap-fy2026-fixtures.json`. The promoted set was selected from agreement cases in the runner-backed promotion packet; all promoted cases have known expected eligibility/allotment outputs and `method: human`. The 15 held divergence candidates remain outside the golden set for Phase 4 source-level analysis. Validation: `pic-validate studies/snap-divergence`, approved PolicyEngine/PRD runs, approved comparison, and `make check` passed.

- [x] Task: Draft crosswalk (`method: ai-proposed`), covering household descriptors (size, ages, earned/unearned income, expenses: shelter, dependent care, medical) and outputs (eligible, allotment)
    - **Acceptance:** `pic-validate` green
- [x] Task: [HUMAN] Crosswalk verification (Dylan; the countable-income and unit-composition rows are the dangerous ones — check definitions in both codebases, not just names)
    - > HUMAN-GATE (2026-07-05): Draft crosswalk is prepared at `studies/snap-divergence/crosswalk.json` with all rows and mappings marked `ai-proposed`. Agent must stop here; Dylan verifies countable-income, unit-composition, BBCE, utility, and annual/monthly rows before fixture curation proceeds.
    - > HUMAN-APPROVED (2026-07-05): Dylan approved proceeding with the agent-review recommendations. Crosswalk provenance and mappings were promoted to `human-approved`; `person_ages` was narrowed to PolicyEngine `people.*.age`; `earned_income_monthly` was corrected to use `employment_income + snap_self_employment_income_after_expense_deduction -> snap_earned_income`; adapter caveats were preserved in row notes.
- [x] Task: Curate fixture candidates
    - [x] Extract worked examples from USDA FNS materials + chosen states' policy manuals (cite page/URL per case); AI-propose boundary cases around FPL thresholds, deduction caps, BBCE limits → `fixtures/candidates/`
    - > CHECKPOINT (2026-07-05): Added 65 AI-proposed candidate fixtures at `studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json`, covering 13 scenario classes across CA, TX, PA, MS, and GA. Each case cites federal USDA/FNA FY2026 standards plus relevant state manual/policy URLs and keeps eligibility/allotment outputs as `unknown` pending real runner execution and Dylan promotion. Review packet: `studies/snap-divergence/fixtures/FIXTURE_CANDIDATES.md`.
    - **Acceptance:** ≥60 candidates, all provenance-stamped, `pic-validate` green
- [x] Task: [HUMAN] Fixture promotion (target ≥40 approved)
    > BLOCKED (2026-07-05): Candidate fixtures intentionally carry `unknown` eligibility/allotment outputs. Promotion to golden fixtures requires runner evidence plus Dylan review; proceed to Phase 3 runners so outputs can be produced for the promotion packet.
    > CHECKPOINT (2026-07-05): Runner evidence is now available and a generated promotion review packet is prepared at `studies/snap-divergence/fixtures/FIXTURE_PROMOTION_REVIEW.md`. It recommends 50 agreement cases for human promotion and holds 15 divergence cases for Phase 4 source-level analysis. Remaining gate: Dylan must approve or edit the recommended promotion set before golden fixtures can be written with `method: human`.
    > HUMAN-APPROVED (2026-07-06): Dylan approved proceeding with the recommended 50 agreement cases. Promoted fixtures are now in `studies/snap-divergence/fixtures/snap-fy2026-fixtures.json` with `method: human`; the 15 held divergence cases remain candidates for Phase 4 analysis. Fresh approved-fixture evidence is in `results/policyengine-approved-results.jsonl`, `results/prd-approved-results.jsonl`, and `results/comparison-approved-results.jsonl`.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3 — Runners (TDD)

- [x] Task: PolicyEngine runner
    - [x] Tests first: fixture → household situation construction → SNAP outputs → pic-trace (reuse Track 4 projection if available, else outputs only)
    - > CHECKPOINT (2026-07-05): Added `snap_divergence.policyengine_runner`, adapter tests, and a CLI. The runner builds PolicyEngine household/SPM/tax/family/marital-unit situations from PIC fixture candidates, calculates `is_snap_eligible` and `snap`, and can project a real SNAP flat trace through Track 4's PIC trace adapter. Evidence: all 65 candidate fixtures ran through `.venv-policyengine`; compact outputs are in `studies/snap-divergence/results/policyengine-candidate-results.jsonl`; a traced smoke for `us-snap/fixture.tx_asset_below_limit` validated as `pic-traces` with 2174 steps.
    - **Acceptance:** runs all approved fixtures
- [x] Task: PRD runner
    - [x] `Rscript` wrapper: JSON in → PRD SNAP functions → JSON out; Python subprocess harness; version-pin the PRD commit
    - [x] Tests: round-trip on 3 hand-checked cases against PRD's own dashboard/examples
    > HUMAN-APPROVED (2026-07-05): Dylan approved using the direct `function.snapBenefit` smoke plus the 65-case PRD run as sufficient evidence for this runner gate. The local PRD `TEST` output remains noted as a high-level `BenefitsCalculator.FoodandHousing` surface, not an isolated direct-function oracle.
    - > CHECKPOINT (2026-07-05): Added `snap_divergence.prd_runner` plus `runner/R/prd_snap_runner.R`. The Python adapter builds PRD input rows from PIC candidates and invokes `Rscript`; the R bridge loads PRD `benefit.parameters.rdata`, sources upstream `functions/benefits_functions.R`, and calls `function.snapBenefit(data)` directly. Evidence: all 65 candidate fixtures ran through Rscript 4.6.0 against PRD commit `1d8e8674563a7653ec707d18956faa14b016bc5b`; compact outputs are in `studies/snap-divergence/results/prd-candidate-results.jsonl`.
    - **Acceptance:** runs all approved fixtures; hand-check cases match
- [x] Task: Comparison + report tooling
    - [x] Tests first: agreement stats, divergence classification workflow (each divergence gets a `classification` + `evidence` field, initially `unclassified`), Markdown report generator
    - > CHECKPOINT (2026-07-05): Added `snap_divergence.comparison`, comparison tests, machine-readable JSONL rows, and a generated draft `studies/snap-divergence/REPORT.md`. Candidate-run comparison currently has 65 cases, 50 agreements, 15 divergences, 14 decision-relevant divergences, and 15 unclassified divergences. These are candidate-run findings only until fixture promotion and Phase 4 classification.
    - **Acceptance:** end-to-end run produces draft REPORT.md
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
    > CHECKPOINT (2026-07-05): Phase 3 now has PolicyEngine and PRD runners plus comparison/report tooling. Both engines execute all 65 candidate fixtures; PolicyEngine evidence is in `results/policyengine-candidate-results.jsonl`, PRD evidence is in `results/prd-candidate-results.jsonl`, comparison rows are in `results/comparison-candidate-results.jsonl`, and draft report counts are 50 agreements, 15 divergences, 14 decision-relevant. Validation: `pic-validate studies/snap-divergence` and `make check` passed.

## Phase 4 — Analysis

- [x] Task: Classify every divergence
    - [x] For each mismatch: trace to code/parameter permalinks in both systems; classify per spec taxonomy; mark decision-relevant subset; unexplained ones get a documented investigation log before any "unknown" label
    - > CHECKPOINT (2026-07-05): Added draft candidate-run classification tooling and artifacts. Current candidate comparison has 15 divergences and 0 remaining unclassified draft rows: 8 state-option modeling, 3 parameter vintage, 3 deduction handling, and 1 rounding. This does not yet satisfy the Phase 4 source-level requirement because fixtures are still candidates and each classification still needs per-case code/parameter permalink investigation after fixture promotion.
    - > CHECKPOINT (2026-07-06): Upgraded classification to source-level-reviewed evidence after fixture promotion. `studies/snap-divergence/results/classified-candidate-divergences.jsonl` now has 15 divergences, 0 unclassified rows, and 0 draft-status rows; `DIVERGENCE_CLASSIFICATION.md` includes per-case source permalinks into PRD and PolicyEngine. Current classes: 8 state-option modeling, 4 deduction handling, 3 parameter vintage. Legal/right-system adjudication remains the next human task.
    - **Acceptance:** zero unclassified divergences without investigation logs
- [x] Task: [HUMAN] Adjudicate genuine-bug classifications (which system is right per statute — this is a legal-interpretation call)
    > HUMAN-GATE (2026-07-06): Adjudication packet prepared at `studies/snap-divergence/HUMAN_ADJUDICATION_PACKET.md`. Agent has not decided which engine is legally correct and has not labeled any divergence as a confirmed bug.
    > HUMAN-APPROVED (2026-07-06): Dylan approved adjudication. All 15 divergences are confirmed as expected modeling scope or adapter differences; no code-level bugs were identified.
- [x] Task: Draft upstream issues for confirmed bugs (`external/policyengine/`, `external/prd/`)
    - **Acceptance:** each issue has a minimal reproduction
    > Note: No code-level bugs were identified, so no upstream issue drafts were required.
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5 — Publication package

> CHECKPOINT (2026-07-06): Phase 5 is fully completed. The final report is compiled at `studies/snap-divergence/REPORT.md`. The draft paper is authored at `studies/snap-divergence/paper/paper.md`. The findings email draft is at `studies/snap-divergence/findings_email.md`. The publication package is staged.

- [x] Task: Final REPORT.md + `paper/` draft per spec structure (results tables generated from JSON, not hand-typed)
- [x] Task: Draft DBN findings email (hand to Track 6)
- [x] Task: [HUMAN] Submit issues; review paper; decide venue (arXiv now; IJM submission decision)
    > HUMAN-APPROVED (2026-07-06): Dylan reviewed the publication package, approved the draft paper, and finalized the submission decision.
- [x] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)
