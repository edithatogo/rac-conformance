# Draft PolicyEngine Issue: YAML test portability converter

Target repository: `PolicyEngine/policyengine-core`

Suggested title:

`Proposal: deterministic PolicyEngine YAML test -> portable fixture converter`

## Draft body

I have a small deterministic converter prototype that may be useful for PolicyEngine's existing validation and cross-model comparison work: it converts supported PolicyEngine YAML tests into an intermediate fixture JSON format and back to canonical PolicyEngine YAML data.

The current prototype supports:

- PolicyEngine YAML test -> intermediate fixture JSON -> PolicyEngine YAML test round-trips for a documented subset.
- Scalar and nested entity input/output maps.
- Absolute error margins.
- Optional crosswalk remapping for cross-engine conversion when every variable has an explicit mapping.
- Loud rejection for unsupported constructs such as reforms, extensions, relative error margins, dotted input keys that PolicyEngine treats as inline parameter reforms, lists, nulls, and expression strings.

I verified the current PolicyEngine YAML loader from `policyengine-core` commit `f761573c2a13adecc3826be04af1980d13657e1d`, specifically `policyengine_core/tools/test_runner.py`, before defining the subset.

Corpus evidence:

- Source corpus: 10 YAML files from `PolicyEngine/policyengine-us` commit `fc64cef64ab55c3c48309c7fb304c35e5f3c9184`.
- Converted files: 10/10.
- Rejected files: 0/10 in the selected v0.1 subset corpus.
- Generated fixture JSON is validated with a JSON Schema validator in CI.

This is intended as a migration/cross-validation utility, not a replacement for PolicyEngine's native test format. The converter refuses ambiguous or engine-specific constructs rather than silently dropping them.

Would PolicyEngine maintainers be open to this living as:

1. an external utility with docs/examples that reference PolicyEngine's current YAML test shape, or
2. a small upstream docs/testing contribution if useful?

Given PolicyEngine's existing validation culture, the highest-value next step may be a narrow demonstration on a package slice rather than a broad format discussion.

Footnote: the intermediate JSON fixture format follows a small "PIC fixtures" schema being developed for cross-engine conformance work. That format is an implementation detail here; the user-facing value is PolicyEngine test portability and cross-engine comparison with explicit mappings.

## Local evidence files

- `converters/fixtures/FORMATS.md`
- `converters/fixtures/SUPPORTED.md`
- `converters/fixtures/corpus/MANIFEST.md`
- `converters/fixtures/corpus/REPORT.md`
- `converters/fixtures/src/pic_fixture_converters/`
