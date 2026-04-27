"""Detect hardcoded (burned-in) subtitles in a video by sampling frames with OCR."""
import argparse
import subprocess
from pathlib import Path

import cv2
import numpy as np
import pytesseract
import yaml


def load_config(config_path="config.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_stream_url(video_url: str) -> str:
    """Get direct CDN URL for a video stream of at least 360p for reliable OCR."""
    result = subprocess.run(
        [
            "yt-dlp", "--get-url", "--no-warnings",
            "-f", "best[height<=480][ext=mp4]/worst[height>=360][ext=mp4]/best[ext=mp4]/best",
            video_url,
        ],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip().split("\n")[0]


def sample_frames(stream_url: str, duration_sec: float | None, sample_times_sec: list) -> list:
    """Capture one frame per timestamp from a video stream URL."""
    if duration_sec and duration_sec > 0:
        times = [t for t in sample_times_sec if t < duration_sec * 0.95]
        if not times:
            times = [duration_sec * 0.1]
    else:
        times = sample_times_sec

    cap = cv2.VideoCapture(stream_url)
    frames = []
    for t in times:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ret, frame = cap.read()
        if ret and frame is not None:
            frames.append(frame)
    cap.release()
    return frames


def ocr_bottom_strip(frame: np.ndarray, bottom_fraction: float = 0.35) -> dict:
    """
    Run OCR on the bottom strip of a frame using multiple preprocessing strategies.
    Returns the result with the most words found.
    """
    h = frame.shape[0]
    strip = frame[int(h * (1 - bottom_fraction)):, :]
    gray = cv2.cvtColor(strip, cv2.COLOR_BGR2GRAY)

    # Try multiple preprocessing approaches — take whichever finds the most words
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, otsu_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    candidates = [gray, otsu, otsu_inv]

    best = {"text": "", "confidence": 0.0, "word_count": 0}
    for img in candidates:
        data = pytesseract.image_to_data(
            img, lang="spa",
            config="--psm 11",  # sparse text — works well for subtitles
            output_type=pytesseract.Output.DICT,
        )
        words = [w for w, c in zip(data["text"], data["conf"]) if w.strip() and int(c) > 20]
        if len(words) > best["word_count"]:
            confs = [int(c) for c in data["conf"] if int(c) > 0]
            best = {
                "text": " ".join(words),
                "confidence": round(sum(confs) / len(confs), 1) if confs else 0.0,
                "word_count": len(words),
            }

    return best


def _get_stream_duration(stream_url: str) -> float | None:
    cap = cv2.VideoCapture(stream_url)
    fps_val = cap.get(cv2.CAP_PROP_FPS)
    n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    if fps_val > 0 and n_frames > 0:
        return n_frames / fps_val
    return None


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
    duration = _get_stream_duration(stream_url)
    frames = sample_frames(stream_url, duration, sample_times)

    if not frames:
        return {
            "subtitle_type": "error",
            "frames_with_text": 0,
            "frames_sampled": 0,
            "ocr_confidence_avg": 0.0,
            "sample_texts": [],
        }

    ocr_results = [ocr_bottom_strip(f, bottom_fraction) for f in frames]

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
