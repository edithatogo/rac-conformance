"""Run a bounded, deterministic mutation corpus against PIC validation."""

from __future__ import annotations

import argparse
import copy
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from pic_contracts.validation import validate_file

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "contracts/process-profile/0.1.0/examples/valid/foi-oia.json"


def _mutations(document: dict[str, Any]) -> list[tuple[str, dict[str, Any], bool]]:
    cases: list[tuple[str, dict[str, Any], bool]] = []

    missing_process = copy.deepcopy(document)
    del missing_process["profileId"]
    cases.append(("missing-required-process", missing_process, False))

    bad_state_kind = copy.deepcopy(document)
    bad_state_kind["states"][0]["kind"] = "runtime-ai"
    cases.append(("unsupported-state-kind", bad_state_kind, False))

    unknown_reference = copy.deepcopy(document)
    unknown_reference["transitions"][0]["toStateId"] = "state-does-not-exist"
    cases.append(("unknown-state-reference", unknown_reference, False))

    hostile_string = copy.deepcopy(document)
    hostile_string["profileId"] = "<script>alert('x')</script>\n$(touch /tmp/nope)"
    cases.append(("hostile-string", hostile_string, False))

    oversized_decimal = copy.deepcopy(document)
    oversized_decimal["states"].append(
        {
            "id": "synthetic/state.large",
            "kind": "intermediate",
            "label": "Large synthetic state",
            "sourceAssertionIds": [document["sourceAssertions"][0]["id"]],
        }
    )
    oversized_decimal["profileId"] = "a" * 10_000
    cases.append(("large-identifier-valid", oversized_decimal, True))

    deep = copy.deepcopy(document)
    nested: Any = {}
    for _ in range(64):
        nested = {"nested": nested}
    deep["unexpected"] = nested
    cases.append(("deep-unknown-value", deep, False))
    return cases


def run_corpus() -> dict[str, Any]:
    document = json.loads(SOURCE.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="rac-v1-fuzz-") as temporary:
        directory = Path(temporary)
        for name, mutation, expected_ok in _mutations(document):
            path = directory / f"{name}.json"
            path.write_text(json.dumps(mutation), encoding="utf-8")
            report = validate_file(path)
            results.append(
                {
                    "name": name,
                    "expectedOk": expected_ok,
                    "observedOk": report.ok,
                    "issueCount": len(report.issues),
                    "diagnosticCodes": sorted({issue.code for issue in report.issues}),
                }
            )
    return {
        "schemaVersion": "rac-v1-validation-fuzz.v0.1.0",
        "seed": "committed-example:contracts/process-profile/0.1.0/examples/valid/foi-oia.json",
        "mutationCount": len(results),
        "bounds": {"maxMutations": 6, "maxDepth": 64, "maxIdentifierLength": 10000},
        "results": results,
        "result": "pass"
        if all(item["observedOk"] == item["expectedOk"] for item in results)
        else "fail",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    corpus = run_corpus()
    rendered = json.dumps(corpus, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if corpus["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
