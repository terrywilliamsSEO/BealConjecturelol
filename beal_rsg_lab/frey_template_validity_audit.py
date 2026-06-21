"""Validity audit for symbolic Frey-template components."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .frey_template_library import candidate_frey_template
from .number_theory import radical
from .signature_normalizer import normalize_signature


VALIDITY_STATUSES = {
    "verified_by_symbolic_formula",
    "computed_by_sage",
    "heuristic_placeholder",
    "missing",
    "needs_human_math_review",
}


@dataclass(frozen=True)
class FreyTemplateValidityRecord:
    """One component of the focused Frey-template validity audit."""

    signature: str
    component: str
    classification: str
    statement: str
    evidence_source: str
    risk_level: str
    next_action: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _value(row: Mapping[str, Any] | None, key: str, default: str = "") -> str:
    if row is None:
        return default
    value = row.get(key, default)
    return "" if value is None else str(value)


def _parse_levels(value: str) -> tuple[int, ...]:
    output: list[int] = []
    for part in value.split(";"):
        if not part:
            continue
        try:
            output.append(int(part))
        except ValueError:
            continue
    return tuple(output)


def build_frey_template_validity_audit_545(
    *,
    sage_payload: Mapping[str, Any] | None,
    level_row: Mapping[str, Any] | None,
    audit_row: Mapping[str, Any] | None,
) -> list[FreyTemplateValidityRecord]:
    """Classify every major Frey-template component for `(5,4,5)`."""
    signature = (5, 4, 5)
    signature_text = "5-4-5"
    template = candidate_frey_template(signature)
    normalized = normalize_signature(signature)
    checked_levels = _parse_levels(_value(audit_row, "checked_levels"))
    level_220_checked = 220 in checked_levels or bool(sage_payload and 220 in sage_payload.get("checked_levels", []))
    support = tuple(sorted({2, *radical(signature), 11}))
    level_source = _value(level_row, "candidate_level_source") or (
        "Generated from support {2, exponent radicals, local primes}; 220 is 2 times base support product 110."
    )
    rows = [
        FreyTemplateValidityRecord(
            signature=signature_text,
            component="curve_equation_used",
            classification="verified_by_symbolic_formula",
            statement=template.equation,
            evidence_source="frey_template_library.candidate_frey_template",
            risk_level="medium",
            next_action="Derive that every primitive solution of A^5+B^4=C^5 gives this exact Frey object after orientation choices.",
        ),
        FreyTemplateValidityRecord(
            signature=signature_text,
            component="discriminant_support",
            classification="verified_by_symbolic_formula",
            statement=template.discriminant_support,
            evidence_source="symbolic template record",
            risk_level="medium",
            next_action="Turn symbolic support into a minimal discriminant calculation for the 5-4-5 case.",
        ),
        FreyTemplateValidityRecord(
            signature=signature_text,
            component="conductor_like_level_formula",
            classification="heuristic_placeholder",
            statement=level_source,
            evidence_source="sage_job_generator._candidate_levels",
            risk_level="high",
            next_action="Compute the actual conductor and any lowered level from a validated minimal model.",
        ),
        FreyTemplateValidityRecord(
            signature=signature_text,
            component="bad_prime_set",
            classification="heuristic_placeholder",
            statement="Candidate support primes: " + ",".join(str(item) for item in support),
            evidence_source="2 plus exponent radical support plus local prime 11",
            risk_level="high",
            next_action="Prove which primes are genuinely bad for the Frey curve attached to a primitive solution.",
        ),
        FreyTemplateValidityRecord(
            signature=signature_text,
            component="reason_level_220_appears",
            classification="heuristic_placeholder",
            statement="220 = 2^2 * 5 * 11 appears as 2 times the base support product 110.",
            evidence_source="level_explanations.csv",
            risk_level="high",
            next_action="Decide whether 220 is an actual conductor, a lowered level, or only a search target.",
        ),
        FreyTemplateValidityRecord(
            signature=signature_text,
            component="level_220_sage_newform_count",
            classification="computed_by_sage" if level_220_checked else "missing",
            statement="Sage imported newform_count=2 at level 220." if level_220_checked else "No completed Sage count at level 220 was imported.",
            evidence_source="sage_results/sage_5_4_5.json",
            risk_level="low" if level_220_checked else "high",
            next_action="Extract labels and q-expansion data for both level-220 newforms.",
        ),
        FreyTemplateValidityRecord(
            signature=signature_text,
            component="level_220_status",
            classification="needs_human_math_review",
            statement="The current pipeline treats level 220 as a heuristic route-audit target, not as a proven conductor or lowered level.",
            evidence_source="deep audit guardrail",
            risk_level="high",
            next_action="Provide a conductor and level-lowering derivation for normalized signature " + normalized.canonical_signature_id + ".",
        ),
        FreyTemplateValidityRecord(
            signature=signature_text,
            component="representation_modulus",
            classification="needs_human_math_review",
            statement="The relevant comparison modulus is not certified by the pipeline; likely candidates include mod 5 from the fifth-power exponents, while mod 2 is entangled with the full-2-torsion template.",
            evidence_source="template uncertainty flags",
            risk_level="high",
            next_action="Choose and justify the residual representation prime before interpreting trace congruences.",
        ),
    ]
    for row in rows:
        if row.classification not in VALIDITY_STATUSES:
            raise ValueError(f"invalid validity status {row.classification!r}")
    return rows

