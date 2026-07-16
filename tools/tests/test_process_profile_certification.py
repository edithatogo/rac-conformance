import json
from pathlib import Path

from tools.validate_process_profile_certification import validate, validate_document


ROOT = Path(__file__).parents[2]
RECORD = ROOT / "conductor/tracks/pic_process_profile_20260714/CERTIFICATION_RECORD.json"


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
