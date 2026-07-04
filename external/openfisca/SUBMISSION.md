# Draft OpenFisca Issue: YAML test portability converter

Target repository: `openfisca/openfisca-core`

Suggested title:

`Proposal: deterministic OpenFisca YAML test -> portable fixture converter`

## Draft body

I have been working on a small deterministic converter for YAML test fixtures that may be useful for OpenFisca maintainers and country-package maintainers who need to compare or migrate test corpora.

The current prototype supports:

- OpenFisca YAML test -> intermediate fixture JSON -> OpenFisca YAML test round-trips for a documented subset.
- Scalar and nested entity input/output maps.
- Absolute error margins, including OpenFisca per-variable/default mappings.
- Loud rejection for unsupported constructs such as reforms, extensions, relative error margins, parameter overrides, lists, nulls, and expression strings.
- Source-preserving provenance for mechanical conversions.

I verified the current OpenFisca YAML loader from `openfisca-core` commit `4f7f09833afe7e8b6856e8d7a3016c04a931009b`, specifically `openfisca_core/tools/test_runner.py`, before defining the subset.

Corpus evidence:

- Source corpus: 10 YAML files from `openfisca/openfisca-france` commit `6eeee2e09b9f807ab3735ef494a92001a975f4ad`.
- Converted files: 10/10.
- Rejected files: 0/10 in the selected v0.1 subset corpus.
- Generated fixture JSON is validated with a JSON Schema validator in CI.

The goal is not to change OpenFisca's native test format. It is to make existing tests portable enough for cross-validation and migration workflows, while refusing cases that are not mechanically safe to convert.

Would OpenFisca maintainers be open to either:

1. a small external tool documented from OpenFisca docs, or
2. a short maintainer-reviewed note describing the supported subset and safe rejection behavior?

I can keep this as an external tool first and bring a focused PR only if there is interest.

Footnote: the intermediate JSON fixture format follows a small "PIC fixtures" schema being developed for cross-engine conformance work. That format is an implementation detail here; the user-facing value is OpenFisca test portability and reviewable rejection statistics.

## Local evidence files

- `converters/fixtures/FORMATS.md`
- `converters/fixtures/SUPPORTED.md`
- `converters/fixtures/corpus/MANIFEST.md`
- `converters/fixtures/corpus/REPORT.md`
- `converters/fixtures/src/pic_fixture_converters/`
