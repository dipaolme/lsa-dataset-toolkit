---
name: estado-del-repo-lsa-dataset-toolkit
description: "Qué hay en el repo, qué funciona, estado del toy dataset, prioridades de la semana y próximos pasos — actualizado 2026-05-26"
metadata: 
  node_type: memory
  type: project
  updated: 2026-05-26
  originSessionId: 9370954d-c2d9-47e4-8057-939c81870dfc
---

**Repo:** `/home/dipa/Proyectos/gcba/lsa-dataset-toolkit`
**Propósito:** Explorar y validar qué data disponible sirve para entrenar Signformer/LSA-T. Parte del proyecto Avatar AI (COPIDIS/GCBA).

---

## Estado actual (2026-05-26)

### Toy Dataset — 29 casos ✅ COMPLETO

- `data/dataset/toy_dataset.json` — 29 entradas, schema: `["id", "text", "source", "n_frames", "feature_size", "keypoints", "metadata"]`
- `data/dataset/toy_dataset.csv` — metadata liviana
- 7 intenciones: accesibilidad, educacion, vida_independiente, trabajo, transporte, salud, servicios_sociales
- Duración media: 24.3s (3x más largo que LSA-T promedio de 9.36s)
- Hapax legomena: 61.8% → NO entrenable tal cual

### Análisis lingüístico
- Corpus GCBA 29 clips: hapax 61.8%, coverage@5 9.6% → problema estructural
- Corpus Legislatura (1 sesión): hapax 55.4% → mismo problema
- Conclusión: Path B (sordatón con vocabulario controlado) es el camino

### Scripts disponibles
| Script | Estado |
|---|---|
| `extract_keypoints.py` | ✅ |
| `build_toy_dataset.py` | ✅ |
| `analyze_subtitles.py` | ✅ |
| `to_signformer.py` | ❌ pendiente — no es prioridad inmediata |

---

## Prioridades semana 2026-05-26

### AHORA — sin dependencias externas
1. **Mail a Juan Bratti** — hoy, 5 minutos. LinkedIn sin respuesta hace 10 días, usar email.
2. **Reunión Jorge** — 26/05 16:30. Preguntar: estado servidor + pipeline síntesis.
3. **Prueba de concepto clasificador** — esta semana. Usar 29 clips existentes:
   - Mean pooling de keypoints → un vector por clip
   - SVM o regresión logística sobre las 7 intenciones
   - Objetivo: validar si Track B es viable antes del sordatón
   - Sin GPU, sin Juan, sin intérpretes

### CUANDO JUAN RESPONDA — se desbloquea todo esto
4. Taxonomía de intents (15-25 trámites GCBA)
5. GPU — cuánta y cuál (depende de si hay fine-tuning desde checkpoint o desde cero)
6. Diseño del sordatón (cuántos clips, protocolo)
7. Specs para el grupo aliado

### PARALELO — no urgente
8. Recolección de más videos sin anotar (director lo pidió)
9. Un mensaje al contacto GPU de Córdoba para calentar relación

### NO HACER TODAVÍA
- Entrenar encoder desde cero en Colab → esperá respuesta de Juan
- Pagar intérpretes para curar videos existentes → sin saber cuántos clips necesitás

---

## Bloqueante crítico único

**Una sola pregunta de Juan desbloquea todo:**
¿Podés hacer fine-tuning desde tu checkpoint LSA-T?
- SÍ → ~300-500 clips en sordatón, Colab Pro alcanza
- NO → 5000+ clips desde cero, no viable para diciembre

---

## Notebook

`notebooks/toy_dataset_analysis.ipynb` — reestructurado con 3 secciones:
1. Calidad de keypoints
2. Análisis lingüístico
3. Simulacro de escala vs LSA-T

**How to apply:** El toy dataset existe y el notebook corre. El próximo hito técnico es la prueba de concepto del clasificador (esta semana). El próximo hito estratégico es la respuesta de Juan.
