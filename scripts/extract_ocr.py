"""
extract_ocr.py — Extracción batch de OCR desde videos YouTube.

Procesa todos los videos del catálogo y guarda el resultado en yt_ocr.json.
Soporta resumir: los videos ya procesados se saltean.

Uso:
  python scripts/extract_ocr.py
  python scripts/extract_ocr.py --interval 3.0
  python scripts/extract_ocr.py --video VIDEO_ID       # un solo video
  python scripts/extract_ocr.py --no-resume            # reprocesar todo
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import yaml
from utils.ocr import extract_ocr_video, load_ocr, save_ocr


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def load_catalog(catalog_path: Path) -> list[dict]:
    """Devuelve lista plana de videos desde channel_catalog.json."""
    with open(catalog_path, encoding="utf-8") as f:
        catalog = json.load(f)
    videos = []
    for pl in catalog.get("playlists", []):
        for v in pl.get("videos", []):
            videos.append({**v, "playlist_title": pl["playlist_title"]})
    return videos


def main():
    parser = argparse.ArgumentParser(description="Batch OCR de videos YouTube → yt_ocr.json")
    parser.add_argument("--config",    default="config.yaml")
    parser.add_argument("--catalog",   default=None, help="Path al channel_catalog.json")
    parser.add_argument("--output",    default=None, help="Path de salida yt_ocr.json")
    parser.add_argument("--interval",  type=float, default=2.0,
                        help="Segundos entre frames muestreados (default: 2.0)")
    parser.add_argument("--video",     default=None, help="Procesar solo este video_id")
    parser.add_argument("--no-resume", action="store_true",
                        help="Reprocesar incluso videos ya en el JSON")
    args = parser.parse_args()

    config = load_config(args.config)
    catalog_path = Path(args.catalog or config["catalog"]["path"]) / "channel_catalog.json"
    output_path  = Path(args.output  or config["catalog"]["path"]) / "yt_ocr.json"

    if not catalog_path.exists():
        print(f"[ERROR] No se encontró el catálogo: {catalog_path}")
        sys.exit(1)

    videos = load_catalog(catalog_path)

    if args.video:
        videos = [v for v in videos if v["video_id"] == args.video]
        if not videos:
            print(f"[ERROR] Video no encontrado en catálogo: {args.video}")
            sys.exit(1)

    ocr_data = {} if args.no_resume else load_ocr(output_path)
    pending  = [v for v in videos if v["video_id"] not in ocr_data]

    print(f"Videos en catálogo:  {len(videos)}")
    print(f"Ya procesados:       {len(ocr_data)}")
    print(f"Por procesar:        {len(pending)}")
    print(f"Intervalo de frames: {args.interval}s")
    print()

    for idx, video in enumerate(pending, 1):
        vid   = video["video_id"]
        title = video.get("title", vid)
        url   = video.get("url", f"https://www.youtube.com/watch?v={vid}")

        print(f"[{idx:02d}/{len(pending)}] {title[:60]}", end=" ... ", flush=True)

        result = extract_ocr_video(url, config, interval_sec=args.interval)

        ocr_data[vid] = {
            "video_id":     vid,
            "title":        title,
            "playlist":     video.get("playlist_title", ""),
            "url":          url,
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            **result,
        }

        status = result["status"]
        n_seg  = len(result.get("segments", []))
        words  = len(result.get("full_text", "").split())
        print(f"{status}  ({n_seg} segmentos, {words} palabras)")

        # Guardado incremental — permite resumir si se interrumpe
        save_ocr(ocr_data, output_path)

    print(f"\nGuardado: {output_path}  ({len(ocr_data)} videos)")


if __name__ == "__main__":
    main()
