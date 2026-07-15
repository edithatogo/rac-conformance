# Independent Rules-as-Code Implementation Agreement and Divergence Study: SNAP Eligibility and Allotments in PolicyEngine and the Policy Rules Database (PRD)

**Author:** Dylan A Mordaunt  
**ORCID:** [0000-0002-9775-0603](https://orcid.org/0000-0002-9775-0603)  
**Affiliations:**
1. Faculty of Health, Education and Psychology, Victoria University of Wellington
2. College of Medicine and Public Health, Flinders University
3. Centre for Health Policy, The University of Melbourne

**Date:** July 2026  
**Track:** `divergence_study_20260704`  
**arXiv status:** submission candidate v0.3.0; authorization pending (see `ARXIV_SUBMISSION.md`; GitHub [#16](https://github.com/edithatogo/rac-conformance/issues/16))
**Author block:** [`papers/AUTHOR.md`](../../../papers/AUTHOR.md)

---

## Abstract
Independent executable models of the same public-benefit program provide an opportunity for differential testing, but agreement alone is not a legal oracle and disagreement is not automatically a software bug. We compare PolicyEngine-US (Python) and the Atlanta Fed Policy Rules Database (PRD, R) for selected Federal Fiscal Year 2026 Supplemental Nutrition Assistance Program (SNAP) scenarios in California, Texas, Pennsylvania, Mississippi, and Georgia. The corpus contains 65 provenance-labelled candidate scenarios. Fifty cases entered the approved comparison set and agreed on eligibility and allotment within the declared tolerance. Fifteen cases were held because state-option pathways, utility-deduction triggers, parameter vintages, or fixture assumptions were not directly aligned. A deterministic source-triangulation process assigns a proposed disposition or an explicit source-review exception to each held case. The study demonstrates a reproducible method for separating output disagreement, model-scope differences, adapter defects, and unresolved source questions; it does not estimate population error rates or establish either implementation as legally authoritative.

---

## 1. Introduction
Translating complex, natural-language statutes into machine-readable rules is an active area of research and civic technology. The Supplemental Nutrition Assistance Program (SNAP) is a particularly rich domain for validation because it combines federal baseline regulations with complex state-level options, including Broad-Based Categorical Eligibility (BBCE), Standard Utility Allowances (SUAs), and asset test thresholds.

To evaluate the reliability of RaC implementations, we differentially test two independent, open-source models:
1. **PolicyEngine-US**: A micro-simulation engine written in Python.
2. **Policy Rules Database (PRD)**: A policy database and simulation engine written in R.

Our study assesses:
- Output agreement rates (eligibility status and allotment amount).
- Root causes of divergence.
- The decision relevance of any observed discrepancies.

---

## 2. Methodology

### 2.1 Scope and Vintages
The study is restricted to the policy state as of **January 2026** (Federal FY2026). Five states were selected to cover key modeling dimensions:
- **California (CA)** and **Pennsylvania (PA)**: High-FPL, no-asset-test BBCE options.
- **Texas (TX)**: $5,000 asset limit and 165% gross FPL categorical eligibility.
- **Georgia (GA)**: No asset limit, but a restricted 130% gross FPL categorical limit.
- **Mississippi (MS)**: A traditional non-BBCE state applying federal asset tests ($3,000/$4,500).

### 2.2 Semantic Crosswalk
A unified `crosswalk.json` schema was designed to map inputs across the two systems:
- Household size, member ages, marital status, and disability.
- Monthly earned and unearned incomes.
- Housing expenses and utility bills.
- Countable liquid assets.

### 2.3 Fixture Corpus and Execution
We assembled 65 provenance-labelled candidate scenarios from source-backed boundary cases and model-surface probes.
- **Approved comparison set (50 cases)**: Retained in `results/comparison-approved-results.jsonl` after both runners yielded equivalent outputs within the declared tolerance and the fixture review gate was completed.
- **Divergences (15 cases)**: Held back for detailed code-level analysis and classification.

Two independent test runners were built:
- A Python situator calling `policyengine-us` (v1.755.5).
- An R bridge sourcing the PRD's `functions/benefits_functions.R` via `Rscript`.

---

## 3. Results

The comparison and exception-queue workflows are summarized in [`FIGURE_1_PIPELINE.md`](FIGURE_1_PIPELINE.md), [`FIGURE_2_EXCEPTION_QUEUE.md`](FIGURE_2_EXCEPTION_QUEUE.md), and [`ARTIFACT_SUMMARY.md`](ARTIFACT_SUMMARY.md).

### 3.1 Overall Agreement
Of the 65 scenarios executed, **50 cases (76.9%)** achieved complete agreement on both eligibility status and monthly allotment.
All 50 agreement fixtures are documented in `results/comparison-approved-results.jsonl`.

### 3.2 Divergence Classification
The remaining 15 cases (23.1%) were held back. All 15 were classified into three structural categories:

| Root Cause Category | Cases | Decision-Relevant | Description / Example |
|---|---:|---:|---|
| **State-Option Modeling** | 8 | 8 | Discrepancies in how state-specific BBCE rules are routed. Georgia gross-FPL limits (130%) and Texas vehicle/asset rules are modeled as direct SNAP limits in PRD, while PolicyEngine routes them via TANF non-cash eligibility tests. |
| **Deduction Handling** | 4 | 3 | Mismatches in utility allowance triggers. Pennsylvania automatic HSUA/LIHEAP triggers and Mississippi phone-only standard utility deductions are handled differently at the adapter interface level. |
| **Parameter Vintage** | 3 | 3 | Divergences in non-BBCE income thresholds (e.g., Mississippi FPL thresholds). |

Fourteen of the 15 divergences are decision-relevant (flipping eligibility or altering allotments by more than $10.00); the Mississippi phone-only utility allowance case is a smaller, non-decision-relevant adapter-surface difference. The classifications are proposed dispositions rather than a blanket finding that either engine is correct. Confirmed-bug labels require controlling primary or official source assertions; blocked, stale, conflicting, or secondary-only evidence is routed to further source review. This distinction prevents model disagreement from being converted into a bug claim without an independent evidentiary basis.

---

## 4. Discussion

The principal result is procedural. A comparison harness can make disagreements observable, but a source ledger and deterministic adjudication rules are needed to distinguish calculation defects from differences in scope, vintage, or fixture interpretation. The held-case queue is therefore part of the result rather than discarded noise.

## Data and code availability

The fixture candidates, approved comparison output, held divergences, source assertions, adjudication rules, runner code, environment manifests, and generated reports are committed under `studies/snap-divergence/`. Commands required to reproduce validation are documented in the study README and exercised by repository CI. Re-running the PRD side requires R and the pinned upstream revision; re-running PolicyEngine requires the recorded Python package versions.

## Limitations
- **Fixture coverage**: The 65 scenarios target selected boundaries and are not a probability sample. They cannot estimate prevalence or population-level error rates.
- **Adapter Assumptions**: Differences in monthly-to-annual income conversions (PRD calculates annually, PolicyEngine monthly) required normalizations that may introduce minor rounding variances.
- **Legislation Vintages**: State administrative options change rapidly; keeping parameter sheets synchronized is a continuous maintenance burden.
- **Oracle independence**: Agreement between the engines is supporting evidence, not proof of legal correctness. Source assertions and human certification remain necessary for controlling interpretations.
- **Generalisability**: Five states and selected rule surfaces do not represent the full SNAP program or other benefits programs.

---

## 5. Related Work

### 5.1 Model-to-Model Validation Precedents
This study builds upon PolicyEngine's prior TAXSIM validation work, which compares PolicyEngine's tax module against the NBER TAXSIM model. It also extends the Atlanta Fed PRD's validation suite.

### 5.2 Rules-as-Code Ontologies and Standards
Related efforts (such as OASIS LegalRuleML and W3C PROV-O) attempt to formalize legislative semantics. This study demonstrates that lightweight, JSON-based contract schemas (such as PIC) can successfully validate multi-engine implementations without the overhead of heavy RDF ontologies.

---

## 6. Conclusion
PolicyEngine and PRD agree across the 50-case approved comparison set, while 15 held cases expose meaningful differences in model pathways, assumptions, and source alignment. The result supports differential testing as a diagnostic method, not a claim of universal reliability. Combining deterministic comparison with provenance-labelled fixtures, primary-source assertions, and an explicit exception queue provides a more defensible quality-assurance process for public-benefit software.
