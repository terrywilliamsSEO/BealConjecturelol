"""Machine-readable assumption register for focused modular audits."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AssumptionRecord:
    """One assumption or verified fact in the focused audit."""

    assumption_id: str
    statement: str
    source: str
    status: str
    required_for: str
    risk_level: str
    next_action: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def build_assumption_register_545() -> list[AssumptionRecord]:
    """Return the focused assumption register for `(5,4,5)`."""
    return [
        AssumptionRecord(
            assumption_id="A545-001",
            statement="Every primitive solution of A^5 + B^4 = C^5 produces the selected split full-2-torsion Frey curve.",
            source="frey_template_library symbolic template",
            status="needs_human_math_review",
            required_for="Frey object attachment",
            risk_level="high",
            next_action="Write the algebraic derivation and check orientation, primitivity, and singular cases.",
        ),
        AssumptionRecord(
            assumption_id="A545-002",
            statement="The symbolic discriminant support captures the relevant bad-prime support after minimization.",
            source="frey_template_validity_audit",
            status="needs_human_math_review",
            required_for="conductor calculation",
            risk_level="high",
            next_action="Compute the minimal discriminant and conductor exponents prime by prime.",
        ),
        AssumptionRecord(
            assumption_id="A545-003",
            statement="The conductor or lowered level is exactly 220.",
            source="level_explanations.csv",
            status="heuristic_placeholder",
            required_for="newform search at level 220",
            risk_level="high",
            next_action="Derive the true conductor and justify level lowering to 220 if applicable.",
        ),
        AssumptionRecord(
            assumption_id="A545-004",
            statement="The relevant residual representation is irreducible.",
            source="modular-method obligation",
            status="missing",
            required_for="level lowering",
            risk_level="high",
            next_action="Prove irreducibility for the chosen residual representation.",
        ),
        AssumptionRecord(
            assumption_id="A545-005",
            statement="Trace comparison should be made modulo 5.",
            source="fifth-power exponent heuristic",
            status="needs_human_math_review",
            required_for="trace congruence interpretation",
            risk_level="medium",
            next_action="Justify the representation prime; distinguish mod 5 from the full-2-torsion structure.",
        ),
        AssumptionRecord(
            assumption_id="A545-006",
            statement="The two level-220 newforms exhaust the possible modular images.",
            source="Sage newform_count=2 at level 220",
            status="needs_human_math_review",
            required_for="newform exclusion step",
            risk_level="high",
            next_action="Confirm coefficient field handling, old/new decomposition choices, nebentypus assumptions, and exact target space.",
        ),
        AssumptionRecord(
            assumption_id="A545-007",
            statement="Sage computed two weight-2 newforms at level 220 in the current query.",
            source="sage_results/sage_5_4_5.json",
            status="computed_by_sage",
            required_for="review prioritization",
            risk_level="low",
            next_action="Export labels and q-expansion coefficients for independent review.",
        ),
        AssumptionRecord(
            assumption_id="A545-008",
            statement="The ell=11 narrow trace row is a reusable modular constraint rather than a local survivor artifact.",
            source="trace_comparison_audit",
            status="needs_human_math_review",
            required_for="local-to-global trace use",
            risk_level="high",
            next_action="Repeat trace comparisons at good primes for the justified level and compare against same-size controls.",
        ),
        AssumptionRecord(
            assumption_id="A545-009",
            statement="The target level 220 is valid for the modular comparison.",
            source="good-prime trace audit",
            status="heuristic_placeholder",
            required_for="good-prime newform filtering",
            risk_level="high",
            next_action="Prove level 220 is the true conductor or a justified lowered level before treating its newforms as exhaustive.",
        ),
        AssumptionRecord(
            assumption_id="A545-010",
            statement="The residual modulus for congruence filtering is 5.",
            source="trace_congruence_filter_545 default",
            status="needs_human_math_review",
            required_for="mod-5 trace comparisons",
            risk_level="high",
            next_action="Justify the residual representation prime and its coefficient-field reduction map.",
        ),
        AssumptionRecord(
            assumption_id="A545-011",
            statement="The Frey template E: y^2 = x(x - A^5)(x + B^4) is the correct object for good-prime trace enumeration.",
            source="frey_trace_possibility_545",
            status="needs_human_math_review",
            required_for="Frey trace possibility sets",
            risk_level="high",
            next_action="Derive the template from a primitive solution and prove nonsingularity at selected good primes.",
        ),
        AssumptionRecord(
            assumption_id="A545-012",
            statement="Newform coefficient comparison is performed in the correct coefficient field and reduction map.",
            source="sage_level_220_newform_expander.sage",
            status="missing",
            required_for="newform trace congruence filtering",
            risk_level="high",
            next_action="Export coefficient fields and define the exact reduction before interpreting non-rational coefficients.",
        ),
        AssumptionRecord(
            assumption_id="A545-013",
            statement="Local residue enumeration captures all primitive reductions at selected good primes.",
            source="frey_trace_possibility_545",
            status="needs_human_math_review",
            required_for="completeness of Frey trace possibilities",
            risk_level="medium",
            next_action="Prove that enumerating nonzero power-image triples u+v=w covers every primitive reduction at good primes.",
        ),
    ]
