---
name: strategic-decisions-avatar-ai
description: "Decisiones estratégicas clave, insights y accionables del proyecto Avatar AI — sesión mayo 2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: d389935d-31c5-4a0f-93f0-1af550f9a0dc
---

**Fecha:** 2026-05-17

## Objetivo del POC (Diciembre 2026)

Persona seña frente a tótem/computadora → sistema identifica intención → agente acciona → respuesta en pantalla (texto + avatar simulado con videos pre-grabados en LSA).

**NO es:** traducción perfecta palabra por palabra.
**SÍ es:** intent accuracy suficiente para que un agente accione.
**Métrica de éxito:** intent accuracy, no BLEU.

---

## Decisión de path: Path B — generar videos propios

**Evidencia:** hapax legomena 61.8% en corpus GCBA existente → mismo problema que LSA-T.
Curar más videos existentes amplía el problema, no lo resuelve.

**Path B = sordatón:**
- Vocabulario controlado, clips cortos (~5-10s), intent labels desde el diseño
- Un evento genera DOS outputs: clips de entrenamiento + clips de respuesta para el avatar simulado
- El grupo aliado construye la herramienta (OBS + Python + interfaz de anotación)

**Path A (curar existentes)** no descartado para material de Legislatura si el análisis lingüístico muestra hapax < 30%. Usar `scripts/analyze_subtitles.py` para verificar cuando llegue el material.

---

## Arquitectura dual-track (POC)

```
Track A: keypoints → Signformer → texto español (display)
Track B: keypoints → clasificador de intención → agente acciona
```

- Corren en paralelo sobre los mismos keypoints
- Track B es el salvaguarda: si Track A falla, Track B igual detecta la intención
- Track B es un clasificador simple, corre en CPU, necesita ~50 clips por intención
- Dataset necesita DOS labels por clip: `text` (Track A) + `intent` (Track B)

**Why:** con datos limitados, intent classification es más alcanzable que traducción word-by-word. Con vocabulario acotado de trámites, 50-150 clips por intención son suficientes para Track B.

---

## Avatar simulado (gestión del director)

El director (Sebastián Tsuji) quiere avatar que responde en LSA. Síntesis real = 2027.

**Solución POC:** videos pre-grabados en LSA. La sordatón genera AMBOS:
1. Clips de input para entrenar el modelo
2. Clips de respuesta (1 por intent) para el avatar del POC

**Comunicación al director:** "avatar como visión 2027" ≠ "avatar simulado para el POC". Conversación pendiente.

---

## Curriculum learning

Propuesta para Juan: entrenar primero con frases muy cortas y vocabulario básico (10-15 frases), luego escalar.
**Pendiente validar con Juan:** si conviene y cómo estructura los datos.

---

## Latencia / POC inference

- Signformer es batch (encoder bidireccional) — necesita clip completo
- **Enfoque más viable para POC:** detección de pausa + inferencia batch → ~1-2s latencia
- Causal masking: posible sin cambiar arquitectura pero requiere reentrenar y baja calidad → no recomendado
- **Incógnita crítica:** tiempo de inferencia en CPU → define si POC necesita GPU

---

## Pregunta crítica pendiente de Juan: fine-tuning

¿Se puede hacer fine-tuning desde el modelo LSA-T ya entrenado de Juan?
Si SÍ → cantidad de clips necesarios cae de ~1000 a ~200-300. Cambia el tamaño de la sordatón.
Esta pregunta es la más importante de la reunión.

---

## Métricas de trainabilidad para evaluar corpus

- **Hapax legomena %:** >40% = no entrenable | 20-40% = insuficiente | <20% = razonable
- **Coverage@5:** % palabras únicas que aparecen ≥5 veces
- Script: `python scripts/analyze_subtitles.py <directorio>`
- Resultado corpus GCBA actual: hapax 61.8%, coverage@5 9.6% → NO entrenable tal cual

---

## Bloqueantes críticos (urgentes)

1. **GPU** — sin GPU Juan no entrena. Opciones: CCAD-UNC, Córdoba, UBA, Colab Pro/GCP
2. **Specs herramienta → grupo aliado** — necesitan specs antes de seguir construyendo
3. **Fecha sordatón** — target julio-agosto. Sin fecha no existe
4. **Rol de Jorge** — indefinido. Resolver adentro o afuera del plan
5. **Taxonomía de intents** — 15-25 trámites específicos GCBA, idealmente con input de comunidad sorda

---

## Accionables

### Completados ✅
- [x] Toy dataset 29 casos generado y analizado
- [x] Notebook reestructurada con secciones alineadas a la agenda
- [x] `scripts/analyze_subtitles.py` creado
- [x] `data/docs/agenda_reunion_juan.md` creado
- [x] `data/docs/preguntas_tecnicas_juan.md` creado
- [x] `data/docs/roadmap_avatar_ai.md` actualizado
- [x] Mensaje a Juan Bratti enviado (17/05/2026)

### Pendientes ⏳
- [ ] Reunión Juan Bratti + Sebastián Tsuji
- [ ] Reunión con grupo aliado → darles specs de la herramienta
- [ ] Resolver GPU (Córdoba / UBA / cloud)
- [ ] Fijar fecha sordatón (julio o agosto)
- [ ] Conversación con director sobre avatar: visión 2027 vs. simulado POC
- [ ] Clarificar rol de Jorge
- [ ] Análisis lingüístico de subtítulos Legislatura cuando lleguen
- [ ] Taxonomía de intents (idealmente con input comunidad sorda)
- [ ] `scripts/to_signformer.py` — convertir JSON → HDF5 + CSV

**How to apply:** Antes de cada sesión verificar qué bloqueante es más urgente y si la reunión con Juan ya ocurrió (cambia las prioridades completamente).
