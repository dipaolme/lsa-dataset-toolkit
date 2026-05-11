"""
match_videos.py — Matching de videos locales contra YouTube con TF-IDF.

Lee catálogo, OCR y DOCX, corre el matcher y exporta CSV.

Uso:
  python scripts/match_videos.py
  python scripts/match_videos.py --ocr data/catalog/yt_ocr.json
  python scripts/match_videos.py --dur-threshold 0.55 --score-threshold 0.20
"""

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import yaml
from scripts.analyze_raw import scan_folder
from scripts.fetch_channel_catalog import load_catalog
from utils.docx_parser import parse_subs_docx
from utils.matching import match_videos
from utils.ocr import load_ocr


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Match videos locales ↔ YouTube con TF-IDF")
    parser.add_argument("--config",          default="config.yaml")
    parser.add_argument("--ocr",             default=None, help="Path a yt_ocr.json")
    parser.add_argument("--output",          default=None, help="Path CSV de salida")
    parser.add_argument("--dur-threshold",   type=float, default=0.60)
    parser.add_argument("--score-threshold", type=float, default=0.25)
    args = parser.parse_args()

    config = load_config(args.config)
    catalog_path = Path(config["catalog"]["path"])
    ocr_path     = Path(args.ocr or catalog_path / "yt_ocr.json")
    output_path  = Path(args.output or catalog_path / "yt_vs_local_matching.csv")
    docx_path    = Path(config["paths"]["subs_docx"])
    videos_dir   = Path(config["paths"]["videos"])

    # Catálogo YouTube
    catalog  = load_catalog(config)
    yt_videos = [
        {**v, "playlist_title": pl["playlist_title"]}
        for pl in catalog["playlists"]
        for v in pl["videos"]
    ]
    print(f"YouTube videos: {len(yt_videos)}")

    # Videos locales
    local_metas = scan_folder(videos_dir)
    local       = [m for m in local_metas if m.readable]
    print(f"MOV locales:    {len(local)}")

    # DOCX
    docx_subs: dict[int, str] = {}
    if docx_path.exists():
        subs = parse_subs_docx(docx_path)
        docx_subs = {s.video_num: s.text for s in subs}
        print(f"Entradas DOCX:  {len(docx_subs)}")
    else:
        print(f"[warn] DOCX no encontrado: {docx_path}")

    # OCR
    ocr_data = load_ocr(ocr_path)
    n_ocr    = sum(1 for v in ocr_data.values() if v.get("full_text"))
    print(f"Videos con OCR: {n_ocr}/{len(yt_videos)}")
    print()

    # Matching
    results = match_videos(
        local_metas    = local_metas,
        yt_videos      = yt_videos,
        docx_subs      = docx_subs,
        ocr_data       = ocr_data,
        dur_threshold  = args.dur_threshold,
        score_threshold= args.score_threshold,
    )

    # Guardar CSV
    ok  = [r for r in results if r["match"] == "OK"]
    nm  = [r for r in results if r["match"] == "SIN MATCH"]
    matched_local = {r["local_file"] for r in ok}
    unmatched_local = [m for m in local if m.filename not in matched_local]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "yt_id", "yt_title", "yt_dur_s", "playlist", "yt_topic",
        "local_file", "local_dur_s", "local_topic", "has_sub",
        "dur_score", "tfidf_score", "score", "match",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sorted(results, key=lambda r: (-int(r["match"] == "OK"), -r["score"])))

    print(f"YouTube con match:    {len(ok)}")
    print(f"YouTube sin match:    {len(nm)}")
    print(f"MOV sin match:        {len(unmatched_local)}")
    print(f"\nGuardado: {output_path}")

    if unmatched_local:
        print("\nMOV locales sin match:")
        for m in unmatched_local:
            print(f"  {m.filename[:55]:55s}  {m.duration_s:.1f}s")


if __name__ == "__main__":
    main()
