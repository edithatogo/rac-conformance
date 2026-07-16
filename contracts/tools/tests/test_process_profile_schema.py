import json
from pathlib import Path

from pic_contracts.validation import detect_contract, validate_file


ROOT = Path(__file__).parents[2] / "process-profile/0.1.0/examples"


def test_detects_process_profile() -> None:
    assert detect_contract({"conformsTo": "pic-process-profile/0.1.0"}) == "process-profile"


def test_valid_process_profiles_pass() -> None:
    for path in sorted((ROOT / "valid").glob("*.json")):
        report = validate_file(path)
        assert report.ok, report.to_dict()


def test_invalid_process_profiles_fail() -> None:
    for path in sorted((ROOT / "invalid").glob("*.json")):
        report = validate_file(path)
        assert not report.ok, path


def test_profile_rejects_event_observed_before_occurrence(tmp_path: Path) -> None:
    source = ROOT / "valid/foi-o-baseline.json"
    doc = json.loads(source.read_text())
    doc["events"][0]["observedAt"] = "2026-07-14T00:00:00Z"
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(doc))
    report = validate_file(path)
    assert any("observedAt precedes occurredAt" in issue.message for issue in report.issues)
