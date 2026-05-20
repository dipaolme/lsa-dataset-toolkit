---
name: estado-del-repo-lsa-dataset-toolkit
description: "Qué hay en el repo, qué funciona, estado del toy dataset, decisiones estratégicas tomadas y próximos pasos"
metadata: 
  node_type: memory
  type: project
  originSessionId: d389935d-31c5-4a0f-93f0-1af550f9a0dc
---

**Repo:** `/home/dipa/Proyectos/gcba/lsa-dataset-toolkit`
**Propósito:** Explorar y validar qué data disponible en YouTube GCBA sirve para entrenar el modelo Signformer/LSA-T. Parte del proyecto Avatar AI (COPIDIS/GCBA).
**Última actualización:** 2026-05-18

---

## Estado actual (mayo 2026)

### Toy Dataset — 29 casos ✅ COMPLETO

```bash
python scripts/build_toy_dataset.py --catalog data/docs/raw_lsa.xlsx --sample-rate 2
# Correr desde la raíz del repo (no desde scripts/)
```

**Outputs generados:**
- `data/dataset/toy_dataset.json` — 29 entradas con keypoints (1086 features/frame)
- `data/dataset/toy_dataset.csv` — metadata liviana
- `data/dataset/toy_test.json` / `toy_test.csv` — 1 entrada de prueba (misma estructura, gitignored)

**Schema actual de toy_dataset.json** (evolucionó desde CLAUDE.md — actualizar):
```json
["id", "text", "source", "n_frames", "feature_size", "keypoints", "metadata"]
```
- Campo renombrado: `gloss` → `text`
- Nuevos campos top-level: `n_frames`, `feature_size`
- Metadata más rica: `tramite`, `playlist`, `yt_title`, `duration_s`, `fps`, `confidence_avg`, `pose_pct`, `face_pct`, `left_hand_pct`, `right_hand_pct`, `word_count`

**data/lsa_raw/:**
- `subtitles/` — 29 archivos .txt (subtítulos de los 29 videos del toy dataset)
- `videos/` — 49 archivos .MOV (más videos que subtítulos → no todos procesados)

**Estadísticas del dataset:**
- 29 clips | feature_size: 1086
- Duración media: **24.3s** | min: 13.6s | max: 37.0s
- Frames media: 728 | min: 407 | max: 1110
- ⚠ LSA-T promedia 9.36s — nuestros clips son ~3x más largos → requieren segmentación

**Distribución por intent:**
Educación(6), Accesibilidad(6), Transporte(5), Trabajo(5), Servicios Sociales(3), Salud(3), Vida Independiente(1)

### Análisis lingüístico — resultado clave

Corrido con `scripts/analyze_subtitles.py` sobre los 29 subtítulos .txt:

- **Hapax legomena: 61.8%** → peor que LSA-T (>50%). Vocabulario muy disperso.
- Coverage@5: 9.6% — muy pocas palabras aparecen 5+ veces
- TTR global: 0.337
- Bigrama más frecuente: "con discapacidad" (31x)

**Conclusión:** el corpus GCBA existente tiene el mismo problema que LSA-T. No es entrenable sin cambios radicales de diseño.

### Decisión estratégica tomada: Path B

Generar videos propios (sordatón) en lugar de curar videos existentes.
Ver `memory/strategic_decisions.md` para el detalle completo.

---

## Scripts disponibles

### scripts/
| Script | Función | Estado |
|---|---|---|
| `extract_keypoints.py` | MediaPipe Tasks → vector 1086 features/frame | ✅ |
| `build_toy_dataset.py` | 29 casos: subtítulos + keypoints → JSON + CSV | ✅ |
| `analyze_subtitles.py` | **NUEVO** Análisis lingüístico de corpus .txt/.srt/.vtt | ✅ |
| `to_signformer.py` | JSON → HDF5 (2172) + CSV para LSAKeypointDataset | ⏳ pendiente |

**Uso de analyze_subtitles.py:**
```bash
python scripts/analyze_subtitles.py data/lsa_raw/subtitles/
python scripts/analyze_subtitles.py data/legislatura/subtitles/ --output data/docs/analisis_legislatura.json
```

### Docs generados (data/docs/)
- `agenda_reunion_juan.md` — agenda estructurada para reunión con Juan Bratti + director
- `preguntas_tecnicas_juan.md` — 6 bloques de preguntas técnicas para Juan
- `roadmap_avatar_ai.md` — roadmap actualizado con estado real al 17/05/2026

---

## Notebook

`notebooks/toy_dataset_analysis.ipynb` — reestructurado para reunión con Juan:
- **Sección 1:** Calidad de keypoints — tabla gradiente, boxplots, duración vs LSA-T, sample rate, imputación
- **Sección 2:** Análisis lingüístico — hapax %, coverage@N, TTR, bigramas, intent con nota de granularidad
- **Sección 3:** Simulacro de escala vs LSA-T

La visualización interactiva de keypoints (slider) fue eliminada del notebook — está en `explore_dataset.ipynb`.

---

## Próximos pasos concretos

1. **Reunión Juan Bratti + Sebastián Tsuji** — mensaje enviado (17/05), esperando respuesta
2. **Reunión con grupo aliado** — darles specs: clips ~5-10s, labels text+intent, formato HDF5+CSV
3. **GPU** — resolver: CCAD-UNC (Juan lo usó), Córdoba, UBA, o cloud pago (Colab Pro)
4. **Fecha sordatón** — fijar julio o agosto antes de que sea tarde para el POC de diciembre
5. **Taxonomía de intents** — 15-25 trámites específicos GCBA para el POC

**How to apply:** El toy dataset existe y el notebook corre. El próximo hito técnico es `to_signformer.py` para convertir a HDF5. El próximo hito estratégico es la reunión con Juan.
