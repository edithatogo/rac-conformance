from copy import deepcopy
from pathlib import Path

from pic_contracts.schema_utils import CONTRACTS_ROOT, load_json, validator_for
from pic_contracts.traces import _step_sources, trace_equivalence

BASE = CONTRACTS_ROOT / "pic-traces" / "0.1.0" / "examples"


def test_valid_traces_validate() -> None:
    validator = validator_for("pic-traces")
    for path in sorted((BASE / "valid").glob("*.json")):
        validator.validate(load_json(path))


def test_invalid_traces_fail_for_intended_reason() -> None:
    validator = validator_for("pic-traces")
    expected: dict[str, tuple[Path, str]] = {
        "bad-kind.json": (Path("steps/0/kind"), "is not one of"),
        "missing-conforms-to.json": (Path(), "is a required property"),
        "bad-parameter-version.json": (
            Path("steps/0/parameterVersions/0"),
            "is a required property",
        ),
    }
    for filename, (error_path, message) in expected.items():
        errors = list(validator.iter_errors(load_json(BASE / "invalid" / filename)))
        assert errors
        assert any(Path(*map(str, error.path)) == error_path for error in errors)
        assert any(message in error.message for error in errors)


def test_trace_equivalence_levels() -> None:
    trace = load_json(BASE / "valid" / "oia-response-deadline.json")
    equal = deepcopy(trace)
    assert trace_equivalence(trace, equal) == {
        "output": True,
        "path": True,
        "semantic": True,
        "diffs": [],
    }

    output_only = deepcopy(trace)
    output_only["steps"][0]["stepId"] = "alternate_path"
    assert trace_equivalence(trace, output_only)["output"] is True
    assert trace_equivalence(trace, output_only)["path"] is False

    path_different = deepcopy(trace)
    path_different["outputs"]["nz-oia/decision.response_deadline"]["value"] = "2026-02-11"
    result = trace_equivalence(trace, path_different)
    assert result["output"] is False
    assert result["path"] is False
    assert result["semantic"] is False

    semantic_different = deepcopy(trace)
    semantic_different["steps"][0]["sourceRefs"] = ["different source"]
    result = trace_equivalence(trace, semantic_different)
    assert result["output"] is True
    assert result["path"] is True
    assert result["semantic"] is False


def test_step_sources() -> None:
    # Happy path: valid stepId and sourceRefs
    trace = {
        "steps": [
            {"stepId": "step1", "sourceRefs": ["ref1", "ref2"]},
            {"stepId": "step2", "sourceRefs": ["ref3"]},
        ]
    }
    assert _step_sources(trace) == [
        ("step1", ("ref1", "ref2")),
        ("step2", ("ref3",)),
    ]

    # Edge case: empty trace
    assert _step_sources({}) == []

    # Edge case: trace missing steps key
    assert _step_sources({"otherKey": "value"}) == []

    # Edge case: step missing stepId or sourceRefs
    trace_missing = {
        "steps": [
            {"sourceRefs": ["ref1"]},  # missing stepId
            {"stepId": "step2"},  # missing sourceRefs
            {},  # missing both
        ]
    }
    assert _step_sources(trace_missing) == [
        ("", ("ref1",)),
        ("step2", ()),
        ("", ()),
    ]
