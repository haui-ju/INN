#!/usr/bin/env python3
"""Plantillas HTML del proyecto (common/html/): copiar y comprobar.

  python3 .claude/skills/_shared/html_tpl.py copiar --visual foda --datos datos.json [--tokens base|ruta] --salida foda.html
  python3 .claude/skills/_shared/html_tpl.py limpiar --visual foda [--salida datos.json]
  python3 .claude/skills/_shared/html_tpl.py comprobar
  python3 .claude/skills/_shared/html_tpl.py preparar        (después de `npm run build`; uso de desarrollo)

`limpiar` entrega el mock.json de un visual sin datos (la skill parte de ahí, nunca de los datos de ejemplo). `copiar` toma common/html/<visual>/index.html (compilada con React, Tailwind y fuentes incrustadas) y sustituye SOLO
el bloque de tokens (variables CSS del sistema de diseño) y el bloque de datos (JSON embebido). `comprobar` verifica
que las plantillas versionadas coinciden con sus fuentes (manifiesto de huellas) sin necesitar node. `preparar`
escribe los tokens base y el mock en cada plantilla compilada y actualiza el manifiesto. Solo biblioteca estándar.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMUN = HERE.parents[2] / "common" / "html"
BASE = COMUN / "_base"
TOKENS_BASE = HERE.parent / "02-design-system" / "references" / "tokens-base.json"
INI, FIN = "/*tokens:inicio*/", "/*tokens:fin*/"
RE_TOKENS = re.compile(re.escape(INI) + r".*?" + re.escape(FIN), re.S)
RE_DATOS = re.compile(r'(<script type="application/json" id="datos">)(.*?)(</script>)', re.S)


def cargar_tokens(raiz, diseno):
    """tokens.json según `diseno` (ruta del tokens.json) o 'base'."""
    ruta = TOKENS_BASE if diseno in (None, "base") else Path(raiz) / diseno
    return json.loads(Path(ruta).read_text(encoding="utf-8"))


def tokens_css(tk):
    """Variables CSS del sistema de diseño (claro por defecto; oscuro con prefers-color-scheme y data-theme)."""
    def bloque(c, ind):
        return "\n".join(f"{ind}--c-{k}: {v};" for k, v in c.items())
    tip = tk["tipografia"]
    comunes = [f"    --fuente: {tip['familia']};"]
    comunes.append(f"    --fuente-titulos: {tip.get('familia-titulos', tip['familia'])};")
    if "familia-mono" in tip:
        comunes.append(f"    --fuente-mono: {tip['familia-mono']};")
    comunes += [f"    --t-{k}: {v};" for k, v in tip["escala"].items()]
    comunes += [f"    --espacio-{k}: {v};" for k, v in tk["espacio"].items()]
    comunes += [f"    --radio-{k}: {v};" for k, v in tk["radio"].items()]
    comunes += [f"    --sombra-{k}: {v};" for k, v in tk["sombra"].items()]
    comunes += [f"    --peso-{k}: {v};" for k, v in tip["peso"].items()]
    return f""":root {{
{bloque(tk['color']['claro'], '    ')}
{chr(10).join(comunes)}
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
{bloque(tk['color']['oscuro'], '      ')}
    }}
  }}
  :root[data-theme="dark"] {{
{bloque(tk['color']['oscuro'], '    ')}
  }}
  :root[data-theme="light"] {{
{bloque(tk['color']['claro'], '    ')}
  }}"""


def datos_json(datos):
    return json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def _leer(p):
    return Path(p).read_text(encoding="utf-8")


CONSERVAR = {"schema", "diseno"}
VACIOS = {"calculado", "tokens", "tareas", "tarjetas"}


def limpiar(datos):
    """Versión vacía de unos datos (p. ej. un mock.json): mismas claves, sin contenido. Conserva `schema` y `diseno`."""
    def v(x, clave=None):
        if clave in CONSERVAR:
            return x
        if clave == "fecha_corte":
            return None
        if isinstance(x, dict):
            return {} if clave in VACIOS else {k: v(y, k) for k, y in x.items()}
        if isinstance(x, list):
            return []
        if isinstance(x, str):
            return ""
        if isinstance(x, bool):
            return False
        return None if x is None else 0
    return v(datos)


def visuales():
    return sorted(d.name for d in COMUN.iterdir() if d.is_dir() and not d.name.startswith("_") and (d / "mock.json").exists())


MANIFIESTO = COMUN / "_build" / "manifiesto.json"


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def huella_fuentes():
    """Huella de las fuentes de la compilación: _build/src, build.mjs, pagina.html, package*.json, tokens base y mocks."""
    b = COMUN / "_build"
    archivos = sorted(p for p in (b / "src").rglob("*") if p.is_file())
    archivos += [b / n for n in ("build.mjs", "pagina.html", "package.json", "package-lock.json") if (b / n).exists()]
    archivos += [TOKENS_BASE] + [COMUN / v / "mock.json" for v in visuales()]
    h = hashlib.sha256()
    for p in archivos:
        try:
            nombre = p.relative_to(COMUN).as_posix()
        except ValueError:
            nombre = p.name
        h.update(nombre.encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def preparar():
    """Deja cada index.html con los tokens base y su mock, y actualiza el manifiesto (después de compilar)."""
    base = cargar_tokens(None, "base")
    for v in visuales():
        p = COMUN / v / "index.html"
        p.write_text(copiar_texto(v, json.loads(_leer(COMUN / v / "mock.json")), base), encoding="utf-8")
    man = {"fuentes": huella_fuentes(), "plantillas": {v: _sha((COMUN / v / "index.html").read_bytes()) for v in visuales()}}
    MANIFIESTO.write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return man


def comprobar():
    """Problemas de sincronía de las plantillas (lista vacía si todo coincide)."""
    inc = []
    if not MANIFIESTO.exists():
        return ["falta _build/manifiesto.json: ejecuta npm run build en common/html/_build"]
    man = json.loads(_leer(MANIFIESTO))
    if man.get("fuentes") != huella_fuentes():
        inc.append("las fuentes de common/html/_build/ cambiaron y las plantillas no se recompilaron (npm run build)")
    base = cargar_tokens(None, "base")
    for v in visuales():
        p = COMUN / v / "index.html"
        if not p.exists():
            inc.append(f"falta la plantilla {v}/index.html")
            continue
        if man["plantillas"].get(v) != _sha(p.read_bytes()):
            inc.append(f"la plantilla {v}/index.html no coincide con el manifiesto")
        if _leer(p) != copiar_texto(v, json.loads(_leer(COMUN / v / "mock.json")), base):
            inc.append(f"la plantilla {v}/index.html no lleva los tokens base y su mock.json")
    return inc


def copiar_texto(visual, datos, tokens):
    """Plantilla `visual` con SOLO el bloque de tokens y el de datos sustituidos."""
    t = _leer(COMUN / visual / "index.html")
    css = INI + "\n" + tokens_css(tokens) + "\n" + FIN
    t = RE_TOKENS.sub(lambda m: css, t, count=1)
    return RE_DATOS.sub(lambda m: m.group(1) + datos_json(datos) + m.group(3), t, count=1)


def copiar(visual, datos, tokens, salida):
    Path(salida).write_text(copiar_texto(visual, datos, tokens), encoding="utf-8")
    return Path(salida)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("copiar")
    c.add_argument("--visual", required=True)
    c.add_argument("--datos", required=True)
    c.add_argument("--tokens", default="base")
    c.add_argument("--salida", required=True)
    l = sub.add_parser("limpiar")
    l.add_argument("--visual", required=True)
    l.add_argument("--salida")
    sub.add_parser("comprobar")
    sub.add_parser("preparar")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "limpiar":
            if a.visual not in visuales():
                print(f"ERROR: no existe la plantilla {a.visual} (hay: {', '.join(visuales())})", file=sys.stderr)
                return 1
            txt = json.dumps(limpiar(json.loads(_leer(COMUN / a.visual / "mock.json"))), ensure_ascii=False, indent=2) + "\n"
            if a.salida:
                Path(a.salida).write_text(txt, encoding="utf-8")
                print(a.salida)
            else:
                print(txt, end="")
            return 0
        if a.cmd == "preparar":
            preparar()
            print("plantillas preparadas y manifiesto actualizado")
            return 0
        if a.cmd == "comprobar":
            inc = comprobar()
            print("\n".join(inc) if inc else "plantillas sincronizadas")
            return 1 if inc else 0
        if a.visual not in visuales():
            print(f"ERROR: no existe la plantilla {a.visual} (hay: {', '.join(visuales())})", file=sys.stderr)
            return 1
        tk = cargar_tokens(".", None if a.tokens == "base" else a.tokens)
        print(copiar(a.visual, json.loads(_leer(a.datos)), tk, a.salida))
        return 0
    except (OSError, ValueError, KeyError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
