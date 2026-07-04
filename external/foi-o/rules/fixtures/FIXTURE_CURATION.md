# Fixture Curation Packet

Track: `oia_rules_20260704`

Candidate file: `external/foi-o/rules/fixtures/candidates/oia-clock-candidates.json`

Crosswalk file: `external/foi-o/rules/crosswalk.json`

Validation command:

```sh
contracts/tools/.venv/bin/pic-validate external/foi-o/rules
```

## Human Review Required

The candidate fixtures are `method: ai-proposed` and must not be treated as golden fixtures until Dylan reviews them against:

- Official Information Act 1982 ss 2, 12(3), 14, 15, 15A, and 28.
- The source notes in `external/foi-o/rules/SOURCES.md`.
- Any Ombudsman guidance Dylan wants to treat as interpretive evidence.
- The exact public-holiday calendar that should be in force for the target years.

## Candidate Coverage

- Friday receipt before a Monday public holiday.
- Transfer deadline from the same Friday-before-holiday receipt date.
- Receipt during the 25 December to 15 January exclusion.
- Receipt immediately before the 25 December to 15 January exclusion.
- Missing receipt date propagation to `unknown`.
- Extension notice after original deadline.
- Extension with large-quantity ground.
- Extension with consultation ground.
- Extension with unrecognised ground.
- Transfer deadline crossing Anzac Day Mondayisation.
- Deemed refusal after deadline.
- No deemed refusal before deadline.
- Urgency reasons as a non-computable discretion point.

## Promotion Checklist

1. Confirm or correct each expected date and warning.
2. Confirm whether the candidate holiday calendar assumptions are sufficient for each case.
3. Move accepted cases from `rules/fixtures/candidates/` to the promoted fixture location used by the eventual upstream patch.
4. Change promoted provenance from `method: ai-proposed` to `method: human`.
5. Replace `interpreterOfRecord: pending Dylan review` with the actual reviewer identity.
6. Record any rejected or changed candidate cases in the Phase 2 checkpoint.
