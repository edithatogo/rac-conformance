# Service Boundary Demos

This directory contains local-only demonstrations of a PIC-tested rules module crossing two boundaries:

1. A Docassemble-style interview mock.
2. A CiviForm-style service mock.

## Docassemble-Style Demo

Run the demo against the committed request example:

```sh
PYTHONPATH=demos/service-boundaries/src:external/foi-o/src \
  uv run python -m service_boundary_demos.docassemble_runner \
  --input demos/service-boundaries/examples/docassemble/request.json
```

The command prints a JSON response with the calculated OIA response deadline and a minimal trace payload.

## What Is Real

- The OIA rules module is the staged `foi-o` rule implementation in `external/foi-o/src`.
- The demo runner is local and deterministic.
- The request/response JSON files are committed examples.

## What Is Mocked

- Docassemble itself is not deployed.
- No external interview engine is running.
- CiviForm is represented later by a local service mock, not a real plugin.

## Limitations

- No real applicant or requester data is used.
- No secrets, credentials, or live services are required.
- The service boundary only proves the integration shape and trace output.

## Next Upstream Path

- Docassemble: a small Python package or interview wrapper that imports the same OIA rules module.
- CiviForm: a service-boundary mock or plugin proof, depending on whether a Java integration is later justified.
