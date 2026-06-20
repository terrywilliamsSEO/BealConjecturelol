"""Resolve collisions between local artifacts and signature-level terrain."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Protocol

from .rsg_residue_engine import Signature
from .theorem_terrain_classifier import TheoremTerrainRecord


class CalibrationCollisionLike(Protocol):
    case_id: str
    signature_text: str
    expected_route: str
    actual_route_label: str
    terrain_label: str
    known_status_label: str
    collision_class: str
    collision_resolved_route_label: str
    collision_rationale: str


@dataclass(frozen=True)
class RouteCollisionRecord:
    """Signature-level route-collision summary."""

    case_id: str
    signature: Signature
    signature_text: str
    expected_route: str
    terrain_label: str
    known_status_label: str
    theorem_route_label: str
    initial_route_label: str
    resolved_route_label: str
    collision_class: str
    local_artifact_prime_count: int
    local_artifact_primes: tuple[int, ...]
    local_artifact_evidence: str
    signature_terrain_evidence: str
    modular_route_evidence: str
    unit_geometry_evidence: str
    padic_lift_evidence: str
    artifact_row_count: int
    sparse_unit_row_count: int
    nonartifact_sparse_row_count: int
    modular_route_row_count: int
    padic_descent_row_count: int
    should_promote_without_external_check: bool
    rationale: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = self.signature_text
        data["local_artifact_primes"] = ";".join(str(prime) for prime in self.local_artifact_primes)
        return data


def _count_matching(keys: Iterable[tuple[Signature, int]], mapping: dict[tuple[Signature, int], object], attr: str, values: set[object]) -> int:
    return sum(1 for key in keys if key in mapping and getattr(mapping[key], attr, None) in values)


def _evidence_for_keys(
    keys: Iterable[tuple[Signature, int]],
    mapping: dict[tuple[Signature, int], object],
    attr: str,
) -> str:
    parts: list[str] = []
    for key in keys:
        _, ell = key
        if key in mapping:
            parts.append(f"ell={ell}:{getattr(mapping[key], attr, 'unknown')}")
    return ";".join(parts) if parts else "none"


def resolve_route_collision(
    *,
    case_id: str,
    signature: Signature,
    keys: list[tuple[Signature, int]],
    terrain: TheoremTerrainRecord,
    primitive_by_key: dict[tuple[Signature, int], object],
    artifact_by_key: dict[tuple[Signature, int], object],
    route_by_key: dict[tuple[Signature, int], object],
    unit_lift_by_key: dict[tuple[Signature, int], object],
    padic_by_key: dict[tuple[Signature, int], object],
    expected_route: str,
    initial_route_label: str,
) -> RouteCollisionRecord:
    """Resolve local artifact-vs-terrain collisions at signature level."""
    artifact_keys = [
        key
        for key in keys
        if key in artifact_by_key and getattr(artifact_by_key[key], "verdict", "") == "artifact_explained"
    ]
    artifact_primes = tuple(sorted({ell for _, ell in artifact_keys}))
    sparse_rows = _count_matching(keys, primitive_by_key, "classification", {"sparse_unit_survivor"})
    nonartifact_sparse_rows = sum(
        1
        for key in keys
        if key in primitive_by_key
        and getattr(primitive_by_key[key], "classification", "") == "sparse_unit_survivor"
        and (key not in artifact_by_key or getattr(artifact_by_key[key], "verdict", "") != "artifact_explained")
    )
    modular_rows = _count_matching(
        keys,
        route_by_key,
        "route_classification",
        {"newform_check_candidate", "frey_template_candidate", "trace_rigid_candidate"},
    )
    padic_rows = sum(1 for key in keys if key in padic_by_key and getattr(padic_by_key[key], "descent_like_lift", False))
    unit_rigid_rows = sum(1 for key in keys if key in unit_lift_by_key and getattr(unit_lift_by_key[key], "collapse_or_rigid", False))

    known_artifact = terrain.expected_route == "artifact" or terrain.known_status_label == "subgroup_artifact"
    terrain_route = terrain.terrain_route_label
    terrain_supports_external = (
        terrain_route == "needs_external_sage_check"
        or terrain.expected_route == "modular_method"
        or terrain.known_modular_method_shape
        or terrain.fourth_power_bridge
        or terrain.mixed_prime_signature
        or terrain.two_equal_exponents
    )
    artifact_ratio = len(artifact_keys) / max(1, sparse_rows)

    if initial_route_label == "calibrated_route_candidate" and not terrain.should_promote_without_external_check:
        collision_class = "overpromotion_risk"
        resolved = "needs_external_sage_check" if terrain_supports_external else "not_promising_yet"
        rationale = "promotion blocked because terrain does not allow promotion without an external check"
    elif known_artifact:
        collision_class = "artifact_dominates"
        resolved = "artifact_like"
        rationale = "known subgroup-artifact terrain remains globally demoted"
    elif terrain_route == "theorem_terrain_route":
        collision_class = "terrain_dominates"
        resolved = "theorem_terrain_route"
        rationale = "known theorem terrain overrides weak or local artifact signals without claiming a new proof"
    elif terrain.artifact_collision_expected and artifact_keys and terrain.should_resolve_to:
        collision_class = "mixed_needs_external_check"
        resolved = terrain.should_resolve_to
        rationale = "artifact collision is expected for this terrain, so route conservatively to external checks"
    elif terrain_supports_external and artifact_keys and (modular_rows or expected_route == "modular_method"):
        collision_class = "mixed_needs_external_check"
        resolved = "needs_external_sage_check"
        rationale = "local artifact evidence exists but signature-level modular terrain is stronger than one local row"
    elif artifact_keys and sparse_rows and len(artifact_keys) == sparse_rows and modular_rows == 0:
        collision_class = "artifact_dominates"
        resolved = "artifact_like"
        rationale = "all sparse evidence is explained by subgroup or tiny-prime artifacts"
    elif terrain_supports_external:
        collision_class = "terrain_dominates"
        resolved = "needs_external_sage_check"
        rationale = "signature terrain points to external modular/descent checks"
    elif artifact_ratio > 0.5:
        collision_class = "artifact_dominates"
        resolved = "artifact_like"
        rationale = "artifact evidence dominates available signature evidence"
    else:
        collision_class = "insufficient_evidence"
        resolved = "not_promising_yet"
        rationale = "signature has no calibrated route beyond local data"

    return RouteCollisionRecord(
        case_id=case_id,
        signature=signature,
        signature_text="-".join(str(part) for part in signature),
        expected_route=expected_route,
        terrain_label=terrain.terrain_label,
        known_status_label=terrain.known_status_label,
        theorem_route_label=terrain.terrain_route_label,
        initial_route_label=initial_route_label,
        resolved_route_label=resolved,
        collision_class=collision_class,
        local_artifact_prime_count=len(artifact_primes),
        local_artifact_primes=artifact_primes,
        local_artifact_evidence=_evidence_for_keys(artifact_keys, artifact_by_key, "verdict"),
        signature_terrain_evidence=f"{terrain.terrain_label}:{terrain.known_status_label}:{terrain.expected_route}",
        modular_route_evidence=_evidence_for_keys(
            [key for key in keys if key in route_by_key],
            route_by_key,
            "route_classification",
        ),
        unit_geometry_evidence=(
            f"sparse={sparse_rows};nonartifact_sparse={nonartifact_sparse_rows};unit_rigid_or_collapsed={unit_rigid_rows}"
        ),
        padic_lift_evidence=f"descent_like_rows={padic_rows}",
        artifact_row_count=len(artifact_keys),
        sparse_unit_row_count=sparse_rows,
        nonartifact_sparse_row_count=nonartifact_sparse_rows,
        modular_route_row_count=modular_rows,
        padic_descent_row_count=padic_rows,
        should_promote_without_external_check=terrain.should_promote_without_external_check,
        rationale=rationale,
    )


def resolved_known_mismatch_rows(
    calibration_records: Iterable[CalibrationCollisionLike],
    collision_records: Iterable[RouteCollisionRecord],
) -> list[dict[str, object]]:
    """Rows where a prior artifact collision is conservatively resolved."""
    collision_by_case = {record.case_id: record for record in collision_records}
    rows: list[dict[str, object]] = []
    for record in calibration_records:
        collision = collision_by_case[record.case_id]
        if collision.collision_class not in {"mixed_needs_external_check", "terrain_dominates"}:
            continue
        if collision.local_artifact_prime_count == 0:
            continue
        if record.actual_route_label not in {"needs_external_sage_check", "theorem_terrain_route"}:
            continue
        rows.append(
            {
                "case_id": record.case_id,
                "signature": record.signature_text,
                "collision_class": collision.collision_class,
                "resolved_route_label": collision.resolved_route_label,
                "local_artifact_primes": ";".join(str(prime) for prime in collision.local_artifact_primes),
                "signature_terrain_evidence": collision.signature_terrain_evidence,
                "modular_route_evidence": collision.modular_route_evidence,
                "why_not_promoted": "resolved only to external/theorem route; no proof promotion allowed",
                "rationale": collision.rationale,
            }
        )
    return rows


def still_blocked_mismatch_rows(
    calibration_records: Iterable[CalibrationCollisionLike],
    collision_records: Iterable[RouteCollisionRecord],
) -> list[dict[str, object]]:
    """Rows still blocked after collision resolution."""
    collision_by_case = {record.case_id: record for record in collision_records}
    rows: list[dict[str, object]] = []
    for record in calibration_records:
        collision = collision_by_case[record.case_id]
        if record.actual_route_label != "known_case_mismatch" and collision.collision_class not in {"overpromotion_risk"}:
            continue
        rows.append(
            {
                "case_id": record.case_id,
                "signature": record.signature_text,
                "collision_class": collision.collision_class,
                "terrain_label": record.terrain_label,
                "expected_route": record.expected_route,
                "actual_route_label": record.actual_route_label,
                "local_artifact_primes": ";".join(str(prime) for prime in collision.local_artifact_primes),
                "rationale": collision.rationale,
            }
        )
    return rows


def route_collision_report_markdown(
    *,
    output_dir: Path,
    collision_rows: list[dict[str, object]],
    resolved_rows: list[dict[str, object]],
    blocked_rows: list[dict[str, object]],
) -> str:
    """Generate a human-readable route-collision report."""
    generated = datetime.now().isoformat(timespec="seconds")
    class_counts: dict[str, int] = {}
    for row in collision_rows:
        klass = str(row["collision_class"])
        class_counts[klass] = class_counts.get(klass, 0) + 1
    lines = [
        "# Route-Collision Triage Report",
        "",
        f"Generated: `{generated}`",
        f"Output directory: `{output_dir.as_posix()}`",
        "",
        "## Interpretation Guardrail",
        "",
        "This report separates local artifact rows from signature-level theorem terrain. It does not promote proof claims.",
        "",
        "A single artifact-prone local prime can force caution, but it should not globally demote a known modular or generalized Fermat signature unless artifacts dominate the whole signature.",
        "",
        "## Counts",
        "",
        f"- Signature collision rows: `{len(collision_rows)}`.",
        f"- Resolved known mismatches: `{len(resolved_rows)}`.",
        f"- Still blocked mismatches: `{len(blocked_rows)}`.",
    ]
    for klass in sorted(class_counts):
        lines.append(f"- `{klass}`: `{class_counts[klass]}`.")

    lines.extend(
        [
            "",
            "## Resolved Known Mismatches",
            "",
        ]
    )
    if not resolved_rows:
        lines.append("No artifact collisions were resolved in this run.")
    else:
        lines.extend(
            [
                "| case | signature | collision | artifact primes | resolved route | why not promoted |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in resolved_rows:
            lines.append(
                f"| {row['case_id']} | {row['signature']} | {row['collision_class']} | "
                f"{row['local_artifact_primes']} | {row['resolved_route_label']} | {row['why_not_promoted']} |"
            )

    lines.extend(
        [
            "",
            "## Still Blocked",
            "",
        ]
    )
    if not blocked_rows:
        lines.append("No known-case mismatches remain blocked after collision resolution.")
    else:
        lines.extend(
            [
                "| case | signature | collision | expected | actual | rationale |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in blocked_rows:
            lines.append(
                f"| {row['case_id']} | {row['signature']} | {row['collision_class']} | "
                f"{row['expected_route']} | {row['actual_route_label']} | {row['rationale']} |"
            )

    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `route_collision_summary.csv`: aggregate signature-level collision evidence.",
            "- `resolved_known_mismatches.csv`: artifact collisions resolved to external/theorem routes.",
            "- `still_blocked_mismatches.csv`: rows that remain blocked after triage.",
            "",
            "## Promotion Rule",
            "",
            "Resolved collision rows are still not proofs. They may route to Sage/newform or theorem terrain, but never to promotion without the full calibrated ladder.",
            "",
        ]
    )
    return "\n".join(lines)
