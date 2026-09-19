import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
import json
import numpy as np

from config import (
    DEFAULT_PREPROCESS_PRESET,
    AUTO_FALLBACK_CONFIDENCE,
    DEFAULT_LANGUAGE,
    OUTPUT_DIR,
    DEFAULT_TROCR_MODEL
)
from preprocessing.preprocessor import ImagePreprocessor
from engines.base_engine import OCRResult
from utils.visualizer import OCRVisualizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("LandRecordOCRPipeline")


class LandRecordOCRPipeline:
    """
    Unified Pipeline Orchestrator for Handwritten English Land Records.
    Implements:
      1. OpenCV Preprocessing (Grayscale, CLAHE, Bilateral Denoising, Deskew)
      2. Primary Engine: PaddleOCR (PP-OCRv5 English)
      3. Fallback Engine: Microsoft TrOCR (Base Handwritten)
      4. Standardized JSON Output layer for downstream Human Verification & NLP
    """

    def __init__(
        self,
        primary_engine: str = "paddleocr",
        fallback_threshold: float = AUTO_FALLBACK_CONFIDENCE,
        trocr_model_name: str = DEFAULT_TROCR_MODEL
    ):
        self.primary_engine_name = primary_engine
        self.fallback_threshold = fallback_threshold
        self.trocr_model_name = trocr_model_name
        self.preprocessor = ImagePreprocessor()

        self._paddle_engine = None
        self._trocr_engine = None

    def get_paddle_engine(self):
        """Lazy-loads PaddleOCR primary engine."""
        if self._paddle_engine is None:
            from engines.paddle_engine import PaddleOCREngine
            self._paddle_engine = PaddleOCREngine(lang="en", use_angle_cls=True)
        return self._paddle_engine

    def get_trocr_engine(self):
        """Lazy-loads TrOCR fallback engine."""
        if self._trocr_engine is None:
            from engines.trocr_engine import TrOCREngine
            self._trocr_engine = TrOCREngine(model_name=self.trocr_model_name)
        return self._trocr_engine

    def process_document(
        self,
        image_input: Union[str, Path, np.ndarray],
        document_id: str = "LR_001",
        engine: str = "auto",
        preprocess_preset: str = DEFAULT_PREPROCESS_PRESET,
        save_artifacts: bool = True
    ) -> Dict[str, Any]:
        """
        Processes a handwritten land record image end-to-end.
        
        Args:
            image_input: File path or numpy BGR array.
            document_id: Identifier for the document.
            engine: 'paddleocr', 'trocr', or 'auto' (paddleocr with automatic TrOCR fallback).
            preprocess_preset: 'raw', 'standard', 'clahe_enhanced', 'denoise_adaptive', 'otsu_binarized'.
            save_artifacts: Whether to write result JSON and annotated image to output directory.

        Returns:
            Standardized JSON-serializable dictionary matching Section 4 & 12 specification.
        """
        logger.info(f"Processing document {document_id} with engine={engine}, preset={preprocess_preset}")

        # 1. Preprocessing
        prep_result = self.preprocessor.process(image_input, preset=preprocess_preset)
        raw_bgr = prep_result["stages"]["raw"]
        preprocessed_img = prep_result["processed"]
        deskew_angle = prep_result["deskew_angle"]

        ocr_result: Optional[OCRResult] = None
        used_fallback = False

        # 2. Engine Execution
        if engine == "trocr":
            # Force fallback engine directly
            logger.info("Using Microsoft TrOCR engine directly...")
            trocr = self.get_trocr_engine()
            ocr_result = trocr.recognize(preprocessed_img, document_id=document_id)

        elif engine == "paddleocr":
            # Force PaddleOCR directly
            logger.info("Using PaddleOCR primary engine...")
            try:
                paddle = self.get_paddle_engine()
                ocr_result = paddle.recognize(preprocessed_img, document_id=document_id)
            except Exception as e:
                logger.warning(f"PaddleOCR primary engine failed with error: {e}. Activating Decision Tree Step 8 emergency fallback to TrOCR...")
                used_fallback = True
                trocr = self.get_trocr_engine()
                ocr_result = trocr.recognize(preprocessed_img, document_id=document_id)
                ocr_result.status = "Fallback to TrOCR (PaddleOCR Windows OneDNN issue)"


        else:
            # 'auto' mode: Attempt Primary Engine (PaddleOCR) first
            try:
                logger.info("Auto mode: Attempting PaddleOCR primary engine...")
                paddle = self.get_paddle_engine()
                ocr_result = paddle.recognize(preprocessed_img, document_id=document_id)

                paddle_insufficient = (
                    ocr_result.confidence < self.fallback_threshold
                    or not ocr_result.text.strip()
                    or len(ocr_result.boxes) == 0
                )
            except Exception as e:
                logger.warning(f"PaddleOCR primary engine encountered error: {e}. Executing emergency fallback to TrOCR...")
                paddle_insufficient = True
                ocr_result = None

            if paddle_insufficient:
                logger.info(
                    f"Triggering Microsoft TrOCR fallback engine (Decision Tree Step 8)..."
                )
                used_fallback = True
                trocr = self.get_trocr_engine()
                line_boxes = [b.box for b in ocr_result.boxes] if (ocr_result and ocr_result.boxes) else None
                trocr_result = trocr.recognize(preprocessed_img, document_id=document_id, line_boxes=line_boxes)
                
                if trocr_result and trocr_result.text.strip():
                    ocr_result = trocr_result
                elif ocr_result is None:
                    ocr_result = trocr_result


        # 3. Format Standardized JSON output
        img_h, img_w = preprocessed_img.shape[:2]
        standard_format = ocr_result.to_standard_format(image_width=img_w, image_height=img_h)

        result_dict = {
            **standard_format,
            "ocr_engine": ocr_result.ocr_engine,
            "confidence": round(ocr_result.confidence, 4),
            "status": ocr_result.status,
            "boxes_count": len(ocr_result.boxes),
            "text": ocr_result.text,
            "boxes": [box.to_dict() for box in ocr_result.boxes],
            "preprocessing": {
                "preset": preprocess_preset,
                "deskew_angle": round(deskew_angle, 2)
            },
            "fallback_triggered": used_fallback
        }

        # 4. Generate visual annotations
        annotated_img = OCRVisualizer.draw_bounding_boxes(
            preprocessed_img,
            ocr_result.boxes
        )
        comparison_grid = OCRVisualizer.create_comparison_grid(
            raw_bgr,
            preprocessed_img,
            annotated_img
        )

        # 5. Save artifacts if requested
        if save_artifacts:
            doc_out_dir = OUTPUT_DIR / document_id
            doc_out_dir.mkdir(parents=True, exist_ok=True)

            # Save standardized OCR result JSON matching required schema
            json_path = doc_out_dir / f"{document_id}_ocr_result.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(standard_format, f, indent=2, ensure_ascii=False)

            # Also save detailed pipeline execution metadata
            meta_path = doc_out_dir / f"{document_id}_metadata.json"
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(result_dict, f, indent=2, ensure_ascii=False)

            annotated_path = doc_out_dir / f"{document_id}_annotated.jpg"
            comparison_path = doc_out_dir / f"{document_id}_comparison.jpg"
            OCRVisualizer.save_annotated_image(annotated_img, annotated_path)
            OCRVisualizer.save_annotated_image(comparison_grid, comparison_path)
            logger.info(f"Saved OCR artifacts to: {doc_out_dir}")

        return {
            "data": result_dict,
            "standard_format": standard_format,
            "images": {
                "raw": raw_bgr,
                "preprocessed": preprocessed_img,
                "annotated": annotated_img,
                "comparison": comparison_grid
            }
        }
