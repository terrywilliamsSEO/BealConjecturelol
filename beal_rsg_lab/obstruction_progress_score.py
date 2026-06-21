"""Progress scoring for focused good-prime trace audits."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .trace_congruence_filter_545 import TraceCongruenceFilterRecord


@dataclass(frozen=True)
class ObstructionProgressRecord:
    """Aggregate status for the focused `(5,4,5)` trace-filter attempt."""

    signature: str
    good_primes_checked: int
    newform_count: int
    usable_comparison_count: int
    coefficient_field_unclear_count: int
    insufficient_data_count: int
    newforms_surviving_all_filters: int
    eliminated_newforms: int
    first_elimination_primes: str
    unresolved_reasons: str
    progress_label: str
    confidence_score: float
    route_ceiling_label: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def score_obstruction_progress_545(
    filter_rows: Iterable[TraceCongruenceFilterRecord],
    *,
    newform_count: int,
) -> ObstructionProgressRecord:
    """Score good-prime filtering progress without making theorem claims."""
    rows = list(filter_rows)
    primes = sorted({row.prime for row in rows})
    usable_count = sum(1 for row in rows if row.filter_classification in {"survives", "eliminated"})
    unclear_count = sum(1 for row in rows if row.filter_classification == "coefficient_field_unclear")
    insufficient_count = sum(1 for row in rows if row.filter_classification == "insufficient_data")
    by_newform: dict[int, list[TraceCongruenceFilterRecord]] = {}
    for row in rows:
        by_newform.setdefault(row.newform_index, []).append(row)
    surviving = 0
    eliminated = 0
    first_eliminations: list[str] = []
    unresolved: list[str] = []
    for index in range(newform_count):
        newform_rows = sorted(by_newform.get(index, []), key=lambda row: row.prime)
        first_eliminated = next((row for row in newform_rows if row.filter_classification == "eliminated"), None)
        if first_eliminated is not None:
            eliminated += 1
            first_eliminations.append(f"newform_{index}:q={first_eliminated.prime}")
            continue
        if newform_rows and all(row.filter_classification == "survives" for row in newform_rows):
            surviving += 1
            continue
        if any(row.filter_classification == "coefficient_field_unclear" for row in newform_rows):
            unresolved.append(f"newform_{index}:coefficient_field_unclear")
            surviving += 1
        elif any(row.filter_classification in {"insufficient_data", "bad_comparison_mode"} for row in newform_rows) or not newform_rows:
            unresolved.append(f"newform_{index}:insufficient_or_unclear_trace_data")
            surviving += 1
        else:
            surviving += 1
    if unclear_count:
        label = "coefficient_field_blocked"
    elif unresolved:
        label = "trace_data_insufficient"
    elif eliminated == newform_count and newform_count > 0:
        label = "trace_mismatch_candidate"
    elif surviving:
        label = "trace_survivor_exists"
    else:
        label = "trace_data_insufficient"
    resolved_fraction = 0.0 if newform_count == 0 else eliminated / newform_count
    confidence = min(7.25, round(2.0 + len(primes) * 0.05 + resolved_fraction * 3.0, 10))
    return ObstructionProgressRecord(
        signature="5-4-5",
        good_primes_checked=len(primes),
        newform_count=newform_count,
        usable_comparison_count=usable_count,
        coefficient_field_unclear_count=unclear_count,
        insufficient_data_count=insufficient_count,
        newforms_surviving_all_filters=surviving,
        eliminated_newforms=eliminated,
        first_elimination_primes=";".join(first_eliminations),
        unresolved_reasons=";".join(unresolved),
        progress_label=label,
        confidence_score=confidence,
        route_ceiling_label="worth_human_modular_review",
    )
