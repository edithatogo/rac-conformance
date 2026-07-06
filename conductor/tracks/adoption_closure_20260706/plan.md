# Implementation Plan

Depends on: `repo_boundaries_20260706` Phase 1. Use `conductor/edithatogo-repo-boundaries.md` before touching any external repo.
Also depends on `roadmap_release_20260706` Phase 1 for GitHub issue/project synchronization.

## Phase 1 - Adoption Inventory

- [x] Task: Build adoption ledger
    - [x] Read every `external/*/SUBMISSION*.md`, `external/dbn/LOG.md`, and archived plan checkpoint that mentions upstream submission.
    - [x] Create `external/ADOPTION_STATUS.md` with target, artifact, status, URL, CI state, owner, and next action columns.
    - [x] Mark unknown external status as `needs_verification`, not complete.
    - **Acceptance:** every staged external artifact has one ledger row.
- [x] Task: Link adoption ledger to GitHub roadmap issue hierarchy
    - [x] Read `conductor/github-planning.md`.
    - [x] Add GitHub issue/project URL columns where useful.
    - [x] Ensure external-gate and human-gate labels are applied to relevant track issues.
    - **Acceptance:** adoption rows can be traced to GitHub issues or explicit non-GitHub contacts.
- [x] Task: Verify live external state
    - [x] Use GitHub CLI/API for issue/PR state where available.
    - [x] Check DBN log and any available mailbox/thread evidence only when the relevant connector/tool is available and authorized.
    - [x] Record exact URLs or "not found / not accessible".
    - **Acceptance:** no row remains uninspected unless access is blocked and logged.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Adoption Inventory' (Protocol in workflow.md)


## Phase 2 - Patch-Ready External Bundles

- [x] Task: Prepare `foi-o` PR bundle
    - [x] Confirm local `foi-o` branch status before editing.
    - [x] Apply the staged OIA rules module into the `foi-o` checkout or refresh the patch bundle, respecting existing user changes.
    - [x] Run `foi-o` tests relevant to the rules module.
    - [x] Commit in the external repo only if changes are authorized and scoped. No external commit was needed because the bundle was already present and verified locally.
    - **Acceptance:** PR-ready branch or patch bundle exists; CI/test command output is logged.
    > CHECKPOINT (2026-07-06): `foi-o` checkout is clean on `main`, the staged OIA rules module already exists under `external/foi-o/`, and `uv run pytest tests/test_oia_rules.py` plus coverage passed in the external repo. The bundle is ready for Dylan's human submission step.
- [ ] Task: Prepare PolicyEngine/OpenFisca issue and PR follow-through
    - [ ] Verify whether trace, missingness, and converter submissions are already open.
    - [ ] If not open, prepare final issue/PR text and mark `[HUMAN]` submission gate.
    - [ ] If open, monitor responses and apply requested documentation/code fixes in this repo or external repo as appropriate.
    - **Acceptance:** every PolicyEngine/OpenFisca artifact has live URL, human gate, or blocked reason.
- [ ] Task: Prepare Alaveteli follow-through
    - [ ] Verify whether the Alaveteli state-taxonomy discussion/issue exists.
    - [ ] If not, prepare final discussion text and mark `[HUMAN]` submission gate.
    - [ ] If open, record response and next action.
    - **Acceptance:** Alaveteli status is not ambiguous.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Patch-Ready External Bundles' (Protocol in workflow.md)

## Phase 3 - CI, Review, And Merge Closure

- [ ] Task: Monitor active PRs and GitHub Actions
    - [ ] For every live PR, record latest commit SHA, required checks, pass/fail state, and reviewer state.
    - [ ] Apply fixes for failing checks where the agent has push authority.
    - [ ] Commit each fix with the external repo's conventions.
    - **Acceptance:** all agent-addressable CI failures are fixed or precisely blocked.
- [ ] Task: Reconcile GitHub Projects status fields
    - [ ] Confirm project items match local track and adoption ledger states.
    - [ ] Use parent issue/sub-issue progress to report completion.
    - [ ] Update issue comments with CI and PR URLs when status changes.
    - **Acceptance:** GitHub project state is not stale relative to local docs.
- [ ] Task: [HUMAN] Merge or maintainer-response gate
    - [ ] Present merge-ready PRs and external-response queue to Dylan.
    - [ ] Record which PRs Dylan merges, which require maintainer review, and which are intentionally deferred.
    - **Acceptance:** no PR is represented as merged without URL evidence.
- [ ] Task: Update adoption ledger and README summary
    - [ ] Refresh `external/ADOPTION_STATUS.md`.
    - [ ] Add a short status pointer in `README.md` or `conductor/tracks.md` if appropriate.
    - **Acceptance:** repo-local documentation matches live external state.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - CI, Review, And Merge Closure' (Protocol in workflow.md)
