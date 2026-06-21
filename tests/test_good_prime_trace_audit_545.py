from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.frey_trace_possibility_545 import build_frey_trace_possibilities_545
from beal_rsg_lab.good_prime_selector import select_good_primes_545
from beal_rsg_lab.newform_coefficient_importer import import_level_220_newform_coefficients
from beal_rsg_lab.obstruction_progress_score import score_obstruction_progress_545
from beal_rsg_lab.trace_congruence_filter_545 import build_trace_congruence_filter_545


class GoodPrimeTraceAudit545Tests(unittest.TestCase):
    def test_good_prime_selection_excludes_level_primes_and_residual_prime(self) -> None:
        rows = select_good_primes_545(level=220, bound=20)
        by_prime = {row.prime: row for row in rows}
        self.assertFalse(by_prime[2].selected)
        self.assertFalse(by_prime[5].selected)
        self.assertFalse(by_prime[11].selected)
        self.assertEqual(by_prime[11].exclusion_reason, "divides_target_level")
        self.assertEqual(by_prime[5].exclusion_reason, "divides_target_level")
        self.assertTrue(by_prime[3].selected)
        self.assertTrue(by_prime[7].selected)

    def test_trace_filter_handles_missing_q_expansion_data_safely(self) -> None:
        good_rows = select_good_primes_545(level=220, bound=7)
        frey_rows = build_frey_trace_possibilities_545(good_rows)
        filters = build_trace_congruence_filter_545(
            good_prime_rows=good_rows,
            frey_trace_rows=frey_rows,
            coefficient_payload={},
            newform_count=2,
            residual_modulus=5,
        )
        self.assertTrue(filters)
        self.assertTrue(all(row.filter_classification == "insufficient_data" for row in filters))
        self.assertTrue(all(not row.contradiction_claim_allowed for row in filters))
        labels = {row.filter_classification for row in filters}
        self.assertTrue(labels.isdisjoint({"proof", "proven", "disproof", "disproven"}))

    def test_missing_coefficient_json_gives_insufficient_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_path = Path(temp_dir) / "level_220_newform_coefficients.json"
            summary, coefficient_rows = import_level_220_newform_coefficients(missing_path)
            self.assertEqual(summary.sage_status, "missing")
            self.assertTrue(summary.schema_valid)
            self.assertEqual(coefficient_rows, [])
            good_rows = [row for row in select_good_primes_545(level=220, bound=3) if row.prime == 3]
            frey_rows = build_frey_trace_possibilities_545(good_rows)
            filters = build_trace_congruence_filter_545(
                good_prime_rows=good_rows,
                frey_trace_rows=frey_rows,
                coefficient_payload={},
                newform_count=2,
                residual_modulus=5,
            )
            self.assertEqual({row.filter_classification for row in filters}, {"insufficient_data"})

    def test_imports_valid_level_220_coefficient_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "level_220_newform_coefficients.json"
            path.write_text(
                json.dumps(
                    {
                        "signature": [5, 4, 5],
                        "level": 220,
                        "weight": 2,
                        "sage_status": "completed",
                        "selected_good_primes": [3, 7],
                        "newform_count": 2,
                        "coefficient_rows": [
                            {
                                "level": 220,
                                "weight": 2,
                                "newform_index": 0,
                                "newform_label": "f0",
                                "prime": 3,
                                "coefficient": "0",
                                "coefficient_field": "Rational Field",
                                "coefficient_field_kind": "rational_integer",
                                "is_rational_integer": True,
                                "reduction_mod_5_available": True,
                                "coefficient_mod_5": "0",
                                "prime_above_5_metadata": "",
                                "row_status": "completed",
                            },
                            {
                                "level": 220,
                                "weight": 2,
                                "newform_index": 1,
                                "newform_label": "f1",
                                "prime": 3,
                                "coefficient": "a",
                                "coefficient_field": "Number Field in a with defining polynomial x^2 + 1",
                                "coefficient_field_kind": "number_field",
                                "is_rational_integer": False,
                                "reduction_mod_5_available": False,
                                "coefficient_mod_5": "",
                                "prime_above_5_metadata": "",
                                "row_status": "coefficient_field_unclear",
                            },
                        ],
                        "contradiction_claim_allowed": False,
                    }
                ),
                encoding="utf-8",
            )
            summary, rows = import_level_220_newform_coefficients(path)
            self.assertTrue(summary.schema_valid)
            self.assertEqual(summary.level, 220)
            self.assertEqual(summary.weight, 2)
            self.assertEqual(summary.newform_count, 2)
            self.assertEqual(summary.coefficient_row_count, 2)
            self.assertEqual(summary.rational_integer_coefficient_count, 1)
            self.assertEqual(summary.unclear_coefficient_count, 1)
            self.assertEqual(rows[0].coefficient_mod_5, "0")

    def test_rational_coefficient_comparison_exact_and_mod_5(self) -> None:
        good_rows = [row for row in select_good_primes_545(level=220, bound=7) if row.prime == 7]
        frey_rows = build_frey_trace_possibilities_545(good_rows)
        exact_coeff = str(frey_rows[0].possible_traces[0])
        mod_5_only = "1"
        self.assertNotIn(int(mod_5_only), set(frey_rows[0].possible_traces))
        payload = {
            "coefficient_rows": [
                {
                    "newform_index": 0,
                    "newform_label": "exact",
                    "prime": 7,
                    "coefficient": exact_coeff,
                    "coefficient_field": "Rational Field",
                    "coefficient_field_kind": "rational_integer",
                    "is_rational_integer": True,
                    "reduction_mod_5_available": True,
                    "coefficient_mod_5": str(int(exact_coeff) % 5),
                },
                {
                    "newform_index": 1,
                    "newform_label": "mod5",
                    "prime": 7,
                    "coefficient": mod_5_only,
                    "coefficient_field": "Rational Field",
                    "coefficient_field_kind": "rational_integer",
                    "is_rational_integer": True,
                    "reduction_mod_5_available": True,
                    "coefficient_mod_5": mod_5_only,
                },
            ]
        }
        filters = build_trace_congruence_filter_545(
            good_prime_rows=good_rows,
            frey_trace_rows=frey_rows,
            coefficient_payload=payload,
            newform_count=2,
            residual_modulus=5,
        )
        by_index = {row.newform_index: row for row in filters}
        self.assertEqual(by_index[0].comparison_mode, "exact")
        self.assertEqual(by_index[0].filter_classification, "survives")
        self.assertEqual(by_index[1].comparison_mode, "mod_5")
        self.assertEqual(by_index[1].filter_classification, "survives")

    def test_coefficient_field_uncertainty_is_safe(self) -> None:
        good_rows = [row for row in select_good_primes_545(level=220, bound=3) if row.prime == 3]
        frey_rows = build_frey_trace_possibilities_545(good_rows)
        payload = {
            "newforms": [
                {
                    "newform_index": 0,
                    "label": "nf0",
                    "coefficient_field": "Number Field in a with defining polynomial x^2 + 1",
                    "coefficients": {"3": "a"},
                }
            ]
        }
        filters = build_trace_congruence_filter_545(
            good_prime_rows=good_rows,
            frey_trace_rows=frey_rows,
            coefficient_payload=payload,
            newform_count=1,
            residual_modulus=5,
        )
        self.assertEqual(filters[0].filter_classification, "coefficient_field_unclear")
        self.assertEqual(filters[0].comparison_mode, "unknown")
        score = score_obstruction_progress_545(filters, newform_count=1)
        self.assertEqual(score.progress_label, "coefficient_field_blocked")

    def test_progress_score_uses_review_ceiling_and_safe_labels(self) -> None:
        good_rows = [row for row in select_good_primes_545(level=220, bound=3) if row.prime == 3]
        frey_rows = build_frey_trace_possibilities_545(good_rows)
        trace_values = frey_rows[0].possible_traces
        trace_mods = {value % 5 for value in trace_values}
        impossible = next(value for value in range(-20, 21) if value % 5 not in trace_mods)
        payload = {
            "newforms": [
                {
                    "newform_index": 0,
                    "label": "nf0",
                    "coefficient_field": "Rational Field",
                    "coefficients": {"3": str(impossible)},
                }
            ]
        }
        filters = build_trace_congruence_filter_545(
            good_prime_rows=good_rows,
            frey_trace_rows=frey_rows,
            coefficient_payload=payload,
            newform_count=1,
            residual_modulus=5,
        )
        score = score_obstruction_progress_545(filters, newform_count=1)
        self.assertIn(score.progress_label, {"trace_mismatch_candidate", "trace_survivor_exists"})
        self.assertEqual(score.route_ceiling_label, "worth_human_modular_review")
        self.assertNotIn(score.progress_label, {"proof", "proven", "disproof", "disproven"})

    def test_focused_generation_writes_good_prime_sidecars(self) -> None:
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
                        "trace_rows": [{"ell": 11, "trace_counts": {"0": 1}, "trace_support_size": 1}],
                    }
                ),
                encoding="utf-8",
            )
            for filename, rows in {
                "sage_import_results.csv": [
                    {
                        "job_id": "sage_5_4_5",
                        "signature": "5-4-5",
                        "sage_status": "completed",
                        "newform_count": "2",
                        "checked_levels": "220",
                        "trace_match_status": "narrow",
                    }
                ],
                "modular_candidate_deep_audit.csv": [
                    {"signature": "5-4-5", "audit_review_label": "worth_human_modular_review", "priority": "7.25"}
                ],
                "sage_known_case_calibration.csv": [
                    {"signature": "5-4-5", "post_sage_label": "modular_followup_candidate", "overpromoted": "False"}
                ],
            }.items():
                with (run_dir / filename).open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                    writer.writeheader()
                    writer.writerows(rows)
            artifacts = generate_focused_545_review(run_dir)
            self.assertTrue(Path(artifacts.good_prime_list_path).exists())
            self.assertTrue(Path(artifacts.frey_trace_possibilities_path).exists())
            self.assertTrue(Path(artifacts.trace_congruence_filter_path).exists())
            self.assertTrue(Path(artifacts.obstruction_progress_path).exists())
            self.assertTrue(Path(artifacts.sage_newform_expander_path).exists())
            report = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Good-Prime Trace Audit", report)
            self.assertIn("trace_data_insufficient", report)

    def test_focused_progress_uses_level_220_coefficient_newform_count(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            (run_dir / "sage_results").mkdir()
            (run_dir / "sage_results" / "sage_5_4_5.json").write_text(
                json.dumps(
                    {
                        "checked_levels": [220],
                        "contradiction_claim_allowed": False,
                        "job_id": "sage_5_4_5",
                        "newform_count": 49,
                        "sage_status": "completed",
                        "signature": [5, 4, 5],
                        "trace_match_status": "narrow",
                        "trace_rows": [{"ell": 11, "trace_counts": {"0": 1}, "trace_support_size": 1}],
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
                                "level": 220,
                                "weight": 2,
                                "newform_index": 0,
                                "newform_label": "f0",
                                "prime": 3,
                                "coefficient": "1",
                                "coefficient_field": "Rational Field",
                                "coefficient_field_kind": "rational_integer",
                                "is_rational_integer": True,
                                "reduction_mod_5_available": True,
                                "coefficient_mod_5": "1",
                                "prime_above_5_metadata": "",
                                "row_status": "completed",
                            },
                            {
                                "level": 220,
                                "weight": 2,
                                "newform_index": 1,
                                "newform_label": "f1",
                                "prime": 3,
                                "coefficient": "2",
                                "coefficient_field": "Rational Field",
                                "coefficient_field_kind": "rational_integer",
                                "is_rational_integer": True,
                                "reduction_mod_5_available": True,
                                "coefficient_mod_5": "2",
                                "prime_above_5_metadata": "",
                                "row_status": "completed",
                            },
                        ],
                        "contradiction_claim_allowed": False,
                    }
                ),
                encoding="utf-8",
            )
            for filename, rows in {
                "sage_import_results.csv": [
                    {
                        "job_id": "sage_5_4_5",
                        "signature": "5-4-5",
                        "sage_status": "completed",
                        "newform_count": "49",
                        "checked_levels": "220",
                        "trace_match_status": "narrow",
                    }
                ],
                "modular_candidate_deep_audit.csv": [
                    {"signature": "5-4-5", "audit_review_label": "worth_human_modular_review", "priority": "7.25"}
                ],
                "sage_known_case_calibration.csv": [
                    {"signature": "5-4-5", "post_sage_label": "modular_followup_candidate", "overpromoted": "False"}
                ],
            }.items():
                with (run_dir / filename).open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                    writer.writeheader()
                    writer.writerows(rows)
            artifacts = generate_focused_545_review(run_dir)
            with Path(artifacts.obstruction_progress_path).open(newline="", encoding="utf-8") as handle:
                progress = list(csv.DictReader(handle))[0]
            self.assertEqual(progress["newform_count"], "2")
            self.assertNotIn("newform_2", progress["unresolved_reasons"])


if __name__ == "__main__":
    unittest.main()
