# RaC Conformance v1.0 Release

Status: Draft | Consumed-by: v1 users and maintainers

## Overview

Release 1.0 only after every required technical, compatibility, security,
independent-adoption, governance, external, and human gate has durable evidence.
If the gates are incomplete, continue supported 0.x releases rather than
relabeling incomplete evidence as 1.0.

Depends on: all preceding v1 roadmap tracks.

## Functional Requirements

1. Freeze normative contracts and generate complete migration and compatibility
   documentation.
2. Build and verify release candidates from clean environments.
3. Publish exact supported-version, known-limit, security, provenance, consumer,
   and conformance matrices.
4. Verify release notes and capability claims against executable evidence.
5. Require human authorization for release candidate promotion, signing, package
   publication, DOI actions, announcements, and final release.
6. Monitor hosted checks and published artifacts, then exercise rollback if any
   integrity or compatibility check fails.
7. Archive completed tracks only after post-release verification and record
   deferred 1.x work separately.

## Non-Functional Requirements

- No manual editing of generated release manifests after validation.
- No weakening branch protection or required checks to publish.
- No publication claim before the external destination confirms the artifact.
- Release artifacts must be immutable, checksummed, provenance-linked, and
  reproducible within documented limits.

## Acceptance Criteria

- Every required machine-readable gate is pass with current evidence.
- All required local and GitHub Actions checks pass on the release commit/tag.
- Published package/tag/archive metadata and checksums agree.
- Known consumers pass the frozen compatibility suite.
- Human release authorization and post-release verification are recorded.

## Out of Scope

- Waiving external or human gates because a deadline is reached.
- New features after release-candidate freeze.
- Publishing papers or DOI records without separate authorization.
