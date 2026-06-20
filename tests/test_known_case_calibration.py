from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from beal_rsg_lab.known_case_library import load_known_cases
from beal_rsg_lab.route_confusion_matrix import build_route_confusion_matrix
from beal_rsg_lab.route_prior_model import score_route_priors
from beal_rsg_lab.sage_export_scripts import export_sage_scripts, sage_script_text
from beal_rsg_lab.signature_family_expander import expanded_signatures


class KnownCaseCalibrationTests(unittest.TestCase):
    def test_load_known_case_library(self) -> None:
        cases = load_known_cases()
        case_ids = {case.case_id for case in cases}
        self.assertIn("diag_3", case_ids)
        self.assertIn("artifact_11_11_13", case_ids)
        self.assertTrue(all(len(case.signature) == 3 for case in cases))

    def test_signature_family_expansion_contains_structured_neighbors(self) -> None:
        signatures = expanded_signatures(exponents=(3, 4, 5))
        self.assertEqual(signatures[(3, 3, 3)], "diagonal_family")
        self.assertEqual(signatures[(4, 5, 5)], "beal_candidate_neighborhood")
        self.assertEqual(signatures[(3, 4, 5)], "mixed_bridge")

    def test_route_confusion_matrix_generation(self) -> None:
        records = [
            SimpleNamespace(
                case_id="artifact_case",
                signature_text="11-11-13",
                known_status="calibration_only",
                expected_route="artifact",
                system_route_label="artifact_like",
                actual_route_label="artifact_like",
                comparison_flag="artifact_match",
            ),
            SimpleNamespace(
                case_id="flt_case",
                signature_text="3-3-3",
                known_status="known_impossible",
                expected_route="FLT_style",
                system_route_label="not_promising_yet",
                actual_route_label="known_case_mismatch",
                comparison_flag="underpromotion",
            ),
        ]
        matrix = build_route_confusion_matrix(records)
        buckets = {row.bucket: row.case_count for row in matrix}
        self.assertEqual(buckets["artifact_correctly_demoted"], 1)
        self.assertEqual(buckets["known_impossible_system_weak"], 1)

    def test_route_prior_scoring_penalizes_artifacts(self) -> None:
        record = SimpleNamespace(
            case_id="artifact_case",
            signature_text="11-11-13",
            family_label="artifact_calibrator",
            known_status="calibration_only",
            expected_route="artifact",
            actual_route_label="artifact_like",
            comparison_flag="artifact_match",
            prime_count=2,
            local_obstruction_rows=0,
            mandatory_single_divisor_rows=0,
            sparse_unit_rows=2,
            artifact_rows=2,
            nonartifact_sparse_rows=0,
            padic_descent_rows=0,
            trace_rigid_rows=0,
            newform_check_rows=0,
            frey_template_candidate_rows=0,
            average_template_confidence=0.5,
        )
        scores = score_route_priors([record], [])
        self.assertEqual(scores[0].output_label, "artifact_like")
        self.assertGreaterEqual(scores[0].artifact_likelihood, 0.65)

    def test_sage_script_export_formatting(self) -> None:
        script = sage_script_text(case_id="demo", signature=(3, 4, 5), ell=11)
        self.assertIn("F = GF(ell)", script)
        self.assertIn("EllipticCurve", script)
        self.assertIn("does not prove a theorem", script)

    def test_sage_export_is_safe_when_sage_unavailable(self) -> None:
        score = SimpleNamespace(
            case_id="demo",
            signature="3-4-5",
            output_label="needs_external_sage_check",
            discovery_readiness_score=4.0,
            proof_route_priority=5.0,
        )
        record = SimpleNamespace(
            case_id="demo",
            signature_text="3-4-5",
            expected_route="modular_method",
            actual_route_label="needs_external_sage_check",
            strongest_prime=11,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("beal_rsg_lab.sage_export_scripts.shutil.which", return_value=None):
                manifest = export_sage_scripts([score], [record], Path(temp_dir))
            self.assertEqual(len(manifest), 1)
            self.assertFalse(manifest[0].sage_available)
            self.assertTrue(Path(manifest[0].script_path).exists())


if __name__ == "__main__":
    unittest.main()
