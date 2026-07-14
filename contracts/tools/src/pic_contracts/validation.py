"""PIC artifact validation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from jsonschema import ValidationError as JsonSchemaValidationError

from pic_contracts.parameters import validate_parameter_periods
from pic_contracts.schema_utils import load_json, validator_for

CONFORMS_TO_CONTRACT = {
    "pic-crosswalk/0.1.0": "pic-crosswalk",
    "pic-parameters/0.1.0": "pic-parameters",
    "pic-parameters/0.2.0": "pic-parameters",
    "pic-fixtures/0.1.0": "pic-fixtures",
    "pic-traces/0.1.0": "pic-traces",
    "pic-traces/0.2.0": "pic-traces",
    "pic-foio-compatibility/0.1.0": "pic-foio-compatibility",
}


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str
    code: str = "validation"


@dataclass
class ValidationReport:
    ok: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)

    def add(self, issue: ValidationIssue) -> None:
        self.ok = False
        self.issues.append(issue)

    def extend(self, issues: list[ValidationIssue]) -> None:
        for issue in issues:
            self.add(issue)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "issues": [
                {"path": issue.path, "code": issue.code, "message": issue.message}
                for issue in self.issues
            ],
        }


def detect_contract(doc: dict[str, Any], path: Path | None = None) -> str | None:
    conforms_to = doc.get("conformsTo")
    if isinstance(conforms_to, str) and conforms_to in CONFORMS_TO_CONTRACT:
        return CONFORMS_TO_CONTRACT[conforms_to]
    if "valueState" in doc:
        return "pic-semantics"
    if path is not None:
        for part in path.parts:
            if part in {
                "pic-semantics",
                "pic-crosswalk",
                "pic-parameters",
                "pic-fixtures",
                "pic-traces",
                "pic-foio-compatibility",
            }:
                return part
    return None


def _format_schema_error(error: JsonSchemaValidationError) -> str:
    location = "/".join(map(str, error.path))
    prefix = f"{location}: " if location else ""
    return f"{prefix}{error.message}"


def validate_file(path: Path) -> ValidationReport:
    report = ValidationReport()
    try:
        doc = load_json(path)
    except json.JSONDecodeError as exc:
        report.add(ValidationIssue(str(path), f"invalid JSON: {exc}", "json"))
        return report
    if not isinstance(doc, dict):
        report.add(ValidationIssue(str(path), "PIC artifact must be a JSON object", "type"))
        return report
    contract = detect_contract(doc, path)
    if contract is None:
        report.add(ValidationIssue(str(path), "could not detect PIC contract type", "type"))
        return report
    conforms_to = doc.get("conformsTo")
    version = "0.1.0"
    if isinstance(conforms_to, str) and "/" in conforms_to:
        version = conforms_to.split("/")[-1]
    validator = validator_for(contract, version)
    for error in sorted(validator.iter_errors(doc), key=lambda item: list(item.path)):
        report.add(ValidationIssue(str(path), _format_schema_error(error), "schema"))
    if contract == "pic-parameters":
        for error in validate_parameter_periods(doc):
            report.add(ValidationIssue(f"{path}:{error.path}", error.message, "period"))
    return report


def _json_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(
        item
        for item in path.rglob("*.json")
        if item.is_file() and ".venv" not in item.parts
    )


def _infer_value_data_type(value_object: dict[str, Any]) -> str | None:
    if "currency" in value_object:
        return "money"
    value = value_object.get("value")
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, str):
        try:
            date.fromisoformat(value)
        except ValueError:
            pass
        else:
            return "date"
        numeric = value.replace("-", "", 1).replace(".", "", 1).isdigit()
        if value_object.get("valueState") == "known" and numeric:
            return "decimal"
        return "string"
    return None


def _collect_docs(paths: list[Path]) -> list[tuple[Path, str, dict[str, Any]]]:
    docs = []
    for path in paths:
        doc = load_json(path)
        if not isinstance(doc, dict):
            continue
        contract = detect_contract(doc, path)
        if contract is not None:
            docs.append((path, contract, doc))
    return docs


def _referential_integrity(paths: list[Path]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    docs = _collect_docs(paths)
    crosswalk_types: dict[str, str] = {}
    parameter_ids: set[str] = set()
    for _, contract, doc in docs:
        if contract == "pic-crosswalk":
            for row in doc.get("rows", []):
                crosswalk_types[row.get("id", "")] = row.get("dataType", "")
        elif contract == "pic-parameters":
            for parameter in doc.get("parameters", []):
                parameter_ids.add(parameter.get("id", ""))

    for path, contract, doc in docs:
        if contract == "pic-fixtures":
            for case_index, case in enumerate(doc.get("cases", [])):
                for pic_id, value_object in case.get("inputs", {}).items():
                    if pic_id not in crosswalk_types:
                        issues.append(
                            ValidationIssue(
                                f"{path}:cases/{case_index}/inputs/{pic_id}",
                                "fixture references unknown crosswalk ID",
                                "reference",
                            )
                        )
                        continue
                    expected_type = crosswalk_types[pic_id]
                    actual_type = _infer_value_data_type(value_object)
                    if actual_type is not None and expected_type != actual_type:
                        issues.append(
                            ValidationIssue(
                                f"{path}:cases/{case_index}/inputs/{pic_id}",
                                "type mismatch: "
                                f"crosswalk={expected_type} fixture={actual_type}",
                                "type",
                            )
                        )
        elif contract == "pic-traces":
            for step_index, step in enumerate(doc.get("steps", [])):
                for version_index, parameter in enumerate(step.get("parameterVersions", [])):
                    parameter_id = parameter.get("id")
                    if parameter_id not in parameter_ids:
                        issues.append(
                            ValidationIssue(
                                f"{path}:steps/{step_index}/parameterVersions/{version_index}",
                                "trace references unknown parameter ID",
                                "reference",
                            )
                        )
    return issues


def validate_path(path: Path, *, check_references: bool = True) -> ValidationReport:
    report = ValidationReport()
    json_paths = _json_files(path)
    if not json_paths:
        report.add(ValidationIssue(str(path), "no JSON files found", "input"))
        return report
    for json_path in json_paths:
        report.extend(validate_file(json_path).issues)
    if path.is_dir() and check_references:
        report.extend(_referential_integrity(json_paths))
    return report
