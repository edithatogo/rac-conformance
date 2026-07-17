# Workflow

This workflow governs all tracks in `conductor/tracks/`. It is written to be executable by different agents (ChatGPT, Codex, Claude) and analysts at different capability levels. See `conductor/TERMINOLOGY.md` for governance vocabulary and compatibility markers.

## Task lifecycle

1. Pick the first unchecked task in the active track's `plan.md` (tracks are ordered; within a track, phases are ordered).
2. If the task has a "Write tests" sub-task, write the failing test first (TDD), then implement until green.
3. Run the verification listed in the task's **Acceptance** block. Do not self-certify with weaker checks.
4. Mark the checkbox `[x]` in `plan.md`, update the track's `metadata.json` `updated_at` (and `status` when the track starts/finishes).
5. Commit (see below). One commit per task. Never batch unrelated tasks.
6. If blocked, do NOT improvise around the blocker: add a `> BLOCKED (date): reason` line under the task in `plan.md`, commit that, and move to the next unblocked task or track.

## Commit conventions

- Message format: `<track_shortname>: <imperative summary>` — e.g. `contracts: add pic-fixtures schema and negative tests`.
- Body: 2–5 lines describing what changed and which plan task it completes (`Completes: contracts_20260704 phase 2 task 3`).
- Commit after every task. Do not amend or rebase published history. Task summaries live in commit messages (not git notes — ChatGPT/Codex containers handle plain commits more reliably).

## Testing policy

- Target: >=80% line coverage for code under `contracts/tools/` and any runner/converter code in this repo. Schema-only changes require example-validation tests instead.
- Every schema MUST have: at least 2 valid examples, at least 3 invalid examples (negative tests), all exercised in CI.
- Every converter MUST have round-trip tests (`A -> B -> A` canonical equality) on its supported subset, and explicit rejection tests for unsupported constructs.
- Golden fixtures: analyst-curated only (see product-guidelines). Agents may draft candidates into `*/candidates/` directories; promotion into `fixtures/` requires analyst review and is never done by an agent.

## Phase completion verification and checkpointing protocol

At the end of every phase, execute the phase's final meta-task:

1. Run the full test suite and schema/example validation (`make check` once Track 1 creates it; until then, `pytest` + the validator commands in the plan).
2. Re-read the phase's Acceptance criteria in `spec.md`; write a 3–8 line checkpoint note in `plan.md` under the phase heading (`> CHECKPOINT (date): …`), stating what is proven and what is deferred.
3. Commit with `<track_shortname>: phase <n> checkpoint`.
4. **Analyst verification gate:** tasks marked `[HUMAN]` (the legacy machine marker for fixture promotion, upstream issue/PR submission, and emails) are for Dylan or another explicitly authorized analyst. Agents prepare the artifact (draft PR body, draft email, candidate fixtures) and stop.

## Cross-repo work protocol (Tracks 2–6)

Work destined for external repos is **staged in this repo first** under `external/<repo>/…` as patch-ready trees plus a `SUBMISSION.md` (what, why, exact upstream path, draft PR/issue text). Submitting upstream is always a `[HUMAN]` task. This keeps the whole program reviewable and portable inside one archive.

## Repo relevance boundary check policy

Before executing any cross-repo work or copying code/documentation to/from any repository under the `edithatogo` organization, the agent must check `conductor/edithatogo-repo-boundaries.md` to ensure the repository is currently relevant and the type of work matches the allowed boundaries. If the repository is not listed, or entry conditions are not met, the task must be treated as blocked.


## AI usage rules (binding on all agents)

- Allowed: scaffolding, schema drafting, converter code, test *proposals*, documentation, red-teaming, divergence-report explanation.
- Forbidden: generating golden fixtures without analyst approval; changing normative spec text without an explicit plan task; adding crosswalk targets without a consumer; any runtime decision logic that calls an LLM.
- Every AI-drafted mapping (variable/parameter crosswalk row) gets `"method": "ai-proposed"` until an analyst flips it to `"human-approved"`.
