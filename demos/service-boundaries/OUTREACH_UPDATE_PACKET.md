# Service-Boundary Demo Update Packet

Audience: DBN / Docassemble / CiviForm stakeholders

## Summary

This track now has two local, deterministic service-boundary demonstrations:

- A Docassemble-style CLI demo that asks for an OIA receipt date and returns a deadline plus trace output.
- A CiviForm-style CLI demo that accepts a JSON application payload and returns a PIC-shaped result plus trace summary.

Both demos call the staged `foi-o` OIA rules module, use committed synthetic examples, and avoid live services or real applicant data.

## What Was Proven

- The demo request and response examples are committed.
- The demo tests cover request validation, rule invocation, trace output, and invalid-request rejection.
- `make check` now includes the demo lint and test targets.
- A local privacy/security review has passed.

## What Is Still Not True

- This is not a production Docassemble deployment.
- This is not a production CiviForm plugin or JVM integration.
- No live service, auth, or external data flow has been exercised.

## Draft Update Text

Subject: Service-boundary demo update for Docassemble/CiviForm

We now have a repo-local proof of two service-boundary integrations:

1. A Docassemble-style CLI demo that invokes the staged OIA rules module.
2. A CiviForm-style CLI demo that accepts a JSON payload and returns a PIC-shaped rule result with trace summary.

The demo package is fully synthetic, locally testable, and included in `make check`.

## Human Gate

[HUMAN] Send or adapt this update only after confirming the target audience and whether the repository should continue toward a production integration path.
