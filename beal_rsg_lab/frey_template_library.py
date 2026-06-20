"""Symbolic Frey-style template library for modular-shadow routing."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import log2

from .number_theory import radical
from .signature_normalizer import NormalizedSignature, normalize_signature
from .rsg_residue_engine import Signature


@dataclass(frozen=True)
class FreyTemplateRecord:
    """Symbolic Frey-template metadata.

    These records are route metadata only. They are not proofs that the template
    is valid for every signature or every primitive solution.
    """

    signature: Signature
    canonical_signature_id: str
    template_id: str
    equation: str
    discriminant_support: str
    bad_prime_support: str
    radical_support: tuple[int, ...]
    conductor_complexity_score: float
    symmetry_behavior: str
    template_confidence: float
    uncertainty_flags: tuple[str, ...]

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["radical_support"] = ";".join(str(part) for part in self.radical_support)
        data["uncertainty_flags"] = ";".join(self.uncertainty_flags)
        return data


def candidate_frey_template(signature: Signature) -> FreyTemplateRecord:
    """Return the candidate template E: y^2 = x(x - A^p)(x + B^q)."""
    normalized = normalize_signature(signature)
    p, q, r = signature
    support = radical(signature)
    uncertainty = [
        "template_not_validated_for_all_signatures",
        "requires_minimal_model_check",
        "requires_irreducibility_check",
        "requires_newform_level_computation",
    ]
    if 2 in support:
        uncertainty.append("even_exponent_minimal_model_subtlety")
    if normalized.fourth_power_involvement:
        uncertainty.append("fourth_power_bridge_requires_separate_descent")

    confidence = 0.45
    if normalized.has_repeated_exponent:
        confidence += 0.08
    if normalized.mixed_prime_structure:
        confidence += 0.05
    if normalized.fourth_power_involvement:
        confidence += 0.03
    confidence = min(0.72, confidence)

    complexity = sum(log2(value) for value in support) + 0.4 * len(set(signature))
    if normalized.fourth_power_involvement:
        complexity += 0.6
    if normalized.has_repeated_exponent:
        complexity += 0.4

    symmetry = "A/B symmetric" if normalized.symmetric_ab else "A/B swap changes template orientation"
    return FreyTemplateRecord(
        signature=signature,
        canonical_signature_id=normalized.canonical_signature_id,
        template_id="frey_split_full_2torsion_candidate",
        equation=f"E: y^2 = x(x - A^{p})(x + B^{q})",
        discriminant_support=f"2^4 * A^{2*p} * B^{2*q} * C^{2*r} (symbolic using A^p+B^q=C^r)",
        bad_prime_support="2 plus primes dividing A*B*C plus unresolved minimal-model primes",
        radical_support=support,
        conductor_complexity_score=round(complexity, 10),
        symmetry_behavior=symmetry,
        template_confidence=round(confidence, 10),
        uncertainty_flags=tuple(uncertainty),
    )


def build_template_records(signatures: list[Signature]) -> list[FreyTemplateRecord]:
    """Build unique template records by exact signature."""
    seen: set[Signature] = set()
    records: list[FreyTemplateRecord] = []
    for signature in signatures:
        if signature in seen:
            continue
        seen.add(signature)
        records.append(candidate_frey_template(signature))
    records.sort(key=lambda item: (item.template_confidence, item.conductor_complexity_score), reverse=True)
    return records
