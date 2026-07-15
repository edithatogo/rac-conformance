"""Keep the optional Camunda adapter isolated and reproducibly pinned."""

import json
from pathlib import Path

ROOT = Path(__file__).parents[3]
ADAPTER = ROOT / "subrepos/process-mappings/adapters/camunda"


def test_camunda_lock_is_optional_and_pinned() -> None:
    lock = json.loads((ADAPTER / "VERSION_LOCK.json").read_text())
    assert lock["camundaVersion"] == "8.9.12"
    assert lock["java"]["minimum"] == "17"
    assert lock["testFramework"]["name"] == "JUnit Jupiter 6.0.3 (JUnit 5 API)"
    assert lock["runtime"]["kind"] == "testcontainers"
    assert lock["normativeDependency"] is False
    assert lock["processTest"]["pomSha256"]
    assert lock["processTest"]["jarSha256"]


def test_camunda_adr_preserves_human_and_platform_boundaries() -> None:
    adr = (ADAPTER / "ARCHITECTURE_DECISION.md").read_text().lower()
    for phrase in (
        "pic schemas and validators remain usable without",
        "human tasks own legal, clinical, ethical",
        "substantive policy rules are not duplicated",
        "active-instance migration",
        "explicit element mappings and a wait-state test",
        "confidential commercial arrangements",
    ):
        assert phrase in adr
