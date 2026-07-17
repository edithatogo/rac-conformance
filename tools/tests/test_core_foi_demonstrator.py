import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).parents[2]
CHAIN = ROOT / "conductor/tracks/core_model_demonstrator_20260717/FOI_DEMONSTRATOR_CHAIN.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_foi_demonstrator_chain_is_pinned_and_fail_closed() -> None:
    chain = _load_json(CHAIN)
    assert chain["status"] == "certified-bounded"
    assert chain["equivalenceClaim"] == "none"
    assert chain["profile"]["promotionStatus"] == "not-promoted"
    assert chain["executionEvidence"]["assertionStatus"] == "inferred"
    assert chain["certification"]["decision"] == "bounded-compatible"
    assert chain["certification"]["analyst"] == "Dylan"
    assert chain["certification"]["reviewedCommit"] == (
        "8343ad5f9dbc1d980ddf49018f2f6f4f6d181dde"
    )
    assert chain["certification"]["evidencePins"] == [
        f"E{index}" for index in range(1, 12)
    ]

    source_authority = ROOT / chain["sourceAuthority"]["path"]
    assert _sha256(source_authority) == chain["sourceAuthority"]["sha256"]

    candidate = ROOT / chain["profile"]["path"]
    assert _sha256(candidate) == chain["profile"]["sha256"]
    candidate_schema = _load_json(ROOT / "contracts/process-profile/0.1.0/schema.json")
    Draft202012Validator(
        candidate_schema, format_checker=Draft202012Validator.FORMAT_CHECKER
    ).validate(_load_json(candidate))

    pic_trace = ROOT / chain["picTraceEvidence"]["path"]
    assert _sha256(pic_trace) == chain["picTraceEvidence"]["sha256"]
    pic_trace_schema_path = ROOT / chain["picTraceEvidence"]["schemaPath"]
    assert _sha256(pic_trace_schema_path) == chain["picTraceEvidence"]["schemaSha256"]
    pic_trace_schema = _load_json(pic_trace_schema_path)
    semantics_schema = _load_json(ROOT / "contracts/pic-semantics/0.1.0/schema.json")
    registry = Registry().with_resource(
        semantics_schema["$id"], Resource.from_contents(semantics_schema)
    )
    Draft202012Validator(
        pic_trace_schema,
        registry=registry,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    ).validate(_load_json(pic_trace))

    execution = ROOT / chain["executionEvidence"]["tracePath"]
    execution_schema = _load_json(ROOT / "external/foi-process/schemas/portable/conformance-trace.schema.json")
    Draft202012Validator(
        execution_schema, format_checker=Draft202012Validator.FORMAT_CHECKER
    ).validate(_load_json(execution))
    assert _sha256(execution) == chain["executionEvidence"]["traceSha256"]

    replay = ROOT / chain["executionEvidence"]["replaySnapshotPath"]
    assert _sha256(replay) == chain["executionEvidence"]["replaySnapshotSha256"]
