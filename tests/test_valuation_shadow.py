from __future__ import annotations

import unittest

from beal_rsg_lab.rsg_modular_shadow import build_shadow_records
from beal_rsg_lab.rsg_residue_engine import run_signature_prime
from beal_rsg_lab.rsg_valuation_engine import analyze_results


class ValuationShadowTests(unittest.TestCase):
    def test_valuation_and_shadow_records_align(self) -> None:
        results = [
            run_signature_prime((3, 3, 3), 7, control_samples=3),
            run_signature_prime((3, 3, 3), 13, control_samples=3),
        ]
        valuations = analyze_results(results)
        shadows, clusters = build_shadow_records(results, valuations)

        self.assertEqual(len(valuations), len(results))
        self.assertEqual(len(shadows), len(results))
        self.assertTrue(clusters)
        for shadow in shadows:
            self.assertIn(shadow.promotion_status, {"promoted_candidate", "watchlist", "control_like"})
            self.assertTrue(shadow.frey_curve_placeholder.startswith("placeholder: Frey data"))


if __name__ == "__main__":
    unittest.main()
