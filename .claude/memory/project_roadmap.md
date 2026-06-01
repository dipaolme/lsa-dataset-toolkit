---
name: project-roadmap-avatar-ai
description: "Roadmap Avatar AI — estado junio 2026, decisión Path B (sordatón), próximos hitos"
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

**Última actualización:** 2026-06-01

## Completado ✅

- Toy dataset 29 casos generado y analizado
- Análisis lingüístico corpus (61.8% hapax)
- Notebook reestructurada para reunión Juan Bratti
- Señario pipeline: FEBRERO + 13 bebidas (playlist CAS) procesadas
- Viewer 2D → Jorge lo integró en Flask
- Viewer 3D construido (`signary_viewer/`)
- Flag `--3d` agregado a `extract_keypoints.py`
- Standalone `signary_viewer/` listo para compartir (ZIP)
- Diapo seguimiento mayo actualizada
- Mail Pedro Dal Bianco redactado (`data/docs/mail_pedro_dal_bianco.md`)
- Respuesta a Signai enviada — reunión semana 01/06

## Pendiente ⏳ — por orden de urgencia

1. **Enviar mail a Pedro Dal Bianco** — `data/docs/mail_pedro_dal_bianco.md`
2. **Reunión Signai** — miércoles o jueves semana 01/06, dar acceso al material
3. **Reunión Juan Bratti** — mensaje enviado 17/05, sin respuesta aún
4. **TE, VINO, YERBA** — descargar desde Windows, extraer keypoints 3D
5. **GPU** — sin resolver
6. **Sordatón** — fecha sin definir, decisiones previas pendientes
7. **Conversación director** sobre avatar: visión 2027 vs. simulado POC
8. **Taxonomía de intents** — 15-25 trámites específicos GCBA
9. **`scripts/to_signformer.py`** — convertir JSON → HDF5 (2172 features)
10. **POC intent classifier** — LSA-T + encoder Signformer (ver [[poc-intent-classifier]])

## Roadmap macro (Q2-Q4 2026)

- Q2 ABR-JUN: herramienta captura, recolección, análisis, keypoints ← EN CURSO
- JUN: primer entrenamiento → Go/No-Go con Juan Bratti
- Q3 JUL-SEP: sordatón, agente inteligente, infraestructura, avatar LSA
- SEP: segundo entrenamiento con data específica de trámites
- DIC: POC final

**Decisión estratégica activa:** Path B (sordatón) — no curar más videos existentes.
Ver [[strategic-decisions-avatar-ai]] para el detalle completo.

**How to apply:** Pedro Dal Bianco es ahora el contacto técnico más estratégico — su respuesta puede cambiar prioridades. Verificar si la reunión con Juan ya ocurrió antes de cada sesión.
