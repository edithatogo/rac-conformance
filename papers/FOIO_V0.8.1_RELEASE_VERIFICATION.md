# FOI-O v0.8.1 release verification

Prepared: 2026-07-15

This is repository-local verification of the immutable software release. It is
not the FOI-O release-evidence bundle and does not certify empirical results,
V2 conformance, independent review, or publication.

## Release identity

- Repository: <https://github.com/edithatogo/foi-o>
- Tag: `v0.8.1`
- Commit: [`d24ae6f9f2d9488052969f633d91eff4a9a47f58`](https://github.com/edithatogo/foi-o/commit/d24ae6f9f2d9488052969f633d91eff4a9a47f58)
- Package version: `0.8.1` in `pyproject.toml`
- Citation version: `0.8.1` in `CITATION.cff`
- Zenodo version DOI: [`10.5281/zenodo.21360138`](https://doi.org/10.5281/zenodo.21360138)
- Zenodo concept DOI: [`10.5281/zenodo.21360137`](https://doi.org/10.5281/zenodo.21360137)

## Content surfaces

The following files were read from the tagged checkout and hashed:

| Surface | Path | SHA-256 |
| --- | --- | --- |
| Empirical overlay contract | `contracts/v2-empirical-overlay.yaml` | `fdfa47df335806063fa41a51cfe52584d087061919cc52bb80fda16a9dc549fb` |
| Ontology release schema | `schemas/json/ontology-release-manifest.schema.json` | `7b7380875c1ce17ad63cd71fff02e9a4d402aa6e753eff5bb467ac106bcde33e` |
| Evidence assertion schema | `schemas/json/evidence-assertion.schema.json` | `9e3b1a3f6a33a0b8bbf46487eef03639553074cef5f04f3a8b36a41154a0b6b6` |
| V2 migration | `migrations/v1-to-v2-empirical-overlay.md` | `e7351ffde967d55ef56a9255c4d7bbc0d7ed02c832b21b8668f2d30a12904323` |

The tagged tree also contains the empirical schemas and valid/invalid fixture
corpora under `schemas/json/` and `examples/v2/`. Capability and reproducibility
surfaces are exposed through the CLI and documented in `docs/19-release-readiness-evidence.md`
and `docs/23-release-package.md`.

## Reproducibility result

In a clean detached checkout, with the optional RDF dependency installed:

```bash
uv sync --extra dev --extra rdf
uv run pytest -q
```

The unmodified `v0.8.1` tag produced `278 passed, 2 skipped, 2 failed`. The
two failures were inventory-fixture mismatches recorded in
`external/foi-o/RELEASE_EVIDENCE_HANDOFF.md`; a detached remediation candidate
reconciled them and produced `280 passed, 2 skipped`, but that candidate has
not been pushed to FOI-O or substituted for the immutable tag.

## Boundary and next gate

This verification closes only the immutable-release inspection task in the
paper track. Import of the accepted release-evidence bundle remains open under
[foi-o#27](https://github.com/edithatogo/foi-o/issues/27). Paper claims must
not be refreshed from this record alone.
