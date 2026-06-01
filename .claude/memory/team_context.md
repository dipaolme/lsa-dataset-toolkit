---
name: team-and-context
description: "Roles del equipo Avatar AI, alianzas activas/inactivas, situación GPU — junio 2026"
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

**Última actualización:** 2026-06-01

## Matías (usuario) — ver [[user-profile]]
PO/PM técnico. Único recurso interno full-time.

## Juan Bratti (externo — CLAVE)
- Rol: entrenar el modelo, asesorar formato del dataset.
- Hizo su tesis entrenando Signformer sobre LSA-T (trabajo de Pedro Dal Bianco).
- **Dependencia crítica** para todo lo que es entrenamiento.
- Reunión siguiente pendiente.

## Jorge (fronton técnico)
- Integró el skeleton viewer 2D en su servidor Flask. Pidió 3D → construido.
- Fix IK cross-body pendiente de commitear en repo Animator.
- El que tiene que empujar es Matías.

## Sebastián Tsuji (director / stakeholder)
- Responsable: videos GCBA, comunidad sorda, pruebas con usuarios.
- Quiere ver avatar que responde en LSA → solución POC: videos pre-grabados.
- Conversación pendiente: "avatar visión 2027" vs "avatar simulado POC".

## Pedro Dal Bianco (NUEVO — CLAVE)
- Creador de LSA-T y arquitectura Signformer (base técnica del proyecto).
- Contactado vía LinkedIn 01/06/2026. Respondió positivamente.
- De viaje próximas semanas. Mail: dalbianco.pedro@gmail.com
- Paper reciente sobre augmentación LLM para SLT (arXiv:2605.31393)
- Mail de presentación y consulta redactado → `data/docs/mail_pedro_dal_bianco.md`
- Ver [[pedro-dal-bianco]] para detalle completo.

## Signai (alianza — grupo de estudiantes/investigadores)
- Respondieron positivamente. Reunión agendada miércoles o jueves de la semana del 01/06.
- Material ya subido al servidor, pendiente darles acceso.
- Objetivo: anotación y curación del material existente.
- Contacto: Federico (del equipo Signai).

## Alianzas

| Alianza | Estado | Notas |
|---|---|---|
| Juan Bratti | Activa | Reunión siguiente pendiente |
| Pedro Dal Bianco | Nueva — en proceso | Mail por enviar, de viaje |
| UNLP | En preparación | Pitch listo en `data/docs/alianza_unlp.txt` |
| Signai | Activa | Reunión semana 01/06, acceso al material pendiente |
| Universidad de Córdoba | En exploración | Contacto de Matías, alternativa GPU/dataset |
| UBA | En exploración | Exploración inicial |
| Microsoft (GPU) | Descartada | Jorge no lo consiguió |

## GPU — situación
Sin GPU Juan no puede entrenar. Alternativas activas:
- CCAD-UNC (Juan lo usó antes)
- Universidad de Córdoba (contacto de Matías)
- UBA (exploración inicial)
- Colab Pro / GCP (cloud pago)

**How to apply:** El proyecto depende fuertemente de alianzas. Pedro Dal Bianco es ahora el contacto técnico más estratégico. Antes de planificar trabajo técnico, verificar si hay GPU disponible y si Juan Bratti tiene agenda libre.
