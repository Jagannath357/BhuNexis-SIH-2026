"""
evidence package - Spatial geometry, bounding-box math, and provenance evidence linking.
"""

from .bbox_utils import (
    validate_bbox,
    normalize_bbox,
    denormalize_bbox,
    merge_bboxes,
    bbox_center,
    compute_iou,
    are_horizontally_aligned,
    are_vertically_aligned,
    calculate_spatial_proximity_score,
)
from .evidence_linker import EvidenceLinker

__all__ = [
    "validate_bbox",
    "normalize_bbox",
    "denormalize_bbox",
    "merge_bboxes",
    "bbox_center",
    "compute_iou",
    "are_horizontally_aligned",
    "are_vertically_aligned",
    "calculate_spatial_proximity_score",
    "EvidenceLinker",
]
