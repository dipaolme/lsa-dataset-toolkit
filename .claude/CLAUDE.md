# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

MediaPipe requires three `.task` model files in `models/` (already present, not in git):
`pose_landmarker.task`, `face_landmarker.task`, `hand_landmarker.task`

## Common commands

```bash
# Catálogo de canal YouTube
python scripts/fetch_channel_catalog.py <url> [--full-metadata] [--detect-subs] [--name catalog_name]

# Registro: construir / ver resumen / ver entrada individual
python utils/registry.py build
python utils/registry.py summary
python utils/registry.py show "DSC_0873 p.87 ..."

# Extraer keypoints de un video
python scripts/extract_keypoints.py path/to/video.mp4 [--sample-rate 2] [--frame-start 0] [--frame-end 300]

# Construir dataset (correr desde scripts/)
cd scripts && python build_dataset.py ../data/raw/video.mp4 ../data/subtitles/video.srt --intent renovar_dni

# Jupyter
jupyter notebook notebooks/
```

## Pipeline de datos

El flujo completo, en orden:

```
fetch_channel_catalog.py   → data/catalog/channel_catalog.json + .csv
detect_hardcoded_subs.py   → enriquece catálogo con OCR
match_videos.py            → data/catalog/yt_vs_local_matching.csv
parse_subs_docx.py         → data/subtitles/<stem>.srt  (desde Guia Subs.docx)
utils/registry.py build    → data/catalog/video_registry.json  ← estado central
extract_keypoints.py       → data/keypoints/<stem>.json
build_dataset.py           → data/dataset/<stem>_dataset.json
export_raw_lsa.py          → dataset final consolidado
```

`utils/registry.py` es el rastreador central del pipeline. La clave es el **stem del archivo local** (ej: `"DSC_0873 p.87 que apoyos te da el Ministerio"`). El registro persiste el estado de cada video a través de todas las fases: matching → revisión → subtítulos → keypoints → dataset.

## Formato de keypoints

`extract_keypoints.py` genera vectores de **1086 features por frame** usando MediaPipe Tasks API 0.10+ (no la API legacy `mp.solutions`):

```
[0   :66  ]  Pose:      33 kp × 2 (x,y)
[66  :1002]  Cara:     468 kp × 2 (x,y)   ← FaceLandmarker devuelve 478; se toman los primeros 468 (sin iris)
[1002:1044]  Mano izq:  21 kp × 2 (x,y)
[1044:1086]  Mano der:  21 kp × 2 (x,y)
```

Esta dimensión es la que espera **Signformer / LSA-T**. No cambiar sin sincronizar con el repo de entrenamiento (`SignformerAdaptation-LSA`).

Cada frame en el JSON de salida tiene: `frame`, `vector` (lista de 1086 floats), `pose_detected`, `face_detected`, `left_hand`, `right_hand`, `confidence`.

## Entradas del dataset

`build_dataset.py` produce entradas con este esquema:

```json
{
  "id": "<video_stem>_<index>",
  "gloss": "texto del segmento de subtítulo",
  "source": "video_stem",
  "frames": {"start": 120, "end": 180},
  "keypoints": [ ...frames... ],
  "metadata": {
    "intent": null,
    "tramite": null,
    "subtitle_type": "auto_cc",
    "sync_ok": true,
    "confidence_avg": 0.73,
    "fps": 30.0,
    "time_start": 4.0,
    "time_end": 6.0
  }
}
```

`intent` y `tramite` se pasan por CLI; son `null` si no se especifican.

## Configuración

`config.yaml` controla todos los paths y parámetros de MediaPipe. El path `paths.videos` apunta al directorio con los videos crudos locales (puede ser una ruta absoluta de red/Windows). `config.yaml` no está gitignoreado — no guardar paths sensibles ahí.

## Imports entre scripts

`build_dataset.py` usa imports relativos (`from extract_subs import load_subtitles`): debe correrse desde el directorio `scripts/`, no desde la raíz.

`fetch_channel_catalog.py` hardcodea la ruta de yt-dlp a `.venv/bin/yt-dlp`. Si el venv está en otro lugar, hay que ajustarlo.

## Qué está gitignoreado

Todo bajo `data/` (raw, subtitles, keypoints, dataset, catalog) y `notebooks/data/`. Los únicos artefactos de datos versionados son `docs/raw_lsa.xlsx` (catálogo curado) y `data/yt_vs_local_matching_catalogYt_v3.xlsx`.
