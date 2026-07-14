# Shared citation and evidence ledger

Status: working ledger for the paper-completion track. Every manuscript claim must point to one or more rows and to a committed artifact where applicable.

| ID | Source | Role | Used by | Verification boundary |
|---|---|---|---|---|
| SRC-OIA-01 | https://www.legislation.govt.nz/act/public/1982/0156/latest/DLM65314.html | New Zealand Official Information Act text and definitions | Coupling paper | Primary legislation; effective text must be checked for the claimed date |
| SRC-IRD-01 | https://www.ird.govt.nz/income-tax/income-tax-for-individuals/tax-codes-and-tax-rates-for-individuals/tax-rates-for-individuals | NZ individual income-tax rates | NZ reconciliation | Official agency source; rates are time-varying |
| SRC-IRD-02 | https://www.ird.govt.nz/income-tax/income-tax-for-individuals/acc-clients-and-carers/acc-earners-levy-rates | NZ ACC earners levy | NZ reconciliation | Official agency source; rates and caps are time-varying |
| SRC-IRD-03 | https://www.ird.govt.nz/kiwisaver/kiwisaver-changes | NZ KiwiSaver rate changes | NZ reconciliation | Official agency source; eligibility and contribution scope remain limited |
| SRC-PE-01 | https://github.com/PolicyEngine/policyengine-taxsim | Independent differential-testing precedent | Coupling, SNAP | Public project description; not evidence for the study's numerical results |
| SRC-PRD-01 | https://github.com/Research-Division/policy-rules-database | PRD implementation and provenance boundary | SNAP | Upstream repository revision must be recorded for reruns |
| SRC-FNS-01 | https://www.fns.usda.gov/snap/eligibility | SNAP programme eligibility context | SNAP | Official federal source; state options require separate sources |
| SRC-RULESPEC-01 | https://github.com/TheAxiomFoundation/rulespec-nz | RuleSpec source and upstream compile gate | NZ reconciliation | Commit and manifest state are part of reproducibility |
| SRC-OF-AO-01 | https://github.com/BetterRules/openfisca-aotearoa | OpenFisca Aotearoa source and coverage boundary | NZ reconciliation | Package revision and dependency compatibility must be recorded |
| SW-FOIO-01 | https://github.com/edithatogo/foi-o; `CITATION.cff`; v0.8.0 | FOI-O ontology, schemas, V2 extraction contract, and process model | All FOI papers | Cite the exact release tag and SHA; Zenodo DOI is pending human deposit |
| SW-FYICLI-01 | https://github.com/edithatogo/fyi-cli; `CITATION.cff`; v1.1.0 | Capture client used to obtain FYI request records | Coupling, archive methods | Cite the exact release tag and SHA; Zenodo DOI is pending human deposit |
| DATA-FYIARCHIVE-01 | https://github.com/edithatogo/fyi-archive; `CITATION.cff`; v0.11.1 | Immutable archive/orchestration and WARC/WACZ distribution layer | Coupling, archive methods | DOI `10.5281/zenodo.21338285` resolves to published Zenodo record version `0.1.0`, not current repository version `0.11.1`; Hugging Face `edithatogo/fyi-archive-nz@fc27bfa471c598a31d975cfa2b603b1a11408e55`, artifact `manifests/latest_manifest.parquet`, SHA-256 `fd5f54be6b94390dce93b4662fc393c855d87569ff70eaf5411c365d0cbca678`; pinned provenance records a dirty source checkout and missing declared split files |
| SW-NLP-NZ-01 | https://github.com/edithatogo/nlp-policy-nz; `CITATION.cff`; v0.1.0 | NLP/NER adapter and derived annotation pipeline | Coupling, archive methods | Cite exact release tag and SHA; Zenodo and Hugging Face revisions remain human-gated |
| SW-LEGISLATION-01 | https://github.com/edithatogo/legislation; `CITATION.cff`; v1.2.0 | Authoritative NZ/Australian legislation retrieval provider | Legal methods and jurisdiction profiles | Cite exact release tag and SHA; Zenodo DOI is pending human deposit |
| SW-RAC-01 | https://github.com/edithatogo/rac-conformance; `CITATION.cff`; v0.2.0 | Policy-interchange conformance and evidence harness | Methods and reproducibility | Cite exact release tag and SHA; Zenodo DOI is pending human deposit |
| SW-FOIPROCESS-01 | https://github.com/edithatogo/foi-process; `CITATION.cff`; v0.1.0 | Deterministic FOI integration, replay, OCEL/process projections, and provenance | Integration and process-methods evidence | Zenodo version DOI [`10.5281/zenodo.21359526`](https://doi.org/10.5281/zenodo.21359526), concept DOI [`10.5281/zenodo.21359525`](https://doi.org/10.5281/zenodo.21359525), verified 2026-07-15 against GitHub release `v0.1.0` at commit `2e635115f61e24d2e109d868119024a5591cce00`; FOI-O remains semantic authority |
| SRC-ALAVETELI-01 | https://github.com/mysociety/alaveteli | Upstream workflow/source intelligence for public FOI request registers | Archive methods | Read-only workflow precedent only; not presented as an included implementation or dataset |

## Claim rules

- A source supports the proposition stated, not a stronger adjacent proposition.
- A secondary source cannot support a confirmed legal or engine-bug claim when a primary source is required.
- Time-varying sources require an effective date in the artifact or the claim is marked unresolved.
- Engine agreement is not an independent legal oracle.

## Quality and extraction evidence

The cross-repository quality register is committed at
`papers/foi-programme-quality-evidence.json`. It pins the local heads and
records stable lanes, Python/spaCy canaries, dependency and type baselines,
SBOM/provenance boundaries, and the deferred V2 extraction re-extraction gate.
It is evidence of repository-local checks only; it does not assert Zenodo,
Hugging Face, upstream merge, or extraction-accuracy publication status.
