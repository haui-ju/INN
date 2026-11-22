#!/usr/bin/env python3
"""Convierte los Markdown de una carpeta de anexos en HTML estándar (common/document-html/).

  python3 .claude/skills/_shared/doc_html.py construir --origen DIR --salida DIR/html [--tokens base|ruta] [--raiz .]
  python3 .claude/skills/_shared/doc_html.py comprobar --origen DIR --salida DIR/html [--tokens base|ruta] [--raiz .]

Un HTML por cada .md, con la misma ruta relativa bajo --salida, más index.html. Autónomos, con los tokens del sistema de
diseño y sin recursos externos. Los enlaces relativos a .md pasan a .html. Solo biblioteca estándar.
"""
import argparse
import functools
import html
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMMON = HERE.parents[2] / "common" / "document-html"
# Hoja de estilos del estándar visual (cabecera, botones y fuentes): la de `pantalla` si existe; si no, la de la vista previa,
# que es una plantilla compilada que siempre está y lleva la misma hoja `<style id="estilos">`.
ESTILOS_VISUALES = [HERE.parents[2] / "common" / "html" / n / "index.html" for n in ("pantalla", "vista-previa")]
sys.path.insert(0, str(HERE))
import html_tpl as H  # noqa: E402
import projectcfg as P  # noqa: E402

INI, FIN = H.INI, H.FIN
EXTERNO = re.compile(r"""\bsrc=["']|<link\b|@import|<script[^>]+src=""", re.I)
RE_ENLACE_HTML = re.compile(r'href="([^"]+)"')


# ---------------------------------------------------------------- Markdown a HTML
def _slug(t, usados):
    base = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", t).lower().translate(str.maketrans("áéíóúüñ", "aeiouun"))).strip("-") or "seccion"
    s, n = base, 2
    while s in usados:
        s, n = f"{base}-{n}", n + 1
    usados.add(s)
    return s


def _enlace(destino):
    """Reescribe .md relativo a .html (conserva el ancla). Externos y otros archivos quedan igual."""
    if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|/)", destino, re.I):
        return destino
    ruta, almoh, ancla = destino.partition("#")
    if ruta.lower().endswith(".md"):
        ruta = ruta[:-3] + ".html"
    return ruta + almoh + ancla


def inline(t):
    """Negrita, cursiva, código y enlaces sobre texto ya sin HTML."""
    partes = re.split(r"(`[^`]+`)", t)
    out = []
    for p in partes:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append(f"<code>{html.escape(p[1:-1], quote=False)}</code>")
            continue
        p = html.escape(p, quote=False)
        p = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(_enlace(html.unescape(m.group(2))), quote=True)}">{m.group(1)}</a>', p)
        p = re.sub(r"(?<![\"'>=(\w])(https?://[^\s<)]+[^\s<).,;:])", r'<a href="\1">\1</a>', p)
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
        p = re.sub(r"(?<![*\w])\*([^*\s][^*]*?)\*(?![*\w])", r"<em>\1</em>", p)
        p = re.sub(r"(?<![_\w])_([^_\s][^_]*?)_(?![_\w])", r"<em>\1</em>", p)
        out.append(p)
    return "".join(out)


def _celdas(l):
    return [c.strip() for c in l.strip().strip("|").split("|")]


def _lista(lineas, i):
    """Lista (con anidado por sangría y casillas) desde la línea i. Devuelve (html, siguiente)."""
    def item(l):
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", l)
        return (len(m.group(1)), m.group(2), m.group(3)) if m else None

    def construir(i, nivel):
        sangria, marca, _ = item(lineas[i])
        tag = "ol" if marca[0].isdigit() else "ul"
        out = [f"<{tag}>"]
        while i < len(lineas):
            it = item(lineas[i])
            if it is None or it[0] < sangria:
                break
            if it[0] > sangria:
                sub, i = construir(i, nivel + 1)
                out[-1] = out[-1].replace("</li>", "") + sub + "</li>"
                continue
            texto = it[2]
            m = re.match(r"^\[([ xX])\]\s+(.*)$", texto)
            if m:
                marcado = " checked" if m.group(1).lower() == "x" else ""
                out.append(f'<li class="tarea"><input type="checkbox" disabled{marcado}>{inline(m.group(2))}</li>')
            else:
                out.append(f"<li>{inline(texto)}</li>")
            i += 1
        out.append(f"</{tag}>")
        return "".join(out), i

    return construir(i, 0)


def md_a_html(texto):
    """(html, título) de un Markdown. El título es el primer encabezado #."""
    lineas = texto.splitlines()
    out, usados, titulo, i = [], set(), None, 0
    while i < len(lineas):
        l = lineas[i]
        if l.lstrip().startswith("```"):
            cod, i = [], i + 1
            while i < len(lineas) and not lineas[i].lstrip().startswith("```"):
                cod.append(html.escape(lineas[i], quote=False))
                i += 1
            out.append("<pre><code>" + "\n".join(cod) + "</code></pre>")
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", l)
        if m:
            n = len(m.group(1))
            if titulo is None and n == 1:
                titulo = re.sub(r"[*`]", "", m.group(2))
            cuerpo = inline(m.group(2))
            out.append(f'<h{n} id="{_slug(m.group(2), usados)}">{cuerpo}</h{n}>')
            i += 1
            continue
        if re.match(r"^\s*([-*_])(\s*\1){2,}\s*$", l) and not re.match(r"^\s*[-*]\s+\S", l):
            out.append("<hr>")
            i += 1
            continue
        if l.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                filas.append(_celdas(lineas[i]))
                i += 1
            filas = [f for f in filas if not all(re.fullmatch(r":?-+:?", c) for c in f)]
            if filas:
                enc = "".join(f'<th scope="col">{inline(c)}</th>' for c in filas[0])
                cuerpo = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in f) + "</tr>" for f in filas[1:])
                out.append(f'<div class="tabla"><table><thead><tr>{enc}</tr></thead><tbody>{cuerpo}</tbody></table></div>')
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", l):
            lista, i = _lista(lineas, i)
            out.append(lista)
            continue
        if l.startswith(">"):
            cita = []
            while i < len(lineas) and lineas[i].startswith(">"):
                cita.append(re.sub(r"^>\s?", "", lineas[i]))
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(cita)) + "</p></blockquote>")
            continue
        if l.strip():
            par = [l.strip()]
            while i + 1 < len(lineas) and lineas[i + 1].strip() and not re.match(r"^(#{1,6}\s|\||>|```|\s*([-*]|\d+\.)\s+)", lineas[i + 1]):
                i += 1
                par.append(lineas[i].strip())
            out.append("<p>" + "<br>\n".join(inline(x) for x in par) + "</p>")
        i += 1
    return "\n".join(out), titulo


# ---------------------------------------------------------------- páginas
def tokens_del_config(raiz, cfg=None):
    """tokens.json junto al DESIGN.md vigente del config; los tokens base si no hay sistema de diseño."""
    raiz = Path(raiz or ".")
    cfg = cfg if cfg is not None else P.load(raiz)
    d = cfg.get("diseno")
    ruta = (raiz / d).with_name("tokens.json") if d else None
    return H.cargar_tokens(raiz, str(ruta.relative_to(raiz))) if ruta and ruta.is_file() else H.cargar_tokens(raiz, "base")


def _plantilla():
    return (COMMON / "plantilla.html").read_text(encoding="utf-8")


@functools.lru_cache(maxsize=1)
def _estilos_visuales():
    """Hoja de estilos compilada del estándar visual (cabecera, botones y fuentes), tal cual la usan los visuales."""
    for f in ESTILOS_VISUALES:
        if f.is_file():
            m = re.search(r'<style id="estilos">(.*?)</style>', f.read_text(encoding="utf-8"), re.S)
            if m:
                return m.group(1)
    raise SystemExit("ERROR: ninguna plantilla de common/html/ (pantalla o vista-previa) tiene la hoja de estilos del estándar visual")


def _documento_css():
    return (COMMON / "documento.css").read_text(encoding="utf-8")


def _rel_a_raiz(rel):
    return "../" * (len(Path(rel).parts) - 1)


def _ruta(rel, titulo, nombre_raiz):
    partes = list(Path(rel).with_suffix("").parts)
    pre = _rel_a_raiz(rel)
    migas = [f'<a href="{pre}index.html">{html.escape(nombre_raiz)}</a>']
    migas += [html.escape(p) for p in partes[:-1]]
    migas.append(f'<span aria-current="page">{html.escape(partes[-1])}</span>')
    return '<nav class="ruta" aria-label="Ruta">' + " / ".join(migas) + "</nav>"


def _vecinos(rel, hermanos):
    i = hermanos.index(rel)
    ant = f'<a href="{Path(hermanos[i - 1]).with_suffix(".html").name}" rel="prev">← {html.escape(Path(hermanos[i - 1]).stem)}</a>' if i > 0 else "<span></span>"
    sig = f'<a href="{Path(hermanos[i + 1]).with_suffix(".html").name}" rel="next">{html.escape(Path(hermanos[i + 1]).stem)} →</a>' if i + 1 < len(hermanos) else "<span></span>"
    return f'<nav class="vecinos" aria-label="Documentos de la carpeta">{ant}{sig}</nav>'


def _pagina(plantilla, tokens, titulo, ruta, contenido, vecinos, pie, archivo=""):
    ini, fin = plantilla.index(INI), plantilla.index(FIN) + len(FIN)
    p = plantilla[:ini] + INI + "\n" + H.tokens_css(tokens) + "\n" + FIN + plantilla[fin:]
    valores = {"titulo": html.escape(titulo), "ruta": ruta, "contenido": contenido, "vecinos": vecinos, "pie": html.escape(pie),
               "estilos": _estilos_visuales(), "documento": _documento_css(), "nombre_archivo": archivo, "fecha": ""}
    # una sola pasada: el contenido inserto no vuelve a interpretarse como marcador
    return re.sub(r"\{\{(\w+)\}\}", lambda m: valores.get(m.group(1), m.group(0)), p)


def _titulo_md(texto, rel):
    m = re.search(r"^#\s+(.+?)\s*$", texto, re.M)
    return re.sub(r"[*`]", "", m.group(1)) if m else Path(rel).stem


RE_ENLACE_MD = re.compile(r"(\]\()([^)\s]+)(\))")


def reubicar_enlaces(texto, desde, hacia):
    """Reescribe los enlaces relativos a archivos que no son .md para que resuelvan desde la carpeta del HTML.

    `desde` es la carpeta del .md y `hacia` la del HTML (los .md enlazados pasan a .html con la misma ruta, así que no cambian).
    """
    def rep(m):
        destino = m.group(2)
        ruta, almoh, ancla = destino.partition("#")
        if not ruta or re.match(r"^(?:[a-z][a-z0-9+.-]*:|/)", ruta, re.I) or ruta.lower().endswith(".md"):
            return m.group(0)
        nuevo = os.path.relpath(os.path.normpath(os.path.join(desde, ruta)), hacia).replace(os.sep, "/")
        return m.group(1) + nuevo + almoh + ancla + m.group(3)
    lineas, dentro = [], False
    for l in texto.split("\n"):
        if l.lstrip().startswith("```"):
            dentro = not dentro
        lineas.append(l if dentro else RE_ENLACE_MD.sub(rep, l))
    return "\n".join(lineas)


def generar(origen, tokens, nombre_raiz=None, salida=None):
    """{ruta relativa .html: contenido} de todo el árbol de `origen` (sin la carpeta html/).

    Con `salida`, los enlaces relativos a archivos que no son .md se reubican para que resuelvan desde el HTML."""
    origen = Path(origen)
    nombre_raiz = nombre_raiz or origen.name
    mds = sorted(p.relative_to(origen).as_posix() for p in origen.rglob("*.md") if "html" not in p.relative_to(origen).parts[:1])
    plantilla, out, titulos = _plantilla(), {}, {}
    for rel in mds:
        texto = (origen / rel).read_text(encoding="utf-8")
        titulos[rel] = _titulo_md(texto, rel)
    por_carpeta = {}
    for rel in mds:
        por_carpeta.setdefault(str(Path(rel).parent), []).append(rel)
    for rel in mds:
        texto = (origen / rel).read_text(encoding="utf-8")
        if salida is not None:
            texto = reubicar_enlaces(texto, str((origen / rel).parent.resolve()), str((Path(salida) / rel).parent.resolve()))
        cuerpo, titulo = md_a_html(texto)
        h = Path(rel).with_suffix(".html").as_posix()
        out[h] = _pagina(plantilla, tokens, titulo or Path(rel).stem, _ruta(rel, titulo, nombre_raiz), cuerpo,
                         _vecinos(rel, por_carpeta[str(Path(rel).parent)]) if len(por_carpeta[str(Path(rel).parent)]) > 1 else "",
                         f"{nombre_raiz} · {rel}", Path(rel).stem)
    # índice
    arbol, carpeta_ant = [], None
    for rel in mds:
        carpeta = str(Path(rel).parent)
        if carpeta != carpeta_ant:
            if carpeta_ant is not None:
                arbol.append("</ul>")
            arbol.append(f"<h2>{html.escape(carpeta if carpeta != '.' else nombre_raiz)}</h2>\n<ul>")
            carpeta_ant = carpeta
        arbol.append(f'<li><a href="{Path(rel).with_suffix(".html").as_posix()}">{html.escape(titulos[rel])}</a></li>')
    if carpeta_ant is not None:
        arbol.append("</ul>")
    cuerpo = f"<h1>{html.escape(nombre_raiz)}</h1>\n<p>{len(mds)} documentos.</p>\n" + "\n".join(arbol)
    out["index.html"] = _pagina(plantilla, tokens, nombre_raiz, f'<nav class="ruta" aria-label="Ruta"><span aria-current="page">{html.escape(nombre_raiz)}</span></nav>', cuerpo, "", f"{nombre_raiz} · índice", "indice")
    return out


def construir(origen, salida, tokens, nombre_raiz=None):
    salida = Path(salida)
    paginas = generar(origen, tokens, nombre_raiz, salida)
    if salida.exists():
        for viejo in salida.rglob("*.html"):
            viejo.unlink()
    for rel, txt in paginas.items():
        d = salida / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_text(txt, encoding="utf-8")
    return sorted(paginas)


def comprobar(origen, salida, tokens, nombre_raiz=None):
    """Lista de incidencias (archivo, causa) del conjunto HTML frente a sus .md."""
    inc, salida = [], Path(salida)
    esperado = generar(origen, tokens, nombre_raiz, salida)
    existentes = {p.relative_to(salida).as_posix() for p in salida.rglob("*.html")} if salida.is_dir() else set()
    for rel in sorted(set(esperado) - existentes):
        inc.append((rel, "falta el HTML de su Markdown"))
    for rel in sorted(existentes - set(esperado)):
        inc.append((rel, "HTML sin Markdown de origen"))
    for rel in sorted(set(esperado) & existentes):
        txt = (salida / rel).read_text(encoding="utf-8")
        if txt != esperado[rel]:
            inc.append((rel, "no coincide con lo que se genera desde su Markdown"))
        if EXTERNO.search(txt):
            inc.append((rel, "carga recursos externos"))
        for destino in RE_ENLACE_HTML.findall(txt):
            if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|/)", destino, re.I):
                continue
            ruta = destino.split("#")[0].split("?")[0]
            if ruta and not (salida / rel).parent.joinpath(html.unescape(ruta)).resolve().exists():
                inc.append((rel, f"el enlace «{destino}» no apunta a un archivo que exista"))
    return inc


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=("construir", "comprobar"))
    ap.add_argument("--origen", required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--tokens", default="base")
    ap.add_argument("--raiz")
    ap.add_argument("--nombre")
    a = ap.parse_args(argv)
    try:
        tk = H.cargar_tokens(a.raiz or ".", a.tokens)
    except (OSError, ValueError) as e:
        print(f"ERROR: tokens: {e}", file=sys.stderr)
        return 1
    if a.cmd == "construir":
        hechos = construir(a.origen, a.salida, tk, a.nombre)
        print(f"{len(hechos)} archivos en {a.salida}")
        return 0
    inc = comprobar(a.origen, a.salida, tk, a.nombre)
    for f, causa in inc:
        print(f"{f}: {causa}")
    print("sin incidencias" if not inc else f"{len(inc)} incidencia(s)")
    return 1 if inc else 0


if __name__ == "__main__":
    sys.exit(main())
