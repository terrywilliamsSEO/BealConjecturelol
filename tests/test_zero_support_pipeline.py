from __future__ import annotations

import unittest

from beal_rsg_lab.padic_lift_audit import audit_padic_lift
from beal_rsg_lab.primitive_obstruction_classifier import PrimitiveClassification, classify_primitive_obstructions
from beal_rsg_lab.rsg_residue_engine import run_signature_prime
from beal_rsg_lab.zero_support_engine import analyze_zero_support, zero_mask_for_values


class ZeroSupportPipelineTests(unittest.TestCase):
    def test_zero_mask_names_are_exact(self) -> None:
        self.assertEqual(zero_mask_for_values(1, 2, 3), "none")
        self.assertEqual(zero_mask_for_values(0, 2, 3), "A_only")
        self.assertEqual(zero_mask_for_values(1, 0, 3), "B_only")
        self.assertEqual(zero_mask_for_values(1, 2, 0), "C_only")
        self.assertEqual(zero_mask_for_values(0, 0, 3), "AB")
        self.assertEqual(zero_mask_for_values(0, 2, 0), "AC")
        self.assertEqual(zero_mask_for_values(1, 0, 0), "BC")
        self.assertEqual(zero_mask_for_values(0, 0, 0), "ABC")

    def test_fourth_power_mod_five_is_demoted_from_forced_single_claim(self) -> None:
        zero = analyze_zero_support((4, 7, 4), 5)
        self.assertEqual(zero.nonzero_survivor_count, 0)
        self.assertEqual(zero.minimum_zero_support_size, 1)
        self.assertEqual(zero.forced_zero_masks, ("A_only", "B_only", "C_only", "ABC"))
        self.assertEqual(zero.variable_forced_zero_if_any, ())
        self.assertEqual(zero.exact_single_variable_mask, "")

        result = run_signature_prime((4, 7, 4), 5, control_samples=0)
        classification = classify_primitive_obstructions([result], [zero])[0]
        self.assertEqual(classification.classification, "likely_small_prime_artifact")
        self.assertIn("tiny_prime", classification.artifact_reasons)

    def test_padic_audit_is_conservative_about_single_divisor_growth(self) -> None:
        classification = PrimitiveClassification(
            signature=(4, 3, 4),
            ell=5,
            classification="mandatory_single_divisor",
            lemma_candidate_tier="tier_2_single_divisor",
            lemma_candidate_score=0.0,
            forced_variable="B",
            artifact_reasons=(),
            subgroup_control_key="test",
            subgroup_control_class_size=1,
            subgroup_control_density_mean=0.0,
            subgroup_control_density_min=0.0,
            subgroup_control_density_max=0.0,
            subgroup_size_explained=False,
            structured_independent=True,
            rationale="test",
        )
        audit = audit_padic_lift(classification)
        self.assertGreater(audit.ell2_lift_count, 0)
        self.assertGreater(audit.ell3_lift_count, 0)
        self.assertEqual(audit.valuation_growth_estimate, "no_growth_detected_through_ell3")
        self.assertFalse(audit.descent_like_lift)


if __name__ == "__main__":
    unittest.main()
