# Next-generation Roadmap Release Status

Last updated: 2026-07-17.

This file records the GitHub execution ledger for the next-generation roadmap. Local Conductor specs and plans remain the source of truth for requirements and acceptance.

## Release decision (2026-07-09)

**Decision: keep external monitoring open.**

Publication decision: keep the coupling, SNAP, and NZ reconciliation papers
deferred until the next `foi-o` release is available; update all three papers
after that release and submit only with Dylan's explicit authorization.

- **Repo-local roadmap work:** complete (`make check` green; non-final tracks archived with evidence).
- **External adoption:** every staged GitHub target has a durable URL in `external/ADOPTION_STATUS.md`.
- **Maintainer replies:** RuleSpec NZ #79/#80 reached a terminal credited-adoption outcome; other replies and unresolved proposals are tracked in `external/MAINTAINER_MONITORING.md`.
- **Do not claim** broad external merge/adoption beyond the merged `foi-o` work and the RuleSpec NZ fix adopted through canonical migration #83. PR #80 was closed with credit, not merged.

Interpreter of record: Dylan (session authorization to address remaining human gates).

## GitHub Ledger

Project: [Rules and Processes Integration Dashboard](https://github.com/users/edithatogo/projects/19)

Milestone: [Next-generation roadmap](https://github.com/edithatogo/rac-conformance/milestone/1)

Parent issue: [#6 Next-generation roadmap: adoption, v0.2, validation, demos, studies, release](https://github.com/edithatogo/rac-conformance/issues/6)

Native sub-issues attached to #6:

| Issue | Conductor track | Local path |
|---|---|---|
| [#7](https://github.com/edithatogo/rac-conformance/issues/7) | `roadmap_release_20260706` | `conductor/archive/roadmap_release_20260706/` |
| [#8](https://github.com/edithatogo/rac-conformance/issues/8) | `repo_boundaries_20260706` | `conductor/archive/repo_boundaries_20260706/` |
| [#9](https://github.com/edithatogo/rac-conformance/issues/9) | `adoption_closure_20260706` | `conductor/archive/adoption_closure_20260706/` |
| [#10](https://github.com/edithatogo/rac-conformance/issues/10) | `pic_v02_20260706` | `conductor/archive/pic_v02_20260706/` |
| [#11](https://github.com/edithatogo/rac-conformance/issues/11) | `axiom_validation_20260706` | `conductor/archive/axiom_validation_20260706/` |
| [#12](https://github.com/edithatogo/rac-conformance/issues/12) | `service_demos_20260706` | `conductor/archive/service_demos_20260706/` |
| [#13](https://github.com/edithatogo/rac-conformance/issues/13) | `comparative_studies_20260706` | `conductor/archive/comparative_studies_20260706/` |
| [#14](https://github.com/edithatogo/rac-conformance/issues/14) | `nz_reconciliation_20260707` | `conductor/archive/nz_reconciliation_20260707/` |

Completed prior-track issues [#1](https://github.com/edithatogo/rac-conformance/issues/1) through [#5](https://github.com/edithatogo/rac-conformance/issues/5) are closed as completed.

## Release Matrix

| Track | Issue | Project status | Depends on | CI gate | External/human gate | Next action |
|---|---:|---|---|---|---|---|
| `roadmap_release_20260706` | [#7](https://github.com/edithatogo/rac-conformance/issues/7) | Done (monitor) | All child tracks | `make check` green 2026-07-09 | Release decision recorded: keep external monitoring open | Monitor upstream issue replies; optional follow-up tracks |
| `repo_boundaries_20260706` | [#8](https://github.com/edithatogo/rac-conformance/issues/8) | Done | None | Docs / `make check` | None | Archived |
| `adoption_closure_20260706` | [#9](https://github.com/edithatogo/rac-conformance/issues/9) | Done | Repo boundaries; roadmap phase 1 | N/A for drafts | URL-backed terminal or externally blocked outcomes recorded in ledger | Monitor unresolved targets in `MAINTAINER_MONITORING.md` |
| `pic_v02_20260706` | [#10](https://github.com/edithatogo/rac-conformance/issues/10) | Done | Adoption evidence | `make check` | Consumer evidence | Archived |
| `axiom_validation_20260706` | [#11](https://github.com/edithatogo/rac-conformance/issues/11) | Done | Axiom artifacts | Harness + Actions | RuleSpec NZ #79/#80 resolved on upstream `main` through canonical migration #83 | None for #79/#80; retain evidence |
| `service_demos_20260706` | [#12](https://github.com/edithatogo/rac-conformance/issues/12) | Done | Boundaries / PIC / Axiom | Demo tests | None blocking | Archived |
| `comparative_studies_20260706` | [#13](https://github.com/edithatogo/rac-conformance/issues/13) | Done | Adoption / validation evidence | Study draft validation | Study selection approved | Archived; spawned NZ recon track |
| `nz_reconciliation_20260707` | [#14](https://github.com/edithatogo/rac-conformance/issues/14) | Done | Comparative study selection | `make nz-recon-*` | Certified engine-gap; [openfisca-aotearoa#199](https://github.com/BetterRules/openfisca-aotearoa/issues/199) | Monitor #199; optional future dual-engine track |

Certification levels used by this matrix:

- `repo-local complete`: local track archived with required checks passing.
- `submitted upstream`: issue, PR, email, or submission URL is recorded.
- `under review`: external actor has acknowledged or the PR/submission remains open.
- `merged`: external repository or destination accepted the contribution.
- `declined`: external actor declined or replaced the contribution.
- `blocked by external actor`: no further local action can advance the item.
- `superseded`: later approved plan makes the item unnecessary.
- `engine_gap`: comparative study completed with documented non-overlap (not numeric agreement).

## Historical external adoption snapshot (2026-07-09)

The counts below are the recorded 2026-07-09 snapshot, not the current ledger.
RuleSpec NZ #79/#80 subsequently reached credited upstream adoption through
canonical migration #83 on 2026-07-17.

| Outcome | Count | Notes |
|---|---:|---|
| Merged upstream (this program) | 1 | `edithatogo/foi-o` PR #20 |
| Submitted open issues | 8 | PE×3, OF-core×2, Alaveteli×1, rulespec-nz×1, openfisca-aotearoa×1 |
| Email sent / monitor | 1 | DBN CoP |
| Maintainer replies | 0 | As of monitoring sweep |

Full table: `external/ADOPTION_STATUS.md`.

## Operating Boundary

GitHub Projects is the visibility layer, not the requirements source. Update the local Conductor plan first, then mirror status, evidence links, PRs, and external blockers to the matching GitHub issue.
