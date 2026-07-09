# Plan: NZ recon live dual-engine re-run

## Phase 1 — Live suite
- [x] Task: Add OpenFisca live runner (`openfisca_live.py`)
- [x] Task: Add dual-engine orchestrator (`run_live_suite.py`)
- [x] Task: Run suite; publish `results/LIVE_DUAL_ENGINE_REPORT.md`
- [x] Task: Fix OF KiwiSaver negative-earnings clamp (pushed to Aotearoa PR #200)
- [x] Task: Record remaining gaps (self-employed ACC, Crown KS parameters)

> CHECKPOINT (2026-07-09): Live suite yields **10/17 numeric agreements** (all income tax, standard ACC, standard KiwiSaver). Remaining 7 are intentional surface gaps (self-employed ACC / weekly purchase / invoice exempt; Crown KS cap case).
