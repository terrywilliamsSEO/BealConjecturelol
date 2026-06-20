"""Final modular proof-route classification."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .artifact_explainer import ArtifactAssessment
from .cross_prime_trace_compatibility import CrossPrimeTraceRecord
from .finite_field_trace_probe import TraceProbeRecord
from .frey_template_library import FreyTemplateRecord
from .modular_shadow_engine import ModularShadowRoute


@dataclass(frozen=True)
class ModularRouteClassification:
    """Final proof-route classification for one signature/prime row."""

    signature: tuple[int, int, int]
    canonical_signature_id: str
    ell: int
    route_classification: str
    route_rank_score: float
    promotion_status: str
    rationale: str
    proof_gap: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        return data


def classify_modular_routes(
    routes: list[ModularShadowRoute],
    artifacts: list[ArtifactAssessment],
    traces: list[TraceProbeRecord],
    templates: list[FreyTemplateRecord],
    cross_prime_records: list[CrossPrimeTraceRecord],
) -> list[ModularRouteClassification]:
    """Classify modular proof routes without claiming obstructions."""
    artifact_by_key = {(item.signature, item.ell): item for item in artifacts}
    trace_by_key = {(item.signature, item.ell): item for item in traces}
    template_by_signature = {item.signature: item for item in templates}
    cross_by_canonical = {item.canonical_signature_id: item for item in cross_prime_records}
    classifications: list[ModularRouteClassification] = []

    for route in routes:
        artifact = artifact_by_key[(route.signature, route.ell)]
        trace = trace_by_key[(route.signature, route.ell)]
        template = template_by_signature[route.signature]
        cross = cross_by_canonical.get(route.canonical_signature_id)
        proof_gap = "Requires a validated Frey model, exact conductor calculation, and newform trace comparison."

        if artifact.verdict == "artifact_explained":
            klass = "artifact_explained"
            status = "artifact explained"
            rationale = artifact.explanation
            score = route.modular_followup_priority - 10
        elif trace.unusually_narrow_trace and template.template_confidence >= 0.5:
            klass = "trace_rigid_candidate"
            status = "proof-route candidate"
            rationale = "trace distribution is unusually narrow against same-size structured controls"
            score = route.modular_followup_priority + 8
        elif cross is not None and cross.trace_compatibility_class == "needs_newform_check":
            klass = "newform_check_candidate"
            status = "needs newform check"
            rationale = "non-artifact trace fingerprints repeat across primes; newform comparison is the next route"
            score = route.modular_followup_priority + 4
        elif template.template_confidence >= 0.58 and artifact.verdict != "artifact_explained":
            klass = "frey_template_candidate"
            status = "needs modular-shadow follow-up"
            rationale = "Frey template confidence is reasonable, but trace data is not rigid yet"
            score = route.modular_followup_priority + 1
        elif artifact.verdict != "artifact_explained":
            klass = "descent_or_modular_followup_candidate"
            status = "needs modular-shadow follow-up"
            rationale = "non-artifact local geometry remains but needs a stronger descent or modular-shadow step"
            score = route.modular_followup_priority
        else:
            klass = "local_only_not_promising"
            status = "not promising"
            rationale = "local data does not survive artifact and trace filters"
            score = route.modular_followup_priority

        classifications.append(
            ModularRouteClassification(
                signature=route.signature,
                canonical_signature_id=route.canonical_signature_id,
                ell=route.ell,
                route_classification=klass,
                route_rank_score=round(score, 10),
                promotion_status=status,
                rationale=rationale,
                proof_gap=proof_gap,
            )
        )
    classifications.sort(key=lambda item: (item.promotion_status == "proof-route candidate", item.route_rank_score), reverse=True)
    return classifications
