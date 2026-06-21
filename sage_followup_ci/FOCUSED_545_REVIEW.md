# Focused Modular Review: `(5,4,5)`

Equation form: `A^5 + B^4 = C^5`.

This is a human-review packet. It separates imported Sage facts from symbolic-template assumptions and open mathematical obligations. It does not certify a theorem, contradiction, or exclusion.

## Route Status

- Current focused label: `not_available`.
- Priority: `unknown`.
- Known-case mismatches: `0`.
- Known-case overpromotions: `0`.
- Highest allowed label in this pipeline: `worth_human_modular_review`.

## Verified Sage Facts

- Sage status: `completed`.
- Checked levels: `110;220;440;550;1210`.
- Level-220 newform count: `49`.
- Trace status: `inconclusive`.
- Imported local trace rows: ell=11 support=1 traces={'0': 1}.
- Contradiction claim allowed: `False`.

## Local Survivor Rows

- ell `31`: verdict `needs_modular_shadow_follow_up`, survivors `15`, lift `persists_or_expands`, explanation: sparsity is not fully explained, but no lift collapse is known yet
- ell `11`: verdict `artifact_explained`, survivors `1`, lift `persists_or_expands`, explanation: sparsity follows from an order-two/tiny power image such as {1,-1}

## Frey Template Validity Audit

| component | classification | risk | next action |
| --- | --- | --- | --- |
| `curve_equation_used` | `verified_by_symbolic_formula` | `medium` | Derive that every primitive solution of A^5+B^4=C^5 gives this exact Frey object after orientation choices. |
| `discriminant_support` | `verified_by_symbolic_formula` | `medium` | Turn symbolic support into a minimal discriminant calculation for the 5-4-5 case. |
| `conductor_like_level_formula` | `heuristic_placeholder` | `high` | Compute the actual conductor and any lowered level from a validated minimal model. |
| `bad_prime_set` | `heuristic_placeholder` | `high` | Prove which primes are genuinely bad for the Frey curve attached to a primitive solution. |
| `reason_level_220_appears` | `heuristic_placeholder` | `high` | Decide whether 220 is an actual conductor, a lowered level, or only a search target. |
| `level_220_sage_newform_count` | `computed_by_sage` | `low` | Extract labels and q-expansion data for both level-220 newforms. |
| `level_220_status` | `needs_human_math_review` | `high` | Provide a conductor and level-lowering derivation for normalized signature 4-5-5. |
| `representation_modulus` | `needs_human_math_review` | `high` | Choose and justify the residual representation prime before interpreting trace congruences. |

## Level 220 Audit

- Factorization: `2^2 * 5 * 11`.
- Level 220 is currently a `heuristic_symbolic` route-audit target, not a verified conductor or lowered level.

| prime | exponent in 220 | why it appears | required assumption |
| ---: | ---: | --- | --- |
| 2 | 2 | Included by the split full-2-torsion Frey template and even-prime minimal-model uncertainty. | A minimal model analysis must determine the exact 2-adic conductor exponent. |
| 5 | 1 | Included from exponent radical support for the two fifth-power positions. | The residual representation and ramification at 5 must be justified. |
| 11 | 1 | Included from the local sparse row used in the Sage route audit. | A human must justify why this local prime belongs in the conductor or lowered level, rather than only in the route-audit search. |

## Level 220 Newforms

| index | label | q-expansion data | status | notes |
| ---: | --- | --- | --- | --- |
| 0 | `level220_newform_0` | `True` | `computed_by_sage` | Imported q-expansion coefficient rows are available. |
| 1 | `level220_newform_1` | `True` | `computed_by_sage` | Imported q-expansion coefficient rows are available. |
| 2 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 3 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 4 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 5 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 6 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 7 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 8 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 9 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 10 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 11 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 12 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 13 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 14 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 15 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 16 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 17 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 18 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 19 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 20 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 21 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 22 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 23 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 24 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 25 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 26 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 27 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 28 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 29 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 30 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 31 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 32 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 33 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 34 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 35 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 36 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 37 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 38 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 39 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 40 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 41 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 42 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 43 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 44 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 45 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 46 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 47 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |
| 48 | `label_unavailable` | `False` | `missing_q_expansion_data` | Sage imported the count but not labels or q-expansion coefficients. |

## Trace Comparison Audit

| level | prime | good for level | Frey traces | newform traces | mode | classification |
| ---: | ---: | --- | --- | --- | --- | --- |
| 220 | 0 | `False` | `none` | `missing` | `unknown` | `trace_data_insufficient` |

The key trace warning: the imported narrow row is at `ell=11`, and `11` divides `220`. That makes it local route evidence, not yet a clean good-prime newform trace comparison.

## Good-Prime Trace Audit

The good-prime audit excludes primes dividing `220` and excludes the residual-prime candidate `5` by default. It is designed to replace the weak `ell=11` signal with trace comparisons at primes where level-220 newform coefficients can be meaningfully tested.

- Selected good primes: `3;7;13;17;19;23;29;31;37;41;43;47;53;59;61;67;71;73;79;83;89;97`.
- Newform coefficient JSON expected at: `runs/sage_followup_ci/level_220_newform_coefficients.json`.
- Coefficient import status: `completed`; schema valid: `True`.
- Imported coefficient rows: `44`.
- Rational/integer coefficients: `44`; non-rational coefficients: `0`; unclear coefficients: `0`.
- Aggregate progress label: `trace_mismatch_candidate`.
- Usable comparisons: `44`.
- Coefficient-field blocked comparisons: `0`.
- Newforms surviving all available filters: `0` of `2`.
- Unresolved reasons: `none`.

### Frey Trace Possibilities At Good Primes

| q | survivors | nonsingular | possible traces |
| ---: | ---: | ---: | --- |
| 3 | 1 | 1 | `0` |
| 7 | 15 | 15 | `-4;0;4` |
| 13 | 33 | 33 | `-6;-2;2;6` |
| 17 | 60 | 60 | `-6;-2;2;6` |
| 19 | 153 | 153 | `-8;-4;0;4;8` |
| 23 | 231 | 231 | `-8;-4;0;4;8` |
| 29 | 189 | 189 | `-10;-6;-2;2;6;10` |
| 31 | 15 | 15 | `-8;-4;0;4;8` |
| 37 | 315 | 315 | `-10;-6;-2;2;6;10` |
| 41 | 14 | 14 | `-6;2;10` |
| 43 | 861 | 861 | `-12;-8;-4;0;4;8;12` |
| 47 | 1035 | 1035 | `-12;-8;-4;0;4;8;12` |
| 53 | 663 | 663 | `-14;-10;-6;-2;2;6;10;14` |
| 59 | 1653 | 1653 | `-12;-8;-4;0;4;8;12` |
| 61 | 33 | 33 | `-2;6;10;14` |
| 67 | 2145 | 2145 | `-16;-12;-8;-4;0;4;8;12;16` |
| 71 | 91 | 91 | `-16;-12;-8;-4;0;4;8;12;16` |
| 73 | 1278 | 1278 | `-14;-10;-6;-2;2;6;10;14` |
| 79 | 3003 | 3003 | `-16;-12;-8;-4;0;4;8;12;16` |
| 83 | 3321 | 3321 | `-16;-12;-8;-4;0;4;8;12;16` |
| 89 | 1914 | 1914 | `-18;-14;-10;-6;-2;2;6;10;14;18` |
| 97 | 2280 | 2280 | `-18;-14;-10;-6;-2;2;6;10;14;18` |

### Congruence Filter Results

| q | newform | coefficient | mode | classification | reason |
| ---: | ---: | --- | --- | --- | --- |
| 3 | 0 | `-2` | `mod_5` | `eliminated` | No Frey trace matches under the selected comparison mode. |
| 7 | 0 | `-4` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 13 | 0 | `-4` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 17 | 0 | `0` | `mod_5` | `eliminated` | No Frey trace matches under the selected comparison mode. |
| 19 | 0 | `-4` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 23 | 0 | `-6` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 29 | 0 | `-6` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 31 | 0 | `8` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 37 | 0 | `2` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 41 | 0 | `6` | `mod_5` | `eliminated` | No Frey trace matches under the selected comparison mode. |
| 43 | 0 | `8` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 47 | 0 | `6` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 53 | 0 | `-6` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 59 | 0 | `-12` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 61 | 0 | `2` | `mod_5` | `eliminated` | No Frey trace matches under the selected comparison mode. |
| 67 | 0 | `-10` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 71 | 0 | `-12` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 73 | 0 | `-16` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 79 | 0 | `8` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 83 | 0 | `0` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 89 | 0 | `6` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 97 | 0 | `14` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 3 | 1 | `2` | `mod_5` | `eliminated` | No Frey trace matches under the selected comparison mode. |
| 7 | 1 | `0` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 13 | 1 | `0` | `mod_5` | `eliminated` | No Frey trace matches under the selected comparison mode. |
| 17 | 1 | `-4` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 19 | 1 | `-4` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 23 | 1 | `6` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 29 | 1 | `2` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 31 | 1 | `0` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 37 | 1 | `-6` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 41 | 1 | `-10` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 43 | 1 | `4` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 47 | 1 | `10` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 53 | 1 | `2` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 59 | 1 | `-4` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 61 | 1 | `-14` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 67 | 1 | `2` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 71 | 1 | `4` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 73 | 1 | `-4` | `mod_5` | `survives` | A Frey trace is congruent to the coefficient modulo 5. |
| 79 | 1 | `-8` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 83 | 1 | `12` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 89 | 1 | `6` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |
| 97 | 1 | `6` | `exact` | `survives` | A Frey trace equals the newform coefficient exactly. |

### Coefficient Field Summary

| newform | q | coefficient | field kind | mod-5 reduction | status |
| ---: | ---: | --- | --- | --- | --- |
| 0 | 3 | `-2` | `rational_integer` | `3` | `completed` |
| 0 | 7 | `-4` | `rational_integer` | `1` | `completed` |
| 0 | 13 | `-4` | `rational_integer` | `1` | `completed` |
| 0 | 17 | `0` | `rational_integer` | `0` | `completed` |
| 0 | 19 | `-4` | `rational_integer` | `1` | `completed` |
| 0 | 23 | `-6` | `rational_integer` | `4` | `completed` |
| 0 | 29 | `-6` | `rational_integer` | `4` | `completed` |
| 0 | 31 | `8` | `rational_integer` | `3` | `completed` |
| 0 | 37 | `2` | `rational_integer` | `2` | `completed` |
| 0 | 41 | `6` | `rational_integer` | `1` | `completed` |
| 0 | 43 | `8` | `rational_integer` | `3` | `completed` |
| 0 | 47 | `6` | `rational_integer` | `1` | `completed` |
| 0 | 53 | `-6` | `rational_integer` | `4` | `completed` |
| 0 | 59 | `-12` | `rational_integer` | `3` | `completed` |
| 0 | 61 | `2` | `rational_integer` | `2` | `completed` |
| 0 | 67 | `-10` | `rational_integer` | `0` | `completed` |
| 0 | 71 | `-12` | `rational_integer` | `3` | `completed` |
| 0 | 73 | `-16` | `rational_integer` | `4` | `completed` |
| 0 | 79 | `8` | `rational_integer` | `3` | `completed` |
| 0 | 83 | `0` | `rational_integer` | `0` | `completed` |
| 0 | 89 | `6` | `rational_integer` | `1` | `completed` |
| 0 | 97 | `14` | `rational_integer` | `4` | `completed` |
| 1 | 3 | `2` | `rational_integer` | `2` | `completed` |
| 1 | 7 | `0` | `rational_integer` | `0` | `completed` |
| 1 | 13 | `0` | `rational_integer` | `0` | `completed` |
| 1 | 17 | `-4` | `rational_integer` | `1` | `completed` |
| 1 | 19 | `-4` | `rational_integer` | `1` | `completed` |
| 1 | 23 | `6` | `rational_integer` | `1` | `completed` |
| 1 | 29 | `2` | `rational_integer` | `2` | `completed` |
| 1 | 31 | `0` | `rational_integer` | `0` | `completed` |
| 1 | 37 | `-6` | `rational_integer` | `4` | `completed` |
| 1 | 41 | `-10` | `rational_integer` | `0` | `completed` |
| 1 | 43 | `4` | `rational_integer` | `4` | `completed` |
| 1 | 47 | `10` | `rational_integer` | `0` | `completed` |
| 1 | 53 | `2` | `rational_integer` | `2` | `completed` |
| 1 | 59 | `-4` | `rational_integer` | `1` | `completed` |
| 1 | 61 | `-14` | `rational_integer` | `1` | `completed` |
| 1 | 67 | `2` | `rational_integer` | `2` | `completed` |
| 1 | 71 | `4` | `rational_integer` | `4` | `completed` |
| 1 | 73 | `-4` | `rational_integer` | `1` | `completed` |
| 1 | 79 | `-8` | `rational_integer` | `2` | `completed` |
| 1 | 83 | `12` | `rational_integer` | `2` | `completed` |
| 1 | 89 | `6` | `rational_integer` | `1` | `completed` |
| 1 | 97 | `6` | `rational_integer` | `1` | `completed` |

If both level-220 newforms are eventually eliminated by good-prime congruence filters, this packet must call that `trace_mismatch_candidate`, not a proof or contradiction. With missing q-expansion data, the correct label is `trace_data_insufficient`; with non-rational coefficients and no justified reduction above `5`, the correct label is `coefficient_field_blocked`.

If coefficient-field handling blocks comparison, the next human check is to choose and justify the prime above `5` in the newform coefficient field, then redo the trace congruence in that residue field.

## Trace Mismatch Robustness

- First eliminating primes: `newform_0:q=3;newform_1:q=3`.
- Excluding `q=3`: `trace_mismatch_candidate` with `2` eliminated newforms.
- Using only `q >= 17`: `trace_survivor_exists` with `1` eliminated newforms.
- Local coverage gaps: `22` selected good primes.
- Level 220 robustness label: `level_220_mismatch_candidate`.
- Nearby levels still lacking coefficient data: `27`.
- Local valuation scope label: `unit_only_trace_mismatch_candidate`.
- Overall local gap label: `local_coverage_gap`.
- q=13 full local coverage: `False`.
- q=17 full local coverage: `False`.

### Trace Mismatch Provenance

| newform | q | a_q | mode | classification | first eliminator |
| ---: | ---: | --- | --- | --- | --- |
| 0 | 3 | `-2` | `mod_5` | `eliminated` | `True` |
| 0 | 7 | `-4` | `exact` | `survives` | `False` |
| 0 | 13 | `-4` | `mod_5` | `survives` | `False` |
| 0 | 17 | `0` | `mod_5` | `eliminated` | `False` |
| 0 | 19 | `-4` | `exact` | `survives` | `False` |
| 0 | 23 | `-6` | `mod_5` | `survives` | `False` |
| 0 | 29 | `-6` | `exact` | `survives` | `False` |
| 0 | 31 | `8` | `exact` | `survives` | `False` |
| 0 | 37 | `2` | `exact` | `survives` | `False` |
| 0 | 41 | `6` | `mod_5` | `eliminated` | `False` |
| 0 | 43 | `8` | `exact` | `survives` | `False` |
| 0 | 47 | `6` | `mod_5` | `survives` | `False` |
| 0 | 53 | `-6` | `exact` | `survives` | `False` |
| 0 | 59 | `-12` | `exact` | `survives` | `False` |
| 0 | 61 | `2` | `mod_5` | `eliminated` | `False` |
| 0 | 67 | `-10` | `mod_5` | `survives` | `False` |
| 0 | 71 | `-12` | `exact` | `survives` | `False` |
| 0 | 73 | `-16` | `mod_5` | `survives` | `False` |
| 0 | 79 | `8` | `exact` | `survives` | `False` |
| 0 | 83 | `0` | `exact` | `survives` | `False` |
| 0 | 89 | `6` | `exact` | `survives` | `False` |
| 0 | 97 | `14` | `exact` | `survives` | `False` |
| 1 | 3 | `2` | `mod_5` | `eliminated` | `True` |
| 1 | 7 | `0` | `exact` | `survives` | `False` |
| 1 | 13 | `0` | `mod_5` | `eliminated` | `False` |
| 1 | 17 | `-4` | `mod_5` | `survives` | `False` |
| 1 | 19 | `-4` | `exact` | `survives` | `False` |
| 1 | 23 | `6` | `mod_5` | `survives` | `False` |
| 1 | 29 | `2` | `exact` | `survives` | `False` |
| 1 | 31 | `0` | `exact` | `survives` | `False` |
| 1 | 37 | `-6` | `exact` | `survives` | `False` |
| 1 | 41 | `-10` | `mod_5` | `survives` | `False` |
| 1 | 43 | `4` | `exact` | `survives` | `False` |
| 1 | 47 | `10` | `mod_5` | `survives` | `False` |
| 1 | 53 | `2` | `exact` | `survives` | `False` |
| 1 | 59 | `-4` | `exact` | `survives` | `False` |
| 1 | 61 | `-14` | `mod_5` | `survives` | `False` |
| 1 | 67 | `2` | `mod_5` | `survives` | `False` |
| 1 | 71 | `4` | `exact` | `survives` | `False` |
| 1 | 73 | `-4` | `mod_5` | `survives` | `False` |
| 1 | 79 | `-8` | `exact` | `survives` | `False` |
| 1 | 83 | `12` | `exact` | `survives` | `False` |
| 1 | 89 | `6` | `exact` | `survives` | `False` |
| 1 | 97 | `6` | `exact` | `survives` | `False` |

### Small-Prime Sensitivity

| profile | surviving | eliminated | first eliminators | label |
| --- | ---: | ---: | --- | --- |
| `exclude_q_3` | 0 | 2 | `newform_0:q=17;newform_1:q=13` | `trace_mismatch_candidate` |
| `exclude_q_3_7` | 0 | 2 | `newform_0:q=17;newform_1:q=13` | `trace_mismatch_candidate` |
| `exclude_q_lt_11` | 0 | 2 | `newform_0:q=17;newform_1:q=13` | `trace_mismatch_candidate` |
| `exclude_q_lt_17` | 1 | 1 | `newform_0:q=17` | `trace_survivor_exists` |
| `use_only_q_ge_17` | 1 | 1 | `newform_0:q=17` | `trace_survivor_exists` |

### Local Coverage Audit

| q | unit residue cases | zero-support cases | excluded cases | label |
| ---: | ---: | ---: | ---: | --- |
| 3 | 2 | 7 | 7 | `local_coverage_gap` |
| 7 | 30 | 19 | 19 | `local_coverage_gap` |
| 13 | 132 | 37 | 37 | `local_coverage_gap` |
| 17 | 240 | 49 | 49 | `local_coverage_gap` |
| 19 | 306 | 55 | 55 | `local_coverage_gap` |
| 23 | 462 | 67 | 67 | `local_coverage_gap` |
| 29 | 756 | 85 | 85 | `local_coverage_gap` |
| 31 | 750 | 211 | 211 | `local_coverage_gap` |
| 37 | 1260 | 109 | 109 | `local_coverage_gap` |
| 41 | 1400 | 281 | 281 | `local_coverage_gap` |
| 43 | 1722 | 127 | 127 | `local_coverage_gap` |
| 47 | 2070 | 139 | 139 | `local_coverage_gap` |
| 53 | 2652 | 157 | 157 | `local_coverage_gap` |
| 59 | 3306 | 175 | 175 | `local_coverage_gap` |
| 61 | 3300 | 421 | 421 | `local_coverage_gap` |
| 67 | 4290 | 199 | 199 | `local_coverage_gap` |
| 71 | 4550 | 491 | 491 | `local_coverage_gap` |
| 73 | 5112 | 217 | 217 | `local_coverage_gap` |
| 79 | 6006 | 235 | 235 | `local_coverage_gap` |
| 83 | 6642 | 247 | 247 | `local_coverage_gap` |
| 89 | 7656 | 265 | 265 | `local_coverage_gap` |
| 97 | 9120 | 289 | 289 | `local_coverage_gap` |

### Local Valuation And Frey Reduction Coverage

| q | eliminated newforms | nonunit possible | nonunit unresolved | full local coverage | label |
| ---: | ---: | ---: | ---: | --- | --- |
| 3 | 2 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 7 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 13 | 1 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 17 | 1 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 19 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 23 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 29 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 31 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 37 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 41 | 1 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 43 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 47 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 53 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 59 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 61 | 1 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 67 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 71 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 73 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 79 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 83 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 89 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 97 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |

Local gap summary: `local_coverage_gap`. Exact next lemma: Local valuation and reduction case split for q | ABC: prove that each single-divisibility mask either cannot occur for primitive solutions at the eliminating primes, or gives a separate modular/reduction argument compatible with the trace filter.

### Level Robustness

| level | newforms | coefficient status | trace status | label |
| ---: | ---: | --- | --- | --- |
| 5 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 10 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 11 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 20 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 22 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 25 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 40 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 44 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 50 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 55 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 88 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 100 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 110 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 121 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 200 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 220 | 2 | `completed` | `trace_mismatch_candidate` | `level_220_mismatch_candidate` |
| 242 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 275 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 440 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 484 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 550 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 605 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 880 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 968 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 1100 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 1210 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 2200 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |
| 2420 | 0 | `not_checked` | `not_checked` | `level_data_insufficient` |

### Theorem Skeleton Summary

| obligation | status | risk | next action |
| --- | --- | --- | --- |
| `TS545-001` | `conditional_setup` | `medium` | State sign, nonzero, coprimality, and normalization conventions exactly. |
| `TS545-002` | `needs_hand_derivation` | `high` | Derive nonsingularity and integral model conditions for all primitive solution cases. |
| `TS545-003` | `needs_hand_derivation` | `high` | Run a prime-by-prime minimal model and conductor analysis. |
| `TS545-004` | `missing` | `high` | Identify the exact representation and prove irreducibility or state required exceptions. |
| `TS545-005` | `needs_hand_derivation` | `high` | Justify why the comparison level is 220 and why no nearby level should be used instead. |
| `TS545-006` | `computed_route_evidence` | `medium` | Confirm old/new decomposition, character choices, coefficient fields, and labels in Sage or Magma. |
| `TS545-007` | `computed_route_evidence` | `medium` | Check the first eliminating primes independently and justify the local enumeration. |
| `TS545-008` | `local_coverage_gap` | `high` | Prove the local valuation and reduction case split for q | ABC, including single-divisibility masks and singular Frey reductions. |
| `TS545-009` | `computed_route_evidence` | `medium` | Decide whether q=13 or q=17 sensitivity should be part of the human check. |

The exact next human mathematical task is to prove the Frey attachment, conductor/level-lowering, residual mod-5 irreducibility, level-220 target-space exhaustion, and local-coverage lemmas needed to turn this route evidence into a valid modular argument.

## Assumption Register

| id | status | risk | required for | next action |
| --- | --- | --- | --- | --- |
| `A545-001` | `needs_human_math_review` | `high` | Frey object attachment | Write the algebraic derivation and check orientation, primitivity, and singular cases. |
| `A545-002` | `needs_human_math_review` | `high` | conductor calculation | Compute the minimal discriminant and conductor exponents prime by prime. |
| `A545-003` | `heuristic_placeholder` | `high` | newform search at level 220 | Derive the true conductor and justify level lowering to 220 if applicable. |
| `A545-004` | `missing` | `high` | level lowering | Prove irreducibility for the chosen residual representation. |
| `A545-005` | `needs_human_math_review` | `medium` | trace congruence interpretation | Justify the representation prime; distinguish mod 5 from the full-2-torsion structure. |
| `A545-006` | `needs_human_math_review` | `high` | newform exclusion step | Confirm coefficient field handling, old/new decomposition choices, nebentypus assumptions, and exact target space. |
| `A545-007` | `computed_by_sage` | `low` | review prioritization | Export labels and q-expansion coefficients for independent review. |
| `A545-008` | `needs_human_math_review` | `high` | local-to-global trace use | Repeat trace comparisons at good primes for the justified level and compare against same-size controls. |
| `A545-009` | `heuristic_placeholder` | `high` | good-prime newform filtering | Prove level 220 is the true conductor or a justified lowered level before treating its newforms as exhaustive. |
| `A545-010` | `needs_human_math_review` | `high` | mod-5 trace comparisons | Justify the residual representation prime and its coefficient-field reduction map. |
| `A545-011` | `needs_human_math_review` | `high` | Frey trace possibility sets | Derive the template from a primitive solution and prove nonsingularity at selected good primes. |
| `A545-012` | `missing` | `high` | newform trace congruence filtering | Export coefficient fields and define the exact reduction before interpreting non-rational coefficients. |
| `A545-013` | `needs_human_math_review` | `medium` | completeness of Frey trace possibilities | Prove that enumerating nonzero power-image triples u+v=w covers every primitive reduction at good primes. |

## Gap Summary

| category | status | risk | required next lemma |
| --- | --- | --- | --- |
| `algebraic_derivation_gap` | `open` | `high` | Prove the Frey-curve attachment lemma for A^5+B^4=C^5, including primitivity and nonsingularity conditions. |
| `conductor_gap` | `open` | `high` | Compute the exact conductor of the attached Frey curve and justify every prime/exponent in the level. |
| `irreducibility_gap` | `open` | `high` | Prove irreducibility for the justified residual representation prime. |
| `level_lowering_gap` | `open` | `high` | Verify the hypotheses for lowering from the true conductor to the claimed comparison level. |
| `newform_trace_gap` | `open` | `high` | Export and compare relevant newform coefficients at good primes using the justified modulus. |
| `local_to_global_gap` | `open` | `high` | Show how local survivor traces constrain the global modular representation, or replace with good-prime trace comparisons. |
| `local_valuation_reduction_gap` | `open` | `high` | Prove the local valuation and reduction case split for q | ABC, including single-divisibility masks and singular Frey reductions. |
| `control_artifact_gap` | `open` | `medium` | Separate artifact local behavior from reusable modular constraints and connect any non-artifact rows to the Frey route. |

## Exact Next Theorem Or Lemma

A human should next prove the Frey-curve attachment and conductor/level-lowering package for `A^5 + B^4 = C^5`: every primitive solution gives the stated Frey object; the residual representation at the justified modulus is irreducible; the true conductor lowers to the claimed comparison level; and the two level-220 newforms, with actual q-expansion coefficients at good primes, fail or pass the justified trace congruence test.

## Timeout Retry Note

The timeout retry manifest remains focused on `(3,5,5)`, `(5,5,7)`, and `(7,7,4)`. Those retries should not change the interpretation of this focused `(5,4,5)` packet unless new data is explicitly imported and this report is regenerated.

## Generated Sidecars

- `runs/sage_followup_ci/frey_template_validity_545.csv`
- `runs/sage_followup_ci/level_220_prime_audit.csv`
- `runs/sage_followup_ci/level_220_newforms.csv`
- `runs/sage_followup_ci/trace_comparison_545.csv`
- `runs/sage_followup_ci/good_prime_list_545.csv`
- `runs/sage_followup_ci/sage_level_220_newform_expander.sage`
- `runs/sage_followup_ci/frey_trace_possibilities_545.csv`
- `runs/sage_followup_ci/trace_congruence_filter_545.csv`
- `runs/sage_followup_ci/obstruction_progress_545.csv`
- `runs/sage_followup_ci/level_220_coefficient_import_summary.csv`
- `runs/sage_followup_ci/level_220_coefficient_rows.csv`
- `runs/sage_followup_ci/trace_mismatch_provenance_545.csv`
- `runs/sage_followup_ci/TRACE_MISMATCH_PROVENANCE_545.md`
- `runs/sage_followup_ci/small_prime_sensitivity_545.csv`
- `runs/sage_followup_ci/SMALL_PRIME_SENSITIVITY_545.md`
- `runs/sage_followup_ci/local_coverage_audit_545.csv`
- `runs/sage_followup_ci/LOCAL_COVERAGE_AUDIT_545.md`
- `runs/sage_followup_ci/frey_invariant_sanity_545.csv`
- `runs/sage_followup_ci/FREY_INVARIANT_SANITY_545.md`
- `runs/sage_followup_ci/level_robustness_545.csv`
- `runs/sage_followup_ci/LEVEL_220_ROBUSTNESS_545.md`
- `runs/sage_followup_ci/THEOREM_SKELETON_545.md`
- `runs/sage_followup_ci/theorem_skeleton_obligations_545.csv`
- `runs/sage_followup_ci/local_valuation_cases_545.csv`
- `runs/sage_followup_ci/valuation_mask_lift_545.csv`
- `runs/sage_followup_ci/frey_reduction_cases_545.csv`
- `runs/sage_followup_ci/trace_filter_case_coverage_545.csv`
- `runs/sage_followup_ci/local_gap_summary_545.csv`
- `runs/sage_followup_ci/LOCAL_GAP_SUMMARY_545.md`
- `runs/sage_followup_ci/assumption_register_545.csv`
- `runs/sage_followup_ci/proof_gap_summary.csv`
- `runs/sage_followup_ci/proof_gap_report.md`
