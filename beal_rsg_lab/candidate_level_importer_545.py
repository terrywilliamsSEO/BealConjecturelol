"""Import Sage candidate-level newform coefficient JSON for `(5,4,5)`."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .candidate_level_generator_545 import CandidateLevelRecord545, build_candidate_levels_545


VALID_CANDIDATE_LEVEL_IMPORT_STATUSES = {"missing", "completed", "partial", "failed", "timeout", "unsupported"}
SAFE_COEFFICIENT_FIELD_STATUS_545 = {
    "all_clear",
    "mixed_or_unclear",
    "coefficient_field_blocked",
    "no_coefficients",
}


@dataclass(frozen=True)
class CandidateLevelImportRecord545:
    """One imported candidate-level summary row."""

    signature: str
    level: int
    weight: int
    sage_status: str
    level_status: str
    schema_valid: bool
    newform_count: int
    selected_good_primes: str
    coefficient_row_count: int
    rational_integer_coefficient_count: int
    nonrational_coefficient_count: int
    unclear_coefficient_count: int
    coefficient_field_status: str
    import_status: str
    error_message: str
    source_path: str
    route_ceiling_label: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class CandidateLevelCoefficientRow545:
    """One imported candidate-level coefficient row."""

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


def _write_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    row_list = list(rows)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in row_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row_list)


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"true", "1", "yes"}


def _missing_records(
    path: Path,
    candidate_rows: Iterable[CandidateLevelRecord545],
    message: str,
    *,
    schema_valid: bool = True,
) -> tuple[list[CandidateLevelImportRecord545], list[CandidateLevelCoefficientRow545]]:
    records = [
        CandidateLevelImportRecord545(
            signature="5-4-5",
            level=row.level,
            weight=2,
            sage_status="missing",
            level_status="missing",
            schema_valid=schema_valid,
            newform_count=0,
            selected_good_primes="",
            coefficient_row_count=0,
            rational_integer_coefficient_count=0,
            nonrational_coefficient_count=0,
            unclear_coefficient_count=0,
            coefficient_field_status="no_coefficients",
            import_status="missing",
            error_message=message,
            source_path=path.as_posix(),
            route_ceiling_label="worth_human_modular_review",
        )
        for row in candidate_rows
    ]
    return records, []


def _coefficient_rows_from_payload(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    rows = payload.get("coefficient_rows", [])
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    return []


def _level_rows_from_payload(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    rows = payload.get("levels", [])
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    return []


def _field_status(rows: list[CandidateLevelCoefficientRow545]) -> str:
    if not rows:
        return "no_coefficients"
    unclear = [row for row in rows if not row.is_rational_integer and not row.reduction_mod_5_available]
    if len(unclear) == len(rows):
        return "coefficient_field_blocked"
    if unclear:
        return "mixed_or_unclear"
    return "all_clear"


def import_candidate_level_newforms_545(
    path: Path,
    candidate_rows: Iterable[CandidateLevelRecord545] | None = None,
) -> tuple[list[CandidateLevelImportRecord545], list[CandidateLevelCoefficientRow545]]:
    """Validate and flatten `candidate_level_newforms_545.json`."""
    candidates = list(candidate_rows) if candidate_rows is not None else build_candidate_levels_545()
    if not path.exists():
        return _missing_records(path, candidates, "candidate_level_newforms_545.json is missing")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return _missing_records(path, candidates, f"invalid candidate-level JSON: {exc}", schema_valid=False)
    if not isinstance(payload, dict):
        return _missing_records(path, candidates, "candidate-level JSON payload is not an object", schema_valid=False)

    sage_status = str(payload.get("sage_status", "failed"))
    weight = _as_int(payload.get("weight"), 2)
    schema_valid = weight == 2 and sage_status in VALID_CANDIDATE_LEVEL_IMPORT_STATUSES | {"completed"}
    if not schema_valid:
        sage_status = sage_status if sage_status in VALID_CANDIDATE_LEVEL_IMPORT_STATUSES else "failed"
    raw_coefficients = _coefficient_rows_from_payload(payload)
    coefficient_rows: list[CandidateLevelCoefficientRow545] = []
    for row in raw_coefficients:
        coefficient = str(row.get("coefficient", ""))
        field_kind = str(row.get("coefficient_field_kind", ""))
        is_integer = _bool_value(row.get("is_rational_integer", coefficient.lstrip("-").isdigit()))
        if not field_kind:
            field_kind = "rational_integer" if is_integer else "unknown"
        coefficient_rows.append(
            CandidateLevelCoefficientRow545(
                signature="5-4-5",
                level=_as_int(row.get("level"), 0),
                weight=_as_int(row.get("weight"), weight or 2),
                newform_index=_as_int(row.get("newform_index"), 0),
                newform_label=str(row.get("newform_label", "label_unavailable")),
                prime=_as_int(row.get("prime"), 0),
                coefficient=coefficient,
                coefficient_field=str(row.get("coefficient_field", "")),
                coefficient_field_kind=field_kind,
                is_rational_integer=is_integer,
                reduction_mod_5_available=_bool_value(row.get("reduction_mod_5_available", False)),
                coefficient_mod_5=str(row.get("coefficient_mod_5", "")),
                prime_above_5_metadata=str(row.get("prime_above_5_metadata", "")),
                row_status=str(row.get("row_status", "completed")),
            )
        )

    level_payload_by_level = {_as_int(row.get("level"), 0): row for row in _level_rows_from_payload(payload)}
    records: list[CandidateLevelImportRecord545] = []
    for candidate in candidates:
        level_payload = level_payload_by_level.get(candidate.level, {})
        default_level_status = (
            sage_status
            if candidate.level not in level_payload_by_level
            and sage_status in {"partial", "failed", "timeout", "unsupported"}
            else "missing"
        )
        level_status = str(level_payload.get("level_status", default_level_status))
        level_coefficients = [row for row in coefficient_rows if row.level == candidate.level]
        rational_count = sum(1 for row in level_coefficients if row.is_rational_integer)
        nonrational_count = sum(1 for row in level_coefficients if not row.is_rational_integer)
        unclear_count = sum(1 for row in level_coefficients if not row.is_rational_integer and not row.reduction_mod_5_available)
        selected = level_payload.get("selected_good_primes", [])
        if not isinstance(selected, list):
            selected = []
        errors = level_payload.get("errors", [])
        error_message = "; ".join(str(item) for item in errors[:5]) if isinstance(errors, list) else str(errors)
        import_status = level_status if level_status in VALID_CANDIDATE_LEVEL_IMPORT_STATUSES else sage_status
        if import_status not in VALID_CANDIDATE_LEVEL_IMPORT_STATUSES:
            import_status = "failed"
            error_message = error_message or "unexpected candidate-level import status"
        field_status = _field_status(level_coefficients)
        if field_status not in SAFE_COEFFICIENT_FIELD_STATUS_545:
            field_status = "coefficient_field_blocked"
        records.append(
            CandidateLevelImportRecord545(
                signature="5-4-5",
                level=candidate.level,
                weight=weight or 2,
                sage_status=sage_status,
                level_status=level_status,
                schema_valid=schema_valid,
                newform_count=_as_int(level_payload.get("newform_count"), len({row.newform_index for row in level_coefficients})),
                selected_good_primes=";".join(str(item) for item in selected),
                coefficient_row_count=len(level_coefficients),
                rational_integer_coefficient_count=rational_count,
                nonrational_coefficient_count=nonrational_count,
                unclear_coefficient_count=unclear_count,
                coefficient_field_status=field_status,
                import_status=import_status,
                error_message=error_message,
                source_path=path.as_posix(),
                route_ceiling_label="worth_human_modular_review",
            )
        )
    return records, coefficient_rows


def write_candidate_level_import_summary_545_csv(
    path: Path,
    rows: Iterable[CandidateLevelImportRecord545],
) -> Path:
    """Write `candidate_level_import_summary_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_candidate_level_coefficient_rows_545_csv(
    path: Path,
    rows: Iterable[CandidateLevelCoefficientRow545],
) -> Path:
    """Write `candidate_level_coefficient_rows_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import focused 5-4-5 candidate-level newform JSON.")
    parser.add_argument("--input", default="candidate_level_newforms_545.json")
    parser.add_argument("--summary-output", default="candidate_level_import_summary_545.csv")
    parser.add_argument("--rows-output", default="candidate_level_coefficient_rows_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary_rows, coefficient_rows = import_candidate_level_newforms_545(Path(args.input))
    write_candidate_level_import_summary_545_csv(Path(args.summary_output), summary_rows)
    write_candidate_level_coefficient_rows_545_csv(Path(args.rows_output), coefficient_rows)
    print(Path(args.summary_output).as_posix())
    print(Path(args.rows_output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
