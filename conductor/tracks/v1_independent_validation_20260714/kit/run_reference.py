"""Run the self-contained structural corpus without repository imports."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / "bundle" / "pic-semantics-0.1.0"


def digest_tree() -> str:
    digest = hashlib.sha256()
    for path in sorted(BUNDLE.rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(BUNDLE)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def run() -> dict:
    schema = json.loads((BUNDLE / "schema.json").read_text())
    validator = Draft202012Validator(schema)
    results = []
    for corpus, expected_valid in (("valid", True), ("invalid", False)):
        for path in sorted((BUNDLE / "examples" / corpus).glob("*.json")):
            document = json.loads(path.read_text())
            errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
            passed = not errors if expected_valid else bool(errors)
            results.append({"path": str(path.relative_to(ROOT)), "expectedValid": expected_valid, "passed": passed, "errorCount": len(errors)})
    return {
        "schemaVersion": "independent-kit-result.v1",
        "kitVersion": "independent-kit/0.1.0",
        "kitDigestSha256": digest_tree(),
        "results": results,
        "status": "pass" if all(result["passed"] for result in results) else "fail",
        "independenceStatus": "reference-runner-only",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8")
    else:
        print(result, end="")
    return 0 if json.loads(result)["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
