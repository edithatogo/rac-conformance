from __future__ import annotations

import json
from pathlib import Path

import pytest

from pic_contracts.process_mappings_consumption import validate_consumption

ROOT = Path(__file__).parents[3]
MANIFEST = ROOT / "subrepos" / "process-mappings" / "contracts" / "consumption.json"


def test_process_mappings_consumption_manifest_is_current() -> None:
    report = validate_consumption(MANIFEST, ROOT)

    assert report.ok, report.errors
    assert report.contract_version == "0.1.0"


def test_process_mappings_consumption_fails_on_drift(tmp_path: Path) -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    document["contract"]["schemaSha256"] = "0" * 64
    drifted = tmp_path / "consumption.json"
    drifted.write_text(json.dumps(document), encoding="utf-8")

    report = validate_consumption(drifted, ROOT)

    assert not report.ok
    assert any("schema digest" in error for error in report.errors)


@pytest.mark.parametrize(
    "relative",
    [
        "contracts/process-profile/0.1.0/examples/valid/foi-oia.json",
        "contracts/process-profile/0.1.0/examples/valid/human-review.json",
    ],
)
def test_pinned_contract_examples_are_valid(relative: str) -> None:
    report = validate_consumption(MANIFEST, ROOT)

    assert relative in report.validated_examples
