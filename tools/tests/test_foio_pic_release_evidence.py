"""Validate the FOI-O/PIC papers handoff without overstating release readiness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_release_evidence_is_pinned_and_fail_closed() -> None:
    evidence = json.loads(
        (ROOT / "papers/foio-pic-release-evidence.json").read_text(encoding="utf-8")
    )
    assert evidence["schema_version"] == "foio-pic-release-evidence.v1.0.0"
    assert evidence["status"] == "blocked_pending_foio_v2_release"
    assert evidence["foio"]["published_release"] is None
    assert len(evidence["foio"]["observed_main_revision"]) == 40
    assert len(evidence["pic"]["contract_revision"]) == 40
    assert len(evidence["pic"]["schema_sha256"]) == 64
    assert len(evidence["pic"]["matrix_sha256"]) == 64

    dataset = evidence["derived_dataset"]
    assert dataset["platform"] == "huggingface"
    assert len(dataset["revision"]) == 40
    assert len(dataset["artifact_sha256"]) == 64
    assert dataset["provenance_status"] == "pinned_with_exceptions"
    assert dataset["exceptions"]

    assert evidence["promotion_gate"]["status"] == "pending_independent_oracle_review"
    assert "not evidence" in evidence["manuscript_boundary"]
