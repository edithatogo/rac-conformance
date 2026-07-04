# Plan: community_20260704

Gated on outputs of Tracks 2, 3, 5 (see per-phase gates). Agents: check the gate before starting a phase; if not met, mark `> GATED (date): waiting on <track/phase>` and stop this track.

## Phase 1 — DBN engagement (gate: Track 2 merged OR Track 5 report drafted)

- [ ] Task: Draft `external/dbn/EMAIL.md` per spec W-A (reference their cross-sector insights report and AI-Powered RaC report specifically; one offer, one ask)
- [ ] Task: Create `external/dbn/LOG.md` contact log template
- [ ] Task: [HUMAN] Send email; log response
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2 — Alaveteli submission (gate: Track 2 phase 3 complete)

- [ ] Task: Build the state mapping table
    - [ ] Extract Alaveteli's request states from its source (clone; locate state machine); map to foi-o's normalized states; note lossy mappings
    - **Acceptance:** table cites Alaveteli code permalinks
- [ ] Task: Draft `external/alaveteli/SUBMISSION.md` per spec W-B
- [ ] Task: [HUMAN] Open the discussion/issue on Alaveteli's repo
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3 — Docassemble/CiviForm assessments (no gate; low priority)

- [ ] Task: `external/docassemble/ASSESSMENT.md` (read their docs/architecture; identify the rule-invocation seam; define smallest demo)
- [ ] Task: `external/civiform/ASSESSMENT.md` (same)
- [ ] Task: [HUMAN] Decide whether either becomes a new track
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4 — Companion paper (gate: Track 2 complete AND (Track 3 corpus report OR Track 5 report))

- [ ] Task: Paper skeleton `papers/coupling/paper.md` per spec W-D structure; claims table mapping every claim → repo artifact
- [ ] Task: Related-work section (L4, Catala, LegalRuleML, DMN, policyengine-taxsim, Policy2Code/DBN reports, foi-o preprint) — honest adoption history, primary citations
- [ ] Task: Results sections generated from Track artifacts (differential agreement numbers, corpus stats, divergence findings)
- [ ] Task: [HUMAN] Review; arXiv submission; venue decision
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
