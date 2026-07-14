# Plan

- [x] Implement `foi-o` maximal quality profile. (local child track evidence captured; basedpyright and extraction-contract follow-ups remain explicit)
- [x] Implement `fyi-archive` maximal quality profile. (local child track evidence captured; basedpyright and dependency follow-ups remain explicit)
- [x] Complete `nlp-policy-nz` Python-runtime reconciliation and spaCy 4 spike. (Python 3.12 production; 3.11 compatibility; 3.13/3.14 canaries; spaCy 4 deferred)
- [x] Reconcile cross-repository release and extraction-contract evidence. (local heads, stable/canary decisions, and deferred re-extraction gate recorded)
- [x] Update the manuscript evidence ledger and release packet. (CITATION_LEDGER.md, FOI_PROGRAMME_RELEASE_PACKET.md, and Zenodo mirror manifest updated)

> CHECKPOINT (2026-07-14): Stable quality lanes and explicit canary results are
> recorded for foi-o, fyi-archive, and nlp-policy-nz. The release packet keeps
> basedpyright debt, dependency warnings, missing native wheels, pending V2
> re-extraction, Zenodo/Hugging Face pins, and manuscript submission as explicit
> boundaries rather than overstating readiness.

> FINAL CHECKPOINT (2026-07-14): `make check` passed on Python 3.14.6 across
> repository audit, 10 tool tests, paper artifacts, PIC schemas/examples,
> converters, harnesses, SNAP/NZ runners, service-boundary tests, and the
> Docassemble OIA clock demo. External publication and next-release
> re-extraction gates remain human/deferred.

> REVIEW (2026-07-14): Revalidated the JSON evidence register and reran
> `make check`; all audit, schema, converter, harness, study, service-boundary,
> and Docassemble gates passed on Python 3.14.6. No corrective code or evidence
> changes were required. Remaining type, dependency, re-extraction, and
> publication gates are accurately recorded as deferred.

## Child tracks

- `foi-o`: `maximal_quality_profile_20260714` ([issue #36](https://github.com/edithatogo/foi-o/issues/36))
- `fyi-archive`: `maximal_quality_profile_20260714` ([issue #189](https://github.com/edithatogo/fyi-archive/issues/189))
- `nlp-policy-nz`: `spacy4_compatibility_spike_20260714` ([issue #104](https://github.com/edithatogo/nlp-policy-nz/issues/104))
- `nlp-policy-nz`: Python runtime reconciliation ([issue #105](https://github.com/edithatogo/nlp-policy-nz/issues/105))
