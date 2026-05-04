"""Parse Guia Subs.docx — maps DSC video N° to subtitle text."""
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from docx import Document


@dataclass
class VideoSub:
    video_num: int
    note: str       # e.g. 'arranca 00:24s', 'primera parte + 1028'
    text: str


# Matches: N° 795: texto  |  N° 812 (nota): texto  |  N° 818 (nota) texto
_ENTRY = re.compile(
    r'N[°º]\s*(\d+)\s*(?:\(([^)]*)\))?\s*[:\.]?\s*(.*)',
    re.DOTALL,
)


def parse_subs_docx(path: Path) -> list[VideoSub]:
    doc = Document(str(path))
    subs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        m = _ENTRY.match(text)
        if not m:
            continue
        num = int(m.group(1))
        note = (m.group(2) or "").strip()
        content = m.group(3).strip()
        subs.append(VideoSub(video_num=num, note=note, text=content))
    return subs


def topic_from_text(text: str) -> str:
    """Heuristic topic label from subtitle text."""
    text_lower = text.lower()
    if any(k in text_lower for k in ["cud", "certificado único"]):
        return "CUD"
    if any(k in text_lower for k in ["salud", "obra social", "cobertura", "médica", "incluir salud"]):
        return "Salud"
    if any(k in text_lower for k in ["transporte", "pase libre", "peaje", "pasaje"]):
        return "Transporte"
    if any(k in text_lower for k in ["educación", "escuela", "beca", "ministerio de educación", "braille", "docente"]):
        return "Educación"
    if any(k in text_lower for k in ["empleo", "trabajo", "pil", "pet", "pei", "laboral", "inserción"]):
        return "Empleo"
    if any(k in text_lower for k in ["pensión", "jubil", "retiro", "prestación", "pnc"]):
        return "Prestaciones"
    if any(k in text_lower for k in ["accesibilidad", "edificio", "barrera", "reclamo", "copidis"]):
        return "Accesibilidad"
    if any(k in text_lower for k in ["comercio", "feria", "artesanal", "fortalecimiento", "osc", "organización"]):
        return "Emprendimiento"
    if any(k in text_lower for k in ["discapacidad", "perro guía", "símbolo", "reserva", "franquicia", "estacionamiento"]):
        return "Derechos"
    if any(k in text_lower for k in ["turismo", "ba accesible", "app"]):
        return "Turismo/Digital"
    return "Otro"


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "data/raw/GUÍA INFO LSA 2018-2019/Guia Subs.docx"
    )
    subs = parse_subs_docx(path)
    print(f"Total subtítulos parseados: {len(subs)}\n")
    for s in subs:
        print(f"N° {s.video_num:4d}  [{topic_from_text(s.text):15s}]  {s.text[:80]}...")
