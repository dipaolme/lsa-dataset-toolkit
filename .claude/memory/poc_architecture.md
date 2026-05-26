---
name: poc-architecture-dual-track
description: "Arquitectura técnica del POC — encoder/decoder, cómo funciona el clasificador de intent, los dos escenarios reales — 2026-05-26"
metadata: 
  node_type: memory
  type: project
  updated: 2026-05-26
  originSessionId: 9370954d-c2d9-47e4-8057-939c81870dfc
---

## El pipeline completo

```
keypoints (T × 1086)
        │
        ▼
    ENCODER   ← aprende a interpretar movimiento LSA
        │
        ├──── DECODER ────→  texto español palabra x palabra   [Track A]
        │
        └──── mean pooling → clasificador → intent             [Track B]
```

El encoder es compartido entre Track A y Track B. Se entrena junto con el decoder (fine-tuning de Signformer completo). No se puede entrenar solo el encoder con texto.

---

## El Encoder

Recibe: secuencia de keypoints (T frames × 1086 features)
Produce: T vectores de 512 dimensiones, uno por frame, con contexto de toda la secuencia (self-attention)

Cada vector no representa solo ese frame — "sabe" lo que pasó antes y después.

---

## El Decoder

Recibe: output del encoder [v1...vT]
Produce: texto palabra por palabra (autoregresivo)
- Paso 1: [START] → "para"
- Paso 2: "para" → "renovar"
- Paso N: → [END]

En cada paso mira todo el encoder output (cross-attention) + lo ya generado.

---

## Mean Pooling (para Track B)

Nombre técnico: **mean pooling**
Operación: promedio de los T vectores del encoder → un solo vector de 512

```python
embedding = encoder_output.mean(dim=0)  # (T, 512) → (512,)
intent = classifier(embedding)           # (512,) → (N_intents,)
```

Otras variantes: max pooling, CLS token.
Bien probado en NLP (BERT para clasificación). No documentado específicamente para LSA+Signformer → pregunta pendiente para Juan.

---

## Los dos escenarios reales del POC

**Sin Juan (emergencia):**
- keypoints → mean pooling crudo (sin encoder) → SVM → intent
- Puede funcionar con 29 clips para probar, escala incierta

**Con Juan (ideal):**
- Fine-tuning Signformer completo (encoder + decoder juntos)
- Track A sale solo del fine-tuning
- Track B: congelar encoder, entrenar capa clasificadora encima (barato, rápido)
- "Congelar" = `param.requires_grad = False` sobre los pesos del encoder

No hay escenario intermedio real.

---

## UX del POC

Avatar saluda → "¿En qué te puedo ayudar?" → usuario seña (~5-10s) → pausa detectada → inferencia → avatar responde con video pre-grabado.

El saludo del avatar controla el contexto: no hay señas previas que confundan al modelo.

---

## Preguntas abiertas para Juan

1. ¿Fine-tuning desde tu checkpoint LSA-T? (la más importante)
2. ¿Qué recomendás para representación de secuencia para clasificación? ¿Mean pooling, CLS token, otro?
3. ¿Cuántos clips por intención necesita el clasificador?
4. ¿Curriculum learning reduce cantidad de clips? ¿Cuánto?
5. ¿Cuánto tarda inferencia en CPU para clip de ~10s?

**How to apply:** Antes de implementar Track B, verificar si Juan tiene opinión sobre la representación de secuencia. Mean pooling es la apuesta segura pero él puede tener algo mejor.
