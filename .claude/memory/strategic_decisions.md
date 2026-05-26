---
name: strategic-decisions-avatar-ai
description: "Decisiones estratégicas, arquitectura del POC, accionables — actualizado 2026-05-26"
metadata: 
  node_type: memory
  type: project
  updated: 2026-05-26
  originSessionId: 9370954d-c2d9-47e4-8057-939c81870dfc
---

## Objetivo del POC (Diciembre 2026)

Persona seña frente a tótem → sistema identifica intención → agente acciona → respuesta en pantalla + avatar en LSA (videos pre-grabados).

**Métrica de éxito:** intent accuracy, no BLEU.
**Avatar POC:** videos pre-grabados, NO síntesis generada. Síntesis es objetivo 2027.

---

## Decisión de path: Path B — generar videos propios (sordatón)

Hapax 61.8% en corpus GCBA + 55.4% en Legislatura → misma limitación estructural.
Path A (curar existentes) no resuelve el problema estadístico.

**Path B = sordatón:** vocabulario controlado, clips cortos (~5-10s), intent labels desde el diseño.
Un evento genera DOS outputs: clips de entrenamiento + clips de respuesta para el avatar.

---

## Arquitectura del POC — DOS escenarios reales

### Escenario A — Sin fine-tuning (sin Juan o sin datos suficientes)
```
keypoints → mean pooling crudo → clasificador simple (SVM/logistic) → intent
```
Sin Signformer. Plan de emergencia. Puede funcionar, puede no funcionar.

### Escenario B — Con fine-tuning (con Juan + GPU + datos anotados)
```
keypoints → Signformer completo entrenado
          → encoder → mean pooling → clasificador → intent   (Track B)
          → decoder → texto en pantalla                      (Track A)
```
Fine-tuning entrena encoder+decoder juntos. Track B es parasitario del encoder entrenado.
Track A (traducción visible en pantalla) suma valor en la demo pero no es indispensable.

**No hay escenario intermedio real** — o tenés Signformer fine-tuneado o no lo tenés.

---

## Cómo funciona el clasificador de intent (Track B)

```
Secuencia keypoints (T × 1086)
        ↓
   Encoder Signformer → (T × 512) vectores contextuales
        ↓
   Mean pooling → un solo vector de 512
        ↓
   Capa lineal pequeña → "renovar_dni" con 87% probabilidad
```

**Mean pooling** = promedio de todos los vectores del encoder a lo largo del tiempo.
Técnica estándar en NLP (BERT para clasificación). No probada específicamente en LSA con Signformer — pregunta pendiente para Juan.

---

## UX del POC — diseño confirmado

```
Avatar saluda en LSA → "¿En qué te puedo ayudar?"
        ↓
Persona seña su pedido (~5-10s)
        ↓
Sistema detecta pausa → inferencia batch
        ↓
Clasificador detecta intent → "renovar_dni"
        ↓
Avatar responde con video pre-grabado en LSA
```

Este diseño controla el contexto: el usuario sabe que tiene que señar después del saludo. Los clips del sordatón son respuestas a "¿en qué te puedo ayudar?" — vocabulario más acotado y repetitivo naturalmente.

---

## Curriculum learning — cómo aplica al sordatón

No significa "señas básicas primero" (alfabeto, números, saludos).
Significa estructurar la dificultad de los **trámites** en fases:

```
Fase 1: 5-10 intenciones muy distintas entre sí, clips cortos (~3-5s), muchas repeticiones
Fase 2: más intenciones, clips más naturales, más variación en cómo se seña
Fase 3: rango completo, LSA más natural
```

Beneficio: el modelo converge más eficientemente. ¿Cuánto reduce la cantidad de clips? → pregunta para Juan.

---

## La pregunta más importante (pendiente de Juan)

**¿Podés hacer fine-tuning desde tu checkpoint LSA-T?**

- SÍ → ~300-500 clips en sordatón, Colab Pro (~10 USD/mes) alcanza
- NO → 5000+ clips desde cero, no viable para diciembre

Esta respuesta cambia TODO: cuántos clips grabar, qué GPU conseguir, si el POC de diciembre es realista.

---

## Cuántos clips necesitamos (estimaciones)

| Escenario | Clips totales | Horas de grabación | Viable |
|---|---|---|---|
| Track B solo (sin Juan) | 750-2500 | 8-50hs | Difícil pero posible |
| Fine-tuning desde checkpoint | 300-1000 | 4-13hs | ✅ Viable con 1-2 jornadas |
| Desde cero | 5000+ | 50+hs | ❌ No viable para diciembre |

---

## Métricas de trainabilidad del corpus

- **Hapax %:** >40% = no entrenable | 20-40% = insuficiente | <20% = razonable
- Corpus GCBA actual: 61.8% → NO entrenable
- Corpus Legislatura: 55.4% → NO entrenable
- Script: `python scripts/analyze_subtitles.py <directorio>`

---

## Accionables

### Completados ✅
- [x] Toy dataset 29 casos
- [x] Notebook reestructurada para reunión Juan
- [x] `analyze_subtitles.py` creado
- [x] Docs reunión director creados
- [x] Análisis lingüístico Legislatura
- [x] Reunión con director (18/05/2026) — entendió 2 tracks, alineado

### Esta semana ⏳
- [ ] Mail a Juan Bratti hoy (26/05)
- [ ] Reunión Jorge 26/05 16:30
- [ ] Prueba de concepto clasificador con 29 clips (mean pooling + SVM)

### Cuando Juan responda
- [ ] Taxonomía de intents (15-25 trámites GCBA)
- [ ] GPU — cuánta y cuál
- [ ] Diseño del sordatón
- [ ] Specs para el grupo aliado

### No hacer todavía
- [ ] Entrenar encoder desde cero
- [ ] Pagar intérpretes para curar videos existentes
- [ ] `to_signformer.py`

**How to apply:** La prueba de concepto del clasificador es el próximo hito técnico concreto. Todo lo demás espera a Juan.
