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

## Verified live smoke command

The repository includes PIC smoke fixtures and a small runner for the mapped
`rulespec-nz` smoke slices. After building the engine and compiling the three
artifacts above, run:

```bash
PYTHONPATH=harness:contracts/tools/src \
  uv run --with jsonschema \
  python external/axiom/run_rulespec_nz_smoke.py
```

On 2026-07-06 this produced `exact_match` for:

- `nz-gst/fixture.add_and_remove_gst`
- `nz-acc/fixture.standard_2026_earnings_below_cap`
- `nz-income-tax/fixture.first_bracket_upper_bound`

The stored report is under `external/axiom/results/rulespec-nz-live-smoke/`.

## Selected validation slices

### KiwiSaver contributions

- module: `nz/statutes/kiwisaver/contributions.yaml`
- companion test: `nz/statutes/kiwisaver/contributions.test.yaml`
- first candidate fixture:
  `external/axiom/fixtures/rulespec-nz-kiwisaver-contributions-source.pic-fixtures.json`

Compile it with:

```bash
AXIOM_RULESPEC_REPO_ROOTS=/path/to/rulespec-nz \
  /path/to/axiom-rules-engine/target/debug/axiom-rules-engine compile \
  --program /path/to/rulespec-nz/nz/statutes/kiwisaver/contributions.yaml \
  --output /tmp/rulespec-nz-kiwisaver-contributions.compiled.json
```

Then run it with:

```python
from axiom import build_rulespec_nz_kiwisaver_contributions_adapter

runner = AxiomHarnessRunner(
    adapter=build_rulespec_nz_kiwisaver_contributions_adapter(),
    executor=AxiomCompiledArtifactExecutor(
        binary_path="/path/to/axiom-rules-engine/target/debug/axiom-rules-engine",
        artifact_path="/tmp/rulespec-nz-kiwisaver-contributions.compiled.json",
    ),
)

results = runner.run_fixtures_file(
    "external/axiom/fixtures/rulespec-nz-kiwisaver-contributions-source.pic-fixtures.json"
)
```

### New Zealand Superannuation core

- module: `nz/statutes/new_zealand_superannuation/core.yaml`
- companion test: `nz/statutes/new_zealand_superannuation/core.test.yaml`
- first candidate fixture:
  `external/axiom/fixtures/rulespec-nz-new-zealand-superannuation-core-source.pic-fixtures.json`

Compile it with:

```bash
AXIOM_RULESPEC_REPO_ROOTS=/path/to/rulespec-nz \
  /path/to/axiom-rules-engine/target/debug/axiom-rules-engine compile \
  --program /path/to/rulespec-nz/nz/statutes/new_zealand_superannuation/core.yaml \
  --output /tmp/rulespec-nz-new-zealand-superannuation-core.compiled.json
```

Then run it with:

```python
from axiom import build_rulespec_nz_new_zealand_superannuation_core_adapter

runner = AxiomHarnessRunner(
    adapter=build_rulespec_nz_new_zealand_superannuation_core_adapter(),
    executor=AxiomCompiledArtifactExecutor(
        binary_path="/path/to/axiom-rules-engine/target/debug/axiom-rules-engine",
        artifact_path="/tmp/rulespec-nz-new-zealand-superannuation-core.compiled.json",
    ),
)

results = runner.run_fixtures_file(
    "external/axiom/fixtures/rulespec-nz-new-zealand-superannuation-core-source.pic-fixtures.json"
)
```

### New Zealand Superannuation special rates

- module: `nz/statutes/new_zealand_superannuation/special_rates.yaml`
- companion test: `nz/statutes/new_zealand_superannuation/special_rates.test.yaml`
- first candidate fixture:
  `external/axiom/fixtures/rulespec-nz-new-zealand-superannuation-special-rates-source.pic-fixtures.json`

Compile it with:

```bash
AXIOM_RULESPEC_REPO_ROOTS=/path/to/rulespec-nz \
  /path/to/axiom-rules-engine/target/debug/axiom-rules-engine compile \
  --program /path/to/rulespec-nz/nz/statutes/new_zealand_superannuation/special_rates.yaml \
  --output /tmp/rulespec-nz-new-zealand-superannuation-special-rates.compiled.json
```

Then run it with:

```python
from axiom import build_rulespec_nz_new_zealand_superannuation_special_rates_adapter

runner = AxiomHarnessRunner(
    adapter=build_rulespec_nz_new_zealand_superannuation_special_rates_adapter(),
    executor=AxiomCompiledArtifactExecutor(
        binary_path="/path/to/axiom-rules-engine/target/debug/axiom-rules-engine",
        artifact_path="/tmp/rulespec-nz-new-zealand-superannuation-special-rates.compiled.json",
    ),
)

results = runner.run_fixtures_file(
    "external/axiom/fixtures/rulespec-nz-new-zealand-superannuation-special-rates-source.pic-fixtures.json"
)
```

## Expansion path

After the GST smoke slice works against a local compiled artifact, use the
built-in ACC earners levy mapping for a higher-overlap tax/payroll case:

- module: `nz/regulations/acc/earners_levy.yaml`
- companion test: `nz/regulations/acc/earners_levy.test.yaml`
- first case: `standard_2026_earnings_below_cap`

Compile it the same way:

```bash
AXIOM_RULESPEC_REPO_ROOTS=/path/to/rulespec-nz \
  /path/to/axiom-rules-engine/target/debug/axiom-rules-engine compile \
  --program /path/to/rulespec-nz/nz/regulations/acc/earners_levy.yaml \
  --output /tmp/rulespec-nz-acc-earners-levy.compiled.json
```

Then swap the adapter and artifact:

```python
from axiom import build_rulespec_nz_acc_earners_levy_adapter

runner = AxiomHarnessRunner(
    adapter=build_rulespec_nz_acc_earners_levy_adapter(),
    executor=AxiomCompiledArtifactExecutor(
        binary_path="/path/to/axiom-rules-engine/target/debug/axiom-rules-engine",
        artifact_path="/tmp/rulespec-nz-acc-earners-levy.compiled.json",
    ),
)
```

For further expansion, add another explicit PIC-to-Axiom ID mapping before
running a new module. Do not infer mappings at runtime.

The third mapped slice is individual income tax schedule 1:

- module: `nz/statutes/income_tax/schedule_1/individual_income_tax.yaml`
- companion test: `nz/statutes/income_tax/schedule_1/individual_income_tax.test.yaml`
- first case: `first_bracket_upper_bound`

Compile it with:

```bash
AXIOM_RULESPEC_REPO_ROOTS=/path/to/rulespec-nz \
  /path/to/axiom-rules-engine/target/debug/axiom-rules-engine compile \
  --program /path/to/rulespec-nz/nz/statutes/income_tax/schedule_1/individual_income_tax.yaml \
  --output /tmp/rulespec-nz-individual-income-tax.compiled.json
```
