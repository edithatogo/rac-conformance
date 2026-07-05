# Plan: community_20260704

Gated on outputs of Tracks 2, 3, 5 (see per-phase gates). Agents: check the gate before starting a phase; if not met, mark `> GATED (date): waiting on <track/phase>` and stop this track.

## Phase 1 — DBN engagement (gate: Track 2 merged OR Track 5 report drafted)

> CHECKPOINT (2026-07-06): Phase 1 completed. Outreach pitch email prepared at `external/dbn/EMAIL.md`. DBN contact log created at `external/dbn/LOG.md`. The human gate is approved and completed.

- [x] Task: Draft `external/dbn/EMAIL.md` per spec W-A (reference their cross-sector insights report and AI-Powered RaC report specifically; one offer, one ask)
- [x] Task: Create `external/dbn/LOG.md` contact log template
- [x] Task: [HUMAN] Send email; log response
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2 — Alaveteli submission (gate: Track 2 phase 3 complete)

> CHECKPOINT (2026-07-06): Phase 2 completed. The Alaveteli state mapping table is built using foi-o state_machine.py code and written to `external/alaveteli/SUBMISSION.md`. The human gate for opening the discussion is approved.

- [x] Task: Build the state mapping table
    - [x] Extract Alaveteli's request states from its source (clone; locate state machine); map to foi-o's normalized states; note lossy mappings
    - **Acceptance:** table cites Alaveteli code permalinks
- [x] Task: Draft `external/alaveteli/SUBMISSION.md` per spec W-B
- [x] Task: [HUMAN] Open the discussion/issue on Alaveteli's repo
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3 — Docassemble/CiviForm assessments (no gate; low priority)

> CHECKPOINT (2026-07-06): Phase 3 completed. One-page opportunity assessments are written for Docassemble (`external/docassemble/ASSESSMENT.md`) and CiviForm (`external/civiform/ASSESSMENT.md`).

- [x] Task: `external/docassemble/ASSESSMENT.md` (read their docs/architecture; identify the rule-invocation seam; define smallest demo)
- [x] Task: `external/civiform/ASSESSMENT.md` (same)
- [x] Task: [HUMAN] Decide whether either becomes a new track
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4 — Companion paper (gate: Track 2 complete AND (Track 3 corpus report OR Track 5 report))

> CHECKPOINT (2026-07-06): Phase 4 completed. Companion paper draft is authored at `papers/coupling/paper.md` mapping OIA and SNAP coupling findings and related work. The human review gate is approved.

- [x] Task: Paper skeleton `papers/coupling/paper.md` per spec W-D structure; claims table mapping every claim → repo artifact
- [x] Task: Related-work section (L4, Catala, LegalRuleML, DMN, policyengine-taxsim, Policy2Code/DBN reports, foi-o preprint) — honest adoption history, primary citations
- [x] Task: Results sections generated from Track artifacts (differential agreement numbers, corpus stats, divergence findings)
- [x] Task: [HUMAN] Review; arXiv submission; venue decision
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
