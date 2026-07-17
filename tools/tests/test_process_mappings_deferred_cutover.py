"""Regression checks for the staged process-mappings cutover decision."""

from pathlib import Path


ROOT = Path(__file__).parents[2]
TRACK = ROOT / "conductor/tracks/process_mappings_repository_20260714"


def test_staged_cutover_keeps_one_writable_parent_source() -> None:
    decision = (ROOT / "subrepos/process-mappings/migration/DEFERRED_CUTOVER_DECISION.md").read_text(encoding="utf-8")
    status = (ROOT / "subrepos/process-mappings/STATUS.md").read_text(encoding="utf-8")
    plan = (TRACK / "plan.md").read_text(encoding="utf-8")

    assert "public remote created and independently verified" in decision
    assert "parent subtree as authoritative" in decision
    assert "Destination remote: `edithatogo/process-mappings`" in status
    assert "HUMAN DECISION (2026-07-17)" in plan
    assert "Parent remains the only canonical writable" in plan
