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
from beal_rsg_lab.single_mask_newform_pressure_545 import (
    build_single_mask_newform_pressure_545,
)
from beal_rsg_lab.tate_algorithm_stub_545 import build_tate_algorithm_stub_545
from beal_rsg_lab.trace_congruence_filter_545 import TraceCongruenceFilterRecord


FORBIDDEN_LABELS = {"proof", "proven", "solved", "contradiction", "disproof", "disproven"}


def _filter_row(prime: int, newform_index: int, classification: str, coefficient: str) -> TraceCongruenceFilterRecord:
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
        reason="synthetic focused diagnostic row",
        contradiction_claim_allowed=False,
    )


def _focused_filter_rows() -> list[TraceCongruenceFilterRecord]:
    return [
        _filter_row(13, 0, "survives", "-4"),
        _filter_row(13, 1, "eliminated", "0"),
        _filter_row(17, 0, "eliminated", "0"),
        _filter_row(17, 1, "survives", "-4"),
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


class FreyReductionDiagnostics545Tests(unittest.TestCase):
    def test_q13_q17_single_masks_are_included_with_multiplicative_diagnostics(self) -> None:
        rows = build_frey_reduction_diagnostics_545()
        self.assertEqual({row.prime for row in rows}, {13, 17})
        self.assertEqual({row.valuation_mask for row in rows}, {"A_only", "B_only", "C_only"})
        self.assertTrue(all(row.reduction_type == "multiplicative_reduction" for row in rows))
        self.assertTrue(all(row.c4_valuation == "0" for row in rows))
        self.assertTrue(all(row.c6_valuation == "0" for row in rows))
        self.assertTrue(all(int(row.discriminant_valuation_lower_bound) > 0 for row in rows))
        self.assertTrue(all(not row.standard_trace_behavior_available for row in rows))

    def test_tate_stub_uses_available_valuations_without_forbidden_labels(self) -> None:
        diagnostics = build_frey_reduction_diagnostics_545()
        tate_rows = build_tate_algorithm_stub_545(diagnostics)
        pressure_rows = build_single_mask_newform_pressure_545(_focused_filter_rows(), diagnostics, tate_rows)
        self.assertTrue(all(not row.needs_human_tate_algorithm for row in tate_rows))
        self.assertEqual({row.stub_reduction_type for row in tate_rows}, {"multiplicative_reduction"})
        self.assertEqual({row.branch_classification for row in pressure_rows}, {"multiplicative_reduction_condition"})
        self.assertEqual({row.prime_local_label for row in pressure_rows}, {"local_case_elimination_candidate"})
        labels = (
            {row.stub_reduction_type for row in tate_rows}
            | {row.tate_algorithm_status for row in tate_rows}
            | {row.branch_classification for row in pressure_rows}
            | {row.prime_local_label for row in pressure_rows}
        )
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))

    def test_missing_c4_formula_downgrades_to_human_tate_analysis(self) -> None:
        diagnostics = build_frey_reduction_diagnostics_545(
            formulas=FreyInvariantFormulaAvailability(c4_available=False)
        )
        tate_rows = build_tate_algorithm_stub_545(diagnostics)
        pressure_rows = build_single_mask_newform_pressure_545(_focused_filter_rows(), diagnostics, tate_rows)
        self.assertEqual({row.reduction_type for row in diagnostics}, {"template_unknown"})
        self.assertTrue(all(row.needs_human_tate_algorithm for row in tate_rows))
        self.assertEqual({row.branch_classification for row in pressure_rows}, {"needs_human_tate_algorithm"})
        self.assertEqual({row.prime_local_label for row in pressure_rows}, {"local_coverage_gap"})

    def test_focused_generation_writes_diagnostic_sidecars_without_overpromotion(self) -> None:
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
                        "selected_good_primes": [13, 17],
                        "newform_count": 2,
                        "coefficient_rows": [
                            {
                                "newform_index": 0,
                                "newform_label": "f0",
                                "prime": 13,
                                "coefficient": "-4",
                                "coefficient_field": "Rational Field",
                                "coefficient_field_kind": "rational_integer",
                                "is_rational_integer": True,
                                "reduction_mod_5_available": True,
                                "coefficient_mod_5": "1",
                                "row_status": "completed",
                            },
                            {
                                "newform_index": 1,
                                "newform_label": "f1",
                                "prime": 13,
                                "coefficient": "0",
                                "coefficient_field": "Rational Field",
                                "coefficient_field_kind": "rational_integer",
                                "is_rational_integer": True,
                                "reduction_mod_5_available": True,
                                "coefficient_mod_5": "0",
                                "row_status": "completed",
                            },
                            {
                                "newform_index": 0,
                                "newform_label": "f0",
                                "prime": 17,
                                "coefficient": "0",
                                "coefficient_field": "Rational Field",
                                "coefficient_field_kind": "rational_integer",
                                "is_rational_integer": True,
                                "reduction_mod_5_available": True,
                                "coefficient_mod_5": "0",
                                "row_status": "completed",
                            },
                            {
                                "newform_index": 1,
                                "newform_label": "f1",
                                "prime": 17,
                                "coefficient": "-4",
                                "coefficient_field": "Rational Field",
                                "coefficient_field_kind": "rational_integer",
                                "is_rational_integer": True,
                                "reduction_mod_5_available": True,
                                "coefficient_mod_5": "1",
                                "row_status": "completed",
                            },
                        ],
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
            for path in (
                artifacts.frey_reduction_diagnostics_path,
                artifacts.tate_algorithm_stub_path,
                artifacts.single_mask_newform_pressure_path,
            ):
                self.assertTrue(Path(path).exists())
            with Path(artifacts.single_mask_newform_pressure_path).open(newline="", encoding="utf-8") as handle:
                pressure_rows = list(csv.DictReader(handle))
            self.assertEqual({row["prime"] for row in pressure_rows}, {"13", "17"})
            self.assertEqual({row["valuation_mask"] for row in pressure_rows}, {"A_only", "B_only", "C_only"})
            self.assertTrue(all(row["route_ceiling_label"] == "worth_human_modular_review" for row in pressure_rows))
            with Path(artifacts.trace_filter_case_coverage_path).open(newline="", encoding="utf-8") as handle:
                coverage_rows = [row for row in csv.DictReader(handle) if row["prime"] in {"13", "17"}]
            self.assertEqual({row["coverage_label"] for row in coverage_rows}, {"local_coverage_gap"})
            report = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Focused Frey Reduction Diagnostics", report)
            self.assertIn(
                "Run the Tate algorithm / reduction analysis for the Frey curve at q=13 and q=17 under A_only, B_only, and C_only.",
                report,
            )
            self.assertIn("Highest allowed label in this pipeline: `worth_human_modular_review`.", report)


if __name__ == "__main__":
    unittest.main()
