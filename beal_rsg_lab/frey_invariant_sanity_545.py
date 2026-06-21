"""Symbolic Frey invariant sanity checks for `(5,4,5)`."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class FreyInvariantSanityRecord:
    """One symbolic invariant or level-support sanity row."""

    signature: str
    component: str
    symbolic_expression: str
    inferred_support: str
    route_interpretation: str
    status: str
    required_assumption: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def build_frey_invariant_sanity_545() -> list[FreyInvariantSanityRecord]:
    """Return symbolic invariant sanity rows for the current Frey template."""
    return [
        FreyInvariantSanityRecord(
            signature="5-4-5",
            component="curve_equation",
            symbolic_expression="E: y^2 = x(x - A^5)(x + B^4)",
            inferred_support="A,B",
            route_interpretation="Candidate split full-2-torsion Frey object used by the audit.",
            status="template_candidate",
            required_assumption="Prove every primitive solution produces this curve in the required orientation.",
        ),
        FreyInvariantSanityRecord(
            signature="5-4-5",
            component="discriminant_like",
            symbolic_expression="Delta = 16 * (A^5)^2 * (B^4)^2 * (A^5 + B^4)^2 = 16*A^10*B^8*C^10",
            inferred_support="2,A,B,C",
            route_interpretation="Bad-prime support should be contained in 2 and primes dividing ABC before minimization.",
            status="verified_by_symbolic_formula",
            required_assumption="Check minimal discriminant valuations at 2, 5, and all primes dividing ABC.",
        ),
        FreyInvariantSanityRecord(
            signature="5-4-5",
            component="j_invariant_like",
            symbolic_expression="j = 256*(A^10 + A^5*B^4 + B^8)^3/(A^10*B^8*C^10)",
            inferred_support="2,A,B,C,A^10 + A^5*B^4 + B^8",
            route_interpretation="Potential integrality and denominator support must be checked prime by prime.",
            status="symbolic_placeholder",
            required_assumption="Derive c4 and j for the exact integral model and verify cancellations.",
        ),
        FreyInvariantSanityRecord(
            signature="5-4-5",
            component="candidate_bad_prime_support",
            symbolic_expression="{2} union primes(A*B*C)",
            inferred_support="2,A,B,C",
            route_interpretation="Good-prime traces are meaningful only away from the actual conductor support.",
            status="needs_human_math_review",
            required_assumption="Prove which primes are genuinely bad after minimization.",
        ),
        FreyInvariantSanityRecord(
            signature="5-4-5",
            component="level_220_support",
            symbolic_expression="220 = 2^2 * 5 * 11",
            inferred_support="2,5,11",
            route_interpretation="Current comparison level includes the exponent prime 5 and local audit prime 11.",
            status="heuristic_route_target",
            required_assumption="Justify whether 11 belongs to the true conductor, lowered level, or only the search route.",
        ),
        FreyInvariantSanityRecord(
            signature="5-4-5",
            component="level_lowering_disappearing_primes",
            symbolic_expression="primes dividing ABC should disappear from the lowered level under a valid modular method package",
            inferred_support="ABC",
            route_interpretation="This is the core gap between local trace data and a modular route.",
            status="missing",
            required_assumption="Prove irreducibility, semistability/ramification hypotheses, and the exact lowering statement.",
        ),
    ]


def frey_invariant_sanity_markdown(rows: list[FreyInvariantSanityRecord]) -> str:
    """Render the Frey invariant sanity report."""
    lines = [
        "# Frey Invariant Sanity For `(5,4,5)`",
        "",
        "These rows are symbolic sanity checks for the current Frey template. They are not a conductor proof.",
        "",
        "| component | expression | inferred support | status | required assumption |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row.component}` | `{row.symbolic_expression}` | `{row.inferred_support}` | "
            f"`{row.status}` | {row.required_assumption} |"
        )
    lines.extend(
        [
            "",
            "The key hand task is to turn the discriminant-like support calculation into a minimal conductor and level-lowering statement.",
            "",
        ]
    )
    return "\n".join(lines)
