import json
from pathlib import Path
import subprocess
import sys

from jsonschema import Draft202012Validator

from tools.independent_validation import verify


ROOT = Path(__file__).parents[2]
KIT = ROOT / "independent/kit"


def test_canonical_kit_is_unique_and_bundle_matches_contract() -> None:
    assert not (ROOT / "conductor/tracks/v1_independent_validation_20260714/kit").exists()
    manifest = json.loads((KIT / "manifest.json").read_text())
    for artifact in manifest["artifacts"]:
        if not artifact["path"].startswith("bundle/"):
            continue
        bundled = KIT / artifact["path"]
        canonical = ROOT / "contracts/pic-semantics/0.1.0" / bundled.relative_to(
            KIT / "bundle/pic-semantics-0.1.0"
        )
        assert bundled.read_bytes() == canonical.read_bytes()


def test_reference_runner_is_self_contained(tmp_path: Path) -> None:
    output = tmp_path / "results.json"
    completed = subprocess.run(
        [sys.executable, "run_reference.py", "--output", str(output)],
        cwd=KIT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads(output.read_text())
    assert result["status"] == "pass"
    assert result["kitVersion"] == "independent-kit/0.2.0"
    assert result["details"]
    assert result["tests"] == [
        {"caseId": item["path"], "status": "pass" if item["passed"] else "fail"}
        for item in result["details"]
    ]


def test_reference_runner_rejects_unmanifested_corpus_file(tmp_path: Path) -> None:
    copied = tmp_path / "kit"
    import shutil

    shutil.copytree(KIT, copied)
    extra = copied / "bundle/pic-semantics-0.1.0/examples/valid/extra.json"
    extra.write_text("{}")
    completed = subprocess.run(
        [sys.executable, "run_reference.py"],
        cwd=copied,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "bundle contents do not match manifest" in completed.stderr


def test_legacy_example_cannot_qualify() -> None:
    report = verify(KIT, KIT / "example-nonqualifying-result.json")
    assert report["status"] == "rejected"
    assert report["qualifiesForV1"] is False


def test_kit_result_schema_matches_submission_contract() -> None:
    canonical = ROOT / "conductor/tracks/v1_independent_validation_20260714/SUBMISSION_SCHEMA.json"
    assert (KIT / "result.schema.json").read_bytes() == canonical.read_bytes()


def test_submission_template_is_schema_valid_but_nonqualifying() -> None:
    schema = json.loads((KIT / "result.schema.json").read_text())
    template = json.loads((KIT / "submission-template.json").read_text())
    assert list(Draft202012Validator(schema).iter_errors(template)) == []
    report = verify(KIT, KIT / "submission-template.json")
    assert report["qualifiesForV1"] is False


def test_compatibility_verifier_rejects_noncanonical_kit(tmp_path: Path) -> None:
    report = verify(tmp_path, KIT / "example-nonqualifying-result.json")
    assert report["status"] == "rejected"
    assert "only the canonical independent/kit is supported" in report["exceptions"]
