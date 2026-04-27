"""Fetch metadata for all playlists and videos in a YouTube channel."""
import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


def load_config(config_path="config.yaml"):
    with open(config_path) as f:
        return yaml.safe_load(f)


def _yt_dlp_flat_json(url: str) -> dict:
    """Run yt-dlp --flat-playlist --dump-single-json on a URL (fast, basic fields only)."""
    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--dump-single-json", "--no-warnings", url],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp error:\n{result.stderr.strip()}")
    return json.loads(result.stdout)


def _yt_dlp_full_metadata(url: str) -> dict[str, dict]:
    """
    Fetch complete video metadata for all videos in a playlist URL.
    Slower than flat mode (one request per video) but returns fps/height/width.
    Returns a dict keyed by video_id.
    """
    print("  Fetching full metadata (fps/resolution) — this may take a while...")
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-warnings", url],
        capture_output=True, text=True,
    )
    metadata: dict[str, dict] = {}
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            vid_id = entry.get("id", "")
            if vid_id:
                metadata[vid_id] = {
                    "fps": entry.get("fps"),
                    "height": entry.get("height"),
                    "width": entry.get("width"),
                    "duration_sec": entry.get("duration"),
                    "upload_date": entry.get("upload_date"),
                    "view_count": entry.get("view_count"),
                }
                print(f"    {vid_id}: {entry.get('fps')}fps {entry.get('height')}p")
        except json.JSONDecodeError:
            pass
    return metadata


def _is_playlist_entry(entry: dict) -> bool:
    """Return True if this entry points to a playlist rather than a video."""
    ie_key = entry.get("ie_key", "")
    if ie_key in ("YoutubeTab", "YoutubePlaylist"):
        return True
    url = entry.get("url", "")
    return "list=" in url and "watch?v=" not in url


def extract_video_info(entry: dict) -> dict:
    """Extract relevant fields from a yt-dlp flat playlist video entry."""
    vid_id = entry.get("id", "")
    return {
        "video_id": vid_id,
        "title": entry.get("title", ""),
        "url": entry.get("url") or f"https://www.youtube.com/watch?v={vid_id}",
        "duration_sec": entry.get("duration"),
        "upload_date": entry.get("upload_date"),
        "view_count": entry.get("view_count"),
        "fps": entry.get("fps"),
        "height": entry.get("height"),
        "width": entry.get("width"),
        "has_auto_subs": bool(entry.get("subtitles") or entry.get("automatic_captions")),
        "subtitle_type": "auto" if bool(entry.get("subtitles") or entry.get("automatic_captions")) else None,
        "ocr_confidence": None,
        "ocr_sample_text": None,
    }


def build_catalog(channel_url: str, config: dict, existing: dict = None,
                  full_metadata: bool = False) -> dict:
    """
    Build a channel catalog from yt-dlp metadata (no video download).
    If existing catalog is provided, skips already-cataloged video IDs.
    If full_metadata=True, fetches fps/height/width per video (slower).
    """
    existing_ids: set = set()
    existing_by_vid: dict = {}
    if existing:
        for pl in existing.get("playlists", []):
            for v in pl.get("videos", []):
                existing_ids.add(v["video_id"])
                existing_by_vid[v["video_id"]] = v

    print(f"Fetching channel metadata: {channel_url}")
    top = _yt_dlp_flat_json(channel_url)
    entries = top.get("entries") or []

    if entries and _is_playlist_entry(entries[0]):
        playlist_entries = entries
        entries_for_direct = None
    else:
        playlist_entries = [{
            "id": top.get("id", "default"),
            "title": top.get("title", "All Videos"),
            "url": channel_url,
            "_direct": True,
        }]
        entries_for_direct = entries

    playlists = []
    for pl_entry in playlist_entries:
        pl_id = pl_entry.get("id", "")
        pl_title = pl_entry.get("title", pl_id)
        pl_url = pl_entry.get("url", channel_url)
        print(f"  Playlist: {pl_title}")

        if pl_entry.get("_direct"):
            raw_entries = [e for e in entries_for_direct if not _is_playlist_entry(e)]
        else:
            try:
                raw_entries = [
                    e for e in (_yt_dlp_flat_json(pl_url).get("entries") or [])
                    if not _is_playlist_entry(e)
                ]
            except RuntimeError as exc:
                print(f"    ERROR: {exc}")
                playlists.append({"playlist_id": pl_id, "playlist_title": pl_title,
                                   "n_videos": 0, "videos": []})
                continue

        # Optionally fetch full metadata (fps/height/width) for new videos
        full_meta: dict[str, dict] = {}
        new_ids = {e.get("id") for e in raw_entries if e.get("id") not in existing_ids}
        if full_metadata and new_ids:
            full_meta = _yt_dlp_full_metadata(pl_url)

        videos = []
        for entry in raw_entries:
            v_id = entry.get("id", "")
            if v_id in existing_ids:
                videos.append(existing_by_vid[v_id])
                print(f"    [skip] {v_id} (already cataloged)")
            else:
                info = extract_video_info(entry)
                if v_id in full_meta:
                    info.update(full_meta[v_id])
                videos.append(info)
                fps_str = f" {info['fps']}fps {info['height']}p" if info.get("fps") else ""
                print(f"    + {v_id}: {info['title'][:55]}{fps_str}")

        playlists.append({"playlist_id": pl_id, "playlist_title": pl_title,
                           "n_videos": len(videos), "videos": videos})

    return {
        "channel_url": channel_url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "playlists": playlists,
    }


def save_catalog(catalog: dict, config: dict, name: str = "channel_catalog"):
    """Save catalog as JSON and flat CSV. Name sets the filename (without extension)."""
    catalog_dir = Path(config["catalog"]["path"])
    catalog_dir.mkdir(parents=True, exist_ok=True)

    json_path = catalog_dir / f"{name}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"JSON saved: {json_path}")

    rows = []
    for pl in catalog["playlists"]:
        for v in pl["videos"]:
            rows.append({"playlist_id": pl["playlist_id"],
                         "playlist_title": pl["playlist_title"], **v})

    csv_path = catalog_dir / f"{name}.csv"
    if rows:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    print(f"CSV saved: {csv_path} ({len(rows)} videos)")


def load_catalog(config: dict, name: str = "channel_catalog") -> dict | None:
    """Load existing catalog from disk by name, or return None."""
    path = Path(config["catalog"]["path"]) / f"{name}.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch YouTube channel/playlist catalog")
    parser.add_argument("channel_url", help="YouTube channel or playlist URL")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--name", default="channel_catalog",
                        help="Catalog filename (without extension). Default: channel_catalog")
    parser.add_argument("--full-metadata", action="store_true",
                        help="Fetch fps/height/width per video (slower, one request per video)")
    parser.add_argument("--detect-subs", action="store_true",
                        help="Run OCR detection for hardcoded subtitles")
    args = parser.parse_args()

    config = load_config(args.config)
    existing = load_catalog(config, args.name)
    catalog = build_catalog(args.channel_url, config, existing,
                            full_metadata=args.full_metadata)

    if args.detect_subs:
        sys.path.insert(0, str(Path(__file__).parent))
        from detect_hardcoded_subs import detect_hardcoded_subs  # noqa: E402

        for pl in catalog["playlists"]:
            for v in pl["videos"]:
                if v.get("subtitle_type") is not None:
                    continue
                print(f"  OCR: {v['video_id']} — {v['title'][:50]}")
                try:
                    r = detect_hardcoded_subs(v["url"], config)
                    v["subtitle_type"] = r["subtitle_type"]
                    v["ocr_confidence"] = r["ocr_confidence_avg"]
                    v["ocr_sample_text"] = " | ".join(r["sample_texts"][:2])
                    print(f"    → {r['subtitle_type']} ({r['frames_with_text']}/{r['frames_sampled']} frames)")
                except Exception as exc:
                    print(f"    ERROR: {exc}")
                    v["subtitle_type"] = "error"

    save_catalog(catalog, config, args.name)
    total = sum(pl["n_videos"] for pl in catalog["playlists"])
    print(f"\nDone: {len(catalog['playlists'])} playlists, {total} videos")
