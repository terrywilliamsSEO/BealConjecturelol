# Local Case Decision Tree For `(5,4,5)` At Eliminating Good Primes

This decision tree narrows the local coverage gap for `A^5 + B^4 = C^5`. It is a route audit only: unit trace eliminations do not become global eliminations until every nonunit branch has a justified local reduction argument.

## q=3

### Unit Case

| newform | classification | mode | reason |
| ---: | --- | --- | --- |
| 0 | `eliminated` | `mod_5` | No Frey trace matches under the selected comparison mode. |
| 1 | `eliminated` | `mod_5` | No Frey trace matches under the selected comparison mode. |

### Nonunit Branches

| mask | mod q | mod q^2 | mod q^3 | primitive | reduction route | branch status |
| --- | --- | --- | --- | --- | --- | --- |
| `AB` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `ABC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `AC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `A_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |
| `BC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `B_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |
| `C_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |

### Single-Mask Frey Reduction Pressure

| mask | reduction type | Tate stub | branch classification | prime label |
| --- | --- | --- | --- | --- |
| `A_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| `B_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| `C_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |

### Multiplicative-Reduction Congruence

| mask | newform | a_q mod 5 | allowed | classification |
| --- | ---: | --- | --- | --- |
| `A_only` | 0 | `3` | `1;4` | `multiplicative_branch_eliminated` |
| `A_only` | 1 | `2` | `1;4` | `multiplicative_branch_eliminated` |
| `B_only` | 0 | `3` | `1;4` | `multiplicative_branch_eliminated` |
| `B_only` | 1 | `2` | `1;4` | `multiplicative_branch_eliminated` |
| `C_only` | 0 | `3` | `1;4` | `multiplicative_branch_eliminated` |
| `C_only` | 1 | `2` | `1;4` | `multiplicative_branch_eliminated` |

### Focused Decision

- Safe label: `local_case_elimination_candidate`.
- Full nonunit resolution: `True`.
- Reduction argument masks: `none`.
- Single-mask condition masks: `A_only;B_only;C_only`.
- Closure label: `local_case_elimination_candidate`.
- Closure summary: `fully_eliminated=newform_0;newform_1; surviving=none; unresolved=none`.
- Reason: Unit, primitive-forbidden, and single-mask multiplicative congruence checks eliminate all tracked newform branches for this q.

## q=13

### Unit Case

| newform | classification | mode | reason |
| ---: | --- | --- | --- |
| 0 | `survives` | `mod_5` | A Frey trace is congruent to the coefficient modulo 5. |
| 1 | `eliminated` | `mod_5` | No Frey trace matches under the selected comparison mode. |

### Nonunit Branches

| mask | mod q | mod q^2 | mod q^3 | primitive | reduction route | branch status |
| --- | --- | --- | --- | --- | --- | --- |
| `AB` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `ABC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `AC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `A_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |
| `BC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `B_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |
| `C_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |

### Single-Mask Frey Reduction Pressure

| mask | reduction type | Tate stub | branch classification | prime label |
| --- | --- | --- | --- | --- |
| `A_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| `B_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| `C_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |

### Multiplicative-Reduction Congruence

| mask | newform | a_q mod 5 | allowed | classification |
| --- | ---: | --- | --- | --- |
| `A_only` | 0 | `1` | `1;4` | `multiplicative_branch_survives` |
| `A_only` | 1 | `0` | `1;4` | `multiplicative_branch_eliminated` |
| `B_only` | 0 | `1` | `1;4` | `multiplicative_branch_survives` |
| `B_only` | 1 | `0` | `1;4` | `multiplicative_branch_eliminated` |
| `C_only` | 0 | `1` | `1;4` | `multiplicative_branch_survives` |
| `C_only` | 1 | `0` | `1;4` | `multiplicative_branch_eliminated` |

### Focused Decision

- Safe label: `single_mask_survivor_exists`.
- Full nonunit resolution: `False`.
- Reduction argument masks: `none`.
- Single-mask condition masks: `A_only;B_only;C_only`.
- Closure label: `single_mask_survivor_exists`.
- Closure summary: `fully_eliminated=newform_1; surviving=newform_0; unresolved=none`.
- Reason: At least one single-mask multiplicative branch has an allowed newform congruence.

## q=17

### Unit Case

| newform | classification | mode | reason |
| ---: | --- | --- | --- |
| 0 | `eliminated` | `mod_5` | No Frey trace matches under the selected comparison mode. |
| 1 | `survives` | `mod_5` | A Frey trace is congruent to the coefficient modulo 5. |

### Nonunit Branches

| mask | mod q | mod q^2 | mod q^3 | primitive | reduction route | branch status |
| --- | --- | --- | --- | --- | --- | --- |
| `AB` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `ABC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `AC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `A_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |
| `BC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `B_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |
| `C_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |

### Single-Mask Frey Reduction Pressure

| mask | reduction type | Tate stub | branch classification | prime label |
| --- | --- | --- | --- | --- |
| `A_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| `B_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| `C_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |

### Multiplicative-Reduction Congruence

| mask | newform | a_q mod 5 | allowed | classification |
| --- | ---: | --- | --- | --- |
| `A_only` | 0 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| `A_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| `B_only` | 0 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| `B_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| `C_only` | 0 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| `C_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |

### Focused Decision

- Safe label: `unit_branch_survivor_exists`.
- Full nonunit resolution: `False`.
- Reduction argument masks: `none`.
- Single-mask condition masks: `A_only;B_only;C_only`.
- Closure label: `unit_branch_survivor_exists`.
- Closure summary: `fully_eliminated=newform_0; surviving=newform_1; unresolved=none`.
- Reason: At least one unit trace branch survives for this q.

## q=41

### Unit Case

| newform | classification | mode | reason |
| ---: | --- | --- | --- |
| 0 | `eliminated` | `mod_5` | No Frey trace matches under the selected comparison mode. |
| 1 | `survives` | `mod_5` | A Frey trace is congruent to the coefficient modulo 5. |

### Nonunit Branches

| mask | mod q | mod q^2 | mod q^3 | primitive | reduction route | branch status |
| --- | --- | --- | --- | --- | --- | --- |
| `AB` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `ABC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `AC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `A_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |
| `BC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `B_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |
| `C_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |

### Single-Mask Frey Reduction Pressure

| mask | reduction type | Tate stub | branch classification | prime label |
| --- | --- | --- | --- | --- |
| `A_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| `B_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| `C_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |

### Multiplicative-Reduction Congruence

| mask | newform | a_q mod 5 | allowed | classification |
| --- | ---: | --- | --- | --- |
| `A_only` | 0 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| `A_only` | 1 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| `B_only` | 0 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| `B_only` | 1 | `0` | `2;3` | `multiplicative_branch_eliminated` |
| `C_only` | 0 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| `C_only` | 1 | `0` | `2;3` | `multiplicative_branch_eliminated` |

### Focused Decision

- Safe label: `unit_branch_survivor_exists`.
- Full nonunit resolution: `False`.
- Reduction argument masks: `none`.
- Single-mask condition masks: `A_only;B_only;C_only`.
- Closure label: `unit_branch_survivor_exists`.
- Closure summary: `fully_eliminated=newform_0; surviving=newform_1; unresolved=none`.
- Reason: At least one unit trace branch survives for this q.

## q=61

### Unit Case

| newform | classification | mode | reason |
| ---: | --- | --- | --- |
| 0 | `eliminated` | `mod_5` | No Frey trace matches under the selected comparison mode. |
| 1 | `survives` | `mod_5` | A Frey trace is congruent to the coefficient modulo 5. |

### Nonunit Branches

| mask | mod q | mod q^2 | mod q^3 | primitive | reduction route | branch status |
| --- | --- | --- | --- | --- | --- | --- |
| `AB` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `ABC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `AC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `A_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |
| `BC` | `False` | `False` | `False` | `False` | `template_unknown` | `primitive_forbidden` |
| `B_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |
| `C_only` | `True` | `True` | `True` | `True` | `needs_human_reduction_argument` | `unresolved` |

### Single-Mask Frey Reduction Pressure

| mask | reduction type | Tate stub | branch classification | prime label |
| --- | --- | --- | --- | --- |
| `A_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| `B_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |
| `C_only` | `multiplicative_reduction` | `valuation_stub_multiplicative` | `multiplicative_reduction_condition` | `local_case_elimination_candidate` |

### Multiplicative-Reduction Congruence

| mask | newform | a_q mod 5 | allowed | classification |
| --- | ---: | --- | --- | --- |
| `A_only` | 0 | `2` | `2;3` | `multiplicative_branch_survives` |
| `A_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| `B_only` | 0 | `2` | `2;3` | `multiplicative_branch_survives` |
| `B_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |
| `C_only` | 0 | `2` | `2;3` | `multiplicative_branch_survives` |
| `C_only` | 1 | `1` | `2;3` | `multiplicative_branch_eliminated` |

### Focused Decision

- Safe label: `single_mask_survivor_exists`.
- Full nonunit resolution: `False`.
- Reduction argument masks: `none`.
- Single-mask condition masks: `A_only;B_only;C_only`.
- Closure label: `single_mask_survivor_exists`.
- Closure summary: `fully_eliminated=none; surviving=newform_0;newform_1; unresolved=none`.
- Reason: At least one single-mask multiplicative branch has an allowed newform congruence.

## Current Conclusion

At least one focused branch survives or still needs a level-lowering/Tate justification, so the current label remains `local_coverage_gap` with `unit_only_trace_mismatch_candidate` scope.
