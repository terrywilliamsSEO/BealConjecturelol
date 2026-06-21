from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.level_220_audit import factorization_220


class FocusedCandidateAudit545Tests(unittest.TestCase):
    def _write_csv(self, path: Path, rows: list[dict[str, object]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames: list[str] = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _seed_run(self, run_dir: Path) -> None:
        result_dir = run_dir / "sage_results"
        result_dir.mkdir(parents=True)
        (result_dir / "sage_5_4_5.json").write_text(
            json.dumps(
                {
                    "checked_levels": [220],
                    "contradiction_claim_allowed": False,
                    "errors": [],
                    "followup_label": "modular_followup_candidate",
                    "job_id": "sage_5_4_5",
                    "level_rows": [{"level": 220, "newform_count": 2, "status": "completed", "error": ""}],
                    "newform_count": 2,
                    "route_label": "mixed_needs_external_check",
                    "sage_status": "completed",
                    "signature": [5, 4, 5],
                    "trace_match_status": "narrow",
                    "trace_rows": [
                        {
                            "ell": 11,
                            "trace_counts": {"0": 1},
                            "trace_support_size": 1,
                            "nonsingular_triple_count": 1,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        self._write_csv(
            run_dir / "sage_import_results.csv",
            [
                {
                    "job_id": "sage_5_4_5",
                    "signature": "5-4-5",
                    "route_label": "mixed_needs_external_check",
                    "sage_status": "completed",
                    "newform_count": "2",
                    "checked_levels": "220",
                    "trace_match_status": "narrow",
                    "contradiction_claim_allowed": "False",
                    "followup_label": "modular_followup_candidate",
                    "schema_valid": "True",
                }
            ],
        )
        self._write_csv(
            run_dir / "modular_candidate_deep_audit.csv",
            [
                {
                    "signature": "5-4-5",
                    "audit_review_label": "worth_human_modular_review",
                    "priority": "7.25",
                    "checked_levels": "220",
                    "candidate_levels": "110;220",
                    "newform_count": "2",
                    "trace_status": "narrow",
                }
            ],
        )
        self._write_csv(
            run_dir / "unit_survivor_summary.csv",
            [
                {
                    "signature": "5-4-5",
                    "ell": "11",
                    "geometry_survivor_count": "1",
                    "artifact_verdict": "artifact_explained",
                    "artifact_explanation": "sparsity follows from tiny power image",
                    "unit_lift_unit_lift_status": "persists_or_expands",
                }
            ],
        )
        self._write_csv(
            run_dir / "level_explanations.csv",
            [
                {
                    "signature": "5-4-5",
                    "level": "220",
                    "candidate_level_source": "Generated from support {2, exponent radicals, local primes}.",
                    "sage_confirmed_level": "True",
                }
            ],
        )
        self._write_csv(
            run_dir / "newform_trace_matrix.csv",
            [
                {
                    "signature": "5-4-5",
                    "level": "220",
                    "ell": "11",
                    "frey_trace_values": "0",
                    "newform_coefficients": "",
                    "comparison_mode": "unknown",
                    "matrix_classification": "trace_data_insufficient",
                    "checked_level": "True",
                }
            ],
        )
        self._write_csv(
            run_dir / "sage_known_case_calibration.csv",
            [
                {
                    "case_id": "bridge_5_4_5",
                    "signature": "5-4-5",
                    "post_sage_label": "modular_followup_candidate",
                    "overpromoted": "False",
                    "calibration_status": "calibrated",
                }
            ],
        )

    def test_focused_report_generation_and_sidecars(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            self._seed_run(run_dir)
            artifacts = generate_focused_545_review(run_dir)
            report = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Focused Modular Review", report)
            self.assertIn("Exact Next Theorem Or Lemma", report)
            self.assertIn("not a verified conductor", report)
            self.assertTrue(Path(artifacts.level_220_newforms_path).exists())
            self.assertTrue(Path(artifacts.assumption_register_path).exists())
            self.assertTrue(Path(artifacts.proof_gap_summary_path).exists())

    def test_assumption_register_schema_and_safe_statuses(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            self._seed_run(run_dir)
            artifacts = generate_focused_545_review(run_dir)
            with Path(artifacts.assumption_register_path).open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertGreaterEqual(len(rows), 5)
            self.assertEqual(
                set(rows[0]),
                {"assumption_id", "statement", "source", "status", "required_for", "risk_level", "next_action"},
            )
            forbidden = {"proof", "proven", "disproof", "disproven"}
            self.assertTrue(all(row["status"] not in forbidden for row in rows))

    def test_level_220_factorization_and_missing_q_expansion(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            self._seed_run(run_dir)
            artifacts = generate_focused_545_review(run_dir)
            self.assertEqual(factorization_220(), "2^2 * 5 * 11")
            with Path(artifacts.level_220_newforms_path).open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 2)
            self.assertTrue(all(row["status"] == "missing_q_expansion_data" for row in rows))

    def test_trace_comparison_does_not_claim_contradiction(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            self._seed_run(run_dir)
            artifacts = generate_focused_545_review(run_dir)
            with Path(artifacts.trace_comparison_path).open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["good_prime_for_level"], "False")
            self.assertEqual(rows[0]["comparison_classification"], "insufficient_bad_prime_for_level")
            text = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("not yet a clean good-prime newform trace comparison", text)

    def test_known_case_mismatch_and_overpromotion_counts_remain_zero(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            self._seed_run(run_dir)
            artifacts = generate_focused_545_review(run_dir)
            text = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Known-case mismatches: `0`", text)
            self.assertIn("Known-case overpromotions: `0`", text)


if __name__ == "__main__":
    unittest.main()
