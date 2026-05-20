# Memory Index

## Proyecto
- [Estado del repo lsa-dataset-toolkit](project_state.md) — toy dataset 29 casos: scripts creados, pendientes, paths, schema JSON, cómo correr, sección 8 en notebook
- [Formato Signformer (HDF5 + CSV)](signformer_format.md) — especificación exacta para LSAKeypointDataset: HDF5 2172 features, CSV id+label, conversión desde 1086
- [Equipo y alianzas — Avatar AI](team_and_context.md) — roles reales (Matías es PO/PM), Juan Bratti, Jorge (incierto), alianzas UNLP/Córdoba/UBA/grupo estudiantes, GPU sin resolver
- [Decisiones estratégicas — mayo 2026](strategic_decisions.md) — dual-track (Signformer+intent classifier), avatar simulado, clips cortos, curriculum learning, accionables, métricas de trainabilidad

## Trabajo técnico
- [extract_keypoints.py — versión canónica](keypoints_canonical.md) — MediaPipe Tasks API 0.10+; output 1086 features; compatible Signformer/LSA-T; versión LOCAL es la correcta
