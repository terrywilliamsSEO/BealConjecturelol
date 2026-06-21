"""Focused trace-comparison audit for `(5,4,5)`."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class TraceComparisonAuditRecord:
    """One explicit trace comparison row for `(5,4,5)`."""

    signature: str
    level: int
    prime: int
    good_prime_for_level: bool
    frey_survivor_trace_values: tuple[str, ...]
    newform_trace_values: tuple[str, ...]
    comparison_mode: str
    comparison_classification: str
    narrow_trace_interpretation: str
    next_action: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["frey_survivor_trace_values"] = ";".join(self.frey_survivor_trace_values)
        data["newform_trace_values"] = ";".join(self.newform_trace_values)
        return data


def _value(row: Mapping[str, Any], key: str, default: str = "") -> str:
    value = row.get(key, default)
    return "" if value is None else str(value)


def _split_values(value: str) -> tuple[str, ...]:
    return tuple(part for part in value.split(";") if part)


def build_trace_comparison_audit_545(
    matrix_rows: Iterable[Mapping[str, Any]],
) -> list[TraceComparisonAuditRecord]:
    """Build explicit trace comparison rows for the focused 5-4-5 packet."""
    rows: list[TraceComparisonAuditRecord] = []
    for row in matrix_rows:
        if _value(row, "signature") != "5-4-5":
            continue
        try:
            level = int(_value(row, "level", "0") or 0)
            prime = int(_value(row, "ell", "0") or 0)
        except ValueError:
            level = 0
            prime = 0
        good = bool(level and prime and level % prime != 0)
        frey_values = _split_values(_value(row, "frey_trace_values"))
        newform_values = _split_values(_value(row, "newform_coefficients"))
        if not good:
            classification = "insufficient_bad_prime_for_level"
            interpretation = (
                "The narrow trace is a local survivor/Frey finite-field signal, but this prime divides the candidate level, "
                "so it is not yet a standard good-prime comparison against level-220 newforms."
            )
        elif not newform_values:
            classification = "insufficient_missing_newform_traces"
            interpretation = (
                "The survivor trace set is narrow, but imported Sage data does not include newform coefficients at this good prime."
            )
        else:
            classification = _value(row, "matrix_classification", "trace_data_insufficient")
            interpretation = "Imported survivor and newform trace data can be compared for this good prime."
        rows.append(
            TraceComparisonAuditRecord(
                signature="5-4-5",
                level=level,
                prime=prime,
                good_prime_for_level=good,
                frey_survivor_trace_values=frey_values,
                newform_trace_values=newform_values,
                comparison_mode=_value(row, "comparison_mode", "unknown"),
                comparison_classification=classification,
                narrow_trace_interpretation=interpretation,
                next_action=(
                    "Compute newform q-expansion coefficients at small primes not dividing the final justified level, "
                    "then compare exactly or modulo the justified representation prime."
                ),
            )
        )
    if not rows:
        rows.append(
            TraceComparisonAuditRecord(
                signature="5-4-5",
                level=220,
                prime=0,
                good_prime_for_level=False,
                frey_survivor_trace_values=(),
                newform_trace_values=(),
                comparison_mode="unknown",
                comparison_classification="trace_data_insufficient",
                narrow_trace_interpretation="No trace matrix rows were available for 5-4-5.",
                next_action="Run Sage with q-expansion export enabled and regenerate the focused audit.",
            )
        )
    return rows

