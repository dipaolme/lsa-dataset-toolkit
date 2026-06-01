---
name: signformer-format-hdf5
description: Especificación exacta del formato HDF5 + CSV para LSAKeypointDataset (SignformerAdaptation-LSA)
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a8ff457-40e7-4b80-83b1-13ff5ed1481b
---

**Repo SignformerAdaptation-LSA:** `/home/dipa/Proyectos/gcba/SignformerAdaptation-LSA`
**Loader:** `data/LSA-T/lsa_dataset.py` → clase `LSAKeypointDataset`

## HDF5 — estructura esperada

```
keypoints.hdf5
└── <clip_id>               ← ej: "DSC_0841 p.66"
    └── signer_0
        ├── keypoints:  (frames, 2172)   ← 543 kp × 4 (x, y, z, visibility)
        └── boxes:      (frames, 4)      ← bounding box (puede ser ceros)
```

El DataLoader hace `_extract_xy_coordinates()` → 2172 → 1086 (toma solo x,y).
**No pre-normalizar** — el DataLoader normaliza per-frame.

## Conversión 1086 → 2172

```python
xy = np.array(entry['keypoints'])   # (T, 1086)
xy_r = xy.reshape(T, 543, 2)
full = np.zeros((T, 543, 4), dtype=np.float32)
full[:, :, :2] = xy_r               # z=0, vis=0
full_flat = full.reshape(T, 2172)
```

## CSV — columnas mínimas

| Columna | Descripción |
|---|---|
| `id` | mismo valor que el key en el HDF5 |
| `label` | texto en español (target del modelo) |

## Constructor DataLoader

```python
LSAKeypointDataset(
    hdf5_path="data/dataset/keypoints.hdf5",
    csv_path="data/dataset/metadata.csv",
    split="train",
    split_ratios=(0.8, 0.1, 0.1),   # con 29 casos → todo train
    normalize=True,
    keypoint_subset="all",
)
```

## Límites del modelo

- feature_size: 1086 (después de la extracción x,y)
- max_sent_length: 1242 frames (~49.7s a 25fps)
- Vocabulario: 13.664 palabras (lsa_t.txt.vocab)
- Modelo **gloss-free** — no usa anotación de señas individuales

## Script pendiente

`scripts/to_signformer.py` — convierte `data/dataset/toy_dataset.json` → `keypoints.hdf5` + `metadata.csv`

**How to apply:** Al crear `to_signformer.py` usar esta especificación exacta. No olvidar el padding 1086→2172.
