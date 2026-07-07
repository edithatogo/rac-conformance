# Service Boundary Demo Design

## Purpose

This directory holds two minimal, local-only demonstrations of a PIC-tested rules module crossing a stable service boundary:

1. A Docassemble-style interview mock that asks for an OIA receipt date and calls the staged `foi-o` OIA rules module.
2. A CiviForm-style HTTP service mock that accepts a JSON application payload and returns a PIC-shaped rule result with trace metadata.

## Layout

- `demos/service-boundaries/examples/docassemble/request.json`
- `demos/service-boundaries/examples/docassemble/response.json`
- `demos/service-boundaries/examples/civiform/request.json`
- `demos/service-boundaries/examples/civiform/response.json`
- `demos/service-boundaries/src/service_boundary_demos/`
- `demos/service-boundaries/tests/`

## Demo 1: Docassemble-Style OIA Interview Mock

Inputs:

- receipt date
- optional holiday dates

Behavior:

- convert the receipt date to the staged `foi_o_nz.oia_rules.ValueObject`
- call `foi_o_nz.oia_rules.evaluate_invocation`
- return the calculated response deadline plus trace/discretion fields

Limitations:

- this is not a Docassemble deployment
- no real user session, file upload, or document assembly is included
- no live external services are contacted

## Demo 2: CiviForm-Style Service Mock

Inputs:

- a small JSON payload with request metadata and the same receipt date boundary

Behavior:

- validate the payload locally
- invoke the same OIA rules module through a service-boundary helper
- return a PIC-shaped JSON result with outputs, trace summary, and a minimal explanation

Limitations:

- this is not a real CiviForm plugin
- this does not depend on Java, Play Framework, or a live HTTP server
- the demo only proves the service boundary and response shape

## Privacy and Boundary Notes

- no real applicant data is stored
- no secrets or credentials are required
- traces only expose the minimum fields needed to show the rule decision path
- the demo stays local and deterministic

## Example JSON

The examples in `examples/` are committed as the canonical request/response pairs for the tests.
