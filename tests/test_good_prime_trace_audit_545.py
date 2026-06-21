from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.frey_trace_possibility_545 import build_frey_trace_possibilities_545
from beal_rsg_lab.good_prime_selector import select_good_primes_545
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
        self.assertNotIn("proof", labels)
        self.assertNotIn("disproof", labels)

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
        self.assertEqual(filters[0].filter_classification, "bad_comparison_mode")
        self.assertEqual(filters[0].comparison_mode, "unknown")

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
        self.assertNotIn("proof", score.progress_label)
        self.assertNotIn("disproof", score.progress_label)

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


if __name__ == "__main__":
    unittest.main()
