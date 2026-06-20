"""Human-readable exact modular explanations for zero-support rows."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .padic_lift_audit import PadicLiftAudit
from .primitive_obstruction_classifier import PrimitiveClassification
from .rsg_residue_engine import ResidueSweepResult, power_residue_set
from .zero_support_engine import ZeroSupportRecord


@dataclass(frozen=True)
class ExactExplanation:
    """Narrative explanation for one candidate row."""

    signature: tuple[int, int, int]
    ell: int
    classification: str
    headline: str
    modular_explanation: str
    proof_gap: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        return data


def _power_set_clause(variable: str, exponent: int, ell: int) -> str:
    residues = power_residue_set(exponent, ell)
    if residues == (1,):
        return f"all nonzero {variable}^{exponent} residues are 1 modulo {ell}"
    if len(residues) <= 4:
        values = ",".join(str(value) for value in residues)
        return f"nonzero {variable}^{exponent} residues are {{{values}}} modulo {ell}"
    return f"nonzero {variable}^{exponent} residues form a subgroup of size {len(residues)} modulo {ell}"


def _mask_sentence(zero: ZeroSupportRecord) -> str:
    counts = [
        f"{mask}={zero.zero_mask_counts.get(mask, 0)}"
        for mask in zero.occurring_zero_masks
    ]
    return "zero-support counts: " + ", ".join(counts)


def generate_exact_explanation(
    result: ResidueSweepResult,
    zero: ZeroSupportRecord,
    classification: PrimitiveClassification,
    audit: PadicLiftAudit | None = None,
) -> ExactExplanation:
    """Generate a compact modular explanation for a candidate row."""
    p, q, r = result.signature
    clauses = [
        _power_set_clause("A", p, result.ell),
        _power_set_clause("B", q, result.ell),
        _power_set_clause("C", r, result.ell),
    ]
    base = (
        f"For ell={result.ell} and signature ({p},{q},{r}), "
        f"{'; '.join(clauses)}. The exact zero-support enumeration gives "
        f"{_mask_sentence(zero)}."
    )

    if classification.classification == "direct_primitive_obstruction":
        headline = "direct primitive obstruction candidate"
        conclusion = (
            "Every local survivor has at least two variables divisible by ell; "
            "modulo a prime this pushes the third variable to zero as well."
        )
        gap = "Needs verification across a broader prime/signature family and compatibility with global primitive conditions."
    elif classification.classification == "mandatory_single_divisor":
        headline = f"mandatory single-divisor candidate forcing {classification.forced_variable}"
        conclusion = (
            f"Every local survivor has exactly {classification.forced_variable} divisible by ell. "
            "This is not a primitive contradiction by itself."
        )
        if audit is not None:
            conclusion += f" The lift audit reports {audit.valuation_growth_estimate}."
        gap = "Needs an LTE or p-adic descent step that turns one-variable divisibility into shared-prime pressure."
    elif classification.classification == "sparse_unit_survivor":
        headline = "sparse unit-survivor lemma candidate"
        conclusion = (
            f"Unit survivors exist, but density {result.density} is below structured/random controls "
            f"with z-score {result.control_z_score}."
        )
        gap = "Needs proof that sparsity is invariant under stronger lifts or modular-shadow constraints."
    elif classification.classification == "likely_small_prime_artifact":
        headline = "likely small-prime or subgroup-collapse artifact"
        conclusion = (
            "The obstruction is largely explained by a tiny prime or a trivial power subgroup, "
            "so it is useful as a sanity check rather than a headline lemma candidate."
        )
        gap = "Needs separation from small-prime subgroup collapse before it can support a reusable theorem."
    else:
        headline = "control-like local row"
        conclusion = "No exact primitive obstruction has been detected in this row."
        gap = "Not currently a lemma candidate."

    return ExactExplanation(
        signature=result.signature,
        ell=result.ell,
        classification=classification.classification,
        headline=headline,
        modular_explanation=f"{base} {conclusion}",
        proof_gap=gap,
    )


def generate_explanations(
    results: list[ResidueSweepResult],
    zero_records: list[ZeroSupportRecord],
    classifications: list[PrimitiveClassification],
    audits: list[PadicLiftAudit],
    *,
    limit: int = 40,
) -> list[ExactExplanation]:
    """Generate explanations for the highest-ranked candidate rows."""
    result_by_key = {(result.signature, result.ell): result for result in results}
    zero_by_key = {(zero.signature, zero.ell): zero for zero in zero_records}
    audit_by_key = {(audit.signature, audit.ell): audit for audit in audits}
    candidate_rows = [
        item
        for item in classifications
        if item.classification
        in {
            "direct_primitive_obstruction",
            "mandatory_single_divisor",
            "sparse_unit_survivor",
            "likely_small_prime_artifact",
        }
    ]
    priority = {
        "direct_primitive_obstruction": 4,
        "mandatory_single_divisor": 3,
        "sparse_unit_survivor": 2,
        "likely_small_prime_artifact": 1,
    }
    candidate_rows.sort(
        key=lambda item: (priority.get(item.classification, 0), item.lemma_candidate_score),
        reverse=True,
    )
    explanations: list[ExactExplanation] = []
    for item in candidate_rows[:limit]:
        key = (item.signature, item.ell)
        explanations.append(
            generate_exact_explanation(
                result_by_key[key],
                zero_by_key[key],
                item,
                audit_by_key.get(key),
            )
        )
    return explanations
