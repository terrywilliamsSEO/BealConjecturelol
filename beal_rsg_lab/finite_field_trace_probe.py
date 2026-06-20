"""Finite-field trace probes for the candidate Frey curve."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from math import log2
import random

from .number_theory import primitive_root_mod_prime, shannon_entropy
from .unit_survivor_geometry import UnitSurvivorGeometry


@dataclass(frozen=True)
class TraceProbeRecord:
    """Trace distribution for one sparse row."""

    signature: tuple[int, int, int]
    ell: int
    survivor_triple_count: int
    nonsingular_triple_count: int
    singular_skipped_count: int
    trace_distribution: dict[int, int]
    trace_support_size: int
    trace_entropy: float
    normalized_trace_entropy: float
    same_size_control_distribution: dict[int, int]
    same_size_control_trace_support_size: int
    same_size_control_trace_entropy: float
    random_subset_control_mean_support: float
    random_subset_control_mean_entropy: float
    unusually_narrow_trace: bool
    trace_rigidity_score: float
    trace_fingerprint: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["trace_distribution"] = ";".join(
            f"{trace}:{count}" for trace, count in sorted(self.trace_distribution.items())
        )
        data["same_size_control_distribution"] = ";".join(
            f"{trace}:{count}" for trace, count in sorted(self.same_size_control_distribution.items())
        )
        return data


def is_singular_frey_curve(a_power: int, b_power: int, ell: int) -> bool:
    """Return True if y^2=x(x-a)(x+b) is singular over F_ell."""
    return a_power % ell == 0 or b_power % ell == 0 or (a_power + b_power) % ell == 0


def _legendre(value: int, ell: int) -> int:
    value %= ell
    if value == 0:
        return 0
    symbol = pow(value, (ell - 1) // 2, ell)
    return -1 if symbol == ell - 1 else symbol


def count_points_on_frey_curve(a_power: int, b_power: int, ell: int) -> int:
    """Count points on y^2=x(x-a)(x+b) over F_ell, including infinity."""
    if is_singular_frey_curve(a_power, b_power, ell):
        raise ValueError("singular Frey curve specialization")
    count = 1
    for x in range(ell):
        rhs = (x * (x - a_power) * (x + b_power)) % ell
        symbol = _legendre(rhs, ell)
        if symbol == 0:
            count += 1
        elif symbol == 1:
            count += 2
    return count


def trace_for_frey_curve(a_power: int, b_power: int, ell: int) -> int:
    """Return a_ell for the candidate Frey curve."""
    return ell + 1 - count_points_on_frey_curve(a_power, b_power, ell)


def _subgroup_of_size(ell: int, size: int) -> tuple[int, ...]:
    root = primitive_root_mod_prime(ell)
    step = (ell - 1) // size
    return tuple(sorted(pow(root, step * index, ell) for index in range(size)))


def _trace_distribution_for_sets(left: tuple[int, ...], right: tuple[int, ...], output: set[int], ell: int) -> tuple[Counter[int], int]:
    traces: Counter[int] = Counter()
    singular = 0
    for u in left:
        for v in right:
            w = (u + v) % ell
            if w not in output:
                continue
            if is_singular_frey_curve(u, v, ell):
                singular += 1
                continue
            traces[trace_for_frey_curve(u, v, ell)] += 1
    return traces, singular


def _entropy(counter: Counter[int]) -> tuple[float, float]:
    entropy = shannon_entropy(counter.values())
    max_entropy = log2(len(counter)) if len(counter) > 1 else 0.0
    normalized = entropy / max_entropy if max_entropy else 0.0
    return round(entropy, 10), round(min(1.0, normalized), 10)


def _random_subset_controls(geometry: UnitSurvivorGeometry, *, samples: int = 24, seed: int = 20260620) -> tuple[float, float]:
    rng = random.Random(seed + geometry.ell * 1009 + sum(geometry.signature))
    universe = tuple(range(1, geometry.ell))
    support_sizes: list[int] = []
    entropies: list[float] = []
    for _ in range(samples):
        left = tuple(sorted(rng.sample(universe, geometry.subgroup_size_shape[0])))
        right = tuple(sorted(rng.sample(universe, geometry.subgroup_size_shape[1])))
        output = set(rng.sample(universe, geometry.subgroup_size_shape[2]))
        traces, _ = _trace_distribution_for_sets(left, right, output, geometry.ell)
        support_sizes.append(len(traces))
        entropies.append(_entropy(traces)[0])
    return round(sum(support_sizes) / samples, 10), round(sum(entropies) / samples, 10)


def trace_probe_for_geometry(geometry: UnitSurvivorGeometry) -> TraceProbeRecord:
    """Probe finite-field trace distribution for actual unit survivor triples."""
    actual_traces: Counter[int] = Counter()
    singular = 0
    for u, v, _ in geometry.survivor_triples:
        if is_singular_frey_curve(u, v, geometry.ell):
            singular += 1
            continue
        actual_traces[trace_for_frey_curve(u, v, geometry.ell)] += 1

    left = _subgroup_of_size(geometry.ell, geometry.subgroup_size_shape[0])
    right = _subgroup_of_size(geometry.ell, geometry.subgroup_size_shape[1])
    output = set(_subgroup_of_size(geometry.ell, geometry.subgroup_size_shape[2]))
    control_traces, _ = _trace_distribution_for_sets(left, right, output, geometry.ell)

    entropy, normalized = _entropy(actual_traces)
    control_entropy, _ = _entropy(control_traces)
    random_support, random_entropy = _random_subset_controls(geometry)
    support = len(actual_traces)
    control_support = len(control_traces)
    unusually_narrow = support < control_support and entropy + 0.25 < control_entropy
    rigidity = max(0.0, control_entropy - entropy) + max(0.0, control_support - support) * 0.5
    if support and geometry.survivor_count:
        rigidity += (1.0 - support / geometry.survivor_count)
    fingerprint = f"traces={dict(sorted(actual_traces.items()))}|support={support}|entropy={entropy}"
    return TraceProbeRecord(
        signature=geometry.signature,
        ell=geometry.ell,
        survivor_triple_count=geometry.survivor_count,
        nonsingular_triple_count=sum(actual_traces.values()),
        singular_skipped_count=singular,
        trace_distribution=dict(actual_traces),
        trace_support_size=support,
        trace_entropy=entropy,
        normalized_trace_entropy=normalized,
        same_size_control_distribution=dict(control_traces),
        same_size_control_trace_support_size=control_support,
        same_size_control_trace_entropy=control_entropy,
        random_subset_control_mean_support=random_support,
        random_subset_control_mean_entropy=random_entropy,
        unusually_narrow_trace=unusually_narrow,
        trace_rigidity_score=round(rigidity, 10),
        trace_fingerprint=fingerprint,
    )


def trace_probes_for_geometries(geometries: list[UnitSurvivorGeometry]) -> list[TraceProbeRecord]:
    """Probe trace distributions for many geometries."""
    records = [trace_probe_for_geometry(geometry) for geometry in geometries]
    records.sort(key=lambda item: (item.unusually_narrow_trace, item.trace_rigidity_score), reverse=True)
    return records
