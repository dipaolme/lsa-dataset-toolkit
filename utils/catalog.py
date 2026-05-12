"""
catalog.py — Utilidades de gestión de catálogo y archivos del proyecto.

Índice:
  move_matched_videos(csv, src_dir, dst_dir) — copia MOV con match YT, opcionalmente
    convierte a MP4 y agrupa por playlist
"""

import re
import shutil
import sys
from pathlib import Path

# Asegurar que el root del proyecto esté en el path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd


def _normalize(s: str) -> str:
    """Minúsculas sin acentos para comparación tolerante."""
    import unicodedata
    return ''.join(
        c for c in unicodedata.normalize('NFKD', s.lower())
        if unicodedata.category(c) != 'Mn'
    )


def _resolve_unicode_path(path: Path) -> Path | None:
    """Resuelve un path tolerando diferencias de normalización Unicode.
    Primero intenta el path directo; si no existe, busca parte por parte
    con matching sin acentos (útil cuando la shell envía NFD y el fs tiene NFC)."""
    import unicodedata
    path = Path(unicodedata.normalize('NFC', str(path)))
    if path.exists():
        return path
    # Reconstruir parte por parte desde la raíz
    parts = path.parts
    current = Path(parts[0])
    for part in parts[1:]:
        if not current.exists():
            return None
        norm_part = _normalize(part)
        candidates = [p for p in current.iterdir()
                      if _normalize(p.name) == norm_part]
        if not candidates:
            return None
        current = candidates[0]
    return current if current.exists() else None


def move_matched_videos(
    csv_path: Path,
    src_dir: Path,
    dst_dir: Path,
    copy: bool = False,
    overwrite: bool = False,
    by_playlist: bool = False,
    convert_mp4: bool = False,
) -> dict:
    """
    Copia o mueve los MOV locales que tienen match con YouTube y opcionalmente
    los convierte a MP4 (sin re-encodear) para reproducción en Windows.

    Args:
        csv_path:    CSV de matching (yt_vs_local_matching.csv).
        src_dir:     Carpeta origen con los MOV.
        dst_dir:     Carpeta destino.
        copy:        Si True, copia en lugar de mover.
        overwrite:   Si True, sobreescribe archivos existentes.
        by_playlist: Si True, crea una subcarpeta por playlist.
        convert_mp4: Si True, convierte cada MOV a MP4 después de copiarlo.
                     El MOV copiado se elimina tras la conversión exitosa.

    Returns:
        Dict con claves 'ok', 'skipped', 'error'.
    """
    from utils.video import convert_mov_to_mp4

    csv_path = Path(csv_path)
    dst_dir  = Path(dst_dir)

    src_dir = _resolve_unicode_path(Path(src_dir))
    if src_dir is None:
        print(f"[ERROR] No se encontró la carpeta origen.")
        return {"ok": [], "skipped": [], "error": []}

    df = pd.read_csv(csv_path)
    matched = df[df['match'] == 'OK'].dropna(subset=['local_file'])

    if matched.empty:
        print("No hay archivos con match OK en el CSV.")
        return {"ok": [], "skipped": [], "error": []}

    action = shutil.copy2 if copy else shutil.move
    results = {"ok": [], "skipped": [], "error": []}

    suffix = " + conversión MP4" if convert_mp4 else ""
    print(f"Procesando {len(matched)} archivos → {dst_dir}/{suffix}")

    for i, row in enumerate(matched.itertuples(), 1):
        # Usar solo la parte temática del nombre: "Guía ... | Salud" → "Salud"
        pl_raw  = row.playlist.split('|')[-1].strip() if '|' in row.playlist else row.playlist
        pl_name = re.sub(r'[<>:"/\\?*]', '_', pl_raw).strip()
        target_dir = (dst_dir / pl_name) if by_playlist else dst_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        src      = src_dir / row.local_file
        dst_mov  = target_dir / row.local_file
        dst_mp4  = target_dir / (Path(row.local_file).stem + '.mp4')
        final    = dst_mp4 if convert_mp4 else dst_mov

        label = f"[{i:02d}/{len(matched)}] {row.local_file[:40]}"
        if by_playlist:
            label += f"  [{pl_name[:25]}]"
        print(f"  {label}", end=" ... ", flush=True)

        if not src.exists():
            print("no encontrado")
            results["error"].append(row.local_file)
            continue
        if final.exists() and not overwrite:
            print("skip")
            results["skipped"].append(row.local_file)
            continue

        # Copiar / mover el MOV
        try:
            action(str(src), str(dst_mov))
        except Exception as e:
            print(f"ERROR copia: {e}")
            results["error"].append(row.local_file)
            continue

        # Convertir a MP4 si se pidió
        if convert_mp4:
            ok = convert_mov_to_mp4(dst_mov, dst_mp4, overwrite=overwrite)
            if ok:
                dst_mov.unlink()  # elimina el MOV intermedio
                print("ok (mp4)")
            else:
                print("ERROR conversión")
                results["error"].append(row.local_file)
                continue
        else:
            print("ok")

        results["ok"].append(row.local_file)

    print(f"\nTotal: {len(results['ok'])} ok, "
          f"{len(results['skipped'])} skipped, "
          f"{len(results['error'])} errores")
    return results


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gestión de catálogo lsa-dataset-toolkit")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("move-matched", help="Copiar/mover MOV con match YT")
    p.add_argument("--csv",         required=True, help="CSV de matching")
    p.add_argument("--src",         required=True, help="Carpeta origen con los MOV")
    p.add_argument("--dst",         required=True, help="Carpeta destino")
    p.add_argument("--copy",        action="store_true", help="Copiar en lugar de mover")
    p.add_argument("--by-playlist", action="store_true", help="Subcarpeta por playlist")
    p.add_argument("--convert-mp4", action="store_true", help="Convertir a MP4 al final")
    p.add_argument("--overwrite",   action="store_true")

    args = parser.parse_args()

    if args.cmd == "move-matched":
        move_matched_videos(
            csv_path    = args.csv,
            src_dir     = args.src,
            dst_dir     = args.dst,
            copy        = args.copy,
            by_playlist = args.by_playlist,
            convert_mp4 = args.convert_mp4,
            overwrite   = args.overwrite,
        )
    else:
        parser.print_help()
