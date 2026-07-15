# Agent-Run Independent Evaluation

**Status: internal rehearsal only.** This evaluation was performed by an
isolated agent in a separate worktree. It is not external independent
adoption, independent organisational evidence, or human certification. No
external author, acceptance, maintainer response, or adoption outcome is
claimed.

## Scope and clean-room boundary

The evaluator reads only committed public JSON Schemas and JSON examples from
the repository. It does not import or call `pic_contracts`,
`pic_fixture_converters`, existing conformance harnesses, production
validators, converters, fixtures, or maintainer-controlled services. Its only
non-stdlib dependency is the independently invoked `jsonschema` package.

The bounded corpus contains 16 cases:

- process profile 0.1.0: 2 valid and 4 schema-invalid examples;
- PIC fixtures 0.1.0: 2 valid and 3 schema-invalid examples;
- PIC traces 0.1.0: 2 valid and 3 schema-invalid examples.

Two repository examples labelled `invalid` were deliberately excluded from
this schema-only corpus: `process-profile/0.1.0/examples/invalid/bad-transition.json`
and `dangling-trace-link.json`. The independent probe observed that they pass
JSON Schema validation, indicating semantic/integrity rules outside this
bounded JSON-Schema check. They are not silently counted as failures or
successes.

## Method

`evaluate.py` constructs a `Draft202012Validator` independently for each
schema, enables the package's `FormatChecker`, and supplies a local registry
of committed schema `$id` documents for references. Each example's directory
(`valid` or `invalid`) supplies the expected verdict. The evaluator records
the first validation error, schema and example SHA-256 digests, repository
commit, Python runtime, platform, and `jsonschema` version in `RESULTS.json`.

The run was performed with:

```sh
contracts/tools/.venv/bin/python \
  conductor/tracks/v1_independent_validation_20260714/evidence/agent-independent/evaluate.py \
  --repo-root . \
  --output-dir conductor/tracks/v1_independent_validation_20260714/evidence/agent-independent
python -m json.tool \
  conductor/tracks/v1_independent_validation_20260714/evidence/agent-independent/RESULTS.json
```

The reproducibility refresh was run from a clean detached worktree at
`8468710300addedddcfe516866c6628f96e346ba` after the kit and verifier were
committed. The result manifest records the exact commit, evaluator digest, and
input digests.

## Result

The independent rehearsal **passed** all 16 expected schema verdicts: 6
valid examples were accepted and 10 invalid examples were rejected. The
machine-readable evidence is in `RESULTS.json`.

The evaluator recorded a clean checkout at capture. The evidence output was
written outside that detached worktree and copied back into this track, so the
captured clean-state claim is not affected by committing the manifest here.

## Blockers and limitations

1. This is an agent-run internal rehearsal, so it cannot satisfy the Track
   #45 external-adoption or human-certification gate.
2. The corpus is bounded and schema-focused. It does not test semantic
   transition integrity, converter behavior, engine behavior, performance,
   hostile inputs, or independent organisational maintenance.
3. The evaluator relies on `jsonschema` 4.26.0 from the local tool environment;
   the exact package version and Python/platform are recorded in
   `RESULTS.json`, but a clean environment must install that dependency before
   reproduction.
4. No external implementation, external owner, public acknowledgement, or
   adoption evidence was available or asserted.

## Reproducibility

From a clean checkout at the captured commit, install a compatible Python
runtime and `jsonschema` 4.26.0, then run the command above. Compare the
recorded input SHA-256 values and expected/observed verdicts in `RESULTS.json`.
The run must remain local-only and must not retrieve remote `$ref` documents.
