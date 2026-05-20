# Agenda — Reunión Juan Bratti
**Proyecto Avatar AI · Mayo 2026**

---

## Objetivo de la reunión

Tomar cuatro decisiones con evidencia para definir el plan de trabajo del trimestre. La notebook `toy_dataset_analysis.ipynb` es el hilo conductor — no es una presentación, es el punto de partida para la conversación.

---

## Contexto rápido (5 min)

Desde la reunión de abril avanzamos en:
- Pipeline de extracción de keypoints funcionando (MediaPipe Tasks API, 1086 features/frame)
- Toy dataset de 29 videos GCBA curados con keypoints y metadata
- Análisis de calidad y lingüístico sobre ese material

Lo que necesitamos resolver hoy es qué hacemos con eso para escalar.

---

## Hilo conductor: notebook toy_dataset_analysis.ipynb

### Sección 1 — Calidad de keypoints
Comparación con LSA-T: detección, imputación, duración de clips.

**Abre la pregunta:** nuestros clips son de 1-2 minutos. LSA-T promedia 9.36 segundos. ¿Podés entrenar algo útil con clips largos o la segmentación a nivel de oración es innegociable?

### Sección 2 — Análisis lingüístico
TTR, vocabulario único, hapax legomena %, distribución de longitud.

**Abre la pregunta:** el mismo problema que encontraste en LSA-T (vocabulario muy amplio, sin repetición) aparece acá también. ¿Cuánto importa esta métrica para predecir si el modelo va a converger?

---

## Las cuatro decisiones a resolver

### 1. ¿Dónde concentramos los esfuerzos de data?

**Opción A:** Curar y anotar videos existentes (GCBA + Legislatura + otros)
**Opción B:** Generar videos propios con vocabulario controlado (sordatón)

Tenemos recursos para una sola. El análisis lingüístico da la evidencia. ¿Qué necesitás vos del material para que el entrenamiento tenga chances de funcionar?

### 2. ¿Cómo tiene que estar estructurada la data?

Esto impacta directamente una herramienta que estamos construyendo con un grupo aliado (OBS + Python + interfaz de anotación). Necesitamos definir antes de que la construyan:

- Duración de clips (¿cuál es el rango ideal?)
- Labels requeridos por clip: ¿solo texto, o también intent?
- Formato de entrega: HDF5 + CSV según lo que ya tenemos definido, ¿algo más?
- ¿Qué hacemos con los frames donde no se detectan manos?

### 3. ¿Tiene sentido incluir una etiqueta de intención?

**La propuesta:** además del texto transcripto, cada clip lleva una etiqueta de intent (`renovar_dni`, `solicitar_turno`, etc.).

Esto habilita una arquitectura dual-track para el POC:
- **Track A:** keypoints → Signformer → texto en español
- **Track B:** keypoints → clasificador de intención → agente acciona

Track B es un clasificador simple, no depende de que Track A traduzca bien. Si la traducción falla, la intención se detecta igual y el agente puede responder.

**Pregunta:** ¿es viable entrenar ambas cosas? ¿Lo harías como multitarea (un solo modelo, dos outputs) o dos modelos separados? ¿Cuántos clips por intención necesitaría el clasificador?

### 4. ¿Conviene curriculum learning?

**La propuesta:** empezar con clips muy cortos y vocabulario muy acotado (10-15 frases básicas de trámites), entrenar una base sólida, luego escalar gradualmente en complejidad.

¿Lo ves viable con la arquitectura de Signformer? ¿Cambia algo en cómo hay que preparar los datos o en los hiperparámetros de entrenamiento?

---

## Tema que introduce Matías: latencia y modo de inferencia

Para el POC necesitamos la menor latencia posible — idealmente que se sienta como un mini-diálogo.

- ¿Cuánto tarda la inferencia para un clip de ~10 segundos en CPU? ¿Es viable para una demo en una notebook sin GPU?
- El enfoque que evaluamos: detección de pausa + inferencia batch → ~1-2 segundos de latencia. ¿Lo ves razonable o hay algo mejor?
- ¿Qué opinás de habilitar CoPE en el entrenamiento con el dataset de trámites (mucho más chico que LSA-T)?

---

## Próximos pasos esperados al salir de la reunión

- Decisión clara sobre Path A vs. Path B (o combinación secuencial)
- Especificación de la estructura de datos → para alinear con el grupo aliado
- Número concreto: ¿cuántos clips por intención/frase necesitamos como mínimo?
- Acuerdo sobre curriculum learning: sí/no y cómo
- GPU: ¿tenés acceso al CCAD-UNC (Nabucodonosor) para este entrenamiento?
