# Independent Implementer Kit

This directory is the sole canonical independent-validation kit. Copy it to a
clean environment; it does not import repository code or require private
services. Install Python and `jsonschema`, then run:

```text
python run_reference.py --output results.json
```

The bundled manifest pins every schema and corpus artifact by SHA-256. The
reference runner verifies those digests before executing all valid and invalid
cases. Its output is a structural rehearsal only and cannot satisfy the v1
independence gate.

`result.schema.json` is the v2 evidence contract and
`submission-template.json` is a schema-valid, deliberately non-qualifying
template. Replace every placeholder and digest. Verify a returned packet and
its local artifact bundle from the repository checkout with:

```text
PYTHONPATH=. uv run --with jsonschema python -m tools.independent_evidence \
  packet.json --evidence-root /path/to/evidence-bundle
```

`example-nonqualifying-result.json` is deliberately a legacy, schema-invalid
example retained to prove that the compatibility verifier fails closed.

The copied kit is self-contained for producing and structurally rehearsing a
submission. Final maintainer-side evidence verification intentionally remains
outside the implementer kit so the submitter does not control the verifier.

An external implementer must use independently controlled code, fixtures,
oracle, repository, and execution infrastructure. Submit evidence against the
schema and policy identified in the parent `independent/` directory.
