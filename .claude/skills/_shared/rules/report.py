"""Reglas del paso 12-make-report (carpeta project/12-report/); las carga validate_run.py por el nombre de la carpeta.

Comprueba la corrida contra sí misma (informe.md, faltantes.md, imagenes/, anexos/ y HTML), no contra el config actual,
para que una corrida anterior siga validando aunque el config avance.
"""
import html
import re
from pathlib import Path

import doc_html as DH
import projectcfg as P
import report as R

A = R.INFORME
RE_SECCION = re.compile(r"^## (\d+(?:\.\d+)?)\. (.+?)\s*$")
RE_ANEXO_H = re.compile(r"^## Anexo ([A-Z]): (.+?)\s*$")
RE_CAP_H = re.compile(r"^# Capítulo (\d+): (.+?)\s*$")
RE_H1 = re.compile(r"^# (.+?)\s*$")
IMAGEN_MD = re.compile(r"!\[[^\]]*\]\([^)]*\)|<img\b", re.I)
IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}
VERSIONES = re.compile(r"^\|\s*(Versión|Avance)\s*\||\bv\d+ · Avance\b|\[A[123]\+?\]|Historial de versiones", re.I)
CAMPOS = ("Título del proyecto", "Tema", "Empresa", "Curso", "Docente", "Integrantes", "Fecha de entrega")
H1_PERMITIDOS = ("Referencias bibliográficas", "Anexos")


def vivas(txt):
    """Líneas fuera de bloques de código (las de dentro quedan vacías para conservar la numeración)."""
    lin = txt.splitlines()
    ok = R.fuera_de_codigo(lin)
    return [l if k in ok else "" for k, l in enumerate(lin)]


def _tabla_md(txt, seccion):
    """Primeras celdas de la tabla bajo «## <seccion>» de faltantes.md."""
    m = re.search(rf"^## {re.escape(seccion)}\s*$(.*?)(?=^## |\Z)", txt, re.M | re.S)
    if not m:
        return None
    filas = [l for l in m.group(1).splitlines() if l.startswith("|")]
    out = []
    for l in filas[2:]:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if c and c[0] not in ("—", ""):
            out.append(c[0])
    return out


def check_control(lin):
    inc = []
    if not lin or not lin[0].startswith("# Informe · "):
        inc.append((A, "el informe debe abrir con «# Informe · <nombre del proyecto>»"))
    try:
        k = lin.index("## Control del documento")
    except ValueError:
        return inc + [(A, "falta «## Control del documento»")]
    bloque = []
    for l in lin[k + 1:]:
        if l.startswith("#"):
            break
        bloque.append(l)
    campos = {c[0]: c[1] for c in ([x.strip() for x in l.strip().strip("|").split("|")] for l in bloque if l.startswith("|")) if len(c) >= 2}
    for c in CAMPOS:
        if not campos.get(c):
            inc.append((A, f"el control del documento no tiene el dato «{c}» (o «{R.PENDIENTE}»)"))
    for l in lin:
        if VERSIONES.search(l):
            inc.append((A, f"el informe es de una sola entrega: no lleva historial de versiones ni marcas de avance («{l.strip()[:50]}»)"))
            break
    return inc


def check_estructura(lin, idx):
    """Capítulos y secciones del índice en orden, sin repetir y bajo su capítulo. Devuelve (incidencias, secciones, anexos, líneas por sección)."""
    inc, vistas, anexos, por_seccion = [], [], [], {}
    orden = list(idx["puntos"])
    cap, ultimo_cap, actual, en_anexos = None, 0, None, False
    for l in lin:
        m = RE_CAP_H.match(l)
        if m:
            cap, actual, en_anexos = int(m.group(1)), None, False
            if idx["caps"].get(cap) != m.group(2):
                inc.append((A, f"el capítulo {cap} debe titularse «{idx['caps'].get(cap)}»"))
            if cap <= ultimo_cap:
                inc.append((A, f"el capítulo {cap} está repetido o fuera de orden"))
            ultimo_cap = cap
            continue
        m = RE_H1.match(l)
        if m and not l.startswith("# Informe · "):
            actual, cap = None, None
            en_anexos = m.group(1) == "Anexos"
            if m.group(1) not in H1_PERMITIDOS:
                inc.append((A, f"encabezado de primer nivel no previsto: «{m.group(1)}»"))
            continue
        m = RE_ANEXO_H.match(l)
        if m:
            actual = None
            if not en_anexos:
                inc.append((A, f"el Anexo {m.group(1)} debe ir bajo «# Anexos»"))
            d = idx["anexos"].get(m.group(1))
            if d is None:
                inc.append((A, f"el Anexo {m.group(1)} no existe en el índice"))
            elif d["titulo"] != m.group(2):
                inc.append((A, f"el Anexo {m.group(1)} debe titularse «{d['titulo']}»"))
            if m.group(1) in anexos or (anexos and m.group(1) < anexos[-1]):
                inc.append((A, f"el Anexo {m.group(1)} está repetido o fuera de orden"))
            anexos.append(m.group(1))
            continue
        m = RE_SECCION.match(l)
        if m:
            p, t = m.group(1), m.group(2)
            actual = p
            por_seccion.setdefault(p, [])
            d = idx["puntos"].get(p)
            if d is None:
                inc.append((A, f"la sección {p} no existe en el índice"))
                continue
            if d["titulo"] != t:
                inc.append((A, f"la sección {p} debe titularse «{d['titulo']}» (título del índice)"))
            if cap != d["capitulo"]:
                inc.append((A, f"la sección {p} debe ir dentro del capítulo {d['capitulo']}"))
            if p in vistas or (vistas and vistas[-1] in orden and orden.index(p) < orden.index(vistas[-1])):
                inc.append((A, f"la sección {p} está repetida o fuera del orden del índice"))
            vistas.append(p)
            continue
        if actual:
            por_seccion[actual].append(l)
    return inc, vistas, anexos, por_seccion


def check_faltantes(run, secciones, anexos, idx):
    f = Path(run) / "faltantes.md"
    if not f.is_file():
        return [("faltantes.md", "falta el archivo")]
    txt = f.read_text(encoding="utf-8")
    inc = []
    falt = _tabla_md(txt, "Secciones")
    falt_an = _tabla_md(txt, "Anexos")
    if falt is None:
        inc.append(("faltantes.md", "falta la tabla «## Secciones»"))
        falt = []
    if falt_an is None:
        inc.append(("faltantes.md", "falta la tabla «## Anexos»"))
        falt_an = []
    for p in idx["puntos"]:
        if p in secciones and p in falt:
            inc.append(("faltantes.md", f"la sección {p} está en el informe y en faltantes.md"))
        elif p not in secciones and p not in falt:
            inc.append(("faltantes.md", f"la sección {p} no está en el informe ni en faltantes.md"))
    for a in idx["anexos"]:
        if a in anexos and a in falt_an:
            inc.append(("faltantes.md", f"el Anexo {a} está en el informe y en faltantes.md"))
        elif a not in anexos and a not in falt_an:
            inc.append(("faltantes.md", f"el Anexo {a} no está en el informe ni en faltantes.md"))
    return inc


def check_figuras(run, archivo, lin, numerar=True):
    """Marcadores consecutivos, cada uno con «Cómo copiarla» y su HTML; sin marcas sin reemplazar ni imágenes incrustadas."""
    inc, esperado = [], 1
    base = (Path(run) / archivo).parent
    for k, l in enumerate(lin):
        if R.RE_FIGURA.match(l):
            inc.append((archivo, f"la marca «{l.strip()}» no se reemplazó por su marcador de imagen"))
        if R.RE_REF_FIGURA.search(l):
            inc.append((archivo, f"la referencia «{R.RE_REF_FIGURA.search(l).group(0)}» no se resolvió a un número de figura"))
        if IMAGEN_MD.search(l):
            inc.append((archivo, "las imágenes no se incrustan: cada figura es un marcador «(INCLUIR IMAGEN: …)»"))
        m = R.MARCADOR.match(l)
        if not m:
            continue
        n = int(m.group(1))
        if numerar and n != esperado:
            inc.append((archivo, f"la Figura {n} debe ser la {esperado} (numeración consecutiva)"))
        esperado = n + 1
        siguiente = next((x for x in lin[k + 1:] if x.strip()), "")
        if not siguiente.startswith(R.COMO_COPIAR):
            inc.append((archivo, f"la Figura {n} no lleva la línea «Cómo copiarla»"))
            continue
        ln = re.search(r"\]\(([^)\s]+\.(?:html|png))\)", siguiente)
        if ln and not (base / ln.group(1)).is_file():
            inc.append((archivo, f"«Cómo copiarla» de la Figura {n} apunta a {ln.group(1)}, que no existe en la corrida"))
    return inc


def check_tablas(lin):
    inc, esperado = [], 1
    for l in lin:
        m = R.RE_TITULO_TABLA.match(l)
        if m:
            n = int(m.group(2))
            if n != esperado:
                inc.append((A, f"la Tabla {n} debe ser la {esperado} (numeración consecutiva)"))
            esperado = n + 1
    return inc


def check_marcas_imagen(por_seccion, idx):
    skill = dict(P.secciones_pipeline())
    inc = []
    for p, lin in por_seccion.items():
        d = idx["puntos"].get(p)
        if d and d["imagen"] and not any(R.MARCADOR.match(l) for l in lin):
            inc.append((A, f"la sección {p} lleva la marca «(incluye imagen)» y no tiene su marcador de imagen: se corrige con {skill.get(p)}-update"))
    return inc


def check_sin_imagenes(run):
    inc = []
    for p in sorted(Path(run).rglob("*")):
        if p.is_file() and p.suffix.lower() in IMG_EXT:
            inc.append((str(p.relative_to(run)), "el informe no incluye archivos de imagen: el usuario las inserta en los marcadores"))
    return inc


def check_referencias(lin):
    try:
        k = lin.index("# Referencias bibliográficas")
    except ValueError:
        return [(A, "falta «# Referencias bibliográficas»")]
    entradas = []
    for l in lin[k + 1:]:
        if l.startswith("# "):
            break
        if l.strip():
            entradas.append(l.strip())
    if entradas and entradas[0].startswith(R.PENDIENTE):
        return []
    inc, vistas = [], set()
    for e in entradas:
        n = R._norm(e).lower()
        if n in vistas:
            inc.append((A, f"la referencia «{e[:60]}» está repetida"))
        vistas.add(n)
    if [R._clave_orden(e) for e in entradas] != sorted(R._clave_orden(e) for e in entradas):
        inc.append((A, "las referencias bibliográficas no están en orden alfabético"))
    return inc


def check_anexos(run, anexos):
    inc = []
    for a in anexos:
        if not (Path(run) / "anexos" / f"anexo-{a.lower()}.md").is_file():
            inc.append((f"anexos/anexo-{a.lower()}.md", f"falta el archivo del Anexo {a}, que está en el informe"))
    return inc


def check_indice_imagenes(run):
    d = Path(run) / "imagenes"
    htmls = sorted(d.glob("*.html")) if d.is_dir() else []
    if not htmls:
        return []
    ind = d / "INDICE.md"
    if not ind.is_file():
        return [("imagenes/INDICE.md", "falta el índice de las imágenes del informe")]
    txt = ind.read_text(encoding="utf-8")
    return [(f"imagenes/{h.name}", "no figura en imagenes/INDICE.md") for h in htmls if f"({h.name})" not in txt]


def _texto_html(h):
    return re.sub(r"[^a-z0-9áéíóúüñ]+", "", html.unescape(re.sub(r"<[^>]+>", "", h)).lower())


def check_html(run, lin):
    p = Path(run) / "informe.html"
    if not p.is_file():
        return []
    h = p.read_text(encoding="utf-8")
    inc = []
    if DH.EXTERNO.search(h):
        inc.append(("informe.html", "carga recursos externos"))
    en_html = [_texto_html(x) for x in re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", h, re.S)]
    en_md = [_texto_html(DH.inline(m.group(2))) for m in (R.RE_HEAD.match(l) for l in lin) if m]
    if en_html != en_md:
        inc.append(("informe.html", f"los encabezados no coinciden con los de informe.md ({len(en_html)} contra {len(en_md)}): vuelve a ejecutar render"))
    return inc


def check_anexos_html(run, raiz):
    origen = Path(run) / "anexos"
    if not (origen / "html").is_dir():
        return []
    try:
        tk = DH.tokens_del_config(raiz)
    except (P.ConfigError, OSError, ValueError):
        return [("anexos/html", "no se pudieron leer los tokens del sistema de diseño")]
    return [(f"anexos/html/{f}", causa) for f, causa in DH.comprobar(origen, origen / "html", tk, R.NOMBRE_ANEXOS)]


def validar(run):
    run = Path(run)
    raiz = run.parents[2]
    inf = run / R.INFORME
    if not inf.is_file():
        return [(A, "falta el archivo")]
    inc = []
    if not (run / "README.md").is_file():
        inc.append(("README.md", "falta el archivo (procedencia del informe)"))
    idx = R.cargar_indice()
    lin = vivas(inf.read_text(encoding="utf-8"))
    inc += check_control(lin)
    est, secciones, anexos, por_seccion = check_estructura(lin, idx)
    inc += est
    inc += check_faltantes(run, secciones, anexos, idx)
    inc += check_figuras(run, A, lin) + check_tablas(lin) + check_marcas_imagen(por_seccion, idx)
    for a in sorted((run / "anexos").glob("anexo-*.md")) if (run / "anexos").is_dir() else []:
        inc += check_figuras(run, f"anexos/{a.name}", vivas(a.read_text(encoding="utf-8")), numerar=False)
    inc += check_sin_imagenes(run) + check_referencias(lin) + check_anexos(run, anexos)
    inc += check_indice_imagenes(run) + check_html(run, lin) + check_anexos_html(run, raiz)
    return inc
