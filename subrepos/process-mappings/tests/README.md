# Tests

Tests must validate released PIC compatibility, source-manifest completeness,
jurisdiction/effective-date isolation, candidate promotion rules, adapter loss
reporting, and deterministic normalized traces. The parent gate currently runs
the contract-consumption manifest check with `make process-mappings-check`.
Profile and adapter tests remain deferred until a named profile is implemented.
