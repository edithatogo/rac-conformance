import copy
import datetime as dt

from tools.independent_evidence import classify


def packet():
    return {
        "implementationId": "external-example",
        "organisation": {"name": "Example Org", "controlRelationship": "external"},
        "repository": {"url": "https://example.org/repo", "accessControl": "external"},
        "sourceRevision": "a" * 40,
        "sourceDigest": "sha256:" + "a" * 64,
        "contractVersions": ["pic-semantics/0.1.0"],
        "kitDigestSha256": "a" * 64,
        "environment": {"runtime": "Python 3.14", "platform": "test", "cleanCheckout": True},
        "command": "python evaluate.py",
        "inputDigest": "sha256:" + "b" * 64,
        "resultDigest": "sha256:" + "c" * 64,
        "testOutcome": "pass",
        "independenceStatus": "qualifying",
        "acknowledgement": {"status": "confirmed", "url": "https://example.org/result"},
        "attestation": {
            "issuerControl": "external",
            "evidenceType": "owner-confirmation",
            "url": "https://example.org/attestation",
        },
        "maintenance": {"owner": "Example Org", "freshnessDate": "2026-07-01"},
        "evidenceUrls": ["https://example.org/result"],
    }


def test_qualifying_packet_is_accepted():
    assert classify(packet(), today=dt.date(2026, 7, 15)) == {"status": "qualifying", "exceptions": [], "qualifiesForV1": True}


def test_internal_rehearsal_is_partial():
    candidate = copy.deepcopy(packet())
    candidate["independenceStatus"] = "internal-rehearsal"
    candidate["organisation"]["controlRelationship"] = "internal"
    candidate["repository"]["accessControl"] = "internal"
    candidate["acknowledgement"]["status"] = "none"
    result = classify(candidate, today=dt.date(2026, 7, 15))
    assert result["status"] == "partial"
    assert result["qualifiesForV1"] is False


def test_self_certified_packet_is_partial():
    candidate = packet()
    candidate["attestation"]["issuerControl"] = "internal"
    result = classify(candidate, today=dt.date(2026, 7, 15))
    assert result["status"] == "partial"
    assert "external owner attestation is missing" in result["exceptions"]


def test_all_non_qualifying_outcomes_are_preserved():
    for outcome in ("conflicting", "withdrawn", "declined", "unresponsive"):
        candidate = packet()
        candidate["independenceStatus"] = outcome
        assert classify(candidate, today=dt.date(2026, 7, 15))["status"] == outcome


def test_stale_or_unverifiable_packet_is_partial():
    candidate = packet()
    candidate["maintenance"]["freshnessDate"] = "2025-01-01"
    candidate["environment"]["cleanCheckout"] = False
    result = classify(candidate, today=dt.date(2026, 7, 15))
    assert result["status"] == "partial"
    assert "maintenance evidence is stale or future-dated" in result["exceptions"]
    assert "execution was not from a clean checkout" in result["exceptions"]


def test_missing_required_data_is_rejected():
    result = classify({})
    assert result["status"] == "rejected"
    assert result["qualifiesForV1"] is False
    assert any(item.startswith("schema:") for item in result["exceptions"])
