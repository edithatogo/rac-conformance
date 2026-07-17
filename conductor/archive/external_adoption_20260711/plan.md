# Plan: external_adoption_20260711

## Phase 1 - Evidence refresh

- [x] Task: Refresh all seven PR branches, checks, reviews, and issue linkages
- [x] Task: Reproduce each contributor-controlled test surface and record versions
- [x] Task: Conductor - Automated Review and Checkpoint 'Evidence refresh' (Protocol in workflow.md)

> CHECKPOINT (2026-07-14): Alaveteli #9355 and PR #9356 are closed without merge; no maintainer rationale is visible. PolicyEngine #515-#517, OpenFisca #1382, RuleSpec NZ #80, and OpenFisca Aotearoa #200 remain open with maintainer, workflow, CI, review, or signing gates. Local repository maintenance PR #27 is merged with all required checks passing. Ledgers were refreshed in `external/UPSTREAM_PR_AUDIT.md` and `external/MAINTAINER_MONITORING.md`.

> CHECKPOINT (2026-07-15): A live PR sweep found no new terminal outcome. PolicyEngine #515-#517 remain open with empty hosted check rollups; OpenFisca #1382 and OpenFisca Aotearoa #200 remain `REVIEW_REQUIRED`; RuleSpec NZ #80 remains `CHANGES_REQUESTED` with two hosted validation failures; Alaveteli #9356 remains closed without merge. RaC Conformance preparation PRs #80 and #81 merged successfully, but they do not change upstream adoption status. Any source-controlled RuleSpec fix remains contributor-preparable; workflow approval, signing, hosted re-run, and merge/decline remain maintainer-controlled.

## Phase 2 - Review response

- [x] Task: Apply actionable maintainer feedback with focused regression tests
- [x] Task: Resolve contributor-controlled CI failures and conflicts
- [x] Task: Prepare maintainer follow-up packets and terminal-state evidence requirements
- [x] Task: [HUMAN] Supply or request maintainer-only workflow approvals, signing, and merge decisions

> BLOCKED (2026-07-14): Remaining upstream actions require maintainer-only
> workflow approval/review, Axiom signing credentials, or upstream merge
> authority. PolicyEngine maintainers have now provided constructive comments
> on #515-#517, but hosted checks remain held pending fork workflow approval;
> upstream follow-up must remain staged here and cannot be pushed by this repo.
> COMPLETED BOUNDARY (2026-07-17): Authorized requests were already posted.
> RuleSpec NZ #79/#80 now have a documented maintainer decision: the diagnosis
> and semantic fix were reproduced through supervised-encoder migration #83 on
> upstream `main`, verified by clean compile and 3/3 companion tests, and closed
> with credit. PolicyEngine and OpenFisca requests remain explicitly externally
> blocked; no additional contributor-controlled request can produce a decision.
- [x] Task: Conductor - Automated Review and Checkpoint 'Review response' (Protocol in workflow.md)

> BLOCKED (2026-07-11): Remaining work requires upstream maintainer workflow approval/review and an Axiom signing key. No contributor-controlled fix can clear these external gates.

## Phase 3 - Adoption closeout

- [x] Task: Record merged, declined, superseded, or externally blocked disposition for every contribution
- [x] Task: Update Project 19 and repository ledgers from URL evidence

> CHECKPOINT (2026-07-14): Every staged contribution now has an explicit disposition in `external/ADOPTION_STATUS.md`. Project 19 issue #23 remains In Progress, matching unresolved external gates; no Project status or local ledger entry is treated as upstream acceptance.
- [x] Task: Conductor - Automated Review and Checkpoint 'Adoption closeout' (Protocol in workflow.md)

> CHECKPOINT (2026-07-14): Review found no correctness, scope, test, contract, or documentation defects requiring remediation after the PolicyEngine maintainer-status refresh. Full `make check` passed. The track remains in progress solely because upstream workflow, signing, review, and merge gates are unresolved.

> CHECKPOINT (2026-07-17): Live review reconciled RuleSpec NZ #80 to its
> terminal, credited upstream-adoption outcome. Every other unresolved
> contribution has current URL evidence and an explicit maintainer-controlled
> disposition. The acceptance rule permits terminal or explicitly blocked
> outcomes, so no contributor-controlled implementation task remains.
