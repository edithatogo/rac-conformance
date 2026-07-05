# Axiom harness runbook

Track: `engine_contributions_20260704` Phase 3
Status: prototype runbook

This prototype targets the public Axiom RuleSpec runtime surface. The first
recommended slice is `TheAxiomFoundation/rulespec-nz` GST:

- repo: `https://github.com/TheAxiomFoundation/rulespec-nz`
- pinned commit: `3c6436b2ecf82dd7a7f7810a406a2695a64af33a`
- module: `nz/statutes/gst/rate.yaml`
- companion test: `nz/statutes/gst/rate.test.yaml`

## Local setup

Clone and build Axiom's public engine:

```bash
git clone https://github.com/TheAxiomFoundation/axiom-rules-engine.git
cd axiom-rules-engine
cargo build
```

Clone the public NZ RuleSpec corpus and pin the commit:

```bash
git clone https://github.com/TheAxiomFoundation/rulespec-nz.git
cd rulespec-nz
git checkout 3c6436b2ecf82dd7a7f7810a406a2695a64af33a
```

Compile the GST module:

```bash
AXIOM_RULESPEC_REPO_ROOTS=/path/to/rulespec-nz \
  /path/to/axiom-rules-engine/target/debug/axiom-rules-engine compile \
  --program /path/to/rulespec-nz/nz/statutes/gst/rate.yaml \
  --output /tmp/rulespec-nz-gst.compiled.json
```

## Python harness use

The harness takes PIC fixture documents and maps their PIC IDs to durable Axiom
RuleSpec IDs. The GST smoke mapping is built in for the first slice.

```python
from axiom import build_rulespec_nz_gst_adapter, write_reports
from axiom.runner import AxiomCompiledArtifactExecutor, AxiomHarnessRunner

runner = AxiomHarnessRunner(
    adapter=build_rulespec_nz_gst_adapter(),
    executor=AxiomCompiledArtifactExecutor(
        binary_path="/path/to/axiom-rules-engine/target/debug/axiom-rules-engine",
        artifact_path="/tmp/rulespec-nz-gst.compiled.json",
    ),
)

results = runner.run_fixtures_file("path/to/pic-fixtures.json")
write_reports(results, "outputs/axiom-rulespec-nz-gst")
```

For tests, pass a deterministic stub executor to `run_case` or
`run_fixture_document`. The stub receives the exact compiled-execution request
dictionary that would be sent to `axiom-rules-engine`.

## Output

`write_reports` emits:

- `report.md`: human-readable divergence summary.
- `report.json`: machine-readable result packet.

Statuses are deterministic:

- `exact_match`
- `output_mismatch`
- `adapter_failure`

## Expansion path

After the GST smoke slice works against a local compiled artifact, move to a
higher-overlap module such as ACC earners levy or income-tax schedule 1. Add a
new explicit PIC-to-Axiom ID mapping for that slice before running the harness.
