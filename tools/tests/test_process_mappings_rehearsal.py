from __future__ import annotations

import json
from pathlib import Path

from tools.process_mappings_rehearsal import run_rehearsal


ROOT = Path(__file__).parents[2]


def test_extraction_rehearsal_produces_auditable_report(tmp_path: Path) -> None:
    report = run_rehearsal(ROOT, tmp_path / "report.json")

    assert report["remoteCreated"] is False
    assert report["trackedFileCount"] > 0
    assert report["sourceCommit"]
    assert report["sourceTree"]
    assert report["parentLicenseSha256"]
    assert {check["status"] for check in report["checks"]} >= {"pass", "deferred", "defined"}
    assert report["transformedLinks"] == ["LICENSE_BOUNDARY.md: ../../LICENSE -> LICENSE"]
    assert json.loads((tmp_path / "report.json").read_text(encoding="utf-8")) == report
