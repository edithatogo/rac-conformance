from pic_contracts.schema_utils import CONTRACTS_ROOT, load_json, validator_for

BASE = CONTRACTS_ROOT / "pic-foio-compatibility" / "0.1.0" / "examples"


def test_valid_foio_compatibility_manifests_validate() -> None:
    validator = validator_for("pic-foio-compatibility")
    paths = sorted((BASE / "valid").glob("*.json"))
    assert len(paths) >= 2
    for path in paths:
        validator.validate(load_json(path))


def test_invalid_foio_compatibility_manifests_fail() -> None:
    validator = validator_for("pic-foio-compatibility")
    for path in sorted((BASE / "invalid").glob("*.json")):
        assert list(validator.iter_errors(load_json(path))), path.name
