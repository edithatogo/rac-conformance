# Next-generation Roadmap Release Status

Last updated: 2026-07-07.

This file records the GitHub execution ledger for the next-generation roadmap. Local Conductor specs and plans remain the source of truth for requirements and acceptance.

## GitHub Ledger

Project: [Rules and Processes Integration Dashboard](https://github.com/users/edithatogo/projects/19)

Milestone: [Next-generation roadmap](https://github.com/edithatogo/rulesandprocesses/milestone/1)

Parent issue: [#6 Next-generation roadmap: adoption, v0.2, validation, demos, studies, release](https://github.com/edithatogo/rulesandprocesses/issues/6)

Native sub-issues attached to #6:

| Issue | Conductor track | Local path |
|---|---|---|
| [#7](https://github.com/edithatogo/rulesandprocesses/issues/7) | `roadmap_release_20260706` | `conductor/tracks/roadmap_release_20260706/` |
| [#8](https://github.com/edithatogo/rulesandprocesses/issues/8) | `repo_boundaries_20260706` | `conductor/tracks/repo_boundaries_20260706/` |
| [#9](https://github.com/edithatogo/rulesandprocesses/issues/9) | `adoption_closure_20260706` | `conductor/tracks/adoption_closure_20260706/` |
| [#10](https://github.com/edithatogo/rulesandprocesses/issues/10) | `pic_v02_20260706` | `conductor/tracks/pic_v02_20260706/` |
| [#11](https://github.com/edithatogo/rulesandprocesses/issues/11) | `axiom_validation_20260706` | `conductor/tracks/axiom_validation_20260706/` |
| [#12](https://github.com/edithatogo/rulesandprocesses/issues/12) | `service_demos_20260706` | `conductor/tracks/service_demos_20260706/` |
| [#13](https://github.com/edithatogo/rulesandprocesses/issues/13) | `comparative_studies_20260706` | `conductor/tracks/comparative_studies_20260706/` |

Completed prior-track issues [#1](https://github.com/edithatogo/rulesandprocesses/issues/1) through [#5](https://github.com/edithatogo/rulesandprocesses/issues/5) are closed as completed and their project status is `Done`.

## Release Matrix

| Track | Issue | Project status | Depends on | CI gate | External/human gate | Next action |
|---|---:|---|---|---|---|---|
| `roadmap_release_20260706` | [#7](https://github.com/edithatogo/rulesandprocesses/issues/7) | Todo | All active tracks for final certification | `make check`; GitHub Actions before final certification | Dylan release decision | Finish Phase 1 checkpoint, then hold mid/final audits until child tracks progress. |
| `repo_boundaries_20260706` | [#8](https://github.com/edithatogo/rulesandprocesses/issues/8) | Done | None | Documentation validation via `make check` where applicable | None unless repo classification is disputed | Completed and archived in `conductor/archive/repo_boundaries_20260706/`. |
| `adoption_closure_20260706` | [#9](https://github.com/edithatogo/rulesandprocesses/issues/9) | Todo | `repo_boundaries_20260706` Phase 1; `roadmap_release_20260706` Phase 1 | GitHub Actions on any pushed branches/PRs | Upstream maintainers and Dylan submission/merge approvals | Build adoption ledger and issue/PR/submission packets. |
| `pic_v02_20260706` | [#10](https://github.com/edithatogo/rulesandprocesses/issues/10) | Done | Adoption Phase 3 consumer evidence | `make check`; contract examples and schema tests; GitHub Actions | Consumer compatibility evidence | Completed and archived in `conductor/archive/pic_v02_20260706/`. |
| `axiom_validation_20260706` | [#11](https://github.com/edithatogo/rulesandprocesses/issues/11) | Todo | Existing Axiom validation artifacts | `make check`; harness regression tests; GitHub Actions | Axiom upstream/source availability where external validation is needed | Expand deterministic RuleSpec NZ fixture/harness coverage. |
| `service_demos_20260706` | [#12](https://github.com/edithatogo/rulesandprocesses/issues/12) | Todo | Repo-boundary Phase 2; PIC/Axiom artifacts where reused | `make check`; demo tests; GitHub Actions | Dylan demo review; no live secrets or third-party calls | Build local-only service-boundary demo packets. |
| `comparative_studies_20260706` | [#13](https://github.com/edithatogo/rulesandprocesses/issues/13) | Done | Adoption and validation evidence for candidate scoring | Candidate evidence validation; later track-specific checks | Dylan study approval before implementation track | Completed and archived in `conductor/archive/comparative_studies_20260706/`. |

Certification levels used by this matrix:

- `repo-local complete`: local track archived with required checks passing.
- `submitted upstream`: issue, PR, email, or submission URL is recorded.
- `under review`: external actor has acknowledged or the PR/submission remains open.
- `merged`: external repository or destination accepted the contribution.
- `declined`: external actor declined or replaced the contribution.
- `blocked by external actor`: no further local action can advance the item.
- `superseded`: later approved plan makes the item unnecessary.

## Project Configuration Applied

- Added `external/ADOPTION_STATUS.md` as the repo-local adoption ledger for staged and submitted upstream work.
- Added labels for Conductor tracks, next-generation roadmap work, external gates, CI-required work, human gates, repo-boundary work, adoption, contracts, validation harnesses, service demos, comparative studies, releases, and GitHub project coordination.
- Added all active roadmap issues to the project.
- Set active roadmap issue project status to `Todo`.
- Set completed prior-track project items to `Done`.
- Attached issues #7-#13 as native sub-issues under #6.
- Added issue dependencies for true downstream blockers:
  - #10 is blocked by #9.
  - #12 is blocked by #8, #10, and #11.
  - #13 is blocked by #9 and #11.

## Recommended Project Views

These views should be maintained in GitHub Projects:

- `Roadmap hierarchy`: table view grouped or filtered by parent issue, with `Parent issue` and `Sub-issues progress` visible.
- `External gates`: filtered by `external-gate` or `human-gate`.
- `CI and PR readiness`: filtered by `ci-required`.
- `By milestone`: grouped by the `Next-generation roadmap` milestone.
- `Review queue`: filtered by linked PRs, reviewers, and labels requiring Dylan review.

## Operating Boundary

GitHub Projects is the visibility layer, not the requirements source. Update the local Conductor plan first, then mirror status, evidence links, PRs, and external blockers to the matching GitHub issue.
