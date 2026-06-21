"""Local valuation/reduction gap summary for `(5,4,5)`."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .trace_filter_case_coverage_545 import TraceFilterCaseCoverageRecord


@dataclass(frozen=True)
class LocalGapSummaryRecord:
    """Aggregate local coverage status for the focused route."""

    signature: str
    good_primes_checked: int
    unit_only_coverage_count: int
    nonunit_cases_resolved_count: int
    unresolved_count: int
    eliminating_prime_count: int
    eliminating_prime_full_coverage_count: int
    eliminating_primes: str
    full_coverage_eliminating_primes: str
    any_eliminating_prime_has_full_local_coverage: bool
    trace_mismatch_scope_label: str
    overall_local_gap_label: str
    exact_next_human_lemma: str
    route_ceiling_label: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def build_local_gap_summary_545(
    coverage_rows: Iterable[TraceFilterCaseCoverageRecord],
) -> LocalGapSummaryRecord:
    """Aggregate local valuation coverage for the trace mismatch."""
    rows = list(coverage_rows)
    eliminating = [row for row in rows if row.trace_filter_eliminates_newform_count > 0]
    full_eliminating = [row for row in eliminating if row.full_local_coverage]
    unresolved = [
        row
        for row in rows
        if row.coverage_label in {"bad_reduction_requires_separate_argument", "nonunit_cases_unresolved"}
    ]
    if full_eliminating:
        scope = "local_trace_mismatch_candidate"
    elif eliminating:
        scope = "unit_only_trace_mismatch_candidate"
    else:
        scope = "unit_only_trace_filter"
    overall = "local_coverage_gap" if unresolved else scope
    lemma = (
        "Local valuation and reduction case split for q | ABC: prove that each single-divisibility mask either cannot occur "
        "for primitive solutions at the eliminating primes, or gives a separate modular/reduction argument compatible with the trace filter."
    )
    return LocalGapSummaryRecord(
        signature="5-4-5",
        good_primes_checked=len(rows),
        unit_only_coverage_count=sum(
            1
            for row in rows
            if row.coverage_label in {"unit_only_trace_filter", "bad_reduction_requires_separate_argument"}
        ),
        nonunit_cases_resolved_count=sum(1 for row in rows if row.coverage_label == "nonunit_cases_resolved"),
        unresolved_count=len(unresolved),
        eliminating_prime_count=len(eliminating),
        eliminating_prime_full_coverage_count=len(full_eliminating),
        eliminating_primes=";".join(str(row.prime) for row in eliminating),
        full_coverage_eliminating_primes=";".join(str(row.prime) for row in full_eliminating),
        any_eliminating_prime_has_full_local_coverage=bool(full_eliminating),
        trace_mismatch_scope_label=scope,
        overall_local_gap_label=overall,
        exact_next_human_lemma=lemma,
        route_ceiling_label="worth_human_modular_review",
    )


def local_gap_summary_markdown(row: LocalGapSummaryRecord) -> str:
    """Render a Markdown local gap summary."""
    lines = [
        "# Local Gap Summary For `(5,4,5)`",
        "",
        "This summary asks whether the current trace mismatch is globally applicable at any eliminating good prime or remains a unit-case signal.",
        "",
        f"- Good primes checked: `{row.good_primes_checked}`.",
        f"- Unit-only coverage count: `{row.unit_only_coverage_count}`.",
        f"- Nonunit cases resolved count: `{row.nonunit_cases_resolved_count}`.",
        f"- Still unresolved count: `{row.unresolved_count}`.",
        f"- Eliminating primes: `{row.eliminating_primes or 'none'}`.",
        f"- Full-coverage eliminating primes: `{row.full_coverage_eliminating_primes or 'none'}`.",
        f"- Any eliminating prime has full local coverage: `{row.any_eliminating_prime_has_full_local_coverage}`.",
        f"- Trace mismatch scope label: `{row.trace_mismatch_scope_label}`.",
        f"- Overall local gap label: `{row.overall_local_gap_label}`.",
        f"- Route ceiling: `{row.route_ceiling_label}`.",
        "",
        "## Exact Next Human Lemma",
        "",
        row.exact_next_human_lemma,
        "",
        "Until that lemma is supplied, the trace mismatch should be read as route evidence with a local valuation coverage gap.",
        "",
    ]
    return "\n".join(lines)
