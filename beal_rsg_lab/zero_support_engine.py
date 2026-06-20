"""Exact zero-support analysis for local power-residue solutions."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from math import gcd
from typing import Iterable

from .rsg_residue_engine import ResidueSweepResult, Signature, power_residue_set

VARIABLES: tuple[str, str, str] = ("A", "B", "C")
ZERO_MASK_ORDER: tuple[str, ...] = ("none", "A_only", "B_only", "C_only", "AB", "AC", "BC", "ABC")
MASK_VARIABLES: dict[str, tuple[str, ...]] = {
    "none": (),
    "A_only": ("A",),
    "B_only": ("B",),
    "C_only": ("C",),
    "AB": ("A", "B"),
    "AC": ("A", "C"),
    "BC": ("B", "C"),
    "ABC": ("A", "B", "C"),
}


@dataclass(frozen=True)
class ZeroSupportRecord:
    """Exact zero-support data for one signature/prime row."""

    signature: Signature
    ell: int
    subgroup_gcd_shape: tuple[int, int, int]
    subgroup_size_shape: tuple[int, int, int]
    nonzero_survivor_count: int
    zero_adjoined_survivor_count: int
    zero_mask_counts: dict[str, int]
    occurring_zero_masks: tuple[str, ...]
    forced_zero_masks: tuple[str, ...]
    minimum_zero_support_size: int
    dominant_zero_mask: str
    dominant_zero_mask_count: int
    variable_forced_zero_if_any: tuple[str, ...]
    exact_single_variable_mask: str
    zero_support_fingerprint: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["subgroup_gcd_shape"] = "-".join(str(part) for part in self.subgroup_gcd_shape)
        data["subgroup_size_shape"] = "-".join(str(part) for part in self.subgroup_size_shape)
        data["zero_mask_counts"] = ";".join(
            f"{mask}:{self.zero_mask_counts.get(mask, 0)}" for mask in ZERO_MASK_ORDER
        )
        data["occurring_zero_masks"] = ";".join(self.occurring_zero_masks)
        data["forced_zero_masks"] = ";".join(self.forced_zero_masks)
        data["variable_forced_zero_if_any"] = ";".join(self.variable_forced_zero_if_any)
        return data


def zero_mask_for_values(u: int, v: int, w: int) -> str:
    """Return the zero-support mask for a residue triple."""
    variables = tuple(name for name, value in zip(VARIABLES, (u, v, w)) if value == 0)
    if not variables:
        return "none"
    if len(variables) == 1:
        return f"{variables[0]}_only"
    return "".join(variables)


def zero_support_size(mask: str) -> int:
    """Return number of variables forced zero by a mask."""
    return len(MASK_VARIABLES[mask])


def _common_forced_variables(masks: Iterable[str]) -> tuple[str, ...]:
    mask_list = list(masks)
    if not mask_list:
        return ()
    common = set(MASK_VARIABLES[mask_list[0]])
    for mask in mask_list[1:]:
        common.intersection_update(MASK_VARIABLES[mask])
    return tuple(variable for variable in VARIABLES if variable in common)


def subgroup_shapes(signature: Signature, ell: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """Return gcd kernel shape and actual power-subgroup sizes modulo ell."""
    gcd_shape = tuple(gcd(exponent, ell - 1) for exponent in signature)
    size_shape = tuple((ell - 1) // value for value in gcd_shape)
    return gcd_shape, size_shape


def analyze_zero_support(signature: Signature, ell: int) -> ZeroSupportRecord:
    """Enumerate zero-adjoined local power-residue solutions and classify masks."""
    p, q, r = signature
    left = power_residue_set(p, ell, include_zero=True, units_only=False)
    right = power_residue_set(q, ell, include_zero=True, units_only=False)
    output = set(power_residue_set(r, ell, include_zero=True, units_only=False))

    counts: Counter[str] = Counter()
    for u in left:
        for v in right:
            w = (u + v) % ell
            if w in output:
                counts[zero_mask_for_values(u, v, w)] += 1

    total = sum(counts.values())
    occurring = tuple(mask for mask in ZERO_MASK_ORDER if counts.get(mask, 0) > 0)
    nonzero = counts.get("none", 0)
    forced = tuple(mask for mask in occurring if mask != "none") if nonzero == 0 else ()
    min_support = min((zero_support_size(mask) for mask in occurring), default=0)
    dominant = max(occurring, key=lambda mask: (counts[mask], -zero_support_size(mask))) if occurring else "none"
    common_variables = _common_forced_variables(occurring)

    exact_single = ""
    single_masks = {"A_only", "B_only", "C_only"}
    if len(occurring) == 1 and occurring[0] in single_masks:
        exact_single = occurring[0]

    gcd_shape, size_shape = subgroup_shapes(signature, ell)
    fingerprint = (
        f"sizes={size_shape}|min_zero={min_support}|"
        f"masks={','.join(occurring)}|common={','.join(common_variables) or 'none'}"
    )
    return ZeroSupportRecord(
        signature=signature,
        ell=ell,
        subgroup_gcd_shape=gcd_shape,
        subgroup_size_shape=size_shape,
        nonzero_survivor_count=nonzero,
        zero_adjoined_survivor_count=total,
        zero_mask_counts={mask: counts.get(mask, 0) for mask in ZERO_MASK_ORDER},
        occurring_zero_masks=occurring,
        forced_zero_masks=forced,
        minimum_zero_support_size=min_support,
        dominant_zero_mask=dominant,
        dominant_zero_mask_count=counts.get(dominant, 0),
        variable_forced_zero_if_any=common_variables,
        exact_single_variable_mask=exact_single,
        zero_support_fingerprint=fingerprint,
    )


def analyze_zero_support_results(results: Iterable[ResidueSweepResult]) -> list[ZeroSupportRecord]:
    """Analyze zero support in the same order as residue results."""
    return [analyze_zero_support(result.signature, result.ell) for result in results]
