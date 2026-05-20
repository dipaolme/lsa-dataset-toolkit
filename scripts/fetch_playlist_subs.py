"""
fetch_playlist_subs.py — Descarga subtítulos de una playlist de YouTube.

Usa yt-dlp con --skip-download: baja solo los .srt, sin video.
Prioriza subtítulos manuales; cae a auto-generados si no hay manuales.

Uso:
    python scripts/fetch_playlist_subs.py <playlist_url>
    python scripts/fetch_playlist_subs.py <playlist_url> --output data/legislatura/subtitles/
    python scripts/fetch_playlist_subs.py <playlist_url> --no-auto-subs
"""

import argparse
import subprocess
import sys
from pathlib import Path

_YTDLP = str(Path(__file__).parent.parent / ".venv/bin/yt-dlp")


def fetch_subs(url: str, output_dir: Path, auto_subs: bool = True, langs: str = "es,es-419"):
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        _YTDLP,
        "--skip-download",
        "--write-subs",
        "--sub-langs", langs,
        "--output", str(output_dir / "%(title)s.%(ext)s"),
        "--no-warnings",
    ]
    if auto_subs:
        cmd.append("--write-auto-subs")

    cmd.append(url)

    print(f"Descargando subtítulos de: {url}")
    print(f"Destino: {output_dir}")
    print(f"Auto-subs: {'sí' if auto_subs else 'no'}")
    print()

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("Error en yt-dlp. Verificá que la URL sea accesible y que yt-dlp esté instalado.")
        sys.exit(1)

    srt_files = sorted(output_dir.glob("*.srt"))
    print(f"\nArchivos descargados: {len(srt_files)}")
    for f in srt_files:
        print(f"  {f.name}")


def main():
    parser = argparse.ArgumentParser(description="Descarga subtítulos de playlist YouTube")
    parser.add_argument("url", help="URL de playlist o video de YouTube")
    parser.add_argument(
        "--output", "-o",
        default="data/lsa_raw/subtitles",
        help="Directorio de salida (default: data/lsa_raw/subtitles)",
    )
    parser.add_argument(
        "--no-auto-subs",
        action="store_true",
        help="No descargar subtítulos auto-generados (solo manuales)",
    )
    parser.add_argument(
        "--langs",
        default="es,es-419",
        help="Idiomas de subtítulos (default: es,es-419)",
    )
    args = parser.parse_args()

    fetch_subs(
        url=args.url,
        output_dir=Path(args.output),
        auto_subs=not args.no_auto_subs,
        langs=args.langs,
    )


if __name__ == "__main__":
    main()
