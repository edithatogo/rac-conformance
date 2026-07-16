import json
from pathlib import Path

from pic_contracts.process_profile import normalize_trace
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


def test_profile_rejects_missing_source_reference(tmp_path: Path) -> None:
    doc = json.loads((ROOT / "valid/foi-o-baseline.json").read_text())
    doc["events"][0]["sourceAssertionIds"] = []
    path = tmp_path / "pic-process-profile" / "profile.json"
    path.parent.mkdir()
    path.write_text(json.dumps(doc))
    report = validate_file(path)
    assert not report.ok
    assert any("sourceAssertionIds" in issue.message for issue in report.issues)


def test_profile_rejects_event_observed_before_occurrence(tmp_path: Path) -> None:
    source = ROOT / "valid/foi-o-baseline.json"
    doc = json.loads(source.read_text())
    doc["events"][0]["observedAt"] = "2026-07-14T00:00:00Z"
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(doc))
    report = validate_file(path)
    assert any("observedAt precedes occurredAt" in issue.message for issue in report.issues)


def test_profile_rejects_unknown_transition_reference(tmp_path: Path) -> None:
    doc = json.loads((ROOT / "valid/foi-o-baseline.json").read_text())
    doc["transitions"][0]["toStateId"] = "foi-o/state/does-not-exist"
    path = tmp_path / "pic-process-profile" / "profile.json"
    path.parent.mkdir()
    path.write_text(json.dumps(doc))
    report = validate_file(path)
    assert any("unknown state ID" in issue.message for issue in report.issues)


def test_profile_rejects_unknown_actor_reference(tmp_path: Path) -> None:
    doc = json.loads((ROOT / "valid/foi-o-baseline.json").read_text())
    doc["events"][0]["actorId"] = "role/does-not-exist"
    path = tmp_path / "pic-process-profile" / "profile.json"
    path.parent.mkdir()
    path.write_text(json.dumps(doc))
    report = validate_file(path)
    assert any("unknown actor ID" in issue.message for issue in report.issues)


def test_profile_rejects_unknown_timer_start_event(tmp_path: Path) -> None:
    doc = json.loads((ROOT / "valid/foi-o-baseline.json").read_text())
    doc["timers"][0]["startEventId"] = "foi-o/event/does-not-exist"
    path = tmp_path / "pic-process-profile" / "profile.json"
    path.parent.mkdir()
    path.write_text(json.dumps(doc))
    report = validate_file(path)
    assert any("unknown event ID" in issue.message for issue in report.issues)


def test_profile_rejects_human_task_with_non_certified_decision(tmp_path: Path) -> None:
    doc = json.loads((ROOT / "valid/human-review.json").read_text())
    doc["events"][0]["kind"] = "proposed_action"
    path = tmp_path / "pic-process-profile" / "profile.json"
    path.parent.mkdir()
    path.write_text(json.dumps(doc))
    report = validate_file(path)
    assert any("certified human decision" in issue.message for issue in report.issues)


def test_profile_normalizes_trace_deterministically() -> None:
    doc = json.loads((ROOT / "valid/foi-o-baseline.json").read_text())
    first = normalize_trace(doc, "foi-o/trace/request.001")
    second = normalize_trace(doc, "foi-o/trace/request.001")
    assert first == second
    assert [event["id"] for event in first["events"]] == [
        "foi-o/event/request.received",
        "foi-o/event/response.deadline",
        "foi-o/event/request.closed",
    ]


def test_foi_candidate_profile_validates() -> None:
    path = (
        Path(__file__).parents[2]
        / ".."
        / "subrepos/process-mappings/profiles/foi/candidates/nz-oia-process-profile.json"
    )
    report = validate_file(path.resolve())
    assert report.ok, report.to_dict()
