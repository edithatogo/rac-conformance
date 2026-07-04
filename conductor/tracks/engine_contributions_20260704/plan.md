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
- [ ] Task: [HUMAN] Review + submit trace issue
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2 — C-B: Missingness cases

- [ ] Task: Reproduce missingness conflation in PolicyEngine
    - [ ] Construct 3–5 runnable cases where unprovided input silently defaults (record engine version); verify each actually reproduces before writing it up
    - [ ] Write `external/policyengine/MISSINGNESS_CASES.md` + `SUBMISSION_missingness.md` issue draft
    - **Acceptance:** every case has verified runnable output pasted in
- [ ] Task: Same for OpenFisca
    - [ ] Use `openfisca-aotearoa` or `-france`; same structure; `external/openfisca/MISSINGNESS_CASES.md` + submission draft
    - **Acceptance:** as above
- [ ] Task: [HUMAN] Review + submit (PolicyEngine first)
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3 — C-C: Axiom harness

- [ ] Task: Write `external/axiom/HARNESS_DESIGN.md` per spec C-C (design only; oracle-independence section mandatory)
    - **Acceptance:** design doc complete
- [ ] Task: [HUMAN] Dylan reviews design and documents Axiom's actual interfaces (what a generated model looks like, how to execute it)
    - > This task gates the prototype. Agents: do not guess Axiom internals.
- [ ] Task: Prototype harness runner in `harness/axiom/`
    - [ ] Tests first against a stub "generated model" interface defined from Dylan's notes; differential run over PIC fixtures; divergence report output (reuse Track 5 report module if it exists yet, else minimal Markdown reporter)
    - **Acceptance:** pytest green on stub; runbook written for pointing it at a real Axiom model
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
