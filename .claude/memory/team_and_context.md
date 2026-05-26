---
name: team-and-context
description: "Roles reales del equipo, alianzas activas/inactivas, y contexto del proyecto Avatar AI — actualizado 2026-05-26"
metadata: 
  node_type: memory
  type: project
  updated: 2026-05-26
  originSessionId: 9370954d-c2d9-47e4-8057-939c81870dfc
---

## Matías (usuario)
- Rol: PO/PM técnico. Único recurso interno full-time.
- Responsable de: diseño de dataset, coordinación con Juan Bratti, agente inteligente, Avatar LSA (futuro).
- No es principalmente desarrollador — coordina y toma decisiones técnicas.

**Why:** El proyecto Avatar AI depende casi 100% de alianzas externas para ML/entrenamiento.

---

## Equipo real (Mayo 2026)

### Juan Bratti (externo — CLAVE)
- Rol: entrenar el modelo, asesorar formato del dataset, compartir checkpoint LSA-T.
- Estado: **NO respondió** mensaje de LinkedIn enviado ~15/05/2026 (10+ días sin respuesta).
- Próxima acción: Matías tiene su email, enviar hoy 26/05/2026.
- Es la dependencia crítica para entrenamiento Y para saber cuántos clips grabar en el sordatón.

### Jorge (ACTIVO — rol confirmado)
- Estado: **activo y comprometido**. Rol anterior incierto, ahora confirmado.
- Trabajando en DOS cosas:
  1. **Pipeline de síntesis**: lenguaje natural → glosas → secuencia de señas → keypoints → representación (el avatar que responde)
  2. **Servidor**: montando servidor para hostear el material del proyecto
- Reuniones semanales con Matías × 3 total. Primera ya realizada.
- Próxima reunión: 26/05/2026 a las 16:30.
- También sirve de apoyo general al proyecto.

### Sebastián
- Responsable: videos GCBA, comunidad sorda, pruebas con usuarios.
- Los intérpretes son material escaso — requieren plan definido o propuesta concreta antes de convocarlos.

### Director (Sebastián Tsuji)
- Reunión realizada: 18/05/2026.
- Entendió los 2 tracks (Track A traducción + Track B intent).
- Quiere seguir recolectando videos aunque no haya quien los anote todavía.
- Quiere algo demostrable para diciembre (POC).
- Puede ayudar a resolver: GPU, fecha sordatón, reunión Juan.

### Grupo de estudiantes (alianza)
- Construyendo herramienta de captura + anotación (OBS + Python + interfaz).
- Esperan specs: duración clips, lista de intents, protocolo de grabación.
- Specs se pueden dar cuando Matías tenga taxonomía de intents + respuesta de Juan.

---

## Alianzas

| Alianza | Estado | Notas |
|---|---|---|
| Juan Bratti | Activa pero sin respuesta | Email pendiente de enviar 26/05 |
| Jorge | ✅ Activa | Síntesis + servidor. Reuniones semanales. |
| Grupo estudiantes | Activa | Esperando specs |
| Universidad de Córdoba | En exploración | Contacto de Matías, posible GPU |
| UBA | En exploración | Inicial |
| UNLP | ❌ Inactiva | No respondieron |
| Microsoft GPU | ❌ Descartada | |

---

## GPU — situación

Sin resolución. Opciones activas:
- Universidad de Córdoba (contacto propio de Matías)
- UBA (exploración)
- Colab Pro (~10 USD/mes) — alcanza si hay fine-tuning desde checkpoint de Juan
- CCAD-UNC (Nabucodonosor) — Juan lo usó en su tesis, acceso por convenio UNC

**Importante:** no vale la pena resolver GPU hasta saber si Juan hace fine-tuning desde su checkpoint o desde cero. Eso define cuánta GPU necesitás.

---

## Intérpretes / Sordatón
- Intérpretes son escasos. El director lo dijo explícitamente.
- No convocarlos sin: (a) taxonomía de intents definida, (b) protocolo de grabación, (c) saber cuántos clips necesitás.
- Target: julio-agosto 2026.

**How to apply:** Jorge está activo — en cada sesión preguntar estado de síntesis y servidor. Juan sigue siendo el bloqueante crítico — hasta que responda, enfocar trabajo en lo que no lo requiere.
