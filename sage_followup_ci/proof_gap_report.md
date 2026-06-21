# Focused 5-4-5 Gap Report

Output directory: `runs/sage_followup_ci`

The focused audit keeps `(5,4,5)` at `worth_human_modular_review`; it does not move beyond review status.

| category | status | risk | next lemma |
| --- | --- | --- | --- |
| `algebraic_derivation_gap` | `open` | `high` | Prove the Frey-curve attachment lemma for A^5+B^4=C^5, including primitivity and nonsingularity conditions. |
| `conductor_gap` | `open` | `high` | Compute the exact conductor of the attached Frey curve and justify every prime/exponent in the level. |
| `irreducibility_gap` | `open` | `high` | Prove irreducibility for the justified residual representation prime. |
| `level_lowering_gap` | `open` | `high` | Verify the hypotheses for lowering from the true conductor to the claimed comparison level. |
| `newform_trace_gap` | `open` | `high` | Export and compare relevant newform coefficients at good primes using the justified modulus. |
| `local_to_global_gap` | `open` | `high` | Show how local survivor traces constrain the global modular representation, or replace with good-prime trace comparisons. |
| `local_valuation_reduction_gap` | `open` | `high` | Prove the local valuation and reduction case split for q | ABC at q=13 or q=17, including A_only, B_only, C_only, and singular Frey reductions. |
| `control_artifact_gap` | `open` | `medium` | Separate artifact local behavior from reusable modular constraints and connect any non-artifact rows to the Frey route. |

## Exact Next Lemma

To advance `(5,4,5)`, a human should first prove the Frey-curve attachment and conductor/level-lowering lemmas: every primitive solution must yield the stated Frey object, its residual representation must be irreducible, and its true conductor must lower to the claimed comparison level. The same package must include the q=13/q=17 local valuation and reduction case split for q | ABC before the two level-220 newforms are tested with q-expansion trace congruences at good primes.
