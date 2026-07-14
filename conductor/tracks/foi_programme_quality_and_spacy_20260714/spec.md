# FOI programme quality and spaCy evaluation

Coordinate the maximal quality profile across `foi-o`, `fyi-archive`, and
`nlp-policy-nz`, while keeping spaCy 4 and Python 3.14 as evidence-gathering
canaries rather than production assumptions.

## Acceptance

- Each child track has a passing stable quality lane and an explicit canary result.
- Release evidence includes dependency lock, Python/runtime matrix, schema,
  provenance, security, SBOM, and cross-repository contract results.
- Manuscript claims identify the exact quality and extraction evidence used.
