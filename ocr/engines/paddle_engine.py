import os
import numpy as np
from typing import List, Optional
import logging
from .base_engine import BaseOCREngine, OCRResult, OCRBox

# Top-level import for static analysis / IDE language server
try:
    os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"
    from paddleocr import PaddleOCR
    import paddle
    PADDLE_AVAILABLE = True
except ImportError:
    PaddleOCR = None  # type: ignore
    paddle = None     # type: ignore
    PADDLE_AVAILABLE = False

logger = logging.getLogger(__name__)



class PaddleOCREngine(BaseOCREngine):
    """
    Primary OCR Engine: PaddleOCR PP-OCRv5 English.
    Spec: en_PP-OCRv5_mobile_rec, local, Apache-2.0, zero cloud dependency.
    """

    def __init__(self, lang: str = "en", use_angle_cls: bool = True, use_gpu: bool = True):
        self.lang = lang
        self.use_angle_cls = use_angle_cls
        self.use_gpu = use_gpu
        self._ocr = None

    def initialize(self) -> None:
        """Initializes PaddleOCR model instance (downloads weights once if missing)."""
        if self._ocr is not None:
            return

        try:
            import os
            os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"
            from paddleocr import PaddleOCR
            import paddle
            
            # Check if GPU is available in paddle
            gpu_available = False
            try:
                gpu_available = paddle.device.is_compiled_with_cuda() and paddle.device.cuda.device_count() > 0
            except Exception:
                gpu_available = False

            actual_use_gpu = self.use_gpu and gpu_available
            logger.info(f"Initializing PaddleOCR (lang={self.lang}, use_gpu={actual_use_gpu})")

            # In paddleocr 3.x, configure detection + recognition without heavy doc unwarping
            try:
                self._ocr = PaddleOCR(
                    lang=self.lang,
                    use_doc_orientation_classify=False,
                    use_doc_unwarping=False,
                    use_textline_orientation=self.use_angle_cls
                )
            except Exception:
                try:
                    self._ocr = PaddleOCR(lang=self.lang)
                except Exception as ex:
                    logger.error(f"Fallback init failed: {ex}")
                    raise
            logger.info("PaddleOCR engine loaded successfully.")


        except Exception as e:
            logger.error(f"Failed to initialize PaddleOCR: {e}")
            raise RuntimeError(f"PaddleOCR initialization failed: {e}")

    @staticmethod
    def _sort_boxes_reading_order(boxes: List[OCRBox], y_tolerance: int = 15) -> List[OCRBox]:
        """
        Sorts bounding boxes top-to-bottom, left-to-right to reconstruct
        correct reading order of land records.
        """
        if not boxes:
            return []

        def get_top_y(b: OCRBox) -> int:
            return min(p[1] for p in b.box)

        def get_left_x(b: OCRBox) -> int:
            return min(p[0] for p in b.box)

        # First sort by top Y coordinate
        sorted_by_y = sorted(boxes, key=get_top_y)
        lines = []
        current_line = [sorted_by_y[0]]

        for box in sorted_by_y[1:]:
            curr_y = get_top_y(box)
            prev_y = get_top_y(current_line[-1])

            if abs(curr_y - prev_y) <= y_tolerance:
                current_line.append(box)
            else:
                # Sort current line horizontally (left to right)
                current_line.sort(key=get_left_x)
                lines.extend(current_line)
                current_line = [box]

        if current_line:
            current_line.sort(key=get_left_x)
            lines.extend(current_line)

        return lines

    def recognize(self, image: np.ndarray, document_id: str = "LR_001") -> OCRResult:
        """
        Runs PaddleOCR detection + recognition pipeline.
        Returns standardized OCRResult schema.
        """
        self.initialize()

        # Ensure image is in BGR uint8 format
        if len(image.shape) == 2:
            import cv2
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        try:
            raw_results = self._ocr.ocr(image)
        except TypeError:
            raw_results = self._ocr.predict(image)


        detected_boxes: List[OCRBox] = []
        # PaddleOCR returns [ [ [points], (text, score) ], ... ]
        if raw_results and len(raw_results) > 0 and raw_results[0] is not None:
            # Handle both single image output and list of outputs
            line_items = raw_results[0] if isinstance(raw_results, list) and isinstance(raw_results[0], list) else raw_results
            for item in line_items:
                if not item or len(item) < 2:
                    continue
                coords, (text, conf) = item
                clean_text = text.strip() if text else ""
                if clean_text:
                    int_coords = [[int(pt[0]), int(pt[1])] for pt in coords]
                    detected_boxes.append(
                        OCRBox(
                            text=clean_text,
                            confidence=float(conf),
                            box=int_coords
                        )
                    )

        sorted_boxes = self._sort_boxes_reading_order(detected_boxes)
        full_text = "\n".join([b.text for b in sorted_boxes])
        mean_conf = (
            float(np.mean([b.confidence for b in sorted_boxes]))
            if sorted_boxes
            else 0.0
        )

        status = "Needs Human Verification" if mean_conf < 0.85 else "Recognized"

        return OCRResult(
            document_id=document_id,
            language="English",
            ocr_engine="PaddleOCR",
            text=full_text,
            confidence=mean_conf,
            boxes=sorted_boxes,
            status=status
        )
