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
    assert primary["sourceStatus"] == "inherited-local-note-not-live-verified"
