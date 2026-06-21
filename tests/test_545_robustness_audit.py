from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.frey_trace_possibility_545 import build_frey_trace_possibilities_545
from beal_rsg_lab.good_prime_selector import select_good_primes_545
from beal_rsg_lab.level_220_robustness_545 import build_level_robustness_545
from beal_rsg_lab.local_coverage_audit_545 import build_local_coverage_audit_545
from beal_rsg_lab.newform_coefficient_importer import NewformCoefficientImportSummary
from beal_rsg_lab.obstruction_progress_score import ObstructionProgressRecord
from beal_rsg_lab.small_prime_sensitivity_545 import build_small_prime_sensitivity_545
from beal_rsg_lab.theorem_skeleton_545 import (
    build_theorem_skeleton_obligations_545,
    theorem_skeleton_markdown,
)
from beal_rsg_lab.trace_congruence_filter_545 import TraceCongruenceFilterRecord


FORBIDDEN_LABELS = {"proof", "proven", "disproof", "disproven", "solved"}


def _filter_row(newform: int, prime: int, classification: str) -> TraceCongruenceFilterRecord:
    return TraceCongruenceFilterRecord(
        signature="5-4-5",
        level=220,
        prime=prime,
        newform_index=newform,
        newform_label=f"f{newform}",
        coefficient_field="Rational Field",
        coefficient_field_kind="rational_integer",
        frey_trace_values=(0,),
        newform_coefficient="1",
        coefficient_mod_5="1",
        prime_above_5_metadata="",
        comparison_mode="mod_5",
        filter_classification=classification,
        reason="synthetic",
        contradiction_claim_allowed=False,
    )


def _progress(label: str = "trace_data_insufficient") -> ObstructionProgressRecord:
    return ObstructionProgressRecord(
        signature="5-4-5",
        good_primes_checked=1,
        newform_count=2,
        usable_comparison_count=0,
        coefficient_field_unclear_count=0,
        insufficient_data_count=2,
        newforms_surviving_all_filters=2,
        eliminated_newforms=0,
        first_elimination_primes="",
        unresolved_reasons="newform_0:insufficient_or_unclear_trace_data",
        progress_label=label,
        confidence_score=2.0,
        route_ceiling_label="worth_human_modular_review",
    )


def _summary(status: str = "missing", newforms: int = 0) -> NewformCoefficientImportSummary:
    return NewformCoefficientImportSummary(
        signature="5-4-5",
        level=220,
        weight=2,
        sage_status=status,
        schema_valid=True,
        newform_count=newforms,
        selected_good_prime_count=0,
        coefficient_row_count=0,
        rational_integer_coefficient_count=0,
        nonrational_coefficient_count=0,
        unclear_coefficient_count=0,
        error_message="",
        source_path="missing",
    )


class Robustness545AuditTests(unittest.TestCase):
    def test_q3_sensitivity_profile_generation(self) -> None:
        rows = [
            _filter_row(0, 3, "eliminated"),
            _filter_row(1, 3, "eliminated"),
            _filter_row(0, 7, "survives"),
            _filter_row(1, 7, "survives"),
        ]
        sensitivity = build_small_prime_sensitivity_545(rows, newform_count=2)
        by_name = {row.profile_name: row for row in sensitivity}
        self.assertEqual(by_name["exclude_q_3"].sensitivity_label, "small_prime_dependent")
        self.assertTrue(by_name["exclude_q_3"].mismatch_depends_entirely_on_q3)
        self.assertEqual(by_name["exclude_q_3"].surviving_newform_count, 2)

    def test_no_forbidden_labels_are_emitted_by_robustness_records(self) -> None:
        rows = [
            _filter_row(0, 3, "eliminated"),
            _filter_row(1, 3, "eliminated"),
        ]
        sensitivity = build_small_prime_sensitivity_545(rows, newform_count=2)
        robustness = build_level_robustness_545(
            coefficient_summary=_summary(status="partial", newforms=0),
            progress_row=_progress(),
            levels=[220, 110],
        )
        labels = {row.sensitivity_label for row in sensitivity} | {row.robustness_label for row in robustness}
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))
        self.assertTrue(all(row.route_ceiling_label == "worth_human_modular_review" for row in robustness))

    def test_local_coverage_distinguishes_unit_and_zero_support_cases(self) -> None:
        good_rows = [row for row in select_good_primes_545(level=220, bound=3) if row.prime == 3]
        frey_rows = build_frey_trace_possibilities_545(good_rows)
        coverage = build_local_coverage_audit_545(good_rows, frey_rows)
        self.assertEqual(len(coverage), 1)
        row = coverage[0]
        self.assertGreater(row.residue_unit_solution_count, 0)
        self.assertGreater(row.zero_support_solution_count, 0)
        self.assertTrue(row.trace_comparison_assumes_q_not_dividing_ABC)
        self.assertEqual(row.coverage_label, "local_coverage_gap")

    def test_theorem_skeleton_is_conditional_and_not_a_finished_argument(self) -> None:
        sensitivity = build_small_prime_sensitivity_545(
            [_filter_row(0, 3, "eliminated"), _filter_row(1, 3, "eliminated")],
            newform_count=2,
        )
        coverage = build_local_coverage_audit_545(
            [row for row in select_good_primes_545(level=220, bound=3) if row.prime == 3],
            build_frey_trace_possibilities_545([row for row in select_good_primes_545(level=220, bound=3) if row.prime == 3]),
        )
        robustness = build_level_robustness_545(
            coefficient_summary=_summary(status="completed", newforms=2),
            progress_row=_progress(label="trace_mismatch_candidate"),
            levels=[220],
        )
        obligations = build_theorem_skeleton_obligations_545(
            progress_row=_progress(label="trace_mismatch_candidate"),
            sensitivity_rows=sensitivity,
            coverage_rows=coverage,
            level_rows=robustness,
        )
        markdown = theorem_skeleton_markdown(obligations).lower()
        self.assertIn("conditional modular route", markdown)
        self.assertIn("not a proof", markdown)
        statuses = {row.status for row in obligations}
        self.assertTrue(statuses.isdisjoint(FORBIDDEN_LABELS))

    def test_level_robustness_handles_missing_and_partial_sage_data(self) -> None:
        missing_rows = build_level_robustness_545(
            coefficient_summary=_summary(status="missing", newforms=0),
            progress_row=_progress(),
            levels=[220],
        )
        partial_rows = build_level_robustness_545(
            coefficient_summary=_summary(status="partial", newforms=0),
            progress_row=_progress(),
            levels=[110],
        )
        self.assertEqual(missing_rows[0].robustness_label, "level_data_insufficient")
        self.assertEqual(partial_rows[0].robustness_label, "level_data_insufficient")

    def test_focused_generation_writes_robustness_sidecars_and_keeps_calibration_clean(self) -> None:
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
                        "selected_good_primes": [3],
                        "newform_count": 2,
                        "coefficient_rows": [
                            {
                                "newform_index": 0,
                                "newform_label": "f0",
                                "prime": 3,
                                "coefficient": "1",
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
                                "prime": 3,
                                "coefficient": "2",
                                "coefficient_field": "Rational Field",
                                "coefficient_field_kind": "rational_integer",
                                "is_rational_integer": True,
                                "reduction_mod_5_available": True,
                                "coefficient_mod_5": "2",
                                "row_status": "completed",
                            },
                        ],
                        "contradiction_claim_allowed": False,
                    }
                ),
                encoding="utf-8",
            )
            with (run_dir / "sage_known_case_calibration.csv").open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["signature", "post_sage_label", "overpromoted", "calibration_status"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "signature": "5-4-5",
                        "post_sage_label": "modular_followup_candidate",
                        "overpromoted": "False",
                        "calibration_status": "calibrated",
                    }
                )
            artifacts = generate_focused_545_review(run_dir)
            self.assertTrue(Path(artifacts.trace_mismatch_provenance_path).exists())
            self.assertTrue(Path(artifacts.small_prime_sensitivity_path).exists())
            self.assertTrue(Path(artifacts.local_coverage_audit_path).exists())
            self.assertTrue(Path(artifacts.theorem_skeleton_path).exists())
            report = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Known-case mismatches: `0`", report)
            self.assertIn("Known-case overpromotions: `0`", report)


if __name__ == "__main__":
    unittest.main()
