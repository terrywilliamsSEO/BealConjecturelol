from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from beal_rsg_lab.candidate_dossier_generator import generate_candidate_dossiers
from beal_rsg_lab.sage_docker_runner import docker_batch_command
from beal_rsg_lab.sage_environment_detector import detect_sage_environment
from beal_rsg_lab.sage_followup_cli import build_parser, import_run, summarize_run


class SageExecutionSupportTests(unittest.TestCase):
    def test_environment_detector_prefers_native_sage(self) -> None:
        def which(name: str) -> str | None:
            return {"sage": "/usr/bin/sage", "docker": "/usr/bin/docker"}.get(name)

        def runner(command: list[str]) -> tuple[int, str, str]:
            if command[0] == "/usr/bin/sage":
                return 0, "SageMath version 10.3", ""
            if command[0] == "/usr/bin/docker":
                return 0, "Docker version 26", ""
            return 1, "", "missing"

        report = detect_sage_environment(which=which, runner=runner, environ={})
        self.assertEqual(report.execution_mode, "native_sage")
        self.assertTrue(report.native_sage)
        self.assertEqual(report.detected_version, "SageMath version 10.3")

    def test_environment_detector_falls_back_to_wsl(self) -> None:
        def which(name: str) -> str | None:
            return {"wsl": "wsl"}.get(name)

        def runner(command: list[str]) -> tuple[int, str, str]:
            return 0, "SageMath version 10.2", "" if command[:2] == ["wsl", "sage"] else "bad"

        report = detect_sage_environment(which=which, runner=runner, environ={})
        self.assertEqual(report.execution_mode, "wsl_sage")
        self.assertTrue(report.wsl_sage)

    def test_environment_detector_detects_docker(self) -> None:
        def which(name: str) -> str | None:
            return {"docker": "docker"}.get(name)

        def runner(command: list[str]) -> tuple[int, str, str]:
            return 0, "Docker version 26", ""

        report = detect_sage_environment(which=which, runner=runner, environ={})
        self.assertEqual(report.execution_mode, "docker")
        self.assertTrue(report.docker_available)

    def test_environment_detector_reports_unavailable(self) -> None:
        report = detect_sage_environment(which=lambda name: None, runner=lambda command: (1, "", "missing"), environ={})
        self.assertEqual(report.execution_mode, "unavailable")
        self.assertIn("native sage not found", report.failure_reason)

    def test_environment_detector_reports_ci_mode(self) -> None:
        report = detect_sage_environment(which=lambda name: None, runner=lambda command: (1, "", "missing"), environ={"CI": "true"})
        self.assertEqual(report.execution_mode, "ci")
        self.assertTrue(report.ci_mode)

    def test_docker_command_generation(self) -> None:
        command = docker_batch_command(
            repo_root=Path("/tmp/repo"),
            run_dir=Path("/tmp/repo/runs/demo"),
            image="sage:test",
        )
        self.assertEqual(command[0:3], ["docker", "run", "--rm"])
        self.assertIn("sage:test", command)
        self.assertIn("runs/demo/sage_jobs/run_all_sage_jobs.sage", command)

    def test_cli_command_parsing(self) -> None:
        parser = build_parser()
        detect = parser.parse_args(["detect", "--run-dir", "runs/demo"])
        generate = parser.parse_args(["generate", "--timestamp", "demo", "--no-lift"])
        importer = parser.parse_args(["import", "--run-dir", "runs/demo"])
        summarize = parser.parse_args(["summarize", "--run-dir", "runs/demo", "--dossier-dir", "docs/dossiers"])
        self.assertEqual(detect.command, "detect")
        self.assertEqual(generate.command, "generate")
        self.assertEqual(importer.command, "import")
        self.assertEqual(summarize.command, "summarize")

    def test_sage_json_roundtrip_import_command(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            (run_dir / "sage_results").mkdir()
            (run_dir / "sage_job_manifest.csv").write_text(
                "job_id,signature,route_label,candidate_case_ids,candidate_rows,primes_involved,candidate_levels,result_path,sage_available\n"
                f"sage_3_5_5,3-5-5,needs_external_sage_check,mixed_3_5_5,row,31,30,{(run_dir / 'sage_results' / 'sage_3_5_5.json').as_posix()},True\n",
                encoding="utf-8",
            )
            (run_dir / "known_case_calibration_summary.csv").write_text(
                "case_id,signature,expected_route,actual_route_label,known_status_label,collision_class\n"
                "mixed_3_5_5,3-5-5,modular_method,needs_external_sage_check,generalized_fermat_terrain,terrain_dominates\n",
                encoding="utf-8",
            )
            payload = {
                "job_id": "sage_3_5_5",
                "signature": [3, 5, 5],
                "sage_status": "completed",
                "checked_levels": [30],
                "newform_count": 1,
                "trace_match_status": "inconclusive",
                "contradiction_claim_allowed": False,
            }
            (run_dir / "sage_results" / "sage_3_5_5.json").write_text(json.dumps(payload), encoding="utf-8")
            import_run(run_dir)
            summary = (run_dir / "sage_roundtrip_summary.csv").read_text(encoding="utf-8")
            self.assertIn("sage_checked_inconclusive", summary)
            known = (run_dir / "sage_known_case_calibration.csv").read_text(encoding="utf-8")
            self.assertIn("False", known)

    def test_dossier_generation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            dossier_dir = Path(temp_dir) / "dossiers"
            records, index = generate_candidate_dossiers(
                run_dir=Path(temp_dir),
                dossier_dir=dossier_dir,
                job_rows=[
                    {
                        "job_id": "sage_3_4_3",
                        "signature": "3-4-3",
                        "route_label": "newform_check_candidate",
                        "candidate_case_ids": "mixed_3_4_3",
                        "candidate_rows": "modular_row:newform_check_candidate:ell=13",
                        "job_path": "runs/demo/sage_jobs/sage_3_4_3.sage",
                        "result_path": "runs/demo/sage_results/sage_3_4_3.json",
                    }
                ],
                import_rows=[
                    {
                        "job_id": "sage_3_4_3",
                        "signature": "3-4-3",
                        "sage_status": "unavailable",
                        "trace_match_status": "not_checked",
                        "newform_count": "0",
                    }
                ],
                confidence_rows=[
                    {
                        "job_id": "sage_3_4_3",
                        "signature": "3-4-3",
                        "updated_followup_label": "needs_external_sage_check",
                    }
                ],
                known_case_rows=[
                    {
                        "case_id": "mixed_3_4_3",
                        "signature": "3-4-3",
                        "known_status_label": "generalized_fermat_terrain",
                        "terrain_label": "known_modular_method_shape",
                        "theorem_route_label": "needs_external_sage_check",
                        "artifact_rows": "0",
                        "sparse_unit_rows": "1",
                        "padic_descent_rows": "0",
                        "unit_lift_rigid_or_collapsed_rows": "0",
                        "average_template_confidence": "0.58",
                    }
                ],
                unit_rows=[],
            )
            self.assertEqual(len(records), 1)
            dossier = (dossier_dir / "3-4-3.md").read_text(encoding="utf-8")
            self.assertIn("Recommended Next Mathematical Check", dossier)
            self.assertIn("contradiction_claim_allowed", dossier)
            self.assertIn("3-4-3.md", index)

    def test_summarize_run_writes_dossier_index(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir) / "run"
            run_dir.mkdir()
            (run_dir / "sage_job_manifest.csv").write_text(
                "job_id,signature,route_label,candidate_case_ids,candidate_rows,job_path,result_path\n"
                "sage_3_4_3,3-4-3,needs_external_sage_check,mixed_3_4_3,row,job,result\n",
                encoding="utf-8",
            )
            for filename in [
                "sage_import_results.csv",
                "modular_confidence_summary.csv",
                "known_case_calibration_summary.csv",
                "unit_survivor_summary.csv",
            ]:
                (run_dir / filename).write_text("", encoding="utf-8")
            records = summarize_run(run_dir, Path(temp_dir) / "docs" / "dossiers")
            self.assertEqual(len(records), 1)
            self.assertTrue((run_dir / "candidate_dossier_index.md").exists())


if __name__ == "__main__":
    unittest.main()
