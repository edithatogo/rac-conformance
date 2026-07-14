import pytest

from tools.validate_programme_citations import validate_commit_pin


def test_integration_release_requires_full_commit_pin() -> None:
    validate_commit_pin(
        {
            "id": "integration",
            "kind": "software_and_integration",
            "commit": "a" * 40,
        },
    )

    for commit in (None, "a" * 39, "g" * 40):
        with pytest.raises(AssertionError):
            validate_commit_pin(
                {
                    "id": "integration",
                    "kind": "software_and_integration",
                    "commit": commit,
                },
            )


def test_other_artifact_kinds_do_not_require_commit_pin() -> None:
    validate_commit_pin({"id": "software", "kind": "software"})
