# Human Fixture Review: nz-oia-clocks

This packet is for Dylan's review. The fixtures in `fixtures.json` are candidate examples only and are not golden fixtures.

## Source Checks Performed

- Current Official Information Act 1982 text was checked on New Zealand Legislation on 2026-07-05.
- Section 2 working-day definition was checked for weekends, listed national holidays, observed Waitangi/Anzac Mondays, and the 25 December to 15 January exclusion.
- Section 14 was checked as the transfer source reference.
- Section 15 was checked as the decision-on-request source reference.
- Section 15A was checked as the extension source reference.
- `edithatogo/foi-o` README was checked on GitHub on 2026-07-05 for the exposed clock command, schema directory, process/event stance, epistemic-status semantics, and human-certification boundary.

## Candidate Fixtures

| Case | Purpose | Human checks needed |
|---|---|---|
| `nz-oia/fixture.response_deadline_plain` | Plain 20-working-day response deadline candidate. | Confirm counting convention and expected date `2026-03-02`. |
| `nz-oia/fixture.receipt_not_provided` | Missing receipt date should propagate unknown. | Confirm missingness behavior aligns with Track 2 foi-o design. |
| `nz-oia/fixture.receipt_verified_stale` | Stale receipt date should warn rather than certify a deadline. | Confirm `verified_stale` handling and warning semantics. |
| `nz-oia/fixture.transfer_deadline_plain` | Transfer notice candidate within 10 working days. | Confirm the transfer deadline interpretation from s 14. |
| `nz-oia/fixture.december_january_exclusion` | Deadline crossing 25 Dec to 15 Jan exclusion. | Confirm expected date `2027-02-11` against OIA s 2 and holiday calendar assumptions. |

## Promotion Steps

1. Verify each fixture against OIA text and Ombudsman guidance.
2. If accepted, change `provenance.method` from `ai-proposed` to `human`.
3. Replace `interpreterOfRecord: "pending Dylan review"` with the actual interpreter-of-record.
4. Record any rejected or amended fixture decisions in this file before Track 2 consumes the examples.

