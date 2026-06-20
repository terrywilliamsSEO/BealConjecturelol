"""Geometry metrics for sparse nonzero unit-survivor rows."""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass
from math import gcd, log2
from typing import Iterable

from .number_theory import shannon_entropy
from .primitive_obstruction_classifier import PrimitiveClassification
from .rsg_residue_engine import ResidueSweepResult, Signature, count_survivors, power_residue_set


@dataclass(frozen=True)
class UnitSurvivorGeometry:
    """Unit-survivor geometry for one sparse row."""

    signature: Signature
    ell: int
    subgroup_gcd_shape: tuple[int, int, int]
    subgroup_size_shape: tuple[int, int, int]
    survivor_count: int
    pair_count: int
    density: float
    survivor_triples: tuple[tuple[int, int, int], ...]
    coset_concentration: float
    a_value_concentration: float
    b_value_concentration: float
    c_value_concentration: float
    common_scaling_subgroup_size: int
    orbit_count: int
    orbit_size_multiset: tuple[int, ...]
    orbit_compression: float
    swap_symmetric: bool
    swap_symmetry_score: float
    additive_energy: int
    normalized_additive_energy: float
    sumset_size: int
    intersection_size_hp_hq_with_hr: int
    survivor_entropy: float
    normalized_survivor_entropy: float
    survivor_compression_score: float
    geometry_fingerprint: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["subgroup_gcd_shape"] = "-".join(str(part) for part in self.subgroup_gcd_shape)
        data["subgroup_size_shape"] = "-".join(str(part) for part in self.subgroup_size_shape)
        data["survivor_triples"] = ";".join(f"{u}:{v}:{w}" for u, v, w in self.survivor_triples)
        data["orbit_size_multiset"] = ";".join(str(size) for size in self.orbit_size_multiset)
        return data


def _subgroups(signature: Signature, ell: int) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    return tuple(power_residue_set(exponent, ell) for exponent in signature)  # type: ignore[return-value]


def _subgroup_shapes(signature: Signature, ell: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    gcd_shape = tuple(gcd(exponent, ell - 1) for exponent in signature)
    size_shape = tuple((ell - 1) // value for value in gcd_shape)
    return gcd_shape, size_shape


def _max_marginal_share(triples: tuple[tuple[int, int, int], ...], index: int) -> float:
    if not triples:
        return 0.0
    counts = Counter(triple[index] for triple in triples)
    return max(counts.values()) / len(triples)


def _sum_counts(left: Iterable[int], right: Iterable[int], ell: int) -> Counter[int]:
    counts: Counter[int] = Counter()
    for u in left:
        for v in right:
            counts[(u + v) % ell] += 1
    return counts


def _orbit_sizes(
    triples: tuple[tuple[int, int, int], ...],
    scaling_subgroup: set[int],
    ell: int,
) -> tuple[int, tuple[int, ...]]:
    if not triples:
        return 0, ()
    triple_set = set(triples)
    seen: set[tuple[int, int, int]] = set()
    sizes: list[int] = []
    for triple in triples:
        if triple in seen:
            continue
        orbit: set[tuple[int, int, int]] = set()
        queue: deque[tuple[int, int, int]] = deque([triple])
        while queue:
            current = queue.popleft()
            if current in orbit:
                continue
            orbit.add(current)
            u, v, w = current
            for scale in scaling_subgroup:
                nxt = ((scale * u) % ell, (scale * v) % ell, (scale * w) % ell)
                if nxt in triple_set and nxt not in orbit:
                    queue.append(nxt)
        seen.update(orbit)
        sizes.append(len(orbit))
    return len(sizes), tuple(sorted(sizes, reverse=True))


def _entropy_for_triples(triples: tuple[tuple[int, int, int], ...]) -> tuple[float, float]:
    if not triples:
        return 0.0, 0.0
    output_counts = Counter(w for _, _, w in triples)
    entropy = shannon_entropy(output_counts.values())
    max_entropy = log2(len(output_counts)) if len(output_counts) > 1 else 0.0
    normalized = entropy / max_entropy if max_entropy else 0.0
    return round(entropy, 10), round(min(1.0, normalized), 10)


def analyze_unit_survivor_geometry(result: ResidueSweepResult) -> UnitSurvivorGeometry:
    """Analyze the unit-survivor geometry for one residue row."""
    hp, hq, hr = _subgroups(result.signature, result.ell)
    survivor_data = count_survivors(hp, hq, hr, result.ell, keep_triples=True)
    triples = survivor_data.triples
    triple_set = set(triples)
    subgroup_gcd_shape, subgroup_size_shape = _subgroup_shapes(result.signature, result.ell)
    hp_set, hq_set, hr_set = set(hp), set(hq), set(hr)
    scaling_subgroup = hp_set.intersection(hq_set).intersection(hr_set)
    orbit_count, orbit_sizes = _orbit_sizes(triples, scaling_subgroup, result.ell)
    sum_counts = _sum_counts(hp, hq, result.ell)
    sumset = set(sum_counts)
    additive_energy = sum(count * count for count in sum_counts.values())
    normalized_energy = additive_energy / (len(hp) * len(hq)) ** 2 if hp and hq else 0.0
    entropy, normalized_entropy = _entropy_for_triples(triples)
    swap_hits = sum(1 for u, v, w in triples if (v, u, w) in triple_set)
    swap_score = swap_hits / len(triples) if triples else 0.0
    orbit_compression = 1.0 - (orbit_count / len(triples)) if triples else 0.0
    concentration_values = (
        _max_marginal_share(triples, 0),
        _max_marginal_share(triples, 1),
        _max_marginal_share(triples, 2),
    )
    coset_concentration = max(concentration_values) if triples else 0.0
    compression_score = (1.0 - result.density) * (0.5 * coset_concentration + 0.5 * orbit_compression)
    fingerprint = (
        f"sizes={subgroup_size_shape}|density={result.density}|"
        f"orbits={orbit_count}|swap={round(swap_score, 4)}|"
        f"energy={round(normalized_energy, 4)}"
    )
    return UnitSurvivorGeometry(
        signature=result.signature,
        ell=result.ell,
        subgroup_gcd_shape=subgroup_gcd_shape,
        subgroup_size_shape=subgroup_size_shape,
        survivor_count=survivor_data.count,
        pair_count=survivor_data.pair_count,
        density=round(result.density, 10),
        survivor_triples=triples,
        coset_concentration=round(coset_concentration, 10),
        a_value_concentration=round(concentration_values[0], 10),
        b_value_concentration=round(concentration_values[1], 10),
        c_value_concentration=round(concentration_values[2], 10),
        common_scaling_subgroup_size=len(scaling_subgroup),
        orbit_count=orbit_count,
        orbit_size_multiset=orbit_sizes,
        orbit_compression=round(orbit_compression, 10),
        swap_symmetric=bool(triples) and swap_hits == len(triples),
        swap_symmetry_score=round(swap_score, 10),
        additive_energy=additive_energy,
        normalized_additive_energy=round(normalized_energy, 10),
        sumset_size=len(sumset),
        intersection_size_hp_hq_with_hr=len(sumset.intersection(hr_set)),
        survivor_entropy=entropy,
        normalized_survivor_entropy=normalized_entropy,
        survivor_compression_score=round(compression_score, 10),
        geometry_fingerprint=fingerprint,
    )


def analyze_sparse_unit_geometries(
    results: Iterable[ResidueSweepResult],
    classifications: Iterable[PrimitiveClassification],
) -> list[UnitSurvivorGeometry]:
    """Analyze geometry for rows classified as sparse unit survivors."""
    result_by_key = {(result.signature, result.ell): result for result in results}
    geometries: list[UnitSurvivorGeometry] = []
    for classification in classifications:
        if classification.classification != "sparse_unit_survivor":
            continue
        geometries.append(analyze_unit_survivor_geometry(result_by_key[(classification.signature, classification.ell)]))
    geometries.sort(key=lambda item: item.survivor_compression_score, reverse=True)
    return geometries
