# Implementation Plan

Depends on: `repo_boundaries_20260706` Phase 2 and `adoption_closure_20260706` Phase 1.

## Phase 1 - Demo Architecture

- [x] Task: Confirm demo surfaces
    - [x] Re-read `external/docassemble/ASSESSMENT.md` and `external/civiform/ASSESSMENT.md`.
    - [x] Select exact local paths for demo artifacts.
    - [x] Define request/response JSON examples.
    - **Acceptance:** `demos/service-boundaries/DESIGN.md` defines both demos and their limits.
- [x] Task: Write schema/tests first
    - [x] Add request/response validation tests.
    - [x] Add trace-presence tests.
    - **Acceptance:** tests fail before implementation.

> CHECKPOINT (2026-07-07): The service-boundary design now names exact Docassemble-style and CiviForm-style demo artifacts under `demos/service-boundaries/`, and the committed examples define both request and response payloads.
> The shared demo helper exercises the staged OIA rules module, and the new tests cover request validation, response shape, and trace presence.
> `make check` passed, while the actual README instructions, privacy review, and outreach packet remain deferred to later phases.

- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Demo Architecture' (Protocol in workflow.md)

## Phase 2 - OIA/Docassemble Demo

- [x] Task: Implement Docassemble-style OIA invocation demo
    - [x] Build a small local runner using the staged OIA rules module.
    - [x] Include representative interview input and rule result output.
    - [x] Add README instructions.
    - **Acceptance:** demo test calculates expected OIA deadline and emits trace fields.
- [x] Task: Validate no process coupling regression
    - [x] Confirm the rules module does not import unrelated `foi-o` process code.
    - [x] Run relevant OIA tests and `pic-validate`.
    - **Acceptance:** import isolation and validation pass.

> CHECKPOINT (2026-07-07): Phase 2 now has a deterministic Docassemble-style demo runner backed by the staged OIA rules module and a real `foi_o_nz.dates` helper in the demo tree.
> The regression check confirms the rules import path stays isolated from unrelated process code, and the targeted OIA tests plus `pic-validate` both pass.
> `make check` also remains green, while the CiviForm mock, privacy/security review, outreach packet, and external packaging work are still deferred to later phases.

- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - OIA/Docassemble Demo' (Protocol in workflow.md)

## Phase 3 - CiviForm-Style Service Mock

- [x] Task: Implement HTTP or CLI service-boundary mock
    - [x] Accept a JSON application payload.
    - [x] Call a PIC-tested rule function.
    - [x] Return a PIC-shaped result and trace summary.
    - **Acceptance:** integration test covers valid and invalid requests.
- [x] Task: Document CiviForm path
    - [x] State what a real CiviForm integration would require.
    - [x] Record whether Java/plugin work is justified.
    - **Acceptance:** README prevents overclaiming production readiness.

> CHECKPOINT (2026-07-07): Phase 3 now has both a runnable CiviForm-style CLI mock and a README that states the integration boundary without overclaiming production readiness.
> The mock accepts the committed JSON request example, returns a PIC-shaped result with trace summary, and the tests cover both the valid example and an invalid-request rejection path.
> `make check` remains green, and the remaining work is now the phase-4 review, CI wiring, outreach packaging, and release/monitoring tasks.

- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - CiviForm-Style Service Mock' (Protocol in workflow.md)

## Phase 4 - CI And External Packaging

- [ ] Task: Privacy/security review
    - [ ] Confirm no real applicant/requester data is committed.
    - [ ] Confirm no secrets, tokens, or live service credentials are required.
    - [ ] Confirm tests mock external calls.
    - [ ] Confirm trace outputs are minimal and do not leak unnecessary private inputs.
    - **Acceptance:** review checklist is committed and all items pass or are blocked.
- [ ] Task: Add checks to `make check`
    - [ ] Include demo tests without requiring external services.
    - [ ] Keep fixtures deterministic.
    - **Acceptance:** `make check` passes locally.
- [ ] Task: Prepare outreach/update packet
    - [ ] Draft update for DBN/Docassemble/CiviForm only if demo is credible.
    - [ ] Mark sending/posting as `[HUMAN]`.
    - **Acceptance:** packet is staged or explicitly deferred.
- [ ] Task: Push branch and monitor GitHub Actions
    - [ ] Push after local green checks.
    - [ ] Apply fixes for failing Actions.
    - **Acceptance:** branch Actions pass or exact blocker is recorded.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - CI And External Packaging' (Protocol in workflow.md)
