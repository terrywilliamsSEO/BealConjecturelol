# Conditional Modular Route For Primitive Solutions Of `A^5 + B^4 = C^5`

This is a theorem skeleton, not a completed argument. It lists the exact hand-written lemmas needed before the computational trace mismatch can carry mathematical force.

## Statement Of Hypothetical Primitive Solution

Assume nonzero integers `A,B,C` satisfy `A^5 + B^4 = C^5` and `gcd(A,B,C)=1`, with all normalization and sign conventions stated explicitly.

## Proposed Frey Object

`E: y^2 = x(x - A^5)(x + B^4)`.

## Required Lemma 1: Frey Attachment

Attach E: y^2 = x(x - A^5)(x + B^4) to every primitive solution in the required orientation.

- Current evidence: Template exists in the route library.
- Status: `needs_hand_derivation`.
- Next action: Derive nonsingularity and integral model conditions for all primitive solution cases.

## Required Lemma 2: Discriminant/Conductor Computation

Compute the minimal discriminant and conductor exponents, including primes 2, 5, 11, and primes dividing ABC.

- Current evidence: Symbolic discriminant-like support is 16*A^10*B^8*C^10.
- Status: `needs_hand_derivation`.
- Next action: Run a prime-by-prime minimal model and conductor analysis.

## Required Lemma 3: Residual Mod-5 Irreducibility

Show the relevant residual representation modulo 5 is irreducible and has the required ramification behavior.

- Current evidence: The current trace filter uses mod-5 comparison mode.
- Status: `missing`.
- Next action: Identify the exact representation and prove irreducibility or state required exceptions.

## Required Lemma 4: Level Lowering To Level 220

Show the modular representation lowers to the weight-2 level-220 space used by the Sage query.

- Current evidence: 110:level_data_insufficient;220:level_220_mismatch_candidate;440:level_data_insufficient
- Status: `needs_hand_derivation`.
- Next action: Justify why the comparison level is 220 and why no nearby level should be used instead.

## Required Lemma 5: Level-220 Newform Exhaustion

Verify that the two imported level-220 newform slots are the complete relevant target space.

- Current evidence: Current trace progress label is trace_mismatch_candidate.
- Status: `computed_route_evidence`.
- Next action: Confirm old/new decomposition, character choices, coefficient fields, and labels in Sage or Magma.

## Required Lemma 6: Good-Prime Trace Exclusion

For each relevant good prime, compare Frey trace possibilities with newform coefficients in the justified residue field.

- Current evidence: 2 of 2 level-220 newforms eliminated by current filter.
- Status: `computed_route_evidence`.
- Next action: Check the first eliminating primes independently and justify the local enumeration.

## Required Lemma 7: Local Valuation And Reduction Case Split For q | ABC

Handle reductions where q divides one or more of A,B,C, or prove they are not needed for the chosen good-prime trace step.

- Current evidence: local_coverage_gap; scope=unit_only_trace_mismatch_candidate; full_coverage_eliminating_primes=none
- Status: `local_coverage_gap`.
- Next action: Prove the q=13/q=17 local valuation and reduction case split for q | ABC, including A_only, B_only, C_only, and singular Frey reductions.

## Current Computational Evidence

| obligation | status | evidence | next action |
| --- | --- | --- | --- |
| `TS545-001` | `conditional_setup` | Framework assumption only. | State sign, nonzero, coprimality, and normalization conventions exactly. |
| `TS545-002` | `needs_hand_derivation` | Template exists in the route library. | Derive nonsingularity and integral model conditions for all primitive solution cases. |
| `TS545-003` | `needs_hand_derivation` | Symbolic discriminant-like support is 16*A^10*B^8*C^10. | Run a prime-by-prime minimal model and conductor analysis. |
| `TS545-004` | `missing` | The current trace filter uses mod-5 comparison mode. | Identify the exact representation and prove irreducibility or state required exceptions. |
| `TS545-005` | `needs_hand_derivation` | 110:level_data_insufficient;220:level_220_mismatch_candidate;440:level_data_insufficient | Justify why the comparison level is 220 and why no nearby level should be used instead. |
| `TS545-006` | `computed_route_evidence` | Current trace progress label is trace_mismatch_candidate. | Confirm old/new decomposition, character choices, coefficient fields, and labels in Sage or Magma. |
| `TS545-007` | `computed_route_evidence` | 2 of 2 level-220 newforms eliminated by current filter. | Check the first eliminating primes independently and justify the local enumeration. |
| `TS545-008` | `local_coverage_gap` | local_coverage_gap; scope=unit_only_trace_mismatch_candidate; full_coverage_eliminating_primes=none | Prove the q=13/q=17 local valuation and reduction case split for q | ABC, including A_only, B_only, C_only, and singular Frey reductions. |
| `TS545-009` | `computed_route_evidence` | exclude_q_3:trace_mismatch_candidate;exclude_q_3_7:trace_mismatch_candidate;exclude_q_lt_11:trace_mismatch_candidate;exclude_q_lt_17:trace_survivor_exists;use_only_q_ge_17:trace_survivor_exists | Decide whether q=13 or q=17 sensitivity should be part of the human check. |

## Exact Open Assumptions

- The Frey object is correct for every primitive solution case.
- The minimal conductor and lowered level are exactly the level used for comparison.
- The residual mod-5 representation is the correct irreducible representation for the trace comparison.
- The relevant level-220 newforms are exhausted by the imported Sage query.
- The q=13 and q=17 good-prime local enumeration covers all reductions required by the modular argument, including single-divisibility branches.

## Why This Is Not A Proof

The computation only supplies conditional route evidence. Until the Frey attachment, conductor, irreducibility, level-lowering, newform-space, and local-coverage lemmas are supplied by hand, the result remains capped at `worth_human_modular_review`.
