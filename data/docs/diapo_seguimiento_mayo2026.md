# Reunión de Seguimiento — Mayo 2026
## Contenido para diapositivas

---

## Diapositiva 1 — Relevamiento de fuentes de datos

**Formato:** similar al template de seguimiento (número grande + flecha + detalle)

**Objetivo:** Identificar material de video en Lengua de Señas Argentina con texto sincronizado y curado para entrenar el modelo

**Status:** El relevamiento confirma insuficiencia de material listo para entrenar. Dos acciones en curso.

---

| Número | Fila | Detalle |
|---|---|---|
| **2** | **Fuentes relevadas** | Canal YouTube GCBA (COPIDIS) · Sesión Legislatura |
| **103 videos · 1 sesión** | **Material analizado** | COPIDIS: ~10 hs totales, solo 41 min curados · Legislatura: sesión completa disponible |
| **3** | **Limitaciones identificadas** | Legislatura: recuadro reducido · subtítulos sin curar · vocabulario amplio |

**Acciones en curso:**
- Material crudo Legislatura solicitado
- Alianza Signai activada · servidor compartido operativo

**En evaluación:** generación de video propio con vocabulario acotado de trámites GCBA

---

## Diapositiva 2 — Síntesis / Avatar (backup)

**Subtítulo:** Primeros pasos hacia el avatar que responde

---

**Pipeline construido:** video del señario CAS → extracción automática del movimiento → animación

| Etapa | Descripción | Estado |
|---|---|---|
| Fuente | Señario de la Confederación Argentina de Sordos (CAS): diccionario visual palabra → video | Identificado |
| Extracción | Captura automática del movimiento: posición, ángulo y forma de la mano frame a frame | Operativo |
| Animación | Dos prototipos evaluados: avatar humanizado y visualizador de esqueleto fiel al movimiento real | Funcionando |

**Conclusión**

Se cuenta con una fuente de datos para el avatar y un pipeline funcional. Primera seña automatizada: FEBRERO. El próximo paso es evaluar con la comunidad sorda qué presentación es más clara para el usuario final.
