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
- Local valuation scope label: `local_trace_mismatch_candidate`.
- Overall local gap label: `local_case_elimination_candidate`.
- Focused eliminating primes: `3;13;17;41;61`.
- Best ranked eliminating prime: `3` with label `local_case_elimination_candidate`.

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
| 3 | 2 | 3 | 0 | `True` | `local_case_elimination_candidate` |
| 7 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 13 | 1 | 3 | 0 | `False` | `local_coverage_gap` |
| 17 | 1 | 3 | 0 | `False` | `local_coverage_gap` |
| 19 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 23 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 29 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 31 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 37 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 41 | 1 | 3 | 0 | `False` | `local_coverage_gap` |
| 43 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 47 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 53 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 59 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 61 | 1 | 3 | 0 | `False` | `local_coverage_gap` |
| 67 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 71 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 73 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 79 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 83 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 89 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |
| 97 | 0 | 3 | 3 | `False` | `bad_reduction_requires_separate_argument` |

Local gap summary: `local_case_elimination_candidate`. Exact next lemma: Local valuation and reduction case split for q | ABC: prove that each single-divisibility mask either cannot occur for primitive solutions at the eliminating primes, or gives a separate modular/reduction argument compatible with the trace filter. Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only, and justify the multiplicative-reduction congruence a_q(f) == +/-(q+1) mod 5 at those primes.

### Focused Frey Reduction Diagnostics

| q | mask | v_q(Delta) | v_q(c4) | v_q(c6) | reduction | standard trace |
| ---: | --- | --- | --- | --- | --- | --- |
| 3 | `A_only` | `10*v_q(A)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 3 | `B_only` | `8*v_q(B)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 3 | `C_only` | `10*v_q(C)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 13 | `A_only` | `10*v_q(A)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 13 | `B_only` | `8*v_q(B)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 13 | `C_only` | `10*v_q(C)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 17 | `A_only` | `10*v_q(A)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 17 | `B_only` | `8*v_q(B)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 17 | `C_only` | `10*v_q(C)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 41 | `A_only` | `10*v_q(A)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 41 | `B_only` | `8*v_q(B)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 41 | `C_only` | `10*v_q(C)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 61 | `A_only` | `10*v_q(A)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 61 | `B_only` | `8*v_q(B)` | `0` | `0` | `multiplicative_reduction` | `False` |
| 61 | `C_only` | `10*v_q(C)` | `0` | `0` | `multiplicative_reduction` | `False` |

### Tate Algorithm Stub

| q | mask | stub reduction | status | needs human Tate |
| ---: | --- | --- | --- | --- |
| 3 | `A_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 3 | `B_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 3 | `C_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 13 | `A_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 13 | `B_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 13 | `C_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 17 | `A_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 17 | `B_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 17 | `C_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 41 | `A_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 41 | `B_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 41 | `C_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 61 | `A_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 61 | `B_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |
| 61 | `C_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `False` |

### Single-Mask Newform Pressure

| q | mask | unit trace | coefficients | branch classification | prime label |
| ---: | --- | --- | --- | --- | --- |
| 3 | `A_only` | `all_newforms_unit_eliminated` | `newform_0:-2;newform_1:2` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 3 | `B_only` | `all_newforms_unit_eliminated` | `newform_0:-2;newform_1:2` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 3 | `C_only` | `all_newforms_unit_eliminated` | `newform_0:-2;newform_1:2` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 13 | `A_only` | `partial_unit_trace_elimination` | `newform_0:-4;newform_1:0` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 13 | `B_only` | `partial_unit_trace_elimination` | `newform_0:-4;newform_1:0` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 13 | `C_only` | `partial_unit_trace_elimination` | `newform_0:-4;newform_1:0` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 17 | `A_only` | `partial_unit_trace_elimination` | `newform_0:0;newform_1:-4` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 17 | `B_only` | `partial_unit_trace_elimination` | `newform_0:0;newform_1:-4` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 17 | `C_only` | `partial_unit_trace_elimination` | `newform_0:0;newform_1:-4` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 41 | `A_only` | `partial_unit_trace_elimination` | `newform_0:6;newform_1:-10` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 41 | `B_only` | `partial_unit_trace_elimination` | `newform_0:6;newform_1:-10` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 41 | `C_only` | `partial_unit_trace_elimination` | `newform_0:6;newform_1:-10` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 61 | `A_only` | `partial_unit_trace_elimination` | `newform_0:2;newform_1:-14` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 61 | `B_only` | `partial_unit_trace_elimination` | `newform_0:2;newform_1:-14` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| 61 | `C_only` | `partial_unit_trace_elimination` | `newform_0:2;newform_1:-14` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |

- Focused pressure labels: `local_case_elimination_candidate`.

### Multiplicative-Reduction Congruence Audit

| q | mask | newform | a_q mod 5 | allowed | classification |
| ---: | --- | ---: | --- | --- | --- |
| 3 | `A_only` | 0 | `3` | `1;4` | `multiplicative_branch_eliminated` |
| 3 | `A_only` | 1 | `2` | `1;4` | `multiplicative_branch_eliminated` |
| 3 | `B_only` | 0 | `3` | `1;4` | `multiplicative_branch_eliminated` |
| 3 | `B_only` | 1 | `2` | `1;4` | `multiplicative_branch_eliminated` |
| 3 | `C_only` | 0 | `3` | `1;4` | `multiplicative_branch_eliminated` |
| 3 | `C_only` | 1 | `2` | `1;4` | `multiplicative_branch_eliminated` |
| 13 | `A_only` | 0 | `1` | `1;4` | `multiplicative_branch_survives` |
| 13 | `A_only` | 1 | `0` | `1;4` | `multiplicative_branch_eliminated` |
| 13 | `B_only` | 0 | `1` | `1;4` | `multiplicative_branch_survives` |
| 13 | `B_only` | 1 | `0` | `1;4` | `multiplicative_branch_eliminated` |
| 13 | `C_only` | 0 | `1` | `1;4` | `multiplicative_branch_survives` |
| 13 | `C_only` | 1 | `0` | `1;4` | `multiplicative_branch_eliminated` |
| 17 | `A_only` | 0 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| 17 | `A_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| 17 | `B_only` | 0 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| 17 | `B_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| 17 | `C_only` | 0 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| 17 | `C_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| 41 | `A_only` | 0 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| 41 | `A_only` | 1 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| 41 | `B_only` | 0 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| 41 | `B_only` | 1 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| 41 | `C_only` | 0 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| 41 | `C_only` | 1 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| 61 | `A_only` | 0 | `2` | `2;3` | `multiplicative_branch_survives` |
| 61 | `A_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| 61 | `B_only` | 0 | `2` | `2;3` | `multiplicative_branch_survives` |
| 61 | `B_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| 61 | `C_only` | 0 | `2` | `2;3` | `multiplicative_branch_survives` |
| 61 | `C_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |

### Local Case Closure Score

| q | unit survivors | single survivors | fully eliminated | surviving | unresolved | label |
| ---: | ---: | ---: | --- | --- | --- | --- |
| 3 | 0 | 0 | `newform_0;newform_1` | `none` | `none` | `local_case_elimination_candidate` |
| 13 | 1 | 3 | `newform_1` | `newform_0` | `none` | `single_mask_survivor_exists` |
| 17 | 1 | 0 | `newform_0` | `newform_1` | `none` | `unit_branch_survivor_exists` |
| 41 | 1 | 0 | `newform_0` | `newform_1` | `none` | `unit_branch_survivor_exists` |
| 61 | 1 | 3 | `none` | `newform_0;newform_1` | `none` | `single_mask_survivor_exists` |

- Closure labels: `local_case_elimination_candidate;single_mask_survivor_exists;unit_branch_survivor_exists`.
- Focused pressure note: At least one focused eliminating prime has all tracked local branches closed by the audit; this is only `local_case_elimination_candidate` route evidence and keeps the review ceiling unchanged.

### Best Eliminating Prime Ranking

| rank | q | label | unit survivors | single-mask survivors | coverage gaps | q=3 penalty |
| ---: | ---: | --- | ---: | ---: | ---: | ---: |
| 1 | 3 | `local_case_elimination_candidate` | 0 | 0 | 0 | 1 |
| 2 | 17 | `unit_branch_survivor_exists` | 1 | 0 | 0 | 0 |
| 3 | 41 | `unit_branch_survivor_exists` | 1 | 0 | 0 | 0 |
| 4 | 13 | `single_mask_survivor_exists` | 1 | 3 | 0 | 0 |
| 5 | 61 | `single_mask_survivor_exists` | 1 | 3 | 0 | 0 |

- Best-prime route ceiling: `worth_human_modular_review`.

### Cross-Prime Branch Compatibility

- Non-q=3 aggregate label: `cross_prime_elimination_candidate`.

| newform | compatible assignment | eliminated at q | allowed branch sets | label |
| --- | --- | --- | --- | --- |
| `q - 2*q^3 + q^5 + O(q^6)` | `False` | `17;41` | `q=13:unit,A_only,B_only,C_only|q=17:none|q=41:none|q=61:A_only,B_only,C_only` | `cross_prime_elimination_candidate` |
| `q + 2*q^3 + q^5 + O(q^6)` | `False` | `13` | `q=13:none|q=17:unit|q=41:unit|q=61:unit` | `cross_prime_elimination_candidate` |

### q=3 Exceptionality

- q=3 good relative to level 220: `True`.
- q=3 closure label: `local_case_elimination_candidate`.
- Non-q=3 cross-prime label: `cross_prime_elimination_candidate`.
- q=3 exceptionality label: `q3_consistent_with_larger_primes`.
- Small-prime risk flags: `smallest_focused_good_prime;q3_reliance_penalty`.

### Best Route Summary

- Best route label: `cross_prime_elimination_candidate`.

| rank | route option | label | primes | q=3 penalty |
| ---: | --- | --- | --- | ---: |
| 1 | `non_q3_cross_prime_closure` | `cross_prime_elimination_candidate` | `13;17;41;61` | 0 |
| 2 | `q3_single_prime_closure` | `q3_single_prime_local_case_candidate` | `3` | 1 |
| 3 | `q17_q41_partial_closure` | `partial_closure_route` | `17;41` | 0 |
| 4 | `q13_q61_survivor_routes` | `survivor_route` | `13;61` | 0 |

### Quantifier Safety Audit

- Aggregate quantifier label: `quantifier_safe_cross_prime_candidate`.
- Safe quantifier: each level-220 newform needs one eliminating prime with complete same-prime branch coverage.
- The audit rejects fixed branch coupling across different primes.

| newform | eliminating q | complete q count | branch gaps | data gaps | fixed-branch dependency | label |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `q - 2*q^3 + q^5 + O(q^6)` | `17;41` | 2 | 2 | 0 | `False` | `valid_exists_prime_elimination` |
| `q + 2*q^3 + q^5 + O(q^6)` | `13` | 1 | 3 | 0 | `False` | `valid_exists_prime_elimination` |

### Conditional Theorem Packet

- Conditional packet label: `quantifier_safe_cross_prime_candidate`.
- The packet states the primitive-solution setup, Frey object, assumed level lowering to 220, newform exhaustion, local eliminations, and open assumptions.
- It remains route evidence only and keeps the ceiling `worth_human_modular_review`.

### Assumption Dependency Graph

- Dependency summary: `AD545-001:needs_human_derivation;AD545-002:needs_human_verification;AD545-003:conditional_route_evidence;AD545-004:missing;AD545-005:needs_human_derivation;AD545-006:computed_route_evidence;AD545-007:conditional_route_evidence;AD545-008:quantifier_safe_cross_prime_candidate`.
- Final dependency node: quantifier safety depends on local branch coverage, which depends on reduction classification and coefficient comparison.

### Adversarial Review Checklist

- Checklist sidecar asks whether level 220 is truly lowered, whether q=13/q=17/q=41 are good relative to the true conductor, whether multiplicative branches and mod-5 comparisons are justified, and whether q | ABC cases survive.

### Frey-Conductor Proof Audit

- Conditional route validity label: `conductor_gap_blocks_upgrade`.
- Frey invariant derivation: `curve_equation:verified_symbolic;c4:verified_symbolic;c6:verified_symbolic;discriminant:verified_symbolic;j_invariant:verified_symbolic`.
- Conductor support gaps: `2:needs_human_review;5:needs_human_review;11:conductor_support_gap`.
- Conductor exponent gaps: `2:needs_human_tate_check;5:needs_human_tate_check;11:needs_human_tate_check`.
- Level-220 provenance gaps: `220:level_220_heuristic_target;11:level_11_factor_unjustified`.
- ABC-prime removal gaps: `ell | A:abc_prime_removal_gap;ell | B:abc_prime_removal_gap;ell | C:abc_prime_removal_gap`.
- Bad-prime Tate gaps: `q=2:blocks_conductor_claim;q=5:blocks_conductor_claim;q=11:blocks_conductor_claim`.
- Level-lowering obligations blocking upgrade: `LL545-001:needs_human_review;LL545-002:missing;LL545-003:standard_input_needs_instantiation;LL545-004:missing;LL545-005:blocks_upgrade;LL545-006:computed_route_evidence`.
- Sage conductor sanity artifacts: `sage_conductor_sanity_545.sage:synthetic_sanity_only`.
- Level 220 remains a heuristic target while `level_11_factor_unjustified` and `abc_prime_removal_gap` remain open.
- Human theorem target: prove Frey attachment, minimal conductor, residual mod-5 irreducibility, level lowering to exactly 220, level-220 newform exhaustion, and the justified good-prime trace comparisons.

| component | current status |
| --- | --- |
| trace logic | `quantifier_safe_trace_candidate` |
| quantifier safety | `quantifier_safe_cross_prime_candidate` |
| symbolic Frey validity | `symbolic_formulas_available` |
| conductor support | `conductor_support_gap` |
| conductor exponent model | `bad_prime_tate_gap` |
| level 220 provenance | `level_220_heuristic_target` |
| ABC-prime removal | `abc_prime_removal_gap` |
| bad-prime local checks | `bad_prime_tate_gap` |
| level lowering | `level_lowering_gap` |
| irreducibility | `missing` |

### Candidate Level Discovery

- Candidate levels generated: `24`.
- Variants without factor 11: `12`; with factor 11: `12`.
- Baseline 220 included: `True`.
- Candidate-level import status counts: `completed:24`.
- Candidate-level coefficient rows imported: `430`.
- Candidate-level trace labels seen: `level_survivor_exists;level_trace_mismatch_candidate`.
- Aggregate level-route label: `level_sensitive_route`.
- Level-route reason: At least one plausible candidate level has surviving newforms or branches.

| rank | level | factorization | trace label | newforms | field status | priority |
| ---: | ---: | --- | --- | ---: | --- | ---: |
| 1 | 20 | `2^2 * 5` | `level_trace_mismatch_candidate` | 1 | `all_clear` | 15 |
| 2 | 100 | `2^2 * 5^2` | `level_trace_mismatch_candidate` | 1 | `all_clear` | 14 |
| 3 | 4 | `2^2` | `level_trace_mismatch_candidate` | 0 | `no_coefficients` | 12 |
| 4 | 10 | `2 * 5` | `level_trace_mismatch_candidate` | 0 | `no_coefficients` | 12 |
| 5 | 40 | `2^3 * 5` | `level_survivor_exists` | 1 | `all_clear` | 12 |
| 6 | 220 | `2^2 * 5 * 11` | `level_trace_mismatch_candidate` | 2 | `all_clear` | 12 |
| 7 | 2 | `2` | `level_trace_mismatch_candidate` | 0 | `no_coefficients` | 11 |
| 8 | 5 | `5` | `level_trace_mismatch_candidate` | 0 | `no_coefficients` | 11 |

The candidate-level layer is a target-discovery audit. Missing Sage data keeps the label `level_data_insufficient`; surviving newforms produce `level_sensitive_route`; multiple mismatch levels produce `multi_level_trace_pressure_candidate`.

### Focused Eliminating-Prime Nonunit Branch Audit

| q | unit eliminations | possible nonunit masks | unresolved masks | condition masks | full nonunit resolution | safe label |
| ---: | ---: | --- | --- | --- | --- | --- |
| 3 | 2 | `A_only;B_only;C_only` | `none` | `A_only;B_only;C_only` | `True` | `local_case_elimination_candidate` |
| 13 | 1 | `A_only;B_only;C_only` | `none` | `A_only;B_only;C_only` | `False` | `single_mask_survivor_exists` |
| 17 | 1 | `A_only;B_only;C_only` | `none` | `A_only;B_only;C_only` | `False` | `unit_branch_survivor_exists` |
| 41 | 1 | `A_only;B_only;C_only` | `none` | `A_only;B_only;C_only` | `False` | `unit_branch_survivor_exists` |
| 61 | 1 | `A_only;B_only;C_only` | `none` | `A_only;B_only;C_only` | `False` | `single_mask_survivor_exists` |

- Focused eliminating primes: `3;13;17;41;61`.
- Best ranked eliminating prime: `3` with label `local_case_elimination_candidate`.
- Pairwise nonunit masks are primitive-forbidden, but `A_only`, `B_only`, and `C_only` remain locally stable and need a separate Frey reduction argument.
- At least one focused eliminating prime has all tracked local branches closed by the audit; this is only `local_case_elimination_candidate` route evidence and keeps the review ceiling unchanged.

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
| `TS545-008` | `local_coverage_gap` | `high` | Prove the local valuation and reduction case split for q in {3,13,17,41,61} with q | ABC, including A_only, B_only, C_only, and singular Frey reductions. |
| `TS545-010` | `needs_human_tate_algorithm` | `high` | Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only. |
| `TS545-011` | `level_lowering_assumption_required` | `high` | Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) == +/-(q+1) mod 5 at q in {3,13,17,41,61}. |
| `TS545-012` | `computed_route_evidence` | `high` | Treat this as a screening audit only; do not use fixed branch compatibility across distinct good primes as the final modular-method quantifier. |
| `TS545-013` | `q3_requires_human_review` | `high` | Compare q=3 behavior with q=13,17,41,61 and justify any use of q=3 as local route evidence. |
| `TS545-014` | `quantifier_safe_cross_prime_candidate` | `high` | Verify the exists-prime-per-newform elimination and reject any argument that couples fixed branch choices across different primes. |
| `TS545-015` | `conductor_gap_blocks_upgrade` | `high` | Prove the conductor support at 2, 5, 11, and primes dividing ABC; decide which primes remain in level 220. |
| `TS545-016` | `blocks_conductor_claim` | `high` | Compute reduction types and conductor exponents at 2, 5, and 11. |
| `TS545-017` | `level_lowering_gap_blocks_upgrade` | `high` | Discharge every level-lowering obligation before interpreting the trace elimination as a modular-method argument. |
| `TS545-018` | `bad_prime_tate_gap` | `high` | Derive the exact local conductor exponent at 2, at 5, and at any 11-adic case used by the route. |
| `TS545-019` | `conductor_gap_blocks_upgrade` | `high` | Justify the factors 2, 5, and 11, or replace the target level and rerun the newform comparison. |
| `TS545-020` | `abc_prime_removal_gap` | `high` | Verify residual irreducibility, minimality, and the local hypotheses needed to remove every prime dividing ABC. |
| `TS545-021` | `synthetic_sanity_only` | `medium` | Do not use synthetic samples as mathematical evidence; use them only to spot formula or conductor-computation mistakes. |
| `TS545-022` | `level_data_insufficient` | `high` | Run the candidate-level Sage expander, import coefficient data, and compare whether trace pressure persists without the unjustified factor 11. |
| `TS545-009` | `computed_route_evidence` | `medium` | Decide whether reliance on q=3 or another focused eliminating prime should be part of the human check. |

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
| `frey_curve_derivation_gap` | `open` | `high` | Derive the Frey curve from a primitive solution and prove the symbolic invariant formulas in the required integral model. |
| `conductor_support_audit_gap` | `open` | `high` | Prove which primes remain in the conductor or lowered level, including why 11 belongs to level 220 if it does. |
| `bad_prime_tate_gap` | `open` | `high` | Run the Tate algorithm at bad primes 2, 5, and 11 and compute the exact conductor exponents. |
| `conductor_exponent_model_gap` | `open` | `high` | Convert the symbolic valuation model into a local minimal-model and conductor-exponent calculation at every relevant prime. |
| `level_220_provenance_gap` | `open` | `high` | Explain the factors 2, 5, and 11 in the lowered level; in particular resolve level_11_factor_unjustified. |
| `abc_prime_removal_gap` | `open` | `high` | Prove residual irreducibility, minimality, and level-lowering hypotheses that remove every prime dividing ABC. |
| `candidate_level_search_gap` | `open` | `high` | Run the candidate-level Sage expander, import newform coefficients across generated levels, and decide whether the route is level-sensitive. |
| `irreducibility_gap` | `open` | `high` | Prove irreducibility for the justified residual representation prime. |
| `level_lowering_gap` | `open` | `high` | Verify the hypotheses for lowering from the true conductor to the claimed comparison level. |
| `formal_level_lowering_obligation_gap` | `open` | `high` | Verify residual modulus 5, residual irreducibility, modularity input, all level-lowering hypotheses, exact level 220, and good-prime trace comparison validity. |
| `newform_trace_gap` | `open` | `high` | Export and compare relevant newform coefficients at good primes using the justified modulus. |
| `local_to_global_gap` | `open` | `high` | Show how local survivor traces constrain the global modular representation, or replace with good-prime trace comparisons. |
| `local_valuation_reduction_gap` | `open` | `high` | Prove the local valuation and reduction case split for q | ABC at q in {3,13,17,41,61}, including A_only, B_only, C_only, and singular Frey reductions. |
| `focused_tate_algorithm_gap` | `open` | `high` | Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only. |
| `multiplicative_congruence_gap` | `open` | `high` | Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) == +/-(q+1) mod 5 at q in {3,13,17,41,61}. |
| `cross_prime_branch_compatibility_gap` | `open` | `high` | Review the cross-prime branch compatibility audit for q in {13,17,41,61} only as a screening layer. |
| `quantifier_safety_gap` | `open` | `high` | Verify the quantifier-safe cross-prime route: newform 0 at q=17 or q=41 and newform 1 at q=13, with complete same-prime branch coverage. |
| `q3_exceptionality_gap` | `open` | `high` | Review whether q=3 behavior is small-prime-sensitive or supported by the larger focused primes q=13,17,41,61. |
| `control_artifact_gap` | `open` | `medium` | Separate artifact local behavior from reusable modular constraints and connect any non-artifact rows to the Frey route. |

## Exact Next Theorem Or Lemma

A human should next prove the Frey-curve attachment and conductor/level-lowering package for `A^5 + B^4 = C^5`: every primitive solution gives the stated Frey object; the residual representation at the justified modulus is irreducible; the true conductor lowers to the claimed comparison level; the multiplicative branches satisfy `a_q(f) == +/-(q+1) mod 5` at q in `{3,13,17,41,61}` where used; the quantifier-safe cross-prime route uses an exists-prime-per-newform elimination; and the two level-220 newforms, with actual q-expansion coefficients at good primes, fail or pass the justified trace congruence test.

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
- `runs/sage_followup_ci/nonunit_eliminations_545.csv`
- `runs/sage_followup_ci/singular_reduction_traces_545.csv`
- `runs/sage_followup_ci/frey_reduction_diagnostics_545.csv`
- `runs/sage_followup_ci/tate_algorithm_stub_545.csv`
- `runs/sage_followup_ci/single_mask_newform_pressure_545.csv`
- `runs/sage_followup_ci/multiplicative_reduction_congruence_545.csv`
- `runs/sage_followup_ci/local_case_closure_score_545.csv`
- `runs/sage_followup_ci/best_eliminating_prime_545.csv`
- `runs/sage_followup_ci/BEST_ELIMINATING_PRIME_545.md`
- `runs/sage_followup_ci/cross_prime_branch_compatibility_545.csv`
- `runs/sage_followup_ci/Q3_EXCEPTIONALITY_AUDIT_545.md`
- `runs/sage_followup_ci/BEST_ROUTE_SUMMARY_545.md`
- `runs/sage_followup_ci/quantifier_safety_audit_545.csv`
- `runs/sage_followup_ci/QUANTIFIER_SAFETY_AUDIT_545.md`
- `runs/sage_followup_ci/CONDITIONAL_THEOREM_PACKET_545.md`
- `runs/sage_followup_ci/assumption_dependency_graph_545.csv`
- `runs/sage_followup_ci/ASSUMPTION_DEPENDENCY_GRAPH_545.md`
- `runs/sage_followup_ci/ADVERSARIAL_REVIEW_CHECKLIST_545.md`
- `runs/sage_followup_ci/frey_curve_derivation_545.csv`
- `runs/sage_followup_ci/FREY_CURVE_DERIVATION_545.md`
- `runs/sage_followup_ci/conductor_support_audit_545.csv`
- `runs/sage_followup_ci/CONDUCTOR_SUPPORT_AUDIT_545.md`
- `runs/sage_followup_ci/conductor_exponent_model_545.csv`
- `runs/sage_followup_ci/CONDUCTOR_EXPONENT_MODEL_545.md`
- `runs/sage_followup_ci/level_220_provenance_545.csv`
- `runs/sage_followup_ci/LEVEL_220_PROVENANCE_545.md`
- `runs/sage_followup_ci/abc_prime_removal_audit_545.csv`
- `runs/sage_followup_ci/ABC_PRIME_REMOVAL_AUDIT_545.md`
- `runs/sage_followup_ci/sage_conductor_sanity_545.sage`
- `runs/sage_followup_ci/sage_conductor_sanity_manifest_545.csv`
- `runs/sage_followup_ci/candidate_levels_545.csv`
- `runs/sage_followup_ci/CANDIDATE_LEVELS_545.md`
- `runs/sage_followup_ci/sage_candidate_level_expander_545.sage`
- `runs/sage_followup_ci/candidate_level_newforms_545.json`
- `runs/sage_followup_ci/candidate_level_import_summary_545.csv`
- `runs/sage_followup_ci/candidate_level_coefficient_rows_545.csv`
- `runs/sage_followup_ci/trace_filter_across_levels_545.csv`
- `runs/sage_followup_ci/level_route_ranking_545.csv`
- `runs/sage_followup_ci/LEVEL_ROUTE_RANKING_545.md`
- `runs/sage_followup_ci/bad_prime_tate_checklist_545.csv`
- `runs/sage_followup_ci/BAD_PRIME_TATE_CHECKLIST_545.md`
- `runs/sage_followup_ci/level_lowering_obligations_545.csv`
- `runs/sage_followup_ci/LEVEL_LOWERING_OBLIGATIONS_545.md`
- `runs/sage_followup_ci/conditional_route_validity_score_545.csv`
- `runs/sage_followup_ci/CONDITIONAL_ROUTE_VALIDITY_SCORE_545.md`
- `runs/sage_followup_ci/nonunit_newform_filter_545.csv`
- `runs/sage_followup_ci/LOCAL_CASE_DECISION_TREE_545.md`
- `runs/sage_followup_ci/assumption_register_545.csv`
- `runs/sage_followup_ci/proof_gap_summary.csv`
- `runs/sage_followup_ci/proof_gap_report.md`
