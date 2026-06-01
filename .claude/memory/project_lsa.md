---
name: project-lsa-dataset-toolkit
description: "Avatar AI — estado del repo lsa-dataset-toolkit, toy dataset 29 casos, scripts, schema JSON"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a8ff457-40e7-4b80-83b1-13ff5ed1481b
---

**Repo:** `/home/mdipaola/lsa-dataset-toolkit` (también en `/home/dipa/Proyectos/gcba/lsa-dataset-toolkit` en otra máquina)
**Propósito:** Explorar y validar data del canal YouTube GCBA para entrenar Signformer/LSA-T. Parte del proyecto Avatar AI (COPIDIS/GCBA).
**Última actualización:** 2026-05-20

---

## Estado actual — Toy Dataset 29 casos ✅ COMPLETO

```bash
python scripts/build_toy_dataset.py --catalog data/docs/raw_lsa.xlsx --sample-rate 2
# Correr desde la raíz del repo (no desde scripts/)
```

**Outputs:**
- `data/dataset/toy_dataset.json` — 29 entradas con keypoints (gitignoreado por peso)
- `data/dataset/toy_dataset.csv` — metadata liviana (versionado en git)
- `data/dataset/toy_test.json` / `toy_test.csv` — 1 entrada de prueba

**Schema actual de toy_dataset.json:**
```json
{
  "id": "<video_stem>_<index>",
  "text": "texto completo del subtítulo",
  "source": "video_stem",
  "n_frames": 572,
  "feature_size": 1086,
  "keypoints": [ [1086 floats], ... ],
  "metadata": {
    "intent": "salud",
    "tramite": "5_cobertura_porteña_salud",
    "playlist": "...",
    "yt_title": "...",
    "duration_s": 19.09,
    "fps": 29.97,
    "confidence_avg": 0.758,
    "pose_pct": 1.0,
    "face_pct": 1.0,
    "left_hand_pct": 0.829,
    "right_hand_pct": 0.795,
    "word_count": 55
  }
}
```
⚠ Campo renombrado: `gloss` → `text`. `keypoints` es lista plana de vectores (un vector 1086 por frame).

**data/lsa_raw/:**
- `subtitles/` — 29 archivos .txt
- `videos/` — 49 archivos .MOV

**Estadísticas:**
- 29 clips | feature_size: 1086
- Duración media: 24.3s | min: 13.6s | max: 37.0s
- ⚠ LSA-T promedia 9.36s → nuestros clips son ~3x más largos → requieren segmentación

---

## Análisis lingüístico — resultado clave

Corrido con `scripts/analyze_subtitles.py` sobre 29 subtítulos:
- **Hapax legomena: 61.8%** → vocabulario muy disperso, mismo problema que LSA-T
- Coverage@5: 9.6% | TTR global: 0.337
- **Conclusión:** corpus GCBA existente no es entrenable sin cambios radicales

---

## Scripts disponibles

| Script | Función | Estado |
|---|---|---|
| `extract_keypoints.py` | MediaPipe Tasks → 1086 features/frame | ✅ |
| `build_toy_dataset.py` | 29 casos: subtítulos + keypoints → JSON + CSV | ✅ |
| `analyze_subtitles.py` | Análisis lingüístico de corpus .txt/.srt/.vtt | ✅ |
| `fetch_playlist_subs.py` | Fetch subtítulos de playlists YouTube | ✅ |
| `to_signformer.py` | JSON → HDF5 (2172) + CSV para LSAKeypointDataset | ⏳ pendiente |
| `analyze_raw.py` | Escanea MOV: duración/fps/resolución/blur | ✅ |
| `parse_subs_docx.py` | Parsea DOCX → texto por video | ✅ |
| `fetch_channel_catalog.py` | Fetch playlists/videos YouTube | ✅ |
| `export_raw_lsa.py` | Copia MOV + .txt a SharePoint | ✅ |
| `update_excel_and_registry.py` | Reconstruye registry y Excel de curación | ✅ |
| `download.py` | Descarga videos/subtítulos con yt-dlp | ✅ |
| `extract_ocr.py` | Extracción batch de OCR desde videos YouTube | ✅ |
| `extract_subs.py` | Parsea SRT/VTT y detecta subtítulos hardcodeados | ✅ |
| `sync_subs.py` | Analiza sincronización subtítulos vs. duración | ✅ |

**utils/:** `registry.py`, `docx_parser.py`, `matching.py`, `ocr.py`
⚠ `catalog.py`, `subtitles.py`, `video.py` fueron **eliminados** de utils/ en commit 2c4d745

---

## Notebooks

- `notebooks/toy_dataset_analysis.ipynb` — reestructurado para reunión Juan: calidad keypoints, análisis lingüístico, escala vs LSA-T
- `notebooks/visualize_keypoints.ipynb` — **NUEVO** visualización interactiva de keypoints
- `notebooks/explore_dataset.ipynb` — exploración general del dataset
- La visualización con slider (keypoints sobre frame) quedó en `explore_dataset.ipynb`

---

## Datos adicionales

- `data/legislatura/` — subtítulo y versión limpia sesión Sánchez Zinny 01-07-2025 (material Legislatura)
- `data/docs/` — agenda Juan, preguntas técnicas, roadmap actualizado, análisis lingüístico, métricas trainabilidad, propuesta GPU, resumen reunión director

---

## Config

`config.yaml` → `paths.videos: data/lsa_raw/videos` (cambiado de ruta Windows OneDrive)
En notebooks: usar `VIDEOS_DIR = REPO_ROOT / cfg['paths']['videos']` (no `Path(cfg['paths']['videos'])` — sería relativo al CWD del kernel).
