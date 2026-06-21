"""Best focused route summary for `(5,4,5)`."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .cross_prime_branch_compatibility_545 import CrossPrimeBranchCompatibilityRecord
from .local_case_closure_score_545 import LocalCaseClosureScoreRecord
from .q3_exceptionality_audit_545 import Q3ExceptionalityAuditRecord


SAFE_BEST_ROUTE_LABELS_545 = {
    "cross_prime_elimination_candidate",
    "q3_dependent_local_case_candidate",
    "q3_single_prime_local_case_candidate",
    "partial_closure_route",
    "survivor_route",
    "branch_data_insufficient",
    "level_lowering_assumption_required",
    "local_coverage_gap",
}


@dataclass(frozen=True)
class BestRouteSummaryRecord:
    """One ranked focused route option."""

    signature: str
    rank: int
    route_option: str
    route_label: str
    supporting_primes: str
    unit_survivor_count: int
    single_mask_survivor_count: int
    q3_reliance_penalty: int
    human_review_priority: int
    route_ceiling_label: str
    reason: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _aggregate_cross_label(rows: list[CrossPrimeBranchCompatibilityRecord]) -> str:
    for row in rows:
        if row.newform_index == -1:
            return row.compatibility_label
    return "branch_data_insufficient"


def _closure_by_prime(rows: Iterable[LocalCaseClosureScoreRecord]) -> dict[int, LocalCaseClosureScoreRecord]:
    return {row.prime: row for row in rows}


def _safe_label(label: str) -> str:
    return label if label in SAFE_BEST_ROUTE_LABELS_545 else "local_coverage_gap"


def build_best_route_summary_545(
    closure_rows: Iterable[LocalCaseClosureScoreRecord],
    cross_prime_rows: Iterable[CrossPrimeBranchCompatibilityRecord],
    q3_audit: Q3ExceptionalityAuditRecord,
) -> list[BestRouteSummaryRecord]:
    """Rank focused route options after q=3 and non-q=3 compatibility audits."""
    closures = _closure_by_prime(closure_rows)
    cross_rows = list(cross_prime_rows)
    cross_label = _aggregate_cross_label(cross_rows)
    q3 = closures.get(3)
    q3_closes = q3 is not None and q3.closure_label == "local_case_elimination_candidate"
    non_q3_closes = cross_label == "cross_prime_elimination_candidate"
    if cross_label == "level_lowering_assumption_required":
        cross_route_label = "level_lowering_assumption_required"
    elif cross_label == "branch_data_insufficient":
        cross_route_label = "branch_data_insufficient"
    elif non_q3_closes:
        cross_route_label = "cross_prime_elimination_candidate"
    else:
        cross_route_label = "local_coverage_gap"
    q3_label = (
        "q3_dependent_local_case_candidate"
        if q3_closes and not non_q3_closes
        else ("q3_single_prime_local_case_candidate" if q3_closes else "local_coverage_gap")
    )
    q17_q41 = [closures.get(17), closures.get(41)]
    q13_q61 = [closures.get(13), closures.get(61)]
    partial_unit = sum(row.unit_surviving_branch_count for row in q17_q41 if row is not None)
    partial_single = sum(row.single_mask_surviving_branches for row in q17_q41 if row is not None)
    survivor_unit = sum(row.unit_surviving_branch_count for row in q13_q61 if row is not None)
    survivor_single = sum(row.single_mask_surviving_branches for row in q13_q61 if row is not None)
    rows = [
        BestRouteSummaryRecord(
            signature="5-4-5",
            rank=0,
            route_option="non_q3_cross_prime_closure",
            route_label=_safe_label(cross_route_label),
            supporting_primes="13;17;41;61",
            unit_survivor_count=0,
            single_mask_survivor_count=0,
            q3_reliance_penalty=0,
            human_review_priority=0,
            route_ceiling_label="worth_human_modular_review",
            reason=(
                "The non-q=3 focused primes jointly eliminate every tracked newform branch assignment."
                if non_q3_closes
                else "The non-q=3 focused primes do not yet jointly close every tracked branch assignment."
            ),
        ),
        BestRouteSummaryRecord(
            signature="5-4-5",
            rank=0,
            route_option="q3_single_prime_closure",
            route_label=_safe_label(q3_label),
            supporting_primes="3",
            unit_survivor_count=q3.unit_surviving_branch_count if q3 else 0,
            single_mask_survivor_count=q3.single_mask_surviving_branches if q3 else 0,
            q3_reliance_penalty=q3_audit.q3_reliance_penalty,
            human_review_priority=0,
            route_ceiling_label="worth_human_modular_review",
            reason=q3_audit.reason,
        ),
        BestRouteSummaryRecord(
            signature="5-4-5",
            rank=0,
            route_option="q17_q41_partial_closure",
            route_label="partial_closure_route",
            supporting_primes="17;41",
            unit_survivor_count=partial_unit,
            single_mask_survivor_count=partial_single,
            q3_reliance_penalty=0,
            human_review_priority=0,
            route_ceiling_label="worth_human_modular_review",
            reason="q=17 and q=41 close the single-mask multiplicative branches but retain unit-branch survivors.",
        ),
        BestRouteSummaryRecord(
            signature="5-4-5",
            rank=0,
            route_option="q13_q61_survivor_routes",
            route_label="survivor_route",
            supporting_primes="13;61",
            unit_survivor_count=survivor_unit,
            single_mask_survivor_count=survivor_single,
            q3_reliance_penalty=0,
            human_review_priority=0,
            route_ceiling_label="worth_human_modular_review",
            reason="q=13 and q=61 retain single-mask multiplicative survivors in the current audit.",
        ),
    ]
    def rank_key(row: BestRouteSummaryRecord) -> tuple[int, int, int, int]:
        label_priority = {
            "cross_prime_elimination_candidate": 0,
            "q3_dependent_local_case_candidate": 1,
            "q3_single_prime_local_case_candidate": 2,
            "partial_closure_route": 3,
            "survivor_route": 4,
            "branch_data_insufficient": 5,
            "level_lowering_assumption_required": 6,
            "local_coverage_gap": 7,
        }
        return (
            label_priority.get(row.route_label, 8),
            row.q3_reliance_penalty,
            row.unit_survivor_count + row.single_mask_survivor_count,
            row.supporting_primes.count(";"),
        )
    ranked = sorted(rows, key=rank_key)
    return [
        BestRouteSummaryRecord(
            signature=row.signature,
            rank=index,
            route_option=row.route_option,
            route_label=row.route_label,
            supporting_primes=row.supporting_primes,
            unit_survivor_count=row.unit_survivor_count,
            single_mask_survivor_count=row.single_mask_survivor_count,
            q3_reliance_penalty=row.q3_reliance_penalty,
            human_review_priority=index,
            route_ceiling_label=row.route_ceiling_label,
            reason=row.reason,
        )
        for index, row in enumerate(ranked, 1)
    ]


def best_route_summary_545_markdown(rows: Iterable[BestRouteSummaryRecord]) -> str:
    """Render `BEST_ROUTE_SUMMARY_545.md`."""
    row_list = list(rows)
    top_label = row_list[0].route_label if row_list else "local_coverage_gap"
    lines = [
        "# Best Route Summary For `(5,4,5)`",
        "",
        "This summary ranks the current focused route options while keeping the route capped at `worth_human_modular_review`.",
        "",
        f"- Current best route label: `{top_label}`.",
        "",
        "| rank | route option | label | primes | unit survivors | single-mask survivors | q=3 penalty | reason |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| {row.rank} | `{row.route_option}` | `{row.route_label}` | `{row.supporting_primes}` | "
            f"{row.unit_survivor_count} | {row.single_mask_survivor_count} | "
            f"{row.q3_reliance_penalty} | {row.reason} |"
        )
    lines.extend(
        [
            "",
            "## Current Interpretation",
            "",
            (
                "The non-q=3 cross-prime route is the preferred current route evidence."
                if top_label == "cross_prime_elimination_candidate"
                else "The focused route still depends on surviving or incomplete local branches."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def write_best_route_summary_545_markdown(path, rows: Iterable[BestRouteSummaryRecord]):
    """Write `BEST_ROUTE_SUMMARY_545.md`."""
    path.write_text(best_route_summary_545_markdown(rows), encoding="utf-8")
    return path
