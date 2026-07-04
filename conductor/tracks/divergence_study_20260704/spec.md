# Spec: SNAP divergence study (policyengine-us vs Atlanta Fed PRD)

## Purpose

The flagship evidence deliverable: do independent rules-as-code encodings of the same law agree? Differentially test SNAP eligibility and allotment across `policyengine-us` (Python) and the Atlanta Fed Policy Rules Database (R; https://github.com/Research-Division/policy-rules-database) on human-curated fixtures. Success = at least one real, previously unknown, maintainer-acknowledged discrepancy, and a publishable report.

Why SNAP: both systems encode it; federal rules with state options (BBCE, SUA) create rich divergence surface; it's the DBN community's home territory; no published systematic comparison exists.

## Research questions

1. Output agreement rate on eligibility (boolean) and allotment (dollar), by state and scenario class.
2. Root causes of divergence, classified: parameter vintage / countable-income definition / deduction handling / state-option modeling (esp. broad-based categorical eligibility) / rounding / missingness defaults / genuine bug.
3. Which divergences are decision-relevant (flip eligibility or change allotment > $10/month)?

## Method

1. **Scope:** SNAP, 3–5 states chosen for option diversity (include at least one BBCE state and one non-BBCE state; propose e.g. GA, CA, TX, PA — finalize in Phase 1 after checking PRD state coverage and vintage). One policy year both systems cover (check PRD's most recent update; PRD's "most recent data" constraint may bind the year choice).
2. **Crosswalk (pic-crosswalk):** map household descriptors and outputs across the two systems. This is where semantic mismatch lives (gross vs net vs countable income; household vs SNAP-unit composition) — every row human-verified before use.
3. **Fixtures (pic-fixtures):** 40–60 golden cases: (a) from USDA FNS worked examples and state policy-manual examples (primary oracle); (b) boundary candidates AI-proposed around thresholds (130%/100% FPL, deduction caps, BBCE limits), human-approved. Provenance per product-guidelines.
4. **Runners:** Python runner calling `policyengine-us`; R runner calling PRD functions via `Rscript` subprocess with JSON in/out (decision: run PRD's own R code — re-implementing it in Python would destroy the independence that makes the comparison meaningful; this is a hard requirement).
5. **Comparison:** `pic-traces`-level where possible (PolicyEngine side via Track 4 projection; PRD side output-only), otherwise output-equivalence with tolerance `$1.00`.
6. **Report:** `studies/snap-divergence/REPORT.md` + per-case JSON: agreement rates, divergence classification, decision-relevant subset, limitations (fixture count, year, state options modeled), and drafted upstream issues for every confirmed bug.

## Deliverables

- `studies/snap-divergence/` — crosswalk, fixtures (+candidates), runners, comparison tooling, report, `paper/` draft (structure: intro/method/results/threats/related work incl. policyengine-taxsim precedent and Policy2Code).
- Drafted upstream issues (`external/policyengine/`, `external/prd/`) for confirmed discrepancies — `[HUMAN]` to submit.
- Findings email draft to rulesascode@georgetown.edu (Track 6 consumes it).

## Acceptance criteria

1. ≥40 human-approved fixtures with full provenance; every AI-proposed case individually approved.
2. Both runners produce results for every fixture (or documented per-case blockers).
3. Every divergence classified with a root cause traced to code/parameter permalinks in both systems; no divergence left as "unknown" without a documented investigation attempt.
4. Report survives the checklist: no claim without a fixture ID; no root cause without permalinks; limitations section present.
5. At least one issue draft per system with confirmed reproduction (if zero discrepancies are found, that is itself the publishable finding — report it, don't manufacture).

## Out of scope

Other programs (TANF/Medicaid — follow-ups); population-weighted analysis; UI/dashboard; policy recommendations.

## Dependencies

Tracks 1 (contracts), 4 phase 1 (trace projection, optional enhancement). Network + R runtime. PRD license check: repo is public GitHub; confirm license permits this use and cite per their CITATION file (Phase 1 task).
