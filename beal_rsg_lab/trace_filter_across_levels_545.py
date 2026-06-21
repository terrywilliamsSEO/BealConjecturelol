"""Trace filtering across candidate comparison levels for `(5,4,5)`."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .candidate_level_generator_545 import CandidateLevelRecord545, build_candidate_levels_545
from .candidate_level_importer_545 import (
    CandidateLevelCoefficientRow545,
    CandidateLevelImportRecord545,
    import_candidate_level_newforms_545,
)
from .frey_reduction_diagnostics_545 import (
    FreyReductionDiagnosticRecord,
    SINGLE_MASKS_545,
    TARGET_PRIMES_545,
    build_frey_reduction_diagnostics_545,
)
from .frey_trace_possibility_545 import FreyTracePossibilityRecord
from .good_prime_selector import select_good_primes_545
from .multiplicative_reduction_congruence_545 import allowed_multiplicative_values_mod_5
from .frey_trace_possibility_545 import build_frey_trace_possibilities_545


SAFE_TRACE_FILTER_ACROSS_LEVELS_LABELS = {
    "level_trace_mismatch_candidate",
    "level_survivor_exists",
    "level_data_insufficient",
    "coefficient_field_blocked",
}


@dataclass(frozen=True)
class TraceFilterAcrossLevelsRecord545:
    """One level-level trace and branch-filter summary."""

    signature: str
    level: int
    factorization: str
    includes_11: bool
    conductor_plausibility_label: str
    import_status: str
    coefficient_field_status: str
    newform_count: int
    selected_good_primes: str
    tested_good_primes: str
    eliminated_newforms: str
    surviving_newforms: str
    unresolved_newforms: str
    first_eliminators: str
    unit_surviving_branch_count: int
    single_mask_surviving_branch_count: int
    unresolved_branch_count: int
    level_trace_label: str
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


def _join_newforms(indices: Iterable[int]) -> str:
    return ";".join(f"newform_{index}" for index in sorted(dict.fromkeys(indices)))


def _coefficient_as_int(value: str) -> int | None:
    text = value.strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _coefficient_mod_values(row: CandidateLevelCoefficientRow545 | None, residual_modulus: int) -> set[int]:
    if row is None:
        return set()
    values = set()
    for part in row.coefficient_mod_5.split(";"):
        text = part.strip()
        if text.lstrip("-").isdigit():
            values.add(int(text) % residual_modulus)
    coeff_int = _coefficient_as_int(row.coefficient)
    if coeff_int is not None:
        values.add(coeff_int % residual_modulus)
    return values


def _unit_eliminated(
    *,
    trace_row: FreyTracePossibilityRecord | None,
    coefficient_values: set[int],
    residual_modulus: int,
) -> tuple[str, str]:
    if trace_row is None or not trace_row.possible_traces:
        return "unresolved", "missing Frey trace possibilities"
    if not coefficient_values:
        return "unresolved", "missing coefficient reduction modulo 5"
    trace_values = {trace % residual_modulus for trace in trace_row.possible_traces}
    if trace_values & coefficient_values:
        return "survives", "unit trace branch has a matching coefficient residue"
    return "eliminated", "unit trace branch has no matching coefficient residue"


def _single_mask_status(
    *,
    diagnostics: list[FreyReductionDiagnosticRecord],
    coefficient_values: set[int],
    prime: int,
    residual_modulus: int,
) -> tuple[str, int, int]:
    if not coefficient_values:
        return "unresolved", 0, len(SINGLE_MASKS_545)
    eliminated = 0
    survives = 0
    unresolved = 0
    allowed = set(allowed_multiplicative_values_mod_5(prime, residual_modulus))
    by_mask = {row.valuation_mask: row for row in diagnostics}
    for mask in SINGLE_MASKS_545:
        diagnostic = by_mask.get(mask)
        if diagnostic is None or diagnostic.reduction_type != "multiplicative_reduction":
            unresolved += 1
        elif coefficient_values & allowed:
            survives += 1
        else:
            eliminated += 1
    if survives:
        return "survives", survives, unresolved
    if unresolved:
        return "unresolved", survives, unresolved
    if eliminated == len(SINGLE_MASKS_545):
        return "eliminated", survives, unresolved
    return "unresolved", survives, unresolved


def _newform_indices(import_record: CandidateLevelImportRecord545, rows: list[CandidateLevelCoefficientRow545]) -> tuple[int, ...]:
    indices = set(range(max(import_record.newform_count, 0)))
    indices.update(row.newform_index for row in rows)
    return tuple(sorted(indices))


def build_trace_filter_across_levels_545(
    candidate_rows: Iterable[CandidateLevelRecord545] | None = None,
    import_rows: Iterable[CandidateLevelImportRecord545] | None = None,
    coefficient_rows: Iterable[CandidateLevelCoefficientRow545] | None = None,
    frey_trace_rows: Iterable[FreyTracePossibilityRecord] | None = None,
    diagnostic_rows: Iterable[FreyReductionDiagnosticRecord] | None = None,
    *,
    residual_modulus: int = 5,
    target_primes: tuple[int, ...] = TARGET_PRIMES_545,
) -> list[TraceFilterAcrossLevelsRecord545]:
    """Apply unit trace and single-mask multiplicative filters across candidate levels."""
    candidates = list(candidate_rows) if candidate_rows is not None else build_candidate_levels_545()
    imports = list(import_rows or [])
    coefficients = list(coefficient_rows or [])
    if frey_trace_rows is None:
        good_primes = select_good_primes_545(level=220, bound=max(target_primes), allow_residual_prime=False)
        frey_traces = build_frey_trace_possibilities_545(good_primes)
    else:
        frey_traces = list(frey_trace_rows)
    diagnostics = list(diagnostic_rows) if diagnostic_rows is not None else build_frey_reduction_diagnostics_545()
    import_by_level = {row.level: row for row in imports}
    trace_by_prime = {row.prime: row for row in frey_traces}
    diagnostics_by_prime: dict[int, list[FreyReductionDiagnosticRecord]] = {}
    for row in diagnostics:
        diagnostics_by_prime.setdefault(row.prime, []).append(row)
    records: list[TraceFilterAcrossLevelsRecord545] = []
    for candidate in candidates:
        import_record = import_by_level.get(candidate.level)
        if import_record is None:
            import_record = CandidateLevelImportRecord545(
                signature="5-4-5",
                level=candidate.level,
                weight=2,
                sage_status="missing",
                level_status="missing",
                schema_valid=True,
                newform_count=0,
                selected_good_primes="",
                coefficient_row_count=0,
                rational_integer_coefficient_count=0,
                nonrational_coefficient_count=0,
                unclear_coefficient_count=0,
                coefficient_field_status="no_coefficients",
                import_status="missing",
                error_message="candidate-level import row missing",
                source_path="",
                route_ceiling_label="worth_human_modular_review",
            )
        level_coefficients = [row for row in coefficients if row.level == candidate.level]
        tested_primes = tuple(prime for prime in target_primes if candidate.level % prime != 0)
        if import_record.import_status != "completed" or not import_record.schema_valid:
            label = "level_data_insufficient"
            reason = "Candidate-level Sage data is missing, partial, failed, or schema-invalid."
            if import_record.coefficient_field_status == "coefficient_field_blocked":
                label = "coefficient_field_blocked"
                reason = "Coefficient fields lack usable reductions modulo 5."
            records.append(
                TraceFilterAcrossLevelsRecord545(
                    signature="5-4-5",
                    level=candidate.level,
                    factorization=candidate.factorization,
                    includes_11=candidate.includes_11,
                    conductor_plausibility_label=candidate.conductor_plausibility_label,
                    import_status=import_record.import_status,
                    coefficient_field_status=import_record.coefficient_field_status,
                    newform_count=import_record.newform_count,
                    selected_good_primes=import_record.selected_good_primes,
                    tested_good_primes=";".join(str(prime) for prime in tested_primes),
                    eliminated_newforms="",
                    surviving_newforms="",
                    unresolved_newforms="",
                    first_eliminators="",
                    unit_surviving_branch_count=0,
                    single_mask_surviving_branch_count=0,
                    unresolved_branch_count=0,
                    level_trace_label=label,
                    route_ceiling_label="worth_human_modular_review",
                    reason=reason,
                )
            )
            continue
        if import_record.coefficient_field_status == "coefficient_field_blocked":
            records.append(
                TraceFilterAcrossLevelsRecord545(
                    signature="5-4-5",
                    level=candidate.level,
                    factorization=candidate.factorization,
                    includes_11=candidate.includes_11,
                    conductor_plausibility_label=candidate.conductor_plausibility_label,
                    import_status=import_record.import_status,
                    coefficient_field_status=import_record.coefficient_field_status,
                    newform_count=import_record.newform_count,
                    selected_good_primes=import_record.selected_good_primes,
                    tested_good_primes=";".join(str(prime) for prime in tested_primes),
                    eliminated_newforms="",
                    surviving_newforms="",
                    unresolved_newforms=_join_newforms(_newform_indices(import_record, level_coefficients)),
                    first_eliminators="",
                    unit_surviving_branch_count=0,
                    single_mask_surviving_branch_count=0,
                    unresolved_branch_count=import_record.coefficient_row_count,
                    level_trace_label="coefficient_field_blocked",
                    route_ceiling_label="worth_human_modular_review",
                    reason="All imported coefficient rows for this level lack usable mod-5 reductions.",
                )
            )
            continue
        indices = _newform_indices(import_record, level_coefficients)
        eliminated: list[int] = []
        surviving: list[int] = []
        unresolved: list[int] = []
        first_eliminators: dict[int, int] = {}
        unit_surviving_count = 0
        single_surviving_count = 0
        unresolved_count = 0
        if not indices:
            label = "level_trace_mismatch_candidate"
            reason = "Sage reports no weight-2 newforms at this candidate level."
        else:
            for index in indices:
                newform_eliminated = False
                newform_survives = False
                newform_unresolved = False
                for prime in tested_primes:
                    coeff = next(
                        (
                            row
                            for row in level_coefficients
                            if row.newform_index == index and row.prime == prime
                        ),
                        None,
                    )
                    coeff_values = _coefficient_mod_values(coeff, residual_modulus)
                    unit_status, _ = _unit_eliminated(
                        trace_row=trace_by_prime.get(prime),
                        coefficient_values=coeff_values,
                        residual_modulus=residual_modulus,
                    )
                    single_status, single_survives, single_unresolved = _single_mask_status(
                        diagnostics=diagnostics_by_prime.get(prime, []),
                        coefficient_values=coeff_values,
                        prime=prime,
                        residual_modulus=residual_modulus,
                    )
                    if unit_status == "survives":
                        unit_surviving_count += 1
                    if single_status == "survives":
                        single_surviving_count += single_survives
                    if unit_status == "unresolved":
                        unresolved_count += 1
                    unresolved_count += single_unresolved
                    if unit_status == "eliminated" and single_status == "eliminated":
                        newform_eliminated = True
                        first_eliminators.setdefault(index, prime)
                        break
                    if unit_status == "survives" or single_status == "survives":
                        newform_survives = True
                    if unit_status == "unresolved" or single_status == "unresolved":
                        newform_unresolved = True
                if newform_eliminated:
                    eliminated.append(index)
                elif newform_survives:
                    surviving.append(index)
                elif newform_unresolved:
                    unresolved.append(index)
                else:
                    unresolved.append(index)
            if len(eliminated) == len(indices):
                label = "level_trace_mismatch_candidate"
                reason = "Every imported newform has at least one focused good prime eliminating unit and single-mask branches."
            elif surviving:
                label = "level_survivor_exists"
                reason = "At least one imported newform has a surviving unit or single-mask branch at this candidate level."
            else:
                label = "level_data_insufficient"
                reason = "Imported rows did not produce a complete level-level branch decision."
        if label not in SAFE_TRACE_FILTER_ACROSS_LEVELS_LABELS:
            label = "level_data_insufficient"
            reason = "Unexpected cross-level trace label was downgraded to level_data_insufficient."
        records.append(
            TraceFilterAcrossLevelsRecord545(
                signature="5-4-5",
                level=candidate.level,
                factorization=candidate.factorization,
                includes_11=candidate.includes_11,
                conductor_plausibility_label=candidate.conductor_plausibility_label,
                import_status=import_record.import_status,
                coefficient_field_status=import_record.coefficient_field_status,
                newform_count=import_record.newform_count,
                selected_good_primes=import_record.selected_good_primes,
                tested_good_primes=";".join(str(prime) for prime in tested_primes),
                eliminated_newforms=_join_newforms(eliminated),
                surviving_newforms=_join_newforms(surviving),
                unresolved_newforms=_join_newforms(unresolved),
                first_eliminators=";".join(
                    f"newform_{index}:q={prime}" for index, prime in sorted(first_eliminators.items())
                ),
                unit_surviving_branch_count=unit_surviving_count,
                single_mask_surviving_branch_count=single_surviving_count,
                unresolved_branch_count=unresolved_count,
                level_trace_label=label,
                route_ceiling_label="worth_human_modular_review",
                reason=reason,
            )
        )
    records.sort(key=lambda row: row.level)
    return records


def write_trace_filter_across_levels_545_csv(
    path: Path,
    rows: Iterable[TraceFilterAcrossLevelsRecord545],
) -> Path:
    """Write `trace_filter_across_levels_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 trace filters across candidate levels.")
    parser.add_argument("--input-json", default="candidate_level_newforms_545.json")
    parser.add_argument("--output", default="trace_filter_across_levels_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    candidates = build_candidate_levels_545()
    import_rows, coefficient_rows = import_candidate_level_newforms_545(Path(args.input_json), candidates)
    rows = build_trace_filter_across_levels_545(candidates, import_rows, coefficient_rows)
    write_trace_filter_across_levels_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
