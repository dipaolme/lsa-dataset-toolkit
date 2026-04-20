"""Build final dataset by aligning subtitles with keypoints."""
import argparse
import json
from pathlib import Path

import yaml

from extract_subs import load_subtitles
from extract_keypoints import extract_keypoints
from sync_subs import analyze_sync, get_video_duration


def load_config(config_path="config.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)


def build_dataset(video_path: Path, subs_path: Path, config: dict, intent: str = None, tramite: str = None) -> list[dict]:
    fps = _get_fps(video_path)
    segments = load_subtitles(subs_path)
    sync_info = analyze_sync(video_path, subs_path)

    entries = []
    for seg in segments:
        frame_start = int(seg.start * fps)
        frame_end = int(seg.end * fps)

        keypoints = extract_keypoints(video_path, config, frame_start, frame_end)

        entry = {
            "id": f"{video_path.stem}_{seg.index:04d}",
            "gloss": seg.text,
            "source": video_path.stem,
            "frames": {"start": frame_start, "end": frame_end},
            "keypoints": keypoints["frames"],
            "metadata": {
                "intent": intent,
                "tramite": tramite,
                "subtitle_type": "auto_cc",
                "sync_ok": sync_info["sync_ok"],
                "confidence_avg": keypoints["confidence_avg"],
                "fps": fps,
                "time_start": seg.start,
                "time_end": seg.end,
            },
        }
        entries.append(entry)

    return entries


def _get_fps(video_path: Path) -> float:
    import cv2
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build dataset from video + subtitles")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("subs", help="Path to subtitle file (.srt/.vtt)")
    parser.add_argument("--output", help="Output JSON path")
    parser.add_argument("--intent", help="Intent label (e.g. renovar_dni)", default=None)
    parser.add_argument("--tramite", help="Tramite category", default=None)
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    video_path = Path(args.video)
    entries = build_dataset(video_path, Path(args.subs), config, args.intent, args.tramite)

    output_path = Path(args.output) if args.output else Path(config["paths"]["dataset"]) / f"{video_path.stem}_dataset.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"Dataset saved: {output_path} ({len(entries)} entries)")
