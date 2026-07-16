"""Measure bounded PIC validation baselines from committed examples."""

from __future__ import annotations

import argparse
import json
import platform
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from pic_contracts.validation import validate_file

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "contracts/process-profile/0.1.0/examples/valid/foi-oia.json"
INVALID = ROOT / "contracts/process-profile/0.1.0/examples/invalid/missing-authority.json"

BUDGETS = {
    "small_valid_ms": 250,
    "small_invalid_ms": 250,
    "large_valid_ms": 1000,
    "deep_invalid_ms": 250,
    "large_document_bytes": 250_000,
    "deep_nesting": 64,
}


def _large_document() -> dict[str, Any]:
    document = json.loads(VALID.read_text(encoding="utf-8"))
    source_id = document["sourceAssertions"][0]["id"]
    actor_id = document["actors"][0]["id"]
    for index in range(100):
        state_id = f"synthetic/state-{index}"
        event_id = f"synthetic/event-{index}"
        document["states"].append(
            {
                "id": state_id,
                "kind": "intermediate",
                "label": f"Synthetic state {index}",
                "sourceAssertionIds": [source_id],
            }
        )
        document["events"].append(
            {
                "id": event_id,
                "kind": "observed_event",
                "eventType": "SyntheticEvent",
                "occurredAt": "2026-07-01T09:00:00Z",
                "observedAt": "2026-07-01T09:00:00Z",
                "actorId": actor_id,
                "sourceAssertionIds": [source_id],
                "evidenceReferenceIds": [],
            }
        )
    return document


def _deep_document() -> dict[str, Any]:
    document = json.loads(INVALID.read_text(encoding="utf-8"))
    nested: Any = {}
    for _ in range(BUDGETS["deep_nesting"]):
        nested = {"nested": nested}
    document["unexpected"] = nested
    return document


def _measure(name: str, document: dict[str, Any], expected_ok: bool, directory: Path) -> dict[str, Any]:
    path = directory / f"{name}.json"
    path.write_text(json.dumps(document, separators=(",", ":")), encoding="utf-8")
    started = time.perf_counter()
    report = validate_file(path)
    elapsed_ms = (time.perf_counter() - started) * 1000
    return {
        "name": name,
        "expectedOk": expected_ok,
        "observedOk": report.ok,
        "issueCount": len(report.issues),
        "elapsedMs": round(elapsed_ms, 3),
        "bytes": path.stat().st_size,
    }


def build_baseline() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="rac-v1-baseline-") as temporary:
        directory = Path(temporary)
        cases = [
            _measure("small-valid", json.loads(VALID.read_text(encoding="utf-8")), True, directory),
            _measure("small-invalid", json.loads(INVALID.read_text(encoding="utf-8")), False, directory),
            _measure("large-valid", _large_document(), True, directory),
            _measure("deep-invalid", _deep_document(), False, directory),
        ]
    return {
        "schemaVersion": "rac-v1-validation-baseline.v0.1.0",
        "observedAt": "2026-07-16",
        "reference": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "implementation": platform.python_implementation(),
            "validator": "pic_contracts.validation.validate_file",
        },
        "budgets": BUDGETS,
        "variancePolicy": "Timings are reference measurements. A budget increase requires a reviewed change to this artifact and a reason; missing or failed cases are not treated as passing.",
        "cases": cases,
        "result": "pass" if all(_case_passes(case) for case in cases) else "fail",
    }


def _case_passes(case: dict[str, Any]) -> bool:
    budget_key = {
        "small-valid": "small_valid_ms",
        "small-invalid": "small_invalid_ms",
        "large-valid": "large_valid_ms",
        "deep-invalid": "deep_invalid_ms",
    }[case["name"]]
    return (
        case["observedOk"] == case["expectedOk"]
        and case["elapsedMs"] <= BUDGETS[budget_key]
        and case["bytes"] <= BUDGETS["large_document_bytes"]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    baseline = build_baseline()
    rendered = json.dumps(baseline, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if baseline["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
