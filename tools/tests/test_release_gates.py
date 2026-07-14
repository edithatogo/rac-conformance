from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from tools.release_gates import load_manifest, validate_manifest


FIXTURES = Path(__file__).parent / "fixtures" / "release_gates"


@pytest.mark.parametrize(
    "name,reason",
    [
        ("invalid-missing-evidence.json", "pass status requires evidence"),
        ("invalid-self-certified-adoption.json", "adoption cannot be self-certified"),
        ("invalid-stale-evidence.json", "expired evidence is stale"),
        ("invalid-ambiguous-status.json", "unknown status is invalid"),
    ],
)
def test_invalid_release_gate_manifests(name: str, reason: str) -> None:
    report = validate_manifest(load_manifest(FIXTURES / name), as_of=date(2026, 7, 15))

    assert not report.ok, reason
    assert report.errors


def test_valid_blocked_manifest_preserves_external_gate() -> None:
    report = validate_manifest(
        load_manifest(FIXTURES / "valid-blocked.json"), as_of=date(2026, 7, 15)
    )

    assert report.ok
    assert report.statuses == {"pass", "blocked"}


def test_valid_full_manifest_has_only_pass_gates() -> None:
    report = validate_manifest(
        load_manifest(FIXTURES / "valid-full.json"), as_of=date(2026, 7, 15)
    )

    assert report.ok
    assert report.statuses == {"pass"}


def test_human_report_is_deterministic() -> None:
    manifest = load_manifest(FIXTURES / "valid-blocked.json")

    first = validate_manifest(manifest, as_of=date(2026, 7, 15)).to_text()
    second = validate_manifest(json.loads(json.dumps(manifest)), as_of=date(2026, 7, 15)).to_text()

    assert first == second
