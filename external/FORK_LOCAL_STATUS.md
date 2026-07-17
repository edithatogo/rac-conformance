# Fork local status — rulespec-nz & openfisca-aotearoa-br

**Date (UTC):** 2026-07-09T03:05:25Z  
**Local checkouts:** `.external-repos/rulespec-nz`, `.external-repos/openfisca-aotearoa`  
**Policy:** work only on Dylan’s edithatogo forks; no force-push to upstream `main`.

> **Historical snapshot:** The branch, PR, blocker, and source-of-truth
> statements below record the local state on 2026-07-09. On 2026-07-17, the
> maintainer confirmed that the RuleSpec NZ fix had been reproduced on upstream
> `main` through supervised-encoder migration #83, with clean compilation and
> 3/3 companion tests, and closed #79/#80 with credit. The local fork remains a
> reproducibility artifact, not the current canonical source.

---

## Task A — `edithatogo/rulespec-nz` (KiwiSaver solidify)

| Item | Value |
|---|---|
| Remote | https://github.com/edithatogo/rulespec-nz |
| Primary branch | `fix/kiwisaver-elective-rates-map` |
| Optional convenience branch | `local/main` (same tip as fix branch) |
| Fork `main` (tracks upstream tip) | `7eb82349dcb7f1e7ce25fd32a66e6f599bbc8b15` |
| **Tip SHA** (fix + local/main) | **`c11ab65190cb39bbd81eb5e609690c0287f719bb`** |
| Upstream PR | https://github.com/TheAxiomFoundation/rulespec-nz/pull/80 (OPEN) |
| Upstream issue | https://github.com/TheAxiomFoundation/rulespec-nz/issues/79 |
| Engine used for verify | `axiom-rules-engine` binary @ `.external-repos/axiom-rules-engine/target/debug/axiom-rules-engine` |
| Engine git pin | `732ad89f47035987ed0510979514aa405a1ee47c` (0.1.0) |

### Commits on fix branch (beyond fork `main` / upstream tip)

| SHA | Summary |
|---|---|
| `ecdc2e3` | `fix(kiwisaver): use indexed parameter map for elective rates` |
| `e7fb237` | `chore: allow LICENSE-CODE and NOTICE in repository structure` |
| `c11ab65` | `docs: record fork as KiwiSaver compile source of truth` |

### Requirements checklist

| # | Requirement | Status |
|---|---|---|
| 1 | Integer-keyed elective contribution rates fix | **Verified.** `kiwisaver_employee_elective_contribution_rates` is `kind: parameter`, `indexed_by: elective_rate_option`, values `1`…`5` → 0.035…0.10. |
| 2 | `LICENSE-CODE` / `NOTICE` in repository-structure allowlist | **Verified.** Both listed under `allowed_root_files` in `.axiom/repository-structure.yaml`; root files present on branch. |
| 3 | Document upstream PR #80 signing-key blocker; fork is compile SoT | **Done.** `docs/FORK_STATUS.md` on the fix branch (and `local/main`). |

### Compile verification (2026-07-09)

```text
axiom-rules-engine compile \
  --program nz/statutes/kiwisaver/contributions.yaml \
  --output /tmp/ks-final.compiled.json
# compiled_program: ... artifact_format_version: 1
# derived_outputs: 3  engine_version: 0.1.0
# evaluation_order: kiwisaver_employee_deduction,
#   kiwisaver_government_contribution_maximum,
#   kiwisaver_minimum_employer_contribution
```

**Negative control:** tip of fork `main` (`7eb8234`) still fails:

```text
yaml parse error: rules[1].versions[0].values: invalid type: sequence, expected a map
```

### Upstream PR #80 note

CI quality/roadmap-coverage pass; **validate fails** on `axiom-encode guard-generated` (manual RuleSpec change without signed encoding manifest). Requires `AXIOM_ENCODE_APPLY_SIGNING_KEY` / maintainer re-sign. At this snapshot date, the fork's `fix/kiwisaver-elective-rates-map` (or `local/main`) was the local compile source of truth. This guidance was superseded on 2026-07-17 when canonical migration #83 placed the semantic fix on upstream `main`. Upstream `origin/main` was not force-pushed.

### Pushes this session

- `fork/fix/kiwisaver-elective-rates-map` → `c11ab65` (docs commit)
- `fork/local/main` → `c11ab65` (new branch, same tip)

---

## Task B — `edithatogo/openfisca-aotearoa-br` (tax / ACC / KS polish)

| Item | Value |
|---|---|
| Remote | https://github.com/edithatogo/openfisca-aotearoa-br |
| Branch | `feat/199-income-tax-acc-kiwisaver` |
| **Tip SHA** | **`d89a078945607bed6fc75ca8b0a4e6f2686606c0`** |
| Upstream PR (BetterRules) | https://github.com/BetterRules/openfisca-aotearoa/pull/200 |
| Local checkout | `.external-repos/openfisca-aotearoa` @ same SHA |

### Recent commits on branch

| SHA | Summary |
|---|---|
| `16ba764` | feat: 2025+ schedule income tax, ACC earners levy, KiwiSaver rates |
| `ae7a8c1` | ci: re-trigger PR checks for BetterRules#200 |
| `db21d53` | fix(kiwisaver): clamp contribution base at zero |
| `d89a078` | test(kiwisaver): negative earnings produce zero contributions |

### Requirements checklist

| # | Requirement | Status |
|---|---|---|
| 1 | Tax / ACC / KS surfaces present | **Yes.** Variables: `income_tax__schedule_1_tax_before_credits` (and alias), `acc__earners_levy*`, `kiwisaver__*minimum_contribution*`. Parameters under `parameters/taxes/income_tax/`, `parameters/acc/earners_levy/`, `parameters/kiwisaver/`. |
| 2 | KiwiSaver negative earnings clamp (`max 0`) | **Yes.** Both employee and employer formulas use `max_(earnings, 0) * rate` in `openfisca_aotearoa/variables/acts/kiwisaver/contributions.py`. |
| 3 | Negative salary test present | **Yes.** `kiwisaver_negative_salary_does_not_create_contributions` in `tests/kiwisaver/minimum_contributions.yaml` (input −100 → contributions 0). |
| 4 | Python 3.11 pytest on new tests | **21 passed** (see below). |

### Test run (2026-07-09)

Environment: Python **3.11.15**, venv `.venv-nz-recon311`, editable country package.

```text
openfisca test --country-package openfisca_aotearoa \
  openfisca_aotearoa/tests/income_tax/schedule_1_tax_before_credits.yaml \
  openfisca_aotearoa/tests/acc/earners_levy.yaml \
  openfisca_aotearoa/tests/kiwisaver/minimum_contributions.yaml \
  openfisca_aotearoa/tests/individual_income_tax_rate.yaml
# 21 passed in 0.05s
```

### Pushes this session

- **None required.** Remote `fork/feat/199-income-tax-acc-kiwisaver` already at `d89a078` with clamp + negative test. Local branch fast-forwarded to match.

---

## Recommended pins for consumers (e.g. NZ recon harness)

| Consumer need | Pin |
|---|---|
| RuleSpec NZ KiwiSaver compile | Current canonical source: `TheAxiomFoundation/rulespec-nz@main` after migration #83. Historical reproduction pin: `edithatogo/rulespec-nz` @ `c11ab65`. |
| OpenFisca Aotearoa tax/ACC/KS | `edithatogo/openfisca-aotearoa-br` @ `feat/199-income-tax-acc-kiwisaver` @ **`d89a078`** |
| Axiom engine binary | `.external-repos/axiom-rules-engine` @ **`732ad89`** |

## Gaps / human follow-ups

1. **rulespec-nz #80:** Resolved 2026-07-17. The maintainer reproduced the semantic fix through supervised-encoder migration #83 and closed #79/#80 with credit.
2. **openfisca-aotearoa #200:** await BetterRules review; local fork already complete for recon surfaces.
3. The former RuleSpec signing-key blocker is historical. Organisation-wide manifest provisioning remains separately tracked at `axiom-encode#1147`.
