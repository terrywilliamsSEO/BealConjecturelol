"""Generate optional Sage scripts for modular follow-up route sketches."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import shutil
from typing import Iterable, Protocol


class SageCalibrationLike(Protocol):
    case_id: str
    signature_text: str
    expected_route: str
    actual_route_label: str
    strongest_prime: int


class SageScoreLike(Protocol):
    case_id: str
    signature: str
    output_label: str
    discovery_readiness_score: float
    proof_route_priority: float


@dataclass(frozen=True)
class SageExportRecord:
    """Manifest row for one exported Sage script."""

    case_id: str
    signature: str
    ell: int
    script_path: str
    sage_available: bool
    export_status: str
    command_hint: str
    notes: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _parse_signature(signature_text: str) -> tuple[int, int, int]:
    parts = tuple(int(part) for part in signature_text.split("-"))
    if len(parts) != 3:
        raise ValueError(f"bad signature text {signature_text!r}")
    return parts  # type: ignore[return-value]


def sage_script_text(*, case_id: str, signature: tuple[int, int, int], ell: int) -> str:
    """Return a standalone Sage script for finite-field trace probing."""
    p, q, r = signature
    return f'''# Auto-generated Sage follow-up script for {case_id}.
# This script is a route-audit helper only. It does not prove a theorem.

ell = {ell}
p, q, r = {p}, {q}, {r}
F = GF(ell)

def power_image(exponent):
    return sorted(set(F(a) ** exponent for a in range(1, ell)), key=lambda x: int(x))

Hp = power_image(p)
Hq = power_image(q)
Hr = set(power_image(r))

trace_counts = {{}}
singular_skipped = 0
triple_count = 0

for u in Hp:
    for v in Hq:
        w = u + v
        if w not in Hr:
            continue
        triple_count += 1
        if u == 0 or v == 0 or u + v == 0:
            singular_skipped += 1
            continue
        # y^2 = x(x-u)(x+v) = x^3 + (v-u)x^2 - uvx
        E = EllipticCurve(F, [0, v - u, 0, -u * v, 0])
        trace = ell + 1 - E.cardinality()
        trace_counts[ZZ(trace)] = trace_counts.get(ZZ(trace), 0) + 1

print("case_id =", "{case_id}")
print("signature =", ({p}, {q}, {r}))
print("ell =", ell)
print("survivor triples =", triple_count)
print("singular skipped =", singular_skipped)
print("trace counts =", sorted(trace_counts.items()))

# Placeholder for later level/newform work:
# 1. Replace the symbolic Frey model with a validated minimal model.
# 2. Compute candidate conductor levels N.
# 3. For each N, compare Newforms(Gamma0(N)) traces with the a_ell values above.
'''


def _select_exports(
    scores: list[SageScoreLike],
    records: dict[str, SageCalibrationLike],
    limit: int,
) -> list[tuple[SageScoreLike, SageCalibrationLike]]:
    priority_labels = {"calibrated_route_candidate", "needs_external_sage_check"}
    selected: list[tuple[SageScoreLike, SageCalibrationLike]] = []
    for score in sorted(scores, key=lambda item: (item.output_label in priority_labels, item.discovery_readiness_score, item.proof_route_priority), reverse=True):
        record = records.get(score.case_id)
        if record is None:
            continue
        if score.output_label in priority_labels or record.expected_route == "modular_method":
            selected.append((score, record))
        if len(selected) >= limit:
            break
    return selected


def export_sage_scripts(
    scores: Iterable[SageScoreLike],
    calibration_records: Iterable[SageCalibrationLike],
    output_dir: Path,
    *,
    limit: int = 12,
) -> list[SageExportRecord]:
    """Write optional Sage scripts and return manifest rows."""
    score_list = list(scores)
    record_by_case = {record.case_id: record for record in calibration_records}
    export_dir = output_dir / "sage_exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    sage_available = shutil.which("sage") is not None
    rows: list[SageExportRecord] = []

    for score, record in _select_exports(score_list, record_by_case, limit):
        signature = _parse_signature(record.signature_text)
        ell = int(record.strongest_prime or 0)
        if ell <= 2:
            ell = 5
        filename = f"{record.case_id}_{record.signature_text}_ell{ell}.sage".replace("-", "_")
        path = export_dir / filename
        path.write_text(sage_script_text(case_id=record.case_id, signature=signature, ell=ell), encoding="utf-8")
        rows.append(
            SageExportRecord(
                case_id=record.case_id,
                signature=record.signature_text,
                ell=ell,
                script_path=path.as_posix(),
                sage_available=sage_available,
                export_status="script_written_sage_available" if sage_available else "script_written_sage_unavailable",
                command_hint=f"sage {path.as_posix()}",
                notes="Script computes finite-field traces only; newform checks require validated conductor levels.",
            )
        )
    return rows
