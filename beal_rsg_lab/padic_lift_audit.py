"""Conservative p-adic lift audit for mandatory single-divisor rows."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache

from .primitive_obstruction_classifier import PrimitiveClassification
from .rsg_residue_engine import Signature, power_residue_set


@dataclass(frozen=True)
class PadicLiftAudit:
    """Lift audit for a mandatory single-divisor row."""

    signature: Signature
    ell: int
    forced_variable: str
    ell2_lift_count: int
    ell3_lift_count: int
    same_variable_forced_ell2: bool
    same_variable_forced_ell3: bool
    exact_valuation_one_supported_ell2: bool
    exact_valuation_one_supported_ell3: bool
    valuation_growth_estimate: str
    descent_like_lift: bool
    notes: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        return data


@lru_cache(maxsize=None)
def _unit_power_set(exponent: int, modulus: int) -> tuple[int, ...]:
    return power_residue_set(exponent, modulus, include_zero=False, units_only=True)


def _negation_pair_count(left: tuple[int, ...], right: tuple[int, ...], modulus: int) -> int:
    right_set = set(right)
    return sum(1 for value in left if (-value) % modulus in right_set)


def _single_mask_lift_count(signature: Signature, ell: int, forced_variable: str, power: int) -> int:
    """Count residue-power lifts preserving an exact one-variable zero mask."""
    modulus = ell**power
    p, q, r = signature
    left = _unit_power_set(p, modulus)
    right = _unit_power_set(q, modulus)
    output = _unit_power_set(r, modulus)

    if forced_variable == "A":
        return len(set(right).intersection(output))
    if forced_variable == "B":
        return len(set(left).intersection(output))
    if forced_variable == "C":
        return _negation_pair_count(left, right, modulus)
    raise ValueError(f"unknown forced variable {forced_variable}")


def audit_padic_lift(classification: PrimitiveClassification) -> PadicLiftAudit:
    """Audit one mandatory single-divisor classification through ell^3."""
    if classification.classification != "mandatory_single_divisor":
        raise ValueError("p-adic lift audit only applies to mandatory_single_divisor rows")

    ell2_count = _single_mask_lift_count(classification.signature, classification.ell, classification.forced_variable, 2)
    ell3_count = _single_mask_lift_count(classification.signature, classification.ell, classification.forced_variable, 3)
    exponent_by_variable = dict(zip(("A", "B", "C"), classification.signature))
    forced_exponent = exponent_by_variable[classification.forced_variable]
    exact_v1_ell2 = ell2_count > 0 and forced_exponent >= 2
    exact_v1_ell3 = ell3_count > 0 and forced_exponent >= 3

    if ell2_count == 0:
        estimate = "branch_dies_mod_ell2"
        descent = True
    elif ell3_count == 0:
        estimate = "branch_dies_mod_ell3"
        descent = True
    elif exact_v1_ell3:
        estimate = "no_growth_detected_through_ell3"
        descent = False
    else:
        estimate = "needs_higher_order_lte"
        descent = False

    notes = (
        "For exponents greater than 2, a variable divisible exactly once by ell "
        "already contributes 0 modulo ell^3. Growth beyond v_ell=1 is therefore "
        "not detectable from power-residue lifts through ell^3 unless the branch dies."
    )
    return PadicLiftAudit(
        signature=classification.signature,
        ell=classification.ell,
        forced_variable=classification.forced_variable,
        ell2_lift_count=ell2_count,
        ell3_lift_count=ell3_count,
        same_variable_forced_ell2=ell2_count > 0,
        same_variable_forced_ell3=ell3_count > 0,
        exact_valuation_one_supported_ell2=exact_v1_ell2,
        exact_valuation_one_supported_ell3=exact_v1_ell3,
        valuation_growth_estimate=estimate,
        descent_like_lift=descent,
        notes=notes,
    )


def audit_padic_lifts(classifications: list[PrimitiveClassification]) -> list[PadicLiftAudit]:
    """Audit every mandatory single-divisor row."""
    audits = [
        audit_padic_lift(classification)
        for classification in classifications
        if classification.classification == "mandatory_single_divisor"
    ]
    audits.sort(key=lambda item: (item.descent_like_lift, item.ell3_lift_count), reverse=True)
    return audits
