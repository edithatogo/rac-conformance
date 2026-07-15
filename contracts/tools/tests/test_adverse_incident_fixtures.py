from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[3]
SCHEMA = json.loads(
    (ROOT / "contracts/process-profile/0.1.0/schema.json").read_text(encoding="utf-8")
)
MODULE_PATH = ROOT / "tools/generate_adverse_incident_fixtures.py"
MODULE_SPEC = importlib.util.spec_from_file_location("adverse_incident_fixtures", MODULE_PATH)
assert MODULE_SPEC and MODULE_SPEC.loader
MODULE = importlib.util.module_from_spec(MODULE_SPEC)
sys.modules[MODULE_SPEC.name] = MODULE
MODULE_SPEC.loader.exec_module(MODULE)


def test_generated_corpus_is_synthetic_and_schema_valid(tmp_path) -> None:
    output_dir = tmp_path / "profiles"
    MODULE.write_corpus(output_dir)
    paths = sorted(output_dir.glob("*.json"))

    assert {path.stem for path in paths} == {scenario[0] for scenario in MODULE.SCENARIOS}
    validator = Draft202012Validator(SCHEMA)
    for path in paths:
        profile = json.loads(path.read_text(encoding="utf-8"))
        assert profile["case"]["synthetic"] is True
        assert all(
            assertion["reviewerState"] == "agent-proposed"
            for assertion in profile["sourceAssertions"]
        )
        assert all(
            not assertion["controlling"] for assertion in profile["sourceAssertions"]
        )
        assert any(
            transition["toStateId"].endswith(":closed")
            for transition in profile["transitions"]
        )
        assert any(
            "culturally-responsive-participation-support" in task["id"]
            for task in profile["humanTasks"]
        )
        assert list(validator.iter_errors(profile)) == []


def test_blocked_source_fixture_fails_closed() -> None:
    profile = MODULE.build_profile(MODULE.SCENARIOS[-1])

    assert profile["sourceAssertions"][0]["sourceStatus"] == "blocked"
    assert profile["humanTasks"][0]["kind"] == "human_review"


def test_parallel_complaint_fixture_has_parallel_pathway() -> None:
    profile = MODULE.build_profile(MODULE.SCENARIOS[4])

    assert any(
        state["id"].endswith(":parallel-pathway") for state in profile["states"]
    )


def test_human_review_template_matches_resolver_queue() -> None:
    template_path = (
        ROOT
        / "subrepos/process-mappings/profiles/adverse-incidents/"
        "HUMAN_REVIEW_DECISIONS.template.json"
    )
    template = json.loads(
        template_path.read_text(encoding="utf-8")
    )

    assert template["status"] == "partially-reviewed"
    assert {item["mappingId"] for item in template["decisions"]} == {
        "mapping.nz.consumer-informed",
        "mapping.nz.review-learning",
        "mapping.au.open-disclosure",
        "mapping.nsw.incident-review",
        "mapping.au.secondary-summary",
        "mapping.local.escalation",
    }
    decisions = {item["mappingId"]: item["decision"] for item in template["decisions"]}
    assert decisions["mapping.nz.consumer-informed"] == "approved"
    assert all(
        decision is None
        for mapping_id, decision in decisions.items()
        if mapping_id != "mapping.nz.consumer-informed"
    )
