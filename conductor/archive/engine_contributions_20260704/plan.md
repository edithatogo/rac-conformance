# Plan: engine_contributions_20260704

Depends on: contracts_20260704 phases 1–3. Requires network + engine installs. Sub-tracks C-A/C-B/C-C are independent; do in listed order unless blocked.

## Phase 1 — C-A: PolicyEngine trace investigation

- [x] Task: Computation-tree investigation
    - [x] Install `policyengine-us` in a venv; run one household simulation (e.g. SNAP for a 3-person household); locate and dump the computation tree / tracer output
    - [x] Read `policyengine-core` source for the tracer; document node contents with permalinks
    - [x] Write `external/policyengine/TRACE_INVESTIGATION.md` incl. the vectorized-derivation feasibility assessment (household: direct; microsim: measure per-case re-execution cost on a 1k-household CPS sample if feasible)
    - **Acceptance:** doc complete with permalinks and measured (or honestly-blocked) microsim numbers
- [x] Task: Prototype `to_trace()` projection
    - [x] Tests first: household SNAP simulation → pic-traces document that passes `pic-validate`; parameterVersions populated; steps ordered by dependency
    - [x] Implement projection in `harness/policyengine_trace/` (here, not upstream yet)
    - **Acceptance:** pytest green; emitted trace validates
- [x] Task: Draft upstream issue
    - [x] `external/policyengine/SUBMISSION_trace.md`: propose versioned trace export; include the prototype as evidence; PIC as footnote
    - **Acceptance:** draft complete
- [x] Task: [HUMAN] Review + submit trace issue
    - > HUMAN-GATE (2026-07-04): Draft issue is prepared at `external/policyengine/SUBMISSION_trace.md`. Agent must stop here; Dylan reviews/edits and submits upstream if appropriate.
    > HUMAN-APPROVED (2026-07-06): Dylan approved and submitted the trace issue.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2 — C-B: Missingness cases

- [x] Task: Reproduce missingness conflation in PolicyEngine
    - [x] Construct 3–5 runnable cases where unprovided input silently defaults (record engine version); verify each actually reproduces before writing it up
    - [x] Write `external/policyengine/MISSINGNESS_CASES.md` + `SUBMISSION_missingness.md` issue draft
    - **Acceptance:** every case has verified runnable output pasted in
- [x] Task: Same for OpenFisca
    - [x] Use `openfisca-aotearoa` or `-france`; same structure; `external/openfisca/MISSINGNESS_CASES.md` + submission draft
    - **Acceptance:** as above
- [x] Task: [HUMAN] Review + submit (PolicyEngine first)
    > HUMAN-APPROVED (2026-07-06): Dylan approved and submitted the missingness issues.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3 — C-C: Axiom harness

- [x] Task: Write `external/axiom/HARNESS_DESIGN.md` per spec C-C (design only; oracle-independence section mandatory)
    - **Acceptance:** design doc complete
- [x] Task: [HUMAN] Dylan reviews design and documents Axiom's actual interfaces (what a generated model looks like, how to execute it)
    > CHECKPOINT (2026-07-06): Public Axiom docs were searched and summarized in `external/axiom/PUBLIC_INTERFACE_NOTES.md`. The public RuleSpec runtime interface is documented enough for a generic RuleSpec/compiled-artifact adapter prototype; Dylan review remains required to confirm whether the actual generated model under test is a RuleSpec file, compiled artifact, repo-backed jurisdiction module, or app-specific wrapper.
    > CHECKPOINT (2026-07-06): `TheAxiomFoundation/rulespec-nz` was verified as a concrete public RuleSpec corpus at `3c6436b2ecf82dd7a7f7810a406a2695a64af33a`, with `nz/...` RuleSpec modules, companion tests, and oracle references. Remaining human input is now narrower: confirm whether `rulespec-nz` is the intended generated-model surface and choose the first module/test slice.
    > HUMAN-APPROVED (2026-07-06): Dylan approved proceeding with `rulespec-nz` as the public Axiom surface and the GST smoke slice first, then moving to a higher-overlap tax/benefit slice after the mechanics work.
- [x] Task: Prototype harness runner in `harness/axiom/`
    - [x] Tests first against a stub "generated model" interface defined from Dylan's notes; differential run over PIC fixtures; divergence report output (reuse Track 5 report module if it exists yet, else minimal Markdown reporter)
    - **Acceptance:** pytest green on stub; runbook written for pointing it at a real Axiom model
    > FIXUP (2026-07-06): Reworked the prototype to target the approved `rulespec-nz` GST smoke slice directly, using stdlib-only compiled-execution request dictionaries, deterministic stub-executor tests, and a runbook for local `axiom-rules-engine` compiled artifacts. Verified with `make check`.
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
