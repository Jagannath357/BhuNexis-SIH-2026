"""
evidence/bbox_utils.py - Spatial Geometry & Bounding Box Math.

Provides coordinate normalization, multi-box union, spatial proximity scoring,
and geometric alignment functions for LayoutLMv3 and Officer UI highlighting.
"""

from typing import List, Tuple, Optional
import math


def validate_bbox(bbox: List[float]) -> List[float]:
    """Validates and returns bbox as float list [x1, y1, x2, y2]."""
    if len(bbox) != 4:
        raise ValueError(f"Bounding box must have 4 coordinates [x1, y1, x2, y2], got {len(bbox)}")
    x1, y1, x2, y2 = [float(c) for c in bbox]
    if x1 > x2:
        raise ValueError(f"Invalid bounding box: x1 ({x1}) > x2 ({x2})")
    if y1 > y2:
        raise ValueError(f"Invalid bounding box: y1 ({y1}) > y2 ({y2})")
    return [x1, y1, x2, y2]


def normalize_bbox(bbox: List[float], image_width: float, image_height: float, target_scale: float = 1000.0) -> List[int]:
    """
    Normalizes pixel coordinates to standard 0-1000 integer scale (required by LayoutLMv3).
    Clamps values within [0, target_scale].
    """
    if image_width <= 0 or image_height <= 0:
        raise ValueError(f"Image dimensions must be positive, got width={image_width}, height={image_height}")
    
    x1, y1, x2, y2 = validate_bbox(bbox)
    norm_x1 = int(round(max(0.0, min(target_scale, (x1 / image_width) * target_scale))))
    norm_y1 = int(round(max(0.0, min(target_scale, (y1 / image_height) * target_scale))))
    norm_x2 = int(round(max(0.0, min(target_scale, (x2 / image_width) * target_scale))))
    norm_y2 = int(round(max(0.0, min(target_scale, (y2 / image_height) * target_scale))))
    
    # Ensure min width/height of 1
    norm_x2 = max(norm_x1 + 1, norm_x2)
    norm_y2 = max(norm_y1 + 1, norm_y2)
    return [norm_x1, norm_y1, min(int(target_scale), norm_x2), min(int(target_scale), norm_y2)]


def denormalize_bbox(norm_bbox: List[int], image_width: float, image_height: float, scale: float = 1000.0) -> List[float]:
    """Converts 0-1000 normalized coordinates back to actual image pixel coordinates."""
    nx1, ny1, nx2, ny2 = norm_bbox
    x1 = (nx1 / scale) * image_width
    y1 = (ny1 / scale) * image_height
    x2 = (nx2 / scale) * image_width
    y2 = (ny2 / scale) * image_height
    return [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)]


def merge_bboxes(bboxes: List[List[float]]) -> List[float]:
    """
    Computes the tight bounding box union enclosing a list of bounding boxes.
    Used to merge multiple token boxes into a single entity box.
    """
    if not bboxes:
        raise ValueError("Cannot merge an empty list of bounding boxes")
    
    validated = [validate_bbox(b) for b in bboxes]
    min_x = min(b[0] for b in validated)
    min_y = min(b[1] for b in validated)
    max_x = max(b[2] for b in validated)
    max_y = max(b[3] for b in validated)
    return [min_x, min_y, max_x, max_y]


def bbox_center(bbox: List[float]) -> Tuple[float, float]:
    """Calculates center point (cx, cy) of a bounding box."""
    x1, y1, x2, y2 = validate_bbox(bbox)
    return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)


def compute_iou(bbox1: List[float], bbox2: List[float]) -> float:
    """Computes Intersection over Union (IoU) between two bounding boxes."""
    b1 = validate_bbox(bbox1)
    b2 = validate_bbox(bbox2)

    inter_x1 = max(b1[0], b2[0])
    inter_y1 = max(b1[1], b2[1])
    inter_x2 = min(b1[2], b2[2])
    inter_y2 = min(b1[3], b2[3])

    if inter_x2 <= inter_x1 or inter_y2 <= inter_y1:
        return 0.0

    inter_area = (inter_x2 - inter_x1) * (inter_y2 - inter_y1)
    b1_area = (b1[2] - b1[0]) * (b1[3] - b1[1])
    b2_area = (b2[2] - b2[0]) * (b2[3] - b2[1])
    union_area = b1_area + b2_area - inter_area

    if union_area <= 0:
        return 0.0
    return inter_area / union_area


def are_horizontally_aligned(bbox_label: List[float], bbox_val: List[float], y_tolerance: float = 30.0) -> bool:
    """
    Checks if bbox_val sits horizontally to the right of bbox_label on approximately the same line.
    Common pattern in land records: [Label: "Plot No:"] [Value: "382/1"]
    """
    l = validate_bbox(bbox_label)
    v = validate_bbox(bbox_val)

    # Label should be to the left of or adjacent to value
    if v[0] < l[0]:
        return False

    # Check vertical overlap or vertical center distance
    l_center_y = (l[1] + l[3]) / 2.0
    v_center_y = (v[1] + v[3]) / 2.0

    return abs(l_center_y - v_center_y) <= y_tolerance


def are_vertically_aligned(bbox_header: List[float], bbox_cell: List[float], x_tolerance: float = 60.0) -> bool:
    """
    Checks if bbox_cell is situated underneath bbox_header in a tabular column structure.
    """
    h = validate_bbox(bbox_header)
    c = validate_bbox(bbox_cell)

    # Cell must be below header
    if c[1] < h[1]:
        return False

    # Check horizontal center alignment
    h_center_x = (h[0] + h[2]) / 2.0
    c_center_x = (c[0] + c[2]) / 2.0

    return abs(h_center_x - c_center_x) <= x_tolerance


def calculate_spatial_proximity_score(
    bbox_label: Optional[List[float]], 
    bbox_value: List[float],
    max_expected_distance: float = 500.0
) -> float:
    """
    Computes Pillar 4 Spatial Proximity Score (0.0 to 1.0).
    - If label and value are horizontally aligned and adjacent: score close to 1.0.
    - If value is distant or misaligned: score drops.
    - If no label bbox provided: defaults to 0.70 (neutral baseline).
    """
    if bbox_label is None:
        return 0.70

    l = validate_bbox(bbox_label)
    v = validate_bbox(bbox_value)

    # Euclidean distance between centers
    lc = bbox_center(l)
    vc = bbox_center(v)
    dist = math.sqrt((lc[0] - vc[0]) ** 2 + (lc[1] - vc[1]) ** 2)

    # Check alignment bonus
    is_aligned = are_horizontally_aligned(l, v) or are_vertically_aligned(l, v)
    base_score = max(0.0, 1.0 - (dist / max_expected_distance))

    if is_aligned:
        return min(1.0, base_score + 0.25)
    return round(max(0.1, base_score * 0.7), 2)
