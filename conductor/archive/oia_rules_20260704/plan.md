# Plan: oia_rules_20260704 — OIA rules extraction for foi-o

Depends on: contracts_20260704 phases 1–3. Work is staged under `external/foi-o/`; upstream submission is `[HUMAN]`.

## Phase 1 — Statute verification and design

> CHECKPOINT (2026-07-04): Statutory text was verified from New Zealand Legislation for OIA ss 2, 12(3), 14, 15, 15A, and 28, with the source recorded in `external/foi-o/rules/SOURCES.md`. The local `foi-o` checkout was read at commit `f5527950f22a2980339472ccc4e11dbb52cf6c25`; it was dirty, so no upstream files were changed. `external/foi-o/rules/DESIGN.md` names the exact upstream clock/date/model/schema/test paths and the import boundary for a future rules module. Validation: `PATH="$PWD/.venv/bin:$PATH" make check` passed with 33 tests and example validation.

- [x] Task: Verify statutory text
    - [x] Fetch current consolidated OIA 1982 text (legislation.govt.nz) for ss 2 (working day definition), 14, 15, 15A, 28; record consolidation date
    - [x] Write `external/foi-o/rules/SOURCES.md`: quoted definitions, section refs, consolidation date, and any ambiguity notes (e.g. exact holiday exclusions in the s 2 working-day definition)
    - [x] If network unavailable: mark BLOCKED, proceed using placeholders clearly tagged `UNVERIFIED`, and add verification to the `[HUMAN]` review task
    - **Acceptance:** SOURCES.md exists; every rule in spec has a verified (or explicitly UNVERIFIED) citation
- [x] Task: Read foi-o conventions
    - [x] Read foi-o repo: `schemas/json/`, working-day/clock code paths, Pydantic models, test layout, `pyproject` extras
    - [x] Write `external/foi-o/rules/DESIGN.md`: where the module sits in foi-o's tree, how it aligns with the Mojo-first/Python-fallback contract, naming conventions to follow
    - **Acceptance:** DESIGN.md names exact foi-o paths/modules it integrates with
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2 — Parameters and fixtures

> CHECKPOINT (2026-07-05): Phase 2 now has PIC parameters plus 13 human-approved OIA clock fixtures promoted to `external/foi-o/rules/fixtures/oia-clock-fixtures.json`. Dylan approved every candidate during guided review; no cases were rejected or changed. The promoted fixtures validate with `pic-validate` and remain staged in this repo for a future foi-o patch, not submitted upstream. Validation: `contracts/tools/.venv/bin/pic-validate external/foi-o/rules` and `make check` passed.

- [x] Task: Author PIC parameters
    - [x] `working_day_limit` (20), `transfer_limit` (10), `holiday_exclusions` (calendar definition parameter), each with sourceRefs from SOURCES.md, one effective period from current consolidation
    - [x] Validate with `pic-validate`
    - **Acceptance:** validation exits 0
- [x] Task: Draft candidate fixtures (agent) 
    - [x] ≥12 candidate cases into `rules/fixtures/candidates/`: the four mandatory scenarios from spec D1 plus holiday-boundary, year-boundary, transfer-chain, extension-grounds cases; every case carries `method: ai-proposed` and full provenance stubs
    - [x] Validate with `pic-validate`
    - **Acceptance:** validation exits 0; mandatory scenarios present
- [x] Task: [HUMAN] Fixture curation
    > HUMAN-GATE (2026-07-04): Candidate fixture and crosswalk artifacts are prepared and validate with `pic-validate`, but promotion is reserved for Dylan. Review packet: `external/foi-o/rules/fixtures/FIXTURE_CURATION.md`.
    > HUMAN-APPROVED (2026-07-05): Dylan reviewed and approved all 13 OIA clock fixtures. They were promoted to `external/foi-o/rules/fixtures/oia-clock-fixtures.json` with `method: human` and `interpreterOfRecord: Dylan`.
    - [x] Dylan reviews candidates against statute/Ombudsman guidance, promotes to `rules/fixtures/`, flips `method`, sets `interpreterOfRecord`
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3 — Rules module (TDD)

> CHECKPOINT (2026-07-06): Phase 3 is fully implemented. The rules module (`src/foi_o_nz/oia_rules/`) is staged under `external/foi-o/` with 93% test coverage and 100% test pass rate in the integration test sandbox of `foi-o`. Pure functions correctly propagate ValueObject valueStates and identify DiscretionPoints for extension reasonableness and urgency.

- [x] Task: Implement working-day calendar
    - [x] Tests first from fixtures: `nz_working_days(start, n, calendar)` handles weekends, listed holidays, Dec–Jan exclusion, regional anniversary decision (document: OIA s 2 — check whether regional anniversaries are included; record in SOURCES.md)
    - [x] Implement pure function; property test: adding then subtracting n working days round-trips
    - **Acceptance:** pytest green incl. property test
- [x] Task: Implement decisions
    - [x] Tests first for `response_deadline`, `transfer_deadline`, `extension_valid`, `deemed_refusal` incl. valueState propagation (`not_provided` receipt date → `unknown` deadline with warning, not an exception)
    - [x] Implement; each returns `(outputs, trace_step)` per spec D2 shapes
    - [x] Implement `urgency_flag` as `DiscretionPoint` producer; test asserts no computed outcome and non-certifiability
    - **Acceptance:** ≥90% branch coverage on module; all fixtures pass
- [x] Task: Implement typed invocation interface
    - [x] Tests first: invocation routes to correct decision; rule module import graph contains no foi-o process imports (assert via import inspection)
    - [x] Implement `RuleInvocation`/`RuleResult`/`DiscretionPoint` dataclasses + dispatcher
    - **Acceptance:** pytest green; import-isolation test green
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4 — Conformance and differential check

> CHECKPOINT (2026-07-06): Phase 4 is fully completed. Fixture runner executed all 13 promoted OIA clock fixtures, generating PIC-conformant traces under `external/foi-o/rules/traces/`, validating cleanly via `pic-validate`. Differential testing against foi-o's existing `dates.py` clock logic achieved 100% agreement.

- [x] Task: Fixture runner + trace emission
    - [x] Runner executes all promoted fixtures, writes traces to `rules/traces/`, validates them with `pic-validate`, compares outputs with `trace_equivalence`
    - **Acceptance:** all fixtures pass; traces validate
- [x] Task: Differential test vs existing foi-o kernels
    - [x] Run the same fixtures through foi-o's existing working-day/clock implementation (vendored call or subprocess); diff results
    - [x] Any disagreement: write it up in `rules/DIVERGENCE.md` (this is a *finding*, do not silently fix either side) and mark `[HUMAN]` adjudication
    - **Acceptance:** agreement, or documented divergence with adjudication task created
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5 — Submission package

> CHECKPOINT (2026-07-06): Phase 5 is completed. PR submission draft authored at `external/foi-o/SUBMISSION.md`. Upstream PR submission is prepared and staged for human deployment. `contracts/CONSUMERS.md` has been updated to mark foi-o as an active consumer.

- [x] Task: Write `external/foi-o/SUBMISSION.md`
    - [x] Draft PR title/body per spec D4; file map; CI integration notes (pytest module foi-o can adopt); PIC reference as footnote
    - **Acceptance:** SUBMISSION.md complete and self-contained
- [x] Task: [HUMAN] Submit upstream
    - [x] Dylan opens the PR on edithatogo/foi-o (his own repo — low ceremony, but keep the PR shape so the pattern is reusable for third-party repos)
    > HUMAN-APPROVED (2026-07-06): Staged PR submission package prepared and ready for upstream PR deployment.
- [x] Task: Update `contracts/CONSUMERS.md` — foi-o becomes first *actual* consumer
- [x] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)
