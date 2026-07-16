"""Regression checks for the deferred process-mappings cutover decision."""

from pathlib import Path


ROOT = Path(__file__).parents[2]
TRACK = ROOT / "conductor/archive/process_mappings_repository_20260714"


def test_deferred_cutover_keeps_one_writable_parent_source() -> None:
    decision = (TRACK / "migration/DEFERRED_CUTOVER_DECISION.md").read_text(encoding="utf-8")
    status = (ROOT / "subrepos/process-mappings/STATUS.md").read_text(encoding="utf-8")
    plan = (TRACK / "plan.md").read_text(encoding="utf-8")

    assert "Do **not** create `edithatogo/process-mappings`" in decision
    assert "sole writable" in decision
    assert "Remote creation/cutover: deferred" in status
    assert "Task: [DEFERRED] Execute extraction" in plan
    assert "No remote or hosted control is created" in plan
