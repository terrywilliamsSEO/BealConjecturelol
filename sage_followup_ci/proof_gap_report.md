# Focused 5-4-5 Gap Report

Output directory: `runs/sage_followup_ci`

The focused audit keeps `(5,4,5)` at `worth_human_modular_review`; it does not move beyond review status.

| category | status | risk | next lemma |
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

## Exact Next Lemma

To advance `(5,4,5)`, a human should first prove the Frey-curve attachment and conductor/level-lowering lemmas: every primitive solution must yield the stated Frey object, its residual representation must be irreducible, and its true conductor must lower to the claimed comparison level. The same package must include the q in {3,13,17,41,61} local valuation and reduction case split for q | ABC, plus the focused Tate algorithm under A_only, B_only, and C_only, run the bad-prime Tate algorithm at 2, 5, and 11, justify the multiplicative congruence a_q(f) == +/-(q+1) mod 5, and verify the exists-prime-per-newform quantifier before the two level-220 newforms are tested with q-expansion trace congruences at good primes. The conductor-exponent model, level-220 provenance audit, candidate-level search, ABC-prime removal audit, conductor-support, level-lowering, cross-prime compatibility, quantifier-safety, and q=3 exceptionality audits must also be reviewed.
