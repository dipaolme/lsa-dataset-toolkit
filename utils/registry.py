"""
registry.py — Registro centralizado del estado del pipeline por video.

Cada video matcheado tiene una entrada que se va completando a medida que
avanza el pipeline: matching → subtítulos → keypoints → dataset.

Uso típico:
    from utils.registry import load_registry, save_registry, build_registry

    reg = load_registry()           # carga data/catalog/video_registry.json
    reg["DSC_0873"]["sync_ok"] = True
    save_registry(reg)
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd

REGISTRY_PATH = Path("data/catalog/video_registry.json")


# ──────────────────────────────────────────────────────────────────────────────
# Estructura de una entrada vacía
# ──────────────────────────────────────────────────────────────────────────────

def _empty_entry() -> dict:
    return {
        # — Matching ——————————————————————————————————————————
        "yt_id":          None,
        "yt_title":       None,
        "playlist":       None,
        "local_file":     None,   # nombre original del MOV/MP4
        "video_path":     None,   # ruta relativa al MP4 en matched_videos/
        "match_score":    None,
        "dur_score":      None,
        "kw_score":       None,
        "has_docx_sub":   False,  # True si tiene entrada en Guia Subs.docx
        # — Revisión manual ——————————————————————————————————
        "review_status":  "pending",   # pending | ok | rejected | corrected
        "review_notes":   "",
        # — Subtítulos ————————————————————————————————————————
        "sub_srt":        None,   # ruta relativa al .srt generado
        "sub_source":     None,   # "ocr" | "ocr_docx" | "expert"
        "n_sub_segments": None,
        "ocr_confidence": None,
        "docx_match_ratio": None,
        "sync_ok":        None,
        # — Keypoints —————————————————————————————————————————
        "keypoints_json":       None,   # ruta relativa al .json
        "n_keypoint_frames":    None,
        "confidence_avg":       None,
        # — Dataset ———————————————————————————————————————————
        "dataset_entries": None,  # n° de entradas en el dataset final
    }


# ──────────────────────────────────────────────────────────────────────────────
# Construcción desde cero
# ──────────────────────────────────────────────────────────────────────────────

def _video_stem(filename: str) -> str:
    """DSC_XXXX... → clave del registro (sin extensión)."""
    return Path(filename).stem


def build_registry(
    csv_path: Path = Path("data/catalog/yt_vs_local_matching.csv"),
    videos_dir: Path = Path("data/raw/matched_videos"),
) -> dict:
    """
    Construye el registro desde el CSV de matching y los MP4 en matched_videos/.

    Sólo incluye videos con match='OK'. Detecta automáticamente la ruta del MP4
    buscando por stem dentro de las subcarpetas de playlist.

    Returns:
        Dict keyed by video stem (e.g. "DSC_0873 p.87 ...").
    """
    df = pd.read_csv(csv_path)
    matched = df[df["match"] == "OK"].copy()

    # Índice stem → ruta real del MP4 en matched_videos/
    mp4_by_stem: dict[str, Path] = {}
    for mp4 in sorted(videos_dir.rglob("*.mp4")):
        mp4_by_stem[mp4.stem] = mp4

    registry: dict[str, dict] = {}

    for row in matched.itertuples(index=False):
        stem = _video_stem(row.local_file)
        entry = _empty_entry()

        entry["yt_id"]        = row.yt_id
        entry["yt_title"]     = row.yt_title
        entry["playlist"]     = row.playlist.split("|")[-1].strip() if "|" in row.playlist else row.playlist
        entry["local_file"]   = row.local_file
        entry["match_score"]  = float(row.score)
        entry["dur_score"]    = float(row.dur_score)
        entry["kw_score"]     = float(row.kw_score)
        entry["has_docx_sub"] = str(row.has_sub).strip().lower() == "true"

        if stem in mp4_by_stem:
            entry["video_path"] = str(mp4_by_stem[stem].as_posix())

        registry[stem] = entry

    return registry


# ──────────────────────────────────────────────────────────────────────────────
# Carga / guardado
# ──────────────────────────────────────────────────────────────────────────────

def load_registry(path: Path = REGISTRY_PATH) -> dict:
    """Carga el registro desde JSON. Si no existe, lo construye desde cero."""
    path = Path(path)
    if not path.exists():
        print(f"[registry] No encontrado en {path} — construyendo desde CSV...")
        reg = build_registry()
        save_registry(reg, path)
        return reg
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_registry(registry: dict, path: Path = REGISTRY_PATH) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    print(f"[registry] Guardado: {path}  ({len(registry)} videos)")


# ──────────────────────────────────────────────────────────────────────────────
# Helpers de actualización
# ──────────────────────────────────────────────────────────────────────────────

def update_entry(registry: dict, stem: str, **kwargs) -> None:
    """Actualiza campos de una entrada. Ignora claves que no existan."""
    if stem not in registry:
        raise KeyError(f"Video no encontrado en registro: {stem!r}")
    for k, v in kwargs.items():
        if k in registry[stem]:
            registry[stem][k] = v
        else:
            raise KeyError(f"Campo desconocido: {k!r}  (video={stem!r})")


def summary(registry: dict) -> None:
    """Imprime un resumen del estado del pipeline."""
    total = len(registry)

    def _count(key, val=None):
        if val is None:
            return sum(1 for e in registry.values() if e.get(key) is not None)
        return sum(1 for e in registry.values() if e.get(key) == val)

    print(f"Videos en registro: {total}")
    print()
    print("Matching / revisión")
    print(f"  review_status=ok        {_count('review_status', 'ok'):3d}")
    print(f"  review_status=pending   {_count('review_status', 'pending'):3d}")
    print(f"  review_status=rejected  {_count('review_status', 'rejected'):3d}")
    print(f"  has_docx_sub=True       {_count('has_docx_sub', True):3d}")
    print()
    print("Subtítulos")
    print(f"  sub_srt presente        {_count('sub_srt'):3d}")
    print(f"  sync_ok=True            {_count('sync_ok', True):3d}")
    print(f"  sync_ok=False           {_count('sync_ok', False):3d}")
    print()
    print("Keypoints")
    print(f"  keypoints_json presente {_count('keypoints_json'):3d}")
    print()
    print("Dataset")
    print(f"  dataset_entries presente {_count('dataset_entries'):3d}")


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gestión del registro de videos")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("build",   help="Construir registro desde CSV (sobreescribe)")
    sub.add_parser("summary", help="Mostrar resumen del estado del pipeline")

    p_show = sub.add_parser("show", help="Mostrar entrada de un video")
    p_show.add_argument("stem", help="Stem del video (ej: 'DSC_0873 p.87 ...')")

    args = parser.parse_args()

    if args.cmd == "build":
        reg = build_registry()
        save_registry(reg)

    elif args.cmd == "summary":
        reg = load_registry()
        summary(reg)

    elif args.cmd == "show":
        reg = load_registry()
        if args.stem in reg:
            print(json.dumps(reg[args.stem], ensure_ascii=False, indent=2))
        else:
            print(f"No encontrado: {args.stem!r}")
            print("Stems disponibles:")
            for s in sorted(reg):
                print(f"  {s}")
    else:
        parser.print_help()
