from __future__ import annotations

from pic_contracts.schema_utils import validator_for
from policyengine_trace import project_flat_trace
from policyengine_trace.projection import parse_trace_key

SNAP_FLAT_TRACE = {
    "snap<2024-01, (default)>": {
        "dependencies": [
            "snap_normal_allotment<2024-01, (default)>",
            "snap_emergency_allotment<2024-01, (default)>",
        ],
        "parameters": {},
        "value": [291.0],
        "calculation_time": 2.615,
        "formula_time": 0.0001338,
    },
    "snap_normal_allotment<2024-01, (default)>": {
        "dependencies": [
            "is_snap_eligible<2024-01, (default)>",
            "snap_max_allotment<2024-01, (default)>",
        ],
        "parameters": {
            "gov.usda.snap.min_allotment<2024-01, (default)>": 23,
        },
        "value": [291.0],
        "calculation_time": 0.4,
        "formula_time": 0.01,
    },
    "is_snap_eligible<2024-01, (default)>": {
        "dependencies": [],
        "parameters": {},
        "value": [True],
        "calculation_time": 0.1,
        "formula_time": 0.1,
    },
    "snap_max_allotment<2024-01, (default)>": {
        "dependencies": [],
        "parameters": {
            "gov.usda.snap.max_allotment.amount<2024-01, (default)>": 291,
        },
        "value": [291.0],
        "calculation_time": 0.1,
        "formula_time": 0.1,
    },
    "snap_emergency_allotment<2024-01, (default)>": {
        "dependencies": [],
        "parameters": {},
        "value": [0.0],
        "calculation_time": 0.1,
        "formula_time": 0.1,
    },
}


def test_parse_policyengine_trace_key() -> None:
    parsed = parse_trace_key("snap<2024-01, (default)>")
    assert parsed.name == "snap"
    assert parsed.period == "2024-01"
    assert parsed.branch == "default"


def test_project_snap_flat_trace_to_valid_pic_trace() -> None:
    trace = project_flat_trace(
        SNAP_FLAT_TRACE,
        output_key="snap<2024-01, (default)>",
        case_id="us-snap/fixture.snap_trace",
        package_id="policyengine-us",
        package_version="1.755.5",
        engine_version="1.755.5",
        timestamp="2026-07-04T22:00:00Z",
        namespace="us-snap",
    )

    validator_for("pic-traces").validate(trace)
    assert trace["outputs"] == {
        "us-snap/decision.snap": {
            "value": "291.0",
            "valueState": "known",
            "currency": "USD",
        }
    }
    assert [step["stepId"] for step in trace["steps"]] == [
        "is_snap_eligible__2024_01__default",
        "snap_max_allotment__2024_01__default",
        "snap_normal_allotment__2024_01__default",
        "snap_emergency_allotment__2024_01__default",
        "snap__2024_01__default",
    ]
    assert trace["steps"][2]["parameterVersions"] == [
        {
            "id": "us-snap/parameter.gov_usda_snap_min_allotment",
            "effectiveFrom": "2024-01-01",
        }
    ]


def test_missing_output_key_fails_closed() -> None:
    try:
        project_flat_trace(
            SNAP_FLAT_TRACE,
            output_key="missing<2024-01, (default)>",
            case_id="us-snap/fixture.snap_trace",
            package_id="policyengine-us",
            package_version="1.755.5",
            engine_version="1.755.5",
            timestamp="2026-07-04T22:00:00Z",
        )
    except KeyError as exc:
        assert "output key not found" in str(exc)
    else:
        raise AssertionError("missing output key should fail")
