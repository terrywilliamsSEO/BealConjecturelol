"""Valuation-mask lift audit for nonunit `(5,4,5)` local cases."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .local_valuation_case_545 import LocalValuationCaseRecord


@dataclass(frozen=True)
class ValuationMaskLiftRecord:
    """Expected q-adic lift behavior for one valuation mask."""

    signature: str
    prime: int
    valuation_mask: str
    base_classification: str
    lift_to_q2_status: str
    lift_to_q3_status: str
    lift_classification: str
    divisibility_strengthens: bool
    method: str
    notes: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _lift_for_case(row: LocalValuationCaseRecord) -> tuple[str, str, str, bool, str, str]:
    if row.classification == "impossible_mod_q":
        return "not_applicable", "not_applicable", "impossible_mod_q", False, "mod_q_classification", row.reason
    if row.classification == "primitive_forbidden":
        return "not_applicable", "not_applicable", "primitive_forbidden", False, "primitivity", row.reason
    if row.valuation_mask == "unit":
        return (
            "unit_case_stable",
            "unit_case_stable",
            "valuation_stable",
            False,
            "existing_unit_trace_enumeration",
            "Unit cases stay inside the current good-prime trace enumeration.",
        )
    return (
        "hensel_stable_expected",
        "hensel_stable_expected",
        "valuation_stable",
        False,
        "unit_partial_derivative",
        "For selected good primes q != 2,5, a unit derivative in one nonzero variable gives stable single-mask lifts; this is a routing audit, not a replacement for a hand lemma.",
    )


def build_valuation_mask_lifts_545(
    valuation_rows: Iterable[LocalValuationCaseRecord],
) -> list[ValuationMaskLiftRecord]:
    """Classify expected lift behavior for every valuation mask."""
    records: list[ValuationMaskLiftRecord] = []
    for row in sorted(valuation_rows, key=lambda item: (item.prime, item.valuation_mask)):
        q2, q3, lift_class, strengthens, method, notes = _lift_for_case(row)
        records.append(
            ValuationMaskLiftRecord(
                signature=row.signature,
                prime=row.prime,
                valuation_mask=row.valuation_mask,
                base_classification=row.classification,
                lift_to_q2_status=q2,
                lift_to_q3_status=q3,
                lift_classification=lift_class,
                divisibility_strengthens=strengthens,
                method=method,
                notes=notes,
            )
        )
    return records
