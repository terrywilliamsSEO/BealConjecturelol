"""Cross-prime trace compatibility for modular-shadow routes."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass

from .artifact_explainer import ArtifactAssessment
from .finite_field_trace_probe import TraceProbeRecord
from .signature_normalizer import normalize_signature


@dataclass(frozen=True)
class CrossPrimeTraceRecord:
    """Trace fingerprint compatibility across primes for one canonical signature."""

    canonical_signature_id: str
    signatures: tuple[str, ...]
    primes: tuple[int, ...]
    prime_count: int
    trace_fingerprints: tuple[str, ...]
    artifact_count: int
    unusually_narrow_count: int
    average_trace_support_size: float
    average_control_support_size: float
    combined_trace_rigidity_score: float
    trace_compatibility_class: str
    explanation: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signatures"] = ";".join(self.signatures)
        data["primes"] = ";".join(str(prime) for prime in self.primes)
        data["trace_fingerprints"] = " || ".join(self.trace_fingerprints)
        return data


def analyze_cross_prime_traces(
    traces: list[TraceProbeRecord],
    artifacts: list[ArtifactAssessment],
) -> list[CrossPrimeTraceRecord]:
    """Combine trace fingerprints across primes by canonical signature."""
    artifact_by_key = {(item.signature, item.ell): item for item in artifacts}
    grouped: dict[str, list[TraceProbeRecord]] = defaultdict(list)
    for trace in traces:
        canonical_id = normalize_signature(trace.signature).canonical_signature_id
        grouped[canonical_id].append(trace)

    records: list[CrossPrimeTraceRecord] = []
    for canonical_id, rows in grouped.items():
        artifact_count = sum(
            1
            for row in rows
            if artifact_by_key[(row.signature, row.ell)].verdict == "artifact_explained"
        )
        active_rows = [
            row
            for row in rows
            if artifact_by_key[(row.signature, row.ell)].verdict != "artifact_explained"
        ] or rows
        signatures = tuple(sorted({"-".join(str(part) for part in row.signature) for row in active_rows}))
        primes = tuple(sorted({row.ell for row in active_rows}))
        narrow_count = sum(1 for row in active_rows if row.unusually_narrow_trace)
        avg_support = sum(row.trace_support_size for row in active_rows) / len(active_rows)
        avg_control = sum(row.same_size_control_trace_support_size for row in active_rows) / len(active_rows)
        rigidity = sum(row.trace_rigidity_score for row in active_rows)

        if artifact_count == len(rows):
            klass = "trace_artifact"
            explanation = "all trace rows are explained by subgroup artifacts"
        elif narrow_count >= 2 and len(primes) >= 2:
            klass = "trace_rigid"
            explanation = "trace distributions are repeatedly narrower than same-size subgroup controls"
        elif len(primes) >= 2 and artifact_count < len(rows):
            klass = "needs_newform_check"
            explanation = "non-artifact trace fingerprints repeat across primes but are not trace-rigid"
        else:
            klass = "trace_control_like"
            explanation = "trace data does not separate from structured controls"

        records.append(
            CrossPrimeTraceRecord(
                canonical_signature_id=canonical_id,
                signatures=signatures,
                primes=primes,
                prime_count=len(primes),
                trace_fingerprints=tuple(row.trace_fingerprint for row in active_rows),
                artifact_count=artifact_count,
                unusually_narrow_count=narrow_count,
                average_trace_support_size=round(avg_support, 10),
                average_control_support_size=round(avg_control, 10),
                combined_trace_rigidity_score=round(rigidity, 10),
                trace_compatibility_class=klass,
                explanation=explanation,
            )
        )
    records.sort(
        key=lambda item: (
            item.trace_compatibility_class == "trace_rigid",
            item.trace_compatibility_class == "needs_newform_check",
            item.combined_trace_rigidity_score,
        ),
        reverse=True,
    )
    return records
