"""Deterministic validation for the v1 release-gate manifest."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

VALID_STATUSES = {"pass", "fail", "blocked", "exception", "not_applicable"}


@dataclass(frozen=True)
class ValidationReport:
    """Stable validation result suitable for CI and human review."""

    statuses: frozenset[str]
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_text(self) -> str:
        lines = ["v1 release-gate manifest", f"result: {'pass' if self.ok else 'fail'}"]
        lines.append("statuses: " + ", ".join(sorted(self.statuses)) if self.statuses else "statuses: none")
        lines.extend(f"error: {error}" for error in self.errors)
        return "\n".join(lines)


def load_manifest(path: Path) -> dict[str, Any]:
    """Load a JSON manifest and reject non-object roots."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root must be an object")
    return value


def _parse_date(value: Any, field: str, errors: list[str], gate_id: str) -> date | None:
    if not isinstance(value, str):
        errors.append(f"{gate_id}: {field} must be an ISO date")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{gate_id}: {field} must be an ISO date")
        return None


def validate_manifest(manifest: dict[str, Any], *, as_of: date) -> ValidationReport:
    """Validate a release-gate manifest without reading the current clock."""

    errors: list[str] = []
    if manifest.get("manifest_version") != "1":
        errors.append("manifest_version: expected '1'")
    if not isinstance(manifest.get("release"), str) or not manifest["release"]:
        errors.append("release: required non-empty string")

    gates = manifest.get("gates")
    if not isinstance(gates, list) or not gates:
        errors.append("gates: required non-empty array")
        return ValidationReport(frozenset(), tuple(errors))

    statuses: set[str] = set()
    seen_ids: set[str] = set()
    for gate in gates:
        if not isinstance(gate, dict):
            errors.append("gate: each entry must be an object")
    for gate in sorted(
        (item for item in gates if isinstance(item, dict)),
        key=lambda item: str(item.get("id", "")),
    ):
        gate_id = gate.get("id")
        if not isinstance(gate_id, str) or not gate_id:
            errors.append("gate: id required")
            gate_id = "<missing-id>"
        elif gate_id in seen_ids:
            errors.append(f"{gate_id}: duplicate id")
        seen_ids.add(gate_id)

        status = gate.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{gate_id}: status must be one of {sorted(VALID_STATUSES)}")
            continue
        statuses.add(status)
        for field in ("owner", "category"):
            if not isinstance(gate.get(field), str) or not gate[field]:
                errors.append(f"{gate_id}: {field} required")
        observed = _parse_date(gate.get("observed_at"), "observed_at", errors, gate_id)
        expires = None
        if "expires_at" in gate:
            expires = _parse_date(gate["expires_at"], "expires_at", errors, gate_id)
        if expires is not None and expires < as_of:
            errors.append(f"{gate_id}: evidence is stale")
        if observed is not None and observed > as_of:
            errors.append(f"{gate_id}: observed_at is in the future")

        evidence = gate.get("evidence")
        if status == "pass":
            if not isinstance(evidence, list) or not evidence:
                errors.append(f"{gate_id}: pass status requires evidence")
            else:
                for index, item in enumerate(evidence):
                    if not isinstance(item, dict) or not (item.get("url") or item.get("digest")):
                        errors.append(f"{gate_id}: evidence[{index}] requires url or digest")
                    elif "observed_at" not in item:
                        errors.append(f"{gate_id}: evidence[{index}] requires observed_at")
        if status == "pass" and gate.get("category") == "adoption" and gate.get("independent") is not True:
            errors.append(f"{gate_id}: adoption cannot be self-certified")
        if status in {"blocked", "fail"}:
            for field in ("reason_code", "next_action"):
                if not isinstance(gate.get(field), str) or not gate[field]:
                    errors.append(f"{gate_id}: {status} status requires {field}")
        if status == "exception":
            for field in ("reason_code", "next_action", "review_by", "approval"):
                if not isinstance(gate.get(field), str) or not gate[field]:
                    errors.append(f"{gate_id}: exception status requires {field}")
        if status == "not_applicable" and not isinstance(gate.get("reason_code"), str):
            errors.append(f"{gate_id}: not_applicable status requires reason_code")

    return ValidationReport(frozenset(statuses), tuple(sorted(errors)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a v1 release-gate manifest")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--as-of", required=True, type=date.fromisoformat)
    args = parser.parse_args(argv)
    report = validate_manifest(load_manifest(args.manifest), as_of=args.as_of)
    print(report.to_text())
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
