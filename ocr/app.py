import streamlit as st
import cv2
import numpy as np
from PIL import Image
import json
from pathlib import Path
import time
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import SAMPLES_DIR, OUTPUT_DIR, PREPROCESS_PRESETS, DEFAULT_PREPROCESS_PRESET
from pipeline import LandRecordOCRPipeline
from utils.sample_generator import generate_sample_documents


# Page configuration
st.set_page_config(
    page_title="Handwritten English Land Record OCR",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished interface
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .badge-high {
        background-color: #065f46;
        color: #34d399;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-mid {
        background-color: #78350f;
        color: #fbbf24;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-low {
        background-color: #7f1d1d;
        color: #f87171;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_pipeline():
    return LandRecordOCRPipeline()


def ensure_samples():
    existing = list(SAMPLES_DIR.glob("*.jpg")) + list(SAMPLES_DIR.glob("*.png"))
    if not existing:
        generate_sample_documents(SAMPLES_DIR)
        existing = list(SAMPLES_DIR.glob("*.jpg")) + list(SAMPLES_DIR.glob("*.png"))
    return existing


def main():
    st.markdown('<div class="main-header">📜 Handwritten English Land Record OCR</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Pretrained OCR (PaddleOCR PP-OCRv5 + Microsoft TrOCR Fallback) with Human Verification Layer</div>', unsafe_allow_html=True)

    pipeline = get_pipeline()
    sample_files = ensure_samples()

    # Sidebar Configuration
    st.sidebar.header("⚙️ OCR Configuration")

    doc_source = st.sidebar.radio(
        "Document Source",
        ["Select Sample Record", "Upload Custom Image"]
    )

    selected_image_path = None
    uploaded_image_array = None

    if doc_source == "Select Sample Record":
        sample_names = [f.name for f in sample_files]
        chosen_sample = st.sidebar.selectbox("Choose Sample Land Record", sample_names)
        selected_image_path = SAMPLES_DIR / chosen_sample
        doc_id = Path(chosen_sample).stem
    else:
        uploaded_file = st.sidebar.file_uploader("Upload Land Record Scan", type=["jpg", "jpeg", "png", "tif", "bmp"])
        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            uploaded_image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            doc_id = Path(uploaded_file.name).stem
        else:
            doc_id = "CUSTOM_001"

    st.sidebar.markdown("---")
    st.sidebar.subheader("Engine & Preprocessing")

    engine_choice = st.sidebar.selectbox(
        "OCR Engine",
        ["auto", "paddleocr", "trocr"],
        format_func=lambda x: {
            "auto": "⚡ Auto (PaddleOCR -> TrOCR Fallback)",
            "paddleocr": "🚀 PaddleOCR (PP-OCRv5 Primary)",
            "trocr": "🛡️ Microsoft TrOCR (Fallback)"
        }[x]
    )

    preset_choice = st.sidebar.selectbox(
        "OpenCV Preprocessing Preset",
        PREPROCESS_PRESETS,
        index=PREPROCESS_PRESETS.index(DEFAULT_PREPROCESS_PRESET)
    )

    fallback_thresh = st.sidebar.slider(
        "Auto-Fallback Confidence Threshold",
        min_value=0.30,
        max_value=0.90,
        value=0.60,
        step=0.05
    )
    pipeline.fallback_threshold = fallback_thresh

    if st.sidebar.button("🔄 Regenerate Samples"):
        generate_sample_documents(SAMPLES_DIR)
        st.sidebar.success("Generated 3 fresh land records!")
        st.rerun()

    # Main Processing Section
    image_to_process = uploaded_image_array if uploaded_image_array is not None else selected_image_path

    if image_to_process is None:
        st.info("👆 Please select a sample record from the sidebar or upload a document to begin.")
        return

    # Process Button
    col_btn, col_info = st.columns([1, 4])
    with col_btn:
        run_button = st.button("🚀 Run OCR Pipeline", type="primary", use_container_width=True)

    # Trigger process if button clicked or if result stored in session
    state_key = f"ocr_res_{doc_id}_{engine_choice}_{preset_choice}"

    if run_button or state_key in st.session_state:
        if run_button:
            with st.spinner("Processing document through OpenCV and Deep Learning OCR..."):
                t0 = time.time()
                ocr_out = pipeline.process_document(
                    image_input=image_to_process,
                    document_id=doc_id,
                    engine=engine_choice,
                    preprocess_preset=preset_choice
                )
                ocr_out["latency"] = time.time() - t0
                st.session_state[state_key] = ocr_out

        ocr_out = st.session_state[state_key]
        data = ocr_out["data"]
        latency = ocr_out.get("latency", 0.0)

        # Status Summary Metrics
        conf = data["confidence"]
        if conf >= 0.85:
            badge_html = f'<span class="badge-high">High Confidence ({conf*100:.1f}%)</span>'
        elif conf >= 0.65:
            badge_html = f'<span class="badge-mid">Medium Confidence ({conf*100:.1f}%)</span>'
        else:
            badge_html = f'<span class="badge-low">Needs Verification ({conf*100:.1f}%)</span>'

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Document ID", data["document_id"])
        with col2:
            st.metric("Active Engine", data["ocr_engine"])
        with col3:
            st.metric("Detected Lines / Boxes", len(data["boxes"]))
        with col4:
            st.metric("Processing Latency", f"{latency:.2f} s")

        if data.get("fallback_triggered"):
            st.info("ℹ️ **Emergency Decision Tree Activated (Section 8)**: Primary engine (PaddleOCR) encountered an upstream OneDNN PIR bug on Windows. The pipeline automatically switched to **Microsoft TrOCR**.")


        st.markdown("---")

        # Two Column Layout: Visuals vs Verification
        left_col, right_col = st.columns([3, 2])

        with left_col:
            st.subheader("🖼️ Document Inspection")
            view_tab1, view_tab2, view_tab3 = st.tabs(["Side-by-Side Comparison", "Annotated Bounding Boxes", "Preprocessed Image"])

            with view_tab1:
                comp_rgb = cv2.cvtColor(ocr_out["images"]["comparison"], cv2.COLOR_BGR2RGB)
                st.image(comp_rgb, caption="Raw Image  |  Preprocessed  |  Detected Text Regions", use_container_width=True)

            with view_tab2:
                anno_rgb = cv2.cvtColor(ocr_out["images"]["annotated"], cv2.COLOR_BGR2RGB)
                st.image(anno_rgb, caption="OCR Detection Polygons with Confidence Scores", use_container_width=True)

            with view_tab3:
                prep_rgb = cv2.cvtColor(ocr_out["images"]["preprocessed"], cv2.COLOR_BGR2RGB)
                st.image(prep_rgb, caption=f"Preprocessed with preset: '{preset_choice}'", use_container_width=True)

        with right_col:
            st.subheader("✍️ Human Verification Layer")
            st.caption("Section 12: OCR output must be verified/edited before legal entity extraction.")

            verified_text = st.text_area(
                "Review & Correct Recognized Text:",
                value=data["text"],
                height=320,
                key=f"editor_{doc_id}"
            )

            is_verified = st.button("✅ Verify & Approve Land Record", use_container_width=True)
            if is_verified:
                data["text"] = verified_text
                data["status"] = "Verified by Human"
                st.success("Record marked as VERIFIED! Ready for downstream processing.")

            st.markdown("### 📋 Standardized JSON Output")
            st.caption("Section 13: Standardized output schema ready for integration.")

            # Synchronize edited text lines with bounding boxes
            edited_lines = [l.strip() for l in verified_text.split("\n") if l.strip()]
            updated_boxes = []
            for i, line in enumerate(edited_lines):
                if i < len(data.get("boxes", [])):
                    b = dict(data["boxes"][i])
                    b["text"] = line
                else:
                    b = {
                        "text": line,
                        "bbox": [0.0, 0.0, 0.0, 0.0],
                        "confidence": round(float(data.get("confidence", 0.90)), 4),
                        "language": "en"
                    }
                b.pop("box", None)
                updated_boxes.append(b)

            img_h, img_w = ocr_out["images"]["preprocessed"].shape[:2]
            export_payload = {
                "document_id": data["document_id"],
                "language": "en",
                "pages": [
                    {
                        "page_number": 1,
                        "image_width": int(img_w),
                        "image_height": int(img_h),
                        "ocr_blocks": [
                            {
                                "text": b.get("text", ""),
                                "bbox": b.get("bbox", [0.0, 0.0, 0.0, 0.0]),
                                "confidence": round(float(b.get("confidence", 0.95)), 2),
                                "language": b.get("language", "en")
                            }
                            for b in updated_boxes
                        ]
                    }
                ]
            }

            st.json(export_payload)

            st.download_button(
                label="📥 Download Standardized JSON",
                data=json.dumps(export_payload, indent=2),
                file_name=f"{doc_id}_standardized_ocr.json",
                mime="application/json",
                use_container_width=True,
                key=f"dl_standard_{doc_id}"
            )



if __name__ == "__main__":
    main()
