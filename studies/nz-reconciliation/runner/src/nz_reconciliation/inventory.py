"""Load and filter the NZ reconciliation case inventory."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_INVENTORY = Path("studies/nz-reconciliation/fixtures/case-inventory.json")


def load_inventory(path: Path | None = None) -> dict[str, Any]:
    """Load the case inventory document."""
    inventory_path = path or DEFAULT_INVENTORY
    return json.loads(inventory_path.read_text(encoding="utf-8"))


def select_cases(
    inventory: dict[str, Any],
    *,
    domains: set[str] | None = None,
    include_blocked: bool = True,
) -> list[dict[str, Any]]:
    """Return inventory cases, optionally filtered by domain or compile status."""
    cases = list(inventory.get("cases") or [])
    if domains is not None:
        cases = [case for case in cases if case.get("domain") in domains]
    if not include_blocked:
        cases = [
            case for case in cases if (case.get("rulespec") or {}).get("compileStatus") == "ok"
        ]
    return cases
