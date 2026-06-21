# Local Case Decision Tree For `(5,4,5)` At q=13 And q=17

This decision tree narrows the local coverage gap for `A^5 + B^4 = C^5`. It is a route audit only: unit trace eliminations do not become global eliminations until every nonunit branch has a justified local reduction argument.

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

### Focused Decision

- Safe label: `reduction_argument_required`.
- Full nonunit resolution: `False`.
- Reduction argument masks: `A_only;B_only;C_only`.
- Reason: At least one single-divisibility branch needs a separate Frey reduction argument.

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

### Focused Decision

- Safe label: `reduction_argument_required`.
- Full nonunit resolution: `False`.
- Reduction argument masks: `A_only;B_only;C_only`.
- Reason: At least one single-divisibility branch needs a separate Frey reduction argument.

## Current Conclusion

For q=13 and q=17, pairwise masks are primitive-forbidden, but the single-divisibility branches `A_only`, `B_only`, and `C_only` remain locally stable and require a separate Frey reduction argument. The current label therefore remains `local_coverage_gap`, with scope `unit_only_trace_mismatch_candidate`.
