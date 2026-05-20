"""
analyze_subtitles.py — Análisis lingüístico de un corpus de subtítulos.

Calcula métricas de trainabilidad: hapax legomena %, coverage@N, TTR, bigramas.
Soporta .txt (texto plano), .srt y .vtt (extrae solo el texto).

Uso:
    python scripts/analyze_subtitles.py data/lsa_raw/subtitles/
    python scripts/analyze_subtitles.py data/legislatura/subtitles/ --output data/docs/analisis_legislatura.json
    python scripts/analyze_subtitles.py data/legislatura/subtitles/ --no-stopwords
"""

import re
import sys
import json
import argparse
from pathlib import Path
from collections import Counter

# Stopwords del español: artículos, preposiciones, conjunciones, pronombres y
# verbos auxiliares muy frecuentes que no aportan significado léxico.
STOPWORDS_ES = {
    'de','la','que','el','en','y','a','los','del','se','las','por','un','para',
    'con','no','una','su','al','lo','como','más','pero','sus','le','ya','o',
    'este','sí','porque','esta','entre','cuando','muy','sin','sobre','también',
    'me','hasta','hay','donde','quien','desde','todo','nos','durante','todos',
    'uno','les','ni','contra','otros','ese','eso','ante','ellos','e','esto',
    'mí','antes','algunos','qué','unos','yo','otro','otras','él','tanto','esa',
    'estos','mucho','quienes','nada','muchos','cual','poco','ella','estar',
    'estas','algunas','algo','nosotros','mi','mis','tú','te','ti','tu','tus',
    'vos','usted','ustedes','os','ellas','nos','les','son','fue','ser','han',
    'era','así','ha','así','si','sea','sino','mientras','aunque','mediante',
    'es','son','está','están','fue','ser','sido','siendo','haber','hacer',
    'tiene','tienen','había','haya','hubiera','será','sería','tendría',
}


# ── Parsers de formatos ──────────────────────────────────────────────────────

def parse_txt(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore').strip()


def parse_srt(path: Path) -> str:
    text = path.read_text(encoding='utf-8', errors='ignore')
    # Eliminar números de bloque, timestamps y líneas vacías
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if re.match(r'^\d+$', line):
            continue
        if re.match(r'\d{2}:\d{2}:\d{2}', line):
            continue
        if line:
            lines.append(line)
    return ' '.join(lines)


def parse_vtt(path: Path) -> str:
    text = path.read_text(encoding='utf-8', errors='ignore')
    lines = []
    prev = None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('WEBVTT') or '-->' in line:
            continue
        # Limpiar tags de timing de YouTube: <00:00:01.234><c> palabra</c>
        line = re.sub(r'<[^>]+>', '', line).strip()
        if not line:
            continue
        # Desduplicar texto rolling: YouTube repite la línea anterior en cada bloque
        if line == prev:
            continue
        lines.append(line)
        prev = line
    return ' '.join(lines)


PARSERS = {'.txt': parse_txt, '.srt': parse_srt, '.vtt': parse_vtt}


def load_corpus(directory: Path) -> dict[str, str]:
    corpus = {}
    for path in sorted(directory.iterdir()):
        if path.suffix.lower() in PARSERS:
            text = PARSERS[path.suffix.lower()](path)
            if text:
                corpus[path.stem] = text
    return corpus


# ── Análisis lingüístico ─────────────────────────────────────────────────────

def tokenize(text: str, remove_stopwords: bool = False) -> list[str]:
    tokens = re.findall(r'\b\w+\b', text.lower())
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS_ES]
    return tokens


def ngrams(tokens: list[str], n: int) -> list[tuple]:
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def coverage_at(word_freq: Counter, n: int) -> float:
    if not word_freq:
        return 0.0
    return sum(1 for c in word_freq.values() if c >= n) / len(word_freq) * 100


def analyze(corpus: dict[str, str]) -> dict:
    all_tokens = []
    per_entry  = []

    for stem, text in corpus.items():
        toks = tokenize(text)
        all_tokens.extend(toks)
        ttr = len(set(toks)) / len(toks) if toks else 0
        per_entry.append({'stem': stem, 'tokens': len(toks), 'types': len(set(toks)), 'ttr': round(ttr, 3)})

    word_freq  = Counter(all_tokens)
    all_types  = set(all_tokens)
    hapax      = [w for w, c in word_freq.items() if c == 1]
    hapax_pct  = len(hapax) / len(all_types) * 100 if all_types else 0
    ttr_global = len(all_types) / len(all_tokens) if all_tokens else 0

    top_bigrams  = Counter(ngrams(all_tokens, 2)).most_common(15)
    top_trigrams = Counter(ngrams(all_tokens, 3)).most_common(10)

    # Vocabulario léxico: mismas frecuencias pero sin stopwords, solo para contexto
    lex_freq = Counter({w: c for w, c in word_freq.items() if w not in STOPWORDS_ES})

    result = {
        'n_documentos'  : len(corpus),
        'tokens_totales': len(all_tokens),
        'vocab_unico'   : len(all_types),
        'ttr_global'    : round(ttr_global, 3),
        'hapax_count'   : len(hapax),
        'hapax_pct'     : round(hapax_pct, 1),
        'coverage_at_2' : round(coverage_at(word_freq, 2), 1),
        'coverage_at_5' : round(coverage_at(word_freq, 5), 1),
        'coverage_at_10': round(coverage_at(word_freq, 10), 1),
        'top_bigrams'   : [[' '.join(bg), c] for bg, c in top_bigrams],
        'top_trigrams'  : [[' '.join(tg), c] for tg, c in top_trigrams],
        'top_palabras'  : [[w, c] for w, c in word_freq.most_common(20)],
        'top_palabras_lexicas': [[w, c] for w, c in lex_freq.most_common(20)],
        'por_documento' : per_entry,
    }
    return result


def print_report(r: dict) -> None:
    print()
    print('=' * 55)
    print('ANÁLISIS LINGÜÍSTICO — MÉTRICAS DE TRAINABILIDAD')
    print('=' * 55)
    print(f'  Documentos          : {r["n_documentos"]}')
    print(f'  Tokens totales      : {r["tokens_totales"]}')
    print(f'  Vocabulario único   : {r["vocab_unico"]} palabras')
    print(f'  TTR global          : {r["ttr_global"]:.3f}')
    print()
    print(f'  Hapax legomena      : {r["hapax_count"]} palabras ({r["hapax_pct"]:.1f}%)')
    print(f'  Coverage@2  (≥2x)  : {r["coverage_at_2"]:.1f}%')
    print(f'  Coverage@5  (≥5x)  : {r["coverage_at_5"]:.1f}%')
    print(f'  Coverage@10 (≥10x) : {r["coverage_at_10"]:.1f}%')
    print()

    hapax_pct = r['hapax_pct']
    if hapax_pct > 40:
        print('  ⚠  Hapax >40% → vocabulario muy disperso.')
        print('     Mismo problema que LSA-T. Difícil entrenar sin más datos.')
    elif hapax_pct > 20:
        print('  ~  Hapax 20-40% → repetición insuficiente.')
        print('     Considerar acotar dominio o generar datos propios.')
    else:
        print('  ✓  Hapax <20% → vocabulario acotado. Trainabilidad razonable.')

    print()
    print('  Top 10 bigramas:')
    for bg, c in r['top_bigrams'][:10]:
        print(f'    {c:>3}x  {bg}')

    print()
    print('  Top 10 palabras (con stopwords):')
    for w, c in r['top_palabras'][:10]:
        print(f'    {c:>4}x  {w}')

    print()
    print('  Top 10 palabras léxicas (sin stopwords — solo para contexto):')
    for w, c in r['top_palabras_lexicas'][:10]:
        print(f'    {c:>4}x  {w}')
    print()


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Análisis lingüístico de subtítulos')
    parser.add_argument('directory', help='Directorio con archivos .txt / .srt / .vtt')
    parser.add_argument('--output', '-o', help='Guardar resultado en JSON (opcional)')
    parser.add_argument('--save-clean', metavar='DIR',
                        help='Guardar texto limpio (sin timestamps ni duplicados) en DIR/')
    args = parser.parse_args()

    directory = Path(args.directory)
    if not directory.is_dir():
        print(f'Error: {directory} no es un directorio válido')
        sys.exit(1)

    corpus = load_corpus(directory)
    if not corpus:
        print(f'No se encontraron archivos .txt/.srt/.vtt en {directory}')
        sys.exit(1)

    print(f'Archivos encontrados: {len(corpus)}')

    if args.save_clean:
        clean_dir = Path(args.save_clean)
        clean_dir.mkdir(parents=True, exist_ok=True)
        lex_dir = clean_dir / 'sin_stopwords'
        lex_dir.mkdir(parents=True, exist_ok=True)
        for stem, text in corpus.items():
            # Texto completo limpio
            (clean_dir / f'{stem}.txt').write_text(text, encoding='utf-8')
            # Texto sin stopwords
            tokens_lex = tokenize(text, remove_stopwords=True)
            (lex_dir / f'{stem}.txt').write_text(' '.join(tokens_lex), encoding='utf-8')
        print(f'Textos limpios guardados en: {clean_dir}')
        print(f'Textos sin stopwords en    : {lex_dir}')

    result = analyze(corpus)
    print_report(result)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f'Resultado guardado en: {out}')


if __name__ == '__main__':
    main()
