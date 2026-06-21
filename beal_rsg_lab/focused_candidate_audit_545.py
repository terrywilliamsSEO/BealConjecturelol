"""Focused modular-method review packet for `(5,4,5)`."""

from __future__ import annotations

import csv
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .assumption_register import AssumptionRecord, build_assumption_register_545
from .frey_trace_possibility_545 import FreyTracePossibilityRecord, build_frey_trace_possibilities_545
from .frey_template_validity_audit import (
    FreyTemplateValidityRecord,
    build_frey_template_validity_audit_545,
)
from .good_prime_selector import GoodPrimeRecord, select_good_primes_545
from .level_220_audit import (
    Level220NewformRecord,
    Level220PrimeRecord,
    build_level_220_newform_records,
    build_level_220_prime_records,
    factorization_220,
)
from .newform_coefficient_importer import (
    NewformCoefficientImportSummary,
    NewformCoefficientRow,
    import_level_220_newform_coefficients,
)
from .obstruction_progress_score import ObstructionProgressRecord, score_obstruction_progress_545
from .proof_gap_report import ProofGapRecord, build_proof_gap_records_545, proof_gap_report_markdown
from .sage_level_220_newform_expander import write_sage_level_220_newform_expander
from .trace_congruence_filter_545 import (
    TraceCongruenceFilterRecord,
    build_trace_congruence_filter_545,
    load_level_220_coefficients,
)
from .trace_comparison_audit import TraceComparisonAuditRecord, build_trace_comparison_audit_545


SIGNATURE_545 = "5-4-5"


@dataclass(frozen=True)
class Focused545Artifacts:
    """Paths written by the focused `(5,4,5)` audit."""

    focused_report_path: str
    frey_template_validity_path: str
    level_220_prime_audit_path: str
    level_220_newforms_path: str
    trace_comparison_path: str
    good_prime_list_path: str
    sage_newform_expander_path: str
    frey_trace_possibilities_path: str
    trace_congruence_filter_path: str
    obstruction_progress_path: str
    coefficient_import_summary_path: str
    coefficient_import_rows_path: str
    assumption_register_path: str
    proof_gap_summary_path: str
    proof_gap_report_path: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
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


def _first(rows: Iterable[Mapping[str, Any]], *, signature: str = SIGNATURE_545) -> Mapping[str, Any] | None:
    for row in rows:
        if str(row.get("signature", "")) == signature:
            return row
    return None


def _filter(rows: Iterable[Mapping[str, Any]], *, signature: str = SIGNATURE_545) -> list[Mapping[str, Any]]:
    return [row for row in rows if str(row.get("signature", "")) == signature]


def _load_sage_payload(run_dir: Path) -> dict[str, Any]:
    path = run_dir / "sage_results" / "sage_5_4_5.json"
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _sage_fact_lines(payload: Mapping[str, Any], import_row: Mapping[str, Any] | None) -> list[str]:
    checked = payload.get("checked_levels", [])
    trace_rows = payload.get("trace_rows", [])
    trace_summary = "none"
    if isinstance(trace_rows, list) and trace_rows:
        parts = []
        for row in trace_rows:
            if isinstance(row, dict):
                parts.append(
                    f"ell={row.get('ell')} support={row.get('trace_support_size')} traces={row.get('trace_counts')}"
                )
        trace_summary = "; ".join(parts)
    return [
        f"- Sage status: `{payload.get('sage_status', import_row.get('sage_status', 'missing') if import_row else 'missing')}`.",
        f"- Checked levels: `{';'.join(str(item) for item in checked) or 'none'}`.",
        f"- Level-220 newform count: `{payload.get('newform_count', import_row.get('newform_count', '0') if import_row else '0')}`.",
        f"- Trace status: `{payload.get('trace_match_status', import_row.get('trace_match_status', 'missing') if import_row else 'missing')}`.",
        f"- Imported local trace rows: {trace_summary}.",
        f"- Contradiction claim allowed: `{payload.get('contradiction_claim_allowed', False)}`.",
    ]


def _unit_lines(unit_rows: Iterable[Mapping[str, Any]]) -> list[str]:
    rows = list(unit_rows)
    if not rows:
        return ["- No local unit-survivor rows were available in this run."]
    lines = []
    for row in rows:
        lines.append(
            "- ell `{ell}`: verdict `{verdict}`, survivors `{survivors}`, lift `{lift}`, explanation: {explanation}".format(
                ell=row.get("ell", ""),
                verdict=row.get("artifact_verdict", ""),
                survivors=row.get("geometry_survivor_count", ""),
                lift=row.get("unit_lift_unit_lift_status", ""),
                explanation=row.get("artifact_explanation", ""),
            )
        )
    return lines


def _status_counts(rows: Iterable[Mapping[str, Any]]) -> tuple[int, int]:
    known = list(rows)
    mismatches = sum(
        1
        for row in known
        if str(row.get("calibration_status", "")).find("mismatch") >= 0
        or str(row.get("post_sage_label", "")) == "known_case_mismatch"
    )
    overpromotions = sum(1 for row in known if str(row.get("overpromoted", "False")) != "False")
    return mismatches, overpromotions


def focused_545_markdown(
    *,
    run_dir: Path,
    sage_payload: Mapping[str, Any],
    import_row: Mapping[str, Any] | None,
    audit_row: Mapping[str, Any] | None,
    unit_rows: list[Mapping[str, Any]],
    validity_rows: list[FreyTemplateValidityRecord],
    prime_rows: list[Level220PrimeRecord],
    newform_rows: list[Level220NewformRecord],
    trace_rows: list[TraceComparisonAuditRecord],
    good_prime_rows: list[GoodPrimeRecord],
    frey_trace_rows: list[FreyTracePossibilityRecord],
    filter_rows: list[TraceCongruenceFilterRecord],
    progress_row: ObstructionProgressRecord,
    coefficient_summary: NewformCoefficientImportSummary,
    coefficient_rows: list[NewformCoefficientRow],
    assumption_rows: list[AssumptionRecord],
    gap_rows: list[ProofGapRecord],
    known_mismatches: int,
    known_overpromotions: int,
) -> str:
    """Return the focused 5-4-5 Markdown report."""
    audit_label = str(audit_row.get("audit_review_label", "not_available")) if audit_row else "not_available"
    priority = str(audit_row.get("priority", "")) if audit_row else ""
    lines = [
        "# Focused Modular Review: `(5,4,5)`",
        "",
        "Equation form: `A^5 + B^4 = C^5`.",
        "",
        "This is a human-review packet. It separates imported Sage facts from symbolic-template assumptions and open mathematical obligations. It does not certify a theorem, contradiction, or exclusion.",
        "",
        "## Route Status",
        "",
        f"- Current focused label: `{audit_label}`.",
        f"- Priority: `{priority or 'unknown'}`.",
        f"- Known-case mismatches: `{known_mismatches}`.",
        f"- Known-case overpromotions: `{known_overpromotions}`.",
        f"- Highest allowed label in this pipeline: `worth_human_modular_review`.",
        "",
        "## Verified Sage Facts",
        "",
        *_sage_fact_lines(sage_payload, import_row),
        "",
        "## Local Survivor Rows",
        "",
        *_unit_lines(unit_rows),
        "",
        "## Frey Template Validity Audit",
        "",
        "| component | classification | risk | next action |",
        "| --- | --- | --- | --- |",
    ]
    for row in validity_rows:
        lines.append(f"| `{row.component}` | `{row.classification}` | `{row.risk_level}` | {row.next_action} |")
    lines.extend(
        [
            "",
            "## Level 220 Audit",
            "",
            f"- Factorization: `{factorization_220()}`.",
            "- Level 220 is currently a `heuristic_symbolic` route-audit target, not a verified conductor or lowered level.",
            "",
            "| prime | exponent in 220 | why it appears | required assumption |",
            "| ---: | ---: | --- | --- |",
        ]
    )
    for row in prime_rows:
        lines.append(
            f"| {row.prime} | {row.exponent_in_level} | {row.reason_in_candidate_support} | {row.required_assumption} |"
        )
    lines.extend(
        [
            "",
            "## Level 220 Newforms",
            "",
            "| index | label | q-expansion data | status | notes |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )
    for row in newform_rows:
        lines.append(
            f"| {row.newform_index} | `{row.label}` | `{row.q_expansion_data_available}` | `{row.status}` | {row.notes} |"
        )
    lines.extend(
        [
            "",
            "## Trace Comparison Audit",
            "",
            "| level | prime | good for level | Frey traces | newform traces | mode | classification |",
            "| ---: | ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for row in trace_rows:
        lines.append(
            f"| {row.level} | {row.prime} | `{row.good_prime_for_level}` | "
            f"`{';'.join(row.frey_survivor_trace_values) or 'none'}` | "
            f"`{';'.join(row.newform_trace_values) or 'missing'}` | `{row.comparison_mode}` | "
            f"`{row.comparison_classification}` |"
        )
    lines.extend(
        [
            "",
            "The key trace warning: the imported narrow row is at `ell=11`, and `11` divides `220`. That makes it local route evidence, not yet a clean good-prime newform trace comparison.",
            "",
            "## Good-Prime Trace Audit",
            "",
            "The good-prime audit excludes primes dividing `220` and excludes the residual-prime candidate `5` by default. It is designed to replace the weak `ell=11` signal with trace comparisons at primes where level-220 newform coefficients can be meaningfully tested.",
            "",
            f"- Selected good primes: `{';'.join(str(row.prime) for row in good_prime_rows if row.selected) or 'none'}`.",
            f"- Newform coefficient JSON expected at: `{(run_dir / 'level_220_newform_coefficients.json').as_posix()}`.",
            f"- Coefficient import status: `{coefficient_summary.sage_status}`; schema valid: `{coefficient_summary.schema_valid}`.",
            f"- Imported coefficient rows: `{coefficient_summary.coefficient_row_count}`.",
            f"- Rational/integer coefficients: `{coefficient_summary.rational_integer_coefficient_count}`; non-rational coefficients: `{coefficient_summary.nonrational_coefficient_count}`; unclear coefficients: `{coefficient_summary.unclear_coefficient_count}`.",
            f"- Aggregate progress label: `{progress_row.progress_label}`.",
            f"- Usable comparisons: `{progress_row.usable_comparison_count}`.",
            f"- Coefficient-field blocked comparisons: `{progress_row.coefficient_field_unclear_count}`.",
            f"- Newforms surviving all available filters: `{progress_row.newforms_surviving_all_filters}` of `{progress_row.newform_count}`.",
            f"- Unresolved reasons: `{progress_row.unresolved_reasons or 'none'}`.",
            "",
            "### Frey Trace Possibilities At Good Primes",
            "",
            "| q | survivors | nonsingular | possible traces |",
            "| ---: | ---: | ---: | --- |",
        ]
    )
    for row in frey_trace_rows[:24]:
        lines.append(
            f"| {row.prime} | {row.survivor_triple_count} | {row.nonsingular_curve_count} | "
            f"`{';'.join(str(item) for item in row.possible_traces) or 'none'}` |"
        )
    lines.extend(
        [
            "",
            "### Congruence Filter Results",
            "",
            "| q | newform | coefficient | mode | classification | reason |",
            "| ---: | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in filter_rows[:48]:
        lines.append(
            f"| {row.prime} | {row.newform_index} | `{row.newform_coefficient or 'missing'}` | "
            f"`{row.comparison_mode}` | `{row.filter_classification}` | {row.reason} |"
        )
    lines.extend(
        [
            "",
            "### Coefficient Field Summary",
            "",
            "| newform | q | coefficient | field kind | mod-5 reduction | status |",
            "| ---: | ---: | --- | --- | --- | --- |",
        ]
    )
    if coefficient_rows:
        for row in coefficient_rows[:48]:
            lines.append(
                f"| {row.newform_index} | {row.prime} | `{row.coefficient}` | `{row.coefficient_field_kind}` | "
                f"`{row.coefficient_mod_5 or 'missing'}` | `{row.row_status}` |"
            )
    else:
        lines.append("| none | none | missing | missing | missing | coefficient JSON not imported |")
    lines.extend(
        [
            "",
            "If both level-220 newforms are eventually eliminated by good-prime congruence filters, this packet must call that `trace_mismatch_candidate`, not a proof or contradiction. With missing q-expansion data, the correct label is `trace_data_insufficient`; with non-rational coefficients and no justified reduction above `5`, the correct label is `coefficient_field_blocked`.",
            "",
            "If coefficient-field handling blocks comparison, the next human check is to choose and justify the prime above `5` in the newform coefficient field, then redo the trace congruence in that residue field.",
            "",
            "## Assumption Register",
            "",
            "| id | status | risk | required for | next action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in assumption_rows:
        lines.append(f"| `{row.assumption_id}` | `{row.status}` | `{row.risk_level}` | {row.required_for} | {row.next_action} |")
    lines.extend(
        [
            "",
            "## Gap Summary",
            "",
            "| category | status | risk | required next lemma |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in gap_rows:
        lines.append(
            f"| `{row.gap_category}` | `{row.gap_status}` | `{row.risk_level}` | {row.required_next_lemma} |"
        )
    lines.extend(
        [
            "",
            "## Exact Next Theorem Or Lemma",
            "",
            "A human should next prove the Frey-curve attachment and conductor/level-lowering package for `A^5 + B^4 = C^5`: every primitive solution gives the stated Frey object; the residual representation at the justified modulus is irreducible; the true conductor lowers to the claimed comparison level; and the two level-220 newforms, with actual q-expansion coefficients at good primes, fail or pass the justified trace congruence test.",
            "",
            "## Timeout Retry Note",
            "",
            "The timeout retry manifest remains focused on `(3,5,5)`, `(5,5,7)`, and `(7,7,4)`. Those retries should not change the interpretation of this focused `(5,4,5)` packet unless new data is explicitly imported and this report is regenerated.",
            "",
            "## Generated Sidecars",
            "",
            f"- `{(run_dir / 'frey_template_validity_545.csv').as_posix()}`",
            f"- `{(run_dir / 'level_220_prime_audit.csv').as_posix()}`",
            f"- `{(run_dir / 'level_220_newforms.csv').as_posix()}`",
            f"- `{(run_dir / 'trace_comparison_545.csv').as_posix()}`",
            f"- `{(run_dir / 'good_prime_list_545.csv').as_posix()}`",
            f"- `{(run_dir / 'sage_level_220_newform_expander.sage').as_posix()}`",
            f"- `{(run_dir / 'frey_trace_possibilities_545.csv').as_posix()}`",
            f"- `{(run_dir / 'trace_congruence_filter_545.csv').as_posix()}`",
            f"- `{(run_dir / 'obstruction_progress_545.csv').as_posix()}`",
            f"- `{(run_dir / 'level_220_coefficient_import_summary.csv').as_posix()}`",
            f"- `{(run_dir / 'level_220_coefficient_rows.csv').as_posix()}`",
            f"- `{(run_dir / 'assumption_register_545.csv').as_posix()}`",
            f"- `{(run_dir / 'proof_gap_summary.csv').as_posix()}`",
            f"- `{(run_dir / 'proof_gap_report.md').as_posix()}`",
            "",
        ]
    )
    return "\n".join(lines)


def generate_focused_545_review(run_dir: Path) -> Focused545Artifacts:
    """Generate the focused `(5,4,5)` review packet in `run_dir`."""
    run_dir.mkdir(parents=True, exist_ok=True)
    sage_payload = _load_sage_payload(run_dir)
    import_rows = _read_csv(run_dir / "sage_import_results.csv")
    audit_rows = _read_csv(run_dir / "modular_candidate_deep_audit.csv")
    unit_rows = _read_csv(run_dir / "unit_survivor_summary.csv")
    level_rows = _read_csv(run_dir / "level_explanations.csv")
    matrix_rows = _read_csv(run_dir / "newform_trace_matrix.csv")
    known_rows = _read_csv(run_dir / "sage_known_case_calibration.csv")
    if not known_rows:
        known_rows = _read_csv(run_dir / "known_case_calibration_summary.csv")

    import_row = _first(import_rows)
    audit_row = _first(audit_rows)
    level_220_row = next((row for row in level_rows if row.get("signature") == SIGNATURE_545 and row.get("level") == "220"), None)
    filtered_units = _filter(unit_rows)
    filtered_matrix = _filter(matrix_rows)
    known_mismatches, known_overpromotions = _status_counts(known_rows)

    validity_rows = build_frey_template_validity_audit_545(
        sage_payload=sage_payload,
        level_row=level_220_row,
        audit_row=audit_row,
    )
    prime_rows = build_level_220_prime_records()
    newform_rows = build_level_220_newform_records(sage_payload)
    trace_rows = build_trace_comparison_audit_545(filtered_matrix)
    good_prime_rows = select_good_primes_545(level=220, bound=100, allow_residual_prime=False)
    frey_trace_rows = build_frey_trace_possibilities_545(good_prime_rows)
    coefficient_path = run_dir / "level_220_newform_coefficients.json"
    coefficient_summary, coefficient_rows = import_level_220_newform_coefficients(coefficient_path)
    coefficient_payload = {
        "newform_count": coefficient_summary.newform_count,
        "coefficient_rows": [row.to_flat_dict() for row in coefficient_rows],
    }
    raw_coefficient_payload = load_level_220_coefficients(coefficient_path)
    if not coefficient_rows and raw_coefficient_payload:
        coefficient_payload = raw_coefficient_payload
    newform_count = int(sage_payload.get("newform_count", 0) or 0)
    filter_rows = build_trace_congruence_filter_545(
        good_prime_rows=good_prime_rows,
        frey_trace_rows=frey_trace_rows,
        coefficient_payload=coefficient_payload,
        newform_count=newform_count,
        residual_modulus=5,
    )
    progress_row = score_obstruction_progress_545(filter_rows, newform_count=newform_count)
    assumption_rows = build_assumption_register_545()
    gap_rows = build_proof_gap_records_545()

    focused_report_path = run_dir / "FOCUSED_545_REVIEW.md"
    frey_path = run_dir / "frey_template_validity_545.csv"
    prime_path = run_dir / "level_220_prime_audit.csv"
    newforms_path = run_dir / "level_220_newforms.csv"
    trace_path = run_dir / "trace_comparison_545.csv"
    good_prime_path = run_dir / "good_prime_list_545.csv"
    sage_expander_path = write_sage_level_220_newform_expander(run_dir)
    frey_trace_path = run_dir / "frey_trace_possibilities_545.csv"
    filter_path = run_dir / "trace_congruence_filter_545.csv"
    progress_path = run_dir / "obstruction_progress_545.csv"
    coefficient_summary_path = run_dir / "level_220_coefficient_import_summary.csv"
    coefficient_rows_path = run_dir / "level_220_coefficient_rows.csv"
    assumptions_path = run_dir / "assumption_register_545.csv"
    gaps_path = run_dir / "proof_gap_summary.csv"
    gap_report_path = run_dir / "proof_gap_report.md"

    _write_csv(frey_path, [row.to_flat_dict() for row in validity_rows])
    _write_csv(prime_path, [row.to_flat_dict() for row in prime_rows])
    _write_csv(newforms_path, [row.to_flat_dict() for row in newform_rows])
    _write_csv(trace_path, [row.to_flat_dict() for row in trace_rows])
    _write_csv(good_prime_path, [row.to_flat_dict() for row in good_prime_rows])
    _write_csv(frey_trace_path, [row.to_flat_dict() for row in frey_trace_rows])
    _write_csv(filter_path, [row.to_flat_dict() for row in filter_rows])
    _write_csv(progress_path, [progress_row.to_flat_dict()])
    _write_csv(coefficient_summary_path, [coefficient_summary.to_flat_dict()])
    _write_csv(coefficient_rows_path, [row.to_flat_dict() for row in coefficient_rows])
    _write_csv(assumptions_path, [row.to_flat_dict() for row in assumption_rows])
    _write_csv(gaps_path, [row.to_flat_dict() for row in gap_rows])
    gap_report_path.write_text(proof_gap_report_markdown(output_dir=run_dir, rows=gap_rows), encoding="utf-8")
    focused_report_path.write_text(
        focused_545_markdown(
            run_dir=run_dir,
            sage_payload=sage_payload,
            import_row=import_row,
            audit_row=audit_row,
            unit_rows=filtered_units,
            validity_rows=validity_rows,
            prime_rows=prime_rows,
            newform_rows=newform_rows,
            trace_rows=trace_rows,
            good_prime_rows=good_prime_rows,
            frey_trace_rows=frey_trace_rows,
            filter_rows=filter_rows,
            progress_row=progress_row,
            coefficient_summary=coefficient_summary,
            coefficient_rows=coefficient_rows,
            assumption_rows=assumption_rows,
            gap_rows=gap_rows,
            known_mismatches=known_mismatches,
            known_overpromotions=known_overpromotions,
        ),
        encoding="utf-8",
    )
    return Focused545Artifacts(
        focused_report_path=focused_report_path.as_posix(),
        frey_template_validity_path=frey_path.as_posix(),
        level_220_prime_audit_path=prime_path.as_posix(),
        level_220_newforms_path=newforms_path.as_posix(),
        trace_comparison_path=trace_path.as_posix(),
        good_prime_list_path=good_prime_path.as_posix(),
        sage_newform_expander_path=sage_expander_path.as_posix(),
        frey_trace_possibilities_path=frey_trace_path.as_posix(),
        trace_congruence_filter_path=filter_path.as_posix(),
        obstruction_progress_path=progress_path.as_posix(),
        coefficient_import_summary_path=coefficient_summary_path.as_posix(),
        coefficient_import_rows_path=coefficient_rows_path.as_posix(),
        assumption_register_path=assumptions_path.as_posix(),
        proof_gap_summary_path=gaps_path.as_posix(),
        proof_gap_report_path=gap_report_path.as_posix(),
    )
