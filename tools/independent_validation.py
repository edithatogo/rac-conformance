"""Verify independent-validation result structure and gate eligibility."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def verify(kit: Path, result: Path) -> dict[str, object]:
    manifest = json.loads((kit / "manifest.json").read_text(encoding="utf-8"))
    document = json.loads(result.read_text(encoding="utf-8"))
    schema = json.loads((kit / "result.schema.json").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda item: list(item.path))
    diagnostics = ["/".join(map(str, error.path)) + ": " + error.message for error in errors]
    if document.get("implementation", {}).get("maintainerControlled"):
        diagnostics.append("implementation is maintainer-controlled")
    if not document.get("oracle", {}).get("independent"):
        diagnostics.append("oracle is not independent")
    if document.get("outcome") == "qualifying" and not document.get("evidence", {}).get("acknowledged"):
        diagnostics.append("qualifying result lacks maintainer acknowledgement")
    return {"ok": not diagnostics, "diagnostics": diagnostics, "kitVersion": manifest["kitVersion"], "resultSha256": hashlib.sha256(result.read_bytes()).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kit", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    report = verify(args.kit, args.result)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
