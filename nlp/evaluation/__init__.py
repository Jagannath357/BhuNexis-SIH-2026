"""
evaluation - Area 10 & Phase 7 Evaluation Suite & Benchmark Metrics.
"""

from .metrics import (
    levenshtein_distance,
    character_error_rate,
    FieldMetric,
    SafetyMetrics,
    EvaluationReport,
)
from .benchmark import (
    CANONICAL_FIELD_TIERS,
    GroundTruthRecord,
    BenchmarkRunner,
)

__all__ = [
    "levenshtein_distance",
    "character_error_rate",
    "FieldMetric",
    "SafetyMetrics",
    "EvaluationReport",
    "CANONICAL_FIELD_TIERS",
    "GroundTruthRecord",
    "BenchmarkRunner",
]
