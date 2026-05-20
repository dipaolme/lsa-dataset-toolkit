# Propuesta: qué hacer con GPU + videos sin anotar (antes del sordatón)
**Para discutir con Juan Bratti · Mayo 2026**

---

## El problema que queremos resolver

El cuello de botella del proyecto no es el modelo — es el dato anotado. El sordatón (julio-agosto) va a generar los clips con texto que necesitamos para entrenar. Pero hay semanas de espera hasta entonces.

**La pregunta:** ¿qué podemos hacer YA con lo que tenemos?

---

## Lo que tenemos ahora

- **Videos crudos sin anotar**: cientos de videos del canal YouTube GCBA en LSA, sin subtítulos ni labels. Tenemos el pipeline completo para extraer keypoints (`extract_keypoints.py` con MediaPipe, output 1086 features/frame).
- **Toy dataset**: 29 clips con keypoints y texto, suficiente para probar el pipeline pero no para entrenar.
- **Repo SignformerAdaptation-LSA**: el código de tu tesis, listo para usar.
- **Bloqueante**: GPU. Sin GPU no podemos entrenar nada.

---

## La insight clave: el encoder pre-entrenado no necesita anotación

El encoder de Signformer aprende a representar secuencias de keypoints. Esa tarea se puede hacer **sin texto, sin subtítulos, sin labels** — usando aprendizaje auto-supervisado.

Si conseguimos GPU, podemos empezar a pre-entrenar el encoder en junio, semanas antes del sordatón. Cuando lleguen los datos anotados, el encoder ya sabe interpretar movimiento LSA y el fine-tuning necesita muchos menos clips.

---

## Plan concreto en 3 etapas (junio → agosto)

### Etapa 1 — Extraer keypoints de todos los videos disponibles
*Requiere: GPU chica o CPU con tiempo*

Tenemos acceso al catálogo completo del canal GCBA en YouTube. Con `fetch_channel_catalog.py` y `extract_keypoints.py` podemos procesar todos los videos sin necesidad de subtítulos.

```
canal YouTube GCBA → download → extract_keypoints.py → keypoints.json (sin texto)
```

**Output:** corpus de keypoints sin anotar, lo más grande posible. Cuantos más videos, mejor pre-entrenamiento.

---

### Etapa 2 — Pre-entrenar el encoder (masked pose modeling)
*Requiere: GPU mediana · Tiempo estimado: días*

**Tarea:** enmascarar el 15-30% de los frames de keypoints de cada secuencia y entrenar al encoder a reconstruirlos. Es análogo a BERT para texto — aprender representaciones útiles sin supervisión.

```
keypoints sin anotar
        ↓
[frame_1, MASK, frame_3, frame_4, MASK, ...]
        ↓
encoder aprende a predecir los frames faltantes
        ↓
checkpoint guardado: encoder pre-entrenado en movimiento LSA
```

**No necesita texto. No necesita el sordatón. Se puede hacer en junio.**

Al llegar agosto con los datos del sordatón, el fine-tuning arranca desde un encoder que ya entiende movimiento LSA — en lugar de empezar desde cero.

**Pregunta para Juan:** ¿cuál es la tarea de pre-entrenamiento que recomendás? ¿Masked frame prediction, next-frame prediction, reconstrucción? ¿Hay alguna implementación de referencia que pueda reusar?

---

### Etapa 3 — Replicar tu entrenamiento sobre LSA-T
*Requiere: GPU + acceso al dataset LSA-T · Tiempo: días*

Antes de tener datos propios necesitamos tener el pipeline de entrenamiento funcionando y validado. LSA-T ya existe y vos lo usaste. Si logramos reproducir tus resultados (BLEU-1: ~15%) sobre LSA-T, tenemos la base técnica lista para cuando lleguen los clips del sordatón.

Esto también nos permite:
- Probar CoPE (descartado en tu tesis por memoria — con GPU real debería entrar)
- Entender los hiperparámetros en la práctica, no solo en el papel
- Tener un baseline de referencia real para medir el aporte del fine-tuning con datos propios

**Pregunta para Juan:** ¿compartís el checkpoint entrenado de tu tesis? ¿Y acceso al repo con la configuración exacta que usaste?

---

## Resumen: qué desbloqueamos con GPU en junio

| Tarea | Sin GPU | Con GPU |
|---|---|---|
| Extraer keypoints de videos crudos | Lento (CPU) | Rápido |
| Pre-entrenar encoder | ❌ | ✅ |
| Replicar entrenamiento LSA-T | ❌ | ✅ |
| Probar CoPE | ❌ | ✅ |
| Fine-tuning con sordatón (agosto) | ❌ | ✅ |

**Cada semana con GPU antes del sordatón vale doble** — no solo acelera el entrenamiento final sino que construye el encoder pre-entrenado que reduce la cantidad de datos anotados necesarios.

---

## Pregunta central para Juan

> Si conseguimos GPU en junio y procesamos todos los videos GCBA sin anotar, ¿tiene sentido pre-entrenar el encoder con masked pose modeling antes del sordatón? ¿Cuánto impacto esperarías en el fine-tuning posterior? ¿Lo implementarías sobre el repo actual de Signformer o requiere una arquitectura distinta?

---

## Opciones de GPU que estamos explorando

- CCAD-UNC (Nabucodonosor) — vos lo usaste, ¿el acceso es por convenio o es abierto?
- Universidad de Córdoba (contacto propio)
- UBA (en exploración)
- Cloud pago (Colab Pro, GCP) — como último recurso
