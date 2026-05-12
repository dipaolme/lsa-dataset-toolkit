"""
ocr.py — Extracción de texto OCR desde streams de video.

Funciones de bajo nivel (compartidas con detect_hardcoded_subs.py):
  get_stream_url(video_url) → str
  get_stream_duration(stream_url) → float | None
  sample_frames(stream_url, duration_sec, times_sec) → list[tuple[float, ndarray]]
  ocr_bottom_strip(frame, bottom_fraction) → dict

API de extracción:
  extract_ocr_video(video_url, config, interval_sec) → dict
  load_ocr(path) → dict
  save_ocr(data, path) → None
"""

import json
import subprocess
from pathlib import Path



import cv2
import numpy as np
import pytesseract

_YTDLP = str(Path(__file__).parent.parent / ".venv/bin/yt-dlp")


# ──────────────────────────────────────────────────────────────────────────────
# Funciones de bajo nivel
# ──────────────────────────────────────────────────────────────────────────────

def get_stream_url(video_url: str) -> str:
    """Obtiene URL CDN directa de un video YouTube (≤480p para OCR rápido)."""
    result = subprocess.run(
        [
            _YTDLP, "--get-url", "--no-warnings",
            "-f", "best[height<=480][ext=mp4]/worst[height>=360][ext=mp4]/best[ext=mp4]/best",
            video_url,
        ],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip().split("\n")[0]


def get_stream_duration(stream_url: str) -> float | None:
    """Duración en segundos del stream, o None si no se puede determinar."""
    cap = cv2.VideoCapture(stream_url)
    fps = cap.get(cv2.CAP_PROP_FPS)
    n = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    return round(n / fps, 2) if fps > 0 and n > 0 else None


def sample_frames(
    stream_url: str,
    duration_sec: float | None,
    times_sec: list[float],
) -> list[tuple[float, np.ndarray]]:
    """Captura frames en los tiempos indicados. Devuelve lista de (time_sec, frame)."""
    if duration_sec and duration_sec > 0:
        times = [t for t in times_sec if t < duration_sec * 0.95]
        if not times:
            times = [duration_sec * 0.1]
    else:
        times = times_sec

    cap = cv2.VideoCapture(stream_url)
    result = []
    for t in times:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ret, frame = cap.read()
        if ret and frame is not None:
            result.append((t, frame))
    cap.release()
    return result


def ocr_bottom_strip(frame: np.ndarray, bottom_fraction: float = 0.35) -> dict:
    """
    OCR sobre la franja inferior del frame con múltiples preprocesados.
    Devuelve el resultado con más palabras encontradas.
    """
    h = frame.shape[0]
    strip = frame[int(h * (1 - bottom_fraction)):, :]
    gray = cv2.cvtColor(strip, cv2.COLOR_BGR2GRAY)

    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, otsu_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    best = {"text": "", "confidence": 0.0, "word_count": 0}
    for img in [gray, otsu, otsu_inv]:
        data = pytesseract.image_to_data(
            img, lang="spa",
            config="--psm 11",
            output_type=pytesseract.Output.DICT,
        )
        words = [w for w, c in zip(data["text"], data["conf"]) if w.strip() and int(c) > 20]
        if len(words) > best["word_count"]:
            confs = [int(c) for c in data["conf"] if int(c) > 0]
            best = {
                "text": " ".join(words),
                "confidence": round(sum(confs) / len(confs), 1) if confs else 0.0,
                "word_count": len(words),
            }
    return best


# ──────────────────────────────────────────────────────────────────────────────
# Extracción completa de un video
# ──────────────────────────────────────────────────────────────────────────────

def _clean_text(text: str) -> str:
    """Elimina artefactos OCR: caracteres solos, números puros, tokens muy cortos."""
    tokens = [t for t in text.split() if len(t) > 1 and not t.isdigit()]
    return " ".join(tokens)


def _deduplicate_segments(segments: list[dict]) -> list[dict]:
    """Fusiona segmentos consecutivos con texto idéntico."""
    if not segments:
        return []
    result = [segments[0].copy()]
    for seg in segments[1:]:
        if seg["text"] == result[-1]["text"]:
            result[-1]["end_sec"] = seg["end_sec"]
        else:
            result.append(seg.copy())
    return result


def extract_ocr_video(
    video_url: str,
    config: dict,
    interval_sec: float = 2.0,
) -> dict:
    """
    Extrae texto OCR de todos los frames de un video YouTube muestreados cada interval_sec.

    Returns dict con:
      status: "ok" | "error"
      duration_sec: float
      segments: [{"start_sec", "end_sec", "text", "confidence"}, ...]
      full_text: str  — textos únicos concatenados, para TF-IDF
      error: str  — solo si status == "error"
    """
    ocr_cfg = config.get("ocr", {})
    bottom_fraction = ocr_cfg.get("bottom_fraction", 0.35)

    try:
        stream_url = get_stream_url(video_url)
        duration = get_stream_duration(stream_url)

        if not duration or duration <= 0:
            return {"status": "error", "error": "no duration", "segments": [], "full_text": ""}

        times = [round(t, 1) for t in np.arange(1.0, duration * 0.98, interval_sec)]
        frames = sample_frames(stream_url, duration, times)

        segments = []
        for t, frame in frames:
            ocr = ocr_bottom_strip(frame, bottom_fraction)
            text = _clean_text(ocr["text"])
            if text:
                segments.append({
                    "start_sec": t,
                    "end_sec": t,
                    "text": text,
                    "confidence": ocr["confidence"],
                })

        segments = _deduplicate_segments(segments)

        seen: set[str] = set()
        unique_texts: list[str] = []
        for seg in segments:
            if seg["text"] not in seen:
                seen.add(seg["text"])
                unique_texts.append(seg["text"])

        return {
            "status": "ok",
            "duration_sec": duration,
            "segments": segments,
            "full_text": " ".join(unique_texts),
        }

    except Exception as e:
        return {"status": "error", "error": str(e), "segments": [], "full_text": ""}


# ──────────────────────────────────────────────────────────────────────────────
# Persistencia
# ──────────────────────────────────────────────────────────────────────────────

def load_ocr(path: str | Path) -> dict:
    """Carga yt_ocr.json. Devuelve dict vacío si no existe."""
    path = Path(path)
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_ocr(data: dict, path: str | Path) -> None:
    """Guarda dict de OCR en JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
