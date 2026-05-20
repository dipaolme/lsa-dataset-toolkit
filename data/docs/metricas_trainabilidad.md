# Métricas de trainabilidad del corpus

---

## TTR — Type-Token Ratio

Divide el número de palabras únicas (*types*) por el total de palabras (*tokens*).

```
"el gato come el pescado" → tokens: 5, types: 4 ("el" se repite)
TTR = 4/5 = 0.80
```

Mide diversidad léxica global. **Problema:** sube artificialmente en corpus chicos. Con 29 clips cortos, nuestro TTR va a parecer bueno aunque el vocabulario sea disperso.

---

## Hapax Legomena %

Porcentaje de palabras únicas que aparecen **exactamente una sola vez** en todo el corpus.

```
corpus: "el perro come, el gato duerme, el pájaro vuela"

"perro", "come", "gato", "duerme", "pájaro", "vuela" → aparecen 1 vez
"el" → aparece 3 veces

hapax = 6/7 palabras únicas = 85%
```

Es el **índice más importante para trainabilidad**. Si una palabra aparece solo una vez, el modelo no puede aprender a predecirla — no hay patrón que aprender.

- LSA-T tiene >50% de hapax → ya es difícil de entrenar
- Nuestro corpus GCBA: **61.8%** → peor que LSA-T

---

## Coverage@N

Porcentaje de palabras únicas que aparecen **al menos N veces**.

```
Coverage@5 = 9.6% → solo el 9.6% del vocabulario aparece 5 o más veces
```

Complementa al hapax: mientras hapax mide el "piso" (palabras que aparecen solo 1 vez), coverage@N mide cuánto vocabulario tiene repetición suficiente para aprender.

**¿Por qué "palabras únicas que aparecen N veces" no es contradictorio?**

"Únicas" se refiere a entradas del diccionario — cada palabra distinta cuenta una sola vez como ítem, sin importar cuántas veces aparece. Coverage@N pregunta: de ese diccionario, ¿cuántas entradas tienen frecuencia ≥ N?

```
corpus: "trámite trámite trámite DNI DNI turno"

vocabulario: ["trámite", "DNI", "turno"] → 3 entradas

Coverage@2: "trámite"(3x), "DNI"(2x) → 2/3 = 66%
Coverage@5: ninguna → 0/3 = 0%
```

Una forma más clara de leerlo: **"¿qué porcentaje del diccionario está bien representado?"**

- Hapax = el peor extremo → mal representado
- Coverage@5 = palabras que el modelo va a poder aprender

Para entrenar un modelo, querés que la mayor parte del vocabulario esté en Coverage@5 o más.

---

## Resumen

| Índice | Pregunta que responde | Corpus GCBA (29 casos) |
|---|---|---|
| TTR | ¿Qué tan diverso es el vocabulario? | ~0.34 (engañoso en corpus chico) |
| Hapax % | ¿Cuántas palabras son "irrepetibles"? | **61.8%** ← el problema |
| Coverage@5 | ¿Cuántas palabras tienen suficiente repetición? | **9.6%** ← muy bajo |
