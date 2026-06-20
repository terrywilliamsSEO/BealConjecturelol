from __future__ import annotations

import random
import unittest

from beal_rsg_lab.rsg_residue_engine import (
    count_survivors,
    lift_survival_count,
    power_residue_set,
    random_subgroup_coset,
    randomized_control_stats,
    run_signature_prime,
)


class ResidueEngineTests(unittest.TestCase):
    def test_power_residue_sets_mod_prime(self) -> None:
        self.assertEqual(power_residue_set(2, 7), (1, 2, 4))
        self.assertEqual(power_residue_set(3, 7), (1, 6))
        self.assertEqual(power_residue_set(4, 5), (1,))

    def test_survivor_count_matches_independent_bruteforce(self) -> None:
        left = power_residue_set(2, 7)
        right = power_residue_set(2, 7)
        output = set(power_residue_set(2, 7))
        expected = 0
        for u in left:
            for v in right:
                if (u + v) % 7 in output:
                    expected += 1
        actual = count_survivors(left, right, output, 7)
        self.assertEqual(actual.count, expected)
        self.assertEqual(actual.pair_count, len(left) * len(right))

    def test_lift_survival_is_bounded_by_survivors(self) -> None:
        signature = (3, 3, 3)
        result = run_signature_prime(signature, 7, compute_lift=True, control_samples=0)
        lifted = lift_survival_count(signature, 7, ())
        self.assertEqual(lifted, 0)
        self.assertLessEqual(result.lift_survivor_count, result.survivor_count)
        self.assertGreaterEqual(result.lift_survival_rate, 0.0)
        self.assertLessEqual(result.lift_survival_rate, 1.0)

    def test_randomized_subgroup_control_is_deterministic_with_seed(self) -> None:
        rng_a = random.Random(123)
        rng_b = random.Random(123)
        self.assertEqual(random_subgroup_coset(13, 3, rng_a), random_subgroup_coset(13, 3, rng_b))

        stats_a = randomized_control_stats(13, (3, 3, 3), 0.2, samples=5, rng=random.Random(5))
        stats_b = randomized_control_stats(13, (3, 3, 3), 0.2, samples=5, rng=random.Random(5))
        self.assertEqual(stats_a, stats_b)
        self.assertEqual(stats_a.samples, 5)


if __name__ == "__main__":
    unittest.main()
