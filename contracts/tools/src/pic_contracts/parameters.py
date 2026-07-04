"""Validation helpers for PIC parameter files."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class ValidationError:
    path: str
    message: str


def _parse_date(value: str | None) -> date | None:
    if value is None:
        return None
    return date.fromisoformat(value)


def validate_parameter_periods(doc: dict[str, Any]) -> list[ValidationError]:
    """Return ordering and overlap errors for PIC parameter periods."""

    errors: list[ValidationError] = []
    for param_index, parameter in enumerate(doc.get("parameters", [])):
        previous_to: date | None = None
        saw_open_ended = False
        for value_index, period in enumerate(parameter.get("values", [])):
            path = f"parameters/{param_index}/values/{value_index}"
            try:
                current_from = _parse_date(period.get("from"))
                current_to = _parse_date(period.get("to"))
            except (TypeError, ValueError) as exc:
                errors.append(ValidationError(path, f"invalid period date: {exc}"))
                continue
            if current_from is None:
                errors.append(ValidationError(f"{path}/from", "period must have a from date"))
                continue
            if saw_open_ended:
                errors.append(ValidationError(path, "period follows an open-ended period"))
            if current_to is not None and current_to <= current_from:
                errors.append(ValidationError(path, "period to must be after from"))
            if previous_to is not None and current_from < previous_to:
                errors.append(ValidationError(path, "period overlaps previous period"))
            if previous_to is not None and current_from == previous_to:
                pass
            if current_to is None:
                saw_open_ended = True
            previous_to = current_to
    return errors

