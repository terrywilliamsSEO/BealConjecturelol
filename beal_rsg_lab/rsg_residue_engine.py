"""Residue signature grid engine.

This module sweeps exponent signatures and local primes, counts nonzero
survivors of u + v = w, measures lift survival to ell^2, and compares true
power-residue behavior against randomized multiplicative subgroup-coset
controls.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from itertools import product
from math import gcd, log2
import random
from statistics import mean, pstdev
from typing import Iterable

from .number_theory import primitive_root_mod_prime, primes_up_to, shannon_entropy, stable_float

DEFAULT_EXPONENTS: tuple[int, ...] = (3, 4, 5, 7, 11, 13)
DEFAULT_PRIME_LIMIT = 43


Signature = tuple[int, int, int]


@dataclass(frozen=True)
class SurvivorData:
    """Raw survivor count data for one residue equation."""

    count: int
    pair_count: int
    triples: tuple[tuple[int, int, int], ...]
    output_counts: dict[int, int]


@dataclass(frozen=True)
class ControlStats:
    """Density statistics for randomized subgroup-coset controls."""

    samples: int
    mean_density: float
    stdev_density: float
    min_density: float
    max_density: float
    z_score: float


@dataclass(frozen=True)
class ResidueSweepResult:
    """One row of residue-sweep output."""

    signature: Signature
    ell: int
    residue_sizes: tuple[int, int, int]
    survivor_count: int
    pair_count: int
    density: float
    entropy_bits: float
    normalized_entropy: float
    lift_survivor_count: int
    lift_trial_count: int
    lift_survival_rate: float
    residue_fingerprint: str
    control_samples: int
    control_mean_density: float
    control_stdev_density: float
    control_min_density: float
    control_max_density: float
    control_z_score: float

    def to_flat_dict(self) -> dict[str, object]:
        """Return a CSV-friendly representation."""
        data = asdict(self)
        p, q, r = self.signature
        sp, sq, sr = self.residue_sizes
        data.update(
            {
                "p": p,
                "q": q,
                "r": r,
                "size_p": sp,
                "size_q": sq,
                "size_r": sr,
                "signature": f"{p}-{q}-{r}",
            }
        )
        data.pop("residue_sizes", None)
        return data


def signature_space(exponents: Iterable[int] = DEFAULT_EXPONENTS) -> tuple[Signature, ...]:
    """Return ordered exponent signatures."""
    values = tuple(exponents)
    return tuple(product(values, repeat=3))


def parse_prime_list(value: str) -> tuple[int, ...]:
    """Parse a comma-separated prime list."""
    primes = tuple(int(part.strip()) for part in value.split(",") if part.strip())
    if not primes:
        raise ValueError("prime list cannot be empty")
    return primes


def power_residue_set(
    exponent: int,
    modulus: int,
    *,
    include_zero: bool = False,
    units_only: bool = True,
) -> tuple[int, ...]:
    """Return sorted exponent-power residues modulo modulus.

    By default this uses unit bases only. For prime moduli that is the same as
    all nonzero bases; for ell^2 it keeps the lift calculation on unit classes.
    """
    if modulus < 2:
        raise ValueError("modulus must be at least 2")
    residues: set[int] = set()
    start = 0 if include_zero else 1
    for base in range(start, modulus):
        if units_only and gcd(base, modulus) != 1:
            continue
        residues.add(pow(base, exponent, modulus))
    if include_zero:
        residues.add(0)
    else:
        residues.discard(0)
    return tuple(sorted(residues))


def count_survivors(
    left_residues: Iterable[int],
    right_residues: Iterable[int],
    output_residues: Iterable[int],
    modulus: int,
    *,
    keep_triples: bool = True,
) -> SurvivorData:
    """Count residue triples u + v = w mod modulus."""
    left = tuple(left_residues)
    right = tuple(right_residues)
    output = set(output_residues)
    pair_count = len(left) * len(right)
    triples: list[tuple[int, int, int]] = []
    output_counts: Counter[int] = Counter()
    count = 0
    for u in left:
        for v in right:
            w = (u + v) % modulus
            if w in output:
                count += 1
                output_counts[w] += 1
                if keep_triples:
                    triples.append((u, v, w))
    return SurvivorData(
        count=count,
        pair_count=pair_count,
        triples=tuple(triples),
        output_counts=dict(output_counts),
    )


def survivor_density(survivor_count: int, pair_count: int) -> float:
    """Return survivor density among possible (u,v) pairs."""
    if pair_count == 0:
        return 0.0
    return survivor_count / pair_count


def output_entropy(output_counts: dict[int, int], output_residue_count: int) -> tuple[float, float]:
    """Return entropy and normalized entropy for survivor output residues."""
    entropy = shannon_entropy(output_counts.values())
    if output_residue_count <= 1:
        return entropy, 0.0
    max_entropy = log2(output_residue_count)
    normalized = min(1.0, entropy / max_entropy) if max_entropy else 0.0
    return entropy, normalized


def _coefficient_lift_sets(exponent: int, ell: int) -> dict[int, frozenset[int]]:
    """Group unit power residues modulo ell^2 by their reduction modulo ell."""
    modulus = ell * ell
    grouped: dict[int, set[int]] = defaultdict(set)
    for residue in power_residue_set(exponent, modulus, units_only=True):
        reduced = residue % ell
        grouped[reduced].add(((residue - reduced) // ell) % ell)
    return {key: frozenset(values) for key, values in grouped.items()}


def _has_lift(
    u: int,
    v: int,
    w: int,
    ell: int,
    left_coeffs: dict[int, frozenset[int]],
    right_coeffs: dict[int, frozenset[int]],
    output_coeffs: dict[int, frozenset[int]],
) -> bool:
    """Return True if a mod ell survivor has a unit lift to ell^2."""
    left = left_coeffs.get(u, frozenset())
    right = right_coeffs.get(v, frozenset())
    output = output_coeffs.get(w, frozenset())
    if not left or not right or not output:
        return False
    carry = (u + v - w) // ell
    for a in left:
        for b in right:
            if (a + b + carry) % ell in output:
                return True
    return False


def lift_survival_count(signature: Signature, ell: int, triples: Iterable[tuple[int, int, int]]) -> int:
    """Count mod ell survivors that have a unit power-residue lift to ell^2."""
    p, q, r = signature
    left_coeffs = _coefficient_lift_sets(p, ell)
    right_coeffs = _coefficient_lift_sets(q, ell)
    output_coeffs = _coefficient_lift_sets(r, ell)
    return sum(1 for u, v, w in triples if _has_lift(u, v, w, ell, left_coeffs, right_coeffs, output_coeffs))


def density_bucket(value: float) -> str:
    """Coarse density bucket for repeated fingerprints."""
    if value == 0:
        return "empty"
    if value < 0.05:
        return "very_sparse"
    if value < 0.15:
        return "sparse"
    if value < 0.35:
        return "thin"
    if value < 0.65:
        return "balanced"
    return "dense"


def lift_bucket(value: float, trials: int) -> str:
    """Coarse lift-survival bucket."""
    if trials == 0:
        return "no_trials"
    if value == 0:
        return "no_lifts"
    if value < 0.25:
        return "rare_lifts"
    if value < 0.75:
        return "mixed_lifts"
    return "stable_lifts"


def residue_fingerprint(
    signature: Signature,
    ell: int,
    residue_sizes: tuple[int, int, int],
    density: float,
    entropy: float,
    lift_rate: float,
    lift_trials: int,
) -> str:
    """Build a repeated residue fingerprint."""
    gcd_shape = tuple(gcd(exponent, ell - 1) for exponent in signature)
    entropy_bucket = "low_entropy" if entropy < 1 else "mid_entropy" if entropy < 3 else "high_entropy"
    return (
        f"gcd_shape={gcd_shape}|sizes={residue_sizes}|"
        f"density={density_bucket(density)}|entropy={entropy_bucket}|"
        f"lift={lift_bucket(lift_rate, lift_trials)}"
    )


def random_subgroup_coset(prime: int, size: int, rng: random.Random) -> tuple[int, ...]:
    """Return a random multiplicative subgroup coset of requested size."""
    if size <= 0 or (prime - 1) % size != 0:
        raise ValueError(f"size {size} must divide {prime - 1}")
    root = primitive_root_mod_prime(prime)
    step = (prime - 1) // size
    subgroup = {pow(root, step * index, prime) for index in range(size)}
    multiplier = rng.randrange(1, prime)
    return tuple(sorted((multiplier * value) % prime for value in subgroup))


def randomized_control_stats(
    ell: int,
    residue_sizes: tuple[int, int, int],
    observed_density: float,
    *,
    samples: int,
    rng: random.Random,
) -> ControlStats:
    """Compare survivor density with randomized subgroup-coset controls."""
    if samples <= 0:
        return ControlStats(0, 0.0, 0.0, 0.0, 0.0, 0.0)
    densities: list[float] = []
    for _ in range(samples):
        left = random_subgroup_coset(ell, residue_sizes[0], rng)
        right = random_subgroup_coset(ell, residue_sizes[1], rng)
        output = random_subgroup_coset(ell, residue_sizes[2], rng)
        survivor_data = count_survivors(left, right, output, ell, keep_triples=False)
        densities.append(survivor_density(survivor_data.count, survivor_data.pair_count))
    control_mean = mean(densities)
    control_stdev = pstdev(densities)
    if control_stdev == 0:
        if observed_density == control_mean:
            z_score = 0.0
        else:
            z_score = float("inf") if observed_density > control_mean else float("-inf")
    else:
        z_score = (observed_density - control_mean) / control_stdev
    return ControlStats(
        samples=samples,
        mean_density=stable_float(control_mean),
        stdev_density=stable_float(control_stdev),
        min_density=stable_float(min(densities)),
        max_density=stable_float(max(densities)),
        z_score=stable_float(z_score),
    )


def run_signature_prime(
    signature: Signature,
    ell: int,
    *,
    compute_lift: bool = True,
    control_samples: int = 24,
    rng: random.Random | None = None,
) -> ResidueSweepResult:
    """Run one signature/prime computation."""
    rng = rng or random.Random(0)
    p, q, r = signature
    left = power_residue_set(p, ell)
    right = power_residue_set(q, ell)
    output = power_residue_set(r, ell)
    residue_sizes = (len(left), len(right), len(output))
    survivor_data = count_survivors(left, right, output, ell, keep_triples=compute_lift)
    density = survivor_density(survivor_data.count, survivor_data.pair_count)
    entropy, normalized_entropy = output_entropy(survivor_data.output_counts, len(output))
    if compute_lift and survivor_data.count:
        lifted = lift_survival_count(signature, ell, survivor_data.triples)
        lift_trials = survivor_data.count
        lift_rate = lifted / lift_trials
    else:
        lifted = 0
        lift_trials = survivor_data.count if compute_lift else 0
        lift_rate = 0.0
    controls = randomized_control_stats(
        ell,
        residue_sizes,
        density,
        samples=control_samples,
        rng=rng,
    )
    fingerprint = residue_fingerprint(signature, ell, residue_sizes, density, entropy, lift_rate, lift_trials)
    return ResidueSweepResult(
        signature=signature,
        ell=ell,
        residue_sizes=residue_sizes,
        survivor_count=survivor_data.count,
        pair_count=survivor_data.pair_count,
        density=stable_float(density),
        entropy_bits=stable_float(entropy),
        normalized_entropy=stable_float(normalized_entropy),
        lift_survivor_count=lifted,
        lift_trial_count=lift_trials,
        lift_survival_rate=stable_float(lift_rate),
        residue_fingerprint=fingerprint,
        control_samples=controls.samples,
        control_mean_density=controls.mean_density,
        control_stdev_density=controls.stdev_density,
        control_min_density=controls.min_density,
        control_max_density=controls.max_density,
        control_z_score=controls.z_score,
    )


def run_sweep(
    *,
    exponents: Iterable[int] = DEFAULT_EXPONENTS,
    primes: Iterable[int] | None = None,
    prime_limit: int = DEFAULT_PRIME_LIMIT,
    compute_lift: bool = True,
    control_samples: int = 24,
    seed: int = 20260620,
) -> list[ResidueSweepResult]:
    """Run the ordered signature sweep."""
    prime_values = tuple(primes) if primes is not None else primes_up_to(prime_limit, odd_only=True)
    signatures = signature_space(exponents)
    results: list[ResidueSweepResult] = []
    for sig_index, signature in enumerate(signatures):
        for prime_index, ell in enumerate(prime_values):
            rng = random.Random(seed + sig_index * 1009 + prime_index * 9176 + ell)
            results.append(
                run_signature_prime(
                    signature,
                    ell,
                    compute_lift=compute_lift,
                    control_samples=control_samples,
                    rng=rng,
                )
            )
    return results
