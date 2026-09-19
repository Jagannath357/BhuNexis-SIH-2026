import numpy as np
import cv2
from typing import List, Optional
import logging
from PIL import Image
from .base_engine import BaseOCREngine, OCRResult, OCRBox

# Top-level imports for static analysis / IDE language server
try:
    import torch
    from transformers import (
        RobertaTokenizer,
        XLMRobertaTokenizer,
        ViTImageProcessor,
        TrOCRProcessor,
        VisionEncoderDecoderModel,
    )
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    torch = None  # type: ignore
    TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)


class TrOCREngine(BaseOCREngine):
    """
    Fallback OCR Engine: Microsoft TrOCR (Transformer-based Optical Character Recognition).
    Spec: microsoft/trocr-base-handwritten or microsoft/trocr-small-handwritten.
    Specifically designed and pre-trained for handwriting recognition.
    """

    def __init__(self, model_name: str = "microsoft/trocr-base-handwritten", device: Optional[str] = None):
        self.model_name = model_name
        self.device = device
        self._processor = None
        self._model = None

    def initialize(self) -> None:
        """Loads TrOCR model and processor weights via HuggingFace transformers."""
        if self._model is not None:
            return

        if not TRANSFORMERS_AVAILABLE:
            raise RuntimeError("The 'transformers' and 'torch' packages are required for TrOCR.")

        try:
            if self.device is None:
                self.device = "cuda" if torch.cuda.is_available() else "cpu"

            logger.info(f"Loading TrOCR model '{self.model_name}' on device '{self.device}'...")
            try:
                self._processor = TrOCRProcessor.from_pretrained(self.model_name)
            except Exception:
                # Explicit tokenizer selection
                if "small" in self.model_name.lower():
                    tok = XLMRobertaTokenizer.from_pretrained(self.model_name)
                else:
                    tok = RobertaTokenizer.from_pretrained(self.model_name)
                img_proc = ViTImageProcessor.from_pretrained(self.model_name)
                self._processor = TrOCRProcessor(image_processor=img_proc, tokenizer=tok)

            self._model = VisionEncoderDecoderModel.from_pretrained(self.model_name).to(self.device)
            self._model.eval()
            logger.info(f"TrOCR engine loaded successfully on {self.device}.")

        except Exception as e:
            logger.error(f"Failed to initialize TrOCR: {e}")
            raise RuntimeError(f"TrOCR initialization failed: {e}")



    @staticmethod
    def _detect_line_segments(gray: np.ndarray) -> List[List[int]]:
        """
        Advanced line segmenter tailored for land deeds with borders, tables, and handwritten lines.
        Filters out outer borders and isolates text lines via morphology.
        Returns list of bounding boxes: [[x, y, w, h], ...]
        """
        img_h, img_w = gray.shape[:2]
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        # 1. Collect valid character/word contours (ignoring borders)
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        clean_text_mask = np.zeros_like(thresh)

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            # Skip page border frames or gigantic shapes
            if w > 0.75 * img_w or h > 0.65 * img_h:
                continue
            # Keep character-like strokes
            if w > 3 and h > 5 and (w * h) > 25:
                clean_text_mask[y:y+h, x:x+w] = thresh[y:y+h, x:x+w]

        # 2. Horizontal dilation to bridge words into cohesive text lines
        kernel_w = max(35, img_w // 30)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_w, 3))
        dilated = cv2.dilate(clean_text_mask, kernel, iterations=2)

        line_contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bounding_boxes = []
        for c in line_contours:
            x, y, w, h = cv2.boundingRect(c)
            # Valid line constraints
            if w > 35 and h > 12 and h < (img_h * 0.35):
                # Add slight padding for descenders and ascenders
                pad_x = 6
                pad_y = 4
                nx = max(0, x - pad_x)
                ny = max(0, y - pad_y)
                nw = min(img_w - nx, w + (2 * pad_x))
                nh = min(img_h - ny, h + (2 * pad_y))
                bounding_boxes.append([nx, ny, nw, nh])

        # Sort reading order (top to bottom, then left to right for columns)
        bounding_boxes.sort(key=lambda b: (b[1] // 25, b[0]))
        return bounding_boxes


    def recognize(self, image: np.ndarray, document_id: str = "LR_001", line_boxes: Optional[List[List[List[int]]]] = None) -> OCRResult:
        """
        Runs TrOCR handwritten text recognition.
        If line_boxes are provided (from PaddleOCR detector), crops each region.
        Otherwise, slices lines using OpenCV morphology.
        """
        self.initialize()
        import torch

        # Ensure RGB format for Pillow / TrOCR
        if len(image.shape) == 2:
            rgb_img = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            gray_img = image
        else:
            rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        h_img, w_img = image.shape[:2]
        crops = []
        box_coords = []

        if line_boxes and len(line_boxes) > 0:
            # Use externally provided bounding boxes (e.g. from PaddleOCR DBNet detector)
            for pts in line_boxes:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                min_x, max_x = max(0, min(xs)), min(w_img, max(xs))
                min_y, max_y = max(0, min(ys)), min(h_img, max(ys))
                if max_x - min_x > 10 and max_y - min_y > 10:
                    crop = rgb_img[min_y:max_y, min_x:max_x]
                    crops.append(Image.fromarray(crop))
                    box_coords.append(pts)
        else:
            # Slices lines via OpenCV
            detected_rects = self._detect_line_segments(gray_img)
            if not detected_rects:
                # Direct whole-image recognition fallback
                crops = [Image.fromarray(rgb_img)]
                box_coords = [[[0, 0], [w_img, 0], [w_img, h_img], [0, h_img]]]
            else:
                for (x, y, w, h) in detected_rects:
                    crop = rgb_img[y:y+h, x:x+w]
                    crops.append(Image.fromarray(crop))
                    box_coords.append([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])

        detected_boxes: List[OCRBox] = []

        # Fast inference setting: greedy decoding (num_beams=1) on CPU for responsiveness
        beams = 1 if self.device == "cpu" else 3

        # Process each line crop with TrOCR
        for crop_pil, box in zip(crops, box_coords):
            try:
                pixel_values = self._processor(images=crop_pil, return_tensors="pt").pixel_values.to(self.device)
                with torch.no_grad():
                    generated_ids = self._model.generate(
                        pixel_values,
                        max_new_tokens=48,
                        num_beams=beams,
                        early_stopping=True if beams > 1 else False,
                        return_dict_in_generate=True,
                        output_scores=True
                    )
                
                # Decode text
                pred_text = self._processor.batch_decode(generated_ids.sequences, skip_special_tokens=True)[0].strip()

                # Authentic confidence computation from model transition scores
                conf = 0.85
                try:
                    transition_scores = self._model.compute_transition_scores(
                        generated_ids.sequences,
                        generated_ids.scores,
                        normalize_logits=True
                    )
                    token_probs = np.exp(transition_scores[0].cpu().numpy())
                    valid_probs = token_probs[np.isfinite(token_probs)]
                    if len(valid_probs) > 0:
                        conf = float(np.mean(valid_probs))
                        conf = float(np.clip(conf, 0.10, 0.99))
                except Exception as ex:
                    logger.debug(f"Transition scores calculation failed: {ex}")


                if pred_text:
                    clean_str = pred_text.strip()
                    # Filter out stray single digits / punctuation on margins (e.g. '0', '0 0', '0 1')
                    if len(clean_str) <= 2 and not any(c.isalpha() for c in clean_str):
                        continue
                    detected_boxes.append(OCRBox(text=clean_str, confidence=conf, box=box, language="en"))
            except Exception as e:
                logger.warning(f"TrOCR failed to process line crop: {e}")


        full_text = "\n".join([b.text for b in detected_boxes])
        mean_conf = float(np.mean([b.confidence for b in detected_boxes])) if detected_boxes else 0.0
        status = "Needs Human Verification" if mean_conf < 0.85 else "Recognized"

        return OCRResult(
            document_id=document_id,
            language="English",
            ocr_engine=f"TrOCR ({self.model_name.split('/')[-1]})",
            text=full_text,
            confidence=mean_conf,
            boxes=detected_boxes,
            status=status
        )
