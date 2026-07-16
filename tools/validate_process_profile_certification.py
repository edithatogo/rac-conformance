"""Validate the PIC process-profile human certification record."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DECISIONS = {"pending", "certified", "rejected", "changes-requested"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_document(root: Path, document: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if document.get("schemaVersion") != "pic-process-profile-certification.v0.1.0":
        errors.append("unsupported certification schema")
    decision = document.get("decision")
    if decision not in DECISIONS:
        errors.append("decision is invalid")
    candidate = document.get("candidate", {})
    contract = document.get("contract", {})
    for label, item in (("candidate", candidate), ("contract", contract)):
        path = root / item.get("path", "")
        digest = item.get("sha256")
        if not path.is_file():
            errors.append(f"{label} artifact is missing")
        elif _sha256(path) != digest:
            errors.append(f"{label} digest does not match the checked-in artifact")
    if decision == "certified":
        if not document.get("reviewer") or not document.get("reviewedAt"):
            errors.append("certified decision requires reviewer and reviewedAt")
    elif document.get("reviewer") or document.get("reviewedAt"):
        errors.append("non-certified decision cannot contain certification identity")
    return errors


def validate(root: Path) -> list[str]:
    record_path = root / "conductor/tracks/pic_process_profile_20260714/CERTIFICATION_RECORD.json"
    return validate_document(root, json.loads(record_path.read_text(encoding="utf-8")))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    errors = validate(Path(args.root))
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("OK: PIC process-profile certification record")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
