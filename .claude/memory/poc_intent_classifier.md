---
name: poc-intent-classifier
description: Plan y estado del POC de clasificador de intent usando LSA-T + encoder Signformer — pendiente para retomar
metadata: 
  node_type: memory
  type: project
  originSessionId: 9843d382-6f93-4cdd-97eb-8f4eb23a873f
---

**Última actualización:** 2026-05-26
**Estado:** ⏳ Pendiente — arrancar mañana

## Objetivo

Probar que keypoints → intent es técnicamente viable (Track B) usando el dataset LSA-T completo y el encoder de Signformer ya entrenado. Sin GPU, sin Juan, sin sordatón.

## Dataset LSA-T — formato confirmado

- **Archivos:** `data/LSA-T/lsa_t.train`, `lsa_t.dev`, `lsa_t.test` en `/home/mdipaola/SignformerAdaptation-LSA/`
- **Formato:** pickle + gzip. Cada objeto es un dict con keys: `name`, `signer`, `gloss`, `text`, `sign`
- `sign`: torch.Tensor shape `(frames, 1086)` — keypoints ya procesados
- `text`: transcripción en español
- `gloss`: vacío (dataset gloss-free)
- **Volumen:** train=6.765, dev=845, test=pendiente contar
- **Entorno:** venv en `/home/mdipaola/SignformerAdaptation-LSA/.venv` con torch + numpy + scikit-learn

## Modelo entrenado

- Checkpoint: `/home/mdipaola/SignformerAdaptation-LSA/lsa_t_model/best.ckpt`
- Entrenado por Juan Bratti sobre LSA-T completo

## Plan del POC — DOS tareas pendientes (orden a definir)

### Tarea 1 — Auto-etiquetar intents desde texto
- Definir 5-8 categorías genéricas que aparezcan naturalmente en LSA-T (salud, educación, política, derechos, cultura, etc.)
- Asignar intent a cada clip desde su `text` (keyword rules o embeddings)
- Output: lista de (clip_id, intent_label)

### Tarea 2 — Extraer features del encoder
- Cargar `best.ckpt`, congelar pesos
- Pasar keypoints de cada clip por el encoder → `(T, hidden_dim)`
- Mean pooling → `(hidden_dim,)` por clip
- Output: matriz de features para entrenar SVM

### Tarea 3 — Entrenar y evaluar SVM
- Input: features del encoder + intent labels
- Modelo: SVM o regresión logística
- Métricas: accuracy + confusion matrix

## Arquitectura — dos escenarios

**Escenario A (sin fine-tuning):** keypoints → mean pooling crudo → SVM. Más débil, no requiere cargar modelo.

**Escenario B (con encoder):** keypoints → encoder Signformer → mean pooling → SVM. Más fuerte porque el encoder ya aprendió LSA.

**Estamos apuntando a Escenario B** — tenemos el checkpoint entrenado.

**Why:** Si funciona con encoder features, valida Track B antes del sordatón y con datos reales.
**How to apply:** Al retomar, arrancar por decidir orden de Tarea 1 vs Tarea 2, luego hacer un notebook en SignformerAdaptation-LSA.
