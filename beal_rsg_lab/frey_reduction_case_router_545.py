"""Route valuation masks to expected Frey reduction cases for `(5,4,5)`."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .local_valuation_case_545 import LocalValuationCaseRecord
from .valuation_mask_lift_545 import ValuationMaskLiftRecord


@dataclass(frozen=True)
class FreyReductionCaseRecord:
    """Expected Frey-template reduction for one valuation mask."""

    signature: str
    prime: int
    valuation_mask: str
    valuation_classification: str
    lift_classification: str
    expected_reduction: str
    current_trace_comparison_applies: bool
    separate_argument_required: bool
    reason: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _reduction_for_mask(row: LocalValuationCaseRecord, lift: ValuationMaskLiftRecord | None) -> tuple[str, bool, bool, str]:
    if row.classification == "impossible_mod_q":
        return "template_unknown", False, False, "The valuation mask is impossible modulo q."
    if row.classification == "primitive_forbidden":
        return "template_unknown", False, False, "The valuation mask is excluded by primitivity before trace comparison."
    if row.valuation_mask == "unit":
        return "good_reduction", True, False, "A,B,C are units and the current good-prime trace filter applies."
    return (
        "singular_reduction",
        False,
        True,
        "A single variable is zero modulo q, causing repeated roots in E: y^2=x(x-A^5)(x+B^4); this needs a separate local reduction argument.",
    )


def build_frey_reduction_cases_545(
    valuation_rows: Iterable[LocalValuationCaseRecord],
    lift_rows: Iterable[ValuationMaskLiftRecord],
) -> list[FreyReductionCaseRecord]:
    """Classify expected Frey-template reduction for every valuation mask."""
    lift_by_key = {(row.prime, row.valuation_mask): row for row in lift_rows}
    records: list[FreyReductionCaseRecord] = []
    for row in sorted(valuation_rows, key=lambda item: (item.prime, item.valuation_mask)):
        lift = lift_by_key.get((row.prime, row.valuation_mask))
        reduction, applies, separate, reason = _reduction_for_mask(row, lift)
        records.append(
            FreyReductionCaseRecord(
                signature=row.signature,
                prime=row.prime,
                valuation_mask=row.valuation_mask,
                valuation_classification=row.classification,
                lift_classification=lift.lift_classification if lift else "valuation_lift_gap",
                expected_reduction=reduction,
                current_trace_comparison_applies=applies,
                separate_argument_required=separate,
                reason=reason,
            )
        )
    return records
