"""
Copia los videos matcheados y los subtítulos a la carpeta raw_lsa en SharePoint.

Estructura de destino:
  raw_lsa/
    videos/     ← MOV originales de los 49 videos matcheados
    subtitles/  ← .txt de los 29 videos con subtítulo DOCX

Uso:
    python scripts/export_raw_lsa.py [--dry-run]
"""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent

SRC_VIDEOS = Path(
    "/mnt/c/Users/mdp_e/Gobierno de la Ciudad de Buenos Aires"
    "/grupo_DG Inclusión Digital - Documents/02-Proyectos/08-Avatar AI"
    "/Material LSA/GUÍA INFO LSA 2018-2019/videos"
)
DEST_BASE = Path(
    "/mnt/c/Users/mdp_e/Gobierno de la Ciudad de Buenos Aires"
    "/grupo_DG Inclusión Digital - Documents/02-Proyectos/08-Avatar AI"
    "/raw_lsa"
)
DEST_VIDEOS = DEST_BASE / "videos"
DEST_SUBS = DEST_BASE / "subtitles"

REGISTRY_PATH = ROOT / "data/catalog/video_registry.json"
SUBTITLES_DIR = ROOT / "data/subtitles"


def export(dry_run: bool):
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    if not dry_run:
        DEST_VIDEOS.mkdir(parents=True, exist_ok=True)
        DEST_SUBS.mkdir(parents=True, exist_ok=True)

    print(f"{'[DRY RUN] ' if dry_run else ''}Destino: {DEST_BASE}\n")

    # ── videos ────────────────────────────────────────────────────────────────
    print(f"[videos] {len(registry)} entradas en registry")
    ok = missing = skipped = 0

    for stem in registry:
        src = SRC_VIDEOS / f"{stem}.MOV"
        dest = DEST_VIDEOS / src.name

        if not src.exists():
            print(f"  FALTA   {src.name}")
            missing += 1
            continue

        if dest.exists():
            skipped += 1
            continue

        if not dry_run:
            shutil.copy2(src, dest)
        print(f"  {'SIMULAR' if dry_run else 'COPIADO'}  {src.name}")
        ok += 1

    print(f"  → copiados={ok}  ya existían={skipped}  faltaban={missing}\n")

    # ── subtítulos ────────────────────────────────────────────────────────────
    txt_files = sorted(SUBTITLES_DIR.glob("*.txt"))
    print(f"[subtitulos] {len(txt_files)} archivos .txt")
    ok_s = skipped_s = 0

    for txt in txt_files:
        dest = DEST_SUBS / txt.name
        if dest.exists():
            skipped_s += 1
            continue
        if not dry_run:
            shutil.copy2(txt, dest)
        print(f"  {'SIMULAR' if dry_run else 'COPIADO'}  {txt.name}")
        ok_s += 1

    print(f"  → copiados={ok_s}  ya existían={skipped_s}")


def main():
    parser = argparse.ArgumentParser(description="Exporta videos y subtítulos a raw_lsa en SharePoint")
    parser.add_argument("--dry-run", action="store_true", help="Muestra qué se copiaría sin hacer nada")
    args = parser.parse_args()
    export(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
