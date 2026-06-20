from __future__ import annotations

import unittest

from beal_rsg_lab.finite_field_trace_probe import (
    count_points_on_frey_curve,
    is_singular_frey_curve,
    trace_probe_for_geometry,
)
from beal_rsg_lab.rsg_residue_engine import run_signature_prime
from beal_rsg_lab.signature_normalizer import canonicalize_signature, normalize_signature
from beal_rsg_lab.unit_survivor_geometry import analyze_unit_survivor_geometry


class ModularShadowPipelineTests(unittest.TestCase):
    def test_signature_normalization_swaps_a_b_only(self) -> None:
        canonical, swapped = canonicalize_signature((7, 4, 7))
        self.assertEqual(canonical, (4, 7, 7))
        self.assertTrue(swapped)

        metadata = normalize_signature((7, 4, 7))
        self.assertEqual(metadata.canonical_signature_id, "4-7-7")
        self.assertTrue(metadata.fourth_power_involvement)
        self.assertTrue(metadata.has_repeated_exponent)
        self.assertTrue(metadata.target_route)

    def test_point_count_for_small_frey_curve(self) -> None:
        self.assertEqual(count_points_on_frey_curve(1, 1, 5), 8)

    def test_singular_frey_curve_is_skipped_safely(self) -> None:
        self.assertTrue(is_singular_frey_curve(1, 4, 5))
        with self.assertRaises(ValueError):
            count_points_on_frey_curve(1, 4, 5)

    def test_trace_distribution_compares_to_same_size_control(self) -> None:
        result = run_signature_prime((4, 7, 7), 29, control_samples=0)
        geometry = analyze_unit_survivor_geometry(result)
        trace = trace_probe_for_geometry(geometry)

        self.assertEqual(trace.singular_skipped_count, 0)
        self.assertEqual(trace.trace_support_size, trace.same_size_control_trace_support_size)
        self.assertFalse(trace.unusually_narrow_trace)


if __name__ == "__main__":
    unittest.main()
