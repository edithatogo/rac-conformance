# Health-technology comparison-case selection packet

Status: **ready for human selection; no case, jurisdiction pair, profile, or fixture is certified**.

This packet supports issue #42's human gate. Scores are evidence-readiness
scores from `candidates/COMPARISON_CASE_CANDIDATES.json`, not clinical,
therapeutic, cost-effectiveness, funding, or access recommendations.

## Ranked candidates

| Candidate | Jurisdictions available | Score | Main limitation |
| --- | --- | ---: | --- |
| `pembrolizumab-adjuvant-stage-iii-melanoma` | NZ, AU, UK, US | 24/30 | Pharmac wording, Australian restriction evidence, and temporal alignment require source-spine verification. |
| `pembrolizumab-advanced-melanoma` | NZ, AU, UK, US | 22/30 | NICE appraisal is older and has a different prior-treatment boundary. |
| `pembrolizumab-first-line-nsclc` | AU, UK, US | 21/30 | NZ evidence was not identified and the NICE/FDA indication boundaries differ. |

## Recommended first slice

Select `pembrolizumab-adjuvant-stage-iii-melanoma` and compare **NZ
Medsafe/Pharmac** with **UK MHRA/NICE**. This is the highest-scoring slice and
keeps the first implementation to two regulator-to-funder pathways with a
clear regulator/HTA/funder distinction. The Australian and US records remain
source material, not executable profile scope, unless separately selected.

The recommendation does not assert that the medicine is appropriate, funded,
cost-effective, or accessible. It compares publicly documented process
structure only. Confidential commercial arrangements, non-public deliberation,
and unverified current restrictions remain unavailable.

## Human response

Choose one of:

- approve the recommended candidate and NZ/UK pair;
- select a different candidate and name the jurisdiction pair;
- defer selection pending source retrieval; or
- record `no-selection` if no candidate has a defensible source spine.

Record the decision-maker, date, candidate ID, jurisdiction pair, source gaps
accepted, and excluded claims. Approval authorizes source verification and
candidate-profile implementation only; it does not authorize fixture promotion
or a clinical/funding conclusion.

The machine-readable candidate ledger remains the source of truth:
`subrepos/process-mappings/profiles/health-technology/candidates/COMPARISON_CASE_CANDIDATES.json`.
