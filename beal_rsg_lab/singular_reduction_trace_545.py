"""Focused Frey-reduction routing for nonunit `(5,4,5)` branches."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .nonunit_elimination_545 import NonunitEliminationRecord


@dataclass(frozen=True)
class SingularReductionTraceRecord:
    """Expected reduction behavior for one q=13 or q=17 nonunit branch."""

    signature: str
    prime: int
    valuation_mask: str
    branch_label: str
    frey_reduction_classification: str
    current_trace_comparison_applies: bool
    needs_human_reduction_argument: bool
    reason: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _classify_reduction(row: NonunitEliminationRecord) -> tuple[str, bool, bool, str]:
    if row.primitive_forbidden:
        return (
            "template_unknown",
            False,
            False,
            "This branch is excluded by primitivity before the Frey reduction type is needed.",
        )
    if not row.possible_mod_q:
        return "template_unknown", False, False, "This branch has no mod-q local solution."
    if row.valuation_mask in {"A_only", "B_only", "C_only"}:
        return (
            "needs_human_reduction_argument",
            False,
            True,
            (
                "The branch is locally stable but makes the current Frey template singular or non-good modulo q; "
                "a hand minimal-model/reduction argument must decide whether it is multiplicative, additive, "
                "or otherwise compatible with the trace filter."
            ),
        )
    return (
        "template_unknown",
        False,
        True,
        "The current focused audit has no certified reduction classification for this nonunit branch.",
    )


def build_singular_reduction_traces_545(
    nonunit_rows: Iterable[NonunitEliminationRecord],
) -> list[SingularReductionTraceRecord]:
    """Classify the Frey-reduction status for focused nonunit branches."""
    records: list[SingularReductionTraceRecord] = []
    for row in sorted(nonunit_rows, key=lambda item: (item.prime, item.valuation_mask)):
        reduction, applies, needs_argument, reason = _classify_reduction(row)
        records.append(
            SingularReductionTraceRecord(
                signature=row.signature,
                prime=row.prime,
                valuation_mask=row.valuation_mask,
                branch_label=row.branch_label,
                frey_reduction_classification=reduction,
                current_trace_comparison_applies=applies,
                needs_human_reduction_argument=needs_argument,
                reason=reason,
            )
        )
    return records
