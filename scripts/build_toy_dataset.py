"""Build toy LSA dataset from curated raw videos + plain-text subtitles.

Reads data/lsa_raw/{videos,subtitles}/, extracts keypoints via MediaPipe,
and writes a JSON + CSV dataset compatible with the SignformerAdaptation-LSA
pipeline.

Output per entry:
  id, text, source, n_frames, feature_size, keypoints (T×1086), metadata
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from extract_keypoints import extract_keypoints, load_config  # noqa: E402

# ── Intent mapping ────────────────────────────────────────────────────────────
INTENT_MAP = {
    "Accesibilidad":       "accesibilidad",
    "Transporte":          "transporte",
    "Educación":           "educacion",
    "Educacion":           "educacion",
    "Trabajo":             "trabajo",
    "Salud":               "salud",
    "Servicios Sociales":  "servicios_sociales",
    "Vida Independiente":  "vida_independiente",
}


def _detect_intent(playlist: str) -> str:
    for key, val in INTENT_MAP.items():
        if key.lower() in playlist.lower():
            return val
    return "otro"


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text[:60]


# ── Catalog loader ────────────────────────────────────────────────────────────

def load_catalog(xlsx_path: Path) -> dict[str, dict]:
    """CATALOGO sheet → dict keyed by local_file stem."""
    df = pd.read_excel(xlsx_path, sheet_name="CATALOGO")
    catalog: dict[str, dict] = {}
    for _, row in df.iterrows():
        local_file = row.get("local_file")
        if not local_file or pd.isna(local_file):
            continue
        stem = Path(str(local_file)).stem
        catalog[stem] = {
            "yt_title": str(row.get("title", stem)),
            "playlist":  str(row.get("playlist", "")),
        }
    return catalog


# ── Per-video builder ─────────────────────────────────────────────────────────

def build_entry(
    stem: str,
    sub_path: Path,
    video_path: Path,
    catalog: dict,
    config: dict,
) -> dict:
    text = sub_path.read_text(encoding="utf-8").strip()

    meta_src = catalog.get(stem, {})
    playlist  = meta_src.get("playlist", "")
    yt_title  = meta_src.get("yt_title", stem)
    intent    = _detect_intent(playlist)
    tramite   = _slugify(yt_title)

    kp = extract_keypoints(video_path, config)

    frames  = kp["frames"]
    n       = len(frames)
    vectors = [f["vector"] for f in frames]

    def _pct(key):
        return round(sum(1 for f in frames if f[key]) / n, 3) if n else 0.0

    return {
        "id":           f"{stem}_0000",
        "text":         text,
        "source":       stem,
        "n_frames":     n,
        "feature_size": kp["feature_size"],
        "keypoints":    vectors,
        "metadata": {
            "intent":          intent,
            "tramite":         tramite,
            "playlist":        playlist,
            "yt_title":        yt_title,
            "duration_s":      round(n / kp["fps"], 2) if kp["fps"] else None,
            "fps":             kp["fps"],
            "confidence_avg":  kp["confidence_avg"],
            "pose_pct":        _pct("pose_detected"),
            "face_pct":        _pct("face_detected"),
            "left_hand_pct":   _pct("left_hand"),
            "right_hand_pct":  _pct("right_hand"),
            "word_count":      len(text.split()),
        },
    }


# ── Main ──────────────────────────────────────────────────────────────────────

CSV_FIELDS = [
    "id", "text", "intent", "tramite", "playlist", "yt_title",
    "n_frames", "duration_s", "fps", "confidence_avg",
    "pose_pct", "face_pct", "left_hand_pct", "right_hand_pct", "word_count",
]


def main():
    parser = argparse.ArgumentParser(description="Build toy LSA dataset")
    parser.add_argument("--config",      default="config.yaml")
    parser.add_argument("--lsa-raw",     default="data/lsa_raw")
    parser.add_argument("--catalog",     default="docs/raw_lsa.xlsx")
    parser.add_argument("--output",      default="data/dataset/toy_dataset.json")
    parser.add_argument("--sample-rate", type=int, default=None,
                        help="Override config dataset.sample_rate (1=every frame)")
    parser.add_argument("--limit",       type=int, default=None,
                        help="Process only first N videos (for quick testing)")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.sample_rate:
        config["dataset"]["sample_rate"] = args.sample_rate

    lsa_raw   = Path(args.lsa_raw)
    subs_dir  = lsa_raw / "subtitles"
    videos_dir = lsa_raw / "videos"

    catalog = load_catalog(Path(args.catalog))

    sub_files = sorted(subs_dir.glob("*.txt"))
    if args.limit:
        sub_files = sub_files[: args.limit]

    print(f"Subtítulos encontrados: {len(sub_files)}")

    entries, errors = [], []

    for sub_path in sub_files:
        stem = sub_path.stem
        video_path = videos_dir / f"{stem}.MOV"

        if not video_path.exists():
            print(f"  [SKIP] Sin video: {stem}")
            errors.append(stem)
            continue

        print(f"  {stem} ...", end=" ", flush=True)
        try:
            entry = build_entry(stem, sub_path, video_path, catalog, config)
            entries.append(entry)
            m = entry["metadata"]
            print(
                f"OK  frames={entry['n_frames']}  "
                f"intent={m['intent']}  "
                f"conf={m['confidence_avg']:.3f}"
            )
        except Exception as exc:
            print(f"ERROR: {exc}")
            errors.append(stem)

    # ── Save JSON ──────────────────────────────────────────────────────────────
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"\nJSON: {out}  ({len(entries)} entradas)")

    # ── Save CSV ───────────────────────────────────────────────────────────────
    csv_path = out.with_suffix(".csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for e in entries:
            writer.writerow({"id": e["id"], "text": e["text"], **e["metadata"]})
    print(f"CSV:  {csv_path}")

    # ── Summary ────────────────────────────────────────────────────────────────
    if entries:
        print("\n─── Resumen ───────────────────────────────────────")
        intents: dict[str, int] = {}
        for e in entries:
            k = e["metadata"]["intent"]
            intents[k] = intents.get(k, 0) + 1
        for intent, n in sorted(intents.items()):
            print(f"  {intent:<25} {n}")
        avg_conf    = sum(e["metadata"]["confidence_avg"] for e in entries) / len(entries)
        total_frames = sum(e["n_frames"] for e in entries)
        total_words  = sum(e["metadata"]["word_count"] for e in entries)
        print(f"\n  Confidence avg:  {avg_conf:.3f}")
        print(f"  Total frames:    {total_frames:,}")
        print(f"  Total words:     {total_words}")
        print(f"  Feature size:    {entries[0]['feature_size']}")

    if errors:
        print(f"\nErrores/skipped ({len(errors)}): {errors}")


if __name__ == "__main__":
    main()
