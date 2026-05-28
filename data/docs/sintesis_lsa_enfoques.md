# Síntesis LSA: Comparación de Enfoques

**Fecha:** 2026-05-28  
**Contexto:** Evaluación técnica post-exploración señario CAS → Animator (Jorge)

---

## Objetivo

Dado un texto en español → generar una animación de un avatar señando en LSA.  
Pipeline mínimo: palabra → secuencia de keypoints → avatar animado.

---

## Approach A — Conversión a Animator (Jorge)

**Cómo funciona:**  
Keypoints MediaPipe → parámetros abstractos → motor IK del Animator

```
video señario
    ↓
MediaPipe (21 landmarks/frame por mano)
    ↓  conversión
wrist (x,y) + angle + curls[5]
    ↓
WORD_DICTIONARY en app.js
    ↓
Avatar IK + renderizado procedural
```

**Lo que funciona bien:**
- Avatar con buena presentación visual (humanoide con ropa, cara, interpolación suave)
- Alfabeto dactilológico implementado (fallback para palabras no conocidas)
- Código base funcionando

**Desafíos de conversión identificados:**

| Problema | Descripción | Severidad |
|---|---|---|
| Selección de keyframes | Hoy es manual. Necesita algoritmo (velocidad + cambio de ángulo) | Alta |
| Mapeo de coordenadas | Mapeo simple no funciona. Necesita anclar a hombros del señante como referencia corporal | Alta |
| Curl formula | Subestima el cierre cuando la mano apunta hacia/desde cámara. Necesita cálculo de ángulos entre joints | Media |
| IK cross-body | Gestos cruzados requieren lógica adicional | Media |
| Fidelidad de forma | Solo 5 valores de curl — no representa dedos juntos, separados, rotación 3D | Alta |
| Escala | Cada palabra requiere ajuste manual iterativo. No viable para 100+ palabras | Crítica |

---

## Approach B — Renderizado Directo de Keypoints

**Cómo funciona:**  
Keypoints MediaPipe → dibujar esqueleto frame a frame — sin conversión, sin IK

```
video señario
    ↓
MediaPipe (21 landmarks/frame por mano)
    ↓  sin conversión
dibujar esqueleto frame a frame en canvas
```

**Conexiones del esqueleto de mano (21 puntos):**
```
Muñeca → base → pip → dip → tip  (4 segmentos × 5 dedos)
Palma: conexiones entre bases (5-9-13-17)
```

**Ventajas:**
- Pipeline 100% automático — sin ajuste manual por palabra
- Fiel a la seña real (sin pérdida de información)
- Escala directamente a todo el señario
- Bajo costo de implementación
- Útil como herramienta de validación: permite ver exactamente qué detectó MediaPipe

**Desafíos:**
- Presentación visual: esqueleto, no avatar humanizado
- Normalización: el señante puede estar en distintas posiciones del frame
- Depende de la calidad del video del señario (iluminación, fondo, oclusiones)

---

## Comparación de puntos (features)

| Parte del cuerpo | Features actuales | Para síntesis A | Para síntesis B |
|---|---|---|---|
| Mano derecha | 42 (21 kp × 2) | 42 + angle + curls[5] | 42 (directo) |
| Mano izquierda | 42 | opcional | opcional |
| Pose (cuerpo) | 66 (33 kp × 2) | Solo ~6 (hombros, codos, muñecas) | Solo ~6 como referencia |
| Cara | 936 (468 kp × 2) | ❌ no necesario | ❌ no necesario |
| **Total actual** | **1086** | ~90 efectivos | ~90 efectivos |

**¿Se pueden cambiar los puntos?**

- MediaPipe HandLandmarker da exactamente **21 puntos por mano** — no se puede aumentar
- Se puede agregar **coordenada Z** (profundidad): 42 → 63 features por mano. Útil para capturar rotación de mano hacia/desde cámara
- Reducir a manos + 6 pose: ~**150 features** en lugar de 1086 → más liviano, suficiente para síntesis
- **Trade-off:** reducir rompe compatibilidad con Signformer (espera 1086). Habría que mantener dos formatos
