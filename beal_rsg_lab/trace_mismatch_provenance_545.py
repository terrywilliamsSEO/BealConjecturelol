"""Trace-mismatch provenance tables for the focused `(5,4,5)` audit."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .trace_congruence_filter_545 import TraceCongruenceFilterRecord


@dataclass(frozen=True)
class TraceMismatchProvenanceRecord:
    """One provenance row for a newform/good-prime comparison."""

    signature: str
    level: int
    newform_index: int
    newform_label: str
    prime: int
    newform_coefficient: str
    frey_trace_values: tuple[int, ...]
    comparison_mode: str
    filter_classification: str
    is_first_eliminating_prime: bool
    all_eliminating_primes: tuple[int, ...]
    provenance_label: str
    contradiction_claim_allowed: bool

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["frey_trace_values"] = ";".join(str(item) for item in self.frey_trace_values)
        data["all_eliminating_primes"] = ";".join(str(item) for item in self.all_eliminating_primes)
        return data


def build_trace_mismatch_provenance_545(
    filter_rows: Iterable[TraceCongruenceFilterRecord],
) -> list[TraceMismatchProvenanceRecord]:
    """Attach first/all eliminating prime provenance to trace-filter rows."""
    rows = sorted(filter_rows, key=lambda row: (row.newform_index, row.prime))
    eliminated_by_newform: dict[int, tuple[int, ...]] = {}
    for row in rows:
        if row.filter_classification != "eliminated":
            continue
        eliminated_by_newform.setdefault(row.newform_index, tuple())
        eliminated_by_newform[row.newform_index] = tuple(
            sorted(set(eliminated_by_newform[row.newform_index] + (row.prime,)))
        )
    records: list[TraceMismatchProvenanceRecord] = []
    for row in rows:
        eliminating = eliminated_by_newform.get(row.newform_index, tuple())
        first = eliminating[0] if eliminating else None
        if row.filter_classification == "eliminated":
            label = "eliminating_comparison"
        elif row.filter_classification == "survives":
            label = "surviving_comparison"
        else:
            label = "incomplete_comparison"
        records.append(
            TraceMismatchProvenanceRecord(
                signature=row.signature,
                level=row.level,
                newform_index=row.newform_index,
                newform_label=row.newform_label,
                prime=row.prime,
                newform_coefficient=row.newform_coefficient,
                frey_trace_values=row.frey_trace_values,
                comparison_mode=row.comparison_mode,
                filter_classification=row.filter_classification,
                is_first_eliminating_prime=row.prime == first and row.filter_classification == "eliminated",
                all_eliminating_primes=eliminating,
                provenance_label=label,
                contradiction_claim_allowed=False,
            )
        )
    return records


def trace_mismatch_provenance_markdown(rows: Iterable[TraceMismatchProvenanceRecord]) -> str:
    """Render a human-readable provenance report."""
    row_list = list(rows)
    by_newform: dict[int, list[TraceMismatchProvenanceRecord]] = {}
    for row in row_list:
        by_newform.setdefault(row.newform_index, []).append(row)
    lines = [
        "# Trace Mismatch Provenance For `(5,4,5)`",
        "",
        "This report records where the current level-220 trace filter survives or eliminates each newform slot. It is an audit artifact only.",
        "",
    ]
    if not row_list:
        lines.append("No trace-filter rows were available.")
        return "\n".join(lines)
    for index in sorted(by_newform):
        newform_rows = sorted(by_newform[index], key=lambda row: row.prime)
        eliminating = newform_rows[0].all_eliminating_primes if newform_rows else tuple()
        first = eliminating[0] if eliminating else "none"
        lines.extend(
            [
                f"## Newform `{index}`",
                "",
                f"- First eliminating prime: `{first}`.",
                f"- All eliminating primes: `{';'.join(str(item) for item in eliminating) or 'none'}`.",
                "",
                "| q | a_q | Frey traces | mode | classification | first eliminator |",
                "| ---: | --- | --- | --- | --- | --- |",
            ]
        )
        for row in newform_rows:
            traces = ";".join(str(item) for item in row.frey_trace_values) or "none"
            lines.append(
                f"| {row.prime} | `{row.newform_coefficient or 'missing'}` | `{traces}` | "
                f"`{row.comparison_mode}` | `{row.filter_classification}` | `{row.is_first_eliminating_prime}` |"
            )
        lines.append("")
    lines.extend(
        [
            "## Interpretation Boundary",
            "",
            "The provenance label is computational route evidence. It does not certify the Frey attachment, conductor calculation, level lowering, residual irreducibility, or global exclusion step.",
            "",
        ]
    )
    return "\n".join(lines)
