"""Scan raw MOV/MP4 files and return metadata + quality metrics."""
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

import cv2
import numpy as np


FLAG_PATTERNS = {
    "rejected":  re.compile(r'NO SE USA', re.IGNORECASE),
    "review":    re.compile(r'\bver\b', re.IGNORECASE),
    "redo":      re.compile(r'rehacer', re.IGNORECASE),
    "confirm":   re.compile(r'CONFIRMAR', re.IGNORECASE),
    "title":     re.compile(r'Titulo', re.IGNORECASE),
    "part1":     re.compile(r'primera parte', re.IGNORECASE),
    "part2":     re.compile(r'ultima parte', re.IGNORECASE),
}


@dataclass
class VideoMeta:
    filename: str
    video_num: int | None
    duration_s: float
    fps: float
    width: int
    height: int
    total_frames: int
    blur_score: float       # Laplacian variance — higher = sharper
    flags: list[str]
    readable: bool          # False if cv2 can't open it


def _extract_num(filename: str) -> int | None:
    m = re.search(r'DSC_(\d+)', filename)
    return int(m.group(1)) if m else None


def _detect_flags(filename: str) -> list[str]:
    return [name for name, pat in FLAG_PATTERNS.items() if pat.search(filename)]


def _blur_score(cap: cv2.VideoCapture, total_frames: int) -> float:
    mid = total_frames // 2
    cap.set(cv2.CAP_PROP_POS_FRAMES, mid)
    ret, frame = cap.read()
    if not ret:
        return 0.0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def scan_video(path: Path) -> VideoMeta:
    flags = _detect_flags(path.name)
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        return VideoMeta(
            filename=path.name,
            video_num=_extract_num(path.name),
            duration_s=0.0, fps=0.0, width=0, height=0, total_frames=0,
            blur_score=0.0, flags=flags, readable=False,
        )

    fps = cap.get(cv2.CAP_PROP_FPS) or 1.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration_s = total_frames / fps
    blur = _blur_score(cap, total_frames)
    cap.release()

    return VideoMeta(
        filename=path.name,
        video_num=_extract_num(path.name),
        duration_s=round(duration_s, 2),
        fps=round(fps, 3),
        width=width,
        height=height,
        total_frames=total_frames,
        blur_score=round(blur, 1),
        flags=flags,
        readable=True,
    )


def scan_folder(folder: Path, extensions=(".mov", ".mp4", ".mpeg")) -> list[VideoMeta]:
    paths = sorted(
        p for p in folder.iterdir()
        if p.suffix.lower() in extensions and not p.name.startswith('._')
    )
    results = []
    for i, p in enumerate(paths, 1):
        print(f"  [{i:02d}/{len(paths)}] {p.name}", flush=True)
        results.append(scan_video(p))
    return results


if __name__ == "__main__":
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/raw")
    metas = scan_folder(folder)
    total_h = sum(m.duration_s for m in metas) / 3600
    print(f"\nTotal: {len(metas)} videos — {total_h:.2f}h")
    for m in metas:
        print(f"  {m.filename}: {m.duration_s:.1f}s  {m.width}x{m.height}@{m.fps:.0f}fps  blur={m.blur_score:.0f}  flags={m.flags}")
