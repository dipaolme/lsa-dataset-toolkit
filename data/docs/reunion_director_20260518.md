# Reunión de seguimiento semanal — Director
**18 mayo 2026**

---

## Hilo narrativo

### 1. El material que existe — curación del canal GCBA (5 min)
*Mostrar: `raw_lsa.xlsx`*

- El canal YouTube GCBA tiene videos en LSA. Curé la playlist completa la semana pasada.
- `raw_lsa.xlsx` es el catálogo curado: qué videos sirven, cuáles no, por qué.
- De ese universo, seleccioné 29 casos limpios para construir el primer dataset de prueba.

**Mensaje:** tenemos material. El problema no es conseguir videos — es que el material existente tiene limitaciones estructurales (ver punto 3).

---

### 2. El dataset de prueba — 29 casos (5 min)
*Mostrar: notebook `toy_dataset_analysis.ipynb` — Sección 1*

- Extraje keypoints (MediaPipe) de los 29 videos → formato compatible con Signformer/LSA-T.
- Métricas de calidad: pose 100%, cara 100%, manos ~80%. El pipeline funciona.
- Duración media: 24s por clip. LSA-T promedia 9s → nuestros clips son 3x más largos, requieren segmentación.

**Mensaje:** el pipeline técnico está validado. Podemos procesar videos y generar el formato que necesita el modelo.

---

### 3. El problema del corpus — análisis lingüístico (5 min)
*Mostrar: notebook — Sección 2 / output de `analyze_subtitles.py`*

- Medimos trainabilidad del corpus con 3 índices: TTR, Hapax legomena, Coverage@N.
- **Resultado:** 61.8% de hapax en nuestros 29 casos. Mismo problema que LSA-T (>50%).
- Hicimos el mismo análisis sobre subtítulos de la Legislatura porteña: 55.4% de hapax.
- **Conclusión:** anotar y sincronizar los videos existentes probablemente no alcance para que el modelo converja. El vocabulario es demasiado disperso.

**Mensaje:** el problema no es técnico — es estadístico. Necesitamos vocabulario acotado y repetitivo.

---

### 4. La decisión estratégica (10 min)
*Mostrar: `roadmap_avatar_ai.md`*

Hay dos caminos:

**Path A — curar videos existentes**
Anotar y sincronizar los videos del canal GCBA.
Problema: vocabulario disperso, mismo resultado que LSA-T. Mucho trabajo, resultado incierto.

**Path B — generar nuestro dataset (sordatón)**
Grabar videos propios con vocabulario controlado, clips cortos, intent labels desde el diseño.
Un evento genera DOS outputs: clips de entrenamiento + clips de respuesta para el avatar.

**Decisión tomada: Path B.** El Path A sirve como pre-entrenamiento, no como dataset principal.

---

### 5. La herramienta de anotación (5 min)
*Mostrar: script `fetch_playlist_subs.py` + output limpio*

- Exploré herramientas para que intérpretes o agentes de la sociedad civil anoten videos.
- Bajamos subtítulos automáticos de YouTube (Legislatura) y los limpiamos automáticamente.
- El grupo aliado podría construir una herramienta de anotación sobre esta base — o directamente entrenar el modelo si Juan no tiene disponibilidad.

**Mensaje:** hay alternativas si la dependencia de Juan se complica.

---

### 6. Qué podemos hacer YA — sin data anotada (5 min)
*Mostrar: `propuesta_gpu_preentrenamiento.md`*

Si conseguimos GPU antes del sordatón (junio):

- Pre-entrenar el encoder con todos los videos GCBA sin anotar (auto-supervisado, sin texto).
- Replicar el entrenamiento de Bratti sobre LSA-T → pipeline validado para cuando lleguen los datos propios.
- Probar CoPE (módulo que Bratti no pudo testear por memoria).

**Mensaje:** la GPU no desbloquea solo el entrenamiento final — desbloquea trabajo técnico que se puede hacer en paralelo al sordatón.

---

### 7. Arquitectura del POC — lo que le vas a mostrar al usuario (3 min)

```
persona firma → keypoints → Signformer → texto clave
                                              ↓
                                    clasificador de intención
                                              ↓
                                        LLM / agente
                                              ↓
                                    respuesta en pantalla
                                    + video LSA pre-grabado
```

Dos tracks paralelos: Track A (traducción) + Track B (intención).
El avatar del POC son videos pre-grabados — no síntesis. La síntesis es 2027.

---

## Bloqueantes a resolver (para que el director ayude)

| Bloqueante | Urgencia | Quién puede resolver |
|---|---|---|
| GPU | Alta | CCAD-UNC / Córdoba / UBA / cloud |
| Fecha sordatón | Alta | Sebastián + comunidad sorda |
| Reunión Juan Bratti | Alta | Matías (mensaje enviado) |
| Rol del grupo aliado | Media | Matías |
| Conversación avatar 2027 vs POC | Media | Matías + director |
