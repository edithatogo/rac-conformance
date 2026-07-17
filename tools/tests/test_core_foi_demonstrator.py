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
    assert chain["status"] == "candidate-human-certification-required"
    assert chain["equivalenceClaim"] == "none"
    assert chain["profile"]["promotionStatus"] == "not-promoted"
    assert chain["executionEvidence"]["assertionStatus"] == "inferred"

    candidate = ROOT / chain["profile"]["path"]
    assert _sha256(candidate) == chain["profile"]["sha256"]
    candidate_schema = _load_json(ROOT / "contracts/process-profile/0.1.0/schema.json")
    Draft202012Validator(candidate_schema).validate(_load_json(candidate))

    pic_trace = ROOT / chain["picTraceEvidence"]["path"]
    assert _sha256(pic_trace) == chain["picTraceEvidence"]["sha256"]
    pic_trace_schema = _load_json(ROOT / "contracts/pic-traces/0.1.0/schema.json")
    semantics_schema = _load_json(ROOT / "contracts/pic-semantics/0.1.0/schema.json")
    registry = Registry().with_resource(
        semantics_schema["$id"], Resource.from_contents(semantics_schema)
    )
    Draft202012Validator(pic_trace_schema, registry=registry).validate(_load_json(pic_trace))

    execution = ROOT / chain["executionEvidence"]["tracePath"]
    execution_schema = _load_json(ROOT / "external/foi-process/schemas/portable/conformance-trace.schema.json")
    Draft202012Validator(execution_schema).validate(_load_json(execution))
    assert _sha256(execution) == chain["executionEvidence"]["traceSha256"]

    replay = ROOT / chain["executionEvidence"]["replaySnapshotPath"]
    assert _sha256(replay) == chain["executionEvidence"]["replaySnapshotSha256"]
