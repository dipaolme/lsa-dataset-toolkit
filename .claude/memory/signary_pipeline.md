---
name: signary-pipeline
description: "Pipeline señario CAS → keypoints → Animator (Jorge). Estado, decisiones, pendientes."
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

**Última actualización:** 2026-07-01

## Objetivo
Conectar el señario CAS (PDF: palabra → URL YouTube) con el Animator de Jorge (`/home/mdipaola/Animator`).

## El Animator (Jorge) — cómo funciona
- Web app HTML/JS/CSS en un servidor Flask. Canvas 600×450px. Avatar procedural con IK solver.
- NO usa matrices de keypoints raw. Usa `WORD_DICTIONARY` en `app.js`:
  ```js
  'PALABRA': [
    { wrist: {x, y},
      angle: -Math.PI/2,
      curls: [t,i,m,r,p],
      face: {...},
      duration: 300 },
    ...
  ]
  ```
- IK solver calcula el codo automáticamente a partir de wrist.
- Fix cross-body aplicado en app.js — flip adaptativo según posición del wrist vs shoulder.

## Pipeline definido
```
Señario CAS (PDF manual) → usuario anota palabra+URL en input.json
  ↓
yt-dlp descarga video → data/signary/videos/PALABRA.mp4
  ↓
extract_keypoints.py → data/signary/PALABRA.json  (1086 features/frame)
  ↓ (opcional --3d)
extract_keypoints.py --3d → data/signary/PALABRA_3d.json  (+ landmarks_3d con x,y,z)
```

## Flag --3d (agregado 01/06/2026)
`python scripts/extract_keypoints.py video.mp4 --3d --output output_3d.json`

Agrega `landmarks_3d` a cada frame:
```json
"landmarks_3d": {
  "pose":       [[x,y,z,vis], ...],   // 33 puntos
  "right_hand": [[x,y,z], ...],       // 21 puntos (sin visibility)
  "left_hand":  [[x,y,z], ...]        // 21 puntos
}
```
Cara excluida del 3D (no necesaria para el Animator).

## Palabras procesadas (playlist bebidas CAS)
FEBRERO, AGUA, CAFE, CERVEZA, COCA_COLA, JUGO, JUGO_EXPRIMIDO, MATE, MATE_COCIDO, SODA, 7UP_SPRITE
Pendientes (requieren cookies YouTube): TE, VINO, YERBA

## Viewer standalone (signary_viewer/)
Carpeta lista para compartir con Jorge:
- `signary_skeleton_viewer.ipynb` — versión 3D con Axes3D, slider + play
- `requirements.txt` — numpy, matplotlib, ipywidgets, ipympl, jupyterlab
- `data/` — JSONs 3D por palabra (gitignoreados, van en ZIP)

Jorge integró el viewer 2D en su servidor Flask. Pidió 3D → viewer 3D construido.

## Landmark reference (MediaPipe mano, 21 puntos)
- 0: wrist | 1-4: pulgar | 5-8: índice | 9-12: medio | 13-16: anular | 17-20: meñique
- En el vector: landmark k → vector[1044 + k*2], vector[1044 + k*2 + 1]

## FEBRERO — ejemplo completo validado ✅
- 124 frames, 25fps, mano abierta, arco sube/baja
- 4 keyframes: frames 0, 35, 70, 80
- Fix IK cross-body aplicado en Animator

## Limitaciones conocidas
- Curl formula: distancia tip→wrist no captura bien cierre con mano de frente
- "Mano plana": dedos juntos no soportado en Animator
- Coordenadas body-relative: mapeo simple pendiente

## Videos Windows → WSL (patrón confirmado 01/07/2026)

Videos en Windows accesibles desde WSL via `/mnt/c/`:
```bash
python scripts/extract_keypoints.py "/mnt/c/Users/mdp_e/Gobierno de la Ciudad de Buenos Aires/grupo_DG Inclusión Digital - Documents/02-Proyectos/08-Avatar AI/Material LSA/GUÍA INFO LSA 2018-2019/videos/NOMBRE.MOV"
```
- `.MOV` funciona directo, sin convertir a mp4
- Archivos `._NOMBRE.MOV` (con punto-guion-bajo) = resource fork de macOS, no son el video real

## Videos procesados para Jorge (más allá del señario)

**DSC_0858 p.75 "ayuda tecnica"** (01/07/2026) — video completo, sin `--3d`. Output: `data/keypoints/DSC_0858 p. 75 ayuda tecnica.json`.

## Pendientes
1. TE, VINO, YERBA: descargar desde Windows y procesar
2. Script `keypoints_to_animator.py`: conversión automática con coord mapping body-relative
3. Script de selección automática de keyframes
4. Mejorar curl formula (ángulos entre joints)
5. Script `build_signary.py`: pipeline completo desde input.json
