"""
subtitles.py — Utilidades de subtítulos del proyecto lsa-dataset-toolkit.

Índice:
  export_matched_subs(csv, docx, dst_dir) — exporta un .txt por video matcheado,
    organizado por playlist, con el texto del subtítulo del DOCX
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

import pandas as pd
from parse_subs_docx import parse_subs_docx


def export_matched_subs(
    csv_path: Path,
    docx_path: Path,
    dst_dir: Path,
    by_playlist: bool = False,
    overwrite: bool = False,
) -> dict:
    """
    Exporta un archivo .txt por cada video matcheado que tenga subtítulo en el DOCX.

    El nombre del .txt es el mismo stem que el MOV (ej: DSC_0795 Sin rta si.txt).
    Si by_playlist=True, replica la misma estructura de carpetas que los videos.

    Args:
        csv_path:    CSV de matching (yt_vs_local_matching.csv).
        docx_path:   Ruta al Guia Subs.docx.
        dst_dir:     Carpeta destino para los .txt.
        by_playlist: Si True, crea subcarpeta por playlist.
        overwrite:   Si True, sobreescribe archivos existentes.

    Returns:
        Dict con claves 'ok', 'skipped', 'sin_sub', 'error'.
    """
    csv_path  = Path(csv_path)
    docx_path = Path(docx_path)
    dst_dir   = Path(dst_dir)

    df      = pd.read_csv(csv_path)
    matched = df[df['match'] == 'OK'].dropna(subset=['local_file'])

    subs       = parse_subs_docx(docx_path)
    sub_by_num = {s.video_num: s for s in subs}

    # Extraer número de video del nombre de archivo (DSC_XXXX)
    def video_num(filename):
        m = re.search(r'DSC_(\d+)', filename)
        return int(m.group(1)) if m else None

    results = {'ok': [], 'skipped': [], 'sin_sub': [], 'error': []}

    print(f"Exportando subtítulos para {len(matched)} videos → {dst_dir}/")

    for i, row in enumerate(matched.itertuples(), 1):
        num = video_num(row.local_file)
        sub = sub_by_num.get(num)

        if by_playlist:
            pl_name    = row.playlist.split('|')[-1].strip() if '|' in row.playlist else row.playlist
            pl_name    = re.sub(r'[<>:"/\\?*]', '_', pl_name).strip()
            target_dir = dst_dir / pl_name
        else:
            target_dir = dst_dir

        target_dir.mkdir(parents=True, exist_ok=True)

        stem    = Path(row.local_file).stem
        out     = target_dir / f"{stem}.txt"

        label = f"[{i:02d}/{len(matched)}] {stem[:45]}"
        print(f"  {label}", end=" ... ", flush=True)

        if sub is None:
            print("sin subtítulo en DOCX")
            results['sin_sub'].append(row.local_file)
            continue
        if out.exists() and not overwrite:
            print("skip")
            results['skipped'].append(row.local_file)
            continue

        try:
            content = f"N° {num}\n"
            if sub.note:
                content += f"Nota: {sub.note}\n"
            content += f"\n{sub.text}\n"
            out.write_text(content, encoding='utf-8')
            print("ok")
            results['ok'].append(row.local_file)
        except Exception as e:
            print(f"ERROR: {e}")
            results['error'].append(row.local_file)

    print(f"\nTotal: {len(results['ok'])} ok, "
          f"{len(results['skipped'])} skipped, "
          f"{len(results['sin_sub'])} sin subtítulo, "
          f"{len(results['error'])} errores")
    return results


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Utilidades de subtítulos lsa-dataset-toolkit")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("export-subs", help="Exportar .txt de subtítulos para videos matcheados")
    p.add_argument("--csv",         required=True, help="CSV de matching")
    p.add_argument("--docx",        required=True, help="Ruta al Guia Subs.docx")
    p.add_argument("--dst",         required=True, help="Carpeta destino")
    p.add_argument("--by-playlist", action="store_true", help="Subcarpeta por playlist")
    p.add_argument("--overwrite",   action="store_true")

    args = parser.parse_args()

    if args.cmd == "export-subs":
        export_matched_subs(
            csv_path    = args.csv,
            docx_path   = args.docx,
            dst_dir     = args.dst,
            by_playlist = args.by_playlist,
            overwrite   = args.overwrite,
        )
    else:
        parser.print_help()
