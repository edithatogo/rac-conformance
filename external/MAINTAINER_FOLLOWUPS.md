# Maintainer follow-up packets

Last prepared: **2026-07-11**.

This file is a contributor-controlled preparation artifact. It does not imply
that any upstream maintainer has approved, reviewed, signed, or merged a
contribution.

## Follow-up sequence

| Target | Prepared action | Required external actor | Evidence to record |
|---|---|---|---|
| PolicyEngine #515-#517 | Ask a maintainer to approve fork workflows, then request review of the addressed comments | PolicyEngine maintainer | Actions run IDs, review decision, merge/decline URL |
| OpenFisca #1382 | Request maintainer review and upstream CI confirmation | OpenFisca maintainer | Review URL, check URLs, merge/decline URL |
| Alaveteli #9356 | Ask whether the intended scope is documentation-only or the request-state hook, then run the agreed suite | Alaveteli maintainer | Scope decision, test output, review/merge URL |
| RuleSpec NZ #80 | Request `sign-applied-files` using the authorized Axiom signing key | Axiom key holder/maintainer | Signed manifest commit, validation check, merge/decline URL |
| OpenFisca Aotearoa #200 | Request maintainer review and CI confirmation | BetterRules maintainer | Review URL, check URLs, merge/decline URL |

## Follow-up protocol

1. Use the existing upstream issue or pull request; do not open a duplicate.
2. Include the exact local evidence path and the current upstream URL.
3. Request one concrete action only: workflow approval, review, signing, scope
   decision, or merge disposition.
4. Refresh `external/UPSTREAM_PR_AUDIT.md` and
   `external/MAINTAINER_MONITORING.md` only after URL evidence exists.
5. Keep Project 19 status `In Progress` until each contribution has a terminal
   disposition.

## Human gate

Sending these follow-ups is `[HUMAN]`. Agents may prepare and update this
packet, but must not post comments, approve workflows, supply credentials, or
merge external contributions.
