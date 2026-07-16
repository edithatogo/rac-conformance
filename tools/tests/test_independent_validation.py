import json
from pathlib import Path

from tools.independent_validation import verify


ROOT = Path(__file__).parents[2]
KIT = ROOT / "independent/kit"


def test_example_result_cannot_qualify() -> None:
    report = verify(KIT, KIT / "example-result.json")
    assert not report["ok"]
    assert "implementation is maintainer-controlled" in report["diagnostics"]


def test_verifier_accepts_structurally_complete_independent_result(tmp_path: Path) -> None:
    result = json.loads((KIT / "example-result.json").read_text())
    result["implementation"].update({"maintainerControlled": False, "revision": "abcdef1234567", "repository": "external/example"})
    result["oracle"].update({"independent": True, "method": "independent-reference"})
    result["outcome"] = "qualifying"
    result["evidence"]["acknowledged"] = True
    path = tmp_path / "result.json"
    path.write_text(json.dumps(result))
    assert verify(KIT, path)["ok"]


def test_verifier_rejects_qualifying_result_without_acknowledgement(tmp_path: Path) -> None:
    result = json.loads((KIT / "example-result.json").read_text())
    result["implementation"].update({"maintainerControlled": False, "revision": "abcdef1234567", "repository": "external/example"})
    result["oracle"]["independent"] = True
    result["outcome"] = "qualifying"
    path = tmp_path / "result.json"
    path.write_text(json.dumps(result))
    report = verify(KIT, path)
    assert "qualifying result lacks maintainer acknowledgement" in report["diagnostics"]
