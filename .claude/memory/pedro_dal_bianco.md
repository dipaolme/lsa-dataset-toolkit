---
name: pedro-dal-bianco
description: Pedro Dal Bianco — creador de LSA-T y Signformer, nuevo contacto clave, paper mayo 2026
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

**Contacto establecido:** 2026-06-01 vía LinkedIn
**Mail:** dalbianco.pedro@gmail.com
**Institución:** III-LIDI, Universidad Nacional de La Plata (UNLP)
**Disponibilidad:** de viaje próximas semanas, contacto por LinkedIn o mail

## Quién es

Pedro Dal Bianco es el autor principal detrás del dataset LSA-T y la arquitectura Signformer — la base técnica del proyecto Avatar AI. Juan Bratti hizo su tesis y entrenó el modelo sobre el trabajo de Pedro.

**Why:** Contacto directo con la fuente original. Puede orientar sobre dataset, arquitectura, y decisiones técnicas que Juan Bratti ya tomó.

## Paper reciente (arXiv:2605.31393, 29 mayo 2026)

**Título:** Target-Side Paraphrase Augmentation for Sign Language Translation with Large Language Models

**Co-autores:** Jean Paul Nunes Reinhold, Oscar Stanchi, Facundo Quiroga, Franco Ronchetti (UNLP/CONICET), Ulisses Brisolara Corrêa (UFPel)

**Técnica:** GPT-4o genera paráfrasis del texto de referencia manteniendo el video/pose fijo → el decoder ve múltiples realizaciones de la misma seña → reduce el problema de heavy-tail vocabulary.

**Resultados:**
- PHOENIX14T (DGS): BLEU-4 sube 9.56 → 10.33 ✅
- GSL: near-saturated, poco impacto
- LSA-T: "extremely sparse LSA-T setting reveal the limits" — confirma el problema de hapax

**Releases públicos:** datasets aumentados para DGS, GSL y **LSA** (con paráfrasis LLM). Código disponible.

**Relevancia directa para Avatar AI:**
1. La técnica de augmentación con LLM es aplicable al toy dataset y a la sordatón
2. El dataset LSA aumentado puede ser útil para el POC de intent classifier
3. Confirma que LSA-T es extremadamente esparso → valida la decisión Path B (sordatón)

## How to apply

Antes de diseñar estrategia de datos, consultar si el dataset LSA aumentado de Pedro es accesible y si la técnica de paráfrasis aplica al vocabulario acotado de trámites GCBA. Considerar invitarlo como colaborador o asesor técnico.
