"""
matching.py — Matching de videos locales contra YouTube.

Estrategia:
  - TF-IDF cosine similarity entre texto local (DOCX o filename) y texto YouTube (OCR o título)
  - Score combinado: tfidf (55%) + duración (35%) + bonus tema coincidente (10%)
  - El tema nunca excluye candidatos — solo suma puntos si coincide

API:
  match_videos(local_metas, yt_videos, docx_subs, ocr_data, ...) → list[dict]
  topic_from_playlist(playlist_title) → str
  topic_from_filename(filename) → str
"""

import re
import unicodedata

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ──────────────────────────────────────────────────────────────────────────────
# Mapeo de tema — extraído de los nombres reales del canal
# ──────────────────────────────────────────────────────────────────────────────

_PLAYLIST_TOPIC: dict[str, str] = {
    "Sistema Previsional":                     "Prestaciones",
    "Certificado Único de Discapacidad - CUD": "CUD",
    "Certificado Único de Discapacidad":       "CUD",
    "Salud":                                   "Salud",
    "Transporte":                              "Transporte",
    "Educación":                               "Educacion",
    "Accesibilidad":                           "Accesibilidad",
    "Beneficios Fiscales":                     "BeneficiosFiscales",
    "Trabajo":                                 "Trabajo",
    "Participación":                           "Participacion",
    "Vida Independiente":                      "VidaIndependiente",
    "Servicios Sociales Zonales":              "SSZonales",
    "Guía de Turismo 2018/2019":               "Turismo",
    "Guía de Turismo":                         "Turismo",
}

# Patterns sobre el nombre del archivo MOV → tema
# Basados en los keywords que aparecen literalmente en los nombres reales
_FILENAME_TOPIC: list[tuple[re.Pattern, str]] = [
    (re.compile(r'\bcud\b|tramite|pierde|cud\d', re.I),                       "CUD"),
    (re.compile(r'\bbf\d*\b|fiscal|franquicia', re.I),                        "BeneficiosFiscales"),
    (re.compile(r'pnc\d*|pension|jubil|retiro|ahhd|sist.?prev|\bcmo\b', re.I), "Prestaciones"),
    (re.compile(r'salud|incluir|\bbeo\b|cobertura', re.I),                    "Salud"),
    (re.compile(r'transp|pasaje|peaje|pase', re.I),                           "Transporte"),
    (re.compile(r'educ|braille|docente|cepapi|libros|ministerio|escuela', re.I), "Educacion"),
    (re.compile(r'\bacc\b|copidis|reclamo|edificio|lugr|perro.?guia|simbolo|reserva', re.I), "Accesibilidad"),
    (re.compile(r'\brul\b|feria|pquenos|pequeno|comercio', re.I),             "Trabajo"),
    (re.compile(r'\bosc\b|organiz|fortalec', re.I),                           "Participacion"),
    (re.compile(r'turismo|circuito', re.I),                                   "Turismo"),
    (re.compile(r'hogares', re.I),                                            "SSZonales"),
    (re.compile(r'vida.?indep', re.I),                                        "VidaIndependiente"),
]

# Páginas del cuadernillo sin keyword → tema por rango
_PAGE_TOPIC: list[tuple[range, str]] = [
    (range(65, 80),  "Accesibilidad"),
    (range(85, 100), "Educacion"),
]

_STOPWORDS = {
    'de', 'la', 'el', 'en', 'y', 'a', 'que', 'es', 'los', 'las', 'se', 'con',
    'para', 'un', 'una', 'por', 'del', 'al', 'como', 'si', 'o', 'su', 'sus',
    'lo', 'le', 'te', 'no', 'tu', 'mi', 'me', 'pero', 'mas', 'sin',
    'lsa', 'guia', 'informacion', 'puede', 'pueden', 'tiene', 'tienen', 'hay',
    'ser', 'podes', 'esta', 'esto', 'ese', 'esa', 'estos',
    'persona', 'personas', 'discapacidad', 'ciudad', 'buenos', 'aires',
}


# ──────────────────────────────────────────────────────────────────────────────
# Detección de tema
# ──────────────────────────────────────────────────────────────────────────────

def _normalize(s: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    ).lower()


def topic_from_playlist(playlist_title: str) -> str:
    """Tema a partir del nombre real de la playlist YouTube. 'unknown' si no reconoce."""
    norm = _normalize(playlist_title)
    for key, topic in _PLAYLIST_TOPIC.items():
        if _normalize(key) in norm:
            return topic
    return "unknown"


def topic_from_filename(filename: str) -> str:
    """Tema a partir del nombre del archivo MOV. 'unknown' si no reconoce."""
    for pattern, topic in _FILENAME_TOPIC:
        if pattern.search(filename):
            return topic
    m = re.search(r'p[.,]?\s*(\d+)', filename, re.I)
    if m:
        page = int(m.group(1))
        for page_range, topic in _PAGE_TOPIC:
            if page in page_range:
                return topic
    return "unknown"


# ──────────────────────────────────────────────────────────────────────────────
# Scoring
# ──────────────────────────────────────────────────────────────────────────────

def _dur_score(a: float | None, b: float | None) -> float:
    if not a or not b or b == 0:
        return 0.0
    return round(min(a, b) / max(a, b), 3)


# ──────────────────────────────────────────────────────────────────────────────
# Pipeline principal
# ──────────────────────────────────────────────────────────────────────────────

def match_videos(
    local_metas: list,
    yt_videos: list[dict],
    docx_subs: dict[int, str],
    ocr_data: dict[str, dict],
    dur_threshold: float = 0.60,
    score_threshold: float = 0.25,
    tfidf_weight: float = 0.55,
    dur_weight: float = 0.35,
    topic_bonus: float = 0.10,
) -> list[dict]:
    """
    Matchea videos locales contra YouTube.

    Scoring:
      score = tfidf_weight * tfidf_score
            + dur_weight   * dur_score
            + topic_bonus  * (1 si temas coinciden, 0 si no)

    El tema nunca descarta candidatos — solo suma puntos si coincide.

    Args:
        local_metas:    Lista de VideoMeta (analyze_raw.scan_folder).
        yt_videos:      Lista de dicts con video_id, title, duration_sec, playlist_title, url.
        docx_subs:      {video_num: texto} extraído del DOCX.
        ocr_data:       {video_id: {full_text, ...}} de yt_ocr.json.
        dur_threshold:  Duración mínima (ratio min/max) para considerar un par.
        score_threshold: Score mínimo para aceptar el match.

    Returns:
        Lista de dicts, uno por video YouTube, con campos de matching.
    """
    local = [m for m in local_metas if m.readable]

    def _local_text(lm) -> str:
        if lm.video_num and lm.video_num in docx_subs:
            return docx_subs[lm.video_num]
        norm = _normalize(lm.filename)
        tokens = [t for t in re.findall(r'[a-z]+', norm)
                  if t not in _STOPWORDS and len(t) > 2]
        return " ".join(tokens)

    def _yt_text(yt: dict) -> str:
        vid = yt["video_id"]
        if vid in ocr_data and ocr_data[vid].get("full_text"):
            return ocr_data[vid]["full_text"]
        return yt.get("title", "")

    local_texts = [_local_text(lm) for lm in local]
    yt_texts    = [_yt_text(yt)    for yt in yt_videos]

    # TF-IDF sobre corpus completo
    vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        stop_words=list(_STOPWORDS),
    )
    try:
        matrix     = vectorizer.fit_transform(yt_texts + local_texts)
        yt_matrix  = matrix[: len(yt_texts)]
        loc_matrix = matrix[len(yt_texts):]
        # sim[i_local, j_yt]
        sim = cosine_similarity(loc_matrix, yt_matrix)
    except ValueError:
        sim = np.zeros((len(local), len(yt_videos)))

    used_local: set[str] = set()
    results: list[dict] = []

    for j, yt in enumerate(yt_videos):
        yt_topic = topic_from_playlist(yt.get("playlist_title", ""))
        yt_dur   = yt.get("duration_sec")

        best_score = -1.0
        best_i     = -1

        for i, lm in enumerate(local):
            if lm.filename in used_local:
                continue

            d = _dur_score(yt_dur, lm.duration_s)
            if d < dur_threshold:
                continue

            t      = float(sim[i, j])
            local_topic = topic_from_filename(lm.filename)
            bonus  = topic_bonus if (yt_topic == local_topic and yt_topic != "unknown") else 0.0
            score  = round(tfidf_weight * t + dur_weight * d + bonus, 3)

            if score > best_score:
                best_score = score
                best_i     = i

        if best_i >= 0 and best_score >= score_threshold:
            lm = local[best_i]
            used_local.add(lm.filename)
            results.append({
                "yt_id":        yt["video_id"],
                "yt_title":     yt["title"],
                "yt_dur_s":     yt_dur,
                "playlist":     yt.get("playlist_title", ""),
                "yt_topic":     yt_topic,
                "local_file":   lm.filename,
                "local_dur_s":  lm.duration_s,
                "local_topic":  topic_from_filename(lm.filename),
                "has_sub":      bool(lm.video_num and lm.video_num in docx_subs),
                "dur_score":    _dur_score(yt_dur, lm.duration_s),
                "tfidf_score":  round(float(sim[best_i, j]), 3),
                "score":        best_score,
                "match":        "OK",
            })
        else:
            results.append({
                "yt_id":       yt["video_id"],
                "yt_title":    yt["title"],
                "yt_dur_s":    yt_dur,
                "playlist":    yt.get("playlist_title", ""),
                "yt_topic":    yt_topic,
                "local_file":  None, "local_dur_s": None, "local_topic": None,
                "has_sub":     False,
                "dur_score":   0, "tfidf_score": 0, "score": 0,
                "match":       "SIN MATCH",
            })

    return results
