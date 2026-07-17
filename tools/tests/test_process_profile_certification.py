import json
from pathlib import Path

from tools.validate_process_profile_certification import (
    TRACK_ID,
    certification_record_path,
    validate,
    validate_document,
)


ROOT = Path(__file__).parents[2]
RECORD = certification_record_path(ROOT)


def test_certified_record_is_valid() -> None:
    assert validate(ROOT) == []
    assert json.loads(RECORD.read_text())["decision"] == "certified"


def test_certification_requires_reviewer_and_date() -> None:
    document = json.loads(RECORD.read_text())
    document["decision"] = "certified"
    document["reviewer"] = None
    document["reviewedAt"] = None
    errors = validate_document(ROOT, document)
    assert "certified decision requires reviewer and reviewedAt" in errors


def test_active_record_resolves(tmp_path: Path) -> None:
    record = tmp_path / "conductor" / "tracks" / TRACK_ID / "CERTIFICATION_RECORD.json"
    record.parent.mkdir(parents=True)
    record.write_text("{}", encoding="utf-8")
    assert certification_record_path(tmp_path) == record


def test_archived_record_resolves(tmp_path: Path) -> None:
    record = tmp_path / "conductor" / "archive" / TRACK_ID / "CERTIFICATION_RECORD.json"
    record.parent.mkdir(parents=True)
    record.write_text("{}", encoding="utf-8")
    assert certification_record_path(tmp_path) == record


def test_duplicate_records_fail_closed(tmp_path: Path) -> None:
    for location in ("tracks", "archive"):
        record = tmp_path / "conductor" / location / TRACK_ID / "CERTIFICATION_RECORD.json"
        record.parent.mkdir(parents=True)
        record.write_text("{}", encoding="utf-8")
    assert validate(tmp_path) == ["PIC process-profile certification record is ambiguous"]


def test_missing_record_fails_closed(tmp_path: Path) -> None:
    assert validate(tmp_path) == ["PIC process-profile certification record is missing"]
