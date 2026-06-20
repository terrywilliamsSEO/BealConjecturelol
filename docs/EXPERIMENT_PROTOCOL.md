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

## Zero-Support Upgrade

Zero-class dominance is not enough. A primitive generalized Fermat solution may
have one variable divisible by `ell`. The exact zero-support pass therefore
uses this stricter ranking:

1. Highest value: `direct_primitive_obstruction`, where every local survivor has
   at least two variables zero modulo `ell`.
2. Second value: `mandatory_single_divisor`, where every local survivor has the
   same exact one-variable zero mask and the p-adic audit kills or strengthens
   the branch.
3. Third value: `sparse_unit_survivor`, where unit survivors exist but are
   unusually sparse against controls and are not explained by tiny-prime
   subgroup collapse.
4. Demoted: `likely_small_prime_artifact`, including tiny primes and trivial
   power-subgroup collapse.

## Unit-Geometry Upgrade

Sparse unit rows are not promoted until they survive artifact checks.

Demote rows when:

- sparsity is explained by an order-two image such as `{1,-1}`;
- identical subgroup-size controls reproduce the same density;
- the row is dominated by tiny-prime behavior.

Promote rows only when:

- the row remains unusually sparse against same-size structured controls; and
- unit survivors collapse or become rigid under `ell^2`/`ell^3` lifts; or
- repeated prime constraints become extremely rigid under CRT-style combined
  density.

Rows that survive artifact checks but do not collapse under unit lifts are
ranked as `needs modular-shadow follow-up`.

## Modular-Shadow Routing

The modular-shadow router is a proof-route ranking stage for the current
non-artifact follow-up signatures:

```text
(4,7,7), (7,4,7), (5,4,5), (4,5,5),
(3,5,5), (5,3,5), (7,7,4), (3,4,3)
```

It combines exact unit-survivor geometry with symbolic Frey-template metadata
and finite-field trace probes. The candidate Frey template

```text
E: y^2 = x(x - A^p)(x + B^q)
```

is stored as a template record, not as a theorem. Each row carries uncertainty
flags for minimal models, conductor computation, irreducibility, and newform
comparison.

Demote rows when:

- the sparse behavior is explained by subgroup size or tiny power images;
- finite-field trace support is no narrower than same-size structured controls;
- the only evidence is local density.

Promote only proof-route sketches when:

- the row is non-artifact under the unit-geometry audit;
- Frey-template confidence is reasonable;
- trace distributions are unusually rigid versus structured controls.

Repeated non-artifact trace fingerprints across primes may be logged as
`needs_newform_check`, but that status is not a proof claim and is not by itself
a promoted route.

## What Counts As Evidence

Useful evidence:

- Repeated residue fingerprints across unrelated `(p,q,r,ell)` contexts.
- Low survivor density compared with matched subgroup-coset controls.
- Stable lift failure to `ell^2`.
- Zero-class dominance that suggests shared-prime collapse.
- Clusters with coherent radical/bad-prime support.
- Finite-field trace distributions that separate from same-size subgroup
  controls.

Insufficient evidence:

- A single sparse prime.
- A pattern that randomized controls produce just as often.
- A lift failure with no repeated cluster.
- A `needs_newform_check` label without trace rigidity.
- Any result phrased as a proof of Beal.

## Recommended Iteration

1. Run a broad default sweep.
2. Inspect `interesting_cases.csv` for promoted and watchlist rows.
3. Inspect `clusters.csv` for repeated obstruction shapes.
4. Add targeted follow-up experiments for the strongest clusters.
5. Convert stable patterns into precise lemma statements in a separate note.
