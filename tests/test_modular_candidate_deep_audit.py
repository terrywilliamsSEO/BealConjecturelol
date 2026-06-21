from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.level_explanation import explain_candidate_levels
from beal_rsg_lab.modular_candidate_deep_audit import build_modular_candidate_deep_audits
from beal_rsg_lab.newform_trace_matrix import build_newform_trace_matrix
from beal_rsg_lab.proof_obligation_generator import build_proof_obligation_records, proof_obligations_markdown
from beal_rsg_lab.timeout_retry_runner import build_timeout_retry_manifest


class ModularCandidateDeepAuditTests(unittest.TestCase):
    def _job_rows(self, result_path: Path) -> list[dict[str, str]]:
        return [
            {
                "job_id": "sage_5_4_5",
                "signature": "5-4-5",
                "route_label": "mixed_needs_external_check",
                "candidate_case_ids": "bridge_5_4_5",
                "candidate_rows": "known_case:bridge_5_4_5:mixed_needs_external_check:prime=11",
                "primes_involved": "11",
                "candidate_levels": "110;220;440;550;1210",
                "frey_template_id": "frey_split_full_2torsion_candidate",
                "frey_template_equation": "E: y^2 = x(x - A^5)(x + B^4)",
                "job_path": "runs/demo/sage_jobs/sage_5_4_5.sage",
                "result_path": result_path.as_posix(),
            },
            {
                "job_id": "sage_7_7_4",
                "signature": "7-7-4",
                "route_label": "needs_external_sage_check",
                "candidate_case_ids": "bridge_7_7_4",
                "candidate_rows": "known_case:bridge_7_7_4:needs_external_sage_check:prime=29",
                "primes_involved": "29",
                "candidate_levels": "406;812",
                "job_path": "runs/demo/sage_jobs/sage_7_7_4.sage",
                "result_path": "runs/demo/sage_results/sage_7_7_4.json",
            },
        ]

    def _import_rows(self) -> list[dict[str, str]]:
        return [
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
            },
            {
                "job_id": "sage_7_7_4",
                "signature": "7-7-4",
                "route_label": "needs_external_sage_check",
                "sage_status": "timeout",
                "newform_count": "0",
                "checked_levels": "",
                "trace_match_status": "not_checked",
                "contradiction_claim_allowed": "False",
                "followup_label": "needs_external_sage_check",
                "schema_valid": "True",
            },
        ]

    def _confidence_rows(self) -> list[dict[str, str]]:
        return [
            {
                "job_id": "sage_5_4_5",
                "signature": "5-4-5",
                "updated_followup_label": "modular_followup_candidate",
                "human_review_priority": "7.25",
                "sage_status": "completed",
                "trace_match_status": "narrow",
                "newform_count": "2",
                "checked_levels": "220",
            },
            {
                "job_id": "sage_7_7_4",
                "signature": "7-7-4",
                "updated_followup_label": "needs_external_sage_check",
                "human_review_priority": "1.5",
                "sage_status": "timeout",
                "trace_match_status": "not_checked",
            },
        ]

    def test_timeout_retry_manifest_selects_timeouts_only(self) -> None:
        rows = build_timeout_retry_manifest(
            job_rows=self._job_rows(Path("result.json")),
            import_rows=self._import_rows(),
            base_timeout_seconds=60,
            timeout_multiplier=5,
        )
        self.assertEqual([row.signature for row in rows], ["7-7-4"])
        self.assertEqual(rows[0].retry_timeout_seconds, 300)
        self.assertFalse(rows[0].rerun_completed)

    def test_level_explanation_factors_level_220(self) -> None:
        rows = explain_candidate_levels(
            job_rows=self._job_rows(Path("result.json")),
            import_rows=self._import_rows(),
            confidence_rows=self._confidence_rows(),
        )
        row_220 = next(row for row in rows if row.signature == "5-4-5" and row.level == 220)
        self.assertEqual(row_220.level_factorization, "2^2 * 5 * 11")
        self.assertTrue(row_220.sage_confirmed_level)
        self.assertEqual(row_220.symbolic_or_heuristic, "heuristic_symbolic")

    def test_trace_matrix_handles_missing_and_present_coefficients(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result_path = Path(temp_dir) / "sage_5_4_5.json"
            payload = {
                "trace_rows": [{"ell": 11, "trace_counts": {"0": 1}, "trace_support_size": 1}],
                "newform_trace_rows": [
                    {"level": 220, "prime": 11, "status": "completed", "coefficient": "0"},
                ],
            }
            result_path.write_text(json.dumps(payload), encoding="utf-8")
            rows = build_newform_trace_matrix(
                job_rows=self._job_rows(result_path),
                import_rows=self._import_rows(),
                confidence_rows=self._confidence_rows(),
            )
        checked = next(row for row in rows if row.level == 220)
        self.assertEqual(checked.matrix_classification, "trace_matches_some_newform")
        self.assertEqual(checked.comparison_mode, "exact")

    def test_modular_candidate_audit_can_mark_worth_human_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result_path = Path(temp_dir) / "sage_5_4_5.json"
            payload = {
                "trace_rows": [{"ell": 11, "trace_counts": {"0": 1}, "trace_support_size": 1, "nonsingular_triple_count": 1}],
            }
            result_path.write_text(json.dumps(payload), encoding="utf-8")
            rows = build_modular_candidate_deep_audits(
                job_rows=self._job_rows(result_path),
                import_rows=self._import_rows(),
                confidence_rows=self._confidence_rows(),
                known_case_rows=[
                    {
                        "signature": "5-4-5",
                        "terrain_label": "known_modular_method_shape",
                        "actual_route_label": "needs_external_sage_check",
                        "artifact_rows": "0",
                        "sparse_unit_rows": "1",
                        "padic_descent_rows": "0",
                        "unit_lift_rigid_or_collapsed_rows": "0",
                    }
                ],
                unit_rows=[],
            )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].audit_review_label, "worth_human_modular_review")
        self.assertTrue(rows[0].obligation_explicit)
        self.assertTrue(rows[0].known_case_clean)

    def test_modular_candidate_audit_blocks_known_case_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result_path = Path(temp_dir) / "sage_5_4_5.json"
            result_path.write_text(
                json.dumps(
                    {
                        "trace_rows": [
                            {"ell": 11, "trace_counts": {"0": 1}, "trace_support_size": 1, "nonsingular_triple_count": 1}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            rows = build_modular_candidate_deep_audits(
                job_rows=self._job_rows(result_path),
                import_rows=self._import_rows(),
                confidence_rows=self._confidence_rows(),
                known_case_rows=[
                    {
                        "signature": "5-4-5",
                        "terrain_label": "known_modular_method_shape",
                        "actual_route_label": "known_case_mismatch",
                    }
                ],
                unit_rows=[],
            )
        self.assertEqual(rows[0].audit_review_label, "modular_followup_candidate")
        self.assertFalse(rows[0].known_case_clean)

    def test_obligation_labels_do_not_emit_forbidden_outcomes(self) -> None:
        audit_rows = [
            {
                "signature": "5-4-5",
                "audit_review_label": "worth_human_modular_review",
                "checked_levels": "220",
                "candidate_levels": "110;220",
                "frey_template_id": "frey_split_full_2torsion_candidate",
            }
        ]
        records = build_proof_obligation_records(audit_rows)
        labels = {records[0].audit_review_label}
        self.assertNotIn("proof", labels)
        self.assertNotIn("proven", labels)
        self.assertNotIn("disproof", labels)
        self.assertNotIn("disproven", labels)
        text = proof_obligations_markdown(records)
        self.assertIn("human-review obligations", text)
        self.assertIn("does not certify", text)


if __name__ == "__main__":
    unittest.main()
