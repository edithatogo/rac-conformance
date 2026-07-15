from tools.validate_foio_evidence_bundle import validate


def bundle():
    return {
        "release": {"tag": "v2.0.0", "commit": "a" * 40},
        "capabilities": [{"id": "pic-v2"}],
        "contracts": [{"id": "pic-traces/0.2.0"}],
        "migrations": [],
        "tests": [{"command": "make check", "status": "pass"}],
        "fixtures": [{"path": "fixtures/manifest.json"}],
        "provenance": {"status": "verified"},
        "empiricalResults": [{"id": "reproduction-1"}],
        "exceptions": [],
        "limitations": ["No legal authority claim"],
    }


def test_complete_verified_bundle_is_accepted():
    assert validate(bundle()) == []


def test_incomplete_or_unverified_bundle_is_rejected():
    candidate = bundle()
    del candidate["empiricalResults"]
    candidate["provenance"]["status"] = "dirty"
    errors = validate(candidate)
    assert "empiricalResults: required" in errors
    assert "provenance.status: must be verified" in errors


def test_release_identity_is_verified_before_intake():
    candidate = bundle()
    candidate["release"]["commit"] = "not-a-sha"
    assert "release.commit: required 40-character commit SHA" in validate(candidate)
