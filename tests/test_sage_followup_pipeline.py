from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from beal_rsg_lab.known_case_sage_calibration import calibrate_known_cases_with_sage
from beal_rsg_lab.modular_confidence_updater import update_modular_confidence
from beal_rsg_lab.sage_job_generator import generate_sage_jobs, sage_job_script_text
from beal_rsg_lab.sage_result_importer import import_sage_results, validate_sage_result


class SageFollowupPipelineTests(unittest.TestCase):
    def _calibration_record(self) -> SimpleNamespace:
        return SimpleNamespace(
            case_id="mixed_3_5_5",
            signature=(3, 5, 5),
            signature_text="3-5-5",
            expected_route="modular_method",
            actual_route_label="needs_external_sage_check",
            collision_class="terrain_dominates",
            collision_resolved_route_label="needs_external_sage_check",
            strongest_prime=31,
            strongest_system_signal="modular:newform_check_candidate",
            notes="test modular route",
        )

    def _score_record(self) -> SimpleNamespace:
        return SimpleNamespace(
            case_id="mixed_3_5_5",
            signature="3-5-5",
            output_label="needs_external_sage_check",
            proof_route_priority=5.0,
            discovery_readiness_score=3.0,
        )

    def test_sage_job_generation_writes_job_and_batch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("beal_rsg_lab.sage_job_generator.shutil.which", return_value=None):
                jobs = generate_sage_jobs(
                    output_dir=Path(temp_dir),
                    source_run="test_run",
                    calibration_records=[self._calibration_record()],
                    route_prior_scores=[self._score_record()],
                )
            self.assertEqual(len(jobs), 1)
            self.assertFalse(jobs[0].sage_available)
            self.assertTrue(Path(jobs[0].job_path).exists())
            self.assertTrue(Path(jobs[0].batch_path).exists())
            script = Path(jobs[0].job_path).read_text(encoding="utf-8")
            self.assertIn('"contradiction_claim_allowed": false', script)
            self.assertIn("json.dump", script)

    def test_sage_job_script_mentions_json_schema_fields(self) -> None:
        script = sage_job_script_text(
            job_id="sage_3_4_5",
            signature=(3, 4, 5),
            route_label="needs_external_sage_check",
            source_run="test",
            candidate_case_ids=("case",),
            candidate_rows=("known_case:case:needs_external_sage_check:prime=11",),
            primes_involved=(11,),
            candidate_levels=(110, 220),
            frey_template_id="frey_split_full_2torsion_candidate",
            frey_template_equation="E: y^2 = x(x - A^3)(x + B^4)",
            limitations="route-audit only",
            result_path=Path("sage_results/sage_3_4_5.json"),
        )
        self.assertIn('"sage_status"', script)
        self.assertIn('"newform_count"', script)
        self.assertIn('"trace_match_status"', script)
        self.assertIn("def _json_safe", script)
        self.assertIn("safe_payload", script)

    def test_validate_sage_result_rejects_contradiction_claims(self) -> None:
        payload = {
            "job_id": "sage_3_5_5",
            "signature": [3, 5, 5],
            "sage_status": "completed",
            "checked_levels": [30],
            "newform_count": 1,
            "trace_match_status": "rigid",
            "contradiction_claim_allowed": True,
        }
        valid, error = validate_sage_result(payload)
        self.assertFalse(valid)
        self.assertIn("must be false", error)

    def test_import_completed_partial_failed_and_timeout_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            jobs = []
            for status in ("completed", "partial", "failed", "timeout"):
                result_path = root / f"sage_{status}.json"
                job = SimpleNamespace(
                    job_id=f"sage_{status}",
                    signature="3-5-5",
                    route_label="needs_external_sage_check",
                    result_path=result_path.as_posix(),
                    sage_available=True,
                )
                jobs.append(job)
                payload = {
                    "job_id": job.job_id,
                    "signature": [3, 5, 5],
                    "sage_status": status,
                    "checked_levels": [30] if status == "completed" else [],
                    "newform_count": 1 if status == "completed" else 0,
                    "trace_match_status": "rigid" if status == "completed" else "not_checked",
                    "contradiction_claim_allowed": False,
                }
                result_path.write_text(json.dumps(payload), encoding="utf-8")
            rows = import_sage_results(jobs)
            by_status = {row.sage_status: row for row in rows}
            self.assertEqual(by_status["completed"].followup_label, "modular_followup_candidate")
            self.assertEqual(by_status["partial"].followup_label, "needs_external_sage_check")
            self.assertEqual(by_status["failed"].followup_label, "needs_external_sage_check")
            self.assertEqual(by_status["timeout"].followup_label, "needs_external_sage_check")

    def test_missing_sage_safety_marks_unavailable(self) -> None:
        job = SimpleNamespace(
            job_id="sage_missing",
            signature="3-5-5",
            route_label="needs_external_sage_check",
            result_path="missing.json",
            sage_available=False,
        )
        rows = import_sage_results([job])
        self.assertEqual(rows[0].sage_status, "unavailable")
        self.assertEqual(rows[0].followup_label, "needs_external_sage_check")
        self.assertFalse(rows[0].contradiction_claim_allowed)

    def test_modular_confidence_never_emits_proof_labels(self) -> None:
        job = SimpleNamespace(
            job_id="sage_3_5_5",
            signature="3-5-5",
            route_label="trace_rigid_candidate",
            candidate_case_ids=("mixed_3_5_5",),
            primes_involved=(31,),
            candidate_levels=(30,),
        )
        import_row = SimpleNamespace(
            job_id="sage_3_5_5",
            signature="3-5-5",
            sage_status="completed",
            newform_count=1,
            checked_levels=(30,),
            trace_match_status="rigid",
            contradiction_claim_allowed=False,
            followup_label="modular_followup_candidate",
            schema_valid=True,
            error_message="",
        )
        rows = update_modular_confidence([job], [import_row])
        labels = {row.updated_followup_label for row in rows}
        self.assertEqual(labels, {"modular_followup_candidate"})
        self.assertNotIn("proof", labels)
        self.assertNotIn("disproof", labels)
        self.assertFalse(rows[0].contradiction_claim_allowed)

    def test_known_cases_remain_calibrated_after_sage_import(self) -> None:
        artifact = SimpleNamespace(
            case_id="artifact_11_11_13",
            signature_text="11-11-13",
            expected_route="artifact",
            actual_route_label="artifact_like",
            known_status_label="subgroup_artifact",
            collision_class="artifact_dominates",
        )
        modular = SimpleNamespace(
            case_id="mixed_3_5_5",
            signature_text="3-5-5",
            expected_route="modular_method",
            actual_route_label="needs_external_sage_check",
            known_status_label="generalized_fermat_terrain",
            collision_class="terrain_dominates",
        )
        job = SimpleNamespace(job_id="sage_3_5_5", signature="3-5-5", candidate_case_ids=("mixed_3_5_5",))
        import_row = SimpleNamespace(job_id="sage_3_5_5", sage_status="completed", trace_match_status="rigid")
        confidence = SimpleNamespace(
            job_id="sage_3_5_5",
            signature="3-5-5",
            updated_followup_label="modular_followup_candidate",
            human_review_priority=7.0,
        )
        rows = calibrate_known_cases_with_sage([artifact, modular], [job], [import_row], [confidence])
        by_case = {row.case_id: row for row in rows}
        self.assertEqual(by_case["artifact_11_11_13"].post_sage_label, "artifact_like")
        self.assertFalse(by_case["artifact_11_11_13"].overpromoted)
        self.assertEqual(by_case["mixed_3_5_5"].post_sage_label, "modular_followup_candidate")
        self.assertFalse(by_case["mixed_3_5_5"].overpromoted)


if __name__ == "__main__":
    unittest.main()
