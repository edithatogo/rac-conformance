# Schema References

This directory may hold local non-normative manifests or adapter schemas with
named consumers. Normative PIC schemas must be consumed from a released or
commit-pinned `rac-conformance` version and must not be copied here as a fork.

`contract-consumption.json` is the machine-readable ledger for the incubator's
current dependency boundary. It records the released PIC revision, each schema
path and digest, and the observed FOI-O/foi-process input schemas. Run
`make process-mappings-check` from the parent repository to verify the PIC
schemas at the recorded Git revision and the matrix's immutable provenance.
