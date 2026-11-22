#!/usr/bin/env python3
"""Corridas versionadas: crear, bifurcar (fork) y localizar la vigente.

  python3 .claude/skills/_shared/runs.py new  --step 04-make-strategic-analysis
  python3 .claude/skills/_shared/runs.py fork --step 04-make-strategic-analysis [--base NOMBRE] --cambios "texto" [--cambios ...]
  python3 .claude/skills/_shared/runs.py current --step 04-make-strategic-analysis

Las corridas se crean en project/<NN-carpeta>/<DD-MM-AAAA-HH-MM-SS>/ (carpeta numerada según pipeline.json).

`new` y `fork` imprimen la ruta creada. Ninguno modifica el config: el registro
lo hace la skill con projectcfg.py register una vez que la corrida esta completa.
Solo biblioteca estandar. PROJECT_ROOT cambia la raiz (pruebas).
"""
import argparse
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import projectcfg as P  # noqa: E402


def timestamp(now=None):
    return time.strftime("%d-%m-%Y-%H-%M-%S", now or time.localtime())


def step_dir(step, root=None):
    carpeta = P.step_info(step)["carpeta"]
    if carpeta is None:
        raise P.ConfigError(f"el paso {step} no tiene carpeta propia")
    return P.repo_root(root) / "project" / carpeta


def _unique(parent, name):
    """Evita choque de nombres si dos corridas caen en el mismo segundo."""
    cand, n = name, 1
    while (parent / cand).exists():
        n += 1
        cand = f"{name}-{n}"
    return cand


def new(step, root=None, now=None):
    parent = step_dir(step, root)
    parent.mkdir(parents=True, exist_ok=True)
    name = _unique(parent, timestamp(now))
    path = parent / name
    path.mkdir()
    return path


def base_run(step, base=None, root=None):
    """Corrida base: la indicada o la vigente del config."""
    name = base or P.current_run(step, root)
    if not name:
        raise P.ConfigError(f"el paso {step} no tiene corrida vigente; indica una con --base")
    path = step_dir(step, root) / name
    if not path.is_dir():
        raise P.ConfigError(f"la corrida base {path} no existe")
    return path


def fork(step, cambios, base=None, root=None, now=None):
    src = base_run(step, base, root)
    parent = src.parent
    name = _unique(parent, timestamp(now) + "-fork")
    dst = parent / name
    shutil.copytree(src, dst)
    readme = dst / "README.md"
    prev = readme.read_text(encoding="utf-8").rstrip("\n") if readme.exists() else ""
    nota = ["", "", "## Origen de esta versión", "", f"Copia de la corrida `{src.name}`. Cambios aplicados:", ""]
    nota += [f"- {c}" for c in cambios] or ["- (sin cambios registrados)"]
    readme.write_text(prev + "\n".join(nota) + "\n", encoding="utf-8")
    return dst


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new"); n.add_argument("--step", required=True)
    f = sub.add_parser("fork"); f.add_argument("--step", required=True); f.add_argument("--base"); f.add_argument("--cambios", action="append", default=[])
    c = sub.add_parser("current"); c.add_argument("--step", required=True)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "new":
            print(new(a.step))
        elif a.cmd == "fork":
            print(fork(a.step, a.cambios, a.base))
        else:
            print(P.current_run(a.step) or "")
    except P.ConfigError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
