import json
from pathlib import Path

from tools.v1_release_audit import audit


ROOT = Path(__file__).parents[2]
GATES = ROOT / "release/v1/gates.json"


def test_current_release_candidate_is_explicitly_not_releasable() -> None:
    report = audit(GATES)
    assert report["diagnostics"] == []
    assert report["releasable"] is False


def test_audit_rejects_missing_release_gate(tmp_path: Path) -> None:
    document = json.loads(GATES.read_text())
    document["gates"] = [gate for gate in document["gates"] if gate["id"] != "publication"]
    path = tmp_path / "gates.json"
    path.write_text(json.dumps(document))
    assert any("missing required gate: publication" in item for item in audit(path)["diagnostics"])


def test_audit_rejects_unknown_status(tmp_path: Path) -> None:
    document = json.loads(GATES.read_text())
    document["gates"][0]["status"] = "maybe"
    path = tmp_path / "gates.json"
    path.write_text(json.dumps(document))
    assert any("unsupported gate status" in item for item in audit(path)["diagnostics"])
