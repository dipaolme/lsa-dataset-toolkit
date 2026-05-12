"""Parse Guia Subs.docx — mapea N° DSC → texto de subtítulo."""
import re
from dataclasses import dataclass
from pathlib import Path

from docx import Document


@dataclass
class VideoSub:
    video_num: int
    note: str
    text: str


_ENTRY = re.compile(
    r'N[°º]\s*(\d+)\s*(?:\(([^)]*)\))?\s*[:\.]?\s*(.*)',
    re.DOTALL,
)


def parse_subs_docx(path: Path) -> list[VideoSub]:
    """Parsea el DOCX y devuelve lista de VideoSub ordenada por número."""
    doc = Document(str(path))
    subs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        m = _ENTRY.match(text)
        if not m:
            continue
        subs.append(VideoSub(
            video_num=int(m.group(1)),
            note=(m.group(2) or "").strip(),
            text=m.group(3).strip(),
        ))
    return subs


if __name__ == "__main__":
    import sys
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "data/raw/GUÍA INFO LSA 2018-2019/Guia Subs.docx"
    )
    subs = parse_subs_docx(path)
    print(f"Total subtítulos parseados: {len(subs)}\n")
    for s in subs:
        print(f"N° {s.video_num:4d}  {s.text[:80]}...")
