# SNAP Fixture Candidate Packet

Track: `divergence_study_20260704`

Candidate file: `studies/snap-divergence/fixtures/candidates/snap-fy2026-candidates.json`

Crosswalk file: `studies/snap-divergence/crosswalk.json`

Validation command:

```sh
contracts/tools/.venv/bin/pic-validate studies/snap-divergence
```

## Status

The fixture corpus contains 65 AI-proposed candidates across the five scoped states: California, Texas, Pennsylvania, Mississippi, and Georgia.

The cases are not golden fixtures. They intentionally keep `expected` eligibility and allotment as `valueState: unknown` until the Phase 3 runners produce outputs and Dylan promotes selected cases.

## Coverage

- Baseline low-income cases.
- Gross-income threshold candidates around 130%, 165%, and 200% FPL surfaces.
- Net-income and excess-shelter candidates.
- Dependent-care deduction candidates.
- Elderly or disabled medical-expense and uncapped-shelter candidates.
- Asset-test candidates.
- Utility allowance and Heat-and-Eat candidates.

## Source Set

- USDA/FNA FY2026 SNAP maximum allotments, deductions, excess shelter cap, homeless shelter deduction, and asset limits.
- USDA/FNA SNAP eligibility and broad-based categorical eligibility pages.
- California CalFresh regulation/manual sources.
- Texas Works Handbook SNAP household, categorical eligibility, and utility/deduction sources.
- Pennsylvania SNAP Handbook and LIHEAP/Heat-and-Eat source.
- Mississippi SNAP manual source.
- Georgia SNAP policy manual source.

## Promotion Checklist

1. Run both Phase 3 runners for each candidate.
2. Replace `unknown` expected outputs only after runner evidence and source review.
3. Promote at least 40 cases to `fixtures/` with `method: human`.
4. Record rejected or changed candidates in the Phase 2 checkpoint.

## Promotion Review Packet

Generated review aid: `studies/snap-divergence/fixtures/FIXTURE_PROMOTION_REVIEW.md`.

Current recommendation after Phase 3 runner evidence:

- 50 agreement cases are recommended for human promotion.
- 15 divergence cases are held for Phase 4 source-level analysis.
- Dylan approval is still required before any candidate can become a golden fixture.

Approval record:

- Dylan approved the recommended 50 agreement cases on 2026-07-06.
- Promoted fixtures: `studies/snap-divergence/fixtures/snap-fy2026-fixtures.json`.
- Approved-fixture comparison evidence: `studies/snap-divergence/results/comparison-approved-results.jsonl`.
