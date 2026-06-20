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
- `beal_rsg_lab/rsg_modular_shadow.py`: symbolic obstruction records,
  conductor-like complexity, Frey-curve placeholder data, and candidate ranking.
- `beal_rsg_lab/run_experiment.py`: full sweep runner that writes
  the broad RSG files plus zero-support reports under `runs/<timestamp>/`.

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
- [docs/AGENT_GUIDE.md](docs/AGENT_GUIDE.md)
