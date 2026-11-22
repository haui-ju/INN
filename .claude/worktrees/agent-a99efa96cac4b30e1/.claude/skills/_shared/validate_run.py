#!/usr/bin/env python3
"""Validador de coherencia de una corrida.

  python3 .claude/skills/_shared/validate_run.py RUTA_CORRIDA [--step 04-make-strategic-analysis]

Reglas genericas: enlaces relativos que resuelven, terminos prohibidos fuera de
README.md, fracciones «N de M» con N <= M y porcentajes coherentes con su fraccion.
Con reglas del paso (rules/<modulo>.py): codigos citados que no estan definidos (PREFIJOS)
y comprobaciones propias del paso (gancho opcional validar(run) -> [(archivo, mensaje)]).
Un codigo esta definido si es el nombre de un archivo, un titulo o la primera
celda de una tabla. Sale con codigo 1 si hay incidencias. Solo biblioteca estandar.
"""
import argparse
import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import projectcfg as P  # noqa: E402

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FRAC = re.compile(r"\b(\d+) de (\d+)\b(?:[^.\n;|\d]{0,40}?\((\d+)\s?%\))?")
RULES_DIR = HERE / "rules"


def modulo_reglas(carpeta):
    """Módulo de reglas de una carpeta de paso: `NN-nombre-con-guiones` -> `rules/nombre_con_guiones.py` (None si no hay)."""
    mod = re.sub(r"^\d{2}-", "", carpeta).replace("-", "_")
    return mod if (RULES_DIR / f"{mod}.py").is_file() else None


def md_files(run):
    return sorted(p for p in Path(run).rglob("*.md") if p.is_file())


def strip_code(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


def check_links(run, files):
    out = []
    for f in files:
        for m in LINK.finditer(strip_code(f.read_text(encoding="utf-8"))):
            t = m.group(1)
            if re.match(r"^[a-z]+:", t) or t.startswith("#"):
                continue
            t = t.split("#")[0]
            if t and not (f.parent / t).exists():
                out.append((f, f"enlace roto: {m.group(1)}"))
    return out


def check_policy(run, files):
    pol = P.load_json("policy.json")
    pro = [re.compile(p, re.I) for p in pol["prohibidos"]]
    exc = [re.compile(e, re.I) for e in pol["excepciones"]]
    exentos = set(pol["archivos_exentos"])
    out = []
    for f in files:
        if f.name in exentos:
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            clean = line
            for e in exc:
                clean = e.sub("", clean)
            for r in pro:
                m = r.search(clean)
                if m:
                    out.append((f, f"línea {i}: término no permitido «{m.group(0)}»"))
    return out


def check_fractions(run, files):
    out = []
    for f in files:
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for m in FRAC.finditer(line):
                n, d, pct = int(m.group(1)), int(m.group(2)), m.group(3)
                if d and n > d:
                    out.append((f, f"línea {i}: fracción incoherente «{m.group(1)} de {m.group(2)}»"))
                elif pct is not None and d and abs(round(100 * n / d) - int(pct)) > 1:
                    out.append((f, f"línea {i}: «{n} de {d}» no coincide con {pct}%"))
    return out


def defined_codes(run, files, prefijos):
    alt = "|".join(re.escape(p) for p in sorted(prefijos, key=len, reverse=True))
    code = re.compile(rf"^(?:{alt})-\d+$")
    cell = re.compile(rf"^\|\s*\**((?:{alt})-\d+)\**\s*\|")
    head = re.compile(rf"^#+\s+\**((?:{alt})-\d+)\b")
    bullet = re.compile(rf"^\s*[-*]\s+\**((?:{alt})-\d+)\**[\s:·.]")
    defs = set()
    for f in files:
        if code.match(f.stem):
            defs.add(f.stem)
        for line in f.read_text(encoding="utf-8").splitlines():
            for rx in (cell, head, bullet):
                m = rx.match(line)
                if m:
                    defs.add(m.group(1))
    return defs


def check_codes(run, files, prefijos):
    alt = "|".join(re.escape(p) for p in sorted(prefijos, key=len, reverse=True))
    cite = re.compile(rf"\b((?:{alt})-\d+)\b")
    defs = defined_codes(run, files, prefijos)
    out, seen = [], set()
    for f in files:
        if f.name == "README.md":
            continue
        for m in cite.finditer(strip_code(f.read_text(encoding="utf-8"))):
            c = m.group(1)
            if c not in defs and (f, c) not in seen:
                seen.add((f, c))
                out.append((f, f"código citado sin definir: {c}"))
    return out


def validate(run, step=None):
    run = Path(run)
    files = md_files(run)
    inc = check_links(run, files) + check_policy(run, files) + check_fractions(run, files)
    mod = modulo_reglas(run.parent.name)
    if mod:
        rules = importlib.import_module(f"rules.{mod}")
        if hasattr(rules, "PREFIJOS"):
            inc += check_codes(run, files, rules.PREFIJOS)
        extra = rules.validar(run) if hasattr(rules, "validar") else []
        return [(str(f.relative_to(run)), msg) for f, msg in inc] + [(str(f), msg) for f, msg in extra]
    return [(str(f.relative_to(run)), msg) for f, msg in inc]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--step")
    a = ap.parse_args(argv)
    if not Path(a.run).is_dir():
        print(f"ERROR: {a.run} no es una carpeta", file=sys.stderr)
        return 2
    inc = validate(a.run, a.step)
    for f, msg in inc:
        print(f"{f}: {msg}")
    print(f"{len(inc)} incidencia(s)" if inc else "sin incidencias")
    return 1 if inc else 0


if __name__ == "__main__":
    sys.exit(main())
