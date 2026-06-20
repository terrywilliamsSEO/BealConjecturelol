"""Experiment runner for the Beal RSG lab."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
from pathlib import Path
from typing import Iterable

from .artifact_explainer import explain_artifacts
from .calibration_runner import build_known_case_calibration
from .character_fingerprint import compute_character_fingerprints
from .cross_prime_trace_compatibility import analyze_cross_prime_traces
from .exact_explanation_generator import generate_explanations
from .exact_sparse_lemma_generator import generate_sparse_lemma_explanations
from .finite_field_trace_probe import trace_probes_for_geometries
from .frey_template_library import build_template_records
from .multi_prime_compatibility import analyze_multi_prime_compatibility
from .modular_route_classifier import classify_modular_routes
from .modular_shadow_engine import build_modular_shadow_routes
from .number_theory import primes_up_to
from .padic_lift_audit import audit_padic_lifts
from .padic_unit_lift import analyze_padic_unit_lifts
from .primitive_obstruction_classifier import classify_primitive_obstructions, sparse_unit_clusters
from .rsg_modular_shadow import ShadowRecord, build_shadow_records
from .rsg_residue_engine import DEFAULT_EXPONENTS, parse_prime_list, run_sweep
from .rsg_valuation_engine import analyze_results
from .sage_optional_newform_probe import run_optional_newform_probe
from .signature_normalizer import normalize_signature
from .unit_survivor_geometry import analyze_sparse_unit_geometries
from .zero_support_engine import analyze_zero_support_results


def _write_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    row_list = list(rows)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in row_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row_list)


def _merged_summary_rows(results, valuations, shadows) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    shadow_by_key = {(shadow.signature, shadow.ell): shadow for shadow in shadows}
    valuation_by_key = {(valuation.signature, valuation.ell): valuation for valuation in valuations}
    for result in results:
        key = (result.signature, result.ell)
        row = result.to_flat_dict()
        valuation = valuation_by_key[key]
        shadow = shadow_by_key[key]
        for prefix, payload in (
            ("valuation", valuation.to_flat_dict()),
            ("shadow", shadow.to_flat_dict()),
        ):
            for field, value in payload.items():
                if field in {"signature", "ell"}:
                    continue
                row[f"{prefix}_{field}"] = value
        rows.append(row)
    return rows


def _zero_support_summary_rows(results, zero_records, classifications) -> list[dict[str, object]]:
    """Return CSV rows joining residue, zero-support, and primitive classification."""
    result_by_key = {(result.signature, result.ell): result for result in results}
    classification_by_key = {
        (classification.signature, classification.ell): classification
        for classification in classifications
    }
    rows: list[dict[str, object]] = []
    for zero in zero_records:
        key = (zero.signature, zero.ell)
        row = result_by_key[key].to_flat_dict()
        for prefix, payload in (
            ("zero", zero.to_flat_dict()),
            ("primitive", classification_by_key[key].to_flat_dict()),
        ):
            for field, value in payload.items():
                if field in {"signature", "ell"}:
                    continue
                row[f"{prefix}_{field}"] = value
        rows.append(row)
    return rows


def _classification_rows(classifications, zero_records, explanations, *, classification_name: str) -> list[dict[str, object]]:
    zero_by_key = {(zero.signature, zero.ell): zero for zero in zero_records}
    explanation_by_key = {
        (explanation.signature, explanation.ell): explanation
        for explanation in explanations
    }
    rows: list[dict[str, object]] = []
    for item in classifications:
        if item.classification != classification_name:
            continue
        key = (item.signature, item.ell)
        row = item.to_flat_dict()
        zero = zero_by_key[key]
        row.update(
            {
                "zero_forced_zero_masks": ";".join(zero.forced_zero_masks),
                "zero_occurring_zero_masks": ";".join(zero.occurring_zero_masks),
                "zero_minimum_zero_support_size": zero.minimum_zero_support_size,
                "zero_dominant_zero_mask": zero.dominant_zero_mask,
                "zero_nonzero_survivor_count": zero.nonzero_survivor_count,
                "zero_adjoined_survivor_count": zero.zero_adjoined_survivor_count,
            }
        )
        if key in explanation_by_key:
            row["modular_explanation"] = explanation_by_key[key].modular_explanation
            row["proof_gap"] = explanation_by_key[key].proof_gap
        rows.append(row)
    rows.sort(key=lambda row: float(row["lemma_candidate_score"]), reverse=True)
    return rows


def _mandatory_rows(classifications, zero_records, audits, explanations) -> list[dict[str, object]]:
    rows = _classification_rows(
        classifications,
        zero_records,
        explanations,
        classification_name="mandatory_single_divisor",
    )
    audit_by_key = {(audit.signature, audit.ell): audit for audit in audits}
    for row in rows:
        signature = tuple(int(part) for part in row["signature"].split("-"))
        key = (signature, int(row["ell"]))
        audit = audit_by_key.get(key)
        if audit is None:
            continue
        for field, value in audit.to_flat_dict().items():
            if field in {"signature", "ell"}:
                continue
            row[f"padic_{field}"] = value
    return rows


def _unit_geometry_summary_rows(geometries, assessments, characters, lifts) -> list[dict[str, object]]:
    """Return joined sparse unit-geometry rows."""
    assessment_by_key = {(item.signature, item.ell): item for item in assessments}
    character_by_key = {(item.signature, item.ell): item for item in characters}
    lift_by_key = {(item.signature, item.ell): item for item in lifts}
    rows: list[dict[str, object]] = []
    for geometry in geometries:
        key = (geometry.signature, geometry.ell)
        row: dict[str, object] = {}
        for prefix, payload in (
            ("geometry", geometry.to_flat_dict()),
            ("artifact", assessment_by_key[key].to_flat_dict()),
            ("character", character_by_key[key].to_flat_dict()),
            ("unit_lift", lift_by_key[key].to_flat_dict()),
        ):
            for field, value in payload.items():
                if field in {"signature", "ell"} and prefix != "geometry":
                    continue
                row[f"{prefix}_{field}" if field not in {"signature", "ell"} else field] = value
        rows.append(row)
    rows.sort(
        key=lambda row: (
            row["artifact_verdict"] != "artifact_explained",
            row["unit_lift_collapse_or_rigid"],
            float(row["unit_lift_unit_lift_rigidity_score"]),
        ),
        reverse=True,
    )
    return rows


def _artifact_rows(unit_summary_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row for row in unit_summary_rows if row["artifact_verdict"] == "artifact_explained"]


def _unexplained_sparse_rows(unit_summary_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row for row in unit_summary_rows if row["artifact_verdict"] != "artifact_explained"]


def _target_geometries(geometries) -> list[object]:
    return [geometry for geometry in geometries if normalize_signature(geometry.signature).target_route]


def _modular_shadow_summary_rows(routes, classifications, traces) -> list[dict[str, object]]:
    classification_by_key = {
        (classification.signature, classification.ell): classification
        for classification in classifications
    }
    trace_by_key = {(trace.signature, trace.ell): trace for trace in traces}
    rows: list[dict[str, object]] = []
    for route in routes:
        key = (route.signature, route.ell)
        row = route.to_flat_dict()
        for prefix, payload in (
            ("route", classification_by_key[key].to_flat_dict()),
            ("trace", trace_by_key[key].to_flat_dict()),
        ):
            for field, value in payload.items():
                if field in {"signature", "ell"}:
                    continue
                row[f"{prefix}_{field}"] = value
        rows.append(row)
    rows.sort(
        key=lambda row: (
            row["route_promotion_status"] == "proof-route candidate",
            row["route_route_classification"] == "newform_check_candidate",
            float(row["route_route_rank_score"]),
        ),
        reverse=True,
    )
    return rows


def _interesting_rows(shadows: Iterable[ShadowRecord], limit: int | None = None) -> list[dict[str, object]]:
    interesting = [
        shadow
        for shadow in shadows
        if shadow.promotion_status in {"promoted_candidate", "watchlist"}
    ]
    interesting.sort(key=lambda shadow: (shadow.promotion_status == "promoted_candidate", shadow.candidate_score), reverse=True)
    if limit is not None:
        interesting = interesting[:limit]
    return [shadow.to_flat_dict() for shadow in interesting]


def _report_markdown(
    *,
    output_dir: Path,
    result_count: int,
    interesting_count: int,
    promoted_count: int,
    prime_values: tuple[int, ...],
    control_samples: int,
    compute_lift: bool,
    top_cases: list[dict[str, object]],
) -> str:
    generated = datetime.now().isoformat(timespec="seconds")
    prime_text = ", ".join(str(prime) for prime in prime_values)
    lines = [
        "# RSG Experiment Report",
        "",
        f"Generated: `{generated}`",
        f"Output directory: `{output_dir.as_posix()}`",
        "",
        "## Scope",
        "",
        f"- Rows: `{result_count}` signature/prime cases.",
        f"- Primes: `{prime_text}`.",
        f"- Control samples per row: `{control_samples}`.",
        f"- Lift survival computed: `{compute_lift}`.",
        "",
        "## Interpretation Guardrail",
        "",
        "This report ranks obstruction candidates. It does not claim a proof of Beal or any generalized Fermat case.",
        "",
        "A promoted candidate repeats across a cluster, beats randomized subgroup-coset controls, and carries a valuation or lift flag.",
        "",
        "## Candidate Counts",
        "",
        f"- Promoted candidates: `{promoted_count}`.",
        f"- Promoted plus watchlist rows: `{interesting_count}`.",
        "",
        "## Top Rows",
        "",
    ]
    if not top_cases:
        lines.append("No rows passed the promoted/watchlist filters in this run.")
    else:
        lines.extend(
            [
                "| rank | status | signature | ell | score | cluster_size | rationale |",
                "| ---: | --- | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for index, row in enumerate(top_cases[:12], start=1):
            lines.append(
                "| {rank} | {status} | {signature} | {ell} | {score} | {cluster_size} | {rationale} |".format(
                    rank=index,
                    status=row["promotion_status"],
                    signature=row["signature"],
                    ell=row["ell"],
                    score=row["candidate_score"],
                    cluster_size=row["cluster_size"],
                    rationale=row["rationale"],
                )
            )
    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `summary.csv`: complete row-level data.",
            "- `interesting_cases.csv`: promoted and watchlist candidates.",
            "- `clusters.csv`: repeated obstruction fingerprints.",
            "- `metadata.json`: run parameters.",
            "",
            "## Next Research Step",
            "",
            "Inspect the strongest clusters and try to restate them as exact local lemmas. Any lemma candidate should then be tested against additional primes and a stricter lift/modular-shadow consistency check.",
            "",
        ]
    )
    return "\n".join(lines)


def _zero_support_report_markdown(
    *,
    output_dir: Path,
    result_count: int,
    classification_counts: dict[str, int],
    direct_rows: list[dict[str, object]],
    mandatory_rows: list[dict[str, object]],
    sparse_clusters: list[dict[str, object]],
    explanation_rows: list[dict[str, object]],
) -> str:
    generated = datetime.now().isoformat(timespec="seconds")
    lines = [
        "# Zero-Support Obstruction Report",
        "",
        f"Generated: `{generated}`",
        f"Output directory: `{output_dir.as_posix()}`",
        "",
        "## Interpretation Guardrail",
        "",
        "This report upgrades zero-class dominance into exact zero-support classification. It does not claim a proof of Beal.",
        "",
        "A primitive contradiction is only suggested when local survival forces at least two variables to be divisible by the same prime, or when a single forced divisor strengthens under p-adic lifting.",
        "",
        "## Classification Counts",
        "",
        f"- Rows analyzed: `{result_count}`.",
    ]
    for name in sorted(classification_counts):
        lines.append(f"- `{name}`: `{classification_counts[name]}`.")

    lines.extend(
        [
            "",
            "## Direct Primitive Obstructions",
            "",
        ]
    )
    if not direct_rows:
        lines.append("No non-artifact direct primitive obstructions were found in this run.")
    else:
        lines.extend(
            [
                "| rank | signature | ell | score | forced masks | rationale |",
                "| ---: | --- | ---: | ---: | --- | --- |",
            ]
        )
        for index, row in enumerate(direct_rows[:12], start=1):
            lines.append(
                f"| {index} | {row['signature']} | {row['ell']} | {row['lemma_candidate_score']} | "
                f"{row['zero_forced_zero_masks']} | {row['rationale']} |"
            )

    lines.extend(
        [
            "",
            "## Mandatory Single-Divisor Candidates",
            "",
        ]
    )
    if not mandatory_rows:
        lines.append("No exact mandatory single-divisor candidates survived the artifact filters in this run.")
    else:
        lines.extend(
            [
                "| rank | signature | ell | variable | score | p-adic estimate |",
                "| ---: | --- | ---: | --- | ---: | --- |",
            ]
        )
        for index, row in enumerate(mandatory_rows[:12], start=1):
            lines.append(
                f"| {index} | {row['signature']} | {row['ell']} | {row['forced_variable']} | "
                f"{row['lemma_candidate_score']} | {row.get('padic_valuation_growth_estimate', '')} |"
            )

    lines.extend(
        [
            "",
            "## Sparse Unit Clusters",
            "",
        ]
    )
    if not sparse_clusters:
        lines.append("No larger-prime sparse unit-survivor clusters survived the exact zero-support filters.")
    else:
        lines.extend(
            [
                "| rank | cluster | size | primes | signatures | best score |",
                "| ---: | --- | ---: | --- | ---: | ---: |",
            ]
        )
        for index, row in enumerate(sparse_clusters[:12], start=1):
            lines.append(
                f"| {index} | {row['cluster_key']} | {row['size']} | {row['primes']} | "
                f"{row['signature_count']} | {row['best_score']} |"
            )

    lines.extend(
        [
            "",
            "## Exact Explanations",
            "",
        ]
    )
    for row in explanation_rows[:8]:
        lines.extend(
            [
                f"### {row['signature']} at ell={row['ell']}",
                "",
                row["modular_explanation"],
                "",
                f"Proof gap: {row['proof_gap']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Files",
            "",
            "- `zero_support_summary.csv`: row-level zero-support and classification data.",
            "- `direct_obstructions.csv`: exact direct primitive obstruction candidates.",
            "- `mandatory_single_divisor_candidates.csv`: exact one-variable candidates with p-adic audit fields.",
            "- `sparse_unit_clusters.csv`: larger-prime sparse unit-survivor clusters.",
            "- `exact_explanations.csv`: generated modular explanations for top rows.",
            "",
            "## Next Proof Work",
            "",
            "Rows in `likely_small_prime_artifact` are useful controls, not headline evidence. The best next proof work is to search for non-artifact direct rows, or mandatory single-divisor rows whose lift branch dies or forces valuation growth beyond v_ell=1.",
            "",
        ]
    )
    return "\n".join(lines)


def _unit_geometry_report_markdown(
    *,
    output_dir: Path,
    sparse_count: int,
    artifact_count: int,
    unexplained_count: int,
    rigid_lift_count: int,
    multi_prime_count: int,
    unit_rows: list[dict[str, object]],
    unexplained_rows: list[dict[str, object]],
    artifact_rows: list[dict[str, object]],
    multi_prime_rows: list[dict[str, object]],
    sparse_explanations: list[dict[str, object]],
) -> str:
    generated = datetime.now().isoformat(timespec="seconds")
    lines = [
        "# Unit-Survivor Geometry Report",
        "",
        f"Generated: `{generated}`",
        f"Output directory: `{output_dir.as_posix()}`",
        "",
        "## Interpretation Guardrail",
        "",
        "This report studies sparse nonzero unit survivors. It does not claim a proof of Beal.",
        "",
        "Rows are demoted when sparsity is explained by tiny power images, order-two subgroups, or identical subgroup-size controls. Remaining rows are ranked as lemma candidates only when p-adic unit lifts collapse or become rigid; otherwise they need modular-shadow follow-up.",
        "",
        "## Counts",
        "",
        f"- Sparse unit rows analyzed: `{sparse_count}`.",
        f"- Artifact explained rows: `{artifact_count}`.",
        f"- Unexplained sparse rows: `{unexplained_count}`.",
        f"- Collapse/rigid unit-lift rows: `{rigid_lift_count}`.",
        f"- Multi-prime compatibility records: `{multi_prime_count}`.",
        "",
        "## Highest Ranked Unexplained Rows",
        "",
    ]
    if not unexplained_rows:
        lines.append("No sparse rows survived artifact demotion.")
    else:
        lines.extend(
            [
                "| rank | signature | ell | density | status | lift | score |",
                "| ---: | --- | ---: | ---: | --- | --- | ---: |",
            ]
        )
        for index, row in enumerate(unexplained_rows[:12], start=1):
            lines.append(
                f"| {index} | {row['signature']} | {row['ell']} | {row['geometry_density']} | "
                f"{row['artifact_lemma_candidate_rank']} | {row['unit_lift_unit_lift_status']} | "
                f"{row['unit_lift_unit_lift_rigidity_score']} |"
            )

    lines.extend(
        [
            "",
            "## Artifact Demotions",
            "",
        ]
    )
    if not artifact_rows:
        lines.append("No artifacts were identified.")
    else:
        lines.extend(
            [
                "| rank | signature | ell | subgroup sizes | reasons |",
                "| ---: | --- | ---: | --- | --- |",
            ]
        )
        for index, row in enumerate(artifact_rows[:12], start=1):
            lines.append(
                f"| {index} | {row['signature']} | {row['ell']} | {row['geometry_subgroup_size_shape']} | "
                f"{row['artifact_artifact_reasons']} |"
            )

    lines.extend(
        [
            "",
            "## Multi-Prime Compatibility",
            "",
        ]
    )
    if not multi_prime_rows:
        lines.append("No non-artifact sparse signature repeated across multiple primes in this run.")
    else:
        lines.extend(
            [
                "| rank | signature | primes | density | rigidity | status |",
                "| ---: | --- | --- | ---: | ---: | --- |",
            ]
        )
        for index, row in enumerate(multi_prime_rows[:12], start=1):
            lines.append(
                f"| {index} | {row['signature']} | {row['primes']} | {row['combined_density']} | "
                f"{row['cross_prime_rigidity_score']} | {row['compatibility_status']} |"
            )

    lines.extend(
        [
            "",
            "## Sparse Lemma Explanations",
            "",
        ]
    )
    for row in sparse_explanations[:8]:
        lines.extend(
            [
                f"### {row['signature']} at ell={row['ell']}",
                "",
                f"Rank: {row['rank']}",
                "",
                row["modular_explanation"],
                "",
                f"Proof gap: {row['proof_gap']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Files",
            "",
            "- `unit_survivor_summary.csv`: joined sparse-row geometry, artifact, character, and unit-lift data.",
            "- `artifact_demotions.csv`: rows explained by subgroup-size or simple group artifacts.",
            "- `unexplained_sparse_rows.csv`: sparse rows not explained by first-pass artifact checks.",
            "- `padic_unit_lift_results.csv`: `ell^2`/`ell^3` unit-lift behavior.",
            "- `multi_prime_cluster_results.csv`: CRT-style combined-density compatibility records.",
            "- `exact_sparse_lemma_explanations.csv`: generated sparse-row explanations.",
            "",
        ]
    )
    return "\n".join(lines)


def _modular_shadow_report_markdown(
    *,
    output_dir: Path,
    target_count: int,
    artifact_count: int,
    proof_route_count: int,
    trace_rigid_count: int,
    newform_candidate_count: int,
    sage_available: bool,
    modular_rows: list[dict[str, object]],
    cross_prime_rows: list[dict[str, object]],
    template_rows: list[dict[str, object]],
) -> str:
    generated = datetime.now().isoformat(timespec="seconds")
    lines = [
        "# Modular-Shadow Routing Report",
        "",
        f"Generated: `{generated}`",
        f"Output directory: `{output_dir.as_posix()}`",
        "",
        "## Interpretation Guardrail",
        "",
        "This report ranks modular proof-route candidates. It does not claim a Beal proof or a local obstruction.",
        "",
        "Rows are promoted only when non-artifact sparse unit geometry has reasonable Frey-template support and trace behavior that separates from same-size structured controls.",
        "",
        "## Counts",
        "",
        f"- Target sparse rows routed: `{target_count}`.",
        f"- Artifact explained route rows: `{artifact_count}`.",
        f"- Proof-route candidate rows: `{proof_route_count}`.",
        f"- Trace-rigid candidate rows: `{trace_rigid_count}`.",
        f"- Newform-check candidate rows: `{newform_candidate_count}`.",
        f"- Sage available: `{sage_available}`.",
        "",
        "## Ranked Routes",
        "",
    ]
    if not modular_rows:
        lines.append("No target sparse rows were available for modular-shadow routing.")
    else:
        lines.extend(
            [
                "| rank | signature | ell | class | score | trace support | control support | rationale |",
                "| ---: | --- | ---: | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for index, row in enumerate(modular_rows[:16], start=1):
            lines.append(
                f"| {index} | {row['signature']} | {row['ell']} | {row['route_route_classification']} | "
                f"{row['route_route_rank_score']} | {row['trace_trace_support_size']} | "
                f"{row['trace_same_size_control_trace_support_size']} | {row['route_rationale']} |"
            )

    lines.extend(
        [
            "",
            "## Cross-Prime Trace Compatibility",
            "",
        ]
    )
    if not cross_prime_rows:
        lines.append("No canonical target signature appeared across multiple routed primes.")
    else:
        lines.extend(
            [
                "| rank | canonical signature | primes | class | rigidity | explanation |",
                "| ---: | --- | --- | --- | ---: | --- |",
            ]
        )
        for index, row in enumerate(cross_prime_rows[:12], start=1):
            lines.append(
                f"| {index} | {row['canonical_signature_id']} | {row['primes']} | "
                f"{row['trace_compatibility_class']} | {row['combined_trace_rigidity_score']} | "
                f"{row['explanation']} |"
            )

    lines.extend(
        [
            "",
            "## Frey Template Notes",
            "",
        ]
    )
    for row in template_rows[:8]:
        lines.extend(
            [
                f"### {row['signature']}",
                "",
                f"Template: `{row['equation']}`",
                "",
                f"Confidence: `{row['template_confidence']}`",
                "",
                f"Uncertainty flags: `{row['uncertainty_flags']}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Files",
            "",
            "- `modular_shadow_summary.csv`: joined route, classifier, and trace data.",
            "- `frey_template_candidates.csv`: symbolic Frey-template records.",
            "- `trace_probe_results.csv`: finite-field trace distributions for target sparse rows.",
            "- `cross_prime_trace_results.csv`: canonical signature trace compatibility.",
            "- `newform_probe_results.csv`: Sage availability and newform-check instructions.",
            "",
            "## Next Work",
            "",
            "Only rows that survive artifact checks and show trace rigidity should be promoted toward proof-route status. Repeated non-artifact rows without trace rigidity may be logged as newform-check sketches, not obstruction claims.",
            "",
        ]
    )
    return "\n".join(lines)


def run_experiment(
    *,
    output_root: Path = Path("runs"),
    exponents: tuple[int, ...] = DEFAULT_EXPONENTS,
    prime_limit: int = 43,
    primes: tuple[int, ...] | None = None,
    compute_lift: bool = True,
    control_samples: int = 24,
    seed: int = 20260620,
    timestamp: str | None = None,
) -> Path:
    """Run an RSG experiment and write structured outputs."""
    prime_values = primes if primes is not None else primes_up_to(prime_limit, odd_only=True)
    run_id = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = output_root / run_id
    output_dir.mkdir(parents=True, exist_ok=False)

    results = run_sweep(
        exponents=exponents,
        primes=prime_values,
        prime_limit=prime_limit,
        compute_lift=compute_lift,
        control_samples=control_samples,
        seed=seed,
    )
    valuations = analyze_results(results)
    shadows, clusters = build_shadow_records(results, valuations)
    zero_records = analyze_zero_support_results(results)
    classifications = classify_primitive_obstructions(results, zero_records)
    padic_audits = audit_padic_lifts(classifications)
    explanations = generate_explanations(results, zero_records, classifications, padic_audits)
    unit_geometries = analyze_sparse_unit_geometries(results, classifications)
    artifact_assessments = explain_artifacts(unit_geometries)
    character_fingerprints = compute_character_fingerprints(unit_geometries)
    padic_unit_lifts = analyze_padic_unit_lifts(unit_geometries)
    multi_prime_records = analyze_multi_prime_compatibility(unit_geometries, artifact_assessments)
    sparse_lemma_explanations = generate_sparse_lemma_explanations(
        unit_geometries,
        artifact_assessments,
        character_fingerprints,
        padic_unit_lifts,
    )
    target_geometries = _target_geometries(unit_geometries)
    target_keys = {(geometry.signature, geometry.ell) for geometry in target_geometries}
    target_artifacts = [item for item in artifact_assessments if (item.signature, item.ell) in target_keys]
    target_templates = build_template_records([geometry.signature for geometry in target_geometries])
    target_traces = trace_probes_for_geometries(target_geometries)
    modular_routes = build_modular_shadow_routes(
        target_geometries,
        target_artifacts,
        target_templates,
        target_traces,
    )
    cross_prime_traces = analyze_cross_prime_traces(target_traces, target_artifacts)
    modular_route_classifications = classify_modular_routes(
        modular_routes,
        target_artifacts,
        target_traces,
        target_templates,
        cross_prime_traces,
    )
    newform_probe_records = run_optional_newform_probe(modular_routes)
    calibration_artifacts = build_known_case_calibration(
        output_dir=output_dir,
        primes=prime_values,
        exponents=exponents,
        compute_lift=compute_lift,
        control_samples=control_samples,
        seed=seed,
    )

    summary_rows = _merged_summary_rows(results, valuations, shadows)
    interesting_rows = _interesting_rows(shadows)
    cluster_rows = [cluster.to_flat_dict() for cluster in clusters]
    zero_summary_rows = _zero_support_summary_rows(results, zero_records, classifications)
    explanation_rows = [explanation.to_flat_dict() for explanation in explanations]
    direct_rows = _classification_rows(
        classifications,
        zero_records,
        explanations,
        classification_name="direct_primitive_obstruction",
    )
    mandatory_candidate_rows = _mandatory_rows(classifications, zero_records, padic_audits, explanations)
    sparse_cluster_rows = [cluster.to_flat_dict() for cluster in sparse_unit_clusters(classifications)]
    unit_summary_rows = _unit_geometry_summary_rows(
        unit_geometries,
        artifact_assessments,
        character_fingerprints,
        padic_unit_lifts,
    )
    artifact_demotion_rows = _artifact_rows(unit_summary_rows)
    unexplained_rows = _unexplained_sparse_rows(unit_summary_rows)
    padic_unit_lift_rows = [record.to_flat_dict() for record in padic_unit_lifts]
    multi_prime_rows = [record.to_flat_dict() for record in multi_prime_records]
    sparse_lemma_rows = [explanation.to_flat_dict() for explanation in sparse_lemma_explanations]
    modular_summary_rows = _modular_shadow_summary_rows(
        modular_routes,
        modular_route_classifications,
        target_traces,
    )
    frey_template_rows = [record.to_flat_dict() for record in target_templates]
    trace_probe_rows = [record.to_flat_dict() for record in target_traces]
    cross_prime_trace_rows = [record.to_flat_dict() for record in cross_prime_traces]
    newform_probe_rows = [record.to_flat_dict() for record in newform_probe_records]
    known_case_rows = [record.to_flat_dict() for record in calibration_artifacts.case_records]
    route_confusion_rows = [record.to_flat_dict() for record in calibration_artifacts.route_matrix_records]
    theorem_terrain_rows = calibration_artifacts.terrain_summary_rows
    remaining_true_mismatch_rows = calibration_artifacts.remaining_true_mismatch_rows
    family_expansion_rows = [record.to_flat_dict() for record in calibration_artifacts.family_expansion_records]
    route_prior_rows = [record.to_flat_dict() for record in calibration_artifacts.route_prior_scores]
    sage_export_rows = [record.to_flat_dict() for record in calibration_artifacts.sage_export_records]

    _write_csv(output_dir / "summary.csv", summary_rows)
    _write_csv(output_dir / "interesting_cases.csv", interesting_rows)
    _write_csv(output_dir / "clusters.csv", cluster_rows)
    _write_csv(output_dir / "zero_support_summary.csv", zero_summary_rows)
    _write_csv(output_dir / "direct_obstructions.csv", direct_rows)
    _write_csv(output_dir / "mandatory_single_divisor_candidates.csv", mandatory_candidate_rows)
    _write_csv(output_dir / "sparse_unit_clusters.csv", sparse_cluster_rows)
    _write_csv(output_dir / "exact_explanations.csv", explanation_rows)
    _write_csv(output_dir / "unit_survivor_summary.csv", unit_summary_rows)
    _write_csv(output_dir / "artifact_demotions.csv", artifact_demotion_rows)
    _write_csv(output_dir / "unexplained_sparse_rows.csv", unexplained_rows)
    _write_csv(output_dir / "padic_unit_lift_results.csv", padic_unit_lift_rows)
    _write_csv(output_dir / "multi_prime_cluster_results.csv", multi_prime_rows)
    _write_csv(output_dir / "exact_sparse_lemma_explanations.csv", sparse_lemma_rows)
    _write_csv(output_dir / "modular_shadow_summary.csv", modular_summary_rows)
    _write_csv(output_dir / "frey_template_candidates.csv", frey_template_rows)
    _write_csv(output_dir / "trace_probe_results.csv", trace_probe_rows)
    _write_csv(output_dir / "cross_prime_trace_results.csv", cross_prime_trace_rows)
    _write_csv(output_dir / "newform_probe_results.csv", newform_probe_rows)
    _write_csv(output_dir / "known_case_calibration_summary.csv", known_case_rows)
    _write_csv(output_dir / "route_confusion_matrix.csv", route_confusion_rows)
    _write_csv(output_dir / "theorem_terrain_summary.csv", theorem_terrain_rows)
    _write_csv(output_dir / "known_case_route_matrix.csv", route_confusion_rows)
    _write_csv(output_dir / "remaining_true_mismatches.csv", remaining_true_mismatch_rows)
    _write_csv(output_dir / "family_expansion_results.csv", family_expansion_rows)
    _write_csv(output_dir / "route_prior_scores.csv", route_prior_rows)
    _write_csv(output_dir / "sage_export_manifest.csv", sage_export_rows)

    promoted_count = sum(1 for shadow in shadows if shadow.promotion_status == "promoted_candidate")
    classification_counts: dict[str, int] = {}
    for classification in classifications:
        classification_counts[classification.classification] = classification_counts.get(classification.classification, 0) + 1
    metadata = {
        "run_id": run_id,
        "exponents": exponents,
        "primes": prime_values,
        "compute_lift": compute_lift,
        "control_samples": control_samples,
        "seed": seed,
        "result_count": len(results),
        "interesting_count": len(interesting_rows),
        "promoted_count": promoted_count,
        "zero_support_classification_counts": classification_counts,
        "direct_obstruction_count": len(direct_rows),
        "mandatory_single_divisor_count": len(mandatory_candidate_rows),
        "sparse_unit_cluster_count": len(sparse_cluster_rows),
        "unit_geometry_sparse_count": len(unit_geometries),
        "unit_geometry_artifact_demotions": len(artifact_demotion_rows),
        "unit_geometry_unexplained_sparse_rows": len(unexplained_rows),
        "unit_geometry_rigid_or_collapsed_lifts": sum(1 for row in padic_unit_lift_rows if row["collapse_or_rigid"]),
        "unit_geometry_multi_prime_records": len(multi_prime_rows),
        "modular_shadow_target_rows": len(modular_summary_rows),
        "modular_shadow_artifact_routes": sum(1 for row in modular_summary_rows if row["artifact_verdict"] == "artifact_explained"),
        "modular_shadow_proof_route_candidates": sum(1 for row in modular_summary_rows if row["route_promotion_status"] == "proof-route candidate"),
        "modular_shadow_trace_rigid_candidates": sum(1 for row in modular_summary_rows if row["route_route_classification"] == "trace_rigid_candidate"),
        "modular_shadow_newform_candidates": sum(1 for row in modular_summary_rows if row["route_route_classification"] == "newform_check_candidate"),
        "sage_available": any(row["sage_available"] for row in newform_probe_rows),
        "known_case_calibration_count": len(known_case_rows),
        "known_case_mismatch_count": sum(1 for row in known_case_rows if row["actual_route_label"] == "known_case_mismatch"),
        "known_case_theorem_terrain_route_count": sum(1 for row in known_case_rows if row["actual_route_label"] == "theorem_terrain_route"),
        "known_case_artifact_like_count": sum(1 for row in known_case_rows if row["actual_route_label"] == "artifact_like"),
        "known_case_external_sage_count": sum(1 for row in known_case_rows if row["actual_route_label"] == "needs_external_sage_check"),
        "known_case_calibrated_route_count": sum(1 for row in known_case_rows if row["actual_route_label"] == "calibrated_route_candidate"),
        "remaining_true_mismatch_count": len(remaining_true_mismatch_rows),
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    report = _report_markdown(
        output_dir=output_dir,
        result_count=len(results),
        interesting_count=len(interesting_rows),
        promoted_count=promoted_count,
        prime_values=prime_values,
        control_samples=control_samples,
        compute_lift=compute_lift,
        top_cases=interesting_rows,
    )
    (output_dir / "README_REPORT.md").write_text(report, encoding="utf-8")
    zero_report = _zero_support_report_markdown(
        output_dir=output_dir,
        result_count=len(results),
        classification_counts=classification_counts,
        direct_rows=direct_rows,
        mandatory_rows=mandatory_candidate_rows,
        sparse_clusters=sparse_cluster_rows,
        explanation_rows=explanation_rows,
    )
    (output_dir / "README_ZERO_SUPPORT_REPORT.md").write_text(zero_report, encoding="utf-8")
    unit_report = _unit_geometry_report_markdown(
        output_dir=output_dir,
        sparse_count=len(unit_geometries),
        artifact_count=len(artifact_demotion_rows),
        unexplained_count=len(unexplained_rows),
        rigid_lift_count=sum(1 for row in padic_unit_lift_rows if row["collapse_or_rigid"]),
        multi_prime_count=len(multi_prime_rows),
        unit_rows=unit_summary_rows,
        unexplained_rows=unexplained_rows,
        artifact_rows=artifact_demotion_rows,
        multi_prime_rows=multi_prime_rows,
        sparse_explanations=sparse_lemma_rows,
    )
    (output_dir / "README_UNIT_GEOMETRY_REPORT.md").write_text(unit_report, encoding="utf-8")
    modular_report = _modular_shadow_report_markdown(
        output_dir=output_dir,
        target_count=len(modular_summary_rows),
        artifact_count=sum(1 for row in modular_summary_rows if row["artifact_verdict"] == "artifact_explained"),
        proof_route_count=sum(1 for row in modular_summary_rows if row["route_promotion_status"] == "proof-route candidate"),
        trace_rigid_count=sum(1 for row in modular_summary_rows if row["route_route_classification"] == "trace_rigid_candidate"),
        newform_candidate_count=sum(1 for row in modular_summary_rows if row["route_route_classification"] == "newform_check_candidate"),
        sage_available=any(row["sage_available"] for row in newform_probe_rows),
        modular_rows=modular_summary_rows,
        cross_prime_rows=cross_prime_trace_rows,
        template_rows=frey_template_rows,
    )
    (output_dir / "README_MODULAR_SHADOW_REPORT.md").write_text(modular_report, encoding="utf-8")
    (output_dir / "README_KNOWN_CASE_CALIBRATION_REPORT.md").write_text(
        calibration_artifacts.report_markdown,
        encoding="utf-8",
    )
    (output_dir / "README_THEOREM_TERRAIN_REPORT.md").write_text(
        calibration_artifacts.terrain_report_markdown,
        encoding="utf-8",
    )
    return output_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Beal RSG discovery sweep.")
    parser.add_argument("--output-root", default="runs", help="Directory that will receive timestamped run folders.")
    parser.add_argument("--prime-limit", type=int, default=43, help="Use odd primes up to this limit when --primes is absent.")
    parser.add_argument("--primes", help="Comma-separated prime list, for example 5,7,11.")
    parser.add_argument("--exponents", default=",".join(str(value) for value in DEFAULT_EXPONENTS))
    parser.add_argument("--control-samples", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--timestamp", help="Optional deterministic run folder name.")
    parser.add_argument("--no-lift", action="store_true", help="Skip ell^2 lift survival for faster smoke runs.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    exponents = tuple(int(part.strip()) for part in args.exponents.split(",") if part.strip())
    if not exponents:
        parser.error("--exponents cannot be empty")
    primes = parse_prime_list(args.primes) if args.primes else None
    output_dir = run_experiment(
        output_root=Path(args.output_root),
        exponents=exponents,
        prime_limit=args.prime_limit,
        primes=primes,
        compute_lift=not args.no_lift,
        control_samples=args.control_samples,
        seed=args.seed,
        timestamp=args.timestamp,
    )
    print(output_dir.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
