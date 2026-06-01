---
name: feedback-utils-structure
description: Preferencia sobre estructura utils/ y organización de scripts
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1a8ff457-40e7-4b80-83b1-13ff5ed1481b
---

Código reutilizable va en `utils/` (raíz del proyecto), archivos temáticos con CLI via argparse.

**Why:** El usuario lo pidió explícitamente para mantener orden y reusabilidad.

**How to apply:** Antes de agregar código reutilizable a un notebook o script, evaluar si pertenece a `utils/`.

⚠ **Nota (mayo 2026):** `utils/catalog.py`, `subtitles.py` y `video.py` fueron **eliminados** en commit 2c4d745 (consolidados en scripts o descartados). Lo que queda en utils/: `registry.py`, `docx_parser.py`, `matching.py`, `ocr.py`. No asumir que todos los utils anteriores siguen existiendo.
