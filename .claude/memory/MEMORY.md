# Memory Index
*Última actualización: 2026-05-26*

## Proyecto
- [Estado del repo lsa-dataset-toolkit](project_state.md) — toy dataset 29 casos completo, prioridades semana 26/05, prueba de concepto clasificador como próximo hito técnico
- [Arquitectura POC dual-track](poc_architecture.md) — encoder/decoder, mean pooling, 2 escenarios reales (con/sin Juan), preguntas abiertas para Juan
- [Decisiones estratégicas — mayo 2026](strategic_decisions.md) — Path B sordatón, UX del POC, curriculum learning, cuántos clips, accionables por semana
- [Formato Signformer (HDF5 + CSV)](signformer_format.md) — especificación exacta para LSAKeypointDataset: HDF5 2172 features, CSV id+label, conversión desde 1086

## Equipo y contexto
- [Equipo y alianzas — Avatar AI](team_and_context.md) — Jorge activo (síntesis+servidor), Juan sin respuesta (email pendiente), director alineado, intérpretes escasos

## Trabajo técnico
- [extract_keypoints.py — versión canónica](keypoints_canonical.md) — MediaPipe Tasks API 0.10+; output 1086 features; compatible Signformer/LSA-T
