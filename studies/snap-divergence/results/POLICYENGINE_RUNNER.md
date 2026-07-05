# PolicyEngine Runner Evidence

Track: `divergence_study_20260704`

Runner: `studies/snap-divergence/runner/src/snap_divergence/policyengine_runner.py`

Pinned engine:

- PolicyEngine-US version: `1.755.5`
- Source commit: `fc64cef64ab55c3c48309c7fb304c35e5f3c9184`

## Candidate Run

Command:

```sh
. .venv-policyengine/bin/activate
PYTHONPATH=studies/snap-divergence/runner/src:harness:contracts/tools/src \
  python -m snap_divergence.policyengine_runner \
  --output studies/snap-divergence/results/policyengine-candidate-results.jsonl \
  --no-trace
```

Result:

- 65 candidate fixtures executed.
- Output file: `studies/snap-divergence/results/policyengine-candidate-results.jsonl`
- First case: `us-snap/fixture.ca_baseline_single_very_low_income`, eligible `true`, allotment `298`.
- Last case: `us-snap/fixture.ga_utility_allowance_phone_only`, eligible `true`, allotment `295.8999938964844`.

## Trace Smoke

Command:

```sh
. .venv-policyengine/bin/activate
PYTHONPATH=studies/snap-divergence/runner/src:harness:contracts/tools/src \
  python -m snap_divergence.policyengine_runner \
  --case-id us-snap/fixture.tx_asset_below_limit \
  --output studies/snap-divergence/results/policyengine-smoke-trace.json
```

Validation:

```sh
PYTHONPATH=contracts/tools/src uv run --with jsonschema python - <<'PY'
import json
from pathlib import Path
from pic_contracts.schema_utils import validator_for
result = json.loads(Path('studies/snap-divergence/results/policyengine-smoke-trace.json').read_text())
trace = result['results'][0]['trace']
validator_for('pic-traces').validate(trace)
print('OK trace steps', len(trace['steps']))
PY
```

Result:

- `OK trace steps 2174`
- The large trace JSON is reproducible and is not committed.
