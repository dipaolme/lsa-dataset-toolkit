---
name: strategic-decisions-avatar-ai
description: Decisiones estratégicas clave del proyecto Avatar AI — mayo 2026
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a8ff457-40e7-4b80-83b1-13ff5ed1481b
---

**Última actualización:** 2026-05-17

## Objetivo del POC (Diciembre 2026)

Persona seña frente a tótem → sistema identifica intención → agente acciona → respuesta (texto + avatar simulado con videos pre-grabados LSA).
- **Métrica de éxito:** intent accuracy, no BLEU.
- **NO es:** traducción perfecta. **SÍ es:** intent accuracy suficiente para accionar un agente.

## Decisión: Path B — Sordatón (generar videos propios)

**Evidencia:** hapax 61.8% en corpus GCBA existente → no entrenable tal cual.

**Path B:** vocabulario controlado, clips cortos (~5-10s), intent labels desde el diseño.
- La sordatón genera DOS outputs: clips de entrenamiento + clips de respuesta para el avatar simulado.
- El grupo aliado construye la herramienta (OBS + Python + interfaz de anotación).

**Path A** (curar existentes): no descartado para Legislatura si hapax < 30%. Usar `scripts/analyze_subtitles.py` para verificar.

## Arquitectura dual-track (POC)

```
Track A: keypoints → Signformer → texto español (display)
Track B: keypoints → clasificador de intención → agente acciona
```
- Corren en paralelo sobre los mismos keypoints
- Track B es el salvaguarda si Track A falla
- Track B necesita ~50 clips por intención (simple, corre en CPU)
- Cada clip necesita DOS labels: `text` (Track A) + `intent` (Track B)

## Avatar simulado (para el director)

Síntesis real de avatar LSA = 2027. Para el POC: videos pre-grabados LSA.
La sordatón genera ambos (clips de input + clips de respuesta por intent).
**Comunicación pendiente al director:** "avatar como visión 2027" ≠ "avatar simulado para el POC".

## Métricas de trainabilidad del corpus

- Hapax >40% = no entrenable | 20-40% = insuficiente | <20% = razonable
- Coverage@5: % palabras únicas con ≥5 apariciones
- Script: `python scripts/analyze_subtitles.py <directorio>`

## Pregunta crítica para Juan Bratti

¿Fine-tuning desde modelo LSA-T ya entrenado?
- Si SÍ → clips necesarios bajan de ~1000 a ~200-300. Cambia el tamaño de la sordatón.

## Bloqueantes críticos

1. **GPU** — sin GPU Juan no entrena. Opciones: CCAD-UNC, Córdoba, UBA, Colab Pro
2. **Specs → grupo aliado** — necesitan specs antes de seguir construyendo
3. **Fecha sordatón** — target julio-agosto
4. **Rol de Jorge** — indefinido
5. **Taxonomía de intents** — 15-25 trámites GCBA

**How to apply:** Antes de cada sesión verificar si la reunión con Juan ya ocurrió — cambia las prioridades completamente. El criterio de éxito es intent accuracy, no calidad de traducción.
