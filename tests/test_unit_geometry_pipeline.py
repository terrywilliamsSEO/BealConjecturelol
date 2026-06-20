from __future__ import annotations

import unittest

from beal_rsg_lab.artifact_explainer import explain_artifacts
from beal_rsg_lab.character_fingerprint import compute_character_fingerprint
from beal_rsg_lab.padic_unit_lift import analyze_padic_unit_lift
from beal_rsg_lab.rsg_residue_engine import run_signature_prime
from beal_rsg_lab.unit_survivor_geometry import analyze_unit_survivor_geometry


class UnitGeometryPipelineTests(unittest.TestCase):
    def test_unit_geometry_captures_sparse_triples(self) -> None:
        result = run_signature_prime((3, 5, 5), 11, control_samples=0)
        geometry = analyze_unit_survivor_geometry(result)

        self.assertEqual(geometry.subgroup_size_shape, (10, 2, 2))
        self.assertEqual(geometry.survivor_count, 2)
        self.assertEqual(geometry.intersection_size_hp_hq_with_hr, 2)
        self.assertEqual(len(geometry.survivor_triples), 2)

    def test_artifact_explainer_demotes_order_two_power_images(self) -> None:
        result = run_signature_prime((3, 5, 5), 11, control_samples=0)
        geometry = analyze_unit_survivor_geometry(result)
        assessment = explain_artifacts([geometry])[0]

        self.assertEqual(assessment.verdict, "artifact_explained")
        self.assertIn("order_two_power_image", assessment.artifact_reasons)

    def test_character_and_unit_lift_records_are_populated(self) -> None:
        result = run_signature_prime((4, 5, 4), 13, control_samples=0)
        geometry = analyze_unit_survivor_geometry(result)
        character = compute_character_fingerprint(geometry)
        lift = analyze_padic_unit_lift(geometry)

        self.assertTrue(character.legendre_distribution)
        self.assertGreaterEqual(character.higher_character_order, 2)
        self.assertGreater(lift.ell2_lift_survival_count, 0)
        self.assertGreater(lift.ell3_lift_survival_count, 0)


if __name__ == "__main__":
    unittest.main()
