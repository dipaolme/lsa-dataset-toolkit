"""
utils.py — Utilidades generales del proyecto lsa-dataset-toolkit.

Cada función resuelve una tarea concreta del pipeline LSA.
Todas son importables desde notebooks y scripts, y ejecutables como CLI.

Índice:
  VIDEO
    convert_mov_to_mp4(src, dst)          — remux MOV → MP4 sin re-encodear
    batch_convert_folder(folder, out_dir) — convierte todos los MOV de una carpeta
"""

import subprocess
import sys
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# VIDEO
# ──────────────────────────────────────────────────────────────────────────────

def convert_mov_to_mp4(src: Path, dst: Path, overwrite: bool = False) -> bool:
    """
    Remuxea un archivo MOV a MP4 sin re-encodear (copia de streams).

    Por qué: los MOV de cámara Nikon (H.264 + PCM) no se reproducen en
    reproductores de Windows aunque el codec sea compatible. Cambiar el
    contenedor a MP4 resuelve el problema sin pérdida de calidad ni tiempo
    de procesamiento significativo.

    Args:
        src:       Ruta al archivo .MOV de entrada.
        dst:       Ruta al archivo .mp4 de salida.
        overwrite: Si True, sobreescribe el destino si ya existe.

    Returns:
        True si la conversión fue exitosa, False si hubo error.
    """
    src, dst = Path(src), Path(dst)
    if not src.exists():
        print(f"  [ERROR] No existe: {src}")
        return False
    if dst.exists() and not overwrite:
        print(f"  [SKIP]  Ya existe: {dst.name}")
        return True

    dst.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-c", "copy", str(dst)],
        capture_output=True,
    )
    if result.returncode != 0:
        print(f"  [ERROR] {src.name}: {result.stderr.decode()[-200:]}")
        return False
    return True


def batch_convert_folder(
    folder: Path,
    out_dir: Path,
    extensions: tuple = (".mov",),
    overwrite: bool = False,
) -> dict:
    """
    Convierte todos los archivos de video de una carpeta a MP4.

    Útil para hacer reproducibles en Windows los MOV crudos de cámara
    sin mover ni modificar los originales.

    Args:
        folder:     Carpeta con los archivos fuente.
        out_dir:    Carpeta de destino para los MP4 generados.
        extensions: Extensiones a procesar (default: .mov).
        overwrite:  Si True, sobreescribe archivos existentes.

    Returns:
        Dict con claves 'ok', 'skipped', 'error' y listas de nombres.
    """
    folder, out_dir = Path(folder), Path(out_dir)
    files = sorted(
        p for p in folder.iterdir()
        if p.suffix.lower() in extensions and not p.name.startswith("._")
    )

    results = {"ok": [], "skipped": [], "error": []}

    for i, src in enumerate(files, 1):
        dst = out_dir / (src.stem + ".mp4")
        print(f"[{i:02d}/{len(files)}] {src.name}", end=" ... ", flush=True)

        if dst.exists() and not overwrite:
            print("skip")
            results["skipped"].append(src.name)
            continue

        ok = convert_mov_to_mp4(src, dst, overwrite=overwrite)
        if ok:
            print("ok")
            results["ok"].append(src.name)
        else:
            results["error"].append(src.name)

    print(f"\nTotal: {len(results['ok'])} ok, "
          f"{len(results['skipped'])} skipped, "
          f"{len(results['error'])} errores")
    return results


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Utilidades lsa-dataset-toolkit")
    sub = parser.add_subparsers(dest="cmd")

    p_conv = sub.add_parser("convert", help="Convertir MOV → MP4")
    p_conv.add_argument("input",  help="Archivo .MOV o carpeta con MOVs")
    p_conv.add_argument("output", help="Archivo .mp4 destino o carpeta destino")
    p_conv.add_argument("--overwrite", action="store_true")

    args = parser.parse_args()

    if args.cmd == "convert":
        src = Path(args.input)
        dst = Path(args.output)
        if src.is_dir():
            batch_convert_folder(src, dst, overwrite=args.overwrite)
        else:
            ok = convert_mov_to_mp4(src, dst, overwrite=args.overwrite)
            sys.exit(0 if ok else 1)
    else:
        parser.print_help()
