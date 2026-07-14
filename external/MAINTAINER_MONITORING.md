# Maintainer response monitoring

Last checked: **2026-07-14** (Alaveteli proposal and PR closed without merge; local Dependabot PR #27 is current repository maintenance; rulespec-nz signing still external).

Bot / author-only comments do **not** count as maintainer replies.

| Target | URL | State | Implementation | Maintainer reply? | Next action |
|---|---|---|---|---|---|
| rulespec-nz KiwiSaver compile | https://github.com/TheAxiomFoundation/rulespec-nz/issues/79 | open | [PR #80](https://github.com/TheAxiomFoundation/rulespec-nz/pull/80) — conflict repaired at `7cafeb0`; compile/Ruff/270 tests OK; **hard-blocked** on `AXIOM_ENCODE_APPLY_SIGNING_KEY` | No (asked @MaxGhenis 2026-07-11) | Await Max re-sign / merge |
| PE trace export | https://github.com/PolicyEngine/policyengine-core/issues/512 | open | [PR #515](https://github.com/PolicyEngine/policyengine-core/pull/515) — Max review addressed (TraceNode fields + format notes) | Yes (Max COMMENTED 2026-07-09; follow-up pushed) | Max: approve fork workflows + re-review |
| PE missingness | https://github.com/PolicyEngine/policyengine-core/issues/513 | open | [PR #516](https://github.com/PolicyEngine/policyengine-core/pull/516) — Max review addressed (`_get_visible_branch_names`) | Yes (Max COMMENTED 2026-07-09; follow-up pushed) | Max: approve fork workflows + re-review |
| PE YAML converter | https://github.com/PolicyEngine/policyengine-core/issues/514 | open | [PR #517](https://github.com/PolicyEngine/policyengine-core/pull/517) — docs link to `test_runner.py` | Yes (Max COMMENTED 2026-07-09; follow-up pushed) | Max: approve fork workflows + re-review |
| OF missingness | https://github.com/openfisca/openfisca-core/issues/1380 | open | [PR #1382](https://github.com/openfisca/openfisca-core/pull/1382) | No (nudge 2026-07-11) | Await review |
| OF YAML converter | https://github.com/openfisca/openfisca-core/issues/1381 | open | External tool only | No | Maintainer direction |
| Alaveteli state taxonomy | https://github.com/mysociety/alaveteli/issues/9355 | **closed; PR not merged** | [PR #9356](https://github.com/mysociety/alaveteli/pull/9356) — closed 2026-07-13; CI passed before closure | No maintainer rationale recorded | Record externally closed/declined; do not reopen or resubmit without direction |
| foi-o OIA rules + wiring | https://github.com/edithatogo/foi-o/pull/20 | **merged** | Also [#21](https://github.com/edithatogo/foi-o/pull/21) merged | N/A | None |
| openfisca-aotearoa coverage | https://github.com/BetterRules/openfisca-aotearoa/issues/199 | open | [PR #200](https://github.com/BetterRules/openfisca-aotearoa/pull/200) | No (nudge 2026-07-11; empty check rollup) | Await BetterRules review / CI confirmation |
| DBN CoP email | `external/dbn/EMAIL.md` | sent | Follow-up draft: `external/dbn/FOLLOWUP.md` | No new evidence | `[HUMAN]` send follow-up if desired |

## Hard external blockers (cannot clear from this agent)

1. **`AXIOM_ENCODE_APPLY_SIGNING_KEY`** for [rulespec-nz#80](https://github.com/TheAxiomFoundation/rulespec-nz/pull/80) — asked [@MaxGhenis](https://github.com/MaxGhenis) to `sign-applied-files` on the PR branch. Fork SoT remains `edithatogo/rulespec-nz` @ `fix/kiwisaver-elective-rates-map`.
2. **First-time fork workflow approval** on PolicyEngine PRs #515–#517 (empty check rollup until a maintainer approves Actions).

## Local demo / publication follow-through (this repo)

| Item | Path | Status |
|---|---|---|
| Docassemble OIA interview package | `demos/docassemble-oia-clock/` | Added 2026-07-09 |
| Coupling arXiv packet | `papers/coupling/ARXIV_SUBMISSION.md` | **Deferred** ([#15](https://github.com/edithatogo/rac-conformance/issues/15)) | Prepare only |
| SNAP arXiv packet | `studies/snap-divergence/paper/ARXIV_SUBMISSION.md` | **Deferred** ([#16](https://github.com/edithatogo/rac-conformance/issues/16)) | Prepare only |
| Unified papers project | https://github.com/users/edithatogo/projects/20 | Active | Ledger for pending/completed preprints |

| Dependabot CodeQL v4 update | https://github.com/edithatogo/rac-conformance/pull/27 | Open; all checks pass; review required | Independent approval, then merge |

## Protocol

- Do not mark `merged` / `declined` without URL evidence.
- Re-run this table when Dylan requests a status pass or after known maintainer activity.
- Do not open additional proposals on a repo while an unresolved PR/issue from this program is still open.
