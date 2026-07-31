from copy import deepcopy

from pic_contracts.schema_utils import CONTRACTS_ROOT, load_json
from pic_contracts.traces import trace_equivalence

BASE = CONTRACTS_ROOT / "pic-traces" / "0.1.0" / "examples"


def test_trace_equivalence_levels() -> None:
    trace = load_json(BASE / "valid" / "oia-response-deadline.json")
    equal = deepcopy(trace)
    result = trace_equivalence(trace, equal)
    assert result == {
        "output": True,
        "path": True,
        "semantic": True,
        "diffs": [],
    }

    output_only = deepcopy(trace)
    output_only["steps"][0]["stepId"] = "alternate_path"
    result = trace_equivalence(trace, output_only)
    assert result["output"] is True
    assert result["path"] is False
    assert result["semantic"] is False
    assert result["diffs"] == [
        {"level": "path", "message": "step IDs or parameter versions differ"}
    ]

    path_different = deepcopy(trace)
    path_different["outputs"]["nz-oia/decision.response_deadline"]["value"] = "2026-02-11"
    result = trace_equivalence(trace, path_different)
    assert result["output"] is False
    assert result["path"] is False
    assert result["semantic"] is False
    assert result["diffs"] == [
        {"level": "output", "message": "outputs differ"}
    ]

    semantic_different = deepcopy(trace)
    semantic_different["steps"][0]["sourceRefs"] = ["different source"]
    result = trace_equivalence(trace, semantic_different)
    assert result["output"] is True
    assert result["path"] is True
    assert result["semantic"] is False
    assert result["diffs"] == [
        {"level": "semantic", "message": "step source references differ"}
    ]

def test_trace_equivalence_empty() -> None:
    # Test completely empty dictionaries
    result = trace_equivalence({}, {})
    assert result == {
        "output": True,
        "path": True,
        "semantic": True,
        "diffs": [],
    }

    # Test one empty dictionary
    trace = load_json(BASE / "valid" / "oia-response-deadline.json")
    result = trace_equivalence(trace, {})
    assert result["output"] is False
    assert result["path"] is False
    assert result["semantic"] is False
    assert result["diffs"] == [
        {"level": "output", "message": "outputs differ"}
    ]

def test_trace_equivalence_missing_keys() -> None:
    # Test traces missing 'outputs' or 'steps' but otherwise populated
    trace1 = {"some_other_key": "value"}
    trace2 = {"some_other_key": "value2"}

    result = trace_equivalence(trace1, trace2)
    assert result == {
        "output": True,
        "path": True,
        "semantic": True,
        "diffs": [],
    }

    trace_with_steps = {
        "steps": [
            {
                "stepId": "s1",
                "parameterVersions": [{"id": "p1", "effectiveFrom": "d1"}],
            }
        ]
    }
    trace_without_steps = {}
    result = trace_equivalence(trace_with_steps, trace_without_steps)
    assert result["output"] is True
    assert result["path"] is False
    assert result["semantic"] is False
    assert result["diffs"] == [
        {"level": "path", "message": "step IDs or parameter versions differ"}
    ]
