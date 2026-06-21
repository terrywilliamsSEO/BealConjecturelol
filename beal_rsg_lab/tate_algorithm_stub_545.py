"""Safe Tate-algorithm stub for focused `(5,4,5)` branches."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .frey_reduction_diagnostics_545 import (
    FreyReductionDiagnosticRecord,
    build_frey_reduction_diagnostics_545,
)


@dataclass(frozen=True)
class TateAlgorithmStubRecord:
    """One conservative Tate-algorithm stub row."""

    signature: str
    prime: int
    valuation_mask: str
    discriminant_valuation: str
    c4_valuation: str
    c6_valuation: str
    invariant_input_status: str
    stub_reduction_type: str
    tate_algorithm_status: str
    needs_human_tate_algorithm: bool
    standard_trace_behavior_available: bool
    human_proof_obligation_remains: bool
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


def _stub_status(row: FreyReductionDiagnosticRecord) -> tuple[str, str, bool, str]:
    missing = [
        name
        for name, available in (
            ("discriminant", row.discriminant_formula_available),
            ("c4", row.c4_formula_available),
        )
        if not available
    ]
    if missing:
        return (
            "template_unknown",
            "needs_human_tate_algorithm",
            True,
            f"Missing invariant formula(s): {', '.join(missing)}.",
        )
    if row.reduction_type == "template_unknown":
        return (
            "template_unknown",
            "needs_human_tate_algorithm",
            True,
            "The valuation diagnostic did not determine a reduction type.",
        )
    if row.reduction_type == "multiplicative_reduction":
        return (
            "multiplicative_reduction",
            "valuation_stub_multiplicative",
            False,
            (
                "The valuation stub sees v_q(Delta)>0 and v_q(c4)=0. "
                "It does not determine split/non-split behavior or replace a written Tate-algorithm check."
            ),
        )
    if row.reduction_type == "additive_reduction":
        return (
            "additive_reduction",
            "valuation_stub_additive",
            False,
            "The valuation stub sees positive discriminant and c4 valuations; a human must still validate the detailed local type.",
        )
    if row.reduction_type == "good_reduction":
        return (
            "good_reduction",
            "valuation_stub_good",
            False,
            "The valuation stub sees v_q(Delta)=0 for the displayed template.",
        )
    return (
        "template_unknown",
        "needs_human_tate_algorithm",
        True,
        "Unexpected diagnostic state was downgraded to a human Tate-algorithm obligation.",
    )


def build_tate_algorithm_stub_545(
    diagnostic_rows: Iterable[FreyReductionDiagnosticRecord] | None = None,
) -> list[TateAlgorithmStubRecord]:
    """Build safe symbolic Tate-algorithm stub rows."""
    rows = list(diagnostic_rows) if diagnostic_rows is not None else build_frey_reduction_diagnostics_545()
    records: list[TateAlgorithmStubRecord] = []
    for row in sorted(rows, key=lambda item: (item.prime, item.valuation_mask)):
        reduction_type, status, needs_human, reason = _stub_status(row)
        records.append(
            TateAlgorithmStubRecord(
                signature=row.signature,
                prime=row.prime,
                valuation_mask=row.valuation_mask,
                discriminant_valuation=row.discriminant_valuation,
                c4_valuation=row.c4_valuation,
                c6_valuation=row.c6_valuation,
                invariant_input_status=row.diagnostic_status,
                stub_reduction_type=reduction_type,
                tate_algorithm_status=status,
                needs_human_tate_algorithm=needs_human,
                standard_trace_behavior_available=row.standard_trace_behavior_available,
                human_proof_obligation_remains=True,
                route_ceiling_label="worth_human_modular_review",
                reason=reason,
            )
        )
    return records


def write_tate_algorithm_stub_545_csv(
    path: Path,
    rows: Iterable[TateAlgorithmStubRecord] | None = None,
) -> Path:
    """Write `tate_algorithm_stub_545.csv` rows to `path`."""
    record_rows = list(rows) if rows is not None else build_tate_algorithm_stub_545()
    _write_csv(path, [row.to_flat_dict() for row in record_rows])
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 Tate-algorithm stub rows.")
    parser.add_argument("--output", default="tate_algorithm_stub_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_tate_algorithm_stub_545_csv(Path(args.output))
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
