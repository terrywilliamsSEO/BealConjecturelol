"""JSON-backed calibration cases for generalized Fermat route testing."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

try:  # pragma: no cover - fallback is for unusual import packaging only.
    from importlib.resources import files
except ImportError:  # pragma: no cover
    files = None  # type: ignore[assignment]

from .rsg_residue_engine import Signature


KNOWN_STATUSES = {"known_impossible", "known_possible", "open_or_unknown", "calibration_only"}
EXPECTED_ROUTES = {"FLT_style", "modular_method", "descent", "local_obstruction", "artifact", "unknown"}


@dataclass(frozen=True)
class KnownCase:
    """One known or calibration-only generalized Fermat case."""

    case_id: str
    signature: Signature
    family_label: str
    known_status: str
    expected_route: str
    notes: str
    source_placeholder: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        return data


def _default_library_text() -> str:
    if files is not None:
        resource = files("beal_rsg_lab").joinpath("known_cases.json")
        return resource.read_text(encoding="utf-8")
    return Path(__file__).with_name("known_cases.json").read_text(encoding="utf-8")


def _parse_signature(raw: Any, *, case_id: str) -> Signature:
    if not isinstance(raw, list | tuple) or len(raw) != 3:
        raise ValueError(f"case {case_id} must have a length-3 signature")
    signature = tuple(int(part) for part in raw)
    if any(part <= 2 for part in signature):
        raise ValueError(f"case {case_id} has exponent <= 2")
    return signature  # type: ignore[return-value]


def _case_from_dict(raw: dict[str, Any]) -> KnownCase:
    case_id = str(raw.get("case_id", "")).strip()
    if not case_id:
        raise ValueError("known case missing case_id")
    signature = _parse_signature(raw.get("signature"), case_id=case_id)
    known_status = str(raw.get("known_status", "")).strip()
    expected_route = str(raw.get("expected_route", "")).strip()
    if known_status not in KNOWN_STATUSES:
        raise ValueError(f"case {case_id} has invalid known_status {known_status!r}")
    if expected_route not in EXPECTED_ROUTES:
        raise ValueError(f"case {case_id} has invalid expected_route {expected_route!r}")
    return KnownCase(
        case_id=case_id,
        signature=signature,
        family_label=str(raw.get("family_label", "")).strip() or "unknown_family",
        known_status=known_status,
        expected_route=expected_route,
        notes=str(raw.get("notes", "")).strip(),
        source_placeholder=str(raw.get("source_placeholder", "")).strip(),
    )


def load_known_cases(path: str | Path | None = None) -> list[KnownCase]:
    """Load the JSON-backed calibration library.

    The bundled library is intentionally modest. It is a calibration harness,
    not a complete theorem database.
    """
    if path is None:
        payload = json.loads(_default_library_text())
    else:
        source = Path(path)
        payload = json.loads(source.read_text(encoding="utf-8"))
    raw_cases = payload.get("cases", [])
    if not isinstance(raw_cases, list):
        raise ValueError("known case library must contain a cases list")
    cases = [_case_from_dict(raw) for raw in raw_cases]
    seen: set[str] = set()
    for case in cases:
        if case.case_id in seen:
            raise ValueError(f"duplicate known case id {case.case_id!r}")
        seen.add(case.case_id)
    return cases


def known_case_signatures(cases: list[KnownCase] | None = None) -> tuple[Signature, ...]:
    """Return unique signatures from the calibration library."""
    items = cases if cases is not None else load_known_cases()
    seen: set[Signature] = set()
    signatures: list[Signature] = []
    for case in items:
        if case.signature not in seen:
            seen.add(case.signature)
            signatures.append(case.signature)
    return tuple(signatures)
