"""Modular-shadow routing scores for sparse follow-up signatures."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import log2

from .artifact_explainer import ArtifactAssessment
from .finite_field_trace_probe import TraceProbeRecord
from .frey_template_library import FreyTemplateRecord
from .signature_normalizer import normalize_signature
from .unit_survivor_geometry import UnitSurvivorGeometry


@dataclass(frozen=True)
class ModularShadowRoute:
    """Route score for one signature/prime row."""

    signature: tuple[int, int, int]
    canonical_signature_id: str
    ell: int
    local_sparse_geometry_score: float
    radical_support_pattern: str
    bad_prime_pressure: float
    conductor_complexity_score: float
    exponent_repetition_score: float
    fourth_power_bridge_score: float
    template_confidence: float
    trace_rigidity_score: float
    artifact_verdict: str
    modular_followup_priority: float
    route_summary: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        return data


def build_modular_shadow_route(
    geometry: UnitSurvivorGeometry,
    artifact: ArtifactAssessment,
    template: FreyTemplateRecord,
    trace: TraceProbeRecord,
) -> ModularShadowRoute:
    """Combine geometry, template, artifact, and trace data."""
    normalized = normalize_signature(geometry.signature)
    sparse_score = -log2(max(geometry.density, 1e-12)) + geometry.survivor_compression_score
    bad_prime_pressure = len(template.radical_support) + (1.0 if 2 in template.radical_support else 0.0)
    repetition_score = 1.25 if normalized.has_repeated_exponent else 0.0
    fourth_score = 1.0 if normalized.fourth_power_involvement else 0.0
    artifact_penalty = 8.0 if artifact.verdict == "artifact_explained" else 0.0
    priority = (
        sparse_score
        + 0.6 * template.conductor_complexity_score
        + 1.2 * repetition_score
        + fourth_score
        + 2.0 * trace.trace_rigidity_score
        + 5.0 * template.template_confidence
        - artifact_penalty
    )
    if artifact.verdict == "artifact_explained":
        summary = "demoted because sparse geometry is explained by subgroup artifacts"
    elif trace.unusually_narrow_trace:
        summary = "non-artifact sparse row with unusually narrow finite-field traces"
    else:
        summary = "non-artifact sparse row with Frey-template route but trace data not rigid yet"
    return ModularShadowRoute(
        signature=geometry.signature,
        canonical_signature_id=normalized.canonical_signature_id,
        ell=geometry.ell,
        local_sparse_geometry_score=round(sparse_score, 10),
        radical_support_pattern=";".join(str(part) for part in template.radical_support),
        bad_prime_pressure=round(bad_prime_pressure, 10),
        conductor_complexity_score=template.conductor_complexity_score,
        exponent_repetition_score=repetition_score,
        fourth_power_bridge_score=fourth_score,
        template_confidence=template.template_confidence,
        trace_rigidity_score=trace.trace_rigidity_score,
        artifact_verdict=artifact.verdict,
        modular_followup_priority=round(priority, 10),
        route_summary=summary,
    )


def build_modular_shadow_routes(
    geometries: list[UnitSurvivorGeometry],
    artifacts: list[ArtifactAssessment],
    templates: list[FreyTemplateRecord],
    traces: list[TraceProbeRecord],
) -> list[ModularShadowRoute]:
    """Build route records for sparse target geometries."""
    artifact_by_key = {(item.signature, item.ell): item for item in artifacts}
    template_by_signature = {item.signature: item for item in templates}
    trace_by_key = {(item.signature, item.ell): item for item in traces}
    routes = [
        build_modular_shadow_route(
            geometry,
            artifact_by_key[(geometry.signature, geometry.ell)],
            template_by_signature[geometry.signature],
            trace_by_key[(geometry.signature, geometry.ell)],
        )
        for geometry in geometries
    ]
    routes.sort(key=lambda item: item.modular_followup_priority, reverse=True)
    return routes
