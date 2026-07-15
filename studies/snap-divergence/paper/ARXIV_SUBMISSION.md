# arXiv submission packet — SNAP divergence study

**Status:** **submission candidate v0.3.0** (2026-07-15) — **do not submit** without explicit human authorization.
**GitHub issue:** [#16](https://github.com/edithatogo/rac-conformance/issues/16)  
**Unified project:** [arXiv and preprint papers](https://github.com/users/edithatogo/projects/20)  
**Source draft:** [`paper.md`](paper.md)  
**Author block:** [`../../../papers/AUTHOR.md`](../../../papers/AUTHOR.md)

**Programme package:** [`../../../papers/SUBMISSION_CANDIDATE_V0.3.0.md`](../../../papers/SUBMISSION_CANDIDATE_V0.3.0.md)

## Proposed metadata

| Field | Value |
|---|---|
| Title | Independent Rules-as-Code Implementation Agreement and Divergence Study: SNAP Eligibility and Allotments in PolicyEngine and the Policy Rules Database (PRD) |
| Authors | Dylan A Mordaunt |
| ORCID | https://orcid.org/0000-0002-9775-0603 |
| Affiliations | (1) Faculty of Health, Education and Psychology, Victoria University of Wellington; (2) College of Medicine and Public Health, Flinders University; (3) Centre for Health Policy, The University of Melbourne |
| Email | **none** (do not include) |
| License | CC-BY-4.0 for the paper text; study code Apache-2.0 |
| Primary category | `cs.CY` |
| Cross-lists (optional) | `cs.SE`; later venue candidate IJM |
| Comments | Companion empirical study to the PIC coupling paper. Fixtures: 50 human-promoted agreement cases (2026-07-06). |

## Abstract (paste into arXiv when authorized)

Rules-as-Code (RaC) promises to improve the precision, transparency, and consistency of public benefits programs by translating statutory and regulatory texts into executable code. However, a critical question remains: do independent implementations of the same legislative rules yield identical results? This paper presents a systematic, differential-testing evaluation of two leading RaC engines—PolicyEngine (Python) and the Atlanta Fed Policy Rules Database (PRD, R)—implementing the Supplemental Nutrition Assistance Program (SNAP) for Federal Fiscal Year 2026. Testing against a corpus of 65 human-curated and AI-proposed scenarios across five states (California, Texas, Pennsylvania, Mississippi, and Georgia) reveals a 100% output agreement rate (50 out of 50) for core compliance scenarios. For the remaining 15 held cases, we document and classify structural differences in state-option modeling, utility deduction triggers, and parameter surfaces.

## Artifact links

- Study root: https://github.com/edithatogo/rac-conformance/tree/main/studies/snap-divergence
- Golden fixtures: `studies/snap-divergence/fixtures/snap-fy2026-fixtures.json` (human-promoted 2026-07-06)
- Report: `studies/snap-divergence/REPORT.md`
- DBN outreach draft: `external/dbn/EMAIL.md`

## Preparation checklist (agents may complete; submit is human-only)

1. [x] Author byline + ORCID + affiliations (no email)
2. [x] Abstract and category proposal recorded
3. [ ] Convert to arXiv-acceptable PDF when Dylan requests
4. [ ] **Submit** — blocked until explicit authorization

## Decision log

| Date | Decision | By |
|---|---|---|
| 2026-07-09 | Packet prepared | Agent |
| 2026-07-09 | **Defer** arXiv submission; keep preparing | Dylan |
