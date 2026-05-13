# Avatar AI — Roadmap 2026

```mermaid
flowchart TD

    Q1["Q1 — COMPLETADO\nInvestigación · base técnica\nalianzas · brechas definidas"]

    Q1 --> TOOL["Q2 · ABR–JUN — EN CURSO\nHerramienta de captura\nRecolección y análisis de videos GCBA\nsubtítulos · sincronía · keypoints"]

    TOOL --> TRAIN1{"PRIMER ENTRENAMIENTO · JUN\n¿Mejora el score?"}

    TRAIN1 -->|NO-GO| FIX["Revisar approach\nJuan Bratti + UNLP"]
    TRAIN1 -->|GO| DATA

    DATA["Q2–Q3 · JUN–SEP\nGeneración de data propia\ntrámites · scripts · sordatón"]

    DATA --> Q3

    subgraph Q3 ["Q3 · EN PARALELO desde JUL"]
        AGENT["Agente inteligente\ntraducción → acción\nJUL"]
        INFRA["Integración + inferencia\nbackend · input · deploy\nJUL → DIC"]
        AVATAR["Avatar LSA\nsíntesis de señas\nJUL–SEP"]
    end

    Q3 --> TRAIN2["SEGUNDO ENTRENAMIENTO · SEP\ndata específica de trámites"]

    TRAIN2 --> POC_PREP["Preparación POC · NOV"]
    POC_PREP --> POC["PRESENTACIÓN POC · DIC\nRecursos 2027"]


    %% Estilos — escala de grises por etapa

    style Q1        fill:#1e1e1e,color:#fff,stroke:#1e1e1e
    style TOOL      fill:#444,color:#fff,stroke:#444
    style TRAIN1    fill:#555,color:#fff,stroke:#555
    style FIX       fill:#555,color:#fff,stroke:#555,stroke-dasharray:6 4
    style DATA      fill:#666,color:#fff,stroke:#666
    style Q3        fill:#7a7a7a,color:#fff,stroke:#7a7a7a
    style AGENT     fill:#888,color:#fff,stroke:#888
    style INFRA     fill:#888,color:#fff,stroke:#888
    style AVATAR    fill:#888,color:#fff,stroke:#888
    style TRAIN2    fill:#a0a0a0,color:#fff,stroke:#a0a0a0
    style POC_PREP  fill:#c0c0c0,color:#222,stroke:#c0c0c0
    style POC       fill:#e0e0e0,color:#222,stroke:#e0e0e0
```

---

**Leyenda de grises**

| Tono | Etapa |
|---|---|
| Negro `#1e1e1e` | Completado |
| Gris oscuro `#444–#555` | En curso (Q2) |
| Gris medio `#666–#888` | Próximo (Q3) |
| Gris claro `#a0–#c0` | Futuro cercano (Q4 inicio) |
| Gris muy claro `#e0` | Meta final — POC Diciembre |

---

**Puntos de decisión GO/NO-GO**

| Fecha | Pregunta | Si NO-GO |
|---|---|---|
| Fin junio | ¿Score mejora con videos GCBA? | Revisar approach con Juan + UNLP |
| Fin julio | ¿Score permite que LLM interprete? | Evaluar si continuar proyecto |
