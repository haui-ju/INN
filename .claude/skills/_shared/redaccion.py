#!/usr/bin/env python3
"""Revisor de calidad de redacción de un texto Markdown (informe o sección). Solo biblioteca estándar.

  python3 .claude/skills/_shared/redaccion.py revisar RUTA.md [--json] [--max-frase 40] [--estricto]

Revisa la prosa (no las tablas, el código, los encabezados ni las marcas de figura) y avisa de rasgos que vuelven genérico un texto:
frases de relleno, palabras infladas, gerundios de cierre, contrastes «no solo… sino», arranques repetidos, frases muy largas,
ritmo uniforme, párrafos sin dato propio (cifra, código o cita) y siglas que se usan sin definir.
Es una guía de calidad para que el equipo edite: NO predice el resultado de Turnitin ni de ningún detector.
Cada tipo de aviso es una regla de common/redaccion/guia.md (R-01 a R-09). Sale con código 0 aunque haya avisos; con --estricto sale con 1
si queda algún aviso bloqueante; con --json imprime la lista completa.
"""
import argparse
import json
import re
import statistics
import sys
from pathlib import Path

RELLENO = [
    r"es importante (?:destacar|mencionar|señalar|resaltar)", r"cabe (?:destacar|mencionar|señalar|resaltar)", r"vale la pena (?:destacar|mencionar)",
    r"en conclusión", r"en resumen", r"sin lugar a dudas", r"en el mundo actual", r"en la actualidad", r"hoy en día",
    r"juega un papel (?:fundamental|clave|crucial)", r"desempeña un papel (?:fundamental|clave|crucial)", r"en el ámbito de",
    r"a lo largo de", r"en el marco de", r"de manera integral", r"se erige como", r"constituye un pilar", r"es fundamental que",
]
INFLADAS = ["fundamental", "crucial", "robusto", "robusta", "innovador", "innovadora", "integral", "transformador", "transformadora",
            "revolucionario", "óptimo", "vital", "esencial", "holístico", "holística", "sinergia"]
GERUNDIO = re.compile(r",\s+(?:permitiendo|facilitando|generando|optimizando|garantizando|asegurando|fomentando|promoviendo|contribuyendo|logrando)\b", re.I)
CONTRASTE = re.compile(r"\bno (?:solo|solamente|es)\b[^.]{0,80}\bsino\b", re.I)
SIGLA = re.compile(r"\b[A-ZÁÉÍÓÚÑ]{2,6}\b(?!-\d)")
COMUNES = {"BI", "ETL", "KPI", "DAX", "PDF", "HTML", "CSV", "UIT", "RUC", "APA", "FODA", "PESTEL", "IA", "UTC", "SQL", "OK", "II", "III", "IV", "OE", "OG", "AV", "SJL"}
CITA = re.compile(r"\([^()]*,\s*(?:19|20)\d{2}[a-z]?\)|[A-ZÁÉÍÓÚÑ][^\s(),]+\s+\((?:19|20)\d{2}[a-z]?\)")
CODIGO = re.compile(r"\b[A-Z]{2,4}-\d{1,3}\b")


# tipo de aviso -> (regla de common/redaccion/guia.md, bloqueante)
REGLAS = {"relleno": ("R-01", True), "inflado": ("R-02", True), "gerundio": ("R-03", True), "contraste": ("R-04", True),
          "arranque-repetido": ("R-05", True), "sigla": ("R-06", True), "frase-larga": ("R-07", False), "ritmo": ("R-08", False), "sin-dato": ("R-09", False)}


def bloqueantes(avisos):
    return [a for a in avisos if REGLAS[a["tipo"]][1]]


def prosa(txt):
    """[(línea, texto)] de los párrafos de prosa, sin tablas, código, encabezados, marcas de figura ni títulos de tabla."""
    txt = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), txt, flags=re.S)
    out, cur, ini = [], [], 0
    for i, ln in enumerate(txt.splitlines() + [""], 1):
        s = ln.strip()
        ignora = (not s or s.startswith(("|", "#", "<!--", "(INCLUIR IMAGEN", ">")) or re.match(r"^(Tabla|Figura) \d+:", s)
                  or re.match(r"^\*\*Cómo (?:copiar|leer)", s) or re.match(r"^[-*] \*\*", s))
        if ignora:
            if cur:
                out.append((ini, " ".join(cur)))
            cur = []
            continue
        if not cur:
            ini = i
        cur.append(re.sub(r"\(INCLUIR IMAGEN:[^)]*\)", "", re.sub(r"^[-*]\s+", "", s)).replace("**", ""))
    return out


def frases(parrafo):
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡«0-9])", parrafo) if f.strip()]


def palabras(t):
    return len(re.findall(r"\w+", t))


def revisar(txt, max_frase=40):
    """[{linea, tipo, detalle}] de avisos de calidad del texto."""
    av = []
    ps = prosa(txt)
    todas = []
    for ln, p in ps:
        fs = frases(p)
        todas += fs
        for pat in RELLENO:
            m = re.search(pat, p, re.I)
            if m:
                av.append({"linea": ln, "tipo": "relleno", "detalle": f"«{m.group(0)}»: empieza por el contenido"})
        for w in INFLADAS:
            if re.search(rf"\b{w}\b", p, re.I):
                av.append({"linea": ln, "tipo": "inflado", "detalle": f"«{w}»: cámbiala por el dato o elimínala"})
        if GERUNDIO.search(p):
            av.append({"linea": ln, "tipo": "gerundio", "detalle": f"gerundio de cierre «{GERUNDIO.search(p).group(0).strip(', ')}»: parte la frase o corta"})
        if CONTRASTE.search(p):
            av.append({"linea": ln, "tipo": "contraste", "detalle": "contraste «no solo… sino»: afirma directamente lo que sí es"})
        for f in fs:
            if palabras(f) > max_frase:
                av.append({"linea": ln, "tipo": "frase-larga", "detalle": f"frase de {palabras(f)} palabras («{f[:50]}…»): divídela"})
        ini = [re.sub(r"\W", "", f.split()[0]).lower() for f in fs if f.split()]
        for k in range(len(ini) - 2):
            if ini[k] and ini[k] == ini[k + 1] == ini[k + 2]:
                av.append({"linea": ln, "tipo": "arranque-repetido", "detalle": f"tres frases seguidas empiezan con «{ini[k]}»: varía el arranque"})
                break
        if palabras(p) >= 35 and not re.search(r"\d", p) and not CODIGO.search(p) and not CITA.search(p):
            av.append({"linea": ln, "tipo": "sin-dato", "detalle": "párrafo sin cifra, código ni cita: agrega el dato propio del caso o una fuente"})
    largos = [palabras(f) for f in todas]
    if len(largos) >= 8 and statistics.pstdev(largos) < 4:
        av.append({"linea": 0, "tipo": "ritmo", "detalle": f"las frases miden casi lo mismo (desviación {statistics.pstdev(largos):.1f}): alterna frases cortas y largas"})
    cuerpo = "\n".join(p for _, p in ps)
    definidas = set(re.findall(r"\(([A-ZÁÉÍÓÚÑ]{2,6})\)", txt))
    vistas = set()
    for ln, p in ps:
        for s in SIGLA.findall(p):
            if s in COMUNES or s in definidas or s in vistas:
                continue
            vistas.add(s)
            av.append({"linea": ln, "tipo": "sigla", "detalle": f"«{s}» se usa sin definirla la primera vez (escribe el nombre completo y la sigla entre paréntesis)"})
    return av


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("revisar")
    r.add_argument("ruta")
    r.add_argument("--json", action="store_true")
    r.add_argument("--max-frase", type=int, default=40)
    r.add_argument("--estricto", action="store_true")
    a = ap.parse_args(argv)
    f = Path(a.ruta)
    if not f.is_file():
        print(f"ERROR: {f} no es un archivo", file=sys.stderr)
        return 2
    av = revisar(f.read_text(encoding="utf-8"), a.max_frase)
    for x in av:
        x["regla"] = REGLAS[x["tipo"]][0]
        x["bloqueante"] = REGLAS[x["tipo"]][1]
    rc = 1 if a.estricto and bloqueantes(av) else 0
    if a.json:
        print(json.dumps(av, ensure_ascii=False, indent=2))
        return rc
    for x in sorted(av, key=lambda x: (x["linea"], x["tipo"])):
        print(f"{f.name}:{x['linea']}: [{x['regla']} {x['tipo']}{' · bloqueante' if x['bloqueante'] else ''}] {x['detalle']}")
    tipos = {}
    for x in av:
        tipos[x["tipo"]] = tipos.get(x["tipo"], 0) + 1
    print(f"{len(av)} aviso(s), {len(bloqueantes(av))} bloqueante(s)" + (": " + ", ".join(f"{k} {v}" for k, v in sorted(tipos.items())) if av else ""))
    return rc


if __name__ == "__main__":
    sys.exit(main())
