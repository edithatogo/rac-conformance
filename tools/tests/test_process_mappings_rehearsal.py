from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.process_mappings_rehearsal import _safe_destination, run_rehearsal


ROOT = Path(__file__).parents[2]


def test_extraction_rehearsal_produces_auditable_report(tmp_path: Path) -> None:
    report = run_rehearsal(ROOT, tmp_path / "report.json", require_clean=False)

    assert report["remoteCreated"] is False
    assert report["trackedFileCount"] > 0
    assert report["sourceCommit"]
    assert report["sourceTree"]
    assert report["historySplitCommit"]
    assert report["parentLicenseSha256"]
    assert {check["status"] for check in report["checks"]} >= {
        "pass",
        "deferred",
        "defined",
        "drafted",
        "not-applicable",
    }
    assert report["transformedLinks"] == ["LICENSE_BOUNDARY.md: ../../LICENSE -> LICENSE"]
    assert json.loads((tmp_path / "report.json").read_text(encoding="utf-8")) == report


@pytest.mark.parametrize("relative", [Path("../escape"), Path("/absolute"), Path("nested/../../escape")])
def test_extraction_rejects_paths_outside_target(tmp_path: Path, relative: Path) -> None:
    with pytest.raises(ValueError, match="unsafe extracted path"):
        _safe_destination(tmp_path, relative)


def test_extraction_resolves_normal_path_under_target(tmp_path: Path) -> None:
    assert _safe_destination(tmp_path, Path("profiles/foi/README.md")) == (
        tmp_path / "profiles/foi/README.md"
    ).resolve()
