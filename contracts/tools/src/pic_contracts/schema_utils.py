"""Schema loading helpers for PIC contract tests and tooling."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from pic_contracts.safety import load_bounded_json

REPO_ROOT = Path(__file__).resolve().parents[4]
CONTRACTS_ROOT = REPO_ROOT / "contracts"


def load_json(path: Path) -> dict[str, Any]:
    return load_bounded_json(path)


def load_schema(contract: str, version: str = "0.1.0") -> dict[str, Any]:
    return load_json(CONTRACTS_ROOT / contract / version / "schema.json")


def schema_registry() -> Registry:
    resources = []
    for schema_path in CONTRACTS_ROOT.glob("pic-*/*/schema.json"):
        schema = load_json(schema_path)
        if "$id" in schema:
            resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def validator_for(contract: str, version: str = "0.1.0") -> Draft202012Validator:
    schema = load_schema(contract, version)
    return Draft202012Validator(schema, registry=schema_registry())
