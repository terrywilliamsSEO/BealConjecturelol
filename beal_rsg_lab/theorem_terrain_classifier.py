"""Classify generalized Fermat signatures by likely theorem terrain."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

try:  # pragma: no cover - fallback is for unusual import packaging only.
    from importlib.resources import files
except ImportError:  # pragma: no cover
    files = None  # type: ignore[assignment]

from .number_theory import is_prime, prime_factors
from .rsg_residue_engine import Signature
from .signature_normalizer import canonicalize_signature, normalize_signature


@dataclass(frozen=True)
class KnownTheoremTerrain:
    """Known theorem-terrain metadata.

    These records route cases to known proof families or artifact explanations.
    They do not contain proofs and must not be used as proof claims.
    """

    case_id: str
    signature: Signature
    terrain_label: str
    known_status_label: str
    expected_route: str
    notes: str
    source_placeholder: str
    should_promote_without_external_check: bool
    artifact_collision_expected: bool = False
    should_resolve_to: str = ""
    ell: int | None = None

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["ell"] = "" if self.ell is None else self.ell
        return data


@dataclass(frozen=True)
class TheoremTerrainRecord:
    """Terrain classification for one signature, optionally at a local prime."""

    signature: Signature
    canonical_signature: Signature
    canonical_signature_id: str
    ell: int
    terrain_label: str
    structural_terrain_labels: tuple[str, ...]
    known_status_label: str
    expected_route: str
    theorem_match_id: str
    should_promote_without_external_check: bool
    artifact_collision_expected: bool
    should_resolve_to: str
    diagonal_flt_style: bool
    two_equal_exponents: bool
    fourth_power_bridge: bool
    mixed_prime_signature: bool
    known_modular_method_shape: bool
    local_obstruction_shape: bool
    artifact_prone_shape: bool
    terrain_route_label: str
    local_support_summary: str
    rationale: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["canonical_signature"] = "-".join(str(part) for part in self.canonical_signature)
        data["structural_terrain_labels"] = ";".join(self.structural_terrain_labels)
        return data


def _library_text() -> str:
    if files is not None:
        return files("beal_rsg_lab").joinpath("known_theorem_library.json").read_text(encoding="utf-8")
    return Path(__file__).with_name("known_theorem_library.json").read_text(encoding="utf-8")


def _parse_signature(raw: Any, *, case_id: str) -> Signature:
    if not isinstance(raw, list | tuple) or len(raw) != 3:
        raise ValueError(f"terrain case {case_id} must have a length-3 signature")
    signature = tuple(int(part) for part in raw)
    if any(part <= 2 for part in signature):
        raise ValueError(f"terrain case {case_id} has exponent <= 2")
    return signature  # type: ignore[return-value]


def _terrain_from_dict(raw: dict[str, Any]) -> KnownTheoremTerrain:
    case_id = str(raw.get("case_id", "")).strip()
    if not case_id:
        raise ValueError("terrain record missing case_id")
    return KnownTheoremTerrain(
        case_id=case_id,
        signature=_parse_signature(raw.get("signature"), case_id=case_id),
        ell=int(raw["ell"]) if raw.get("ell") is not None else None,
        terrain_label=str(raw.get("terrain_label", "unknown_route")).strip() or "unknown_route",
        known_status_label=str(raw.get("known_status_label", "unclassified_terrain")).strip(),
        expected_route=str(raw.get("expected_route", "unknown")).strip() or "unknown",
        notes=str(raw.get("notes", "")).strip(),
        source_placeholder=str(raw.get("source_placeholder", "")).strip(),
        should_promote_without_external_check=bool(raw.get("should_promote_without_external_check", False)),
        artifact_collision_expected=bool(raw.get("artifact_collision_expected", False)),
        should_resolve_to=str(raw.get("should_resolve_to", "")).strip(),
    )


def load_known_theorem_library(path: str | Path | None = None) -> list[KnownTheoremTerrain]:
    """Load theorem-terrain metadata."""
    if path is None:
        payload = json.loads(_library_text())
    else:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    raw_records = payload.get("terrains", [])
    if not isinstance(raw_records, list):
        raise ValueError("known theorem library must contain a terrains list")
    records = [_terrain_from_dict(raw) for raw in raw_records]
    seen: set[tuple[str, int | None]] = set()
    for record in records:
        key = (record.case_id, record.ell)
        if key in seen:
            raise ValueError(f"duplicate theorem terrain record {record.case_id!r}")
        seen.add(key)
    return records


def _exponent_prime_signature(exponent: int) -> tuple[int, ...]:
    return prime_factors(exponent)


def _is_diagonal_flt_style(signature: Signature) -> bool:
    if signature[0] == signature[1] == signature[2]:
        return True
    supports = tuple(_exponent_prime_signature(exponent) for exponent in signature)
    return all(len(support) == 1 for support in supports) and len({support[0] for support in supports}) == 1


def _is_mixed_prime_signature(signature: Signature) -> bool:
    if _is_diagonal_flt_style(signature):
        return False
    if all(is_prime(exponent) and exponent % 2 == 1 for exponent in signature):
        return len(set(signature)) == 3
    non_fourth = tuple(exponent for exponent in signature if exponent != 4)
    return 4 in signature and len(non_fourth) >= 2 and all(is_prime(exponent) and exponent % 2 == 1 for exponent in non_fourth)


def _theorem_match(
    signature: Signature,
    ell: int | None,
    library: list[KnownTheoremTerrain],
) -> KnownTheoremTerrain | None:
    canonical, _ = canonicalize_signature(signature)
    exact_candidates = [record for record in library if record.signature == signature]
    if ell is not None:
        exact_local = [record for record in exact_candidates if record.ell == ell]
        if exact_local:
            return exact_local[0]
    exact_global = [record for record in exact_candidates if record.ell is None]
    if exact_global:
        return exact_global[0]

    canonical_candidates = [
        record
        for record in library
        if canonicalize_signature(record.signature)[0] == canonical
    ]
    if ell is not None:
        canonical_local = [record for record in canonical_candidates if record.ell == ell]
        if canonical_local:
            return canonical_local[0]
    canonical_global = [record for record in canonical_candidates if record.ell is None]
    return canonical_global[0] if canonical_global else None


def _support_summary(
    primitive_classification: object | None,
    artifact_assessment: object | None,
    trace_record: object | None,
    route_classification: object | None,
) -> str:
    parts: list[str] = []
    if primitive_classification is not None:
        parts.append(f"primitive={getattr(primitive_classification, 'classification', 'unknown')}")
    if artifact_assessment is not None:
        parts.append(f"artifact={getattr(artifact_assessment, 'verdict', 'unknown')}")
    if trace_record is not None:
        parts.append(f"trace_rigid={getattr(trace_record, 'unusually_narrow_trace', False)}")
    if route_classification is not None:
        parts.append(f"modular={getattr(route_classification, 'route_classification', 'unknown')}")
    return ";".join(parts) if parts else "structural_only"


def classify_theorem_terrain(
    signature: Signature,
    *,
    ell: int | None = None,
    primitive_classification: object | None = None,
    artifact_assessment: object | None = None,
    trace_record: object | None = None,
    route_classification: object | None = None,
    library: list[KnownTheoremTerrain] | None = None,
) -> TheoremTerrainRecord:
    """Classify a signature into theorem terrain without claiming a proof."""
    terrain_library = library if library is not None else load_known_theorem_library()
    normalized = normalize_signature(signature)
    match = _theorem_match(signature, ell, terrain_library)
    counts = {exponent: signature.count(exponent) for exponent in set(signature)}
    two_equal = sorted(counts.values()) == [1, 2]
    fourth_bridge = 4 in signature
    diagonal = _is_diagonal_flt_style(signature)
    mixed = _is_mixed_prime_signature(signature)

    artifact_verdict = getattr(artifact_assessment, "verdict", "")
    artifact_prone = artifact_verdict == "artifact_explained" or (match is not None and match.known_status_label == "subgroup_artifact")

    primitive_name = getattr(primitive_classification, "classification", "")
    local_obstruction = primitive_name in {"direct_primitive_obstruction", "mandatory_single_divisor"}
    if getattr(trace_record, "unusually_narrow_trace", False):
        local_obstruction = True

    expected_route = match.expected_route if match is not None else "unknown"
    known_modular_shape = (
        expected_route == "modular_method"
        or (not diagonal and not artifact_prone and (two_equal or fourth_bridge or mixed))
    )

    labels: list[str] = []
    if diagonal:
        labels.append("diagonal_flt_style")
    if two_equal:
        labels.append("two_equal_exponents")
    if fourth_bridge:
        labels.append("fourth_power_bridge")
    if mixed:
        labels.append("mixed_prime_signature")
    if known_modular_shape:
        labels.append("known_modular_method_shape")
    if local_obstruction:
        labels.append("local_obstruction_shape")
    if artifact_prone:
        labels.append("artifact_prone_shape")
    if not labels:
        labels.append("unknown_route")

    if artifact_prone:
        terrain_label = "artifact_prone_shape"
        route_label = "artifact_like"
        rationale = "terrain is subgroup-artifact prone or artifact explainer demoted it"
    elif match is not None and match.known_status_label in {"known_solved_terrain", "follows_FLT_style_reduction", "descent_terrain"}:
        terrain_label = match.terrain_label
        route_label = "theorem_terrain_route"
        rationale = "known solved theorem terrain is routed structurally, not by local obstruction"
    elif local_obstruction:
        terrain_label = "local_obstruction_shape"
        route_label = "calibrated_route_candidate"
        rationale = "exact zero-support or trace rigidity supplied local obstruction support"
    elif known_modular_shape:
        terrain_label = match.terrain_label if match is not None else "known_modular_method_shape"
        route_label = "needs_external_sage_check"
        rationale = "generalized Fermat terrain needs external Frey/newform or descent checks"
    else:
        terrain_label = match.terrain_label if match is not None else labels[0]
        route_label = "not_promising_yet"
        rationale = "terrain is not enough for a calibrated route"

    if expected_route == "unknown" and match is None:
        if diagonal:
            expected_route = "descent_or_modularity"
        elif artifact_prone:
            expected_route = "artifact"
        elif local_obstruction:
            expected_route = "local_obstruction"
        elif known_modular_shape:
            expected_route = "modular_method"

    return TheoremTerrainRecord(
        signature=signature,
        canonical_signature=normalized.canonical_signature,
        canonical_signature_id=normalized.canonical_signature_id,
        ell=ell or 0,
        terrain_label=terrain_label,
        structural_terrain_labels=tuple(labels),
        known_status_label=match.known_status_label if match is not None else "unclassified_terrain",
        expected_route=expected_route,
        theorem_match_id=match.case_id if match is not None else "",
        should_promote_without_external_check=match.should_promote_without_external_check if match is not None else False,
        artifact_collision_expected=match.artifact_collision_expected if match is not None else False,
        should_resolve_to=match.should_resolve_to if match is not None else "",
        diagonal_flt_style=diagonal,
        two_equal_exponents=two_equal,
        fourth_power_bridge=fourth_bridge,
        mixed_prime_signature=mixed,
        known_modular_method_shape=known_modular_shape,
        local_obstruction_shape=local_obstruction,
        artifact_prone_shape=artifact_prone,
        terrain_route_label=route_label,
        local_support_summary=_support_summary(
            primitive_classification,
            artifact_assessment,
            trace_record,
            route_classification,
        ),
        rationale=rationale,
    )
