---
name: Formato de datos Signformer (LSAKeypointDataset)
description: Especificación exacta del formato HDF5 + CSV que espera SignformerAdaptation-LSA para cargar datos
type: project
originSessionId: fffc986a-d61a-4ef2-8f5e-5c03b0e34450
---
**Repo:** `/home/dipa/Proyectos/gcba/SignformerAdaptation-LSA`
**Loader:** `data/LSA-T/lsa_dataset.py` → clase `LSAKeypointDataset`

## HDF5 — estructura esperada

```
keypoints.hdf5
└── <clip_id>               ← puede ser "DSC_0841 p.66" o "DSC_0841 p.66.mp4"
    └── signer_0
        ├── keypoints:  (frames, 2172)   ← 543 kp × 4 (x, y, z, visibility)
        └── boxes:      (frames, 4)      ← bounding box — puede ser ceros
```

**IMPORTANTE:** el HDF5 espera 2172 features. El DataLoader hace `_extract_xy_coordinates()` que convierte 2172 → 1086 (toma solo x,y). La normalización per-frame también la hace el DataLoader — no pre-normalizar.

## Conversión de nuestros keypoints (1086) al formato HDF5 (2172)

```python
# (T, 1086) → (T, 2172)
xy = np.array(entry['keypoints'])       # (T, 1086)
xy_r = xy.reshape(T, 543, 2)            # (T, 543, 2)
full = np.zeros((T, 543, 4), dtype=np.float32)
full[:, :, :2] = xy_r                   # x,y; z=0, vis=0
full_flat = full.reshape(T, 2172)       # → (T, 2172)
```

## CSV de metadata — columnas mínimas requeridas

| Columna | Descripción |
|---|---|
| `id` | mismo valor que el key en el HDF5 |
| `label` | texto en español (el target del modelo) |

Columnas adicionales que agregamos para análisis: `intent`, `tramite`, `playlist`, `n_frames`, `duration_s`, `confidence_avg`

## Constructor del DataLoader

```python
LSAKeypointDataset(
    hdf5_path="data/dataset/keypoints.hdf5",
    csv_path="data/dataset/metadata.csv",
    split="train",                          # "train" | "dev" | "test"
    split_ratios=(0.8, 0.1, 0.1),           # con 29 casos → todo train
    normalize=True,                          # el DataLoader normaliza
    keypoint_subset="all",                   # "all" usa los 1086
)
```

## Rangos de keypoints en el vector 1086

```
[0   :66  ]  Pose:      33 kp × 2 (x,y)
[66  :1002]  Cara:     468 kp × 2 (x,y)   ← FaceLandmarker 478 puntos, tomamos 468 (sin iris)
[1002:1044]  Mano izq:  21 kp × 2 (x,y)
[1044:1086]  Mano der:  21 kp × 2 (x,y)
```

## Límites del modelo

- feature_size: 1086
- max_sent_length: 1242 frames (~49.7 seg a 25fps)
- Vocabulario texto: 13.664 palabras (lsa_t.txt.vocab)
- El modelo es **gloss-free** — no usa anotación de señas individuales

## Script de conversión (pendiente de crear)

`scripts/to_signformer.py` — convierte `data/dataset/toy_dataset.json` → `keypoints.hdf5` + `metadata.csv`

**How to apply:** Al crear `to_signformer.py`, usar esta especificación exacta. No olvidar el padding 1086→2172.
