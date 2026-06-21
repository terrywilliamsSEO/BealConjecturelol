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
                "irreducible, and its true conductor must lower to the claimed comparison level. Only after that should "
                "the two level-220 newforms be tested with q-expansion trace congruences at good primes."
            ),
            "",
        ]
    )
    return "\n".join(lines)

