"""Run the self-contained structural corpus without repository imports."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.json"


def verify_artifacts() -> list[dict[str, str]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    verified = []
    for artifact in manifest["artifacts"]:
        path = (ROOT / artifact["path"]).resolve()
        if ROOT.resolve() not in path.parents:
            raise ValueError(f"artifact escapes kit: {artifact['path']}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != artifact["sha256"]:
            raise ValueError(f"artifact digest mismatch: {artifact['path']}")
        verified.append(artifact)
    declared_bundle = {
        artifact["path"] for artifact in verified if artifact["path"].startswith("bundle/")
    }
    discovered_bundle = {
        str(path.relative_to(ROOT))
        for path in (ROOT / "bundle").rglob("*")
        if path.is_file()
    }
    if discovered_bundle != declared_bundle:
        raise ValueError("bundle contents do not match manifest")
    return verified


def digest_tree(artifacts: list[dict[str, str]]) -> str:
    digest = hashlib.sha256()
    for artifact in artifacts:
        digest.update(artifact["path"].encode())
        digest.update(b"\0")
        digest.update(artifact["sha256"].encode())
        digest.update(b"\n")
    return digest.hexdigest()


def run() -> dict:
    artifacts = verify_artifacts()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    schema_artifact = next(item for item in artifacts if item["role"] == "schema")
    schema = json.loads((ROOT / schema_artifact["path"]).read_text())
    validator = Draft202012Validator(schema)
    results = []
    for artifact in artifacts:
        if artifact["role"] not in {"valid", "invalid"}:
            continue
        expected_valid = artifact["role"] == "valid"
        document = json.loads((ROOT / artifact["path"]).read_text())
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        passed = not errors if expected_valid else bool(errors)
        results.append({"path": artifact["path"], "expectedValid": expected_valid, "passed": passed, "errorCount": len(errors)})
    return {
        "schemaVersion": "independent-kit-result.v1",
        "kitVersion": manifest["kitVersion"],
        "kitDigestSha256": digest_tree(artifacts),
        "tests": [
            {"caseId": result["path"], "status": "pass" if result["passed"] else "fail"}
            for result in results
        ],
        "details": results,
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
