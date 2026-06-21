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
            current_evidence="Symbolic invariants are computed for the displayed model: Delta=16*A^10*B^8*C^10, c4=16*(A^10+A^5*B^4+B^8), and c6=32*(A^5-B^4)*(2*A^10+5*A^5*B^4+2*B^8).",
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
            statement="Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) == +/-(q+1) mod 5 at q in {3,13,17,41,61}.",
            current_evidence=local_gap_evidence,
            status="level_lowering_assumption_required",
            risk_level="high",
            next_action="Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) == +/-(q+1) mod 5 at q in {3,13,17,41,61}.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-012",
            title="Cross-prime branch compatibility",
            statement="Check whether q in {13,17,41,61} jointly eliminate all compatible unit and single-mask branch assignments for the level-220 newforms.",
            current_evidence=local_gap_evidence,
            status="computed_route_evidence",
            risk_level="high",
            next_action="Treat this as a screening audit only; do not use fixed branch compatibility across distinct good primes as the final modular-method quantifier.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-013",
            title="q=3 exceptionality review",
            statement="Decide whether the q=3 local closure is small-prime-sensitive or supported by the non-q=3 focused primes.",
            current_evidence=local_gap_evidence,
            status="q3_requires_human_review",
            risk_level="high",
            next_action="Compare q=3 behavior with q=13,17,41,61 and justify any use of q=3 as local route evidence.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-014",
            title="Quantifier-safe cross-prime route",
            statement="For each level-220 newform, identify at least one non-q=3 prime where unit, A_only, B_only, C_only, and pairwise primitive-forbidden masks are all covered.",
            current_evidence=local_gap_evidence,
            status="quantifier_safe_cross_prime_candidate",
            risk_level="high",
            next_action="Verify the exists-prime-per-newform elimination and reject any argument that couples fixed branch choices across different primes.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-015",
            title="Frey-conductor proof audit",
            statement="Turn the symbolic Frey invariant formulas into a minimal conductor and exact bad-prime support statement.",
            current_evidence="The Frey-conductor audit computes symbolic c4, c6, Delta, and j, but conductor exponents remain unproved.",
            status="conductor_gap_blocks_upgrade",
            risk_level="high",
            next_action="Prove the conductor support at 2, 5, 11, and primes dividing ABC; decide which primes remain in level 220.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-016",
            title="Bad-prime Tate algorithm",
            statement="Run the local Tate/minimal-model analysis at the bad primes 2, 5, and 11.",
            current_evidence="The checklist records symbolic valuation formulas but no completed local Tate analysis.",
            status="blocks_conductor_claim",
            risk_level="high",
            next_action="Compute reduction types and conductor exponents at 2, 5, and 11.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-017",
            title="Formal level-lowering package",
            statement="Verify residual modulus 5, residual irreducibility, modularity input, level-lowering hypotheses, exact target level 220, and good-prime trace validity.",
            current_evidence="The obligation list is generated, with irreducibility and exact level still missing.",
            status="level_lowering_gap_blocks_upgrade",
            risk_level="high",
            next_action="Discharge every level-lowering obligation before interpreting the trace elimination as a modular-method argument.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-018",
            title="Conductor-exponent model provenance",
            statement="Separate generic multiplicative ABC-prime behavior from bad-prime exponent calculations at 2, 5, and 11.",
            current_evidence="The conductor-exponent model records generic multiplicative rows away from 2,5,11 but leaves bad-prime exponents as human Tate checks.",
            status="bad_prime_tate_gap",
            risk_level="high",
            next_action="Derive the exact local conductor exponent at 2, at 5, and at any 11-adic case used by the route.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-019",
            title="Level-220 provenance",
            statement="Explain each factor in 220 = 2^2 * 5 * 11 from the Frey conductor or lowered level.",
            current_evidence="The level-220 provenance audit labels the aggregate target as level_220_heuristic_target and the factor 11 as level_11_factor_unjustified.",
            status="conductor_gap_blocks_upgrade",
            risk_level="high",
            next_action="Justify the factors 2, 5, and 11, or replace the target level and rerun the newform comparison.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-020",
            title="ABC-prime removal",
            statement="Show why primes dividing A, B, or C disappear from the final comparison level after level lowering.",
            current_evidence="The ABC-prime removal audit marks A, B, and C prime cases with abc_prime_removal_gap.",
            status="abc_prime_removal_gap",
            risk_level="high",
            next_action="Verify residual irreducibility, minimality, and the local hypotheses needed to remove every prime dividing ABC.",
        ),
        TheoremSkeletonObligationRecord(
            signature="5-4-5",
            obligation_id="TS545-021",
            title="Sage conductor sanity samples",
            statement="Use generated Sage code only to sanity-check formulas and optional exact samples supplied later.",
            current_evidence="The generated Sage script contains symbolic formulas and finite-field residue samples only.",
            status="synthetic_sanity_only",
            risk_level="medium",
            next_action="Do not use synthetic samples as mathematical evidence; use them only to spot formula or conductor-computation mistakes.",
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
    lemma_rows = [row for row in rows if row.obligation_id != "TS545-001"]
    for index, row in enumerate(lemma_rows, start=1):
        lines.extend(
            [
                f"## Required Lemma {index}: {row.title}",
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
            "- Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) == +/-(q+1) mod 5 at q in {3,13,17,41,61}.",
            "- Treat the cross-prime branch compatibility audit for q in {13,17,41,61} as a screen, not as fixed-branch coupling.",
            "- Review whether q=3 behavior is small-prime-sensitive or supported by the larger focused primes.",
            "- Verify the quantifier-safe cross-prime route: each level-220 newform must have one non-q=3 eliminating prime with complete same-prime branch coverage.",
            "- Prove the symbolic Frey invariant formulas give the minimal conductor support after local minimization.",
            "- Run the bad-prime Tate algorithm at 2, 5, and 11.",
            "- Verify every formal level-lowering obligation, including residual irreducibility and exact target level 220.",
            "- Derive the conductor-exponent model rather than relying on symbolic valuation heuristics at bad primes.",
            "- Explain each factor of level 220 and resolve `level_11_factor_unjustified`.",
            "- Remove every prime dividing ABC by a verified level-lowering argument or change the comparison level.",
            "- Treat the Sage conductor sanity script as formula-checking support only.",
            "",
            "## Why This Is Not A Proof",
            "",
            "The computation only supplies conditional route evidence. Until the Frey attachment, conductor, irreducibility, level-lowering, newform-space, and local-coverage lemmas are supplied by hand, the result remains capped at `worth_human_modular_review`.",
            "",
        ]
    )
    return "\n".join(lines)
