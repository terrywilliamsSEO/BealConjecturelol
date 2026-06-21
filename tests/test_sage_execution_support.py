from __future__ import annotations

import json
from pathlib import Path
import subprocess
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from beal_rsg_lab.candidate_dossier_generator import generate_candidate_dossiers
from beal_rsg_lab.sage_docker_runner import docker_batch_command
from beal_rsg_lab.sage_environment_detector import detect_sage_environment
from beal_rsg_lab.sage_followup_cli import build_parser, import_run, summarize_run, command_roundtrip
from beal_rsg_lab.sage_job_runner import run_one_sage_job, run_sage_jobs
from beal_rsg_lab.sage_result_importer import validate_sage_result
from beal_rsg_lab.sage_smoke import sage_smoke_script_text


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
            text = " ".join(command)
            if "printf wsl-ok" in text:
                return 0, "wsl-ok", ""
            if "command -v sage" in text:
                return 0, "/usr/bin/sage", ""
            if "sage --version" in text:
                return 0, "SageMath version 10.2", ""
            return 1, "", "bad"

        report = detect_sage_environment(which=which, runner=runner, environ={})
        self.assertEqual(report.execution_mode, "wsl_sage")
        self.assertTrue(report.wsl_sage)
        self.assertTrue(report.wsl_launched)
        self.assertTrue(report.wsl_sage_binary_found)

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

    def test_ci_manifest_contains_roundtrip_and_artifact_upload(self) -> None:
        workflow = Path(".github/workflows/sage-followup.yml").read_text(encoding="utf-8")
        self.assertIn("sage_followup_cli roundtrip", workflow)
        self.assertIn("sage_smoke.json", workflow)
        self.assertIn("actions/upload-artifact", workflow)
        self.assertIn("sage_job_manifest.csv", workflow)
        self.assertIn("level_220_newform_coefficients.json", workflow)
        self.assertIn("sage_candidate_level_expander_545.sage", workflow)
        self.assertIn("candidate_level_newforms_545.json", workflow)
        self.assertIn("candidate_level_import_summary_545.csv", workflow)
        self.assertIn("level_route_ranking_545.csv", workflow)
        self.assertIn("trace_congruence_filter_545.csv", workflow)
        self.assertIn("FOCUSED_545_REVIEW.md", workflow)

    def test_runner_includes_candidate_level_expander_after_level_220(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            calls: list[str] = []

            def fake_run_one(job, **kwargs):
                calls.append(job.job_id)
                result_path = Path(job.result_path)
                result_path.parent.mkdir(parents=True, exist_ok=True)
                result_path.write_text(
                    json.dumps(
                        {
                            "job_id": job.job_id,
                            "signature": [5, 4, 5] if job.signature == "5-4-5" else [0, 0, 0],
                            "sage_status": "completed",
                            "checked_levels": [],
                            "newform_count": 0,
                            "trace_match_status": "not_checked",
                            "contradiction_claim_allowed": False,
                        }
                    ),
                    encoding="utf-8",
                )
                return SimpleNamespace(
                    job_id=job.job_id,
                    signature=job.signature,
                    execution_mode="native_sage",
                    command="sage",
                    result_path=job.result_path,
                    sage_status="completed",
                    return_code=0,
                    timed_out=False,
                    stdout_excerpt="",
                    stderr_excerpt="",
                    to_flat_dict=lambda: {},
                )

            env = SimpleNamespace(execution_mode="native_sage")
            with patch("beal_rsg_lab.sage_job_runner.run_one_sage_job", side_effect=fake_run_one):
                run_sage_jobs(
                    run_dir=run_dir,
                    jobs=[],
                    repo_root=Path.cwd(),
                    environment=env,
                    backend="native_sage",
                )
            self.assertEqual(
                calls[:3],
                ["sage_smoke", "level_220_newform_coefficients", "candidate_level_newforms_545"],
            )
            self.assertTrue((run_dir / "candidate_levels_545.csv").exists())
            self.assertTrue((run_dir / "sage_candidate_level_expander_545.sage").exists())

    def test_cli_command_parsing(self) -> None:
        parser = build_parser()
        detect = parser.parse_args(["detect", "--run-dir", "runs/demo"])
        generate = parser.parse_args(["generate", "--timestamp", "demo", "--no-lift"])
        importer = parser.parse_args(["import", "--run-dir", "runs/demo"])
        runner = parser.parse_args(["run", "--run-dir", "runs/demo", "--backend", "docker"])
        summarize = parser.parse_args(["summarize", "--run-dir", "runs/demo", "--dossier-dir", "docs/dossiers"])
        roundtrip = parser.parse_args(["roundtrip", "--run-dir", "runs/demo", "--skip-generate", "--backend", "docker"])
        self.assertEqual(detect.command, "detect")
        self.assertEqual(generate.command, "generate")
        self.assertEqual(importer.command, "import")
        self.assertEqual(runner.command, "run")
        self.assertEqual(summarize.command, "summarize")
        self.assertEqual(roundtrip.command, "roundtrip")

    def test_smoke_json_schema_fields(self) -> None:
        script = sage_smoke_script_text(Path("sage_results/sage_smoke.json"))
        self.assertIn('"job_id": "sage_smoke"', script)
        self.assertIn('"contradiction_claim_allowed": False', script)
        self.assertIn("def _json_safe", script)
        self.assertIn("py_int = builtins.int", script)
        payload = {
            "job_id": "sage_smoke",
            "signature": [0, 0, 0],
            "sage_status": "completed",
            "checked_levels": [11],
            "newform_count": 1,
            "trace_match_status": "not_checked",
            "contradiction_claim_allowed": False,
        }
        valid, error = validate_sage_result(payload)
        self.assertTrue(valid, error)

    def test_timeout_json_import_schema(self) -> None:
        payload = {
            "job_id": "sage_3_5_5",
            "signature": [3, 5, 5],
            "sage_status": "timeout",
            "checked_levels": [],
            "newform_count": 0,
            "trace_match_status": "not_checked",
            "contradiction_claim_allowed": False,
        }
        valid, error = validate_sage_result(payload)
        self.assertTrue(valid, error)

    def test_timeout_runner_writes_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            job_path = root / "job.sage"
            result_path = root / "result.json"
            job_path.write_text("print('slow')", encoding="utf-8")
            job = SimpleNamespace(
                job_id="sage_3_5_5",
                signature="3-5-5",
                route_label="needs_external_sage_check",
                job_path=job_path.as_posix(),
                result_path=result_path.as_posix(),
            )
            with patch(
                "beal_rsg_lab.sage_job_runner.subprocess.run",
                side_effect=subprocess.TimeoutExpired(["sage"], 1),
            ):
                record = run_one_sage_job(
                    job,
                    mode="native_sage",
                    repo_root=root,
                    timeout_seconds=1,
                )
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(record.sage_status, "timeout")
            self.assertEqual(payload["sage_status"], "timeout")
            self.assertFalse(payload["contradiction_claim_allowed"])

    def test_failed_runner_replaces_invalid_partial_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            job_path = root / "job.sage"
            result_path = root / "result.json"
            job_path.write_text("print('bad json')", encoding="utf-8")
            result_path.write_text('{"checked_levels": [', encoding="utf-8")
            job = SimpleNamespace(
                job_id="sage_3_5_5",
                signature="3-5-5",
                route_label="needs_external_sage_check",
                job_path=job_path.as_posix(),
                result_path=result_path.as_posix(),
            )
            completed = subprocess.CompletedProcess(["sage"], 1, stdout="", stderr="json crash")
            with patch("beal_rsg_lab.sage_job_runner.subprocess.run", return_value=completed):
                record = run_one_sage_job(
                    job,
                    mode="native_sage",
                    repo_root=root,
                    timeout_seconds=1,
                )
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(record.sage_status, "failed")
            self.assertEqual(payload["sage_status"], "failed")
            self.assertIn("json crash", payload["errors"][0])

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

    def test_roundtrip_command_with_mocked_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir) / "run"
            run_dir.mkdir()
            (run_dir / "sage_job_manifest.csv").write_text(
                "job_id,signature,route_label,candidate_case_ids,candidate_rows,primes_involved,candidate_levels,job_path,result_path,sage_available\n"
                f"sage_3_5_5,3-5-5,needs_external_sage_check,mixed_3_5_5,row,31,30,{(run_dir / 'job.sage').as_posix()},{(run_dir / 'sage_results' / 'sage_3_5_5.json').as_posix()},True\n",
                encoding="utf-8",
            )
            (run_dir / "known_case_calibration_summary.csv").write_text(
                "case_id,signature,expected_route,actual_route_label,known_status_label,collision_class\n"
                "mixed_3_5_5,3-5-5,modular_method,needs_external_sage_check,generalized_fermat_terrain,terrain_dominates\n",
                encoding="utf-8",
            )
            (run_dir / "unit_survivor_summary.csv").write_text("", encoding="utf-8")

            def fake_run_sage_jobs(**kwargs):
                result_dir = run_dir / "sage_results"
                result_dir.mkdir()
                smoke = {
                    "job_id": "sage_smoke",
                    "signature": [0, 0, 0],
                    "sage_status": "completed",
                    "checked_levels": [11],
                    "newform_count": 1,
                    "trace_match_status": "not_checked",
                    "contradiction_claim_allowed": False,
                }
                real = {
                    "job_id": "sage_3_5_5",
                    "signature": [3, 5, 5],
                    "route_label": "needs_external_sage_check",
                    "sage_status": "completed",
                    "checked_levels": [30],
                    "newform_count": 1,
                    "trace_match_status": "inconclusive",
                    "contradiction_claim_allowed": False,
                }
                (result_dir / "sage_smoke.json").write_text(json.dumps(smoke), encoding="utf-8")
                (result_dir / "sage_3_5_5.json").write_text(json.dumps(real), encoding="utf-8")
                return []

            args = SimpleNamespace(
                skip_generate=True,
                run_dir=run_dir.as_posix(),
                output_root=temp_dir,
                prime_limit=31,
                control_samples=1,
                no_lift=True,
                timestamp=None,
                backend="native_sage",
                timeout_seconds=1,
                dossier_dir=(Path(temp_dir) / "dossiers").as_posix(),
            )
            with patch("beal_rsg_lab.sage_followup_cli.run_sage_jobs", side_effect=fake_run_sage_jobs):
                code = command_roundtrip(args)
            self.assertEqual(code, 0)
            self.assertTrue((run_dir / "sage_roundtrip_summary.csv").exists())
            self.assertTrue((Path(temp_dir) / "dossiers" / "3-5-5.md").exists())

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
