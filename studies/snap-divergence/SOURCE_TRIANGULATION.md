# SNAP Source Triangulation Pack

Track: `divergence_study_20260704`

Prepared: 2026-07-06 local time.

Status: source pack for human adjudication and earlier-decision audit. This file does not decide which engine is legally correct and does not label any divergence as a confirmed bug.

## How To Use This Pack

Use sources in this order:

1. Federal statute/regulation, current eCFR, and USDA/FNS FY2026 guidance for federal SNAP eligibility, resources, deductions, and allotments.
2. Current state agency manuals, state agency memos, and USDA/FNS state-option tables for state implementation choices.
3. Engine source code and local runner evidence for what PRD and PolicyEngine actually computed.
4. Secondary research or advocacy sources only as cross-checks, context, or pointers to primary sources.

Do not use secondary sources alone to mark `confirmed_bug_policyengine` or `confirmed_bug_prd`.

## Federal And USDA/FNS Sources

| Source | Use | Notes |
|---|---|---|
| [USDA/FNS SNAP Eligibility](https://www.fns.usda.gov/snap/recipient/eligibility) | FY2026 income/resource limits, broad BBCE explanation, monthly benefit formula, max allotment table, excess shelter overview. | Page says the information applies Oct. 1, 2025 through Sept. 30, 2026. Use for the study's `2026-01` scope and general federal tables. |
| [FY2026 SNAP maximum allotments and deductions PDF](https://fns-prod.azureedge.us/sites/default/files/resource-files/snap-fy26maximumAllotments-deductions.pdf) | Monthly maximum allotments and allowable deductions for FY2026. | Primary FNS table for fixture and runner normalization. |
| [FY2026 SNAP COLA memo](https://www.usda.gov/sites/default/files/guidance-documents/fns.snap-cola-fy26memo.pdf) | FY2026 COLA changes; resource limits; shelter cap; standard deduction; minimum benefit. | Useful for confirming that $3,000/$4,500 resource limits stayed unchanged in FY2026. |
| [7 CFR 273.9, Income and deductions](https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-C/part-273/subpart-D/section-273.9) | Gross/net income standards, categorical eligibility exemption from income standards, deduction categories, standard utility allowance rules, HCSUA/LIHEAP trigger. | eCFR is current but not the official print CFR. Use as the current regulatory text unless a point-in-time legal issue arises. |
| [7 CFR 273.8, Resource eligibility standards](https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-C/part-273/subpart-D/section-273.8) | Federal resource standards and categorical eligibility exemption from resource limits. | Use for asset-test questions before applying state BBCE surfaces. |
| [7 CFR 273.2, Categorical eligibility](https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-C/part-273/subpart-A/section-273.2) | Categorical eligibility via PA/SSI/TANF/MOE non-cash benefits and deemed resource/gross/net factors. | Central source for BBCE route differences between direct SNAP tests and TANF non-cash categorical pathways. |
| [FNS Broad-Based Categorical Eligibility chart](https://www.fns.usda.gov/snap/broad-based-categorical-eligibility) | State BBCE program descriptions, asset limits, and gross income limits. | Live-checked page showed Georgia: no asset limit, 130%; Pennsylvania: no asset limit, 200%; Texas: $5,000 asset limit with vehicle treatment, 165%. Mississippi is not listed in the 46-state BBCE chart. |
| [FNS State Options Report page](https://www.fns.usda.gov/snap/waivers/state-options-report) | Current and prior state-option reports, citations, option profiles, state profiles. | Use latest report for state-option context, not as a substitute for a state manual when adjudicating a specific case. |
| [SNAP State Options Report, 17th edition PDF](https://fns-prod.azureedge.us/sites/default/files/resource-files/snap-stateOptionsReport-17edition-120925.pdf) | State-option profiles current as of Oct. 1, 2024. | Useful for background and consistency checks across states; not enough alone for a Jan. 2026 confirmed-bug call. |

## State Sources For Open Adjudication Groups

### Georgia Limited-BBCE / Gross-Income Cases

Cases:

- `us-snap/fixture.ga_bbce_165_boundary`
- `us-snap/fixture.ga_gross_130_above`
- `us-snap/fixture.ga_gross_130_below`

Primary sources to consult:

- [Georgia PAMMS Appendix A SNAP Income Limits](https://pamms.dhs.ga.gov/dfcs/snap/appendix-a-food-stamp-income-limits/) - effective October 2025 table for 130% gross, 100% net, elderly/disabled 165%, and FY2026 max allotments.
- [Georgia PAMMS 3610 SNAP Budgeting](https://pamms.dhs.ga.gov/dfcs/snap/3610/) - gross income ceiling and net income limit rules.
- [FNS BBCE chart](https://www.fns.usda.gov/snap/broad-based-categorical-eligibility) - Georgia BBCE surface: all households; no asset limit; 130% gross income limit.
- [NCCP Georgia SNAP profile](https://www.nccp.org/wp-content/uploads/2024/08/SNAP-profile-Georgia.pdf) - secondary cross-check that Georgia has BBCE but still uses a 130% gross limit.

Triangulation target:

- Decide whether a fixture above 130% gross but below 165% should ever be expected to pass for Georgia in FY2026 under the fixture assumptions.
- If the answer is no, the divergence is likely an expected modeling/fixture-surface difference rather than a confirmed engine bug.

### Texas BBCE / Asset Cases

Cases:

- `us-snap/fixture.tx_asset_above_limit`
- `us-snap/fixture.tx_bbce_165_boundary`
- `us-snap/fixture.tx_gross_130_above`
- `us-snap/fixture.tx_gross_130_below`

Primary sources to consult:

- [FNS BBCE chart](https://www.fns.usda.gov/snap/broad-based-categorical-eligibility) - Texas BBCE surface: all households; $5,000 asset limit; excludes one vehicle up to $22,000 and includes excess vehicle value; 165% gross income limit.
- [Texas Works Handbook B-470, Categorically Eligible Households](https://www.hhs.texas.gov/handbooks/texas-works-handbook/b-470-categorically-eligible-households) - search index text confirms the $5,000 combined resource limit and says categorically eligible households are not subject to resource and gross/net income limits once the categorical route is met.
- [Texas Works Handbook A-1220, Limits](https://www.hhs.texas.gov/handbooks/texas-works-handbook/a-1220-limits) - search index text confirms SNAP ineligibility when countable resources plus excess vehicle value are over $5,000.
- [Texas Works Handbook C-120, Supplemental Nutrition Assistance Program](https://www.hhs.texas.gov/handbooks/texas-works-handbook/c-120-supplemental-nutrition-assistance-program) - search index text confirms Texas SNAP allotment/income and utility allowance values, including SUA/BUA/telephone allowance.

Access note:

- Texas HHSC pages returned Akamai "Access Denied" to both browser and CLI fetches in this session. The FNS BBCE chart is still a strong primary source for the state-option surface, but a human reviewer should open the Texas handbook in a normal browser before marking any Texas case as a confirmed bug.

Triangulation target:

- Distinguish "Texas BBCE categorical eligibility with its TANF/MOE gross/resource screen" from "regular SNAP gross/net/resource tests."
- Confirm how the fixture's `total_assets_monthly` should be interpreted against the Texas combined liquid-resource-plus-excess-vehicle surface.

### Mississippi Non-BBCE / Resource / Gross Cases

Cases:

- `us-snap/fixture.ms_asset_above_limit`
- `us-snap/fixture.ms_bbce_165_boundary`
- `us-snap/fixture.ms_gross_130_above`
- `us-snap/fixture.ms_gross_130_below`

Primary sources to consult:

- [Mississippi MDHS SNAP page](https://www.mdhs.ms.gov/help/snap/) - state page says SNAP eligibility includes income and resource limits and lists FY2026 gross/net/max-benefit values effective Oct. 1, 2025.
- [Mississippi SNAP Policy Manual PDF](https://www.sos.ms.gov/adminsearch/ACCode/00000331c.pdf) - revised Dec. 20, 2025. Chapter 15 covers categorical eligibility; Chapter 16 covers resources; Chapter 17 sets gross income at 130% FPL and net income at 100% FPL.
- [FNS BBCE chart](https://www.fns.usda.gov/snap/broad-based-categorical-eligibility) - Mississippi is not listed among states implementing BBCE on the current FNS chart.
- [NCCP Mississippi SNAP profile](https://www.nccp.org/wp-content/uploads/2024/08/SNAP-profile-Mississippi.pdf) - secondary cross-check that Mississippi has not adopted BBCE.

Triangulation target:

- Confirm whether the fixture assumptions should be treated as regular non-BBCE SNAP unless every household member is TANF/SSI categorically eligible.
- For upstream issue drafting, prefer the MDHS manual plus FNS federal resource/income sources over secondary summaries.

### Mississippi Phone-Only Utility Case

Case:

- `us-snap/fixture.ms_utility_allowance_phone_only`

Primary sources to consult:

- [Mississippi SNAP Policy Manual PDF](https://www.sos.ms.gov/adminsearch/ACCode/00000331c.pdf) - use Chapter 18 expenses/deductions and Chapter 30 benefit-level rules.
- [7 CFR 273.9 standard utility allowance rules](https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-C/part-273/subpart-D/section-273.9) - allowable utility-cost categories; standard utility allowance types; HCSUA and LUA rules.
- [FNS SNAP Eligibility page](https://www.fns.usda.gov/snap/recipient/eligibility) - high-level federal shelter-cost list includes the basic fee for one telephone.

Triangulation target:

- Decide whether the fixture should explicitly encode phone-only, limited utilities, or heating/cooling responsibility for both engines.
- This is currently non-decision-relevant; likely disposition remains `fixture_adapter_issue` unless the manual proves one engine's utility classification is plainly wrong.

### Pennsylvania Heat-and-Eat / SUA Cases

Cases:

- `us-snap/fixture.pa_bbce_165_boundary`
- `us-snap/fixture.pa_gross_130_above`
- `us-snap/fixture.pa_gross_130_below`

Primary sources to consult:

- [Pennsylvania SNAP Income Limits](https://www.pa.gov/agencies/dhs/resources/snap/snap-income-limits) - effective Oct. 1, 2025 maximum gross monthly income table; household size 1 starts at $2,610, consistent with 200% FPL.
- [Pennsylvania Federal Poverty Income Guidelines](https://www.pa.gov/agencies/dhs/resources/data-reports/federal-poverty-income-guidelines) - same SNAP income guideline table for October 2025 through October 2026.
- [Pennsylvania OPS-25-10-01 HSUA/LIHEAP memo](https://www.pa.gov/content/dam/copapwp-pagov/en/dhs/documents/docs/publications/oim-pcs-and-ops-memos/ops-25-10-01-hsua-liheap.pdf) - effective Oct. 27, 2025 changes to automatic HSUA based on LIHEAP/Heat-and-Eat; H&E limited to SNAP households with an elderly or disabled member, while other households may still qualify with heating/cooling responsibility.
- [PA SNAP Handbook operations-memo index](https://services.dpw.state.pa.us/oimpolicymanuals/snap/500_OpsMemos_PolicyClarifications/SNAP_Handbook_Operations_Memoranda.htm) - index entry for OPS-25-10-01.
- [PA SNAP Manual 560.8 Shelter/Utility Deduction](https://services.dpw.state.pa.us/oimpolicymanuals/snap/560_Income_Deductions/560_8_Shelter_Utility_Deduction.htm) - manual-review target for shelter/utility deduction details.
- [PA SNAP Manual 560 Appendix A](https://services.dpw.state.pa.us/oimpolicymanuals/snap/560_Income_Deductions/560_Appendix_A.htm) - manual-review target for standard deduction and utility allowance tables.

Access note:

- PA manual pages timed out in CLI fetches during this session, while the PA memo PDF and PA income-limit pages were accessible. Before drafting a confirmed bug issue on PA utility values, a human reviewer should reopen 560.8 and Appendix A in a browser or obtain the current manual export.

Triangulation target:

- Split two questions: Pennsylvania BBCE/income eligibility appears separately supported by the 200% state guideline and FNS BBCE chart; the remaining divergence is the utility/SUA/Heat-and-Eat treatment.
- For January 2026 fixtures, the Oct. 27, 2025 HSUA change matters if the fixture assumes automatic Heat-and-Eat without elderly/disabled status or without explicit heating/cooling responsibility.

## Existing Ontology And Standards Sources For Earlier Decisions

These sources help audit the earlier "do not build a new ontology/crosswalk without a consumer" and "use narrow JSON contracts first" decisions. They are not sources for SNAP legal correctness.

| Source | What it helps triangulate | Implication for this repo |
|---|---|---|
| [OASIS LegalRuleML Core Specification 1.0](https://www.oasis-open.org/standard/legalruleml-core-specification-version-1-0-oasis-standard/) | Existing legal-rule markup standard for normative rules. | Supports the decision not to claim novelty as a general legal-rule ontology. Use as related work, not as a required Track 5 dependency. |
| [OASIS Akoma Ntoso 1.0](https://www.oasis-open.org/standard/akn-v1-0/) | Existing legal-document interchange standard for legislative, parliamentary, and judicial documents. | Reinforces that source-document markup and executable benefit-engine fixtures are different layers. |
| [W3C PROV-O](https://www.w3.org/TR/prov-o/) | Existing provenance ontology. | Useful precedent for provenance semantics, but Track 5 already has concrete PIC provenance fields and engine-run evidence. |
| [W3C SHACL](https://www.w3.org/TR/shacl/) | Existing RDF graph validation standard. | Supports the validation concept; does not require making this SNAP study RDF-first. |
| [PolicyEngine TAXSIM validation](https://policyengine.github.io/policyengine-us/validation/taxsim.html) | Existing differential-validation precedent in tax. | Supports Track 5's empirical comparison strategy and paper related-work section. |
| [PolicyEngine-NBER TAXSIM MOU](https://www.policyengine.org/us/research/policyengine-nber-mou-taxsim) | Maintainer-recognized model-to-model validation program. | Supports the choice to run real independent engines rather than a common reimplementation. |
| [PolicyEngine policyengine-taxsim repo](https://github.com/PolicyEngine/policyengine-taxsim) | Concrete implementation of a compatibility/emulation harness. | Useful comparator for issue style, tolerances, and evidence expectations. |
| [PolicyEngine-Atlanta Fed PRD MOU](https://www.policyengine.org/us/research/policyengine-atlanta-fed-mou-prd) | Direct precedent for comparing PolicyEngine with PRD. | Supports the choice of PRD as the independent comparison engine. |
| [DBN Rules as Code Community of Practice](https://digitalgovernmenthub.org/library/rules-as-code-community-of-practice/) | Public-benefits audience and policy-to-code problem framing. | Supports the dissemination target and benefits-domain relevance. |
| [DBN Cross-Sector Insights from the Rules as Code Community of Practice](https://digitalgovernmenthub.org/publications/cross-sector-insights-from-the-rules-as-code-community-of-practice/) | Practitioner interest in sharing rules, tools, code, and standards. | Supports evidence-first engagement without prematurely proposing a new standard. |
| [AI-Powered Rules as Code: Experiments with Public Benefits Policy](https://digitalgovernmenthub.org/publications/ai-powered-rules-as-code-experiments-with-public-benefits-policy/) | AI-to-code experiments in SNAP/Medicaid and the verification problem. | Supports the repo rule that AI may draft but deterministic code and humans validate. |

## Earlier Decision Audit Map

| Earlier decision | Sources to use for triangulation | What would change the decision |
|---|---|---|
| Scope locked to SNAP, `2026-01`, CA/TX/PA/MS/GA. | FNS FY2026 eligibility/allotment sources; PRD notes; PolicyEngine notes; FNS BBCE/state-option sources. | Evidence that PRD or PolicyEngine lacked Jan. 2026 coverage for a state or that a state option materially changed before Jan. 2026 and is unmodeled. |
| Use real PRD R code, not a Python rewrite. | Local PRD runner notes; PRD `function.snapBenefit`; PolicyEngine TAXSIM/PRD validation precedent. | Only changes if PRD cannot be run or licensed, which Phase 1/3 evidence already disproved locally. |
| Monthly/annual normalization in runners. | FNS monthly FY2026 allotment tables; PRD source returning annualized `snapValue`; PolicyEngine monthly `snap`; local comparison evidence. | A source-level finding that either engine output was misinterpreted as monthly/annual. |
| Promote 50 agreement cases as approved fixtures. | FNS FY2026 federal tables; state income/BBCE pages; approved runner evidence; human approval note in plan. | Discovery that any promoted fixture encoded a state option not supported by primary sources or did not have independent provenance. |
| Hold 15 divergences out of golden fixtures. | Candidate comparison evidence; source-level classification; this source pack. | Human adjudication can move specific cases into expected modeling differences, fixture adapter issues, or confirmed bug issue drafts, but not into golden fixtures without a separate approval step. |
| Classify Georgia/Texas as state-option modeling. | FNS BBCE chart; Georgia PAMMS; Texas Works Handbook manual-review target; eCFR categorical eligibility. | A primary state source showing a different FY2026 gross/resource route than currently captured. |
| Classify Mississippi gross/BBCE cases as parameter-vintage/surface mismatch. | MDHS SNAP page; MDHS manual; eCFR 273.8/273.9; FNS BBCE chart; NCCP secondary profile. | A primary source proving Mississippi adopted BBCE for the relevant household class by Jan. 2026. |
| Classify PA cases as deduction handling. | PA income guidelines; PA HSUA/LIHEAP memo; PA 560.8 and Appendix A manual-review targets; eCFR 273.9. | A current PA manual table showing the exact HCSUA/SUA value and trigger used by one engine, or showing that the fixture assumption should be rewritten. |
| Keep ontology/standard work out of Track 5. | LegalRuleML, Akoma Ntoso, PROV-O, SHACL; DBN/Policy2Code sources. | A real consumer asks for one of these formats in a concrete converter or submission target. Otherwise, cite them as related work. |

## Remaining Source-Gathering Gaps

- Texas HHSC pages should be opened in a normal browser or obtained as an official PDF/manual export before confirmed-bug issue drafting.
- PA SNAP manual 560.8 and Appendix A should be reopened or exported before confirmed-bug issue drafting on exact utility allowance values.
- If a case is elevated to `confirmed_bug_*`, add the exact source excerpt, effective date, and engine permalink to the issue draft. Do not rely on this pack's summary alone.
