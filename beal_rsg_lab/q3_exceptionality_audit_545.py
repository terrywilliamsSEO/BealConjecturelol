"""q=3 exceptionality audit for the focused `(5,4,5)` route."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .cross_prime_branch_compatibility_545 import CrossPrimeBranchCompatibilityRecord
from .local_case_closure_score_545 import LocalCaseClosureScoreRecord


SAFE_Q3_EXCEPTIONALITY_LABELS = {
    "q3_consistent_with_larger_primes",
    "q3_small_prime_sensitive",
    "q3_requires_human_review",
}


@dataclass(frozen=True)
class Q3ExceptionalityAuditRecord:
    """One q=3 exceptionality audit row."""

    signature: str
    prime: int
    level: int
    level_prime_factors: str
    residual_prime: int
    is_good_prime_for_level: bool
    is_residual_prime: bool
    q3_closure_label: str
    q3_single_prime_closes: bool
    non_q3_cross_prime_label: str
    larger_prime_closure_labels: str
    small_prime_risk_flags: str
    q3_reliance_penalty: int
    q3_exceptionality_label: str
    route_ceiling_label: str
    reason: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _aggregate_cross_label(rows: list[CrossPrimeBranchCompatibilityRecord]) -> str:
    for row in rows:
        if row.newform_index == -1:
            return row.compatibility_label
    return "branch_data_insufficient"


def build_q3_exceptionality_audit_545(
    closure_rows: Iterable[LocalCaseClosureScoreRecord],
    cross_prime_rows: Iterable[CrossPrimeBranchCompatibilityRecord],
    *,
    level: int = 220,
    residual_prime: int = 5,
) -> Q3ExceptionalityAuditRecord:
    """Compare q=3 closure behavior with larger focused primes."""
    closures = list(closure_rows)
    cross_rows = list(cross_prime_rows)
    q3 = next((row for row in closures if row.prime == 3), None)
    larger = [row for row in closures if row.prime in {13, 17, 41, 61}]
    level_factors = "2;5;11"
    is_good = level % 3 != 0
    is_residual = 3 == residual_prime
    q3_label = q3.closure_label if q3 else "missing"
    q3_closes = q3_label == "local_case_elimination_candidate"
    cross_label = _aggregate_cross_label(cross_rows)
    larger_labels = ";".join(f"q={row.prime}:{row.closure_label}" for row in sorted(larger, key=lambda item: item.prime))
    risks = ["smallest_focused_good_prime", "q3_reliance_penalty"]
    if not is_good:
        risks.append("divides_level")
    if is_residual:
        risks.append("residual_prime")
    if q3 is None:
        label = "q3_requires_human_review"
        reason = "No q=3 closure row is available."
    elif not is_good or is_residual:
        label = "q3_requires_human_review"
        reason = "q=3 is not currently a clean good-prime input for this level/residual setup."
    elif q3_closes and cross_label == "cross_prime_elimination_candidate":
        label = "q3_consistent_with_larger_primes"
        reason = "q=3 closes locally, and the non-q=3 cross-prime compatibility audit also eliminates all tracked newform branch assignments."
    elif q3_closes:
        label = "q3_small_prime_sensitive"
        reason = "q=3 is the only currently closed local route, so the small-prime reliance needs human review."
    else:
        label = "q3_requires_human_review"
        reason = "q=3 does not currently close the tracked local branches."
    if label not in SAFE_Q3_EXCEPTIONALITY_LABELS:
        label = "q3_requires_human_review"
        reason = "Unexpected q=3 exceptionality label was downgraded to q3_requires_human_review."
    return Q3ExceptionalityAuditRecord(
        signature="5-4-5",
        prime=3,
        level=level,
        level_prime_factors=level_factors,
        residual_prime=residual_prime,
        is_good_prime_for_level=is_good,
        is_residual_prime=is_residual,
        q3_closure_label=q3_label,
        q3_single_prime_closes=q3_closes,
        non_q3_cross_prime_label=cross_label,
        larger_prime_closure_labels=larger_labels,
        small_prime_risk_flags=";".join(risks),
        q3_reliance_penalty=1,
        q3_exceptionality_label=label,
        route_ceiling_label="worth_human_modular_review",
        reason=reason,
    )


def q3_exceptionality_audit_545_markdown(row: Q3ExceptionalityAuditRecord) -> str:
    """Render `Q3_EXCEPTIONALITY_AUDIT_545.md`."""
    lines = [
        "# q=3 Exceptionality Audit For `(5,4,5)`",
        "",
        "This audit checks whether the q=3 local closure is isolated small-prime behavior or is supported by the larger focused primes.",
        "",
        f"- Level: `{row.level}` with prime factors `{row.level_prime_factors}`.",
        f"- q=3 is good relative to level 220: `{row.is_good_prime_for_level}`.",
        f"- q=3 is the residual prime: `{row.is_residual_prime}`.",
        f"- q=3 closure label: `{row.q3_closure_label}`.",
        f"- Non-q=3 cross-prime label: `{row.non_q3_cross_prime_label}`.",
        f"- Larger-prime closure labels: `{row.larger_prime_closure_labels or 'missing'}`.",
        f"- Small-prime risk flags: `{row.small_prime_risk_flags}`.",
        f"- q=3 reliance penalty: `{row.q3_reliance_penalty}`.",
        f"- Exceptionality label: `{row.q3_exceptionality_label}`.",
        f"- Route ceiling: `{row.route_ceiling_label}`.",
        "",
        "## Interpretation",
        "",
        row.reason,
        "",
    ]
    return "\n".join(lines)


def write_q3_exceptionality_audit_545_markdown(path, row: Q3ExceptionalityAuditRecord):
    """Write `Q3_EXCEPTIONALITY_AUDIT_545.md`."""
    path.write_text(q3_exceptionality_audit_545_markdown(row), encoding="utf-8")
    return path
