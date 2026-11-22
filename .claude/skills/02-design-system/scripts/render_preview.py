#!/usr/bin/env python3
"""Genera preview.html (autónomo, claro y oscuro) copiando la plantilla common/html/vista-previa/ con los tokens.

  python3 .claude/skills/02-design-system/scripts/render_preview.py <tokens.json> <preview.html> [--titulo "Nombre del proyecto"]

Determinista: la misma entrada produce el mismo archivo. Solo se sustituyen el bloque de tokens (variables CSS) y el
bloque de datos (proyecto y tokens). Solo biblioteca estándar.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
import html_tpl as H  # noqa: E402


def pagina(t, titulo):
    return H.copiar_texto("vista-previa", {"schema": 1, "proyecto": titulo, "tokens": t}, t)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tokens")
    ap.add_argument("salida")
    ap.add_argument("--titulo", default="Proyecto")
    a = ap.parse_args(argv)
    t = json.loads(Path(a.tokens).read_text(encoding="utf-8"))
    Path(a.salida).write_text(pagina(t, a.titulo), encoding="utf-8")
    print(a.salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
