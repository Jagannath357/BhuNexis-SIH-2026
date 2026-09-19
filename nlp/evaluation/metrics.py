"""
evaluation/metrics.py - Evaluation Metrics for Land Record Document Understanding.

Computes:
1. Field-level precision, recall, F1, exact match accuracy, and Character Error Rate (CER).
2. Tier-specific performance (Tier 1 vs Tier 2 vs Tier 3).
3. Land Record Safety Metrics:
   - False Acceptance Rate (FAR): % of corrupted/ambiguous records auto-approved without review (MUST be 0.0% for Tier 1).
   - False Rejection Rate (FRR): % of pristine records routed unnecessarily to human review.
   - Rule 5 Guardrail Compliance: 100% required.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
try:
    from ..schemas.field_result import FieldTier
except (ImportError, ValueError):
    from schemas.field_result import FieldTier


def levenshtein_distance(s1: str, s2: str) -> int:
    """Computes Levenshtein edit distance between two strings."""
    if s1 == s2:
        return 0
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    v0 = list(range(len(s2) + 1))
    v1 = [0] * (len(s2) + 1)

    for i in range(len(s1)):
        v1[0] = i + 1
        for j in range(len(s2)):
            cost = 0 if s1[i] == s2[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        v0, v1 = v1, v0

    return v0[len(s2)]


def character_error_rate(reference: str, hypothesis: str) -> float:
    """Calculates Character Error Rate (CER) = Levenshtein Distance / max(len(ref), 1)."""
    if not reference and not hypothesis:
        return 0.0
    ref_len = max(len(reference), 1)
    dist = levenshtein_distance(reference, hypothesis)
    return min(1.0, dist / ref_len)


@dataclass
class FieldMetric:
    """Evaluates extraction performance for a specific canonical field."""
    field_name: str
    tier: FieldTier
    true_positives: int = 0
    false_positives: int = 0
    false_negatives: int = 0
    exact_matches: int = 0
    total_evaluated: int = 0
    total_char_distance: int = 0
    total_ref_chars: int = 0

    @property
    def precision(self) -> float:
        total = self.true_positives + self.false_positives
        return round(self.true_positives / total, 4) if total > 0 else 1.0

    @property
    def recall(self) -> float:
        total = self.true_positives + self.false_negatives
        return round(self.true_positives / total, 4) if total > 0 else 1.0

    @property
    def f1_score(self) -> float:
        p = self.precision
        r = self.recall
        return round(2 * (p * r) / (p + r), 4) if (p + r) > 0 else 0.0

    @property
    def exact_match_accuracy(self) -> float:
        return round(self.exact_matches / self.total_evaluated, 4) if self.total_evaluated > 0 else 1.0

    @property
    def cer(self) -> float:
        return round(self.total_char_distance / max(self.total_ref_chars, 1), 4) if self.total_ref_chars > 0 else 0.0

    def record_match(self, ground_truth: Optional[str], predicted: Optional[str]) -> None:
        """Updates metric tally for one document sample."""
        self.total_evaluated += 1

        gt_clean = (ground_truth or "").strip()
        pred_clean = (predicted or "").strip()

        if gt_clean and pred_clean:
            self.total_ref_chars += len(gt_clean)
            dist = levenshtein_distance(gt_clean, pred_clean)
            self.total_char_distance += dist

            if gt_clean.lower() == pred_clean.lower():
                self.true_positives += 1
                self.exact_matches += 1
            else:
                # Close match counts as partial or false positive depending on threshold
                if dist <= 2:
                    self.true_positives += 1
                else:
                    self.false_positives += 1
        elif gt_clean and not pred_clean:
            self.false_negatives += 1
            self.total_ref_chars += len(gt_clean)
            self.total_char_distance += len(gt_clean)
        elif not gt_clean and pred_clean:
            self.false_positives += 1
        else:
            # Neither present, accurate non-extraction
            self.exact_matches += 1


@dataclass
class SafetyMetrics:
    """
    Measures ambiguity firewall effectiveness and adherence to Rule 5.
    
    FAR (False Acceptance Rate): Proportion of ambiguous or corrupt documents 
    erroneously passed without requiring officer review.
    FRR (False Rejection Rate): Proportion of clean documents needlessly routed to review.
    """
    clean_docs_total: int = 0
    clean_docs_routed_to_review: int = 0
    corrupted_docs_total: int = 0
    corrupted_docs_auto_approved: int = 0
    rule_5_violations: int = 0

    @property
    def false_acceptance_rate(self) -> float:
        """FAR should be 0.00% for legal safety."""
        if self.corrupted_docs_total == 0:
            return 0.0
        return round(self.corrupted_docs_auto_approved / self.corrupted_docs_total, 4)

    @property
    def false_rejection_rate(self) -> float:
        """FRR measures efficiency/workload for human officers."""
        if self.clean_docs_total == 0:
            return 0.0
        return round(self.clean_docs_routed_to_review / self.clean_docs_total, 4)

    @property
    def is_rule_5_compliant(self) -> bool:
        return self.rule_5_violations == 0


@dataclass
class EvaluationReport:
    """Comprehensive benchmark evaluation report."""
    total_documents: int
    field_metrics: Dict[str, FieldMetric] = field(default_factory=dict)
    safety_metrics: SafetyMetrics = field(default_factory=SafetyMetrics)
    mean_latency_ms: float = 0.0

    def get_tier_summary(self) -> Dict[str, Dict[str, float]]:
        """Aggregates metrics across Tiers."""
        tier_data: Dict[str, Dict[str, Any]] = {
            FieldTier.TIER_1_IMMUTABLE.value: {"p": [], "r": [], "f1": [], "cer": [], "em": []},
            FieldTier.TIER_2_SAFE_NORMALIZABLE.value: {"p": [], "r": [], "f1": [], "cer": [], "em": []},
            FieldTier.TIER_3_ENTITY_LINGUISTIC.value: {"p": [], "r": [], "f1": [], "cer": [], "em": []},
        }

        for m in self.field_metrics.values():
            t = m.tier.value
            if t in tier_data:
                tier_data[t]["p"].append(m.precision)
                tier_data[t]["r"].append(m.recall)
                tier_data[t]["f1"].append(m.f1_score)
                tier_data[t]["cer"].append(m.cer)
                tier_data[t]["em"].append(m.exact_match_accuracy)

        summary = {}
        for t, metrics in tier_data.items():
            count = len(metrics["p"])
            if count > 0:
                summary[t] = {
                    "mean_precision": round(sum(metrics["p"]) / count, 4),
                    "mean_recall": round(sum(metrics["r"]) / count, 4),
                    "mean_f1": round(sum(metrics["f1"]) / count, 4),
                    "mean_cer": round(sum(metrics["cer"]) / count, 4),
                    "mean_exact_match": round(sum(metrics["em"]) / count, 4),
                }
        return summary

    def to_dict(self) -> Dict[str, Any]:
        """Serializes report to structured dictionary."""
        return {
            "total_documents": self.total_documents,
            "mean_latency_ms": round(self.mean_latency_ms, 2),
            "safety_metrics": {
                "false_acceptance_rate": self.safety_metrics.false_acceptance_rate,
                "false_rejection_rate": self.safety_metrics.false_rejection_rate,
                "rule_5_compliant": self.safety_metrics.is_rule_5_compliant,
                "rule_5_violations": self.safety_metrics.rule_5_violations,
            },
            "tier_summary": self.get_tier_summary(),
            "field_details": {
                name: {
                    "tier": m.tier.value,
                    "precision": m.precision,
                    "recall": m.recall,
                    "f1_score": m.f1_score,
                    "exact_match_accuracy": m.exact_match_accuracy,
                    "cer": m.cer,
                    "evaluated_samples": m.total_evaluated,
                }
                for name, m in self.field_metrics.items()
            }
        }

    def to_markdown(self) -> str:
        """Generates audit-ready Markdown table report."""
        lines = [
            "# BhuNexis NLP Document Understanding - Benchmark Report",
            "",
            f"- **Evaluated Documents:** {self.total_documents}",
            f"- **Mean Processing Latency:** {self.mean_latency_ms:.2f} ms / document",
            f"- **False Acceptance Rate (FAR):** {self.safety_metrics.false_acceptance_rate * 100:.2f}% (Target: 0.0%)",
            f"- **False Rejection Rate (FRR):** {self.safety_metrics.false_rejection_rate * 100:.2f}%",
            f"- **Rule 5 Compliance:** {'PASS (100%)' if self.safety_metrics.is_rule_5_compliant else 'FAIL (VIOLATION)'}",
            "",
            "## Field-Level Accuracy & Extraction Performance",
            "| Field Name | Risk Tier | Precision | Recall | F1 Score | Exact Match | CER |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        ]

        for name, m in sorted(self.field_metrics.items()):
            lines.append(
                f"| `{name}` | {m.tier.name} | {m.precision:.2%} | {m.recall:.2%} | {m.f1_score:.2%} | {m.exact_match_accuracy:.2%} | {m.cer:.3f} |"
            )

        lines.extend([
            "",
            "## Tier Summary",
            "| Tier | Mean Precision | Mean Recall | Mean F1 | Mean Exact Match | Mean CER |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |"
        ])

        for tier, vals in self.get_tier_summary().items():
            lines.append(
                f"| **{tier}** | {vals['mean_precision']:.2%} | {vals['mean_recall']:.2%} | {vals['mean_f1']:.2%} | {vals['mean_exact_match']:.2%} | {vals['mean_cer']:.3f} |"
            )

        return "\n".join(lines)
