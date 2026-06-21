from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.frey_reduction_diagnostics_545 import (
    FreyInvariantFormulaAvailability,
    build_frey_reduction_diagnostics_545,
)
from beal_rsg_lab.best_eliminating_prime_545 import build_best_eliminating_prime_545
from beal_rsg_lab.local_case_closure_score_545 import build_local_case_closure_scores_545
from beal_rsg_lab.multiplicative_reduction_congruence_545 import (
    allowed_multiplicative_values_mod_5,
    build_multiplicative_reduction_congruences_545,
)
from beal_rsg_lab.newform_coefficient_importer import NewformCoefficientRow
from beal_rsg_lab.trace_congruence_filter_545 import TraceCongruenceFilterRecord


FORBIDDEN_LABELS = {"proof", "proven", "solved", "contradiction", "disproof", "disproven"}
FOCUSED_PRIMES = {3, 13, 17, 41, 61}


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
        _coefficient(3, 0, "0"),
        _coefficient(3, 1, "0"),
        _coefficient(13, 0, "-4"),
        _coefficient(13, 1, "0"),
        _coefficient(17, 0, "0"),
        _coefficient(17, 1, "-4"),
        _coefficient(41, 0, "0"),
        _coefficient(41, 1, "1"),
        _coefficient(61, 0, "2"),
        _coefficient(61, 1, "0"),
    ]


def _filter_row(prime: int, newform_index: int, classification: str) -> TraceCongruenceFilterRecord:
    return TraceCongruenceFilterRecord(
        signature="5-4-5",
        level=220,
        prime=prime,
        newform_index=newform_index,
        newform_label=f"f{newform_index}",
        coefficient_field="Rational Field",
        coefficient_field_kind="rational_integer",
        frey_trace_values=(0,),
        newform_coefficient="0",
        coefficient_mod_5="0",
        prime_above_5_metadata="",
        comparison_mode="mod_5",
        filter_classification=classification,
        reason="synthetic unit branch",
        contradiction_claim_allowed=False,
    )


def _unit_filter_rows() -> list[TraceCongruenceFilterRecord]:
    return [
        _filter_row(3, 0, "eliminated"),
        _filter_row(3, 1, "eliminated"),
        _filter_row(13, 0, "survives"),
        _filter_row(13, 1, "eliminated"),
        _filter_row(17, 0, "eliminated"),
        _filter_row(17, 1, "survives"),
        _filter_row(41, 0, "eliminated"),
        _filter_row(41, 1, "eliminated"),
        _filter_row(61, 0, "eliminated"),
        _filter_row(61, 1, "eliminated"),
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


class MultiplicativeCongruence545Tests(unittest.TestCase):
    def test_focused_q_set_is_included_and_allowed_values_are_correct(self) -> None:
        self.assertEqual(allowed_multiplicative_values_mod_5(3), (1, 4))
        self.assertEqual(allowed_multiplicative_values_mod_5(13), (1, 4))
        self.assertEqual(allowed_multiplicative_values_mod_5(17), (2, 3))
        self.assertEqual(allowed_multiplicative_values_mod_5(41), (2, 3))
        self.assertEqual(allowed_multiplicative_values_mod_5(61), (2, 3))
        rows = build_multiplicative_reduction_congruences_545(_coefficient_rows(), newform_count=2)
        self.assertEqual({row.prime for row in rows}, FOCUSED_PRIMES)
        self.assertEqual({row.valuation_mask for row in rows}, {"A_only", "B_only", "C_only"})
        self.assertEqual({row.newform_index for row in rows}, {0, 1})
        self.assertEqual(len(rows), 30)

    def test_congruence_classifies_survival_and_elimination_safely(self) -> None:
        rows = build_multiplicative_reduction_congruences_545(_coefficient_rows(), newform_count=2)
        labels = {row.congruence_classification for row in rows}
        self.assertEqual(labels, {"multiplicative_branch_survives", "multiplicative_branch_eliminated"})
        q13_f0 = [
            row for row in rows if row.prime == 13 and row.newform_index == 0
        ]
        self.assertTrue(all(row.congruence_classification == "multiplicative_branch_survives" for row in q13_f0))
        q17_rows = [row for row in rows if row.prime == 17]
        self.assertTrue(all(row.congruence_classification == "multiplicative_branch_eliminated" for row in q17_rows))
        q41_rows = [row for row in rows if row.prime == 41]
        self.assertTrue(all(row.congruence_classification == "multiplicative_branch_eliminated" for row in q41_rows))
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))

    def test_missing_coefficient_is_safe(self) -> None:
        rows = build_multiplicative_reduction_congruences_545([_coefficient(13, 0, "-4")], newform_count=2)
        self.assertIn("coefficient_missing", {row.congruence_classification for row in rows})
        self.assertTrue(all(row.route_ceiling_label == "worth_human_modular_review" for row in rows))

    def test_missing_formula_is_safe(self) -> None:
        diagnostics = build_frey_reduction_diagnostics_545(
            formulas=FreyInvariantFormulaAvailability(c4_available=False)
        )
        rows = build_multiplicative_reduction_congruences_545(
            _coefficient_rows(),
            diagnostics,
            newform_count=2,
        )
        self.assertEqual({row.congruence_classification for row in rows}, {"formula_missing"})

    def test_level_lowering_assumption_required_is_safe(self) -> None:
        rows = build_multiplicative_reduction_congruences_545(
            _coefficient_rows(),
            newform_count=2,
            level_lowering_congruence_available=False,
        )
        self.assertEqual({row.congruence_classification for row in rows}, {"level_lowering_assumption_required"})

    def test_closure_score_keeps_survivors_and_gaps_conservative(self) -> None:
        mult_rows = build_multiplicative_reduction_congruences_545(_coefficient_rows(), newform_count=2)
        closure = build_local_case_closure_scores_545(_unit_filter_rows(), mult_rows, newform_count=2)
        by_prime = {row.prime: row for row in closure}
        self.assertEqual(set(by_prime), FOCUSED_PRIMES)
        self.assertEqual(by_prime[3].closure_label, "local_case_elimination_candidate")
        self.assertEqual(by_prime[13].closure_label, "single_mask_survivor_exists")
        self.assertEqual(by_prime[17].closure_label, "unit_branch_survivor_exists")
        self.assertEqual(by_prime[41].closure_label, "local_case_elimination_candidate")
        self.assertEqual(by_prime[61].closure_label, "single_mask_survivor_exists")
        self.assertEqual(by_prime[13].single_mask_surviving_branches, 3)
        self.assertEqual(by_prime[17].unit_surviving_branch_count, 1)
        labels = {row.closure_label for row in closure}
        self.assertTrue(labels <= {"local_case_elimination_candidate", "unit_branch_survivor_exists", "single_mask_survivor_exists", "level_lowering_assumption_required", "local_coverage_gap"})
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))
        self.assertTrue(all(row.route_ceiling_label == "worth_human_modular_review" for row in closure))

    def test_best_eliminating_prime_ranking_deprioritizes_q3_ties(self) -> None:
        mult_rows = build_multiplicative_reduction_congruences_545(_coefficient_rows(), newform_count=2)
        closure = build_local_case_closure_scores_545(_unit_filter_rows(), mult_rows, newform_count=2)
        best_rows = build_best_eliminating_prime_545(closure)
        self.assertEqual({row.prime for row in best_rows}, FOCUSED_PRIMES)
        self.assertEqual(best_rows[0].prime, 41)
        self.assertEqual(best_rows[0].closure_label, "local_case_elimination_candidate")
        self.assertEqual(best_rows[0].route_ceiling_label, "worth_human_modular_review")
        self.assertTrue({row.best_priority_label for row in best_rows}.isdisjoint(FORBIDDEN_LABELS))

    def test_focused_generation_writes_congruence_sidecars_without_overpromotion(self) -> None:
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
            self.assertTrue(Path(artifacts.multiplicative_reduction_congruence_path).exists())
            self.assertTrue(Path(artifacts.local_case_closure_score_path).exists())
            self.assertTrue(Path(artifacts.best_eliminating_prime_path).exists())
            self.assertTrue(Path(artifacts.best_eliminating_prime_report_path).exists())
            with Path(artifacts.local_case_closure_score_path).open(newline="", encoding="utf-8") as handle:
                closure_rows = list(csv.DictReader(handle))
            self.assertEqual({int(row["prime"]) for row in closure_rows}, FOCUSED_PRIMES)
            closure_labels = {row["closure_label"] for row in closure_rows}
            self.assertIn("single_mask_survivor_exists", closure_labels)
            self.assertIn("unit_branch_survivor_exists", closure_labels)
            self.assertTrue(closure_labels <= {"local_case_elimination_candidate", "unit_branch_survivor_exists", "single_mask_survivor_exists", "level_lowering_assumption_required", "local_coverage_gap"})
            report = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Multiplicative-Reduction Congruence Audit", report)
            self.assertIn("Best Eliminating Prime Ranking", report)
            self.assertIn("so the route keeps `local_coverage_gap`", report)
            self.assertIn(
                "multiplicative branches satisfy `a_q(f) == +/-(q+1) mod 5` at q in `{3,13,17,41,61}` where used",
                report,
            )
            self.assertIn("Highest allowed label in this pipeline: `worth_human_modular_review`.", report)


if __name__ == "__main__":
    unittest.main()
