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

## 3. Modular Shadow

The modular-shadow layer creates symbolic obstruction records:

- Radical support from the exponent signature and local prime.
- Bad-prime support using `2`, exponent radicals, and `ell`.
- A conductor-like complexity score.
- Placeholder Frey-curve metadata that records what a later modular method
  would need to instantiate.
- Cluster keys that group cases with the same obstruction shape.

## 4. Experiment Runner

The runner writes each sweep to `runs/<timestamp>/`:

- `summary.csv`: one row per `(p,q,r,ell)`.
- `interesting_cases.csv`: ranked candidate/watchlist rows.
- `clusters.csv`: repeated obstruction fingerprints.
- `metadata.json`: parameters and reproducibility data.
- `README_REPORT.md`: human-readable report.

The generated report explicitly avoids proof language.
