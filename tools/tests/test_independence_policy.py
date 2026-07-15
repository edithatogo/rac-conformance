from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_independence_criteria_are_explicit_and_fail_closed() -> None:
    criteria = json.loads(
        (ROOT / "conductor" / "tracks" / "v1_independent_validation_20260714" / "INDEPENDENCE_CRITERIA.json").read_text()
    )
    assert len(criteria["requiredDimensions"]) == 8
    assert "qualifying" in criteria["outcomes"]
    assert set(criteria["nonQualifyingStatuses"]) >= {
        "internal-rehearsal",
        "unacknowledged",
        "maintainer-fork",
    }
    assert criteria["v1Gate"]["silenceCountsAsAdoption"] is False
    assert criteria["v1Gate"]["maintainerForkCountsAsIndependent"] is False
    assert criteria["v1Gate"]["agentRehearsalCountsAsIndependent"] is False


def test_policy_names_the_external_evidence_boundary() -> None:
    policy = (ROOT / "docs" / "INDEPENDENT_VALIDATION_POLICY.md").read_text()
    for phrase in ("separately controlled", "silence is not acceptance", "internal-rehearsal", "Screenshots"):
        assert phrase in policy
