# Frey Invariant Sanity For `(5,4,5)`

These rows are symbolic sanity checks for the current Frey template. They are not a conductor proof.

| component | expression | inferred support | status | required assumption |
| --- | --- | --- | --- | --- |
| `curve_equation` | `E: y^2 = x(x - A^5)(x + B^4)` | `A,B` | `template_candidate` | Prove every primitive solution produces this curve in the required orientation. |
| `discriminant_like` | `Delta = 16 * (A^5)^2 * (B^4)^2 * (A^5 + B^4)^2 = 16*A^10*B^8*C^10` | `2,A,B,C` | `verified_by_symbolic_formula` | Check minimal discriminant valuations at 2, 5, and all primes dividing ABC. |
| `j_invariant_like` | `j = 256*(A^10 + A^5*B^4 + B^8)^3/(A^10*B^8*C^10)` | `2,A,B,C,A^10 + A^5*B^4 + B^8` | `symbolic_placeholder` | Derive c4 and j for the exact integral model and verify cancellations. |
| `candidate_bad_prime_support` | `{2} union primes(A*B*C)` | `2,A,B,C` | `needs_human_math_review` | Prove which primes are genuinely bad after minimization. |
| `level_220_support` | `220 = 2^2 * 5 * 11` | `2,5,11` | `heuristic_route_target` | Justify whether 11 belongs to the true conductor, lowered level, or only the search route. |
| `level_lowering_disappearing_primes` | `primes dividing ABC should disappear from the lowered level under a valid modular method package` | `ABC` | `missing` | Prove irreducibility, semistability/ramification hypotheses, and the exact lowering statement. |

The key hand task is to turn the discriminant-like support calculation into a minimal conductor and level-lowering statement.
