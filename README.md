# lsa-dataset-toolkit

Toolkit de validación y exploración de datasets de Lengua de Señas Argentina (LSA).

Parte del proyecto **Avatar AI** — Fase 0: determinar si los videos GCBA sirven como material de entrenamiento.

## Preguntas que responde este toolkit

- ¿Los videos disponibles tienen subtítulos? ¿Están sincronizados?
- ¿Se pueden extraer keypoints de calidad con MediaPipe?
- ¿Qué estructura de dataset es compatible con los trabajos previos?

## Estructura

```
lsa-dataset-toolkit/
├── notebooks/
│   └── explore_dataset.ipynb   # exploración end-to-end (empezar acá)
├── scripts/
│   ├── download.py             # descargar videos (yt-dlp)
│   ├── extract_subs.py         # extraer subtítulos (CC o OCR)
│   ├── extract_keypoints.py    # MediaPipe → keypoints
│   ├── sync_subs.py            # analizar sincronización
│   └── build_dataset.py        # generar dataset final
├── data/
│   ├── raw/                    # videos descargados (no versionado)
│   ├── subtitles/              # archivos SRT/VTT
│   ├── keypoints/              # JSON con keypoints por video
│   └── dataset/                # dataset final
├── config.yaml                 # parámetros configurables
└── requirements.txt
```

## Quickstart

```bash
pip install -r requirements.txt
jupyter notebook notebooks/explore_dataset.ipynb
```

## Formato del dataset

Cada entrada tiene la estructura:

```json
{
  "id": "video_id_0001",
  "gloss": "texto del subtítulo",
  "source": "gcba_youtube",
  "frames": { "start": 120, "end": 180 },
  "keypoints": { ... },
  "metadata": {
    "intent": null,
    "tramite": null,
    "subtitle_type": "auto_cc",
    "sync_ok": true,
    "confidence_avg": 0.87
  }
}
```

El campo `metadata.intent` está reservado para el dataset propio (ej: `"renovar_dni"`).
