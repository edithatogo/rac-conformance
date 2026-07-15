#!/usr/bin/env python3
"""Clean-room JSON Schema corpus evaluator.

This file intentionally has no imports from the repository's production or
test packages. It is a small evidence tool, not a replacement validator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import warnings
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, RefResolver


CASES = (
    ("contracts/process-profile/0.1.0/schema.json", "valid", "foi-oia.json"),
    ("contracts/process-profile/0.1.0/schema.json", "valid", "human-review.json"),
    ("contracts/process-profile/0.1.0/schema.json", "invalid", "agent-controlling.json"),
    ("contracts/process-profile/0.1.0/schema.json", "invalid", "ambiguous-time.json"),
    ("contracts/process-profile/0.1.0/schema.json", "invalid", "bad-task-kind.json"),
    ("contracts/process-profile/0.1.0/schema.json", "invalid", "missing-authority.json"),
    ("contracts/pic-fixtures/0.1.0/schema.json", "valid", "missingness.json"),
    ("contracts/pic-fixtures/0.1.0/schema.json", "valid", "plain.json"),
    ("contracts/pic-fixtures/0.1.0/schema.json", "invalid", "bad-tolerance.json"),
    ("contracts/pic-fixtures/0.1.0/schema.json", "invalid", "float-money.json"),
    ("contracts/pic-fixtures/0.1.0/schema.json", "invalid", "missing-curator.json"),
    ("contracts/pic-traces/0.1.0/schema.json", "valid", "missingness-trace.json"),
    ("contracts/pic-traces/0.1.0/schema.json", "valid", "oia-response-deadline.json"),
    ("contracts/pic-traces/0.1.0/schema.json", "invalid", "bad-kind.json"),
    ("contracts/pic-traces/0.1.0/schema.json", "invalid", "bad-parameter-version.json"),
    ("contracts/pic-traces/0.1.0/schema.json", "invalid", "missing-conforms-to.json"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_value(repo: Path, *args: str) -> str:
    return subprocess.check_output(("git", *args), cwd=repo, text=True).strip()


def load_schema_registry(contracts: Path) -> dict[str, dict]:
    registry = {}
    for path in sorted(contracts.glob("*/**/schema.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        identifier = document.get("$id")
        if identifier:
            registry[identifier] = document
    return registry


def evaluate(repo: Path) -> dict:
    registry = load_schema_registry(repo / "contracts")
    results = []
    for schema_name, expected_kind, example_name in CASES:
        schema_path = repo / schema_name
        example_path = schema_path.parent / "examples" / expected_kind / example_name
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        instance = json.loads(example_path.read_text(encoding="utf-8"))
        # The repository is evaluated from committed local artifacts only.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            resolver = RefResolver.from_schema(schema, store=registry)
        validator = Draft202012Validator(
            schema, resolver=resolver, format_checker=FormatChecker()
        )
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
        observed = "valid" if not errors else "invalid"
        results.append(
            {
                "schema": schema_name,
                "schema_sha256": sha256(schema_path),
                "example": str(example_path.relative_to(repo)),
                "example_sha256": sha256(example_path),
                "expected": expected_kind,
                "observed": observed,
                "pass": observed == expected_kind,
                "error": errors[0].message if errors else None,
            }
        )
    return {
        "evaluation": {
            "status": "pass" if all(item["pass"] for item in results) else "fail",
            "internal_rehearsal": True,
            "qualifies_as_external_adoption": False,
            "qualifies_as_human_certification": False,
            "method": "jsonschema Draft 2020-12 validator with local $id registry and FormatChecker",
            "corpus_size": len(results),
            "valid_expected": sum(item["expected"] == "valid" for item in results),
            "invalid_expected": sum(item["expected"] == "invalid" for item in results),
        },
        "repository": {
            "commit": git_value(repo, "rev-parse", "HEAD"),
            "commit_short": git_value(repo, "rev-parse", "--short", "HEAD"),
            "clean_at_capture": not bool(git_value(repo, "status", "--porcelain")),
        },
        "environment": {
            "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "jsonschema": metadata.version("jsonschema"),
        },
        "evaluator": {
            "path": str(Path(__file__).resolve().relative_to(repo)),
            "sha256": sha256(Path(__file__).resolve()),
        },
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    report = evaluate(args.repo_root.resolve())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "RESULTS.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report["evaluation"], sort_keys=True))
    return 0 if report["evaluation"]["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
