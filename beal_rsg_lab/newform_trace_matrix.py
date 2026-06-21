"""Trace/newform comparison matrix for modular follow-up candidates."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class NewformTraceMatrixRecord:
    """One matrix row comparing survivor traces to available newform data."""

    signature: str
    job_id: str
    level: int
    ell: int
    frey_trace_values: tuple[str, ...]
    newform_coefficients: tuple[str, ...]
    comparison_mode: str
    matrix_classification: str
    sage_status: str
    trace_status: str
    newform_count: int
    checked_level: bool
    notes: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["frey_trace_values"] = ";".join(self.frey_trace_values)
        data["newform_coefficients"] = ";".join(self.newform_coefficients)
        return data


def _value(row: Mapping[str, Any], key: str, default: str = "") -> str:
    value = row.get(key, default)
    return "" if value is None else str(value)


def _split_ints(value: str) -> tuple[int, ...]:
    output: list[int] = []
    for part in value.split(";"):
        if not part:
            continue
        try:
            output.append(int(part))
        except ValueError:
            continue
    return tuple(output)


def _parse_signature(signature: str) -> tuple[int, int, int]:
    parts = tuple(int(part) for part in signature.split("-") if part)
    if len(parts) != 3:
        return (0, 0, 0)
    return parts  # type: ignore[return-value]


def _import_by_job(import_rows: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {_value(row, "job_id"): row for row in import_rows if _value(row, "job_id")}


def _confidence_by_signature(confidence_rows: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {_value(row, "signature"): row for row in confidence_rows if _value(row, "signature")}


def _load_payload(job: Mapping[str, Any], results_dir: Path | None = None) -> dict[str, Any]:
    result_path = Path(_value(job, "result_path"))
    if results_dir is not None:
        result_path = results_dir / f"{_value(job, 'job_id')}.json"
    if not result_path.exists():
        return {}
    try:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _trace_values(trace_row: Mapping[str, Any]) -> tuple[str, ...]:
    counts = trace_row.get("trace_counts", {})
    if not isinstance(counts, dict):
        return ()
    return tuple(sorted(str(key) for key in counts))


def _newform_coefficients(payload: Mapping[str, Any], *, level: int, ell: int) -> tuple[str, ...]:
    rows = payload.get("newform_trace_rows", [])
    if not isinstance(rows, list):
        return ()
    coeffs: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        try:
            row_level = int(row.get("level", 0))
            row_prime = int(row.get("prime", 0))
        except (TypeError, ValueError):
            continue
        if row_level != level or row_prime != ell:
            continue
        if str(row.get("status", "completed")) not in {"completed", "ok"}:
            continue
        coeffs.append(str(row.get("coefficient", "")))
    return tuple(sorted(item for item in coeffs if item))


def _modulus_for_signature(signature: str) -> int:
    exponents = [part for part in _parse_signature(signature) if part > 2]
    return min(exponents) if exponents else 0


def _classification(
    *,
    trace_status: str,
    frey_values: tuple[str, ...],
    coeffs: tuple[str, ...],
    modulus: int,
    newform_count: int,
) -> tuple[str, str]:
    if trace_status in {"control_like", "artifact_like"}:
        return "unknown", "trace_control_like"
    if not frey_values:
        return "unknown", "trace_data_insufficient"
    if not coeffs:
        return "unknown", "trace_data_insufficient"
    if set(frey_values) & set(coeffs):
        return "exact", "trace_matches_some_newform"
    if modulus:
        frey_mod = {int(value) % modulus for value in frey_values if value.lstrip("-").isdigit()}
        coeff_mod = {int(value) % modulus for value in coeffs if value.lstrip("-").isdigit()}
        if frey_mod and coeff_mod and frey_mod & coeff_mod:
            return f"mod_{modulus}", "trace_matches_some_newform"
    if newform_count > 0:
        return "exact", "trace_mismatch_candidate"
    return "unknown", "trace_data_insufficient"


def build_newform_trace_matrix(
    *,
    job_rows: Iterable[Mapping[str, Any]],
    import_rows: Iterable[Mapping[str, Any]],
    confidence_rows: Iterable[Mapping[str, Any]],
    results_dir: Path | None = None,
    only_modular_followup: bool = True,
) -> list[NewformTraceMatrixRecord]:
    """Build trace/newform comparison rows without making contradiction claims."""
    imports = _import_by_job(import_rows)
    confidence = _confidence_by_signature(confidence_rows)
    rows: list[NewformTraceMatrixRecord] = []
    for job in job_rows:
        signature = _value(job, "signature")
        if not signature:
            continue
        conf = confidence.get(signature, {})
        label = _value(conf, "updated_followup_label") or _value(job, "route_label")
        if only_modular_followup and label != "modular_followup_candidate":
            continue
        imported = imports.get(_value(job, "job_id"), {})
        payload = _load_payload(job, results_dir=results_dir)
        trace_rows = payload.get("trace_rows", [])
        if not isinstance(trace_rows, list):
            trace_rows = []
        candidate_levels = _split_ints(_value(job, "candidate_levels"))
        checked_levels = set(_split_ints(_value(imported, "checked_levels")))
        if not candidate_levels:
            candidate_levels = tuple(sorted(checked_levels)) or (0,)
        if not trace_rows:
            trace_rows = [{"ell": 0, "trace_counts": {}}]
        for level in candidate_levels:
            for trace_row in trace_rows:
                if not isinstance(trace_row, dict):
                    continue
                try:
                    ell = int(trace_row.get("ell", 0))
                except (TypeError, ValueError):
                    ell = 0
                frey_values = _trace_values(trace_row)
                coeffs = _newform_coefficients(payload, level=level, ell=ell)
                mode, classification = _classification(
                    trace_status=_value(imported, "trace_match_status", "not_checked"),
                    frey_values=frey_values,
                    coeffs=coeffs,
                    modulus=_modulus_for_signature(signature),
                    newform_count=int(_value(imported, "newform_count", "0") or 0),
                )
                notes = (
                    "Newform q-coefficients were unavailable in the imported Sage JSON."
                    if not coeffs
                    else "Compared available survivor traces against imported newform coefficients."
                )
                rows.append(
                    NewformTraceMatrixRecord(
                        signature=signature,
                        job_id=_value(job, "job_id"),
                        level=level,
                        ell=ell,
                        frey_trace_values=frey_values,
                        newform_coefficients=coeffs,
                        comparison_mode=mode,
                        matrix_classification=classification,
                        sage_status=_value(imported, "sage_status", "missing"),
                        trace_status=_value(imported, "trace_match_status", "not_checked"),
                        newform_count=int(_value(imported, "newform_count", "0") or 0),
                        checked_level=level in checked_levels,
                        notes=notes,
                    )
                )
    rows.sort(key=lambda row: (row.signature, not row.checked_level, row.level, row.ell))
    return rows

