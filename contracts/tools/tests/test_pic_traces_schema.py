from pathlib import Path

from pic_contracts.schema_utils import CONTRACTS_ROOT, load_json, validator_for

BASE = CONTRACTS_ROOT / "pic-traces" / "0.1.0" / "examples"


def test_valid_traces_validate() -> None:
    validator = validator_for("pic-traces")
    for path in sorted((BASE / "valid").glob("*.json")):
        validator.validate(load_json(path))


def test_invalid_traces_fail_for_intended_reason() -> None:
    validator = validator_for("pic-traces")
    expected: dict[str, tuple[Path, str]] = {
        "bad-kind.json": (Path("steps/0/kind"), "is not one of"),
        "missing-conforms-to.json": (Path(), "is a required property"),
        "bad-parameter-version.json": (
            Path("steps/0/parameterVersions/0"),
            "is a required property",
        ),
    }
    for filename, (error_path, message) in expected.items():
        errors = list(validator.iter_errors(load_json(BASE / "invalid" / filename)))
        assert errors
        assert any(Path(*map(str, error.path)) == error_path for error in errors)
        assert any(message in error.message for error in errors)


