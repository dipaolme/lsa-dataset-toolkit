"""Detect hardcoded (burned-in) subtitles in a video by sampling frames with OCR."""
import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from utils.ocr import get_stream_url, get_stream_duration, sample_frames, ocr_bottom_strip


def load_config(config_path="config.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)


def detect_hardcoded_subs(video_url: str, config: dict) -> dict:
    """
    Sample frames from video_url and detect if subtitles are burned into the video.

    Returns:
        subtitle_type: "hardcoded" | "uncertain" | "none"
        frames_with_text: int
        frames_sampled: int
        ocr_confidence_avg: float
        sample_texts: list[str]
    """
    ocr_cfg = config.get("ocr", {})
    sample_times = ocr_cfg.get("sample_times_sec", [5, 10, 30, 60, 90])
    bottom_fraction = ocr_cfg.get("bottom_fraction", 0.35)
    threshold = ocr_cfg.get("text_threshold", 3)

    stream_url = get_stream_url(video_url)
    duration = get_stream_duration(stream_url)
    frame_pairs = sample_frames(stream_url, duration, sample_times)

    if not frame_pairs:
        return {
            "subtitle_type": "error",
            "frames_with_text": 0,
            "frames_sampled": 0,
            "ocr_confidence_avg": 0.0,
            "sample_texts": [],
        }

    ocr_results = [ocr_bottom_strip(frame, bottom_fraction) for _, frame in frame_pairs]

    frames_with_text = sum(1 for r in ocr_results if r["word_count"] >= 1)
    sample_texts = [r["text"] for r in ocr_results if r["text"].strip()]
    confs = [r["confidence"] for r in ocr_results if r["word_count"] >= 1 and r["confidence"] > 0]
    ocr_confidence_avg = round(sum(confs) / len(confs), 1) if confs else 0.0

    if frames_with_text >= threshold:
        subtitle_type = "hardcoded"
    elif frames_with_text >= 1:
        subtitle_type = "uncertain"
    else:
        subtitle_type = "none"

    return {
        "subtitle_type": subtitle_type,
        "frames_with_text": frames_with_text,
        "frames_sampled": len(frames),
        "ocr_confidence_avg": ocr_confidence_avg,
        "sample_texts": sample_texts,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect hardcoded subtitles via OCR frame sampling")
    parser.add_argument("video_url", help="YouTube video URL")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    result = detect_hardcoded_subs(args.video_url, config)

    print(f"subtitle_type:    {result['subtitle_type']}")
    print(f"frames_with_text: {result['frames_with_text']}/{result['frames_sampled']}")
    print(f"ocr_confidence:   {result['ocr_confidence_avg']}")
    if result["sample_texts"]:
        print("sample texts:")
        for t in result["sample_texts"]:
            print(f"  → {t[:120]}")
