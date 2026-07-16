"""PIC artifact validation."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

from jsonschema import ValidationError as JsonSchemaValidationError

from pic_contracts.parameters import validate_parameter_periods
from pic_contracts.safety import SafetyLimitError
from pic_contracts.schema_utils import load_json, validator_for

CONFORMS_TO_CONTRACT = {
    "pic-crosswalk/0.1.0": "pic-crosswalk",
    "pic-parameters/0.1.0": "pic-parameters",
    "pic-parameters/0.2.0": "pic-parameters",
    "pic-fixtures/0.1.0": "pic-fixtures",
    "pic-traces/0.1.0": "pic-traces",
    "pic-traces/0.2.0": "pic-traces",
    "pic-foio-compatibility/0.1.0": "pic-foio-compatibility",
    "pic-process-profile/0.1.0": "process-profile",
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
                "process-profile",
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
    except (json.JSONDecodeError, SafetyLimitError, OSError, UnicodeDecodeError) as exc:
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
    if contract == "pic-foio-compatibility" and report.ok:
        report.extend(_compatibility_semantics(path, doc))
    if contract == "process-profile" and report.ok:
        report.extend(_process_profile_semantics(path, doc))
    if contract == "pic-parameters":
        for error in validate_parameter_periods(doc):
            report.add(ValidationIssue(f"{path}:{error.path}", error.message, "period"))
    return report


def _process_profile_semantics(path: Path, doc: dict[str, Any]) -> list[ValidationIssue]:
    """Check cross-record process invariants that JSON Schema cannot express."""
    issues: list[ValidationIssue] = []
    source_by_id = {item["id"]: item for item in doc["sourceAssertions"]}
    actor_by_id = {item["id"]: item for item in doc["actors"]}
    state_by_id = {item["id"]: item for item in doc["states"]}
    event_by_id = {item["id"]: item for item in doc["events"]}
    timer_by_id = {item["id"]: item for item in doc["timers"]}
    task_by_id = {item["id"]: item for item in doc["tasks"]}
    invocation_by_id = {item["id"]: item for item in doc["ruleInvocations"]}
    evidence_by_id = {item["id"]: item for item in doc["evidenceReferences"]}
    trace_by_id = {item["id"]: item for item in doc["traces"]}

    def unique(kind: str, records: list[dict[str, Any]]) -> None:
        ids = [record["id"] for record in records]
        if len(ids) != len(set(ids)):
            issues.append(ValidationIssue(str(path), f"duplicate {kind} ID", "reference"))

    def refs_exist(kind: str, owner: str, refs: list[str], records: dict[str, Any]) -> None:
        for ref in refs:
            if ref not in records:
                issues.append(
                    ValidationIssue(f"{path}:{owner}", f"unknown {kind} ID: {ref}", "reference")
                )

    for kind, records in (
        ("source assertion", doc["sourceAssertions"]),
        ("actor", doc["actors"]),
        ("state", doc["states"]),
        ("event", doc["events"]),
        ("timer", doc["timers"]),
        ("task", doc["tasks"]),
        ("rule invocation", doc["ruleInvocations"]),
        ("evidence reference", doc["evidenceReferences"]),
        ("trace", doc["traces"]),
    ):
        unique(kind, records)

    for assertion in doc["sourceAssertions"]:
        if assertion["controlling"]:
            eligible = (
                assertion["sourceType"] == "official_primary"
                or assertion["reviewStatus"] == "human-approved"
            )
            if not eligible:
                issues.append(
                    ValidationIssue(
                        f"{path}:sourceAssertions/{assertion['id']}",
                        "controlling assertion must be official primary or human-approved",
                        "authority",
                    )
                )
            if assertion["effectiveFrom"] is None:
                issues.append(
                    ValidationIssue(
                        f"{path}:sourceAssertions/{assertion['id']}",
                        "controlling assertion requires effectiveFrom",
                        "time",
                    )
                )
        if assertion["effectiveFrom"] and assertion["effectiveTo"] and date.fromisoformat(
            assertion["effectiveTo"]
        ) < date.fromisoformat(assertion["effectiveFrom"]):
            issues.append(
                ValidationIssue(
                    f"{path}:sourceAssertions/{assertion['id']}",
                    "effectiveTo precedes effectiveFrom",
                    "time",
                )
            )

    for item in doc["states"]:
        refs_exist("source assertion", item["id"], item.get("sourceAssertionIds", []), source_by_id)
    for item in doc["actors"]:
        refs_exist(
            "source assertion",
            item["id"],
            item.get("authoritySourceAssertionIds", []),
            source_by_id,
        )
    for item in doc["events"]:
        refs_exist("actor", item["id"], [item["actorId"]], actor_by_id)
        if item.get("timerId"):
            refs_exist("timer", item["id"], [item["timerId"]], timer_by_id)
        refs_exist("source assertion", item["id"], item["sourceAssertionIds"], source_by_id)
        refs_exist(
            "evidence reference", item["id"], item.get("evidenceReferenceIds", []), evidence_by_id
        )
        occurred = datetime.fromisoformat(item["occurredAt"].replace("Z", "+00:00"))
        observed = datetime.fromisoformat(item["observedAt"].replace("Z", "+00:00"))
        if observed < occurred:
            issues.append(
                ValidationIssue(
                    f"{path}:events/{item['id']}", "observedAt precedes occurredAt", "time"
                )
            )
    for item in doc["timers"]:
        refs_exist("event", item["id"], [item["startEventId"]], event_by_id)
        refs_exist("source assertion", item["id"], item["sourceAssertionIds"], source_by_id)
    for item in doc["transitions"]:
        refs_exist("state", item["id"], [item["fromStateId"], item["toStateId"]], state_by_id)
        refs_exist("event", item["id"], [item["triggerEventId"]], event_by_id)
        refs_exist("task", item["id"], [item["taskId"]], task_by_id) if item.get("taskId") else None
        refs_exist("source assertion", item["id"], item.get("sourceAssertionIds", []), source_by_id)
    for item in doc["tasks"]:
        refs_exist("source assertion", item["id"], item.get("sourceAssertionIds", []), source_by_id)
        if item["kind"] == "human_task" and "ruleInvocationId" in item:
            issues.append(
                ValidationIssue(
                    f"{path}:tasks/{item['id']}",
                    "human task cannot reference a rule invocation",
                    "task-kind",
                )
            )
        if item["kind"] == "deterministic_rule_task" and "ruleInvocationId" not in item:
            issues.append(
                ValidationIssue(
                    f"{path}:tasks/{item['id']}",
                    "deterministic rule task requires a rule invocation",
                    "task-kind",
                )
            )
        if item.get("ruleInvocationId"):
            refs_exist("rule invocation", item["id"], [item["ruleInvocationId"]], invocation_by_id)
        if item.get("decisionEventId"):
            refs_exist("event", item["id"], [item["decisionEventId"]], event_by_id)
            if (
                item["kind"] == "human_task"
                and item["decisionEventId"] in event_by_id
                and event_by_id[item["decisionEventId"]]["kind"] != "certified_human_decision"
            ):
                issues.append(
                    ValidationIssue(
                        f"{path}:tasks/{item['id']}",
                        "human task decisionEventId must identify a certified human decision",
                        "task-kind",
                    )
                )
    for item in doc["ruleInvocations"]:
        refs_exist("trace", item["id"], [item["traceId"]], trace_by_id)
    for item in doc["evidenceReferences"]:
        refs_exist("source assertion", item["id"], item["sourceAssertionIds"], source_by_id)
    for item in doc["traces"]:
        refs_exist("event", item["id"], item["eventIds"], event_by_id)
        refs_exist("rule invocation", item["id"], item["ruleInvocationIds"], invocation_by_id)

    applicable = datetime.fromisoformat(doc["applicableAt"].replace("Z", "+00:00"))
    observed = datetime.fromisoformat(doc["observedAt"].replace("Z", "+00:00"))
    if observed < applicable:
        issues.append(
            ValidationIssue(str(path), "profile observedAt precedes applicableAt", "time")
        )
    return issues


def _compatibility_semantics(path: Path, doc: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    jurisdiction = doc["jurisdiction"]
    declared_packages = set(doc["picPackages"])
    evidence_ids = set(doc["governance"]["evidenceAssertionIds"])

    try:
        applicable_at = datetime.fromisoformat(
            jurisdiction["applicableAt"].replace("Z", "+00:00")
        )
        observed_at = datetime.fromisoformat(jurisdiction["observedAt"].replace("Z", "+00:00"))
    except ValueError:
        issues.append(ValidationIssue(str(path), "invalid compatibility timestamp", "time"))
        applicable_at = observed_at = None
    if applicable_at is not None and observed_at is not None:
        try:
            if observed_at < applicable_at:
                issues.append(
                    ValidationIssue(str(path), "observation time precedes applicable time", "time")
                )
        except TypeError:
            issues.append(
                ValidationIssue(
                    str(path),
                    "cannot compare offset-naive and offset-aware timestamps",
                    "time",
                )
            )

    matching_profiles = [
        profile
        for profile in doc["foioRelease"]["profiles"]
        if profile["id"] == jurisdiction["profileId"]
    ]
    if not matching_profiles:
        issues.append(
            ValidationIssue(
                str(path),
                "FOI-O profile ID not found in release profiles",
                "jurisdiction",
            )
        )
    else:
        profile = matching_profiles[0]
        if profile["jurisdiction"] != jurisdiction["id"]:
            issues.append(
                ValidationIssue(
                    str(path),
                    "FOI-O profile jurisdiction does not match envelope",
                    "jurisdiction",
                )
            )
        if profile["version"] != jurisdiction["profileVersion"]:
            issues.append(
                ValidationIssue(
                    str(path), "FOI-O profile version does not match envelope", "version"
                )
            )

    for index, artifact in enumerate(doc["picArtifacts"]):
        location = f"{path}:picArtifacts/{index}"
        if not _is_immutable_uri(artifact["artifactUri"]):
            issues.append(
                ValidationIssue(location, "artifact URI is not content-addressed", "provenance")
            )
        if artifact["contract"] not in declared_packages:
            issues.append(
                ValidationIssue(
                    location,
                    "artifact contract is not declared in picPackages",
                    "reference",
                )
            )
        if artifact["jurisdiction"] != jurisdiction["id"]:
            issues.append(
                ValidationIssue(
                    location,
                    "artifact jurisdiction does not match release envelope",
                    "jurisdiction",
                )
            )
        if not _timestamps_equal(artifact["applicableAt"], jurisdiction["applicableAt"]):
            issues.append(
                ValidationIssue(
                    location,
                    "artifact applicable time does not match release envelope",
                    "time",
                )
            )
        if not _timestamps_equal(artifact["observedAt"], jurisdiction["observedAt"]):
            issues.append(
                ValidationIssue(
                    location,
                    "artifact observation time does not match release envelope",
                    "time",
                )
            )
        unknown_evidence = set(artifact["evidenceReferenceIds"]) - evidence_ids
        if unknown_evidence:
            issues.append(
                ValidationIssue(
                    location,
                    "artifact references undeclared evidence assertions",
                    "reference",
                )
            )
    for index, promotion in enumerate(doc["promotionRecords"]):
        location = f"{path}:promotionRecords/{index}"
        expected_promotion = {
            "fixture": "gold_fixture",
            "crosswalk_row": "human_approved_crosswalk",
        }[promotion["candidateKind"]]
        if promotion["requestedPromotion"] != expected_promotion:
            issues.append(
                ValidationIssue(
                    location,
                    "candidate kind and requested promotion do not match",
                    "promotion",
                )
            )
        review_uri = promotion["reviewEvidenceUri"]
        if promotion["status"] == "approved" and not _is_immutable_uri(review_uri):
            issues.append(
                ValidationIssue(
                    location,
                    "review evidence URI is not content-addressed",
                    "provenance",
                )
            )
    if doc["governance"]["promotionState"] == "gold" and any(
        record["status"] != "approved" for record in doc["promotionRecords"]
    ):
        issues.append(
            ValidationIssue(
                str(path),
                "gold promotion requires every candidate promotion record to be approved",
                "promotion",
            )
        )
    return issues


def _is_immutable_uri(uri: str | None) -> bool:
    if uri is None:
        return False
    if re.fullmatch(r"urn:sha256:[a-f0-9]{64}", uri):
        return True
    return bool(
        re.fullmatch(
            r"https://raw\.githubusercontent\.com/[^/]+/[^/]+/[a-f0-9]{40}/.+",
            uri,
        )
    )


def _timestamps_equal(left: str, right: str) -> bool:
    try:
        left_time = datetime.fromisoformat(left.replace("Z", "+00:00"))
        right_time = datetime.fromisoformat(right.replace("Z", "+00:00"))
    except ValueError:
        return left == right
    return left_time == right_time


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
