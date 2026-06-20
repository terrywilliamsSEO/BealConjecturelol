"""Optional SageMath hooks for future newform checks."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import shutil
import subprocess

from .modular_shadow_engine import ModularShadowRoute


@dataclass(frozen=True)
class NewformProbeRecord:
    """Status of an optional SageMath newform probe."""

    canonical_signature_id: str
    sage_available: bool
    probe_status: str
    suggested_level_notes: str
    command_hint: str
    output_excerpt: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def run_optional_newform_probe(routes: list[ModularShadowRoute]) -> list[NewformProbeRecord]:
    """Run a tiny Sage availability check and write route instructions.

    The probe intentionally does not claim anything about modularity. It only
    records whether Sage exists and how a future level/newform computation could
    be launched.
    """
    canonical_ids = sorted({route.canonical_signature_id for route in routes})
    sage_path = shutil.which("sage")
    if sage_path is None:
        return [
            NewformProbeRecord(
                canonical_signature_id=canonical_id,
                sage_available=False,
                probe_status="skipped_sage_unavailable",
                suggested_level_notes="Need explicit conductor model before computing candidate levels.",
                command_hint="Install SageMath, then compute Newforms(Gamma0(N)) for candidate conductor levels.",
                output_excerpt="SageMath executable not found on PATH.",
            )
            for canonical_id in canonical_ids
        ]

    try:
        completed = subprocess.run(
            [sage_path, "-c", "print('sage-ok')"],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        excerpt = (completed.stdout + completed.stderr).strip()[:300]
        status = "sage_available_no_level_probe"
    except Exception as exc:  # pragma: no cover - depends on local Sage install
        excerpt = str(exc)
        status = "sage_invocation_failed"

    return [
        NewformProbeRecord(
            canonical_signature_id=canonical_id,
            sage_available=True,
            probe_status=status,
            suggested_level_notes="Conductor is symbolic; level enumeration requires a validated Frey model and local minimal data.",
            command_hint="After conductor candidates N are known, run Sage: Newforms(Gamma0(N)) and compare a_ell values.",
            output_excerpt=excerpt,
        )
        for canonical_id in canonical_ids
    ]
