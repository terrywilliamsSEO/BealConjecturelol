# Beal RSG Lab

`beal_rsg_lab` is a computational research lab for finding reusable obstruction
patterns in primitive generalized Fermat equations

```text
A^x + B^y = C^z,  x,y,z > 2,  gcd(A,B,C) = 1.
```

The Beal Conjecture is the flagship test case, but the code does not try to
prove Beal directly. It searches for residue, valuation, and modular-shadow
patterns that primitive counterexamples would be forced to satisfy.

## Current Engine

- `beal_rsg_lab/rsg_residue_engine.py`: residue sets, survivor density, entropy,
  lift survival to `ell^2`, repeated fingerprints, and randomized coset controls.
- `beal_rsg_lab/rsg_valuation_engine.py`: zero-class, lift-failure, and
  descent-like valuation diagnostics.
- `beal_rsg_lab/zero_support_engine.py`: exact zero-support masks
  (`none`, `A_only`, `B_only`, `C_only`, `AB`, `AC`, `BC`, `ABC`) for
  zero-adjoined local survivors.
- `beal_rsg_lab/primitive_obstruction_classifier.py`: separates direct
  primitive obstructions, mandatory single-divisor candidates, sparse unit
  survivors, and likely small-prime artifacts.
- `beal_rsg_lab/padic_lift_audit.py`: conservative `ell^2`/`ell^3` audit for
  mandatory single-divisor rows.
- `beal_rsg_lab/exact_explanation_generator.py`: human-readable modular
  explanations for top rows.
- `beal_rsg_lab/unit_survivor_geometry.py`: geometry metrics for sparse nonzero
  unit survivors, including triples, orbits, additive energy, entropy, and
  compression.
- `beal_rsg_lab/artifact_explainer.py`: demotes sparse rows explained by tiny
  power images, order-two images, or identical subgroup-size controls.
- `beal_rsg_lab/character_fingerprint.py`: Legendre and higher-character
  fingerprints for survivor triples.
- `beal_rsg_lab/padic_unit_lift.py`: `ell^2`/`ell^3` unit-survivor lift audit.
- `beal_rsg_lab/multi_prime_compatibility.py`: CRT-style combined-density
  compatibility for repeated sparse signatures.
- `beal_rsg_lab/exact_sparse_lemma_generator.py`: human-readable sparse
  unit-survivor lemma explanations.
- `beal_rsg_lab/rsg_modular_shadow.py`: symbolic obstruction records,
  conductor-like complexity, Frey-curve placeholder data, and candidate ranking.
- `beal_rsg_lab/signature_normalizer.py`: canonical signature IDs under
  `A/B` swapping, with repeated-exponent and fourth-power flags.
- `beal_rsg_lab/frey_template_library.py`: symbolic Frey-style template records
  with uncertainty flags rather than proof claims.
- `beal_rsg_lab/finite_field_trace_probe.py`: point-count and trace probes for
  nonsingular candidate Frey curves over finite fields.
- `beal_rsg_lab/modular_shadow_engine.py`: route scoring that combines
  non-artifact survivor geometry, Frey templates, and trace rigidity.
- `beal_rsg_lab/cross_prime_trace_compatibility.py`: canonical-signature trace
  compatibility across repeated prime shadows.
- `beal_rsg_lab/sage_optional_newform_probe.py`: optional Sage availability and
  newform-check instructions.
- `beal_rsg_lab/modular_route_classifier.py`: final proof-route sketch
  classification.
- `beal_rsg_lab/run_experiment.py`: full sweep runner that writes
  the broad RSG files plus zero-support, unit-geometry, and modular-shadow
  reports under `runs/<timestamp>/`.

## Quick Start

```powershell
python -m unittest discover
python run_experiment.py --prime-limit 31 --control-samples 16
```

For a faster smoke run:

```powershell
python run_experiment.py --primes 5,7,11 --control-samples 6 --no-lift
```

## Research Standard

The report ranks possible publishable obstruction candidates. It must not be
read as a proof. A pattern is promoted only when it repeats across multiple
prime/signature contexts and beats randomized subgroup-coset controls.

See:

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md)
- [docs/RESEARCH_STATUS.md](docs/RESEARCH_STATUS.md)
- [docs/reports/initial_20260620_103500.md](docs/reports/initial_20260620_103500.md)
- [docs/reports/zero_support_20260620_105000.md](docs/reports/zero_support_20260620_105000.md)
- [docs/reports/unit_geometry_20260620_111500.md](docs/reports/unit_geometry_20260620_111500.md)
- [docs/reports/modular_shadow_20260620_154000.md](docs/reports/modular_shadow_20260620_154000.md)
- [docs/AGENT_GUIDE.md](docs/AGENT_GUIDE.md)
