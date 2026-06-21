"""Import level-220 newform coefficient JSON for focused trace audits."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Mapping


VALID_IMPORT_STATUSES = {"missing", "completed", "partial", "failed", "unsupported"}


@dataclass(frozen=True)
class NewformCoefficientImportSummary:
    """Schema/import summary for level-220 coefficient JSON."""

    signature: str
    level: int
    weight: int
    sage_status: str
    schema_valid: bool
    newform_count: int
    selected_good_prime_count: int
    coefficient_row_count: int
    rational_integer_coefficient_count: int
    nonrational_coefficient_count: int
    unclear_coefficient_count: int
    error_message: str
    source_path: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class NewformCoefficientRow:
    """One imported newform coefficient row."""

    signature: str
    level: int
    weight: int
    newform_index: int
    newform_label: str
    prime: int
    coefficient: str
    coefficient_field: str
    coefficient_field_kind: str
    is_rational_integer: bool
    reduction_mod_5_available: bool
    coefficient_mod_5: str
    prime_above_5_metadata: str
    row_status: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _missing(
    path: Path,
    message: str = "level_220_newform_coefficients.json is missing",
    *,
    schema_valid: bool = True,
) -> tuple[NewformCoefficientImportSummary, list[NewformCoefficientRow]]:
    return (
        NewformCoefficientImportSummary(
            signature="5-4-5",
            level=220,
            weight=2,
            sage_status="missing",
            schema_valid=schema_valid,
            newform_count=0,
            selected_good_prime_count=0,
            coefficient_row_count=0,
            rational_integer_coefficient_count=0,
            nonrational_coefficient_count=0,
            unclear_coefficient_count=0,
            error_message=message,
            source_path=path.as_posix(),
        ),
        [],
    )


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coefficient_rows_from_payload(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    flat = payload.get("coefficient_rows", [])
    if isinstance(flat, list) and flat:
        return [row for row in flat if isinstance(row, dict)]
    rows: list[Mapping[str, Any]] = []
    for newform in payload.get("newforms", []):
        if not isinstance(newform, dict):
            continue
        coefficients = newform.get("coefficients", {})
        if not isinstance(coefficients, dict):
            continue
        for prime, coefficient in coefficients.items():
            rows.append(
                {
                    "newform_index": newform.get("newform_index", 0),
                    "newform_label": newform.get("label", ""),
                    "prime": prime,
                    "coefficient": coefficient,
                    "coefficient_field": newform.get("coefficient_field", ""),
                    "coefficient_field_kind": newform.get("coefficient_field_kind", ""),
                    "is_rational_integer": str(coefficient).lstrip("-").isdigit(),
                    "reduction_mod_5_available": False,
                    "coefficient_mod_5": "",
                    "prime_above_5_metadata": "",
                    "row_status": "completed",
                }
            )
    return rows


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"true", "1", "yes"}


def import_level_220_newform_coefficients(path: Path) -> tuple[NewformCoefficientImportSummary, list[NewformCoefficientRow]]:
    """Validate and flatten level-220 coefficient JSON."""
    if not path.exists():
        return _missing(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return _missing(path, f"invalid coefficient JSON: {exc}", schema_valid=False)
    if not isinstance(payload, dict):
        return _missing(path, "coefficient JSON payload is not an object", schema_valid=False)
    level = _as_int(payload.get("level"), 0)
    weight = _as_int(payload.get("weight"), 0)
    status = str(payload.get("sage_status", "failed"))
    errors = payload.get("errors", [])
    error_message = "; ".join(str(item) for item in errors[:5]) if isinstance(errors, list) else str(errors)
    schema_valid = level == 220 and weight == 2 and status in VALID_IMPORT_STATUSES | {"completed"}
    good_primes = payload.get("selected_good_primes", payload.get("good_primes", []))
    if not isinstance(good_primes, list):
        good_primes = []
    raw_rows = _coefficient_rows_from_payload(payload)
    rows: list[NewformCoefficientRow] = []
    for row in raw_rows:
        field_kind = str(row.get("coefficient_field_kind", ""))
        coefficient = str(row.get("coefficient", ""))
        is_integer = _bool_value(row.get("is_rational_integer", coefficient.lstrip("-").isdigit()))
        reduction_available = _bool_value(row.get("reduction_mod_5_available", False))
        row_status = str(row.get("row_status", row.get("status", "completed")))
        if field_kind == "" and is_integer:
            field_kind = "rational_integer"
        elif field_kind == "":
            field_kind = "unknown"
        rows.append(
            NewformCoefficientRow(
                signature="5-4-5",
                level=level or 220,
                weight=weight or 2,
                newform_index=_as_int(row.get("newform_index"), 0),
                newform_label=str(row.get("newform_label", row.get("label", "label_unavailable"))),
                prime=_as_int(row.get("prime"), 0),
                coefficient=coefficient,
                coefficient_field=str(row.get("coefficient_field", "")),
                coefficient_field_kind=field_kind,
                is_rational_integer=is_integer,
                reduction_mod_5_available=reduction_available,
                coefficient_mod_5=str(row.get("coefficient_mod_5", "")),
                prime_above_5_metadata=str(row.get("prime_above_5_metadata", "")),
                row_status=row_status,
            )
        )
    newform_count = _as_int(payload.get("newform_count"), len({row.newform_index for row in rows}))
    rational_count = sum(1 for row in rows if row.is_rational_integer)
    nonrational_count = sum(1 for row in rows if not row.is_rational_integer)
    unclear_count = sum(
        1
        for row in rows
        if not row.is_rational_integer and not row.reduction_mod_5_available
    )
    if not schema_valid and not error_message:
        error_message = "expected level=220, weight=2, and valid sage_status"
    return (
        NewformCoefficientImportSummary(
            signature="5-4-5",
            level=level or 220,
            weight=weight or 2,
            sage_status=status,
            schema_valid=schema_valid,
            newform_count=newform_count,
            selected_good_prime_count=len(good_primes),
            coefficient_row_count=len(rows),
            rational_integer_coefficient_count=rational_count,
            nonrational_coefficient_count=nonrational_count,
            unclear_coefficient_count=unclear_count,
            error_message=error_message,
            source_path=path.as_posix(),
        ),
        rows,
    )
