# Independent PIC Implementer Kit

Version: `independent-kit/0.1.0`.

This kit is self-contained for the bundled `pic-semantics/0.1.0` structural
corpus. It contains the schema, valid/invalid examples, expected-result policy,
and a reference runner. It does not require a checkout-relative path, private
service, or maintainer runtime.

## Run

From this directory in a clean Python environment with `jsonschema`:

```sh
python run_reference.py --output results.json
```

The result is evidence of the runner's structural behavior only. An external
implementation must use its own codebase and oracle to produce qualifying
independent evidence; this runner is not an independent adoption result.

