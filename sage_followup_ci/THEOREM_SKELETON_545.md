# Conditional Modular Route For Primitive Solutions Of `A^5 + B^4 = C^5`

This is a theorem skeleton, not a completed argument. It lists the exact hand-written lemmas needed before the computational trace mismatch can carry mathematical force.

## Statement Of Hypothetical Primitive Solution

Assume nonzero integers `A,B,C` satisfy `A^5 + B^4 = C^5` and `gcd(A,B,C)=1`, with all normalization and sign conventions stated explicitly.

## Proposed Frey Object

`E: y^2 = x(x - A^5)(x + B^4)`.

## Required Lemma 1: Frey attachment

Attach E: y^2 = x(x - A^5)(x + B^4) to every primitive solution in the required orientation.

- Current evidence: Template exists in the route library.
- Status: `needs_hand_derivation`.
- Next action: Derive nonsingularity and integral model conditions for all primitive solution cases.

## Required Lemma 2: Discriminant and conductor calculation

Compute the minimal discriminant and conductor exponents, including primes 2, 5, 11, and primes dividing ABC.

- Current evidence: Symbolic invariants are computed for the displayed model: Delta=16*A^10*B^8*C^10, c4=16*(A^10+A^5*B^4+B^8), and c6=32*(A^5-B^4)*(2*A^10+5*A^5*B^4+2*B^8).
- Status: `needs_hand_derivation`.
- Next action: Run a prime-by-prime minimal model and conductor analysis.

## Required Lemma 3: Residual mod-5 irreducibility

Show the relevant residual representation modulo 5 is irreducible and has the required ramification behavior.

- Current evidence: The current trace filter uses mod-5 comparison mode.
- Status: `missing`.
- Next action: Identify the exact representation and prove irreducibility or state required exceptions.

## Required Lemma 4: Level lowering to level 220

Show the modular representation lowers to the weight-2 level-220 space used by the Sage query.

- Current evidence: 110:level_data_insufficient;220:level_220_mismatch_candidate;440:level_data_insufficient
- Status: `needs_hand_derivation`.
- Next action: Justify why the comparison level is 220 and why no nearby level should be used instead.

## Required Lemma 5: Level-220 newform exhaustion

Verify that the two imported level-220 newform slots are the complete relevant target space.

- Current evidence: Current trace progress label is trace_mismatch_candidate.
- Status: `computed_route_evidence`.
- Next action: Confirm old/new decomposition, character choices, coefficient fields, and labels in Sage or Magma.

## Required Lemma 6: Good-prime trace exclusion

For each relevant good prime, compare Frey trace possibilities with newform coefficients in the justified residue field.

- Current evidence: 2 of 2 level-220 newforms eliminated by current filter.
- Status: `computed_route_evidence`.
- Next action: Check the first eliminating primes independently and justify the local enumeration.

## Required Lemma 7: Local valuation and reduction case split for q | ABC

Handle reductions where q divides one or more of A,B,C, or prove they are not needed for the chosen good-prime trace step.

- Current evidence: local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3
- Status: `local_coverage_gap`.
- Next action: Prove the local valuation and reduction case split for q in {3,13,17,41,61} with q | ABC, including A_only, B_only, C_only, and singular Frey reductions.

## Required Lemma 8: Focused Tate algorithm for single masks

Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only.

- Current evidence: local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3
- Status: `needs_human_tate_algorithm`.
- Next action: Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only.

## Required Lemma 9: Multiplicative-reduction congruence

Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) == +/-(q+1) mod 5 at q in {3,13,17,41,61}.

- Current evidence: local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3
- Status: `level_lowering_assumption_required`.
- Next action: Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) == +/-(q+1) mod 5 at q in {3,13,17,41,61}.

## Required Lemma 10: Cross-prime branch compatibility

Check whether q in {13,17,41,61} jointly eliminate all compatible unit and single-mask branch assignments for the level-220 newforms.

- Current evidence: local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3
- Status: `computed_route_evidence`.
- Next action: Treat this as a screening audit only; do not use fixed branch compatibility across distinct good primes as the final modular-method quantifier.

## Required Lemma 11: q=3 exceptionality review

Decide whether the q=3 local closure is small-prime-sensitive or supported by the non-q=3 focused primes.

- Current evidence: local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3
- Status: `q3_requires_human_review`.
- Next action: Compare q=3 behavior with q=13,17,41,61 and justify any use of q=3 as local route evidence.

## Required Lemma 12: Quantifier-safe cross-prime route

For each level-220 newform, identify at least one non-q=3 prime where unit, A_only, B_only, C_only, and pairwise primitive-forbidden masks are all covered.

- Current evidence: local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3
- Status: `quantifier_safe_cross_prime_candidate`.
- Next action: Verify the exists-prime-per-newform elimination and reject any argument that couples fixed branch choices across different primes.

## Required Lemma 13: Frey-conductor proof audit

Turn the symbolic Frey invariant formulas into a minimal conductor and exact bad-prime support statement.

- Current evidence: The Frey-conductor audit computes symbolic c4, c6, Delta, and j, but conductor exponents remain unproved.
- Status: `conductor_gap_blocks_upgrade`.
- Next action: Prove the conductor support at 2, 5, 11, and primes dividing ABC; decide which primes remain in level 220.

## Required Lemma 14: Bad-prime Tate algorithm

Run the local Tate/minimal-model analysis at the bad primes 2, 5, and 11.

- Current evidence: The checklist records symbolic valuation formulas but no completed local Tate analysis.
- Status: `blocks_conductor_claim`.
- Next action: Compute reduction types and conductor exponents at 2, 5, and 11.

## Required Lemma 15: Formal level-lowering package

Verify residual modulus 5, residual irreducibility, modularity input, level-lowering hypotheses, exact target level 220, and good-prime trace validity.

- Current evidence: The obligation list is generated, with irreducibility and exact level still missing.
- Status: `level_lowering_gap_blocks_upgrade`.
- Next action: Discharge every level-lowering obligation before interpreting the trace elimination as a modular-method argument.

## Required Lemma 16: Conductor-exponent model provenance

Separate generic multiplicative ABC-prime behavior from bad-prime exponent calculations at 2, 5, and 11.

- Current evidence: The conductor-exponent model records generic multiplicative rows away from 2,5,11 but leaves bad-prime exponents as human Tate checks.
- Status: `bad_prime_tate_gap`.
- Next action: Derive the exact local conductor exponent at 2, at 5, and at any 11-adic case used by the route.

## Required Lemma 17: Level-220 provenance

Explain each factor in 220 = 2^2 * 5 * 11 from the Frey conductor or lowered level.

- Current evidence: The level-220 provenance audit labels the aggregate target as level_220_heuristic_target and the factor 11 as level_11_factor_unjustified.
- Status: `conductor_gap_blocks_upgrade`.
- Next action: Justify the factors 2, 5, and 11, or replace the target level and rerun the newform comparison.

## Required Lemma 18: ABC-prime removal

Show why primes dividing A, B, or C disappear from the final comparison level after level lowering.

- Current evidence: The ABC-prime removal audit marks A, B, and C prime cases with abc_prime_removal_gap.
- Status: `abc_prime_removal_gap`.
- Next action: Verify residual irreducibility, minimality, and the local hypotheses needed to remove every prime dividing ABC.

## Required Lemma 19: Sage conductor sanity samples

Use generated Sage code only to sanity-check formulas and optional exact samples supplied later.

- Current evidence: The generated Sage script contains symbolic formulas and finite-field residue samples only.
- Status: `synthetic_sanity_only`.
- Next action: Do not use synthetic samples as mathematical evidence; use them only to spot formula or conductor-computation mistakes.

## Required Lemma 20: Candidate-level target discovery

Stop assuming level 220 and test plausible comparison levels generated from bad-prime exponent variants.

- Current evidence: The candidate-level layer generates 2^0..3 * 5^0..2 * 11^0..1, writes a Sage expander, and ranks levels by trace pressure and conductor plausibility.
- Status: `level_data_insufficient`.
- Next action: Run the candidate-level Sage expander, import coefficient data, and compare whether trace pressure persists without the unjustified factor 11.

## Required Lemma 21: Small-prime robustness

Show the route does not rely on an accidental tiny-prime phenomenon unless that reliance is mathematically justified.

- Current evidence: exclude_q_3:trace_mismatch_candidate;exclude_q_3_7:trace_mismatch_candidate;exclude_q_lt_11:trace_mismatch_candidate;exclude_q_lt_17:trace_survivor_exists;use_only_q_ge_17:trace_survivor_exists
- Status: `computed_route_evidence`.
- Next action: Decide whether reliance on q=3 or another focused eliminating prime should be part of the human check.

## Current Computational Evidence

| obligation | status | evidence | next action |
| --- | --- | --- | --- |
| `TS545-001` | `conditional_setup` | Framework assumption only. | State sign, nonzero, coprimality, and normalization conventions exactly. |
| `TS545-002` | `needs_hand_derivation` | Template exists in the route library. | Derive nonsingularity and integral model conditions for all primitive solution cases. |
| `TS545-003` | `needs_hand_derivation` | Symbolic invariants are computed for the displayed model: Delta=16*A^10*B^8*C^10, c4=16*(A^10+A^5*B^4+B^8), and c6=32*(A^5-B^4)*(2*A^10+5*A^5*B^4+2*B^8). | Run a prime-by-prime minimal model and conductor analysis. |
| `TS545-004` | `missing` | The current trace filter uses mod-5 comparison mode. | Identify the exact representation and prove irreducibility or state required exceptions. |
| `TS545-005` | `needs_hand_derivation` | 110:level_data_insufficient;220:level_220_mismatch_candidate;440:level_data_insufficient | Justify why the comparison level is 220 and why no nearby level should be used instead. |
| `TS545-006` | `computed_route_evidence` | Current trace progress label is trace_mismatch_candidate. | Confirm old/new decomposition, character choices, coefficient fields, and labels in Sage or Magma. |
| `TS545-007` | `computed_route_evidence` | 2 of 2 level-220 newforms eliminated by current filter. | Check the first eliminating primes independently and justify the local enumeration. |
| `TS545-008` | `local_coverage_gap` | local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3 | Prove the local valuation and reduction case split for q in {3,13,17,41,61} with q | ABC, including A_only, B_only, C_only, and singular Frey reductions. |
| `TS545-010` | `needs_human_tate_algorithm` | local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3 | Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only. |
| `TS545-011` | `level_lowering_assumption_required` | local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3 | Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) == +/-(q+1) mod 5 at q in {3,13,17,41,61}. |
| `TS545-012` | `computed_route_evidence` | local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3 | Treat this as a screening audit only; do not use fixed branch compatibility across distinct good primes as the final modular-method quantifier. |
| `TS545-013` | `q3_requires_human_review` | local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3 | Compare q=3 behavior with q=13,17,41,61 and justify any use of q=3 as local route evidence. |
| `TS545-014` | `quantifier_safe_cross_prime_candidate` | local_case_elimination_candidate; scope=local_trace_mismatch_candidate; full_coverage_eliminating_primes=3 | Verify the exists-prime-per-newform elimination and reject any argument that couples fixed branch choices across different primes. |
| `TS545-015` | `conductor_gap_blocks_upgrade` | The Frey-conductor audit computes symbolic c4, c6, Delta, and j, but conductor exponents remain unproved. | Prove the conductor support at 2, 5, 11, and primes dividing ABC; decide which primes remain in level 220. |
| `TS545-016` | `blocks_conductor_claim` | The checklist records symbolic valuation formulas but no completed local Tate analysis. | Compute reduction types and conductor exponents at 2, 5, and 11. |
| `TS545-017` | `level_lowering_gap_blocks_upgrade` | The obligation list is generated, with irreducibility and exact level still missing. | Discharge every level-lowering obligation before interpreting the trace elimination as a modular-method argument. |
| `TS545-018` | `bad_prime_tate_gap` | The conductor-exponent model records generic multiplicative rows away from 2,5,11 but leaves bad-prime exponents as human Tate checks. | Derive the exact local conductor exponent at 2, at 5, and at any 11-adic case used by the route. |
| `TS545-019` | `conductor_gap_blocks_upgrade` | The level-220 provenance audit labels the aggregate target as level_220_heuristic_target and the factor 11 as level_11_factor_unjustified. | Justify the factors 2, 5, and 11, or replace the target level and rerun the newform comparison. |
| `TS545-020` | `abc_prime_removal_gap` | The ABC-prime removal audit marks A, B, and C prime cases with abc_prime_removal_gap. | Verify residual irreducibility, minimality, and the local hypotheses needed to remove every prime dividing ABC. |
| `TS545-021` | `synthetic_sanity_only` | The generated Sage script contains symbolic formulas and finite-field residue samples only. | Do not use synthetic samples as mathematical evidence; use them only to spot formula or conductor-computation mistakes. |
| `TS545-022` | `level_data_insufficient` | The candidate-level layer generates 2^0..3 * 5^0..2 * 11^0..1, writes a Sage expander, and ranks levels by trace pressure and conductor plausibility. | Run the candidate-level Sage expander, import coefficient data, and compare whether trace pressure persists without the unjustified factor 11. |
| `TS545-009` | `computed_route_evidence` | exclude_q_3:trace_mismatch_candidate;exclude_q_3_7:trace_mismatch_candidate;exclude_q_lt_11:trace_mismatch_candidate;exclude_q_lt_17:trace_survivor_exists;use_only_q_ge_17:trace_survivor_exists | Decide whether reliance on q=3 or another focused eliminating prime should be part of the human check. |

## Exact Open Assumptions

- The Frey object is correct for every primitive solution case.
- The minimal conductor and lowered level are exactly the level used for comparison.
- The residual mod-5 representation is the correct irreducible representation for the trace comparison.
- The relevant level-220 newforms are exhausted by the imported Sage query.
- The q in {3,13,17,41,61} good-prime local enumeration covers all reductions required by the modular argument, including single-divisibility branches.
- Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only.
- Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) == +/-(q+1) mod 5 at q in {3,13,17,41,61}.
- Treat the cross-prime branch compatibility audit for q in {13,17,41,61} as a screen, not as fixed-branch coupling.
- Review whether q=3 behavior is small-prime-sensitive or supported by the larger focused primes.
- Verify the quantifier-safe cross-prime route: each level-220 newform must have one non-q=3 eliminating prime with complete same-prime branch coverage.
- Prove the symbolic Frey invariant formulas give the minimal conductor support after local minimization.
- Run the bad-prime Tate algorithm at 2, 5, and 11.
- Verify every formal level-lowering obligation, including residual irreducibility and exact target level 220.
- Derive the conductor-exponent model rather than relying on symbolic valuation heuristics at bad primes.
- Explain each factor of level 220 and resolve `level_11_factor_unjustified`.
- Remove every prime dividing ABC by a verified level-lowering argument or change the comparison level.
- Treat the Sage conductor sanity script as formula-checking support only.
- Generate and test plausible comparison levels before treating level 220 as the target.

## Why This Is Not A Proof

The computation only supplies conditional route evidence. Until the Frey attachment, conductor, irreducibility, level-lowering, newform-space, and local-coverage lemmas are supplied by hand, the result remains capped at `worth_human_modular_review`.
