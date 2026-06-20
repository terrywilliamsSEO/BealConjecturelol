"""Explain sparse unit-survivor rows using subgroup-size artifacts when possible."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from statistics import mean

from .unit_survivor_geometry import UnitSurvivorGeometry


@dataclass(frozen=True)
class ArtifactAssessment:
    """Artifact assessment for one sparse unit-survivor row."""

    signature: tuple[int, int, int]
    ell: int
    verdict: str
    artifact_reasons: tuple[str, ...]
    same_size_control_count: int
    same_size_density_mean: float
    same_size_density_min: float
    same_size_density_max: float
    residual_density_gap: float
    same_size_explained: bool
    lemma_candidate_rank: str
    explanation: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["artifact_reasons"] = ";".join(self.artifact_reasons)
        return data


def _shape_key(geometry: UnitSurvivorGeometry) -> str:
    return "-".join(str(size) for size in geometry.subgroup_size_shape)


def _artifact_reasons(geometry: UnitSurvivorGeometry, same_size_count: int) -> tuple[str, ...]:
    reasons: list[str] = []
    if geometry.ell <= 5:
        reasons.append("tiny_prime")
    if min(geometry.subgroup_size_shape) <= 1:
        reasons.append("trivial_power_image")
    if 2 in geometry.subgroup_size_shape:
        reasons.append("order_two_power_image")
    half_size = (geometry.ell - 1) // 2
    if half_size in geometry.subgroup_size_shape and geometry.ell <= 23:
        reasons.append("quadratic_half_group_controls")
    if same_size_count > 1:
        reasons.append("identical_subgroup_size_family")
    return tuple(reasons)


def explain_artifacts(geometries: list[UnitSurvivorGeometry]) -> list[ArtifactAssessment]:
    """Assess whether sparse rows are explained by subgroup size and simple group facts."""
    groups: dict[str, list[UnitSurvivorGeometry]] = defaultdict(list)
    for geometry in geometries:
        groups[_shape_key(geometry)].append(geometry)

    assessments: list[ArtifactAssessment] = []
    for geometry in geometries:
        peers = groups[_shape_key(geometry)]
        densities = [peer.density for peer in peers]
        density_mean = mean(densities)
        residual_gap = density_mean - geometry.density
        reasons = _artifact_reasons(geometry, len(peers))
        same_size_explained = len(peers) > 1 and geometry.density >= min(densities) - 1e-12

        if reasons and same_size_explained:
            verdict = "artifact_explained"
            rank = "artifact explained"
            explanation = "sparsity is explained by tiny images or by an identical subgroup-size family"
        elif reasons and ("order_two_power_image" in reasons or "tiny_prime" in reasons):
            verdict = "artifact_explained"
            rank = "artifact explained"
            explanation = "sparsity follows from an order-two/tiny power image such as {1,-1}"
        elif same_size_explained and residual_gap <= 0.01:
            verdict = "artifact_explained"
            rank = "artifact explained"
            explanation = "same-size structured controls reproduce the density"
        elif residual_gap > 0.02:
            verdict = "needs_modular_shadow_follow_up"
            rank = "needs modular-shadow follow-up"
            explanation = "row remains below same-size structured controls after simple artifact checks"
        else:
            verdict = "needs_modular_shadow_follow_up"
            rank = "needs modular-shadow follow-up"
            explanation = "sparsity is not fully explained, but no lift collapse is known yet"

        assessments.append(
            ArtifactAssessment(
                signature=geometry.signature,
                ell=geometry.ell,
                verdict=verdict,
                artifact_reasons=reasons,
                same_size_control_count=len(peers),
                same_size_density_mean=round(density_mean, 10),
                same_size_density_min=round(min(densities), 10),
                same_size_density_max=round(max(densities), 10),
                residual_density_gap=round(residual_gap, 10),
                same_size_explained=same_size_explained,
                lemma_candidate_rank=rank,
                explanation=explanation,
            )
        )
    assessments.sort(key=lambda item: (item.verdict != "artifact_explained", item.residual_density_gap), reverse=True)
    return assessments
