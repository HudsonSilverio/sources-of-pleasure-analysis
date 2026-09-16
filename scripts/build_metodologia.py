"""
build_metodologia.py — Assemble the methodology document.

Concatenates the chapter files in outputs/reports/metodologia/ in a fixed
order and writes outputs/reports/metodologia_completa.md with a table of
contents. Chapters that do not exist yet are skipped with a warning, so the
document can be rebuilt at any point while chapters are still being written.

Usage:
    python scripts/build_metodologia.py
"""

from datetime import datetime
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHAPTER_DIR = PROJECT_ROOT / "outputs" / "reports" / "metodologia"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "reports" / "metodologia_completa.md"

# Ordem fixa dos capitulos. Um arquivo ausente e pulado com aviso.
CHAPTERS = [
    "00_arquitetura.md",
    "01_rastreabilidade.md",
    "fase0_instrumento.md",
    "fase1_limpeza.md",
    "fase2_descritiva.md",
    "fase3_eda.md",
    "fase4_hipoteses.md",
    "fase5_6_analistas.md",
    "fase7_integrador.md",
    "fase8_banco_insights.md",
    "fase9_storytelling.md",
]

TITLE = "Sources of Pleasure — Memorial descritivo da análise"


def first_heading(text):
    """Return the first level-1 heading of a chapter, or None."""
    m = re.search(r"^# (.+)$", text, flags=re.MULTILINE)
    return m.group(1).strip() if m else None


def slugify(title):
    """GitHub-style anchor for a heading (good enough for our titles)."""
    s = title.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def main():
    present, missing = [], []
    for name in CHAPTERS:
        path = CHAPTER_DIR / name
        if path.exists():
            present.append(path)
        else:
            missing.append(name)

    toc_lines = []
    body_parts = []
    for path in present:
        text = path.read_text(encoding="utf-8").rstrip() + "\n"
        title = first_heading(text) or path.stem
        toc_lines.append(f"- [{title}](#{slugify(title)})")
        body_parts.append(text)

    header = (
        f"# {TITLE}\n\n"
        f"*Documento gerado por `scripts/build_metodologia.py` em "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')} a partir de "
        f"{len(present)} capítulo(s) em `outputs/reports/metodologia/`.*\n\n"
        "## Sumário\n\n" + "\n".join(toc_lines) + "\n\n---\n\n"
    )

    OUTPUT_PATH.write_text(header + "\n\n---\n\n".join(body_parts), encoding="utf-8")

    print(f"Capítulos incluídos ({len(present)}):")
    for p in present:
        print(f"  + {p.name}")
    if missing:
        print(f"Capítulos ainda não escritos ({len(missing)}):")
        for m in missing:
            print(f"  - {m}")
    print(f"\nDocumento: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
