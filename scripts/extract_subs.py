"""Parse subtitle files (SRT/VTT) and detect hardcoded subtitles via OCR."""
import argparse
from pathlib import Path
from dataclasses import dataclass

import pysrt
import webvtt
import yaml


@dataclass
class SubSegment:
    index: int
    start: float   # seconds
    end: float     # seconds
    text: str


def parse_srt(path: Path) -> list[SubSegment]:
    subs = pysrt.open(str(path))
    return [
        SubSegment(i, _ts_to_sec(s.start), _ts_to_sec(s.end), s.text.strip())
        for i, s in enumerate(subs)
    ]


def parse_vtt(path: Path) -> list[SubSegment]:
    segments = []
    for i, caption in enumerate(webvtt.read(str(path))):
        segments.append(SubSegment(
            index=i,
            start=caption.start_in_seconds,
            end=caption.end_in_seconds,
            text=caption.text.strip(),
        ))
    return segments


def load_subtitles(path: Path) -> list[SubSegment]:
    ext = path.suffix.lower()
    if ext == ".srt":
        return parse_srt(path)
    elif ext in (".vtt", ".webvtt"):
        return parse_vtt(path)
    raise ValueError(f"Unsupported subtitle format: {ext}")


def _ts_to_sec(ts) -> float:
    return ts.hours * 3600 + ts.minutes * 60 + ts.seconds + ts.milliseconds / 1000


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse subtitle file")
    parser.add_argument("path", help="Path to .srt or .vtt file")
    args = parser.parse_args()

    segs = load_subtitles(Path(args.path))
    for s in segs[:10]:
        print(f"[{s.start:.2f}s - {s.end:.2f}s] {s.text}")
    print(f"\nTotal segments: {len(segs)}")
