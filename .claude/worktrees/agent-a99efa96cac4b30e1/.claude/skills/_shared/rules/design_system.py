"""Reglas específicas del paso 02-design-system (se invocan desde validate_run.py)."""
import json
import re
from pathlib import Path

import html_tpl as H

CLAVES_COLOR = ["fondo", "superficie", "texto", "texto-secundario", "borde",
                "acento", "acento-texto", "exito", "alerta", "error"]
MINIMOS = {"normal": 4.5, "grande": 3.0, "interfaz": 3.0}
COMPONENTES = ["Encabezado", "Tarjeta", "Tabla", "Etiqueta de estado", "Barra de progreso", "Botón"]
TEMAS = ("claro", "oscuro")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


def luminancia(hex_color):
    """Luminancia relativa (WCAG) de un color #RRGGBB."""
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))

    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _cargar(run):
    p = Path(run) / "tokens.json"
    if not p.exists():
        return None, [("tokens.json", "falta el archivo")]
    try:
        return json.loads(p.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as e:
        return None, [("tokens.json", f"JSON inválido: {e}")]


def tokens_planos(t):
    """Conjunto de rutas de token válidas, p. ej. color.claro.acento, espacio.4."""
    out = set()
    for tema in TEMAS:
        for k in t.get("color", {}).get(tema, {}):
            out.add(f"color.{tema}.{k}")
    for grupo in ("espacio", "radio", "sombra"):
        for k in t.get(grupo, {}):
            out.add(f"{grupo}.{k}")
    tip = t.get("tipografia", {})
    for k, v in tip.items():
        if isinstance(v, dict):
            for kk in v:
                out.add(f"tipografia.{k}.{kk}")
        else:
            out.add(f"tipografia.{k}")
    return out


def check_tokens(t):
    inc = []
    col = t.get("color", {})
    for tema in TEMAS:
        if tema not in col:
            inc.append(("tokens.json", f"falta color.{tema}"))
    if inc:
        return inc
    if set(col["claro"]) != set(col["oscuro"]):
        dif = sorted(set(col["claro"]) ^ set(col["oscuro"]))
        inc.append(("tokens.json", f"claro y oscuro no tienen las mismas claves: {', '.join(dif)}"))
    for k in CLAVES_COLOR:
        for tema in TEMAS:
            if k not in col[tema]:
                inc.append(("tokens.json", f"falta color.{tema}.{k}"))
    for tema in TEMAS:
        for k, v in col[tema].items():
            if not (isinstance(v, str) and HEX.match(v)):
                inc.append(("tokens.json", f"color.{tema}.{k}: «{v}» no es #RRGGBB"))
    for g in ("tipografia", "espacio", "radio", "sombra"):
        if not t.get(g):
            inc.append(("tokens.json", f"falta el grupo {g}"))
    return inc


def check_pares(t):
    inc = []
    pares = t.get("pares")
    if not pares:
        return [("tokens.json", "no declara pares de contraste")]
    for p in pares:
        tipo = p.get("tipo")
        if tipo not in MINIMOS:
            inc.append(("tokens.json", f"par {p.get('texto')}/{p.get('fondo')}: tipo «{tipo}» no válido"))
            continue
        for tema in TEMAS:
            c = t["color"][tema]
            if p.get("texto") not in c or p.get("fondo") not in c:
                inc.append(("tokens.json", f"par {p.get('texto')}/{p.get('fondo')}: clave inexistente en {tema}"))
                continue
            r = contraste(c[p["texto"]], c[p["fondo"]])
            if r < MINIMOS[tipo]:
                inc.append(("tokens.json", f"contraste {r:.2f}:1 en {tema} para {p['texto']} sobre {p['fondo']} (mínimo {MINIMOS[tipo]}:1, tipo {tipo})"))
    return inc


def check_design_md(run, t):
    inc = []
    p = Path(run) / "DESIGN.md"
    if not p.exists():
        return [("DESIGN.md", "falta el archivo")]
    txt = p.read_text(encoding="utf-8")
    validos = tokens_planos(t)
    for m in re.finditer(r"`((?:color\.(?:claro|oscuro)|espacio|radio|sombra|tipografia)\.[\w.\-]+)`", txt):
        if m.group(1) not in validos:
            inc.append(("DESIGN.md", f"token inexistente: {m.group(1)}"))
    m = re.search(r"^## Componentes\s*$(.*?)(?=^## |\Z)", txt, re.M | re.S)
    cuerpo = m.group(1) if m else ""
    if not m:
        inc.append(("DESIGN.md", "falta la sección «Componentes»"))
    for comp in COMPONENTES:
        s = re.search(rf"^### {re.escape(comp)}\s*$(.*?)(?=^### |\Z)", cuerpo, re.M | re.S)
        if not s:
            inc.append(("DESIGN.md", f"falta el componente «{comp}»"))
            continue
        for campo in ("Estados", "Tokens", "Uso"):
            if not re.search(rf"\*\*{campo}:\*\*\s*\S", s.group(1)):
                inc.append(("DESIGN.md", f"componente «{comp}» sin «{campo}»"))
    return inc


def check_preview(run, t):
    inc = []
    p = Path(run) / "preview.html"
    if not p.exists():
        return [("preview.html", "falta el archivo")]
    h = p.read_text(encoding="utf-8")
    patrones = [
        (r"<script[^>]+src\s*=", "script externo"),
        (r"<link[^>]+href\s*=\s*[\"']?(?:https?:)?//", "hoja de estilos o fuente externa"),
        (r"@import", "@import"),
        (r"url\(\s*[\"']?(?:https?:)?//", "url() externa"),
        (r"<(?:img|iframe|source)[^>]+src\s*=\s*[\"']?(?:https?:)?//", "recurso externo"),
    ]
    for rx, nombre in patrones:
        if re.search(rx, h, re.I):
            inc.append(("preview.html", f"recurso externo: {nombre}"))
    if 'name="viewport"' not in h:
        inc.append(("preview.html", "falta la metaetiqueta viewport"))
    for k in t["color"]["claro"]:
        valores = re.findall(rf"--c-{re.escape(k)}\s*:\s*([^;]+);", h)
        permitidos = {t["color"]["claro"][k].lower(), t["color"]["oscuro"][k].lower()}
        if not valores:
            inc.append(("preview.html", f"no define la variable --c-{k}"))
        for v in valores:
            if v.strip().lower() not in permitidos:
                inc.append(("preview.html", f"--c-{k}: {v.strip()} no coincide con tokens.json"))
        if t["color"]["claro"][k].lower() not in [v.strip().lower() for v in valores] or \
                t["color"]["oscuro"][k].lower() not in [v.strip().lower() for v in valores]:
            inc.append(("preview.html", f"--c-{k} no incluye los valores claro y oscuro de tokens.json"))
    if "prefers-color-scheme" not in h or "data-theme" not in h:
        inc.append(("preview.html", "no alterna entre tema claro y oscuro"))
    if not inc:
        m = H.RE_DATOS.search(h)
        try:
            proyecto = json.loads(m.group(2).replace("<\\/", "</")).get("proyecto", "") if m else ""
        except (ValueError, AttributeError):
            proyecto = ""
        if h != H.copiar_texto("vista-previa", {"schema": 1, "proyecto": proyecto, "tokens": t}, t):
            inc.append(("preview.html", "no es la plantilla vista-previa con los tokens de tokens.json; vuelve a generarlo con render_preview.py"))
    return inc


def validar(run):
    t, inc = _cargar(run)
    if t is None:
        return inc
    inc = check_tokens(t)
    if inc:
        return inc
    return check_pares(t) + check_design_md(run, t) + check_preview(run, t)
