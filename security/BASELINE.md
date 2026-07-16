# Engineering Baseline

Reference environment captured for the local qualification run on 2026-07-16:
macOS, Python 3.14, `uv`, and the repository's pinned development dependencies.
Hosted qualification must additionally run Python 3.12 on Ubuntu and record
the GitHub Actions run URLs.

The initial budgets are deliberately explicit and conservative:

| Input class | Maximum bytes | Maximum nesting | Maximum string | Diagnostic requirement |
| --- | ---: | ---: | ---: | --- |
| ordinary PIC artifact | 4 MiB | 64 | 512 KiB | structured path and code |
| generated report | 16 MiB | 64 | 512 KiB | no unescaped user content |
| fixture archive | 64 MiB | n/a | n/a | isolated temporary directory |

The JSON parser boundary enforces the first row through
`pic_contracts.safety.load_bounded_json`. A budget may only be changed with a
new benchmark, regression test, and release-note justification. Wall-clock and
memory measurements belong in hosted qualification evidence because local
developer hardware is not a stable performance oracle.

Required qualification commands:

```text
make check
cd contracts/tools && uv run pytest tests/test_safety.py
PYTHONPATH=. uv run python tools/validate_hardening_evidence.py
```
