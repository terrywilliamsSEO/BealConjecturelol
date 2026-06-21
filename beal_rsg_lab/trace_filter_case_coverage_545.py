"""Combine trace-filter eliminations with valuation/reduction case coverage."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .frey_reduction_case_router_545 import FreyReductionCaseRecord
from .local_case_closure_score_545 import LocalCaseClosureScoreRecord
from .single_mask_newform_pressure_545 import SingleMaskNewformPressureRecord
from .trace_congruence_filter_545 import TraceCongruenceFilterRecord


@dataclass(frozen=True)
class TraceFilterCaseCoverageRecord:
    """Case-coverage summary for one good prime."""

    signature: str
    prime: int
    trace_filter_eliminates_newform_count: int
    trace_filter_survives_newform_count: int
    nonunit_locally_possible_count: int
    nonunit_resolved_count: int
    nonunit_unresolved_count: int
    full_local_coverage: bool
    supports_stronger_local_trace_candidate: bool
    coverage_label: str
    reason: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def build_trace_filter_case_coverage_545(
    filter_rows: Iterable[TraceCongruenceFilterRecord],
    reduction_rows: Iterable[FreyReductionCaseRecord],
    *,
    pressure_rows: Iterable[SingleMaskNewformPressureRecord] = (),
    closure_rows: Iterable[LocalCaseClosureScoreRecord] = (),
) -> list[TraceFilterCaseCoverageRecord]:
    """Summarize whether each q-filter is unit-only or locally global."""
    filters_by_prime: dict[int, list[TraceCongruenceFilterRecord]] = {}
    for row in filter_rows:
        filters_by_prime.setdefault(row.prime, []).append(row)
    reductions_by_prime: dict[int, list[FreyReductionCaseRecord]] = {}
    for row in reduction_rows:
        reductions_by_prime.setdefault(row.prime, []).append(row)
    pressure_by_prime: dict[int, list[SingleMaskNewformPressureRecord]] = {}
    for row in pressure_rows:
        pressure_by_prime.setdefault(row.prime, []).append(row)
    closure_by_prime = {row.prime: row for row in closure_rows}
    records: list[TraceFilterCaseCoverageRecord] = []
    for prime in sorted(set(filters_by_prime) | set(reductions_by_prime)):
        trace_rows = filters_by_prime.get(prime, [])
        reductions = reductions_by_prime.get(prime, [])
        pressure = pressure_by_prime.get(prime, [])
        eliminated = sum(1 for row in trace_rows if row.filter_classification == "eliminated")
        survived = sum(1 for row in trace_rows if row.filter_classification == "survives")
        nonunit_possible = [
            row
            for row in reductions
            if row.valuation_mask != "unit" and row.valuation_classification == "locally_possible"
        ]
        if pressure:
            resolved_masks = {row.valuation_mask for row in pressure if row.single_mask_resolved}
            unresolved_masks = {
                row.valuation_mask
                for row in pressure
                if row.branch_classification in {"needs_human_tate_algorithm", "unresolved_single_mask"}
            }
            nonunit_unresolved = [
                row
                for row in nonunit_possible
                if row.valuation_mask in unresolved_masks or row.valuation_mask not in resolved_masks
            ]
        else:
            nonunit_unresolved = [
                row
                for row in nonunit_possible
                if row.separate_argument_required or not row.current_trace_comparison_applies
            ]
        nonunit_resolved = len(nonunit_possible) - len(nonunit_unresolved)
        full = not nonunit_unresolved
        closure = closure_by_prime.get(prime)
        if closure is not None:
            full = closure.closure_label == "local_case_elimination_candidate"
            if closure.closure_label == "local_case_elimination_candidate":
                label = "local_case_elimination_candidate"
            elif closure.closure_label == "level_lowering_assumption_required":
                label = "level_lowering_assumption_required"
            else:
                label = "local_coverage_gap"
            reason = closure.reason
        elif eliminated and full and pressure:
            label = "local_case_elimination_candidate"
            reason = "The trace filter eliminates at least one newform and the focused single masks are classified by the reduction diagnostic layer."
        elif eliminated and full:
            label = "globally_applicable_trace_filter"
            reason = "The trace filter eliminates at least one newform and all nonunit masks are resolved."
        elif nonunit_unresolved:
            label = "bad_reduction_requires_separate_argument"
            reason = "At least one locally possible nonunit mask gives singular or non-good reduction outside the current trace comparison."
        elif nonunit_possible and nonunit_resolved == len(nonunit_possible):
            label = "nonunit_cases_resolved"
            reason = "Nonunit cases are locally possible but resolved by the current routing."
        elif trace_rows:
            label = "unit_only_trace_filter"
            reason = "The current trace comparison applies to unit cases only."
        else:
            label = "nonunit_cases_unresolved"
            reason = "No trace rows are available for this prime."
        records.append(
            TraceFilterCaseCoverageRecord(
                signature="5-4-5",
                prime=prime,
                trace_filter_eliminates_newform_count=eliminated,
                trace_filter_survives_newform_count=survived,
                nonunit_locally_possible_count=len(nonunit_possible),
                nonunit_resolved_count=nonunit_resolved,
                nonunit_unresolved_count=len(nonunit_unresolved),
                full_local_coverage=full,
                supports_stronger_local_trace_candidate=bool(eliminated and full),
                coverage_label=label,
                reason=reason,
            )
        )
    return records
