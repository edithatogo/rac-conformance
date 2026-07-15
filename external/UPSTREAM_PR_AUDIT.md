# Upstream pull request quality audit

Last verified: 2026-07-15.

## Audit standard

Every contribution must have a corresponding issue, focused problem statement, explicit scope and non-goals, reproducible verification, compatibility/risk notes, a concrete reviewer ask, and honest CI status. Issue and PR URLs must both appear in GitHub Project 19. External review, workflow approval, signing, and merge remain maintainer gates.

| PR | Issue linkage | Project | Current state | Remaining action |
|---|---|---|---|---|
| PolicyEngine [#515](https://github.com/PolicyEngine/policyengine-core/pull/515) | Closes [#512](https://github.com/PolicyEngine/policyengine-core/issues/512) | Both In Progress | Externally blocked: maintainer reviewed with follow-up suggestions, while first-time fork workflow approval is still required and no hosted checks are reported | Address review comments as applicable; maintainer approves CI, re-reviews, and merges/declines |
| PolicyEngine [#516](https://github.com/PolicyEngine/policyengine-core/pull/516) | Closes [#513](https://github.com/PolicyEngine/policyengine-core/issues/513) | Both In Progress | Externally blocked: maintainer reviewed with follow-up suggestions, while first-time fork workflow approval is still required and no hosted checks are reported | Address review comments as applicable; maintainer approves CI, re-reviews, and merges/declines |
| PolicyEngine [#517](https://github.com/PolicyEngine/policyengine-core/pull/517) | Closes [#514](https://github.com/PolicyEngine/policyengine-core/issues/514) | Both In Progress | Externally blocked: maintainer reviewed with follow-up suggestions, while first-time fork workflow approval is still required and no hosted checks are reported | Address review comments as applicable; maintainer approves CI, re-reviews, and merges/declines |
| OpenFisca [#1382](https://github.com/openfisca/openfisca-core/pull/1382) | Fixes [#1380](https://github.com/openfisca/openfisca-core/issues/1380) | Both In Progress | Externally blocked: maintainer review is required and no hosted checks are reported | Maintainer reviews, confirms CI, and merges/declines |
| Alaveteli [#9356](https://github.com/mysociety/alaveteli/pull/9356) | References [#9355](https://github.com/mysociety/alaveteli/issues/9355) | Closed, not merged | Proposal and implementation PR closed by upstream on 2026-07-13; all triggered checks passed, but no merge occurred | No contributor action; retain as closed/declined unless maintainer reopens |
| RuleSpec NZ [#80](https://github.com/TheAxiomFoundation/rulespec-nz/pull/80) | Closes [#79](https://github.com/TheAxiomFoundation/rulespec-nz/issues/79) | Both In Progress | `CHANGES_REQUESTED`; hosted `validate / validate` and `validate / validate (nz)` fail while shard, roadmap, and quality checks pass; a signing key is still required; local compile/Ruff/270-test evidence is not upstream CI | Contributor may diagnose and stage any source-controlled fix; maintainer must approve workflows, provide signing, authorize the hosted re-run, and review/merge or decline |
| OpenFisca Aotearoa [#200](https://github.com/BetterRules/openfisca-aotearoa/pull/200) | Closes [#199](https://github.com/BetterRules/openfisca-aotearoa/issues/199) | Both In Progress | Externally blocked: maintainer review is required and no hosted checks are reported | Maintainer reviews, confirms CI, and merges/declines |

## Boundaries

- Empty check rollups are not passes.
- Local test evidence does not replace upstream CI.
- No maintainer approval, signing credential, or merge is inferred from contributor evidence.
- Project status `In Progress` means submitted and unresolved, not accepted upstream.
