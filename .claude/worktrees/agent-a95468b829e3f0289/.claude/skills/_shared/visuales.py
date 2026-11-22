#!/usr/bin/env python3
"""Visuales HTML del informe: extracción de sus datos desde el markdown de las corridas vigentes.

  python3 .claude/skills/_shared/visuales.py disponibles [--raiz .]
  python3 .claude/skills/_shared/visuales.py extraer --visual <visual> [--raiz .] [--salida datos.json]
  python3 .claude/skills/_shared/visuales.py construir --visual <visual> --carpeta <corrida>/visuales [--raiz .]
  python3 .claude/skills/_shared/visuales.py origen --visual <visual>            (skill, archivo y -update que lo cambian)

El markdown de las skills de origen es la fuente de verdad: aquí solo se lee. Cada visual tiene su plantilla en
common/html/<plantilla>/. `construir` escribe <visual>.json y <visual>.html y, al lado de visuales/, leer-imagen/<visual>.md
(puntos cortos que explican qué muestra la imagen y qué transmite, para el informe).

Los registros (VISUALES, EXTRACTORES, EXPLICACION, PROPOSITOS, TITULOS y ORIGEN) los completa cada skill que aporta
un visual (por ejemplo FODA, PESTEL, Business Model Canvas e Ishikawa en el capítulo 1). Solo biblioteca estándar.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import html_tpl as H  # noqa: E402
import projectcfg as P  # noqa: E402

# visual -> (plantilla, paso de origen o None, carpeta del paso)
VISUALES = {}
PLANTILLAS = sorted({v[0] for v in VISUALES.values()})


class SinFuente(Exception):
    """Falta la corrida o el archivo de origen de un visual."""


# ------------------------------------------------------------------ lectura de markdown
def _limpia(s):
    return re.sub(r"\s+", " ", s.replace("**", "").replace("`", "")).strip()


def tablas(txt):
    """Todas las tablas de un markdown: lista de (encabezados, filas) con las celdas como texto."""
    out, cur = [], []
    for ln in txt.splitlines() + [""]:
        if ln.strip().startswith("|"):
            cur.append(ln.strip())
            continue
        if len(cur) >= 2:
            filas = [[_limpia(c) for c in r.strip("|").split("|")] for r in cur]
            if all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cur[1].strip("|").split("|")):
                out.append((filas[0], filas[2:]))
        cur = []
    return out


def _norm(s):
    return re.sub(r"[^a-z0-9 ]", "", _sin_tildes(s).lower()).strip()


def _busca(enc, nombre):
    """Índice de la columna `nombre`: por coincidencia completa o, si no, por las 3 primeras letras (Imp. = Impacto)."""
    n = _norm(nombre)
    e = [_norm(x) for x in enc]
    for i, x in enumerate(e):
        if n in x:
            return i
    for i, x in enumerate(e):
        if len(n) > 3 and n[:3] in x.split(" ")[0][:3]:
            return i
    return None


def tabla(txt, *claves):
    """Primera tabla cuyo encabezado tiene todas las `claves` (sin tildes ni mayúsculas); None si no hay."""
    for enc, filas in tablas(txt):
        if all(_busca(enc, c) is not None for c in claves):
            return enc, filas
    return None


def _sin_tildes(s):
    return s.translate(str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU"))


def secciones(txt, nivel=2):
    """{título: cuerpo} de los encabezados del nivel indicado."""
    partes = re.split(rf"(?m)^{'#' * nivel}\s+(?!#)(.+)$", txt)
    return {partes[i].strip(): partes[i + 1].strip() for i in range(1, len(partes) - 1, 2)}


def campo(txt, rotulo):
    """Valor de «**Rótulo.** valor» (hasta el siguiente rótulo o el fin de la línea/párrafo)."""
    m = re.search(rf"\*\*{re.escape(rotulo)}[.:]?\*\*\s*(.*?)(?=\s*\*\*[^*]+\*\*|\n\s*\n|\Z)", txt, re.S)
    return _limpia(m.group(1)) if m else ""


def fecha_iso(s):
    m = re.search(r"(\d{2})-(\d{2})-(\d{4})", s or "")
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


def _entero(s):
    m = re.search(r"[−-]?\d+", (s or "").replace("−", "-"))
    return int(m.group(0)) if m else 0


def _item(celda):
    """«texto» (REF) -> {texto, ref}."""
    c = _limpia(celda)
    m = re.match(r"^(.*?)\s*\(([^()]*)\)\.?$", c)
    texto, ref = (m.group(1), m.group(2)) if m else (c, "")
    ref = re.sub(r"^(?:inferid[oa]s? de|basad[oa]s? en)\s+", "", ref.strip(), flags=re.I)
    return {"texto": texto.strip().strip("«»\"“” ").rstrip(".;").strip(), "ref": ref.strip()}


def _col(enc, fila, *nombres):
    for nom in nombres:
        i = _busca(enc, nom)
        if i is not None and i < len(fila):
            return fila[i]
    return ""


# ------------------------------------------------------------------ corridas vigentes
def _run(raiz, paso, carpeta):
    try:
        r = P.current_run(paso, raiz)
    except P.ConfigError as e:
        raise SinFuente(str(e))
    if not r:
        raise SinFuente(f"no hay una corrida vigente de {paso}")
    return Path(raiz) / "project" / carpeta / r


def _leer(run, *nombres):
    """Primer archivo de la corrida con alguno de esos nombres (en cualquier subcarpeta)."""
    for nom in nombres:
        f = run / nom
        if not f.exists():
            hallados = sorted(run.rglob(nom))
            f = hallados[0] if hallados else None
        if f is not None and f.exists():
            return f.read_text(encoding="utf-8")
    raise SinFuente(f"falta {' o '.join(nombres)} en la corrida {run.name}")


def proyecto(raiz):
    try:
        p = P.load(raiz)["proyecto"]
        return p["nombre"] if isinstance(p, dict) else str(p)
    except (P.ConfigError, KeyError, OSError):
        return ""


def _base(raiz):
    return {"schema": 1, "proyecto": proyecto(raiz)}


# ------------------------------------------------------------------ registro de visuales
EXTRACTORES = {}


def extraer(visual, raiz, run=None):
    """Datos del visual desde las corridas vigentes. Lanza SinFuente si falta algo."""
    if visual not in EXTRACTORES:
        raise SinFuente(f"visual desconocido: {visual} (hay: {', '.join(sorted(EXTRACTORES)) or 'ninguno'})")
    return EXTRACTORES[visual](raiz, run=run)


def disponibles(raiz, run=None):
    """{visual: None si hay fuente, o el motivo si falta}."""
    out = {}
    for v in sorted(EXTRACTORES):
        try:
            extraer(v, raiz, run)
            out[v] = None
        except SinFuente as e:
            out[v] = str(e)
    return out


# ------------------------------------------------------------------ «leer la imagen»
TITULOS = {}
# Una frase fija por visual (para qué sirve la imagen); lo demás se deriva de los datos.
PROPOSITOS = {}

def _lista(items, n=3):
    items = [str(i) for i in items if i]
    if len(items) <= n:
        return ", ".join(items[:-1]) + (" y " if len(items) > 1 else "") + items[-1] if items else ""
    return ", ".join(items[:n]) + f" y {len(items) - n} más"


def _corto(t, n=110):
    t = str(t).strip().rstrip(".")
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def _comp(a, b, x, y):
    return f"más {x} que {y}" if a > b else f"menos {x} que {y}" if a < b else f"tantas {x} como {y}"


def _pl(n, uno, varios):
    return f"{n} {uno if n == 1 else varios}"


def _fecha_txt(d):
    return f"al {d[8:10]}-{d[5:7]}-{d[:4]}" if d else "Línea base"


# Purpose catalog: one fixed sentence per visual (what the image is for). Everything else is derived from the data.


ROTULO_SIRVE, ROTULO_DICE, ROTULO_RESALTA, ROTULO_PIE = "Para qué sirve", "Qué dice", "Por qué se resalta", "Pie de foto sugerido"
MAX_FRASES = 3
MAX_PALABRAS = 70


class SinProposito(KeyError):
    """The visual has no entry in PROPOSITOS."""


def armar_leer(titulo, sirve, dice, resalta, pie):
    """Text of a `leer-imagen/*.md` file: purpose, conclusion, optional reason for the highlight, and the suggested caption."""
    puntos = [(ROTULO_SIRVE, sirve), (ROTULO_DICE, dice)]
    if resalta:
        puntos.append((ROTULO_RESALTA, resalta))
    puntos.append((ROTULO_PIE, pie))
    return f"# Leer la imagen · {titulo}\n\n" + "\n".join(f"- **{r}.** {t}" for r, t in puntos) + "\n"


def _frases(texto):
    return len(re.findall(r"[.!?](?=\s+[A-ZÁÉÍÓÚÑ¿¡«0-9]|\s*$)", texto.strip()))


def validar_explicacion(texto, resaltado):
    """Causes (empty when valid) for a `leer-imagen` text: labels, highlight reason iff `resaltado`, sentence and word caps."""
    pts = {}
    for l in texto.splitlines():
        m = re.match(r"^- \*\*([^*]+?)\.\*\*\s*(.*)$", l)
        if m:
            pts[m.group(1)] = m.group(2).strip()
    causas = []
    for r in (ROTULO_SIRVE, ROTULO_DICE):
        if not pts.get(r):
            causas.append(f"falta la función «{r.lower()}»")
    if resaltado and not pts.get(ROTULO_RESALTA):
        causas.append("la imagen resalta algo y falta «por qué se resalta»")
    if not resaltado and ROTULO_RESALTA in pts:
        causas.append("incluye «por qué se resalta» pero la imagen no resalta nada")
    cuerpo = [pts[r] for r in (ROTULO_SIRVE, ROTULO_DICE, ROTULO_RESALTA) if pts.get(r)]
    if sum(_frases(t) for t in cuerpo) > MAX_FRASES or any(_frases(t) > 1 for t in cuerpo):
        causas.append(f"pasa de {MAX_FRASES} frases (una por función)")
    if sum(len(t.split()) for t in cuerpo) > MAX_PALABRAS:
        causas.append(f"pasa de {MAX_PALABRAS} palabras")
    if not pts.get(ROTULO_PIE):
        causas.append("falta el pie de foto sugerido")
    return causas

# visual -> función(datos) que devuelve (qué dice, por qué se resalta o None)
EXPLICACION = {}


def resaltado(visual, datos):
    """True cuando los datos de la imagen resaltan algo (y su explicación debe decir por qué)."""
    return EXPLICACION[visual](datos)[1] is not None


def leer_imagen(visual, datos):
    """Texto de `leer-imagen/<visual>.md`: para qué sirve la imagen, qué dice y por qué resalta algo, derivado de los datos."""
    if visual not in PROPOSITOS:
        raise SinProposito(visual)
    dice, resalta = EXPLICACION[visual](datos)
    return armar_leer(TITULOS[visual], PROPOSITOS[visual], dice, resalta, f"Figura X: {TITULOS[visual]}.")


# visual -> (skill de origen, archivo de la corrida)
ORIGEN = {}


def origen(visual):
    """(skill de origen, archivo, skill -update que lo modifica); None si el visual no está registrado."""
    if visual not in ORIGEN:
        return None
    paso, archivo = ORIGEN[visual]
    return paso, archivo, f"{paso}-update"


def construir(visual, raiz, carpeta, tokens, run=None):
    """Escribe <carpeta>/<visual>.json y <carpeta>/<visual>.html; devuelve los datos."""
    datos = extraer(visual, raiz, run)
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / f"{visual}.json").write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (carpeta / f"{visual}.html").write_text(H.copiar_texto(VISUALES[visual][0], datos, tokens), encoding="utf-8")
    leer = carpeta.parent / "leer-imagen"
    leer.mkdir(exist_ok=True)
    (leer / f"{visual}.md").write_text(leer_imagen(visual, datos), encoding="utf-8")
    return datos


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("disponibles", "extraer", "construir", "origen"):
        s = sub.add_parser(n)
        s.add_argument("--raiz", default=".")
        s.add_argument("--run")
        if n in ("extraer", "construir", "origen"):
            s.add_argument("--visual", required=True)
        if n == "extraer":
            s.add_argument("--salida")
        if n == "construir":
            s.add_argument("--carpeta", required=True)
            s.add_argument("--diseno")
    a = ap.parse_args(argv)
    raiz = Path(a.raiz).resolve()
    try:
        if a.cmd == "disponibles":
            for v, motivo in disponibles(raiz, a.run).items():
                print(f"{v}: {'disponible' if motivo is None else 'falta fuente — ' + motivo}")
            return 0
        if a.cmd == "origen":
            o = origen(a.visual)
            print("visual no registrado" if o is None else f"{o[0]} · {o[1]} · se cambia con {o[2]}")
            return 0
        if a.cmd == "extraer":
            txt = json.dumps(extraer(a.visual, raiz, a.run), ensure_ascii=False, indent=2) + "\n"
            if a.salida:
                Path(a.salida).write_text(txt, encoding="utf-8")
            else:
                print(txt, end="")
            return 0
        tokens = H.cargar_tokens(raiz, a.diseno)
        construir(a.visual, raiz, a.carpeta, tokens, a.run)
        print(Path(a.carpeta) / f"{a.visual}.html")
        return 0
    except SinFuente as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
