# Maintainer response monitoring

Last checked: **2026-07-11** (blocker pass: PE coverage tests; rulespec-nz signing still external).

Bot / author-only comments do **not** count as maintainer replies.

| Target | URL | State | Implementation | Maintainer reply? | Next action |
|---|---|---|---|---|---|
| rulespec-nz KiwiSaver compile | https://github.com/TheAxiomFoundation/rulespec-nz/issues/79 | open | [PR #80](https://github.com/TheAxiomFoundation/rulespec-nz/pull/80) — compile OK; **hard-blocked** on `AXIOM_ENCODE_APPLY_SIGNING_KEY` | No | Maintainer must `sign-applied-files` / re-encode |
| PE trace export | https://github.com/PolicyEngine/policyengine-core/issues/512 | open | [PR #515](https://github.com/PolicyEngine/policyengine-core/pull/515) — rebased + extra `to_trace` tests (2026-07-11) | No | Await Codecov / review |
| PE missingness | https://github.com/PolicyEngine/policyengine-core/issues/513 | open | [PR #516](https://github.com/PolicyEngine/policyengine-core/pull/516) — rebased + `is_input` edge tests (2026-07-11) | No | Await Codecov / review |
| PE YAML converter | https://github.com/PolicyEngine/policyengine-core/issues/514 | open | [PR #517](https://github.com/PolicyEngine/policyengine-core/pull/517) docs | No | Review |
| OF missingness | https://github.com/openfisca/openfisca-core/issues/1380 | open | [PR #1382](https://github.com/openfisca/openfisca-core/pull/1382) | No | Review |
| OF YAML converter | https://github.com/openfisca/openfisca-core/issues/1381 | open | External tool only | No | Maintainer direction |
| Alaveteli state taxonomy | https://github.com/mysociety/alaveteli/issues/9355 | open | [PR #9356](https://github.com/mysociety/alaveteli/pull/9356) | No | Review |
| foi-o OIA rules + wiring | https://github.com/edithatogo/foi-o/pull/20 | **merged** | Also [#21](https://github.com/edithatogo/foi-o/pull/21) merged | N/A | None |
| openfisca-aotearoa coverage | https://github.com/BetterRules/openfisca-aotearoa/issues/199 | open | [PR #200](https://github.com/BetterRules/openfisca-aotearoa/pull/200) — empty commit to re-trigger checks (2026-07-11) | No | Review |
| DBN CoP email | `external/dbn/EMAIL.md` | sent | n/a | No new evidence | Monitor / optional follow-up |

## Hard external blockers (cannot clear from this agent)

1. **`AXIOM_ENCODE_APPLY_SIGNING_KEY`** for [rulespec-nz#80](https://github.com/TheAxiomFoundation/rulespec-nz/pull/80). Fork SoT remains `edithatogo/rulespec-nz` @ `fix/kiwisaver-elective-rates-map` (see `external/FORK_LOCAL_STATUS.md`).

## Local demo / publication follow-through (this repo)

| Item | Path | Status |
|---|---|---|
| Docassemble OIA interview package | `demos/docassemble-oia-clock/` | Added 2026-07-09 |
| Coupling arXiv packet | `papers/coupling/ARXIV_SUBMISSION.md` | **Deferred** ([#15](https://github.com/edithatogo/rulesandprocesses/issues/15)) | Prepare only |
| SNAP arXiv packet | `studies/snap-divergence/paper/ARXIV_SUBMISSION.md` | **Deferred** ([#16](https://github.com/edithatogo/rulesandprocesses/issues/16)) | Prepare only |
| Unified papers project | https://github.com/users/edithatogo/projects/20 | Active | Ledger for pending/completed preprints |

## Protocol

- Do not mark `merged` / `declined` without URL evidence.
- Re-run this table when Dylan requests a status pass or after known maintainer activity.
- Do not open additional proposals on a repo while an unresolved PR/issue from this program is still open.
