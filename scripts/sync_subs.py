"""Analyze subtitle synchronization against video duration."""
import argparse
from pathlib import Path

import cv2

from extract_subs import load_subtitles


def get_video_duration(video_path: Path) -> float:
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    return frame_count / fps if fps > 0 else 0.0


def analyze_sync(video_path: Path, subs_path: Path) -> dict:
    duration = get_video_duration(video_path)
    segments = load_subtitles(subs_path)

    if not segments:
        return {"sync_ok": False, "reason": "no_subtitles", "duration_video": duration}

    sub_start = segments[0].start
    sub_end = segments[-1].end
    coverage = (sub_end - sub_start) / duration if duration > 0 else 0

    gaps = [
        segments[i + 1].start - segments[i].end
        for i in range(len(segments) - 1)
    ]
    avg_gap = sum(gaps) / len(gaps) if gaps else 0

    # Heuristic: subtitles that start >10s after video or end >15s before are suspect
    offset_start = sub_start
    tail_gap = duration - sub_end
    sync_ok = offset_start < 10 and tail_gap < 15 and coverage > 0.5

    return {
        "sync_ok": sync_ok,
        "duration_video": round(duration, 2),
        "sub_start": round(sub_start, 2),
        "sub_end": round(sub_end, 2),
        "coverage_ratio": round(coverage, 3),
        "avg_gap_between_segments": round(avg_gap, 3),
        "n_segments": len(segments),
        "offset_start": round(offset_start, 2),
        "tail_gap": round(tail_gap, 2),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check subtitle sync")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("subs", help="Path to subtitle file (.srt/.vtt)")
    args = parser.parse_args()

    result = analyze_sync(Path(args.video), Path(args.subs))
    for k, v in result.items():
        print(f"  {k}: {v}")
