# AGENTS.md — implementation guide for AI agents

You are an AI agent (ChatGPT, Codex, Claude, or similar) asked to implement work in this repository. Read this file completely before doing anything.

## 1. Orientation (read in this order, ~10 minutes)

1. `README.md` — what this repo is and the six tracks.
2. `views/07_fable5_reassessment_and_pivot.md` — the current strategy and why.
3. `conductor/index.md` → `conductor/workflow.md` — how work is done here (task lifecycle, commits, TDD, `[HUMAN]` gates).
4. The `spec.md` and `plan.md` of the track you are implementing.

Do **not** take design direction from `project_repo_racx/` (superseded design notebook — see its `STATUS.md`) or from `views/00–05` (historical ChatGPT views). Where they conflict with `views/06`, `views/07`, or the conductor files, the latter win.

## 2. What to work on

- Follow `conductor/tracks.md` order. **Track 1 (`contracts_20260704`) is the critical path — if it is not complete, work on it first.**
- Within a track: first unchecked task, in order. One commit per task, message format per `conductor/workflow.md`.
- Tasks marked `[HUMAN]` are for Dylan: prepare the artifact (draft, candidates, submission text), then stop. Never send emails, open external issues/PRs, or promote fixture candidates yourself.
- Blocked? Add `> BLOCKED (date): reason` under the task in `plan.md`, commit, move to the next unblocked task. Never improvise around a blocker (especially: never fake network-dependent facts, never invent statute text, never re-implement PRD in Python).

## 3. Hard rules (violations invalidate the work)

1. **No runtime AI decisions** in any code produced here. AI drafts; deterministic code validates/executes; humans certify.
2. **Oracle independence**: never generate golden fixtures for code you (or another model) wrote and promote them yourself. Candidates go to `*/candidates/` with `method: ai-proposed`; humans promote.
3. **Verify before encoding**: statute sections, engine formats, and API shapes must be read from primary sources (legislation.govt.nz, actual repo code at cited permalinks). If you cannot verify (no network), tag output `UNVERIFIED` and record it.
4. **No mapping without a consumer**; no new external-standard crosswalks, no JSON-LD contexts, no expression languages. These are settled scope decisions (`views/06` §5, §8, §10).
5. **Floats never represent money.** Decimal strings everywhere.
6. Cross-repo work is staged under `external/<repo>/` with a `SUBMISSION.md`; it is not pushed anywhere by agents.

## 4. Capability-based division of labour

### If you are ChatGPT (web interface, container with limited/no network)

Well-suited — do these:
- All documentation tasks: contract `SPEC.md` files, `FORMATS.md`/`DESIGN.md` skeletons, submission drafts, paper sections, report templates.
- JSON Schema authoring + valid/invalid example corpora.
- Pure-Python tooling with stdlib + `jsonschema` + `pyyaml`: `pic-validate`, `pic-diff`, converters against *vendored* sample files, the OIA rules module (pure functions), unit tests.
- Git commits inside the provided archive (the `.git` directory is included; commit as you go and return the whole directory as a zip).

Not suited — leave for Codex/Cursor (mark `> DEFERRED-TO-CLI (date)` in the plan):
- Anything requiring cloning upstream repos or installing `policyengine-us`/OpenFisca (Track 3 phase 1/3, Track 4, Track 5 phases 1/3).
- Anything requiring R (Track 5 PRD runner).
- Live verification of statute text or repo permalinks if your network is restricted (produce `UNVERIFIED`-tagged drafts instead).

### If you are Codex / a CLI agent with full toolchain

- Everything above, plus the engine-dependent tracks. Prefer real installs and measured results over described ones. Pin versions and record them in the artifacts.
- Before starting, run `git log --oneline | head -20` and read recent checkpoint notes in the active track's `plan.md` to avoid redoing work.

## 5. Quality gates before every commit

- `make check` if it exists; else `pytest` + `ruff check` + validating any touched examples with `pic-validate` (once built).
- Schemas: every schema change re-runs its valid/invalid corpus.
- Plans: checkbox updated, `metadata.json` `updated_at` bumped.
- No `__pycache__`, caches, venvs, or `data/processed` in commits (`.gitignore` covers these; keep it that way).

## 6. Context budget guidance

This repo is designed so you rarely need more than: this file + `conductor/workflow.md` + the active track's `spec.md`/`plan.md` + the files you are editing. Avoid loading `source_material/` and `conversation/` (historical archive) unless a task explicitly cites them.

## 7. Handoff protocol (multi-agent relay)

This repo travels as a zip (with `.git`) between agents. On receipt:
1. Unzip, `git log --oneline | head` — confirm history is intact. If `.git` is missing, STOP and report; do not re-init.
2. Read the latest `> CHECKPOINT` notes in each in-progress track plan.
3. Work per §2. Commit per task.
4. On finishing your session: write/refresh a checkpoint note in the active plan, commit, and produce the return archive:
   `zip -rq handoff_$(date +%Y%m%d).zip . -x "*.pyc" "*__pycache__*" ".pytest_cache/*" "*.zip"`
   (from the repo root; the `.git` directory MUST be included).
