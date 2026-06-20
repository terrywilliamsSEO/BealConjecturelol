from __future__ import annotations

import json
import tempfile
from pathlib import Path
import unittest

from beal_rsg_lab.run_experiment import run_experiment


class RunExperimentTests(unittest.TestCase):
    def test_smoke_run_writes_required_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = run_experiment(
                output_root=Path(temp_dir),
                exponents=(3, 4),
                primes=(5, 7),
                compute_lift=False,
                control_samples=2,
                seed=99,
                timestamp="smoke",
            )
            self.assertTrue((output / "summary.csv").exists())
            self.assertTrue((output / "interesting_cases.csv").exists())
            self.assertTrue((output / "clusters.csv").exists())
            self.assertTrue((output / "README_REPORT.md").exists())
            self.assertTrue((output / "zero_support_summary.csv").exists())
            self.assertTrue((output / "direct_obstructions.csv").exists())
            self.assertTrue((output / "mandatory_single_divisor_candidates.csv").exists())
            self.assertTrue((output / "sparse_unit_clusters.csv").exists())
            self.assertTrue((output / "README_ZERO_SUPPORT_REPORT.md").exists())
            self.assertTrue((output / "unit_survivor_summary.csv").exists())
            self.assertTrue((output / "artifact_demotions.csv").exists())
            self.assertTrue((output / "unexplained_sparse_rows.csv").exists())
            self.assertTrue((output / "padic_unit_lift_results.csv").exists())
            self.assertTrue((output / "multi_prime_cluster_results.csv").exists())
            self.assertTrue((output / "README_UNIT_GEOMETRY_REPORT.md").exists())
            self.assertTrue((output / "modular_shadow_summary.csv").exists())
            self.assertTrue((output / "frey_template_candidates.csv").exists())
            self.assertTrue((output / "trace_probe_results.csv").exists())
            self.assertTrue((output / "cross_prime_trace_results.csv").exists())
            self.assertTrue((output / "newform_probe_results.csv").exists())
            self.assertTrue((output / "README_MODULAR_SHADOW_REPORT.md").exists())
            self.assertTrue((output / "known_case_calibration_summary.csv").exists())
            self.assertTrue((output / "route_confusion_matrix.csv").exists())
            self.assertTrue((output / "theorem_terrain_summary.csv").exists())
            self.assertTrue((output / "known_case_route_matrix.csv").exists())
            self.assertTrue((output / "remaining_true_mismatches.csv").exists())
            self.assertTrue((output / "route_collision_summary.csv").exists())
            self.assertTrue((output / "resolved_known_mismatches.csv").exists())
            self.assertTrue((output / "still_blocked_mismatches.csv").exists())
            self.assertTrue((output / "family_expansion_results.csv").exists())
            self.assertTrue((output / "route_prior_scores.csv").exists())
            self.assertTrue((output / "sage_export_manifest.csv").exists())
            self.assertTrue((output / "sage_job_manifest.csv").exists())
            self.assertTrue((output / "sage_import_results.csv").exists())
            self.assertTrue((output / "sage_known_case_calibration.csv").exists())
            self.assertTrue((output / "modular_confidence_summary.csv").exists())
            self.assertTrue((output / "sage_environment.json").exists())
            self.assertTrue((output / "sage_environment_report.md").exists())
            self.assertTrue((output / "sage_execution_manifest.csv").exists())
            self.assertTrue((output / "sage_roundtrip_summary.csv").exists())
            self.assertTrue((output / "candidate_dossier_index.md").exists())
            self.assertTrue((output / "README_KNOWN_CASE_CALIBRATION_REPORT.md").exists())
            self.assertTrue((output / "README_THEOREM_TERRAIN_REPORT.md").exists())
            self.assertTrue((output / "README_ROUTE_COLLISION_REPORT.md").exists())
            self.assertTrue((output / "README_SAGE_FOLLOWUP_REPORT.md").exists())
            metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["result_count"], 16)
            self.assertIn("zero_support_classification_counts", metadata)
            self.assertIn("unit_geometry_sparse_count", metadata)
            self.assertIn("modular_shadow_target_rows", metadata)
            self.assertIn("known_case_calibration_count", metadata)
            self.assertIn("known_case_theorem_terrain_route_count", metadata)
            self.assertIn("resolved_known_mismatch_count", metadata)
            self.assertIn("sage_job_count", metadata)
            self.assertIn("sage_execution_mode", metadata)
            self.assertIn("sage_import_unavailable_count", metadata)
            self.assertIn("sage_known_case_overpromotion_count", metadata)
            self.assertIn("candidate_dossier_count", metadata)


if __name__ == "__main__":
    unittest.main()
