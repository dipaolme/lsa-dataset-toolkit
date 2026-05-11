"""
parse_subs_docx.py — Re-exporta desde utils/docx_parser para compatibilidad
con notebooks y código existente que importa desde scripts/.
"""
from pathlib import Path
from utils.docx_parser import parse_subs_docx, VideoSub  # noqa: F401


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
    import sys
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "data/raw/GUÍA INFO LSA 2018-2019/Guia Subs.docx"
    )
    subs = parse_subs_docx(path)
    print(f"Total subtítulos parseados: {len(subs)}\n")
    for s in subs:
        print(f"N° {s.video_num:4d}  {s.text[:80]}...")
