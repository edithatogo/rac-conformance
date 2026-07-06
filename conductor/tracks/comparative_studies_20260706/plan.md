# Implementation Plan

Depends on: `adoption_closure_20260706` Phase 1. DBN or maintainer feedback should influence candidate scoring when available.

## Phase 1 - Candidate Matrix

- [ ] Task: Gather candidate evidence
    - [ ] Review DBN response/log if available.
    - [ ] Review PolicyEngine/PRD public validation direction.
    - [ ] Inspect candidate model repos for runnable access and licensing.
    - **Acceptance:** each candidate has source URLs, access notes, and risk notes.
- [ ] Task: Score candidates
    - [ ] Create `studies/NEXT_STUDY_SELECTION.md`.
    - [ ] Score candidate studies against the required criteria.
    - [ ] Identify primary and reserve recommendations.
    - **Acceptance:** recommendation is evidence-backed and does not duplicate existing work without reason.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Candidate Matrix' (Protocol in workflow.md)

## Phase 2 - Feasibility Smokes

- [ ] Task: Run minimal feasibility checks for top candidate
    - [ ] Verify install/runtime availability.
    - [ ] Run one existing example or public smoke command.
    - [ ] Record exact versions and blockers.
    - **Acceptance:** feasibility is proven or the candidate is demoted.
- [ ] Task: Source and oracle assessment
    - [ ] Identify primary sources and independent oracles.
    - [ ] Draft source-assertion requirements.
    - **Acceptance:** no study proceeds without a feasible oracle strategy.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Feasibility Smokes' (Protocol in workflow.md)

## Phase 3 - New Study Track Draft

- [ ] Task: Draft selected study conductor track
    - [ ] Create draft spec and plan under `studies/next-study-draft/` or directly as a new conductor track after approval.
    - [ ] Include human gates for fixture curation and legal/source adjudication.
    - [ ] Include CI and publication package phases.
    - **Acceptance:** draft is implementation-ready but not started without approval.
- [ ] Task: [HUMAN] Approve next study
    - [ ] Present recommendation, feasibility proof, and draft track.
    - [ ] Dylan selects proceed, revise, or defer.
    - **Acceptance:** decision is recorded.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - New Study Track Draft' (Protocol in workflow.md)
