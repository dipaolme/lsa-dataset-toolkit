# Análisis lingüístico — Legislatura CABA
**Fuente:** subtítulos automáticos YouTube · 1 sesión completa

---

## Métricas de trainabilidad

| Métrica | Valor |
|---|---|
| Documentos | 1 |
| Tokens totales | 41.770 |
| Vocabulario único | 6.000 palabras |
| TTR global | 0.144 |
| **Hapax legomena** | **3.324 palabras (55.4%)** |
| Coverage@2 (≥2x) | 44.6% |
| Coverage@5 (≥5x) | 17.2% |
| Coverage@10 (≥10x) | 8.4% |

> ⚠ **Hapax >40% → vocabulario muy disperso. Mismo problema que LSA-T.**

---

## Vocabulario frecuente

**Top 10 palabras (con stopwords):**

| Frecuencia | Palabra |
|---:|---|
| 2545x | de |
| 1864x | que |
| 1789x | la |
| 1086x | y |
| 1058x | el |
| 1023x | en |
| 880x | a |
| 637x | los |
| 627x | no |
| 515x | con |

**Top 10 palabras léxicas (sin stopwords — para entender el dominio):**

| Frecuencia | Palabra |
|---:|---|
| 348x | ciudad |
| 321x | eh |
| 134x | gobierno |
| 128x | buenos |
| 124x | aires |
| 111x | jefe |
| 110x | gracias |
| 104x | ley |
| 94x | año |
| 92x | gabinete |

**Top 10 bigramas:**

| Frecuencia | Bigrama |
|---:|---|
| 440x | de la |
| 284x | la ciudad |
| 187x | en la |
| 151x | de los |
| 131x | en el |
| 124x | buenos aires |
| 123x | que se |
| 119x | lo que |
| 114x | a la |
| 113x | de buenos |

---

## Interpretación

El problema no es técnico — es **estadístico**. El modelo aprende por repetición. Si una palabra aparece 1-2 veces en todo el corpus, no hay suficiente señal para que el gradiente aprenda la correspondencia seña→palabra. Simplemente no converge en esa parte del vocabulario.

Anotar y sincronizar videos no cambia ese número. Podés tener los 41.770 tokens perfectamente sincronizados con las señas correspondientes, y el modelo igual va a aprender "de", "la", "ciudad" y no va a poder predecir "presupuesto", "municipalidad" o "licitación" que aparecen 1-2 veces.

---

## Qué cambia el panorama

1. **Más sesiones del mismo dominio** — con 20 sesiones de Legislatura el hapax cae porque el vocabulario legislativo es repetitivo: "sesión", "diputados", "proyecto de ley", "Buenos Aires" acumulan cientos de apariciones.

2. **Dominio más acotado** — tomando solo debates sobre un tema (presupuesto, educación, salud), el vocabulario significativo se repite mucho más.

3. **Clasificador de intención (Track B)** — no necesita predecir texto libre, solo distinguir entre 15-25 intenciones. Con vocabulario acotado y etiquetas de intent, 55% de hapax deja de ser un problema fatal.

---

## Conclusión para la reunión con Juan

> Los videos de Legislatura son útiles para **pre-entrenar el encoder** (señas → representación), pero probablemente no sean suficientes para que el **Track A** (Signformer → texto) converja con vocabulario abierto. El **Track B** (clasificador de intención) es el camino realista para el POC de diciembre.
