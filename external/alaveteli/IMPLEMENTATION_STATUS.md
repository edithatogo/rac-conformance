# Alaveteli #9355 — implementation status

**Date:** 2026-07-09  
**Upstream issue:** https://github.com/mysociety/alaveteli/issues/9355  
**Upstream PR:** https://github.com/mysociety/alaveteli/pull/9356  
**Issue comment:** https://github.com/mysociety/alaveteli/issues/9355#issuecomment-4920684381  
**Fork branch:** https://github.com/edithatogo/alaveteli/tree/9355-request-state-taxonomy-hooks  

## Outcome

Opened a **minimal, reviewable PR** against `mysociety/alaveteli` `develop` (not a core rewrite).

### Delivered

1. **`doc/REQUEST-STATES.md`** — state taxonomy for theme authors and statutory-clock consumers (described vs calculated layers; process/platform/admin/calculated roles; existing `customstates` extension; informative external mapping table).
2. **`InfoRequest::State.roles` / `role_for`** — programmatic role classification (no behaviour change).
3. **`InfoRequest#process_clock_metadata`** — optional theme hook (`theme_process_clock_metadata`); when non-empty, included in `json_for_api` as `process_clock_metadata`.
4. Specs for roles + metadata hook.
5. Design summary comment on #9355 linking the PR.

### Explicitly not done (by design)

- No database migration / no `jsonb` column on `info_requests` (theme-computed hash keeps multi-site schema stable; column can come later if maintainers want persistence).
- No change to default UX states, transitions, or labels.
- No jurisdiction-specific (e.g. NZ OIA) enum encoded in core.
- Full Alaveteli RSpec suite not executed locally (no app DB stack); syntax-checked with Ruby 3.x; new examples added for CI.

## Local workspace notes

- Clone used for the PR: `/Volumes/PortableSSD/GitHub/alaveteli` (shallow fork of `edithatogo/alaveteli`, branch `9355-request-state-taxonomy-hooks`).
- Proposal packet remains: `external/alaveteli/SUBMISSION.md`.

## Next actions (human / maintainer)

- [ ] Monitor PR #9356 for review feedback.
- [ ] If maintainers want docs-only, drop the Ruby hook commits and keep `doc/REQUEST-STATES.md`.
- [ ] If maintainers want persistence, follow up with optional `jsonb` column feeding the same `process_clock_metadata` method.
