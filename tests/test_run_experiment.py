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
            metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["result_count"], 16)


if __name__ == "__main__":
    unittest.main()
