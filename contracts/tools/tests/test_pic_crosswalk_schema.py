from pathlib import Path

from pic_contracts.schema_utils import CONTRACTS_ROOT, load_json, validator_for

BASE = CONTRACTS_ROOT / "pic-crosswalk" / "0.1.0" / "examples"


def test_valid_crosswalks_validate() -> None:
    validator = validator_for("pic-crosswalk")
    for path in sorted((BASE / "valid").glob("*.json")):
        validator.validate(load_json(path))


def test_invalid_crosswalks_fail_for_intended_reason() -> None:
    validator = validator_for("pic-crosswalk")
    expected: dict[str, tuple[Path, str]] = {
        "bad-id.json": (Path("rows/0/id"), "does not match"),
        "bad-kind.json": (Path("rows/0/kind"), "is not one of"),
        "bad-method.json": (Path("rows/0/mappings/0/method"), "is not one of"),
        "mapping-without-system.json": (Path("rows/0/mappings/0"), "is a required property"),
    }
    for filename, (error_path, message) in expected.items():
        errors = list(validator.iter_errors(load_json(BASE / "invalid" / filename)))
        assert errors, filename
        assert any(Path(*map(str, error.path)) == error_path for error in errors)
        assert any(message in error.message for error in errors)

