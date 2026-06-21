from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.best_route_summary_545 import build_best_route_summary_545
from beal_rsg_lab.cross_prime_branch_compatibility_545 import (
    SAFE_CROSS_PRIME_COMPATIBILITY_LABELS,
    build_cross_prime_branch_compatibility_545,
)
from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.frey_reduction_diagnostics_545 import build_frey_reduction_diagnostics_545
from beal_rsg_lab.good_prime_selector import select_good_primes_545
from beal_rsg_lab.local_case_closure_score_545 import build_local_case_closure_scores_545
from beal_rsg_lab.multiplicative_reduction_congruence_545 import (
    build_multiplicative_reduction_congruences_545,
)
from beal_rsg_lab.newform_coefficient_importer import NewformCoefficientRow
from beal_rsg_lab.nonunit_elimination_545 import build_nonunit_eliminations_545
from beal_rsg_lab.q3_exceptionality_audit_545 import (
    SAFE_Q3_EXCEPTIONALITY_LABELS,
    build_q3_exceptionality_audit_545,
)
from beal_rsg_lab.trace_congruence_filter_545 import TraceCongruenceFilterRecord


FORBIDDEN_LABELS = {"proof", "proven", "solved", "contradiction", "disproof", "disproven"}


def _coefficient(prime: int, newform_index: int, coefficient: str) -> NewformCoefficientRow:
    return NewformCoefficientRow(
        signature="5-4-5",
        level=220,
        weight=2,
        newform_index=newform_index,
        newform_label=f"f{newform_index}",
        prime=prime,
        coefficient=coefficient,
        coefficient_field="Rational Field",
        coefficient_field_kind="rational_integer",
        is_rational_integer=True,
        reduction_mod_5_available=True,
        coefficient_mod_5=str(int(coefficient) % 5),
        prime_above_5_metadata="",
        row_status="completed",
    )


def _coefficient_rows() -> list[NewformCoefficientRow]:
    return [
        _coefficient(3, 0, "-2"),
        _coefficient(3, 1, "2"),
        _coefficient(13, 0, "-4"),
        _coefficient(13, 1, "0"),
        _coefficient(17, 0, "0"),
        _coefficient(17, 1, "-4"),
        _coefficient(41, 0, "6"),
        _coefficient(41, 1, "-10"),
        _coefficient(61, 0, "2"),
        _coefficient(61, 1, "-14"),
    ]


def _filter_row(prime: int, newform_index: int, classification: str, coefficient: str = "0") -> TraceCongruenceFilterRecord:
    return TraceCongruenceFilterRecord(
        signature="5-4-5",
        level=220,
        prime=prime,
        newform_index=newform_index,
        newform_label=f"f{newform_index}",
        coefficient_field="Rational Field",
        coefficient_field_kind="rational_integer",
        frey_trace_values=(0,),
        newform_coefficient=coefficient,
        coefficient_mod_5=str(int(coefficient) % 5) if coefficient.lstrip("-").isdigit() else "",
        prime_above_5_metadata="",
        comparison_mode="mod_5",
        filter_classification=classification,
        reason="synthetic cross-prime branch row",
        contradiction_claim_allowed=False,
    )


def _unit_rows() -> list[TraceCongruenceFilterRecord]:
    return [
        _filter_row(3, 0, "eliminated", "-2"),
        _filter_row(3, 1, "eliminated", "2"),
        _filter_row(13, 0, "survives", "-4"),
        _filter_row(13, 1, "eliminated", "0"),
        _filter_row(17, 0, "eliminated", "0"),
        _filter_row(17, 1, "survives", "-4"),
        _filter_row(41, 0, "eliminated", "6"),
        _filter_row(41, 1, "survives", "-10"),
        _filter_row(61, 0, "eliminated", "2"),
        _filter_row(61, 1, "survives", "-14"),
    ]


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _audit_inputs(
    *,
    coefficient_rows: list[NewformCoefficientRow] | None = None,
    unit_rows: list[TraceCongruenceFilterRecord] | None = None,
    level_lowering_available: bool = True,
):
    coefficients = coefficient_rows if coefficient_rows is not None else _coefficient_rows()
    filters = unit_rows if unit_rows is not None else _unit_rows()
    diagnostics = build_frey_reduction_diagnostics_545()
    multiplicative = build_multiplicative_reduction_congruences_545(
        coefficients,
        diagnostics,
        newform_count=2,
        level_lowering_congruence_available=level_lowering_available,
    )
    closure = build_local_case_closure_scores_545(filters, multiplicative, newform_count=2)
    nonunit = build_nonunit_eliminations_545(select_good_primes_545(level=220, bound=61))
    cross = build_cross_prime_branch_compatibility_545(filters, multiplicative, nonunit, newform_count=2)
    q3 = build_q3_exceptionality_audit_545(closure, cross)
    return filters, multiplicative, closure, nonunit, cross, q3


class CrossPrimeBranchCompatibility545Tests(unittest.TestCase):
    def test_non_q3_primes_jointly_eliminate_current_newform_branches(self) -> None:
        _, _, _, _, cross, _ = _audit_inputs()
        by_index = {row.newform_index: row for row in cross}
        self.assertEqual(by_index[-1].compatibility_label, "cross_prime_elimination_candidate")
        self.assertFalse(by_index[-1].compatible_branch_assignment_exists)
        self.assertEqual(by_index[0].compatibility_label, "cross_prime_elimination_candidate")
        self.assertIn("17", by_index[0].eliminated_at_primes)
        self.assertEqual(by_index[1].compatibility_label, "cross_prime_elimination_candidate")
        self.assertIn("13", by_index[1].eliminated_at_primes)
        labels = {row.compatibility_label for row in cross}
        self.assertTrue(labels <= SAFE_CROSS_PRIME_COMPATIBILITY_LABELS)
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))
        self.assertTrue(all(row.route_ceiling_label == "worth_human_modular_review" for row in cross))

    def test_cross_prime_survivor_exists_when_one_newform_has_every_prime_branch(self) -> None:
        survivor_units = [
            _filter_row(3, 0, "eliminated", "-2"),
            _filter_row(3, 1, "eliminated", "2"),
            _filter_row(13, 0, "survives", "-4"),
            _filter_row(13, 1, "eliminated", "0"),
            _filter_row(17, 0, "survives", "0"),
            _filter_row(17, 1, "survives", "-4"),
            _filter_row(41, 0, "survives", "6"),
            _filter_row(41, 1, "survives", "-10"),
            _filter_row(61, 0, "eliminated", "2"),
            _filter_row(61, 1, "survives", "-14"),
        ]
        _, _, _, _, cross, _ = _audit_inputs(unit_rows=survivor_units)
        by_index = {row.newform_index: row for row in cross}
        self.assertEqual(by_index[0].compatibility_label, "cross_prime_survivor_exists")
        self.assertEqual(by_index[-1].compatibility_label, "cross_prime_survivor_exists")

    def test_missing_branch_data_and_level_lowering_are_conservative(self) -> None:
        missing_coefficients = [row for row in _coefficient_rows() if row.prime != 41]
        _, _, _, _, missing_cross, _ = _audit_inputs(coefficient_rows=missing_coefficients)
        self.assertIn("branch_data_insufficient", {row.compatibility_label for row in missing_cross})
        _, _, _, _, level_cross, _ = _audit_inputs(level_lowering_available=False)
        self.assertEqual({row.compatibility_label for row in level_cross}, {"level_lowering_assumption_required"})

    def test_q3_exceptionality_and_best_route_labels_are_safe(self) -> None:
        _, _, closure, _, cross, q3 = _audit_inputs()
        self.assertEqual(q3.q3_exceptionality_label, "q3_consistent_with_larger_primes")
        self.assertTrue(q3.is_good_prime_for_level)
        self.assertIn(q3.q3_exceptionality_label, SAFE_Q3_EXCEPTIONALITY_LABELS)
        route_rows = build_best_route_summary_545(closure, cross, q3)
        self.assertEqual(route_rows[0].route_option, "non_q3_cross_prime_closure")
        self.assertEqual(route_rows[0].route_label, "cross_prime_elimination_candidate")
        route_labels = {row.route_label for row in route_rows}
        self.assertTrue(route_labels.isdisjoint(FORBIDDEN_LABELS))
        self.assertTrue(all(row.route_ceiling_label == "worth_human_modular_review" for row in route_rows))

    def test_q3_dependent_label_when_cross_prime_survivor_remains(self) -> None:
        survivor_units = [
            _filter_row(3, 0, "eliminated", "-2"),
            _filter_row(3, 1, "eliminated", "2"),
            _filter_row(13, 0, "survives", "-4"),
            _filter_row(13, 1, "eliminated", "0"),
            _filter_row(17, 0, "survives", "0"),
            _filter_row(17, 1, "survives", "-4"),
            _filter_row(41, 0, "survives", "6"),
            _filter_row(41, 1, "survives", "-10"),
            _filter_row(61, 0, "eliminated", "2"),
            _filter_row(61, 1, "survives", "-14"),
        ]
        _, _, closure, _, cross, q3 = _audit_inputs(unit_rows=survivor_units)
        route_rows = build_best_route_summary_545(closure, cross, q3)
        by_option = {row.route_option: row for row in route_rows}
        self.assertEqual(by_option["q3_single_prime_closure"].route_label, "q3_dependent_local_case_candidate")
        self.assertEqual(q3.q3_exceptionality_label, "q3_small_prime_sensitive")

    def test_focused_generation_writes_cross_prime_sidecars_without_overpromotion(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            (run_dir / "sage_results").mkdir()
            (run_dir / "sage_results" / "sage_5_4_5.json").write_text(
                json.dumps(
                    {
                        "checked_levels": [220],
                        "contradiction_claim_allowed": False,
                        "job_id": "sage_5_4_5",
                        "newform_count": 2,
                        "sage_status": "completed",
                        "signature": [5, 4, 5],
                        "trace_match_status": "narrow",
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "level_220_newform_coefficients.json").write_text(
                json.dumps(
                    {
                        "signature": [5, 4, 5],
                        "level": 220,
                        "weight": 2,
                        "sage_status": "completed",
                        "selected_good_primes": [3, 13, 17, 41, 61],
                        "newform_count": 2,
                        "coefficient_rows": [row.to_flat_dict() for row in _coefficient_rows()],
                        "contradiction_claim_allowed": False,
                    }
                ),
                encoding="utf-8",
            )
            _write_csv(
                run_dir / "modular_candidate_deep_audit.csv",
                [{"signature": "5-4-5", "audit_review_label": "worth_human_modular_review", "priority": "7.25"}],
            )
            _write_csv(
                run_dir / "sage_known_case_calibration.csv",
                [{"signature": "5-4-5", "post_sage_label": "modular_followup_candidate", "overpromoted": "False"}],
            )
            artifacts = generate_focused_545_review(run_dir)
            self.assertTrue(Path(artifacts.cross_prime_branch_compatibility_path).exists())
            self.assertTrue(Path(artifacts.q3_exceptionality_audit_report_path).exists())
            self.assertTrue(Path(artifacts.best_route_summary_report_path).exists())
            with Path(artifacts.cross_prime_branch_compatibility_path).open(newline="", encoding="utf-8") as handle:
                cross_rows = list(csv.DictReader(handle))
            aggregate = next(row for row in cross_rows if row["newform_index"] == "-1")
            self.assertEqual(aggregate["compatibility_label"], "cross_prime_elimination_candidate")
            focused = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Cross-Prime Branch Compatibility", focused)
            self.assertIn("q=3 Exceptionality", focused)
            self.assertIn("Best Route Summary", focused)
            best_route = Path(artifacts.best_route_summary_report_path).read_text(encoding="utf-8")
            self.assertIn("cross_prime_elimination_candidate", best_route)
            self.assertIn("worth_human_modular_review", best_route)


if __name__ == "__main__":
    unittest.main()
