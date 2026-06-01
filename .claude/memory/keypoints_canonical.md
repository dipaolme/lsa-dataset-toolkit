---
name: extract_keypoints.py — versión canónica
description: Detalles técnicos de extract_keypoints.py — MediaPipe Tasks API, estructura 1086 features, flag --3d
type: project
originSessionId: fffc986a-d61a-4ef2-8f5e-5c03b0e34450
---
**Archivo:** `scripts/extract_keypoints.py`
**API:** MediaPipe Tasks 0.10+ (NO usar mp.solutions.holistic — fue eliminada)

## Estructura del vector 1086 features

```
Pose:       33 kp × 2 (x,y) =  66 features  [0:66]
Cara:      468 kp × 2 (x,y) = 936 features  [66:1002]
Mano izq:  21 kp × 2 (x,y) =  42 features  [1002:1044]
Mano der:  21 kp × 2 (x,y) =  42 features  [1044:1086]
```

FaceLandmarker devuelve 478 puntos; se toman los primeros 468 (face mesh sin iris) para compatibilidad con LSA-T.

**Why:** Signformer/LSA-T espera exactamente 1086 features. El repo SignformerAdaptation-LSA también usa esta dimensión.

## Modelos requeridos (en models/)
- `pose_landmarker.task`
- `face_landmarker.task`
- `hand_landmarker.task`

## Resultados sobre videos COPIDIS (1920×1080, 30fps)
- Pose detectada: 97% frames
- Cara detectada: 87% frames
- Confidence avg: ~0.73
- Manos: ~50% cada una (normal — señas unimanuales)

## Flag --3d (agregado 01/06/2026)
`python scripts/extract_keypoints.py video.mp4 --3d --output output_3d.json`
Agrega `landmarks_3d` por frame: pose [x,y,z,vis], right_hand/left_hand [x,y,z]. Cara excluida.
Compatible con el viewer 3D en `signary_viewer/`.

**How to apply:** Antes de trabajar en el toolkit verificar que los modelos están en `models/`. El venv está en `.venv/` dentro del repo.
