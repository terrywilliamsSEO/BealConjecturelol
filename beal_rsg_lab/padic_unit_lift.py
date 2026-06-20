"""P-adic unit lift analysis for sparse unit-survivor rows."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from math import gcd, log2

from .number_theory import shannon_entropy
from .rsg_residue_engine import Signature, power_residue_set
from .unit_survivor_geometry import UnitSurvivorGeometry


@dataclass(frozen=True)
class PadicUnitLiftRecord:
    """Lift behavior of unit survivor triples through ell^2 and ell^3."""

    signature: Signature
    ell: int
    base_survivor_count: int
    ell2_lift_survival_count: int
    ell2_total_lift_count: int
    ell2_lift_branching_factor: float
    ell2_lift_entropy: float
    ell3_lift_survival_count: int
    ell3_total_lift_count: int
    ell3_lift_branching_factor: float
    ell3_lift_entropy: float
    unit_lift_status: str
    unit_lift_rigidity_score: float
    collapse_or_rigid: bool

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        return data


@lru_cache(maxsize=None)
def _grouped_power_residues(exponent: int, ell: int, power: int) -> tuple[tuple[int, tuple[int, ...]], ...]:
    modulus = ell**power
    grouped: dict[int, set[int]] = defaultdict(set)
    for residue in power_residue_set(exponent, modulus, include_zero=False, units_only=True):
        grouped[residue % ell].add(residue)
    return tuple(sorted((key, tuple(sorted(values))) for key, values in grouped.items()))


def _group_map(exponent: int, ell: int, power: int) -> dict[int, tuple[int, ...]]:
    return dict(_grouped_power_residues(exponent, ell, power))


def _branch_count_for_power(geometry: UnitSurvivorGeometry, power: int) -> tuple[int, int, tuple[int, ...]]:
    modulus = geometry.ell**power
    p, q, r = geometry.signature
    left = _group_map(p, geometry.ell, power)
    right = _group_map(q, geometry.ell, power)
    output = _group_map(r, geometry.ell, power)
    surviving_base_triples = 0
    total_lifts = 0
    branch_counts: list[int] = []

    for u, v, w in geometry.survivor_triples:
        left_values = left.get(u, ())
        right_values = right.get(v, ())
        output_values = set(output.get(w, ()))
        count = 0
        if left_values and right_values and output_values:
            if len(left_values) > len(right_values):
                first, second = right_values, left_values
            else:
                first, second = left_values, right_values
            for a in first:
                for b in second:
                    if (a + b) % modulus in output_values:
                        count += 1
        if count:
            surviving_base_triples += 1
            total_lifts += count
            branch_counts.append(count)
        else:
            branch_counts.append(0)
    return surviving_base_triples, total_lifts, tuple(branch_counts)


def _lift_entropy(branch_counts: tuple[int, ...]) -> float:
    positive = [count for count in branch_counts if count > 0]
    return round(shannon_entropy(positive), 10) if positive else 0.0


def analyze_padic_unit_lift(geometry: UnitSurvivorGeometry) -> PadicUnitLiftRecord:
    """Measure whether sparse unit geometry persists under ell^2 and ell^3 lifts."""
    ell2_survivors, ell2_lifts, ell2_branches = _branch_count_for_power(geometry, 2)
    ell3_survivors, ell3_lifts, ell3_branches = _branch_count_for_power(geometry, 3)
    base = max(1, geometry.survivor_count)
    ell2_branching = ell2_lifts / base
    ell3_branching = ell3_lifts / base

    expected_ell3_scale = geometry.ell * geometry.ell
    if ell2_survivors == 0:
        status = "collapses_mod_ell2"
    elif ell3_survivors == 0:
        status = "collapses_mod_ell3"
    elif ell3_branching < max(1.0, expected_ell3_scale / 8):
        status = "rigid_unit_lift"
    else:
        status = "persists_or_expands"

    rigidity_score = -log2(max(geometry.density, 1e-12))
    if status.startswith("collapses"):
        rigidity_score += 12.0
    elif status == "rigid_unit_lift":
        rigidity_score += 6.0
    else:
        rigidity_score += max(0.0, 4.0 - log2(max(1.0, ell3_branching / max(1.0, expected_ell3_scale))))

    return PadicUnitLiftRecord(
        signature=geometry.signature,
        ell=geometry.ell,
        base_survivor_count=geometry.survivor_count,
        ell2_lift_survival_count=ell2_survivors,
        ell2_total_lift_count=ell2_lifts,
        ell2_lift_branching_factor=round(ell2_branching, 10),
        ell2_lift_entropy=_lift_entropy(ell2_branches),
        ell3_lift_survival_count=ell3_survivors,
        ell3_total_lift_count=ell3_lifts,
        ell3_lift_branching_factor=round(ell3_branching, 10),
        ell3_lift_entropy=_lift_entropy(ell3_branches),
        unit_lift_status=status,
        unit_lift_rigidity_score=round(rigidity_score, 10),
        collapse_or_rigid=status in {"collapses_mod_ell2", "collapses_mod_ell3", "rigid_unit_lift"},
    )


def analyze_padic_unit_lifts(geometries: list[UnitSurvivorGeometry]) -> list[PadicUnitLiftRecord]:
    """Analyze p-adic unit lifts for sparse geometries."""
    records = [analyze_padic_unit_lift(geometry) for geometry in geometries]
    records.sort(key=lambda item: (item.collapse_or_rigid, item.unit_lift_rigidity_score), reverse=True)
    return records
