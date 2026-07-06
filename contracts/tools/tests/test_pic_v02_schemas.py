from pic_contracts.schema_utils import CONTRACTS_ROOT, load_json, validator_for


def test_traces_v02_validation() -> None:
    validator = validator_for("pic-traces", "0.2.0")

    # Valid
    valid_path = (
        CONTRACTS_ROOT
        / "pic-traces"
        / "0.2.0"
        / "examples"
        / "valid"
        / "trace-v02-missingness.json"
    )
    validator.validate(load_json(valid_path))

    # Invalid
    invalid_path = (
        CONTRACTS_ROOT
        / "pic-traces"
        / "0.2.0"
        / "examples"
        / "invalid"
        / "trace-v02-bad-valuestate.json"
    )
    errors = list(validator.iter_errors(load_json(invalid_path)))
    assert errors
    assert any(
        "valueOrigin" in error.path or "is not one of" in error.message
        for error in errors
    )


def test_parameters_v02_validation() -> None:
    validator = validator_for("pic-parameters", "0.2.0")

    # Valid
    valid_path = (
        CONTRACTS_ROOT
        / "pic-parameters"
        / "0.2.0"
        / "examples"
        / "valid"
        / "parameters-v02-exclusions.json"
    )
    validator.validate(load_json(valid_path))

    # Invalid
    invalid_path = (
        CONTRACTS_ROOT
        / "pic-parameters"
        / "0.2.0"
        / "examples"
        / "invalid"
        / "parameters-v02-bad-exclusions.json"
    )
    errors = list(validator.iter_errors(load_json(invalid_path)))
    assert errors
    assert any(
        "holidayExclusions" in error.path or "is not of type 'array'" in error.message
        for error in errors
    )
