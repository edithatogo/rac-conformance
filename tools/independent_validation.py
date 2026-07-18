"""Compatibility CLI for the canonical fail-closed evidence verifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.independent_evidence import KIT, _load_json, classify


def verify(kit: Path, result: Path) -> dict[str, object]:
    if kit.resolve() != KIT.resolve():
        return {
            "schemaValid": False,
            "evidenceVerified": False,
            "status": "rejected",
            "exceptions": ["only the canonical independent/kit is supported"],
            "qualifiesForV1": False,
            "expiresAt": None,
        }
    document = _load_json(result)
    return classify(document, evidence_root=result.parent)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kit", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = verify(args.kit, args.result)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        report = {
            "schemaValid": False,
            "evidenceVerified": False,
            "status": "rejected",
            "exceptions": [f"input: {exc}"],
            "qualifiesForV1": False,
            "expiresAt": None,
        }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["qualifiesForV1"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
