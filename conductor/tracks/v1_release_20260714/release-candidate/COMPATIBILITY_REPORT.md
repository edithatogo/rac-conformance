# v1.0.0-rc.1 Compatibility Report

Source commit: `0c4a83b55208bae59592af017c6e0f66194ec8bb`

The clean-checkout `make check` gate passed, including repository audit,
contract tests, converter tests, harness tests, study tests, demo tests, and
the example corpus. The full output is retained in the build workspace used
for this candidate; the reproducible command is recorded in `PROVENANCE.json`.

Package compatibility is versioned independently from the programme release:
`pic-contracts` remains `0.1.0`; PIC contract versions are listed in
`V1_NORMATIVE_FREEZE.md`. The two clean package builds produced identical
SHA-256 digests for both the wheel and source distribution.

This is a release candidate only. The gate audit remains blocked by external
FOI-O evidence, independent adoption, paper refresh, and Zenodo deposit. No
public package, tag, DOI, or final v1.0 release is claimed.
