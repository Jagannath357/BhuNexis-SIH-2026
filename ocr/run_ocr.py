import argparse
import sys
import json
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import SAMPLES_DIR, OUTPUT_DIR, PREPROCESS_PRESETS
from pipeline import LandRecordOCRPipeline
from utils.sample_generator import generate_sample_documents



def format_table_row(cols, widths):
    return " | ".join(str(c).ljust(w) for c, w in zip(cols, widths))


def main():
    parser = argparse.ArgumentParser(
        description="Handwritten English Land Record OCR Pipeline CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--image", type=str, default=None, help="Path to land record document image")
    parser.add_argument("--doc-id", type=str, default=None, help="Document ID (e.g. LR_001)")
    parser.add_argument("--engine", type=str, choices=["paddleocr", "trocr", "auto"], default="auto",
                        help="OCR Engine: 'paddleocr' (primary), 'trocr' (fallback), or 'auto'")
    parser.add_argument("--preset", type=str, choices=PREPROCESS_PRESETS, default="standard",
                        help="Preprocessing preset")
    parser.add_argument("--generate-samples", action="store_true",
                        help="Generate synthetic handwritten land record samples in samples/")
    parser.add_argument("--benchmark", action="store_true",
                        help="Run benchmark evaluation over all samples in samples/ directory")

    args = parser.parse_args()

    # 1. Generate Samples if requested or if samples/ is empty
    existing_samples = list(SAMPLES_DIR.glob("*.jpg")) + list(SAMPLES_DIR.glob("*.png"))
    if args.generate_samples or (not existing_samples and (args.benchmark or not args.image)):
        print("\n[+] Generating synthetic handwritten land record samples...")
        created = generate_sample_documents(SAMPLES_DIR)
        print(f"[+] Successfully generated {len(created)} sample documents in {SAMPLES_DIR}\n")
        existing_samples = created

    # 2. Benchmark Mode
    if args.benchmark:
        print("=" * 85)
        print("  HANDWRITTEN ENGLISH OCR PIPELINE — BENCHMARK EVALUATION")
        print("=" * 85)

        pipeline = LandRecordOCRPipeline()
        results_summary = []

        for sample_path in sorted(existing_samples):
            doc_id = sample_path.stem
            print(f"\n--- Testing Document: {sample_path.name} ---")
            start_t = time.time()
            res = pipeline.process_document(
                image_input=sample_path,
                document_id=doc_id,
                engine=args.engine,
                preprocess_preset=args.preset
            )
            elapsed = time.time() - start_t
            data = res["data"]
            results_summary.append({
                "doc_id": doc_id,
                "engine": data["ocr_engine"],
                "confidence": f"{data['confidence'] * 100:.1f}%",
                "boxes": len(data["boxes"]),
                "time": f"{elapsed:.2f}s",
                "text_snippet": (data["text"].split("\n")[0] if data["text"] else "None")[:35]
            })

            print(f"Engine Used    : {data['ocr_engine']}")
            print(f"Confidence     : {data['confidence'] * 100:.1f}%")
            print(f"Boxes Detected : {len(data['boxes'])}")
            print(f"Time Taken     : {elapsed:.2f}s")
            print(f"Recognized Text:\n{'-'*40}\n{data['text']}\n{'-'*40}")

        print("\n" + "=" * 85)
        print("  BENCHMARK SUMMARY TABLE")
        print("=" * 85)
        headers = ["Document ID", "Engine", "Conf.", "Boxes", "Latency", "First Line Preview"]
        widths = [16, 18, 8, 7, 9, 35]
        print(format_table_row(headers, widths))
        print("-" * 85)
        for r in results_summary:
            print(format_table_row([r["doc_id"], r["engine"], r["confidence"], r["boxes"], r["time"], r["text_snippet"]], widths))
        print("=" * 85)
        return

    # 3. Single Image Mode
    target_image = args.image
    if not target_image:
        if existing_samples:
            target_image = str(existing_samples[0])
            print(f"[*] No image specified. Defaulting to sample: {target_image}")
        else:
            print("[-] No image provided and no samples found. Use --generate-samples or specify --image.")
            sys.exit(1)

    doc_id = args.doc_id or Path(target_image).stem
    pipeline = LandRecordOCRPipeline()

    print(f"\n[+] Processing image: {target_image}")
    print(f"[*] Engine: {args.engine} | Preset: {args.preset} | Document ID: {doc_id}")

    res = pipeline.process_document(
        image_input=target_image,
        document_id=doc_id,
        engine=args.engine,
        preprocess_preset=args.preset
    )

    data = res["data"]
    print("\n" + "=" * 60)
    print(f"  OCR RESULT FOR {doc_id}")
    print("=" * 60)
    print(f"OCR Engine : {data['ocr_engine']}")
    print(f"Confidence : {data['confidence'] * 100:.2f}%")
    print(f"Status     : {data['status']}")
    print(f"Boxes Count: {len(data['boxes'])}")
    print(f"Skew Angle : {data['preprocessing']['deskew_angle']} deg")
    print("-" * 60)
    print("Recognized Text:")
    print(data["text"])
    print("-" * 60)
    print("Standardized Output JSON (pages & ocr_blocks):")
    print(json.dumps(res["standard_format"], indent=2))
    print("-" * 60)
    print(f"[+] Output JSON saved at: output/{doc_id}/{doc_id}_ocr_result.json")
    print(f"[+] Annotated visual image saved at: output/{doc_id}/{doc_id}_annotated.jpg")
    print(f"[+] Side-by-side comparison saved at: output/{doc_id}/{doc_id}_comparison.jpg\n")


if __name__ == "__main__":
    main()
