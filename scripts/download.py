"""Download videos and subtitles from YouTube using yt-dlp."""
import argparse
import subprocess
import yaml
from pathlib import Path


def load_config(config_path="config.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)


def download_video(url: str, config: dict, output_dir: Path = None):
    cfg = config["download"]
    raw_dir = output_dir or Path(config["paths"]["raw"])
    subs_dir = Path(config["paths"]["subtitles"])
    raw_dir.mkdir(parents=True, exist_ok=True)
    subs_dir.mkdir(parents=True, exist_ok=True)

    langs = ",".join(cfg["subtitle_langs"])
    cmd = [
        "yt-dlp",
        "--format", cfg["format"],
        "--write-subs",
        "--sub-langs", langs,
        "--convert-subs", "srt",
        "--output", str(raw_dir / "%(id)s.%(ext)s"),
        "--write-info-json",
    ]
    if cfg.get("write_auto_subs"):
        cmd.append("--write-auto-subs")

    cmd.append(url)
    subprocess.run(cmd, check=True)

    # Move generated .srt files to subtitles/
    for srt in raw_dir.glob("*.srt"):
        srt.rename(subs_dir / srt.name)

    print(f"Done. Video in {raw_dir}, subtitles in {subs_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube video + subtitles")
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    download_video(args.url, config)
