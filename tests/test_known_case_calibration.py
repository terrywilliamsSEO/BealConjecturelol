from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from beal_rsg_lab.calibration_confusion_matrix import build_calibration_confusion_matrix
from beal_rsg_lab.known_case_library import load_known_cases
from beal_rsg_lab.route_prior_model import score_route_priors
from beal_rsg_lab.route_collision_resolver import resolve_route_collision
from beal_rsg_lab.sage_export_scripts import export_sage_scripts, sage_script_text
from beal_rsg_lab.signature_family_expander import expanded_signatures
from beal_rsg_lab.theorem_terrain_classifier import classify_theorem_terrain, load_known_theorem_library


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

    def test_diagonal_signatures_route_to_theorem_terrain(self) -> None:
        terrain = classify_theorem_terrain((3, 3, 3))
        self.assertEqual(terrain.terrain_label, "diagonal_flt_style")
        self.assertEqual(terrain.terrain_route_label, "theorem_terrain_route")
        self.assertEqual(terrain.known_status_label, "known_solved_terrain")

    def test_artifact_calibrators_remain_demoted(self) -> None:
        terrain = classify_theorem_terrain((11, 11, 13), ell=23)
        self.assertEqual(terrain.terrain_label, "artifact_prone_shape")
        self.assertEqual(terrain.terrain_route_label, "artifact_like")

    def test_sage_needed_cases_remain_external_check_only(self) -> None:
        terrain = classify_theorem_terrain((3, 5, 5))
        self.assertEqual(terrain.terrain_route_label, "needs_external_sage_check")
        self.assertFalse(terrain.should_promote_without_external_check)

    def test_known_theorem_library_loads(self) -> None:
        terrains = load_known_theorem_library()
        labels = {terrain.terrain_label for terrain in terrains}
        self.assertIn("diagonal_flt_style", labels)
        self.assertIn("artifact_prone_shape", labels)

    def test_route_confusion_matrix_generation(self) -> None:
        records = [
            SimpleNamespace(
                case_id="artifact_case",
                signature_text="11-11-13",
                known_status="calibration_only",
                expected_route="artifact",
                terrain_label="artifact_prone_shape",
                known_status_label="subgroup_artifact",
                system_route_label="artifact_like",
                actual_route_label="artifact_like",
                comparison_flag="artifact_match",
                collision_class="artifact_dominates",
                should_promote_without_external_check=False,
            ),
            SimpleNamespace(
                case_id="flt_case",
                signature_text="3-3-3",
                known_status="known_impossible",
                expected_route="descent_or_modularity",
                terrain_label="diagonal_flt_style",
                known_status_label="known_solved_terrain",
                system_route_label="theorem_terrain_route",
                actual_route_label="theorem_terrain_route",
                comparison_flag="terrain_match",
                collision_class="terrain_dominates",
                should_promote_without_external_check=False,
            ),
        ]
        matrix = build_calibration_confusion_matrix(records)
        buckets = {row.bucket: row.case_count for row in matrix}
        self.assertEqual(buckets["correct_artifact_demotion"], 1)
        self.assertEqual(buckets["correct_theorem_terrain_route"], 1)
        self.assertNotIn("true_mismatch", buckets)

    def test_route_prior_scoring_penalizes_artifacts(self) -> None:
        record = SimpleNamespace(
            case_id="artifact_case",
            signature_text="11-11-13",
            family_label="artifact_calibrator",
            known_status="calibration_only",
            expected_route="artifact",
            terrain_label="artifact_prone_shape",
            known_status_label="subgroup_artifact",
            theorem_route_label="artifact_like",
            actual_route_label="artifact_like",
            comparison_flag="artifact_match",
            collision_class="artifact_dominates",
            collision_resolved_route_label="artifact_like",
            should_promote_without_external_check=False,
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

    def test_artifact_row_does_not_globally_demote_known_modular_signature(self) -> None:
        terrain = classify_theorem_terrain((5, 3, 5), ell=11)
        signature = (5, 3, 5)
        key = (signature, 11)
        collision = resolve_route_collision(
            case_id="mixed_5_3_5",
            signature=signature,
            keys=[key],
            terrain=terrain,
            primitive_by_key={key: SimpleNamespace(classification="sparse_unit_survivor")},
            artifact_by_key={key: SimpleNamespace(verdict="artifact_explained")},
            route_by_key={},
            unit_lift_by_key={},
            padic_by_key={},
            expected_route="modular_method",
            initial_route_label="artifact_like",
        )
        self.assertEqual(collision.collision_class, "mixed_needs_external_check")
        self.assertEqual(collision.resolved_route_label, "needs_external_sage_check")

    def test_true_subgroup_artifacts_still_demote(self) -> None:
        terrain = classify_theorem_terrain((11, 11, 13), ell=23)
        signature = (11, 11, 13)
        key = (signature, 23)
        collision = resolve_route_collision(
            case_id="artifact_11_11_13",
            signature=signature,
            keys=[key],
            terrain=terrain,
            primitive_by_key={key: SimpleNamespace(classification="sparse_unit_survivor")},
            artifact_by_key={key: SimpleNamespace(verdict="artifact_explained")},
            route_by_key={},
            unit_lift_by_key={},
            padic_by_key={},
            expected_route="artifact",
            initial_route_label="artifact_like",
        )
        self.assertEqual(collision.collision_class, "artifact_dominates")
        self.assertEqual(collision.resolved_route_label, "artifact_like")

    def test_no_candidate_promotes_without_terrain_calibration(self) -> None:
        record = SimpleNamespace(
            case_id="unknown_case",
            signature_text="3-7-11",
            family_label="unknown",
            known_status="open_or_unknown",
            expected_route="unknown",
            terrain_label="mixed_prime_signature",
            known_status_label="unclassified_terrain",
            theorem_route_label="calibrated_route_candidate",
            actual_route_label="calibrated_route_candidate",
            comparison_flag="uncertain",
            collision_class="overpromotion_risk",
            collision_resolved_route_label="not_promising_yet",
            should_promote_without_external_check=False,
            prime_count=2,
            local_obstruction_rows=2,
            mandatory_single_divisor_rows=0,
            sparse_unit_rows=0,
            artifact_rows=0,
            nonartifact_sparse_rows=0,
            padic_descent_rows=0,
            trace_rigid_rows=0,
            newform_check_rows=0,
            frey_template_candidate_rows=0,
            average_template_confidence=0.5,
        )
        scores = score_route_priors([record], [])
        self.assertNotEqual(scores[0].output_label, "calibrated_route_candidate")

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
