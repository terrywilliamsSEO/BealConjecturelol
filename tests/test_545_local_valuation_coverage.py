from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.frey_reduction_case_router_545 import build_frey_reduction_cases_545
from beal_rsg_lab.good_prime_selector import select_good_primes_545
from beal_rsg_lab.local_gap_summary_545 import build_local_gap_summary_545
from beal_rsg_lab.local_valuation_case_545 import build_local_valuation_cases_545
from beal_rsg_lab.trace_congruence_filter_545 import TraceCongruenceFilterRecord
from beal_rsg_lab.trace_filter_case_coverage_545 import build_trace_filter_case_coverage_545
from beal_rsg_lab.valuation_mask_lift_545 import build_valuation_mask_lifts_545


FORBIDDEN_LABELS = {"proof", "proven", "contradiction", "solved", "disproof", "disproven"}


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
        newform_coefficient="1",
        coefficient_mod_5="1",
        prime_above_5_metadata="",
        comparison_mode="mod_5",
        filter_classification=classification,
        reason="synthetic",
        contradiction_claim_allowed=False,
    )


class LocalValuationCoverage545Tests(unittest.TestCase):
    def test_pairwise_masks_are_primitive_forbidden(self) -> None:
        good_rows = [row for row in select_good_primes_545(level=220, bound=13) if row.prime == 13]
        valuation_rows = build_local_valuation_cases_545(good_rows)
        by_mask = {row.valuation_mask: row for row in valuation_rows}
        for mask in ("AB", "AC", "BC", "ABC"):
            self.assertEqual(by_mask[mask].classification, "primitive_forbidden")
            self.assertFalse(by_mask[mask].primitive_compatible)

    def test_q5_and_primes_dividing_220_remain_excluded(self) -> None:
        rows = select_good_primes_545(level=220, bound=13)
        by_prime = {row.prime: row for row in rows}
        self.assertFalse(by_prime[2].selected)
        self.assertFalse(by_prime[5].selected)
        self.assertFalse(by_prime[11].selected)
        self.assertEqual(by_prime[5].exclusion_reason, "divides_target_level")
        self.assertEqual(by_prime[11].exclusion_reason, "divides_target_level")

    def test_unit_only_trace_filter_is_not_global(self) -> None:
        good_rows = [row for row in select_good_primes_545(level=220, bound=13) if row.prime == 13]
        valuation_rows = build_local_valuation_cases_545(good_rows)
        lift_rows = build_valuation_mask_lifts_545(valuation_rows)
        reduction_rows = build_frey_reduction_cases_545(valuation_rows, lift_rows)
        coverage_rows = build_trace_filter_case_coverage_545(
            [_filter_row(13, 0, "eliminated"), _filter_row(13, 1, "survives")],
            reduction_rows,
        )
        self.assertEqual(len(coverage_rows), 1)
        row = coverage_rows[0]
        self.assertFalse(row.full_local_coverage)
        self.assertFalse(row.supports_stronger_local_trace_candidate)
        self.assertEqual(row.coverage_label, "bad_reduction_requires_separate_argument")
        summary = build_local_gap_summary_545(coverage_rows)
        self.assertEqual(summary.unit_only_coverage_count, 1)
        self.assertEqual(summary.trace_mismatch_scope_label, "unit_only_trace_mismatch_candidate")
        self.assertEqual(summary.overall_local_gap_label, "local_coverage_gap")

    def test_no_forbidden_labels_are_emitted(self) -> None:
        good_rows = [row for row in select_good_primes_545(level=220, bound=17) if row.selected]
        valuation_rows = build_local_valuation_cases_545(good_rows)
        lift_rows = build_valuation_mask_lifts_545(valuation_rows)
        reduction_rows = build_frey_reduction_cases_545(valuation_rows, lift_rows)
        coverage_rows = build_trace_filter_case_coverage_545(
            [_filter_row(13, 0, "eliminated"), _filter_row(17, 1, "eliminated")],
            reduction_rows,
        )
        summary = build_local_gap_summary_545(coverage_rows)
        labels = (
            {row.classification for row in valuation_rows}
            | {row.lift_classification for row in lift_rows}
            | {row.expected_reduction for row in reduction_rows}
            | {row.coverage_label for row in coverage_rows}
            | {summary.trace_mismatch_scope_label, summary.overall_local_gap_label}
        )
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))

    def test_focused_generation_keeps_calibration_clean_and_writes_local_gap_files(self) -> None:
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
                                "prime": 17,
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
            self.assertTrue(Path(artifacts.local_valuation_cases_path).exists())
            self.assertTrue(Path(artifacts.valuation_mask_lift_path).exists())
            self.assertTrue(Path(artifacts.frey_reduction_cases_path).exists())
            self.assertTrue(Path(artifacts.trace_filter_case_coverage_path).exists())
            self.assertTrue(Path(artifacts.local_gap_summary_path).exists())
            report = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Known-case mismatches: `0`", report)
            self.assertIn("Known-case overpromotions: `0`", report)
            self.assertIn("Local valuation scope label", report)


if __name__ == "__main__":
    unittest.main()
