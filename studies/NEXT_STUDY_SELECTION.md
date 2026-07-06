# Comparative Study Selection Report

This document records the evaluation, scoring, and selection of the next comparative tax-benefit microsimulation study to be integrated into the Policy Interchange Contracts (PIC) validation harness.

## Candidate Evaluation Matrix

| Candidate | Interest | Runtime Access | Oracle Availability | Source Burden | Maintainer Alignment | Novelty | **Total** |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **NZ RuleSpec vs OpenFisca Aotearoa** (Selected) | 9/10 | 10/10 | 10/10 | 9/10 | 9/10 | 8/10 | **55/60** |
| **US EITC/CTC Three-Way** (Reserve) | 10/10 | 8/10 | 7/10 | 8/10 | 8/10 | 9/10 | **50/60** |
| **UK PolicyEngine vs UKMOD** | 8/10 | 5/10 | 6/10 | 8/10 | 7/10 | 8/10 | **42/60** |
| **France OpenFisca vs LexImpact** | 8/10 | 7/10 | 6/10 | 5/10 | 7/10 | 8/10 | **41/60** |
| **SNAP State-Options Expansion** | 7/10 | 9/10 | 8/10 | 7/10 | 7/10 | 6/10 | **44/60** |

## Selection Reasoning

### Primary Recommendation: NZ RuleSpec vs OpenFisca Aotearoa (Reconciliation)
*   **Feasibility:** Both `rulespec-nz` and `openfisca-core` (plus Aotearoa rules) checkouts are already present locally.
*   **Oracle:** Excellent test suites and companion oracles are available in `rulespec-nz`.
*   **Source Burden:** English-language NZ legislation (Official Information Act, Income Tax Act) is readily available and mapped.

### Reserve Recommendation: US EITC/CTC Three-Way
*   **Feasibility:** Highly interesting but blocked by remote API/licensing constraints of NBER TAXSIM.

## Feasibility Smokes
- **NZ RuleSpec:** Verified that `rulespec-nz` integration tests pass successfully in 0.10s.
- **OpenFisca Aotearoa:** Core and Aotearoa rules packages are locally installed and runnable.

## Source & Oracle Assessment
- **Primary Sources:** NZ Income Tax Act 2007 (Part C and Part RD), Accident Compensation Act 2001 (Section 219).
- **Oracle Strategy:** Cross-engine validation using `rulespec-nz` YAML tests and OpenFisca Aotearoa execution traces.

