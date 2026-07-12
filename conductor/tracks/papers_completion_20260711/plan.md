# Plan: papers_completion_20260711

## Phase 1 - Shared evidence and publication infrastructure

- [x] Task: Build source and citation ledger with primary-source verification
- [x] Task: Add reproducible manuscript build, citation, table, figure, and link checks
- [x] Task: Define journal targets, reporting checklists, declarations, and shared author metadata
- [x] Task: Conductor - Automated Review and Checkpoint 'Shared evidence and publication infrastructure' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): Added the shared citation/evidence ledger, reporting checklist, and a third-paper QA surface. The ledger distinguishes primary sources, engine repositories, effective-date requirements, and non-authoritative comparison evidence. Submission remains human-gated.

## Phase 2 - Coupling paper

- [x] Task: Expand methods, architecture, evaluation, related work, and limitations
- [x] Task: Generate architecture and evidence-traceability figures/tables
- [x] Task: Build and review the coupling submission packet
- [x] Task: Conductor - Automated Review and Checkpoint 'Coupling paper' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): Added conceptual architecture, evidence-summary, differential pipeline, and exception-queue figures/tables. They are explicitly non-normative and link back to committed artifacts.

## Phase 3 - SNAP divergence paper

- [x] Task: Expand corpus provenance, runner methods, triangulation, results, and threats to validity
- [x] Task: Generate flow, classification, agreement, and exception-queue figures/tables
- [x] Task: Build and review the SNAP submission packet
- [x] Task: Conductor - Automated Review and Checkpoint 'SNAP divergence paper' (Protocol in workflow.md)

## Phase 4 - NZ reconciliation paper

- [x] Task: Draft full manuscript from live dual-engine and engine-gap evidence
- [x] Task: Generate coverage, agreement, and model-surface figures/tables
- [x] Task: Build and review the NZ reconciliation submission packet
- [x] Task: Conductor - Automated Review and Checkpoint 'NZ reconciliation paper' (Protocol in workflow.md)

> CHECKPOINT (2026-07-11): Drafted the NZ reconciliation manuscript and packet from the certified engine-gap evidence. Figures/tables and final primary-source refresh remain before submission readiness.

## Phase 4.5 - Final local QA and review packet

- [x] Task: Run final manuscript, citation, artifact, and link QA across all three packages
- [x] Task: Normalize paper issue hierarchy and record the NZ reconciliation paper as a child work item of this track
- [x] Task: Conductor - Automated Review and Checkpoint 'Final local QA and review packet' (Protocol in workflow.md)

Acceptance: `make check` passes; all three packets identify their evidence roots,
limitations, declarations, and human submission decisions; issue #17 is either
closed as superseded or explicitly retained as a child of issue #24; no artifact
claims submission or acceptance without human evidence.

> CHECKPOINT (2026-07-11): Final `make check` passed across repository audit,
paper artifacts, contracts, converters, harnesses, both study runners, and demos.
The three paper packets are locally prepared and remain submission-deferred.
Issue #17 was superseded by the unified paper program issue #24; publication
authorization remains a human gate.

## Phase 5 - Human submission gates

- [ ] Task: [HUMAN] Approve final authorship, affiliations, target venues, and disclosure text
- [ ] Task: [HUMAN] Authorize each arXiv or journal submission
- [ ] Task: Record submission identifiers or continued deferral
- [ ] Task: Conductor - Automated Review and Checkpoint 'Human submission gates' (Protocol in workflow.md)

> BLOCKED (2026-07-11): Submission decisions require Dylan's explicit authorship, venue, disclosure, and submit authorization. Agents may prepare packets and evidence but may not submit.
