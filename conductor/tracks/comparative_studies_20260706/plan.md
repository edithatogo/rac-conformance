# Implementation Plan

Depends on: `adoption_closure_20260706` Phase 1. DBN or maintainer feedback should influence candidate scoring when available.

## Phase 1 - Candidate Matrix

- [x] Task: Gather candidate evidence (SHA: 6ece405)
    - [x] Review DBN response/log if available.
    - [x] Review PolicyEngine/PRD public validation direction.
    - [x] Inspect candidate model repos for runnable access and licensing.
    - **Acceptance:** each candidate has source URLs, access notes, and risk notes.
- [x] Task: Score candidates (SHA: 6ece405)
    - [x] Create `studies/NEXT_STUDY_SELECTION.md`.
    - [x] Score candidate studies against the required criteria.
    - [x] Identify primary and reserve recommendations.
    - **Acceptance:** recommendation is evidence-backed and does not duplicate existing work without reason.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Candidate Matrix' (Protocol in workflow.md)

## Phase 2 - Feasibility Smokes

- [x] Task: Run minimal feasibility checks for top candidate (SHA: 6ece405)
    - [x] Verify install/runtime availability.
    - [x] Run one existing example or public smoke command.
    - [x] Record exact versions and blockers.
    - **Acceptance:** feasibility is proven or the candidate is demoted.
- [x] Task: Source and oracle assessment (SHA: 6ece405)
    - [x] Identify primary sources and independent oracles.
    - [x] Draft source-assertion requirements.
    - **Acceptance:** no study proceeds without a feasible oracle strategy.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Feasibility Smokes' (Protocol in workflow.md)

## Phase 3 - New Study Track Draft

- [x] Task: Draft selected study conductor track (SHA: 6ece405)
    - [x] Create draft spec and plan under `studies/next-study-draft/` or directly as a new conductor track after approval.
    - [x] Include human gates for fixture curation and legal/source adjudication.
    - [x] Include CI and publication package phases.
    - **Acceptance:** draft is implementation-ready but not started without approval.
- [x] Task: [HUMAN] Approve next study
    - [x] Present recommendation, feasibility proof, and draft track.
    - [x] Dylan selects proceed, revise, or defer.
    - **Acceptance:** decision is recorded.
- [x] Task: Create approved study implementation track (SHA: 9866b59)
    - [x] If Dylan approves proceeding, create the new Conductor track using the approved draft.
    - [x] Add it to `conductor/tracks.md` in dependency order.
    - [x] Create or update a GitHub sub-issue under the roadmap parent issue.
    - [x] If Dylan defers, record the deferral and do not create a placeholder implementation track.
    - **Acceptance:** approved study has an executable Conductor track and GitHub issue, or deferral is explicit.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - New Study Track Draft' (Protocol in workflow.md)

