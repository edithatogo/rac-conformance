# New Zealand Rules-as-Code Coverage Gaps: RuleSpec and OpenFisca Aotearoa

**Author:** Dylan A Mordaunt  
**ORCID:** [0000-0002-9775-0603](https://orcid.org/0000-0002-9775-0603)  
**Status:** submission candidate v0.3.0; human authorization pending
**Evidence track:** `nz_reconciliation_20260707`, `nz_recon_live_20260709`

## Abstract

Comparative rules-as-code studies can fail before numerical comparison when the selected engines do not expose the same policy surfaces. We examine a 17-case inventory spanning New Zealand individual schedule income tax, ACC earners' levy, and KiwiSaver contributions in a RuleSpec implementation and OpenFisca Aotearoa. A live dual-engine rerun produced 10 numeric agreements within a NZD 0.02 tolerance and seven remaining engine gaps. The agreements cover selected income-tax, standard earners' levy, and minimum KiwiSaver cases; the gaps cover self-employed ACC surfaces and the KiwiSaver government-contribution cap. The contribution is methodological: report coverage and model-surface compatibility before interpreting differential outputs.

## 1. Introduction

Differential testing assumes that two implementations expose comparable decisions, parameters, periods, and outputs. In public-policy software that assumption is often false: packages may model different years, variables, or administrative pathways. A zero-agreement result is therefore uninterpretable unless coverage gaps are measured separately.

## 2. Materials and methods

The inventory contains 17 cases: five income-tax cases, nine ACC earners' levy cases, and three KiwiSaver cases. The RuleSpec side uses companion fixtures and the pinned Axiom validation harness. The OpenFisca Aotearoa side uses a live simulation on the PR branch, with the static probe retained as historical context. Results are classified as `agreement` or `engine_gap` before any claim about parity is made.

The source and effective-date boundary is maintained in [`papers/CITATION_LEDGER.md`](../../../papers/CITATION_LEDGER.md). Reproduction artifacts are listed in [`results/DIVERGENCE_REPORT.md`](../results/DIVERGENCE_REPORT.md) and the runner tests. The study does not invent missing OpenFisca formulas and does not treat RuleSpec output as a legal oracle.

## 3. Results

RuleSpec produced 17 usable oracle rows and OpenFisca Aotearoa produced 10 live comparable rows. Ten cases agreed within NZD 0.02: five income-tax cases, three standard earners' levy cases, and two minimum KiwiSaver cases. Seven cases remained `engine_gap`: five self-employed/weekly-compensation ACC cases and one each for the KiwiSaver government-contribution cap and related non-overlapping surface. The live report records the exact case IDs and evidence files. The RuleSpec compile fix is tracked in [rulespec-nz#79](https://github.com/TheAxiomFoundation/rulespec-nz/issues/79).

## 4. Discussion

The study demonstrates a precondition gate for cross-engine research: establish policy-vintage and surface overlap before computing agreement rates. Ten agreements provide a bounded parity result for selected surfaces, while seven coverage gaps remain findings about package scope and maintenance, not evidence that either engine's formulas are wrong. The result also provides a constructive upstream request, [openfisca-aotearoa#199](https://github.com/BetterRules/openfisca-aotearoa/issues/199), and a potential follow-up if maintainers add the missing surfaces.

## Data and code availability

Fixtures, static probes, candidate results, live results, compiled RuleSpec artifacts, runner tests, the live dual-engine report, and the certified human review are committed under `studies/nz-reconciliation/`. Repository validation is run by `make check`; live engine reruns require the recorded third-party revisions and compatible runtimes.

## Limitations

This is a purposive 17-case inventory, not a population sample. It does not measure legal correctness, engine quality, or agreement outside the jointly implemented cases. The live OpenFisca run used the contributor PR branch and Python 3.11 with the 41.x core line; the default package and modern-Python environment had compatibility limitations. Rates and statutory interpretations are time-varying and require refresh before publication. The certified result combines bounded parity for 10 cases with seven documented coverage gaps.

## 5. Conclusion

Cross-engine comparison should fail closed when the engines do not share a policy surface. Separating 10 bounded numeric agreements from seven `engine_gap` cases prevented an invalid claim of universal parity and produced actionable upstream work.
