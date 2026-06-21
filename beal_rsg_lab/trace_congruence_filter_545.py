"""Good-prime trace congruence filters for `(5,4,5)`."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .frey_trace_possibility_545 import FreyTracePossibilityRecord
from .good_prime_selector import GoodPrimeRecord


@dataclass(frozen=True)
class TraceCongruenceFilterRecord:
    """One newform/good-prime trace comparison."""

    signature: str
    level: int
    prime: int
    newform_index: int
    newform_label: str
    coefficient_field: str
    coefficient_field_kind: str
    frey_trace_values: tuple[int, ...]
    newform_coefficient: str
    coefficient_mod_5: str
    prime_above_5_metadata: str
    comparison_mode: str
    filter_classification: str
    reason: str
    contradiction_claim_allowed: bool

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["frey_trace_values"] = ";".join(str(item) for item in self.frey_trace_values)
        return data


def load_level_220_coefficients(path: Path) -> dict[str, Any]:
    """Load Sage-exported level-220 newform coefficients if present."""
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"sage_status": "failed", "errors": ["invalid or unreadable coefficient JSON"]}
    return payload if isinstance(payload, dict) else {}


def _newform_rows(payload: Mapping[str, Any], newform_count: int) -> list[dict[str, Any]]:
    flat_rows = payload.get("coefficient_rows", [])
    if isinstance(flat_rows, list) and flat_rows:
        grouped: dict[int, dict[str, Any]] = {}
        for row in flat_rows:
            if not isinstance(row, dict):
                continue
            index = int(row.get("newform_index", 0) or 0)
            entry = grouped.setdefault(
                index,
                {
                    "newform_index": index,
                    "label": row.get("newform_label", "label_unavailable"),
                    "coefficient_field": row.get("coefficient_field", ""),
                    "coefficient_field_kind": row.get("coefficient_field_kind", ""),
                    "coefficient_rows": {},
                },
            )
            entry["coefficient_rows"][str(row.get("prime", ""))] = row
        return [grouped[index] for index in sorted(grouped)]
    rows = payload.get("newforms", [])
    if isinstance(rows, list) and rows:
        return [row for row in rows if isinstance(row, dict)]
    return [
        {
            "newform_index": index,
            "label": "label_unavailable",
            "coefficient_field": "",
            "coefficients": {},
        }
        for index in range(newform_count)
    ]


def _coefficient_as_int(value: str) -> int | None:
    text = value.strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _field_is_uncertain(field: str, coeff: str) -> bool:
    if not coeff:
        return False
    if _coefficient_as_int(coeff) is not None:
        return False
    field_lower = field.lower()
    if "rational" in field_lower or field_lower in {"qq", "integer ring", "zz"}:
        return False
    return True


def _row_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"true", "1", "yes"}


def _classify(
    *,
    frey_values: tuple[int, ...],
    coefficient: str,
    coefficient_field: str,
    coefficient_field_kind: str,
    coefficient_mod_5: str,
    reduction_mod_5_available: bool,
    residual_modulus: int,
) -> tuple[str, str, str]:
    if not coefficient:
        return "unknown", "insufficient_data", "Missing q-expansion coefficient for this good prime."
    coeff_int = _coefficient_as_int(coefficient)
    if coeff_int is not None:
        if coeff_int in set(frey_values):
            return "exact", "survives", "A Frey trace equals the newform coefficient exactly."
        if residual_modulus > 1 and any((trace - coeff_int) % residual_modulus == 0 for trace in frey_values):
            return f"mod_{residual_modulus}", "survives", f"A Frey trace is congruent to the coefficient modulo {residual_modulus}."
        return f"mod_{residual_modulus}" if residual_modulus > 1 else "exact", "eliminated", "No Frey trace matches under the selected comparison mode."
    if reduction_mod_5_available and coefficient_mod_5:
        reduced_values = {
            int(part.strip()) % residual_modulus
            for part in coefficient_mod_5.split(";")
            if part.strip().lstrip("-").isdigit()
        }
        if reduced_values and any(trace % residual_modulus in reduced_values for trace in frey_values):
            return f"mod_{residual_modulus}_with_field_reduction", "survives", "A Frey trace matches an imported coefficient-field reduction."
        if reduced_values:
            return f"mod_{residual_modulus}_with_field_reduction", "eliminated", "No Frey trace matches the imported coefficient-field reductions."
    if coefficient_field_kind == "number_field" or _field_is_uncertain(coefficient_field, coefficient):
        return (
            "unknown",
            "coefficient_field_unclear",
            "Coefficient field is not rational/integer and no reduction map was provided.",
        )
    return "unknown", "bad_comparison_mode", "Coefficient could not be interpreted as an integer."


def build_trace_congruence_filter_545(
    *,
    good_prime_rows: Iterable[GoodPrimeRecord],
    frey_trace_rows: Iterable[FreyTracePossibilityRecord],
    coefficient_payload: Mapping[str, Any],
    newform_count: int,
    residual_modulus: int = 5,
) -> list[TraceCongruenceFilterRecord]:
    """Compare Frey trace possibilities with level-220 newform coefficients."""
    selected_primes = [row.prime for row in good_prime_rows if row.selected]
    frey_by_prime = {row.prime: row for row in frey_trace_rows}
    newforms = _newform_rows(coefficient_payload, newform_count)
    rows: list[TraceCongruenceFilterRecord] = []
    for prime in selected_primes:
        frey_row = frey_by_prime.get(prime)
        frey_values = frey_row.possible_traces if frey_row is not None else ()
        for newform in newforms:
            coefficients = newform.get("coefficients", {})
            if not isinstance(coefficients, dict):
                coefficients = {}
            coefficient_row = {}
            coefficient_rows = newform.get("coefficient_rows", {})
            if isinstance(coefficient_rows, dict):
                raw = coefficient_rows.get(str(prime), {})
                coefficient_row = raw if isinstance(raw, dict) else {}
            coefficient = str(coefficient_row.get("coefficient", coefficients.get(str(prime), "")))
            mode, classification, reason = _classify(
                frey_values=frey_values,
                coefficient=coefficient,
                coefficient_field=str(coefficient_row.get("coefficient_field", newform.get("coefficient_field", ""))),
                coefficient_field_kind=str(coefficient_row.get("coefficient_field_kind", newform.get("coefficient_field_kind", ""))),
                coefficient_mod_5=str(coefficient_row.get("coefficient_mod_5", "")),
                reduction_mod_5_available=_row_bool(coefficient_row.get("reduction_mod_5_available", False)),
                residual_modulus=residual_modulus,
            )
            rows.append(
                TraceCongruenceFilterRecord(
                    signature="5-4-5",
                    level=220,
                    prime=prime,
                    newform_index=int(newform.get("newform_index", len(rows))),
                    newform_label=str(newform.get("label", "label_unavailable")),
                    coefficient_field=str(coefficient_row.get("coefficient_field", newform.get("coefficient_field", ""))),
                    coefficient_field_kind=str(coefficient_row.get("coefficient_field_kind", newform.get("coefficient_field_kind", ""))),
                    frey_trace_values=frey_values,
                    newform_coefficient=coefficient,
                    coefficient_mod_5=str(coefficient_row.get("coefficient_mod_5", "")),
                    prime_above_5_metadata=str(coefficient_row.get("prime_above_5_metadata", "")),
                    comparison_mode=mode,
                    filter_classification=classification,
                    reason=reason,
                    contradiction_claim_allowed=False,
                )
            )
    rows.sort(key=lambda row: (row.newform_index, row.prime))
    return rows
