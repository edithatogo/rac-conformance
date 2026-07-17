from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "contracts/tools/src"))

from pic_contracts.process_profile import normalize_trace
from pic_contracts.validation import validate_file


ROOT = Path(__file__).parents[2] / "subrepos/process-mappings/profiles/health-technology/candidates"
PROFILES = sorted(ROOT.glob("*pembrolizumab-adjuvant.json"))


def test_candidate_profiles_validate_without_controlling_assertions() -> None:
    assert [path.stem for path in PROFILES] == [
        "nz-pembrolizumab-adjuvant",
        "uk-pembrolizumab-adjuvant",
    ]
    for path in PROFILES:
        document = json.loads(path.read_text(encoding="utf-8"))
        report = validate_file(path)
        assert report.ok, report.to_dict()
        assert all(not assertion["controlling"] for assertion in document["sourceAssertions"])
        assert document["states"][-1]["label"] == "Held for source and comparability review"
        assert document["exceptions"][0]["kind"] == "human_adjudication_required"


def test_candidate_traces_normalize_deterministically() -> None:
    for path in PROFILES:
        document = json.loads(path.read_text(encoding="utf-8"))
        trace_id = document["traces"][0]["id"]
        original_normalized = normalize_trace(document, trace_id)
        reordered_document = json.loads(path.read_text(encoding="utf-8"))
        reordered_document["events"].reverse()
        reordered_document["ruleInvocations"].reverse()
        assert normalize_trace(reordered_document, trace_id) == original_normalized


def test_candidate_profile_rejects_undated_controlling_assertion(tmp_path: Path) -> None:
    document = json.loads(PROFILES[0].read_text(encoding="utf-8"))
    document["sourceAssertions"][0]["controlling"] = True
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    report = validate_file(path)
    assert any("controlling assertion requires effectiveFrom" in issue.message for issue in report.issues)
