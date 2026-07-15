# Maintainer response monitoring

Last checked: **2026-07-15** (live PR sweep: no unresolved contribution reached a terminal upstream outcome; Alaveteli remains closed without merge; RaC Conformance preparation PRs #80 and #81 merged; RuleSpec NZ still has failed hosted validation and `CHANGES_REQUESTED`).

Bot / author-only comments do **not** count as maintainer replies.

| Target | URL | State | Implementation | Maintainer reply? | Next action |
|---|---|---|---|---|---|
| rulespec-nz KiwiSaver compile | https://github.com/TheAxiomFoundation/rulespec-nz/issues/79 | open | [PR #80](https://github.com/TheAxiomFoundation/rulespec-nz/pull/80) — `CHANGES_REQUESTED`; hosted `validate / validate` and `validate / validate (nz)` fail; local compile/Ruff/270-test evidence remains separate; **hard-blocked** on `AXIOM_ENCODE_APPLY_SIGNING_KEY` | No resolving maintainer action | Contributor may diagnose and stage any source-controlled fix; maintainer must approve workflows, provide signing, authorize the hosted re-run, and review/merge or decline |
| PE trace export | https://github.com/PolicyEngine/policyengine-core/issues/512 | open | [PR #515](https://github.com/PolicyEngine/policyengine-core/pull/515) — contributor follow-up posted 2026-07-15 addressing structured `TraceNode` fields and v1 documentation; no hosted checks | Yes (Max COMMENTED; follow-up addressed; workflow approval still pending) | Maintainer approves fork workflows, re-reviews, and merges/declines |
| PE missingness | https://github.com/PolicyEngine/policyengine-core/issues/513 | open | [PR #516](https://github.com/PolicyEngine/policyengine-core/pull/516) — contributor follow-up posted 2026-07-15 addressing visible-branch reuse and value-state documentation; no hosted checks | Yes (Max COMMENTED; follow-up addressed; workflow approval still pending) | Maintainer approves fork workflows, re-reviews, and merges/declines |
| PE YAML converter | https://github.com/PolicyEngine/policyengine-core/issues/514 | open | [PR #517](https://github.com/PolicyEngine/policyengine-core/pull/517) — contributor follow-up posted 2026-07-15 addressing source-code links and docs-build confirmation; no hosted checks | Yes (Max COMMENTED; follow-up addressed; workflow approval still pending) | Maintainer approves fork workflows, re-reviews, and merges/declines |
| OF missingness | https://github.com/openfisca/openfisca-core/issues/1380 | open | [PR #1382](https://github.com/openfisca/openfisca-core/pull/1382) | No (nudge 2026-07-11) | Await review |
| OF YAML converter | https://github.com/openfisca/openfisca-core/issues/1381 | open | External tool only | No | Maintainer direction |
| Alaveteli state taxonomy | https://github.com/mysociety/alaveteli/issues/9355 | **closed; PR not merged** | [PR #9356](https://github.com/mysociety/alaveteli/pull/9356) — closed 2026-07-13; CI passed before closure | No maintainer rationale recorded | Record externally closed/declined; do not reopen or resubmit without direction |
| foi-o OIA rules + wiring | https://github.com/edithatogo/foi-o/pull/20 | **merged** | Also [#21](https://github.com/edithatogo/foi-o/pull/21) merged | N/A | None |
| openfisca-aotearoa coverage | https://github.com/BetterRules/openfisca-aotearoa/issues/199 | open | [PR #200](https://github.com/BetterRules/openfisca-aotearoa/pull/200) | No (nudge 2026-07-11; empty check rollup) | Await BetterRules review / CI confirmation |
| DBN CoP email | `external/dbn/EMAIL.md` | sent | Follow-up draft: `external/dbn/FOLLOWUP.md` | No new evidence | `[HUMAN]` send follow-up if desired |

## Hard external blockers (cannot clear from this agent)

1. **`AXIOM_ENCODE_APPLY_SIGNING_KEY`** for [rulespec-nz#80](https://github.com/TheAxiomFoundation/rulespec-nz/pull/80) — asked [@MaxGhenis](https://github.com/MaxGhenis) to `sign-applied-files` on the PR branch. Fork SoT remains `edithatogo/rulespec-nz` @ `fix/kiwisaver-elective-rates-map`.
2. **First-time fork workflow approval** on PolicyEngine PRs #515–#517 (empty check rollup until a maintainer approves Actions).

3. **Maintainer review and hosted CI** remain unresolved for OpenFisca #1382
   (`REVIEW_REQUIRED`) and OpenFisca Aotearoa #200 (`REVIEW_REQUIRED`); neither
   has a contributor-controlled action that can produce an upstream outcome.

## Local demo / publication follow-through (this repo)

| Item | Path | Status |
|---|---|---|
| Docassemble OIA interview package | `demos/docassemble-oia-clock/` | Added 2026-07-09 |
| Coupling arXiv packet | `papers/coupling/ARXIV_SUBMISSION.md` | **Deferred** ([#15](https://github.com/edithatogo/rac-conformance/issues/15)) | Prepare only |
| SNAP arXiv packet | `studies/snap-divergence/paper/ARXIV_SUBMISSION.md` | **Deferred** ([#16](https://github.com/edithatogo/rac-conformance/issues/16)) | Prepare only |
| Unified papers project | https://github.com/users/edithatogo/projects/20 | Active | Ledger for pending/completed preprints |

| Dependabot CodeQL v4 update | https://github.com/edithatogo/rac-conformance/pull/27 | **Merged**; all required checks passed | None |

## Protocol

- Do not mark `merged` / `declined` without URL evidence.
- Re-run this table when Dylan requests a status pass or after known maintainer activity.
- Do not open additional proposals on a repo while an unresolved PR/issue from this program is still open.
