# Preguntas técnicas para Juan Bratti
**Proyecto Avatar AI · Reunión Mayo 2026**

---

## 0. Decisión crítica previa — formato de anotación
> *Esta pregunta define todo lo que viene. No avanzar en diseño de dataset sin respuesta.*

**0.1** LSA tiene gramática distinta al español: sin artículos, orden SOV, espacio en lugar de preposiciones. Si anotamos con texto español completo (como LSA-T), el modelo tiene que aprender a generar artículos y conectores que nunca vio en las señas de entrada. ¿Tiene sentido anotar con **texto simplificado** (solo contenido léxico, sin stopwords ni artículos) para que el output esté más alineado con la entrada visual?

**0.2** Si usamos texto simplificado como target de Signformer, y un LLM como post-proceso para generar respuesta en español completo — ¿ves problemas con ese enfoque? ¿O perdemos compatibilidad con LSA-T de formas que no estamos viendo?

**0.3** ¿Conviene guardar dos versiones del label por clip (`text_simplified` + `text_full`) para poder entrenar con simplificado y evaluar con completo comparando contra LSA-T?

---

## 1. Datos de entrada — segmentación y formato

**1.1** Nuestros clips actuales son videos completos de 1-2 minutos con el texto completo como label. LSA-T usa clips de promedio 9.36 segundos a nivel de oración. ¿Podés entrenar algo con clips largos o la segmentación previa a nivel de oración es innegociable para que el modelo converja?

**1.2** Si necesitamos segmentar: ¿cuál es el rango de duración ideal por clip? ¿Hay un mínimo (clip demasiado corto) y un máximo práctico?

**1.3** Usamos sample_rate=2 (procesamos 1 de cada 2 frames → 15fps efectivos). ¿Afecta esto la calidad de la señal para señas rápidas? ¿Recomendás 30fps completo?

**1.4** Para imputación de keypoints faltantes usamos zeros directamente. Vos usás interpolación lineal → extrapolación → zeros. ¿Esa diferencia impacta en el entrenamiento o es marginal?

---

## 2. Arquitectura dual-track (Signformer + clasificador de intención)

**2.1** La propuesta es entrenar dos cosas sobre los mismos keypoints en paralelo:
- Track A: keypoints → Signformer → texto en español
- Track B: keypoints → clasificador de intención (ej. `renovar_dni`, `solicitar_turno`)

¿Lo ves viable? ¿Lo implementarías como multitarea (un modelo con dos heads de salida) o dos modelos completamente separados?

**2.2** ¿Cuántos clips por intención necesitaría el Track B (clasificador) para aprender algo útil? ¿50? ¿200?

**2.3** Si el clasificador de intención es un modelo separado y más simple, ¿qué arquitectura recomendarías? ¿SVM sobre los embeddings del encoder, una red pequeña, otro enfoque?

---

## 3. Curriculum learning

**3.1** La propuesta: empezar entrenando con clips muy cortos y vocabulario muy acotado (10-15 frases básicas de trámites), luego escalar en complejidad gradualmente. ¿Lo ves como una mejora sobre entrenar con todo el dataset desde el inicio?

**3.2** Si conviene: ¿cambia algo en cómo hay que estructurar los datos o en los hiperparámetros (epochs, learning rate, batch size)?

**3.3** ¿Cuántos clips por frase/palabra necesitamos como mínimo para que el modelo aprenda una correspondencia básica seña→texto?

---

## 4. Latencia e inferencia para el POC

**4.1** ¿Cuánto tarda la inferencia de un clip de ~10 segundos en CPU (sin GPU)? ¿Es viable para una demo en una notebook?

**4.2** Evaluamos detección de pausa + inferencia batch como el enfoque más simple para el POC: la persona seña, detectamos cuando para (~0.5s sin movimiento de manos), mandamos el clip al modelo. Latencia estimada: 1-2 segundos. ¿Lo ves razonable o hay algo mejor sin cambiar el modelo?

**4.3** ¿Signformer soporta causal masking en el encoder pasando `src_mask` triangular a `nn.Transformer`? ¿Lo recomendarías para el caso de uso de baja latencia o el trade-off de calidad no vale?

---

## 5. CoPE y configuración de entrenamiento

**5.1** En tu tesis desactivaste CoPE por limitaciones de memoria. Con un dataset de trámites mucho más chico (~500-2000 clips vs 8457 de LSA-T), ¿entra en memoria? ¿Vale la pena habilitarlo?

**5.2** Los hiperparámetros que usaste (batch_size=2, lr=3e-5, 4 encoders) — ¿los ajustarías para un dataset más chico pero más específico de dominio?

**5.3** ¿Tenés acceso al CCAD-UNC (Nabucodonosor) para entrenar este modelo? ¿O necesitamos conseguir GPU por otro lado?

---

## 6. Vocabulario y trainabilidad

**6.1** En tu análisis de LSA-T encontraste >50% de palabras con frecuencia 1 (hapax legomena). Para el dataset de trámites GCBA: ¿cuál es el umbral mínimo de repetición por palabra para que el modelo la aprenda? ¿Necesitamos que cada frase aparezca al menos N veces?

**6.2** Con vocabulario muy acotado (por ejemplo 200 palabras de trámites frecuentes) y buena repetición, ¿qué BLEU o intent accuracy esperarías como resultado realista con ~500-1000 clips?

**6.3** ¿Tiene sentido pre-entrenar el encoder con LSA-T y luego hacer fine-tuning con nuestro dataset de trámites? ¿Cuánto ahorra en datos propios necesarios?

---

## 7. Estrategia pre-sordatón: qué hacer con GPU + videos sin anotar
> *Estas preguntas apuntan a un escenario concreto: conseguimos GPU en junio, antes del sordatón. Tenemos cientos de videos GCBA en LSA sin subtítulos ni labels, y el pipeline de extracción de keypoints funcionando. ¿Qué conviene hacer con ese tiempo?*

**7.1** En tu tesis planteás como trabajo a futuro pre-entrenar el encoder con datasets grandes de poses humanas (auto-supervisado, sin texto). ¿Lo llegaste a explorar informalmente? ¿Tenés intuición de cuánto impacto tiene sobre el fine-tuning posterior?

**7.2** Si usamos masked pose modeling (enmascarar 15-30% de frames y entrenar al encoder a reconstruirlos), ¿esa tarea es suficiente para que el encoder aprenda representaciones útiles de movimiento LSA? ¿O recomendarías otra tarea — next-frame prediction, aprendizaje contrastivo, otra cosa?

**7.3** ¿Tiene sentido implementar ese pre-entrenamiento sobre el repo actual de Signformer, o requiere una arquitectura distinta para el encoder?

**7.4** Con el encoder pre-entrenado en videos sin anotar + curriculum learning en el fine-tuning con los datos del sordatón: ¿cuánto reducís la cantidad de clips anotados necesarios? ¿Pasamos de ~1000 a ~300? ¿O el impacto no es tan directo?

**7.5** Con GPU disponible: ¿vale la pena replicar tu entrenamiento completo sobre LSA-T antes del sordatón, para tener el pipeline validado y un baseline de referencia? ¿Compartís el checkpoint de tu tesis y la configuración exacta que usaste?

**7.6** CoPE lo descartaste por memoria. Con una GPU real (A100 o similar), ¿entra? ¿Tiene sentido probarlo sobre LSA-T como experimento paralelo mientras esperamos los datos propios?
