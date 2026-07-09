# Contributing

This repository is an evidence-first research and engineering program. Detailed agent and human workflow rules live in:

- [`AGENTS.md`](AGENTS.md) — implementation guide for AI agents and humans
- [`conductor/workflow.md`](conductor/workflow.md) — task lifecycle, commits, `[HUMAN]` gates
- [`conductor/product-guidelines.md`](conductor/product-guidelines.md) — product constraints

## Quick rules

1. Prefer small, reviewable changes with tests (`make check` when available).
2. Do not invent statute text, golden fixtures, or network-dependent facts.
3. Do not submit upstream issues/PRs or send external email unless a plan task marks that work `[HUMAN]` and Dylan authorizes it.
4. Money values are decimal strings, never floats.
5. No runtime AI decisions in product code.

## License

Contributions are accepted under the [Apache License 2.0](LICENSE).
