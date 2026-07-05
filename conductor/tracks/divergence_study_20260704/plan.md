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

- [x] Task: Draft crosswalk (`method: ai-proposed`), covering household descriptors (size, ages, earned/unearned income, expenses: shelter, dependent care, medical) and outputs (eligible, allotment)
    - **Acceptance:** `pic-validate` green
- [x] Task: [HUMAN] Crosswalk verification (Dylan; the countable-income and unit-composition rows are the dangerous ones — check definitions in both codebases, not just names)
    - > HUMAN-GATE (2026-07-05): Draft crosswalk is prepared at `studies/snap-divergence/crosswalk.json` with all rows and mappings marked `ai-proposed`. Agent must stop here; Dylan verifies countable-income, unit-composition, BBCE, utility, and annual/monthly rows before fixture curation proceeds.
    - > HUMAN-APPROVED (2026-07-05): Dylan approved proceeding with the agent-review recommendations. Crosswalk provenance and mappings were promoted to `human-approved`; `person_ages` was narrowed to PolicyEngine `people.*.age`; `earned_income_monthly` was corrected to use `employment_income + snap_self_employment_income_after_expense_deduction -> snap_earned_income`; adapter caveats were preserved in row notes.
- [x] Task: Curate fixture candidates
    - [x] Extract worked examples from USDA FNS materials + chosen states' policy manuals (cite page/URL per case); AI-propose boundary cases around FPL thresholds, deduction caps, BBCE limits → `fixtures/candidates/`
    - > CHECKPOINT (2026-07-05): Added 65 AI-proposed candidate fixtures at `studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json`, covering 13 scenario classes across CA, TX, PA, MS, and GA. Each case cites federal USDA/FNA FY2026 standards plus relevant state manual/policy URLs and keeps eligibility/allotment outputs as `unknown` pending real runner execution and Dylan promotion. Review packet: `studies/snap-divergence/fixtures/FIXTURE_CANDIDATES.md`.
    - **Acceptance:** ≥60 candidates, all provenance-stamped, `pic-validate` green
- [ ] Task: [HUMAN] Fixture promotion (target ≥40 approved)
    > BLOCKED (2026-07-05): Candidate fixtures intentionally carry `unknown` eligibility/allotment outputs. Promotion to golden fixtures requires runner evidence plus Dylan review; proceed to Phase 3 runners so outputs can be produced for the promotion packet.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3 — Runners (TDD)

- [x] Task: PolicyEngine runner
    - [x] Tests first: fixture → household situation construction → SNAP outputs → pic-trace (reuse Track 4 projection if available, else outputs only)
    - > CHECKPOINT (2026-07-05): Added `snap_divergence.policyengine_runner`, adapter tests, and a CLI. The runner builds PolicyEngine household/SPM/tax/family/marital-unit situations from PIC fixture candidates, calculates `is_snap_eligible` and `snap`, and can project a real SNAP flat trace through Track 4's PIC trace adapter. Evidence: all 65 candidate fixtures ran through `.venv-policyengine`; compact outputs are in `studies/snap-divergence/results/policyengine-candidate-results.jsonl`; a traced smoke for `us-snap/fixture.tx_asset_below_limit` validated as `pic-traces` with 2174 steps.
    - **Acceptance:** runs all approved fixtures
- [ ] Task: PRD runner
    - [ ] `Rscript` wrapper: JSON in → PRD SNAP functions → JSON out; Python subprocess harness; version-pin the PRD commit
    - [ ] Tests: round-trip on 3 hand-checked cases against PRD's own dashboard/examples
    - **Acceptance:** runs all approved fixtures; hand-check cases match
- [ ] Task: Comparison + report tooling
    - [ ] Tests first: agreement stats, divergence classification workflow (each divergence gets a `classification` + `evidence` field, initially `unclassified`), Markdown report generator
    - **Acceptance:** end-to-end run produces draft REPORT.md
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4 — Analysis

- [ ] Task: Classify every divergence
    - [ ] For each mismatch: trace to code/parameter permalinks in both systems; classify per spec taxonomy; mark decision-relevant subset; unexplained ones get a documented investigation log before any "unknown" label
    - **Acceptance:** zero unclassified divergences without investigation logs
- [ ] Task: [HUMAN] Adjudicate genuine-bug classifications (which system is right per statute — this is a legal-interpretation call)
- [ ] Task: Draft upstream issues for confirmed bugs (`external/policyengine/`, `external/prd/`)
    - **Acceptance:** each issue has a minimal reproduction
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5 — Publication package

- [ ] Task: Final REPORT.md + `paper/` draft per spec structure (results tables generated from JSON, not hand-typed)
- [ ] Task: Draft DBN findings email (hand to Track 6)
- [ ] Task: [HUMAN] Submit issues; review paper; decide venue (arXiv now; IJM submission decision)
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)
