"""Tests for the local process-mappings extraction rehearsal."""

from __future__ import annotations

from pathlib import Path

from tools.rehearse_process_mappings_extraction import rehearse


ROOT = Path(__file__).parents[2]


def test_extraction_rehearsal_preserves_history_and_stays_local() -> None:
    report = rehearse(ROOT)

    assert report["remoteCreated"] is False
    assert report["canonicalCutover"] is False
    assert report["subtreeCommit"]
    extracted = report["extracted"]
    assert extracted["commitCount"] >= 1
    assert extracted["requiredStandaloneCheck"] == "passed"
    assert extracted["gitFsck"] == "passed"
    assert extracted["writableSourceCount"] == 1
