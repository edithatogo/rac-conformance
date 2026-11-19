# Generated PIC input-boundary checks

`contracts/tools/tests/test_safety_generated.py` exercises the production
`load_bounded_json` reader with deterministic, bounded synthetic inputs. It adds
379 parametrized tests: 270 Unicode string cases, 64 nested object/list cases,
34 encoded-size cases, ten non-object roots and one complete prefix-truncation
campaign. The admitted cases must retain their JSON value. Limits are checked at
one byte/depth below the boundary, at the boundary, and one above it.

String cases include one-, two-, three- and four-byte UTF-8 characters, control
characters and escapes; keys, values and list elements; and both literal and
ASCII-escaped JSON wire forms. The bound applies to decoded string bytes, while
the input-size bound includes wire encoding and whitespace. Nested cases remain
at depth 32 or below and truncated JSON stays below 128 bytes. No external input,
engine, statute interpretation, promoted fixture or runtime AI is involved.

The existing `make check` gate already executes this test file on pull requests.
The separate path-scoped PR/weekly/manual workflow uses Python 3.12.14, the repository's locked
PIC dependencies, uv 0.11.8 and pytest 9.2.0. A five-minute command budget and an
eight-minute job budget bound execution; parameter-labelled test output and the
interpreter revision and commit are retained for 14 days.

```sh
uv run --locked --directory contracts/tools --with pytest==9.2.0 \
  python -m pytest -v tests/test_safety_generated.py
```

The existing `tools/v1_fuzz.py` six-case validation mutation campaign and all
release/independence gates remain in place. These properties are additional
parser assurance, not a new maturity or policy-conformance certification and not
a claim of coverage-guided native fuzzing.
