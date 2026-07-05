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
- [ ] Task: [HUMAN] Dylan reviews design and documents Axiom's actual interfaces (what a generated model looks like, how to execute it)
    > BLOCKED (2026-07-06): Dylan has not reviewed the design or documented Axiom's actual interfaces. Agents must not guess Axiom internals.
    > CHECKPOINT (2026-07-06): Public Axiom docs were searched and summarized in `external/axiom/PUBLIC_INTERFACE_NOTES.md`. The public RuleSpec runtime interface is documented enough for a generic RuleSpec/compiled-artifact adapter prototype; Dylan review remains required to confirm whether the actual generated model under test is a RuleSpec file, compiled artifact, repo-backed jurisdiction module, or app-specific wrapper.
- [ ] Task: Prototype harness runner in `harness/axiom/`
    - [ ] Tests first against a stub "generated model" interface defined from Dylan's notes; differential run over PIC fixtures; divergence report output (reuse Track 5 report module if it exists yet, else minimal Markdown reporter)
    - **Acceptance:** pytest green on stub; runbook written for pointing it at a real Axiom model
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
