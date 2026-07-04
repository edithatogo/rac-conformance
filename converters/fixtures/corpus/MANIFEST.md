# Fixture Converter Corpus Manifest

Status: Draft | Generated for `fixture_converter_20260704`

The corpus vendors small YAML test samples for deterministic converter validation. Both source projects are AGPL-licensed; vendoring these excerpts with attribution keeps the sample corpus reviewable inside this repository and does not change the upstream licenses.

## Source Repositories

| Ecosystem | Source repo | Commit | License |
|---|---|---:|---|
| OpenFisca | `openfisca/openfisca-france` | `6eeee2e09b9f807ab3735ef494a92001a975f4ad` | AGPL-3.0 (`LICENSE.AGPL.txt`) |
| PolicyEngine | `PolicyEngine/policyengine-us` | `fc64cef64ab55c3c48309c7fb304c35e5f3c9184` | AGPL-3.0 (`LICENSE`) |

`openfisca-aotearoa` was attempted first but was unavailable at the expected GitHub URL, so `openfisca-france` is used as the plan's fallback country package.

## OpenFisca Samples

| Local file | Source path |
|---|---|
| `openfisca/thesard_2011-07.yaml` | `tests/fiches_de_paie/thesard_2011-07.yaml` |
| `openfisca/aah_eligible.yaml` | `tests/formulas/aah/aah_eligible.yaml` |
| `openfisca/aide_logement_non_calculable.yaml` | `tests/formulas/aide_logement_non_calculable.yaml` |
| `openfisca/arrco_tranche_a_employeur.yaml` | `tests/formulas/arrco_tranche_a_employeur.yaml` |
| `openfisca/caah.yaml` | `tests/formulas/caah.yaml` |
| `openfisca/cf.yaml` | `tests/formulas/cf.yaml` |
| `openfisca/formation_professionnelle.yaml` | `tests/formulas/formation_professionnelle.yaml` |
| `openfisca/glo.yaml` | `tests/formulas/glo.yaml` |
| `openfisca/irpp_niches_fiscales.yaml` | `tests/formulas/irpp_niches_fiscales.yaml` |
| `openfisca/irpp_pret_etudiant.yaml` | `tests/formulas/irpp_pret_etudiant.yaml` |

## PolicyEngine Samples

| Local file | Source path |
|---|---|
| `policyengine/basic_income.yaml` | `policyengine_us/tests/policy/baseline/contrib/ubi_center/basic_income.yaml` |
| `policyengine/marketplace_csr_eligible.yaml` | `policyengine_us/tests/policy/baseline/gov/aca/csr/marketplace_csr_eligible.yaml` |
| `policyengine/marketplace_effective_actuarial_value.yaml` | `policyengine_us/tests/policy/baseline/gov/aca/csr/marketplace_effective_actuarial_value.yaml` |
| `policyengine/coverage_report_model_conflict.yaml` | `policyengine_us/tests/policy/baseline/gov/aca/eligibility/coverage_report_model_conflict.yaml` |
| `policyengine/has_qualifying_non_marketplace_health_coverage_at_interview.yaml` | `policyengine_us/tests/policy/baseline/gov/aca/eligibility/has_qualifying_non_marketplace_health_coverage_at_interview.yaml` |
| `policyengine/is_aca_eshi_eligible.yaml` | `policyengine_us/tests/policy/baseline/gov/aca/eligibility/is_aca_eshi_eligible.yaml` |
| `policyengine/is_aca_ptc_immigration_status_eligible.yaml` | `policyengine_us/tests/policy/baseline/gov/aca/eligibility/is_aca_ptc_immigration_status_eligible.yaml` |
| `policyengine/lcbp_age_0.yaml` | `policyengine_us/tests/policy/baseline/gov/aca/lcbp/lcbp_age_0.yaml` |
| `policyengine/lcbp_person.yaml` | `policyengine_us/tests/policy/baseline/gov/aca/lcbp/lcbp_person.yaml` |
| `policyengine/aca_required_contribution_percentage.yaml` | `policyengine_us/tests/policy/baseline/gov/aca/ptc/aca_required_contribution_percentage.yaml` |
