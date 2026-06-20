# Experiment Protocol

## Goal

Discover publishable obstruction candidates for primitive generalized Fermat
equations, using the Beal Conjecture as the motivating test case.

The target output is a reusable lemma candidate:

```text
Any primitive solution would be forced into pattern P,
but pattern P appears incompatible with stronger local or modular consistency.
```

## Default Sweep

- Exponents: ordered triples from `{3,4,5,7,11,13}`.
- Primes: odd primes up to the selected `--prime-limit`.
- Controls: randomized multiplicative subgroup cosets with the same residue-set
  sizes as the true power-residue sets.

## Promotion Gate

A case is promoted only if it satisfies all of the following:

1. Its obstruction cluster repeats across multiple primes or multiple
   signatures. For `promoted_candidate`, the default gate requires both
   multiple primes and multiple signatures; one-axis repetition is a watchlist
   signal.
2. Its survivor density beats randomized controls, currently encoded as a
   negative z-score at or below the configured gate (`-1.5` by default).
3. It has a valuation or lift flag that gives the pattern mathematical content.

Rows that are suggestive but miss one gate are listed as `watchlist`, not
`promoted_candidate`.

## What Counts As Evidence

Useful evidence:

- Repeated residue fingerprints across unrelated `(p,q,r,ell)` contexts.
- Low survivor density compared with matched subgroup-coset controls.
- Stable lift failure to `ell^2`.
- Zero-class dominance that suggests shared-prime collapse.
- Clusters with coherent radical/bad-prime support.

Insufficient evidence:

- A single sparse prime.
- A pattern that randomized controls produce just as often.
- A lift failure with no repeated cluster.
- Any result phrased as a proof of Beal.

## Recommended Iteration

1. Run a broad default sweep.
2. Inspect `interesting_cases.csv` for promoted and watchlist rows.
3. Inspect `clusters.csv` for repeated obstruction shapes.
4. Add targeted follow-up experiments for the strongest clusters.
5. Convert stable patterns into precise lemma statements in a separate note.
