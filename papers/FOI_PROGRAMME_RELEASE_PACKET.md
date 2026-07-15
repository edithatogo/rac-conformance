# FOI programme quality release packet

As of 2026-07-15, the three child repositories have explicit stable and
canary quality evidence. The machine-readable source of truth is
[`foi-programme-quality-evidence.json`](foi-programme-quality-evidence.json).

FOI-O `v0.8.1` is now an immutable published release with verified Zenodo
version and concept DOIs. Its release-evidence bundle, V2 compatibility
exercise, and empirical extraction gates remain open under
[foi-o#27](https://github.com/edithatogo/foi-o/issues/27); this packet does not
infer those results from release metadata.

## Stable lanes

- `foi-o`: Python 3.12 locked production lane with stable Ruff, schema,
  provenance, security, SBOM, and optional preview checks. Its strict
  basedpyright baseline remains advisory at 434 findings.
- `fyi-archive`: Python 3.12 locked production lane; 202 tests passed, one
  skipped, and 90.31% coverage. Its basedpyright baseline remains advisory at
  974 findings; the yanked pandas warning is recorded for explicit review.
- `nlp-policy-nz`: Python 3.12 production and 3.11 compatibility lanes. spaCy
  3.8.14 remains the production parser and adapter baseline.

## Canary and release boundaries

- Python 3.13 and 3.14 are non-blocking native-wheel canaries.
- spaCy 4.0.0.dev3 is deferred: Python 3.14 has no wheel and its source build
  fails in `blis`; the spaCy 4 deontic adapter also has a Pydantic forward
  reference failure.
- The cross-repository FOI-O/NLP extraction contract is pinned for testing, but
  the next full re-extraction remains pending. No manuscript claim should call
  this extraction-accuracy evidence.
- Remaining Zenodo deposits, Hugging Face revision pins, upstream merges, and final
  manuscript submission remain human/publication gates.

## Reproducibility

The release register pins local repository heads, quality decisions, and the
exact boundary between repo-local evidence and external publication evidence.
When the FOI-O release-evidence bundle is published, rerun the extraction
contract and update this packet and the citation ledger together.
