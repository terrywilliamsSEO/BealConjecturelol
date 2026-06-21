"""Gap reports for focused modular-method review packets."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ProofGapRecord:
    """One open gap in the focused modular-method route."""

    signature: str
    gap_category: str
    gap_status: str
    description: str
    required_next_lemma: str
    risk_level: str
    blocks_label_beyond_review: bool

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def build_proof_gap_records_545() -> list[ProofGapRecord]:
    """Return focused gap records for `(5,4,5)`."""
    signature = "5-4-5"
    return [
        ProofGapRecord(
            signature=signature,
            gap_category="algebraic_derivation_gap",
            gap_status="open",
            description="The pipeline has not derived that a primitive solution gives the selected Frey curve in all cases.",
            required_next_lemma="Prove the Frey-curve attachment lemma for A^5+B^4=C^5, including primitivity and nonsingularity conditions.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="conductor_gap",
            gap_status="open",
            description="Level 220 is a route-audit target, not a verified conductor.",
            required_next_lemma="Compute the exact conductor of the attached Frey curve and justify every prime/exponent in the level.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="irreducibility_gap",
            gap_status="open",
            description="The residual representation has not been shown irreducible.",
            required_next_lemma="Prove irreducibility for the justified residual representation prime.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="level_lowering_gap",
            gap_status="open",
            description="No level-lowering theorem has been checked against the template hypotheses.",
            required_next_lemma="Verify the hypotheses for lowering from the true conductor to the claimed comparison level.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="newform_trace_gap",
            gap_status="open",
            description="The current imported Sage result has a newform count but no q-expansion coefficient data.",
            required_next_lemma="Export and compare relevant newform coefficients at good primes using the justified modulus.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="local_to_global_gap",
            gap_status="open",
            description="The ell=11 narrow trace row is local data and 11 divides level 220, so it is not yet a good-prime modular comparison.",
            required_next_lemma="Show how local survivor traces constrain the global modular representation, or replace with good-prime trace comparisons.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="local_valuation_reduction_gap",
            gap_status="open",
            description="The focused good-prime trace mismatches at q in {3,13,17,41,61} are currently unit-case evidence unless reductions with q dividing A, B, or C are separately handled.",
            required_next_lemma="Prove the local valuation and reduction case split for q | ABC at q in {3,13,17,41,61}, including A_only, B_only, C_only, and singular Frey reductions.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="focused_tate_algorithm_gap",
            gap_status="open",
            description="The q in {3,13,17,41,61} A_only, B_only, and C_only branches now have a diagnostic layer, but the stub does not replace a human Tate-algorithm/reduction analysis.",
            required_next_lemma="Run the Tate algorithm / reduction analysis for the Frey curve at q in {3,13,17,41,61} under A_only, B_only, and C_only.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="multiplicative_congruence_gap",
            gap_status="open",
            description="The multiplicative-reduction congruence audit compares coefficients with +/-(q+1) modulo 5, but the level-lowering use of that condition has not been justified by hand.",
            required_next_lemma="Justify that the multiplicative-reduction branches satisfy the level-lowering congruence a_q(f) == +/-(q+1) mod 5 at q in {3,13,17,41,61}.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="cross_prime_branch_compatibility_gap",
            gap_status="open",
            description="The non-q=3 focused primes are compared across unit and single-mask branch assignments, but fixed branch coupling across different primes cannot be used as the final modular-method quantifier.",
            required_next_lemma="Review the cross-prime branch compatibility audit for q in {13,17,41,61} only as a screening layer.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="quantifier_safety_gap",
            gap_status="open",
            description="The conditional route now requires an exists-prime-per-newform check: each newform must be eliminated at one prime where every local branch is covered.",
            required_next_lemma="Verify the quantifier-safe cross-prime route: newform 0 at q=17 or q=41 and newform 1 at q=13, with complete same-prime branch coverage.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="q3_exceptionality_gap",
            gap_status="open",
            description="q=3 is good relative to level 220 but remains the smallest focused good prime and carries a small-prime sensitivity risk.",
            required_next_lemma="Review whether q=3 behavior is small-prime-sensitive or supported by the larger focused primes q=13,17,41,61.",
            risk_level="high",
            blocks_label_beyond_review=True,
        ),
        ProofGapRecord(
            signature=signature,
            gap_category="control_artifact_gap",
            gap_status="open",
            description="One 5-4-5 sparse row at ell=11 is artifact-explained; the non-artifact ell=31 row is not yet connected to the level-220 route.",
            required_next_lemma="Separate artifact local behavior from reusable modular constraints and connect any non-artifact rows to the Frey route.",
            risk_level="medium",
            blocks_label_beyond_review=True,
        ),
    ]


def proof_gap_report_markdown(*, output_dir: Path, rows: Iterable[ProofGapRecord]) -> str:
    """Return a human-readable focused gap report."""
    row_list = list(rows)
    lines = [
        "# Focused 5-4-5 Gap Report",
        "",
        f"Output directory: `{output_dir.as_posix()}`",
        "",
        "The focused audit keeps `(5,4,5)` at `worth_human_modular_review`; it does not move beyond review status.",
        "",
        "| category | status | risk | next lemma |",
        "| --- | --- | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| `{row.gap_category}` | `{row.gap_status}` | `{row.risk_level}` | {row.required_next_lemma} |"
        )
    lines.extend(
        [
            "",
            "## Exact Next Lemma",
            "",
            (
                "To advance `(5,4,5)`, a human should first prove the Frey-curve attachment and conductor/level-lowering "
                "lemmas: every primitive solution must yield the stated Frey object, its residual representation must be "
                "irreducible, and its true conductor must lower to the claimed comparison level. The same package must "
                "include the q in {3,13,17,41,61} local valuation and reduction case split for q | ABC, plus the focused Tate algorithm "
                "under A_only, B_only, and C_only, justify the multiplicative congruence a_q(f) == +/-(q+1) mod 5, and verify the "
                "exists-prime-per-newform quantifier before the two level-220 newforms are tested with q-expansion trace congruences at good primes. "
                "The cross-prime compatibility, quantifier-safety, and q=3 exceptionality audits must also be reviewed."
            ),
            "",
        ]
    )
    return "\n".join(lines)
