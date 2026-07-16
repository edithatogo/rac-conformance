# Provenance and Reproducibility Evidence

The current evidence set is anchored to reviewed commit
`7420d7b83a5df19be46db14a9f8eadd827cf9ac9`. Dependency resolution is pinned by
`contracts/tools/uv.lock`, whose SHA-256 is
`3fc7fa479b9e3cc53640dd4b6c408afa22a2c0c27d32c3c2451ea0b889248fa3`.

The reproducibility procedure is:

1. clone the exact commit in two clean environments;
2. install from the lock file with the pinned `uv` version in CI;
3. run `make check`;
4. hash each generated artifact and compare the manifests.

The repository currently proves deterministic test and manifest generation.
Byte-for-byte package reproducibility and hosted provenance attestations remain release-blocking until the clean-environment runs are attached.
