import json
from pathlib import Path

ROOT = Path(__file__).parents[3] / "subrepos" / "process-mappings" / "profiles" / "foi"


def test_foi_candidate_mappings_remain_agent_proposed() -> None:
    document = json.loads((ROOT / "PROFILE_CANDIDATES.json").read_text(encoding="utf-8"))

    assert document["method"] == "agent-proposed"
    assert document["reviewState"] == "candidate"
    assert document["mappings"]
    assert all(mapping["sourceRefs"] and mapping["loss"] for mapping in document["mappings"])


def test_foi_source_manifest_does_not_claim_live_primary_verification() -> None:
    document = json.loads((ROOT / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    primary = next(
        source for source in document["sources"] if source["kind"] == "primary-source-notes"
    )

    assert primary["reviewerState"] == "agent-proposed"
    assert primary["sourceStatus"].startswith("locator-verified-content-matched")


def test_foi_source_references_are_pinned_and_portable() -> None:
    candidates = json.loads((ROOT / "PROFILE_CANDIDATES.json").read_text(encoding="utf-8"))
    portability = json.loads(
        (ROOT / "SOURCE_REFERENCE_PORTABILITY.json").read_text(encoding="utf-8")
    )
    commit = portability["commit"]

    assert portability["contentMatch"] == "local-staged-bytes-match-pinned-upstream-bytes"
    assert all(
        ref.startswith(f"https://github.com/edithatogo/foi-o/blob/{commit}/")
        for mapping in candidates["mappings"]
        for ref in mapping["sourceRefs"]
    )
    assert all(item["sha256"] for item in portability["references"])


def test_foi_human_certification_template_covers_all_pending_rows() -> None:
    template = json.loads(
        (ROOT / "HUMAN_CERTIFICATION_DECISIONS.template.json").read_text(
            encoding="utf-8"
        )
    )
    ids = {item["id"] for item in template["decisions"]}
    assert len(ids) == 9
    assert all(item["outcome"] == "pending" for item in template["decisions"])
    assert template["reviewer"] is None
    assert set(template["allowedOutcomes"]) == {
        "approve-bounded",
        "limit",
        "reject",
        "defer",
    }
    assert "No fixture is promoted" in template["promotionStatement"]
