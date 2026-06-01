# Memory Index
*Última actualización: 2026-06-01*

## Proyecto
- [Estado del repo y dataset](project_lsa.md) — toy dataset 29 casos completo, scripts, schema JSON
- [Roadmap y próximos pasos](project_roadmap.md) — Path B activo, bloqueantes, pendientes por orden de urgencia
- [Decisiones estratégicas](strategic_decisions.md) — dual-track (Signformer+intent), sordatón, avatar simulado, métricas trainabilidad
- [Formato Signformer HDF5](signformer_format.md) — LSAKeypointDataset: HDF5 2172 features, CSV id+label, conversión 1086→2172
- [POC clasificador de intent](poc_intent_classifier.md) — LSA-T 6765 clips, encoder Signformer ya entrenado, plan 3 tareas
- [Arquitectura POC dual-track](poc_architecture.md) — encoder/decoder, mean pooling, 2 escenarios reales (con/sin Juan)
- [Pipeline señario → Animator](signary_pipeline.md) — CAS PDF → URL → keypoints → WORD_DICTIONARY app.js; 11 palabras procesadas; viewer 3D

## Equipo y alianzas
- [Equipo y alianzas](team_context.md) — Juan Bratti, Jorge (Flask+3D), Sebastián, Signai (reunión semana 01/06), GPU sin resolver
- [Pedro Dal Bianco](pedro_dal_bianco.md) — creador LSA-T + Signformer, contactado 01/06, paper paráfrasis LLM mayo 2026

## Técnico
- [extract_keypoints.py — canónico](keypoints_canonical.md) — MediaPipe Tasks API 0.10+; 1086 features; flag --3d disponible
- [Perfil de usuario](user_profile.md) — Matías es PO/PM técnico, no principalmente dev
- [Feedback: estructura utils/](feedback_utils_structure.md) — utils/ para reutilizables; catalog.py/subtitles.py/video.py eliminados en mayo 2026
