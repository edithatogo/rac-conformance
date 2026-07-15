# arXiv submission packet — coupling paper

**Status:** **submission candidate v0.3.0** (2026-07-15) — **do not submit** without explicit human authorization.
**GitHub issue:** [#15](https://github.com/edithatogo/rac-conformance/issues/15)  
**Unified project:** [arXiv and preprint papers](https://github.com/users/edithatogo/projects/20)  
**Source draft:** [`paper.md`](paper.md)  
**Author block:** [`../AUTHOR.md`](../AUTHOR.md)

**Programme package:** [`../SUBMISSION_CANDIDATE_V0.3.0.md`](../SUBMISSION_CANDIDATE_V0.3.0.md)

## Proposed metadata

| Field | Value |
|---|---|
| Title | Coupling Statutory Rules and Administrative Processes: A Pragmatic Contract-Based Approach to Rules-as-Code |
| Authors | Dylan A Mordaunt |
| ORCID | https://orcid.org/0000-0002-9775-0603 |
| Affiliations | (1) Faculty of Health, Education and Psychology, Victoria University of Wellington; (2) College of Medicine and Public Health, Flinders University; (3) Centre for Health Policy, The University of Melbourne |
| Email | **none** (do not include) |
| License | CC-BY-4.0 for the paper text; code/schemas Apache-2.0 (see repo `LICENSE`) |
| Primary category | `cs.CY` (Computers and Society) |
| Cross-lists (optional) | `cs.SE` |
| Comments | Draft companion paper to the SNAP divergence study and foi-o OIA rules module. |

## Abstract (paste into arXiv when authorized)

Rules-as-Code (RaC) initiatives typically focus on rules-heavy domains (such as tax-benefit calculations) or process-heavy domains (such as public record lifecycle tracking) in isolation. However, actual administrative operations require coupling these two surfaces. This paper presents a pragmatic, contract-based approach to coupling statutory rules and administrative processes. We define a lightweight Policy Interchange Contract (PIC) schema that acts as a boundary between process state machines (like foi-o for official information requests) and isolated rules modules. We evaluate this approach across two distinct case studies: Official Information Act (OIA) clocks in New Zealand, and a multi-state SNAP eligibility study. Our results demonstrate that decoupled rules modules can achieve 100% differential testing parity while maintaining strict import-graph isolation and preserving non-computable discretion points.

## Artifact links

- Repository: https://github.com/edithatogo/rac-conformance
- OIA rules consumer: https://github.com/edithatogo/foi-o (PRs #20, #21)
- SNAP study: `studies/snap-divergence/`
- Cite software: `CITATION.cff`

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
