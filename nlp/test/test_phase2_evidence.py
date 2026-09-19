"""
test/test_phase2_evidence.py - Unit tests for Phase 2 (Evidence & Bounding Box Math).

Validates:
1. Coordinate normalization (0-1000 scale for LayoutLM) and denormalization.
2. Bounding box merging (multi-word entity unions).
3. IoU calculations and spatial alignment checks (horizontal & vertical).
4. Spatial proximity scoring (Pillar 4 confidence signal).
5. EvidenceLinker provenance binding on synthetic and real fixture OCR blocks.
"""

import sys
import json
from pathlib import Path
import pytest

NLP_ROOT = Path(__file__).resolve().parent.parent
if str(NLP_ROOT) not in sys.path:
    sys.path.insert(0, str(NLP_ROOT))

from schemas.ocr_contract import OCRBlock, OCRDocument
from schemas.field_result import EvidenceSnippet
from evidence.bbox_utils import (
    validate_bbox,
    normalize_bbox,
    denormalize_bbox,
    merge_bboxes,
    compute_iou,
    are_horizontally_aligned,
    are_vertically_aligned,
    calculate_spatial_proximity_score,
)
from evidence.evidence_linker import EvidenceLinker

FIXTURES_DIR = NLP_ROOT / "fixtures"


class TestBBoxGeometry:
    """Tests spatial math and coordinate utilities."""

    def test_normalize_and_denormalize_coordinates(self):
        img_w, img_h = 2000.0, 3000.0
        # Box covering 25% of image
        pixel_bbox = [500.0, 750.0, 1000.0, 1500.0]

        norm_box = normalize_bbox(pixel_bbox, img_w, img_h, target_scale=1000.0)
        assert norm_box == [250, 250, 500, 500]

        # Revert back to pixels
        reverted = denormalize_bbox(norm_box, img_w, img_h, scale=1000.0)
        assert reverted == [500.0, 750.0, 1000.0, 1500.0]

    def test_merge_multiple_bboxes_into_union(self):
        # 3 words: "Ramesh" [100, 200, 180, 230], "Chandra" [190, 200, 300, 230], "Sahu" [310, 200, 380, 230]
        boxes = [
            [100.0, 200.0, 180.0, 230.0],
            [190.0, 200.0, 300.0, 230.0],
            [310.0, 200.0, 380.0, 230.0],
        ]
        union_bbox = merge_bboxes(boxes)
        assert union_bbox == [100.0, 200.0, 380.0, 230.0]

    def test_compute_iou(self):
        box1 = [0.0, 0.0, 100.0, 100.0]
        box2 = [50.0, 0.0, 150.0, 100.0]
        
        # Overlap is 50x100 = 5000; Union is 150x100 = 15000; IoU = 5000/15000 = 0.333...
        iou = compute_iou(box1, box2)
        assert round(iou, 3) == 0.333

        # Non-overlapping boxes
        box3 = [200.0, 200.0, 300.0, 300.0]
        assert compute_iou(box1, box3) == 0.0

    def test_horizontal_alignment(self):
        # Label: "Plot No:" at line y=500
        label_box = [100.0, 490.0, 220.0, 520.0]
        # Value: "382/1" to the right at same y
        value_box = [240.0, 492.0, 340.0, 522.0]
        # Different line
        other_box = [240.0, 700.0, 340.0, 730.0]

        assert are_horizontally_aligned(label_box, value_box, y_tolerance=20.0) is True
        assert are_horizontally_aligned(label_box, other_box, y_tolerance=20.0) is False

    def test_vertical_alignment(self):
        # Column Header at x=400..600
        header_box = [400.0, 100.0, 600.0, 140.0]
        # Table cell underneath at x=405..595, y=250..280
        cell_box = [405.0, 250.0, 595.0, 280.0]
        # Cell above header (invalid)
        above_box = [405.0, 50.0, 595.0, 80.0]

        assert are_vertically_aligned(header_box, cell_box, x_tolerance=30.0) is True
        assert are_vertically_aligned(header_box, above_box, x_tolerance=30.0) is False

    def test_spatial_proximity_score(self):
        label_box = [100.0, 500.0, 200.0, 530.0]
        close_val_box = [210.0, 500.0, 310.0, 530.0]
        distant_box = [800.0, 900.0, 900.0, 930.0]

        score_close = calculate_spatial_proximity_score(label_box, close_val_box)
        score_distant = calculate_spatial_proximity_score(label_box, distant_box)

        # Close aligned value should have high proximity score
        assert score_close >= 0.90
        assert score_distant <= 0.35


class TestEvidenceLinker:
    """Tests binding tokens to evidence snippets for the Officer UI."""

    def test_create_evidence_from_blocks(self):
        b1 = OCRBlock(text="Ramesh", bbox=[100.0, 400.0, 200.0, 440.0], confidence=0.96)
        b2 = OCRBlock(text="Chandra", bbox=[210.0, 400.0, 320.0, 440.0], confidence=0.94)
        b3 = OCRBlock(text="Sahu", bbox=[330.0, 400.0, 400.0, 440.0], confidence=0.98)

        evidence = EvidenceLinker.create_evidence([b1, b2, b3], page_number=1)
        assert isinstance(evidence, EvidenceSnippet)
        assert evidence.page_number == 1
        assert evidence.source_text == "Ramesh Chandra Sahu"
        assert evidence.bbox == [100.0, 400.0, 400.0, 440.0]
        assert 0.94 <= evidence.ocr_confidence <= 0.98

    def test_evidence_grounding_with_real_fixture(self):
        with open(FIXTURES_DIR / "english_sample.json", "r", encoding="utf-8") as f:
            doc_data = json.load(f)

        doc = OCRDocument.model_validate(doc_data)
        page = doc.pages[0]

        # Find "Khata No: 45" block
        khata_block = next((b for b in page.ocr_blocks if "Khata No" in b.text), None)
        assert khata_block is not None

        evidence = EvidenceLinker.create_evidence([khata_block], page_number=page.page_number)
        assert "Khata No: 45" in evidence.source_text
        assert evidence.ocr_confidence >= 0.95
        assert evidence.bbox == khata_block.bbox

    def test_empty_blocks_raises_error(self):
        with pytest.raises(ValueError, match="Cannot create evidence without at least one source OCRBlock"):
            EvidenceLinker.create_evidence([], page_number=1)
