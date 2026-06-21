"""Theorem skeleton builder for the focused `(5,4,5)` route."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .level_220_robustness_545 import LevelRobustnessRecord
from .local_gap_summary_545 import LocalGapSummaryRecord
from .local_coverage_audit_545 import LocalCoverageAuditRecord
from .obstruction_progress_score import ObstructionProgressRecord
from .small_prime_sensitivity_545 import SmallPrimeSensitivityRecord


@dataclass(frozen=True)
class TheoremSkeletonObligationRecord:
    """One hand-check obligation for the conditional route."""

    signature: str
    obligation_id: str
    title: str
    statement: str
    current_evidence: str
    status: str
    risk_level: str
    next_action: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def build_theorem_skeleton_obligations_545(
    *,
    progress_row: ObstructionProgressRecord,
    sensitivity_rows: list[SmallPrimeSensitivityRecord],
    coverage_rows: list[LocalCoverageAuditRecord],
    level_rows: list[LevelRobustnessRecord],
    local_gap_summary: LocalGapSummaryRecord | None = None,
) -> list[TheoremSkeletonObligationRecord]:
    """Return the exact obligations for a conditional `(5,4,5)` modular route."""
    coverage_gaps = sum(1 for row in coverage_rows if row.coverage_label == "local_coverage_gap")
    sensitivity_summary = ";".join(f"{row.profile_name}:{row.sensitivity_label}" for row in sensitivity_rows)
    level_summary = ";".join(
        f"{row.level}:{row.robustness_label}" for row in level_rows if row.level in {110, 220, 440}
    )
    local_gap_evidence = (
        f"{local_gap_summary.overall_local_gap_label}; scope={local_gap_summary.trace_mismatch_scope_label}; "
        f"full_coverage_eliminating_primes={local_gap_summary.full_coverage_eliminating_primes or 'none'}"
        if local_gap_summary is not None
        else f"Local coverage gaps flagged at {coverage_gaps} selected good primes."
    )
    return [
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-001",
            title="Hypothetical primitive solution setup",
            statement="Assume pairwise nonzero integers A,B,C satisfy A^5 + B^4 = C^5 and gcd(A,B,C)=1.",
            current_evidence="Framework assumption only.",
            status="conditional_setup",
            risk_level="medium",
            next_action="State sign, nonzero, coprimality, and normalization conventions exactly.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-002",
            title="Frey attachment",
            statement="Attach E: y^2 = x(x - A^5)(x + B^4) to every primitive solution in the required orientation.",
            current_evidence="Template exists in the route library.",
            status="needs_hand_derivation",
            risk_level="high",
            next_action="Derive nonsingularity and integral model conditions for all primitive solution cases.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-003",
            title="Discriminant and conductor calculation",
            statement="Compute the minimal discriminant and conductor exponents, including primes 2, 5, 11, and primes dividing ABC.",
            current_evidence="Symbolic discriminant-like support is 16*A^10*B^8*C^10.",
            status="needs_hand_derivation",
            risk_level="high",
            next_action="Run a prime-by-prime minimal model and conductor analysis.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-004",
            title="Residual mod-5 irreducibility",
            statement="Show the relevant residual representation modulo 5 is irreducible and has the required ramification behavior.",
            current_evidence="The current trace filter uses mod-5 comparison mode.",
            status="missing",
            risk_level="high",
            next_action="Identify the exact representation and prove irreducibility or state required exceptions.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-005",
            title="Level lowering to level 220",
            statement="Show the modular representation lowers to the weight-2 level-220 space used by the Sage query.",
            current_evidence=level_summary or "Level 220 coefficient extraction completed; nearby levels are not checked.",
            status="needs_hand_derivation",
            risk_level="high",
            next_action="Justify why the comparison level is 220 and why no nearby level should be used instead.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-006",
            title="Level-220 newform exhaustion",
            statement="Verify that the two imported level-220 newform slots are the complete relevant target space.",
            current_evidence=f"Current trace progress label is {progress_row.progress_label}.",
            status="computed_route_evidence",
            risk_level="medium",
            next_action="Confirm old/new decomposition, character choices, coefficient fields, and labels in Sage or Magma.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-007",
            title="Good-prime trace exclusion",
            statement="For each relevant good prime, compare Frey trace possibilities with newform coefficients in the justified residue field.",
            current_evidence=f"{progress_row.eliminated_newforms} of {progress_row.newform_count} level-220 newforms eliminated by current filter.",
            status="computed_route_evidence",
            risk_level="medium",
            next_action="Check the first eliminating primes independently and justify the local enumeration.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-008",
            title="Local valuation and reduction case split for q | ABC",
            statement="Handle reductions where q divides one or more of A,B,C, or prove they are not needed for the chosen good-prime trace step.",
            current_evidence=local_gap_evidence,
            status="local_coverage_gap" if coverage_gaps else "computed_route_evidence",
            risk_level="high" if coverage_gaps else "medium",
            next_action="Prove the local valuation and reduction case split for q in {3,13,17,41,61} with q | ABC, including A_only, B_only, C_only, and singular Frey reductions.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-010",
            title="Focused Tate algorithm for single masks",
            statement="Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only.",
            current_evidence=local_gap_evidence,
            status="needs_human_tate_algorithm",
            risk_level="high",
            next_action="Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-011",
            title="Multiplicative-reduction congruence",
            statement="Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) ≡ ±(q+1) mod 5 at q in {3,13,17,41,61}.",
            current_evidence=local_gap_evidence,
            status="level_lowering_assumption_required",
            risk_level="high",
            next_action="Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) ≡ ±(q+1) mod 5 at q in {3,13,17,41,61}.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-009",
            title="Small-prime robustness",
            statement="Show the route does not rely on an accidental tiny-prime phenomenon unless that reliance is mathematically justified.",
            current_evidence=sensitivity_summary or "Sensitivity profiles not available.",
            status="computed_route_evidence",
            risk_level="medium",
            next_action="Decide whether reliance on q=3 or another focused eliminating prime should be part of the human check.",
        ),
    ]


def theorem_skeleton_markdown(rows: list[TheoremSkeletonObligationRecord]) -> str:
    """Render the requested conditional theorem skeleton."""
    lines = [
        "# Conditional Modular Route For Primitive Solutions Of `A^5 + B^4 = C^5`",
        "",
        "This is a theorem skeleton, not a completed argument. It lists the exact hand-written lemmas needed before the computational trace mismatch can carry mathematical force.",
        "",
        "## Statement Of Hypothetical Primitive Solution",
        "",
        "Assume nonzero integers `A,B,C` satisfy `A^5 + B^4 = C^5` and `gcd(A,B,C)=1`, with all normalization and sign conventions stated explicitly.",
        "",
        "## Proposed Frey Object",
        "",
        "`E: y^2 = x(x - A^5)(x + B^4)`.",
        "",
    ]
    lemma_titles = [
        "Required Lemma 1: Frey Attachment",
        "Required Lemma 2: Discriminant/Conductor Computation",
        "Required Lemma 3: Residual Mod-5 Irreducibility",
        "Required Lemma 4: Level Lowering To Level 220",
        "Required Lemma 5: Level-220 Newform Exhaustion",
        "Required Lemma 6: Good-Prime Trace Exclusion",
        "Required Lemma 7: Local Valuation And Reduction Case Split For q | ABC",
        "Required Lemma 8: Focused Tate Algorithm At q In {3,13,17,41,61}",
        "Required Lemma 9: Multiplicative-Reduction Congruence",
    ]
    lemma_rows = list(rows[1:10])
    for title, row in zip(lemma_titles, lemma_rows):
        lines.extend(
            [
                f"## {title}",
                "",
                row.statement,
                "",
                f"- Current evidence: {row.current_evidence}",
                f"- Status: `{row.status}`.",
                f"- Next action: {row.next_action}",
                "",
            ]
        )
    lines.extend(
        [
            "## Current Computational Evidence",
            "",
            "| obligation | status | evidence | next action |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(f"| `{row.obligation_id}` | `{row.status}` | {row.current_evidence} | {row.next_action} |")
    lines.extend(
        [
            "",
            "## Exact Open Assumptions",
            "",
            "- The Frey object is correct for every primitive solution case.",
            "- The minimal conductor and lowered level are exactly the level used for comparison.",
            "- The residual mod-5 representation is the correct irreducible representation for the trace comparison.",
            "- The relevant level-220 newforms are exhausted by the imported Sage query.",
            "- The q in {3,13,17,41,61} good-prime local enumeration covers all reductions required by the modular argument, including single-divisibility branches.",
            "- Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only.",
            "- Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) ≡ ±(q+1) mod 5 at q in {3,13,17,41,61}.",
            "",
            "## Why This Is Not A Proof",
            "",
            "The computation only supplies conditional route evidence. Until the Frey attachment, conductor, irreducibility, level-lowering, newform-space, and local-coverage lemmas are supplied by hand, the result remains capped at `worth_human_modular_review`.",
            "",
        ]
    )
    return "\n".join(lines)
