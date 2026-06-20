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
- `beal_rsg_lab/rsg_modular_shadow.py`: symbolic obstruction records,
  conductor-like complexity, Frey-curve placeholder data, and candidate ranking.
- `beal_rsg_lab/run_experiment.py`: full sweep runner that writes
  `summary.csv`, `interesting_cases.csv`, `clusters.csv`, and `README_REPORT.md`
  under `runs/<timestamp>/`.

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
- [docs/AGENT_GUIDE.md](docs/AGENT_GUIDE.md)
