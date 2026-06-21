"""Single-mask newform pressure rows for focused `(5,4,5)` branches."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .frey_reduction_diagnostics_545 import (
    FreyReductionDiagnosticRecord,
    TARGET_PRIMES_545,
    build_frey_reduction_diagnostics_545,
)
from .tate_algorithm_stub_545 import TateAlgorithmStubRecord, build_tate_algorithm_stub_545
from .trace_congruence_filter_545 import TraceCongruenceFilterRecord


SAFE_SINGLE_MASK_BRANCH_LABELS = {
    "eliminated_by_unit_trace",
    "multiplicative_reduction_condition",
    "additive_reduction_condition",
    "needs_human_tate_algorithm",
    "unresolved_single_mask",
}
SAFE_PRIME_PRESSURE_LABELS = {
    "local_case_elimination_candidate",
    "local_coverage_gap",
    "unresolved_single_mask",
}


@dataclass(frozen=True)
class SingleMaskNewformPressureRecord:
    """One focused q/mask row combining trace, coefficient, and reduction data."""

    signature: str
    prime: int
    valuation_mask: str
    unit_trace_result: str
    unit_eliminated_newform_count: int
    unit_surviving_newform_count: int
    newform_coefficients: str
    reduction_type: str
    tate_algorithm_status: str
    standard_trace_behavior_available: bool
    branch_classification: str
    single_mask_resolved: bool
    prime_local_label: str
    route_ceiling_label: str
    reason: str

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


def _coefficient_summary(rows: list[TraceCongruenceFilterRecord]) -> str:
    if not rows:
        return "missing"
    return ";".join(
        f"newform_{row.newform_index}:{row.newform_coefficient or 'missing'}"
        for row in sorted(rows, key=lambda item: item.newform_index)
    )


def _unit_trace_result(rows: list[TraceCongruenceFilterRecord]) -> tuple[str, int, int]:
    eliminated = sum(1 for row in rows if row.filter_classification == "eliminated")
    surviving = sum(1 for row in rows if row.filter_classification == "survives")
    if not rows:
        return "unit_trace_missing", eliminated, surviving
    if eliminated and surviving:
        return "partial_unit_trace_elimination", eliminated, surviving
    if eliminated:
        return "all_newforms_unit_eliminated", eliminated, surviving
    if surviving:
        return "unit_trace_survivor_exists", eliminated, surviving
    return "unit_trace_insufficient_or_unclear", eliminated, surviving


def _branch_classification(
    *,
    diagnostic: FreyReductionDiagnosticRecord,
    tate: TateAlgorithmStubRecord,
    unit_eliminated_newform_count: int,
) -> tuple[str, bool, str]:
    if tate.needs_human_tate_algorithm:
        return (
            "needs_human_tate_algorithm",
            False,
            "The valuation inputs are insufficient for the Tate-algorithm stub.",
        )
    if diagnostic.reduction_type == "good_reduction":
        if diagnostic.standard_trace_behavior_available and unit_eliminated_newform_count:
            return (
                "eliminated_by_unit_trace",
                True,
                "Good reduction would let the unit trace comparison apply to this branch.",
            )
        return (
            "unresolved_single_mask",
            False,
            "Good reduction was indicated, but no unit trace elimination is available for this q.",
        )
    if diagnostic.reduction_type == "multiplicative_reduction":
        return (
            "multiplicative_reduction_condition",
            True,
            "The branch is reduced to a multiplicative-reduction local condition, not a proof claim.",
        )
    if diagnostic.reduction_type == "additive_reduction":
        return (
            "additive_reduction_condition",
            True,
            "The branch is reduced to an additive-reduction local condition, not a proof claim.",
        )
    return (
        "unresolved_single_mask",
        False,
        "The reduction diagnostic did not classify this single-mask branch.",
    )


def _prime_labels(rows: list[dict[str, object]]) -> dict[int, str]:
    labels: dict[int, str] = {}
    by_prime: dict[int, list[dict[str, object]]] = {}
    for row in rows:
        by_prime.setdefault(int(row["prime"]), []).append(row)
    for prime, prime_rows in by_prime.items():
        branch_labels = {str(row["branch_classification"]) for row in prime_rows}
        all_resolved = all(bool(row["single_mask_resolved"]) for row in prime_rows)
        unit_eliminated = any(int(row["unit_eliminated_newform_count"]) > 0 for row in prime_rows)
        if branch_labels & {"needs_human_tate_algorithm", "unresolved_single_mask"}:
            labels[prime] = "local_coverage_gap"
        elif all_resolved and unit_eliminated:
            labels[prime] = "local_case_elimination_candidate"
        else:
            labels[prime] = "unresolved_single_mask"
    return labels


def build_single_mask_newform_pressure_545(
    filter_rows: Iterable[TraceCongruenceFilterRecord],
    diagnostic_rows: Iterable[FreyReductionDiagnosticRecord] | None = None,
    tate_rows: Iterable[TateAlgorithmStubRecord] | None = None,
    *,
    target_primes: tuple[int, ...] = TARGET_PRIMES_545,
) -> list[SingleMaskNewformPressureRecord]:
    """Combine q=13/q=17 trace, coefficient, and reduction data for single masks."""
    diagnostics = list(diagnostic_rows) if diagnostic_rows is not None else build_frey_reduction_diagnostics_545()
    tate_records = list(tate_rows) if tate_rows is not None else build_tate_algorithm_stub_545(diagnostics)
    diagnostic_by_key = {(row.prime, row.valuation_mask): row for row in diagnostics}
    tate_by_key = {(row.prime, row.valuation_mask): row for row in tate_records}

    targets = set(target_primes)
    filters_by_prime: dict[int, list[TraceCongruenceFilterRecord]] = {}
    for row in filter_rows:
        if row.prime in targets:
            filters_by_prime.setdefault(row.prime, []).append(row)

    raw_rows: list[dict[str, object]] = []
    for key in sorted(diagnostic_by_key):
        prime, mask = key
        if prime not in targets:
            continue
        diagnostic = diagnostic_by_key[key]
        tate = tate_by_key.get(key)
        if tate is None:
            tate = build_tate_algorithm_stub_545([diagnostic])[0]
        prime_filters = filters_by_prime.get(prime, [])
        unit_result, eliminated, surviving = _unit_trace_result(prime_filters)
        branch_label, resolved, reason = _branch_classification(
            diagnostic=diagnostic,
            tate=tate,
            unit_eliminated_newform_count=eliminated,
        )
        if branch_label not in SAFE_SINGLE_MASK_BRANCH_LABELS:
            branch_label = "unresolved_single_mask"
            resolved = False
            reason = "Unexpected branch label was downgraded to unresolved_single_mask."
        raw_rows.append(
            {
                "signature": diagnostic.signature,
                "prime": prime,
                "valuation_mask": mask,
                "unit_trace_result": unit_result,
                "unit_eliminated_newform_count": eliminated,
                "unit_surviving_newform_count": surviving,
                "newform_coefficients": _coefficient_summary(prime_filters),
                "reduction_type": diagnostic.reduction_type,
                "tate_algorithm_status": tate.tate_algorithm_status,
                "standard_trace_behavior_available": diagnostic.standard_trace_behavior_available,
                "branch_classification": branch_label,
                "single_mask_resolved": resolved,
                "reason": reason,
            }
        )

    prime_labels = _prime_labels(raw_rows)
    records: list[SingleMaskNewformPressureRecord] = []
    for row in raw_rows:
        prime_label = prime_labels.get(int(row["prime"]), "local_coverage_gap")
        if prime_label not in SAFE_PRIME_PRESSURE_LABELS:
            prime_label = "local_coverage_gap"
        records.append(
            SingleMaskNewformPressureRecord(
                signature=str(row["signature"]),
                prime=int(row["prime"]),
                valuation_mask=str(row["valuation_mask"]),
                unit_trace_result=str(row["unit_trace_result"]),
                unit_eliminated_newform_count=int(row["unit_eliminated_newform_count"]),
                unit_surviving_newform_count=int(row["unit_surviving_newform_count"]),
                newform_coefficients=str(row["newform_coefficients"]),
                reduction_type=str(row["reduction_type"]),
                tate_algorithm_status=str(row["tate_algorithm_status"]),
                standard_trace_behavior_available=bool(row["standard_trace_behavior_available"]),
                branch_classification=str(row["branch_classification"]),
                single_mask_resolved=bool(row["single_mask_resolved"]),
                prime_local_label=prime_label,
                route_ceiling_label="worth_human_modular_review",
                reason=str(row["reason"]),
            )
        )
    return records


def write_single_mask_newform_pressure_545_csv(
    path: Path,
    rows: Iterable[SingleMaskNewformPressureRecord] | None = None,
) -> Path:
    """Write `single_mask_newform_pressure_545.csv` rows to `path`."""
    record_rows = list(rows) if rows is not None else build_single_mask_newform_pressure_545([])
    _write_csv(path, [row.to_flat_dict() for row in record_rows])
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 single-mask pressure rows.")
    parser.add_argument("--output", default="single_mask_newform_pressure_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_single_mask_newform_pressure_545_csv(Path(args.output))
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
