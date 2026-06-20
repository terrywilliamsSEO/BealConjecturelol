# Architecture

The lab is organized as a pipeline. Each stage emits structured records that
can be checked, clustered, and reviewed by another agent.

## 1. Residue Engine

Input:

- Ordered exponent signatures `(p,q,r)` from `{3,4,5,7,11,13}`.
- Odd primes `ell`.

For each `(p,q,r,ell)` the engine computes nonzero power residue sets:

```text
R_p(ell) = { a^p mod ell : a in F_ell^* }
```

It then counts primitive local survivors of

```text
u + v = w mod ell,
u in R_p(ell), v in R_q(ell), w in R_r(ell).
```

The current primitive proxy is "all three local classes are nonzero." Global
coprimality is not inferred from a single prime.

Measured fields include:

- Survivor count and pair density.
- Shannon entropy of the output residue distribution.
- Lift survival to unit power residues modulo `ell^2`.
- Residue fingerprints based on subgroup shape and coarse density/lift buckets.
- Randomized multiplicative subgroup-coset controls with matching cardinalities.

## 2. Valuation Engine

The valuation layer asks whether the residue survivors behave like the start of
a local descent obstruction.

It records:

- Zero-class solution counts after adjoining zero to each residue set.
- Zero-dominance ratios.
- Unit lift failure rates.
- Flags such as `no_unit_lifts`, `high_lift_failure`,
  `zero_class_dominates`, and `descent_like_chain`.

These are diagnostics, not theorems. They are intended to help identify
patterns worth turning into precise lemmas.

## 3. Zero-Support Engine

The zero-support layer converts coarse zero-class dominance into exact masks.
For every zero-adjoined local survivor it records whether the support is:

```text
none, A_only, B_only, C_only, AB, AC, BC, ABC
```

This distinction matters because one-variable divisibility is not a primitive
contradiction. A primitive counterexample may have `ell | A` while
`ell` does not divide `B` or `C`. The promising cases are:

- every local survivor has at least two variables zero modulo `ell`;
- every local survivor has the same exact one-variable mask, and p-adic lifting
  makes that branch impossible or forces valuation growth;
- unit survivors exist but are unusually sparse against controls.

## 4. Primitive Obstruction Classifier

Rows are classified as:

- `direct_primitive_obstruction`
- `mandatory_single_divisor`
- `sparse_unit_survivor`
- `likely_small_prime_artifact`
- `control_like`

Small-prime and trivial subgroup-collapse rows are intentionally demoted so they
do not masquerade as Beal-type contradictions.

## 5. P-Adic Lift Audit

Mandatory single-divisor rows are lifted through `ell^2` and `ell^3` where
feasible. The audit is conservative: for exponents greater than `2`, a variable
divisible exactly once by `ell` already contributes `0` modulo `ell^3`, so no
valuation growth is claimed unless the branch actually dies.

## 6. Modular Shadow

The modular-shadow layer creates symbolic obstruction records:

- Radical support from the exponent signature and local prime.
- Bad-prime support using `2`, exponent radicals, and `ell`.
- A conductor-like complexity score.
- Placeholder Frey-curve metadata that records what a later modular method
  would need to instantiate.
- Cluster keys that group cases with the same obstruction shape.

## 7. Experiment Runner

The runner writes each sweep to `runs/<timestamp>/`:

- `summary.csv`: one row per `(p,q,r,ell)`.
- `interesting_cases.csv`: ranked candidate/watchlist rows.
- `clusters.csv`: repeated obstruction fingerprints.
- `zero_support_summary.csv`: exact zero-support and primitive classification.
- `direct_obstructions.csv`: exact direct primitive obstruction candidates.
- `mandatory_single_divisor_candidates.csv`: exact one-variable candidates with
  p-adic audit fields.
- `sparse_unit_clusters.csv`: larger-prime sparse unit-survivor clusters.
- `metadata.json`: parameters and reproducibility data.
- `README_REPORT.md`: human-readable report.
- `README_ZERO_SUPPORT_REPORT.md`: exact zero-support report.

The generated report explicitly avoids proof language.
