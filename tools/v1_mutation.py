"""Run a small deterministic mutation gate against stable validator oracles."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "contracts/process-profile/0.1.0/examples/valid/foi-oia.json"
SOURCE = ROOT / "contracts/tools/src/pic_contracts/validation.py"

MUTATIONS = [
    {
        "id": "contract-detection-guard",
        "old": "if contract is None:",
        "new": "if contract is not None:",
    },
    {
        "id": "event-reference-membership",
        "old": 'refs_exist("event", item["id"], [item["triggerEventId"]], event_by_id)',
        "new": "pass  # mutation: skip event reference check",
    },
    {
        "id": "rule-reference-membership",
        "old": 'refs_exist("trace", item["id"], [item["traceId"]], trace_by_id)',
        "new": "pass  # mutation: skip trace reference check",
    },
]


def _cases() -> list[tuple[str, dict[str, Any], bool]]:
    valid = json.loads(VALID.read_text(encoding="utf-8"))
    missing_process = json.loads(json.dumps(valid))
    del missing_process["profileId"]
    unknown_event = json.loads(json.dumps(valid))
    unknown_event["transitions"][0]["triggerEventId"] = "missing.event"
    unknown_rule = json.loads(json.dumps(valid))
    unknown_rule["ruleInvocations"][0]["traceId"] = "missing.trace"
    return [
        ("valid-profile", valid, True),
        ("missing-process", missing_process, False),
        ("unknown-event-state", unknown_event, False),
        ("unknown-rule-assertion", unknown_rule, False),
    ]


def _load_mutant(path: Path, identifier: str) -> Any:
    spec = importlib.util.spec_from_file_location(f"pic_validation_mutant_{identifier}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load mutant {identifier}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_mutations() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="rac-v1-mutants-") as temporary:
        directory = Path(temporary)
        source = SOURCE.read_text(encoding="utf-8")
        for mutation in MUTATIONS:
            if source.count(mutation["old"]) != 1:
                raise ValueError(f"mutation anchor is not unique: {mutation['id']}")
            mutant_path = directory / f"{mutation['id']}.py"
            mutant_path.write_text(source.replace(mutation["old"], mutation["new"]), encoding="utf-8")
            module = _load_mutant(mutant_path, mutation["id"])
            observed = []
            for name, document, expected_ok in _cases():
                document_path = directory / f"{mutation['id']}-{name}.json"
                document_path.write_text(json.dumps(document), encoding="utf-8")
                observed.append(
                    {
                        "case": name,
                        "expectedOk": expected_ok,
                        "observedOk": module.validate_file(document_path).ok,
                    }
                )
            killed = any(case["expectedOk"] != case["observedOk"] for case in observed)
            results.append({"id": mutation["id"], "killed": killed, "cases": observed})
    killed_count = sum(result["killed"] for result in results)
    return {
        "schemaVersion": "rac-v1-mutation-gate.v0.1.0",
        "source": str(SOURCE.relative_to(ROOT)),
        "oracle": "committed process-profile valid and invalid examples with reference checks",
        "threshold": {"minimumKilled": len(MUTATIONS), "equivalentMutants": 0},
        "mutations": results,
        "killed": killed_count,
        "result": "pass" if killed_count == len(MUTATIONS) else "fail",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_mutations()
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
