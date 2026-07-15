from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[3]
BASE = ROOT / "subrepos/process-mappings/profiles/adverse-incidents/safety-handoff"


def test_valid_handoff_is_aggregate_and_not_action_authorized() -> None:
    schema = json.loads((BASE / "schema.json").read_text(encoding="utf-8"))
    document = json.loads(
        (BASE / "examples/valid-aggregate.json").read_text(encoding="utf-8")
    )

    errors = list(Draft202012Validator(schema).iter_errors(document))

    assert errors == []
    assert document["aggregation"]["patientLevelDataIncluded"] is False
    assert document["signal"]["causation"] == "not-inferred"
    assert document["consumptionStatus"] == "blocked-until-human-review"
    assert document["downstreamAction"]["authorized"] is False


def test_negative_handoffs_fail_closed() -> None:
    schema = json.loads((BASE / "schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    for path in sorted((BASE / "examples").glob("invalid-*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        assert list(validator.iter_errors(document)), path
