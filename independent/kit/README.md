# Independent Implementer Kit

This kit is designed to be copied to a clean environment. It contains the
versioned contract identifiers, expected-result policy, negative-test policy,
and result submission schema. The maintainer repository is not an execution
service and no private source material is required.

Run the reference check from the repository root:

```text
PYTHONPATH=. uv run python tools/independent_validation.py --kit independent/kit --result independent/kit/example-result.json
```

The example result is deliberately `not-submitted` and cannot satisfy the v1
gate. An external implementer must create a new result using its own code,
fixtures, oracle, and environment.
