#!/usr/bin/env python3
"""Lectura, validación y registro del config del proyecto (project/config.yaml).

Uso (desde la raíz del repositorio):
  python3 .claude/skills/_shared/projectcfg.py show
  python3 .claude/skills/_shared/projectcfg.py validate
  python3 .claude/skills/_shared/projectcfg.py register --step 04-make-strategic-analysis --run 10-11-2026-00-00-46 [--no-mover]
  python3 .claude/skills/_shared/projectcfg.py check --skill 04-make-strategic-analysis
  python3 .claude/skills/_shared/projectcfg.py secciones [--json]
  python3 .claude/skills/_shared/projectcfg.py salida --step 09-make-dashboard --key enlace --value URL
  python3 .claude/skills/_shared/projectcfg.py set-diseno --value project/02-design-system/<corrida>/DESIGN.md
  python3 .claude/skills/_shared/projectcfg.py set-nucleo --tema "..." --inicio 01-11-2026 --entrega 30-11-2026
  python3 .claude/skills/_shared/projectcfg.py set-roles --rol "Ana=Analista de datos" --rol "Luis=Desarrollador Power BI"

Solo biblioteca estándar. El config nunca guarda credenciales.
Variable PROJECT_ROOT: raíz alternativa del repositorio (para pruebas).
"""
import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import yamlmini  # noqa: E402

SCHEMA = 3
MODOS = ("generado", "real")
TIPOS = ("empresa", "propio")
ESTADOS = ("disponible", "pendiente")
MAX_ROL = 60
BRIEF = "01-make-project-brief"
DISENO = "02-design-system"

CABECERA = """# Config del proyecto. Lo leen y actualizan las skills 00-init, 00-init-update y las numeradas.
# Puedes editar los valores a mano. Los comentarios explicativos de cada campo se regeneran al guardar;
# los comentarios propios que agregues se pierden cuando una skill escribe este archivo.
"""

COMENTARIOS = {
    "schema": "versión del formato (no cambiar)",
    "proyecto": "datos generales del proyecto",
    "proyecto.nombre": "nombre corto del proyecto",
    "proyecto.tema": "problema y solución de BI en una frase (copia del brief; lo define 01-make-project-brief)",
    "proyecto.tipo": "empresa = se aplica a una empresa (requiere ruc) · propio = proyecto o solución propia, sin empresa",
    "proyecto.ruc": "RUC de 11 dígitos (solo si tipo es empresa; con él se buscan sus datos en domain.md) · null si es propio",
    "proyecto.rubro": "sector o giro (por ejemplo: restaurantes, retail, salud)",
    "equipo": "integrantes del equipo",
    "equipo[].nombre": "nombre del integrante",
    "equipo[].rol": "responsabilidad en el proyecto, texto libre (por ejemplo: Analista de datos) · null si aún no tiene",
    "calendario": "fechas del proyecto (una sola entrega; copia del brief)",
    "calendario.inicio": "inicio del proyecto DD-MM-AAAA · null si aún no se conoce (lo define 01-make-project-brief)",
    "calendario.entrega": "fecha de entrega y exposición DD-MM-AAAA · null si aún no se conoce (lo define 01-make-project-brief)",
    "modo_datos": "generado = datos generados para el proyecto · real = datos abiertos o autorizados por la empresa",
    "diseno": "DESIGN.md vigente dentro de project/ · null hasta crear el sistema de diseño (02-design-system)",
    "dominio": "archivo con los datos de la empresa o de la solución",
    "informe": "estado del informe: qué secciones ya tienen contenido",
    "informe.secciones": "una entrada por punto del índice; la marca cada skill al registrar su corrida (12-make-report usa solo las disponibles)",
    "pasos": "corrida vigente de cada skill",
}

_SECCION_COM = {
    "skill": "skill que produce esta sección (de pipeline.json)",
    "run": "corrida vigente de esa skill que alimenta la sección · null si aún no hay",
    "estado": "disponible = tiene corrida · pendiente = falta ejecutar la skill",
}

_PASOS_COM = {
    "run": "carpeta de la corrida vigente en project/<NN-carpeta>/ · cámbiala a mano para usar otra versión",
    "fijada": "true = ninguna corrida nueva reemplaza a run · false = la última corrida pasa a ser la vigente",
    "historial": "todas las corridas de este paso, en orden",
    "salidas": "enlaces de resultados, nunca credenciales",
}


def comentario(ruta):
    """Comentario breve de un campo, por su ruta («a.b», «lista[].campo»)."""
    if ruta in COMENTARIOS:
        return COMENTARIOS[ruta]
    if ruta.startswith("informe.secciones."):
        return _SECCION_COM.get(ruta.rsplit(".", 1)[-1])
    partes = ruta.split(".")
    if partes[0] == "pasos" and len(partes) > 2:
        return _PASOS_COM.get(partes[-1])
    return None


class ConfigError(Exception):
    pass


def repo_root(root=None):
    if root:
        return Path(root)
    env = os.environ.get("PROJECT_ROOT")
    return Path(env) if env else HERE.parents[2]


def config_path(root=None):
    return repo_root(root) / "project" / "config.yaml"


def load_json(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def pipeline():
    return load_json("pipeline.json")["skills"]


def secciones_pipeline():
    """Lista ordenada de (sección, skill) según pipeline.json."""
    return [(x, s["nombre"]) for s in pipeline() for x in s.get("secciones", [])]


def _prohibidos():
    pol = load_json("policy.json")
    return [re.compile(p, re.I) for p in pol["prohibidos"]], [re.compile(e, re.I) for e in pol["excepciones"]]


def _strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from _strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from _strings(v)


def _check_entry(name, e, errs):
    if not isinstance(e, dict):
        errs.append(f"pasos.{name}: debe ser un objeto")
        return
    if "run" not in e or not (e["run"] is None or isinstance(e["run"], str)):
        errs.append(f"pasos.{name}.run: falta o no es texto")
    if not isinstance(e.get("fijada", False), bool):
        errs.append(f"pasos.{name}.fijada: debe ser booleano")
    if not isinstance(e.get("historial", []), list):
        errs.append(f"pasos.{name}.historial: debe ser una lista")


def _fecha(t):
    """date de un texto DD-MM-AAAA (None si no lo es)."""
    m = re.fullmatch(r"(\d{2})-(\d{2})-(\d{4})", t or "")
    if not m:
        return None
    try:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None


def a_txt(d):
    return d.strftime("%d-%m-%Y")


def _check_calendario(cal, errs):
    if not isinstance(cal, dict) or not all(cal.get(k) is None or isinstance(cal.get(k), str) for k in ("inicio", "entrega")):
        errs.append("calendario: requiere inicio y entrega (DD-MM-AAAA o null)")
        return
    fs = {}
    for k in ("inicio", "entrega"):
        if cal.get(k) is not None:
            f = _fecha(cal[k])
            if f is None:
                errs.append(f"calendario.{k}: «{cal[k]}» no es una fecha DD-MM-AAAA válida")
            else:
                fs[k] = f
    if len(fs) == 2 and fs["entrega"] < fs["inicio"]:
        errs.append(f"calendario: la entrega ({a_txt(fs['entrega'])}) debe ser igual o posterior al inicio ({a_txt(fs['inicio'])})")


def _check_informe(inf, errs):
    if not isinstance(inf, dict) or not isinstance(inf.get("secciones"), dict):
        errs.append("informe.secciones: debe ser un objeto con una entrada por sección")
        return
    validas = dict(secciones_pipeline())
    for sec, e in inf["secciones"].items():
        if sec not in validas:
            errs.append(f"informe.secciones: la sección {sec} no está declarada en pipeline.json")
            continue
        if not isinstance(e, dict):
            errs.append(f"informe.secciones.{sec}: debe ser un objeto")
            continue
        if e.get("skill") != validas[sec]:
            errs.append(f"informe.secciones.{sec}.skill: debe ser {validas[sec]} (según pipeline.json)")
        if e.get("estado") not in ESTADOS:
            errs.append(f"informe.secciones.{sec}.estado: debe ser uno de {ESTADOS}")
        if not (e.get("run") is None or isinstance(e.get("run"), str)):
            errs.append(f"informe.secciones.{sec}.run: texto o null")
        elif e.get("estado") == "disponible" and not e.get("run"):
            errs.append(f"informe.secciones.{sec}: disponible sin corrida")


def validate(cfg):
    """Devuelve la lista de errores (vacía si el config es válido)."""
    errs = []
    if not isinstance(cfg, dict):
        return ["el config debe ser un objeto"]
    if cfg.get("schema") != SCHEMA:
        return [f"schema {cfg.get('schema')!r} no soportado (se esperaba {SCHEMA}); ejecuta 00-init para crear un config nuevo"]
    p = cfg.get("proyecto")
    if not isinstance(p, dict) or not all(isinstance(p.get(k), str) for k in ("nombre", "tema", "rubro")):
        errs.append("proyecto: requiere nombre, tema y rubro (texto)")
    elif p.get("tipo") not in TIPOS:
        errs.append(f"proyecto.tipo: debe ser uno de {TIPOS}")
    elif p["tipo"] == "empresa" and not (isinstance(p.get("ruc"), str) and re.fullmatch(r"\d{11}", p["ruc"])):
        errs.append("proyecto.ruc: con tipo empresa debe ser un texto de 11 dígitos")
    elif p["tipo"] == "propio" and p.get("ruc") is not None:
        errs.append("proyecto.ruc: con tipo propio debe estar vacío (null)")
    eq = cfg.get("equipo")
    if not isinstance(eq, list) or not all(isinstance(m, dict) and isinstance(m.get("nombre"), str) and (m.get("rol") is None or isinstance(m.get("rol"), str)) for m in eq):
        errs.append("equipo: lista de {nombre, rol opcional}")
    else:
        for m in eq:
            if m.get("rol") is not None and not (0 < len(m["rol"].strip()) <= MAX_ROL):
                errs.append(f"equipo: el rol de {m['nombre']} debe tener entre 1 y {MAX_ROL} caracteres")
    _check_calendario(cfg.get("calendario"), errs)
    if cfg.get("modo_datos") not in MODOS:
        errs.append(f"modo_datos: debe ser uno de {MODOS}")
    if not (cfg.get("diseno") is None or isinstance(cfg.get("diseno"), str)):
        errs.append("diseno: ruta (texto) o null")
    if not isinstance(cfg.get("dominio"), str):
        errs.append("dominio: ruta (texto)")
    _check_informe(cfg.get("informe"), errs)
    pasos = cfg.get("pasos")
    if not isinstance(pasos, dict):
        errs.append("pasos: debe ser un objeto")
    else:
        for name, e in pasos.items():
            _check_entry(name, e, errs)
    pro, exc = _prohibidos()
    for s in _strings(cfg):
        if any(r.search(s) for r in pro) and not any(x.search(s) for x in exc):
            errs.append(f"texto no permitido en el config: {s[:60]!r}")
    return errs


def _seccion_vacia(skill):
    return {"skill": skill, "run": None, "estado": "pendiente"}


def completar_secciones(cfg):
    """Agrega como pendientes las secciones de pipeline.json que falten en el config, en el orden del índice.

    Devuelve la lista de secciones agregadas. Las ya presentes no cambian; las desconocidas se
    conservan al final para que `validate` las informe.
    """
    inf = cfg.setdefault("informe", {})
    actuales = inf.get("secciones") if isinstance(inf.get("secciones"), dict) else {}
    nuevas, agregadas = {}, []
    for sec, skill in secciones_pipeline():
        if sec in actuales:
            nuevas[sec] = actuales[sec]
        else:
            nuevas[sec] = _seccion_vacia(skill)
            agregadas.append(sec)
    for sec, e in actuales.items():
        if sec not in nuevas:
            nuevas[sec] = e
    inf["secciones"] = nuevas
    return agregadas


def load(root=None):
    path = config_path(root)
    if not path.exists():
        raise ConfigError(f"no existe {path}; ejecuta la skill 00-init")
    try:
        cfg = yamlmini.loads(path.read_text(encoding="utf-8"))
    except yamlmini.YamlError as e:
        raise ConfigError(f"{path} no es YAML válido ({e}); corrígelo a mano o ejecuta 00-init-update")
    if isinstance(cfg, dict) and cfg.get("schema") == SCHEMA:
        completar_secciones(cfg)
    errs = validate(cfg)
    if errs:
        raise ConfigError("config inválido: " + "; ".join(errs))
    return cfg


def save(cfg, root=None):
    errs = validate(cfg)
    if errs:
        raise ConfigError("no se guarda: " + "; ".join(errs))
    path = config_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".yaml.tmp")
    tmp.write_text(CABECERA + "\n" + yamlmini.dumps(cfg, comentario), encoding="utf-8")
    os.replace(tmp, path)


def new_config(**kw):
    cfg = {
        "schema": SCHEMA,
        "proyecto": {"nombre": "", "tema": "", "tipo": "propio", "ruc": None, "rubro": ""},
        "equipo": [],
        "calendario": {"inicio": None, "entrega": None},
        "modo_datos": "generado",
        "diseno": None,
        "dominio": "project/domain.md",
        "informe": {"secciones": {}},
        "pasos": {},
    }
    cfg.update(kw)
    completar_secciones(cfg)
    return cfg


def _marcar_secciones(cfg, step):
    """Apunta las secciones de `step` a la corrida vigente del paso (disponibles si la hay)."""
    run = cfg["pasos"].get(step, {}).get("run")
    for sec, skill in secciones_pipeline():
        if skill != step:
            continue
        e = cfg["informe"]["secciones"].setdefault(sec, _seccion_vacia(skill))
        e["run"] = run
        e["estado"] = "disponible" if run else "pendiente"


def register(step, run, root=None, mover=True):
    """Agrega la corrida al historial; mueve `run` salvo que `fijada` sea true o mover=False.

    Además apunta las secciones del informe de esa skill a la corrida vigente del paso.
    """
    step_info(step)
    cfg = load(root)
    entry = cfg["pasos"].setdefault(step, {"run": None, "fijada": False, "historial": []})
    entry.setdefault("historial", [])
    if run not in entry["historial"]:
        entry["historial"].append(run)
    moved = mover and not entry.get("fijada", False)
    if moved:
        entry["run"] = run
    _marcar_secciones(cfg, step)
    save(cfg, root)
    secs = [s for s, k in secciones_pipeline() if k == step]
    return {"step": step, "run": entry["run"], "movido": moved, "fijada": entry.get("fijada", False), "secciones": secs}


def secciones(root=None):
    """Estado de cada sección del informe: [{seccion, skill, estado, run, motivo}].

    Una sección disponible cuya carpeta de corrida no existe se devuelve como pendiente, con el motivo.
    """
    cfg = load(root)
    out = []
    for sec, e in cfg["informe"]["secciones"].items():
        item = {"seccion": sec, "skill": e["skill"], "estado": e["estado"], "run": e.get("run"), "motivo": None}
        if e["estado"] == "disponible":
            d = run_dir(e["skill"], e["run"], root)
            if d is not None and not d.exists():
                item["estado"] = "pendiente"
                item["motivo"] = f"no existe la carpeta de la corrida {e['run']}"
        else:
            item["motivo"] = f"falta ejecutar {e['skill']}"
        out.append(item)
    return out


def set_salida(step, key, value, root=None):
    cfg = load(root)
    entry = cfg["pasos"].setdefault(step, {"run": None, "fijada": False, "historial": []})
    entry.setdefault("salidas", {})[key] = value
    save(cfg, root)


def set_roles(roles, root=None):
    """Guarda roles libres en equipo[].rol. `roles` es {nombre: rol}; solo cambian los nombrados.

    Rechaza el reparto completo si nombra a alguien que no está en el equipo o si un rol es vacío o muy largo.
    """
    cfg = load(root)
    nombres = [m["nombre"] for m in cfg["equipo"]]
    errs = [f"{n} no pertenece al equipo" for n in roles if n not in nombres]
    errs += [f"el rol de {n} debe tener entre 1 y {MAX_ROL} caracteres" for n, r in roles.items() if not (0 < len((r or "").strip()) <= MAX_ROL)]
    if errs:
        raise ConfigError("reparto de roles rechazado: " + "; ".join(errs))
    for m in cfg["equipo"]:
        if m["nombre"] in roles:
            m["rol"] = roles[m["nombre"]].strip()
    save(cfg, root)
    return {m["nombre"]: m["rol"] for m in cfg["equipo"]}


_SIN_CAMBIO = object()


def set_nucleo(tema=None, inicio=_SIN_CAMBIO, entrega=_SIN_CAMBIO, root=None):
    """Copia al config lo que define el brief: tema y fechas de inicio y entrega (None = pendiente).

    Valida el config completo antes de guardar; si falla, no escribe nada.
    """
    cfg = load(root)
    if tema is not None:
        cfg["proyecto"]["tema"] = tema
    if inicio is not _SIN_CAMBIO:
        cfg["calendario"]["inicio"] = inicio
    if entrega is not _SIN_CAMBIO:
        cfg["calendario"]["entrega"] = entrega
    errs = validate(cfg)
    if errs:
        raise ConfigError("núcleo rechazado: " + "; ".join(errs))
    save(cfg, root)
    return {"tema": cfg["proyecto"]["tema"], "calendario": cfg["calendario"]}


def set_diseno(path, root=None):
    """Apunta `diseno` al DESIGN.md vigente, salvo que el paso 02-design-system esté fijado."""
    cfg = load(root)
    if cfg["pasos"].get(DISENO, {}).get("fijada", False):
        return False
    cfg["diseno"] = path
    save(cfg, root)
    return True


def step_info(step):
    for s in pipeline():
        if s["nombre"] == step:
            return s
    raise ConfigError(f"paso desconocido: {step}")


def current_run(step, root=None):
    cfg = load(root)
    e = cfg["pasos"].get(step)
    return None if e is None else e.get("run")


def run_dir(step, name, root=None):
    carpeta = step_info(step)["carpeta"]
    if carpeta is None or not name:
        return None
    return repo_root(root) / "project" / carpeta / name


def check(skill, root=None):
    """Avisos de prerrequisitos que ya existen como skill y no tienen corrida. No bloquea."""
    info = step_info(skill)
    skills_dir = repo_root(root) / ".claude" / "skills"
    avisos = []
    try:
        cfg = load(root)
    except ConfigError as e:
        if skill != "00-init":
            avisos.append(str(e))
        return avisos
    if not skill.startswith(("00-", "01-")) and not (repo_root(root) / cfg["dominio"]).exists():
        avisos.append(f"no existe {cfg['dominio']}: ejecuta {BRIEF} para crear los datos del dominio")
    if int(skill[:2]) >= 3:
        b = cfg["pasos"].get(BRIEF)
        if not (b and b.get("run")):
            avisos.append(f"falta el brief del proyecto: no tiene corrida registrada (ejecuta {BRIEF}; las demás skills leen de él el tema, los objetivos y el calendario)")
    for req in info["requiere"]:
        if not (skills_dir / req).is_dir() or req == "00-init":
            continue
        e = cfg["pasos"].get(req)
        if not (e and e.get("run")):
            avisos.append(f"falta el paso {req}: no tiene corrida registrada en el config")
        else:
            d = run_dir(req, e["run"], root)
            if d is not None and not d.exists():
                avisos.append(f"la corrida {e['run']} del paso {req} no existe en disco")
    return avisos


def _fecha_arg(v):
    return None if v in (None, "-") else v


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show")
    sub.add_parser("validate")
    r = sub.add_parser("register"); r.add_argument("--step", required=True); r.add_argument("--run", required=True); r.add_argument("--no-mover", action="store_true")
    c = sub.add_parser("check"); c.add_argument("--skill", required=True)
    se = sub.add_parser("secciones"); se.add_argument("--json", action="store_true")
    s = sub.add_parser("salida"); s.add_argument("--step", required=True); s.add_argument("--key", required=True); s.add_argument("--value", required=True)
    d = sub.add_parser("set-diseno"); d.add_argument("--value", required=True)
    nu = sub.add_parser("set-nucleo"); nu.add_argument("--tema")
    nu.add_argument("--inicio", help="DD-MM-AAAA o - si no se conoce"); nu.add_argument("--entrega", help="DD-MM-AAAA o - si no se conoce")
    ro = sub.add_parser("set-roles"); ro.add_argument("--rol", action="append", required=True, help='"Nombre=Rol", repetible')
    g = sub.add_parser("current"); g.add_argument("--step", required=True)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "show":
            print(json.dumps(load(), ensure_ascii=False, indent=2))
        elif a.cmd == "validate":
            load()
            print("config válido")
        elif a.cmd == "register":
            print(json.dumps(register(a.step, a.run, mover=not a.no_mover), ensure_ascii=False))
        elif a.cmd == "check":
            av = check(a.skill)
            print("\n".join(av) if av else "prerrequisitos en orden")
        elif a.cmd == "secciones":
            res = secciones()
            if a.json:
                print(json.dumps(res, ensure_ascii=False, indent=1))
            else:
                for x in res:
                    extra = f" ({x['motivo']})" if x["estado"] == "pendiente" else f" ({x['run']})"
                    print(f"{x['seccion']:>5}  {x['estado']:<10}  {x['skill']}{extra}")
        elif a.cmd == "salida":
            set_salida(a.step, a.key, a.value)
            print("salida registrada")
        elif a.cmd == "set-roles":
            pares = {}
            for x in a.rol:
                if "=" not in x:
                    raise ConfigError(f"formato no válido «{x}»: use \"Nombre=Rol\"")
                n, r_ = x.split("=", 1)
                pares[n.strip()] = r_.strip()
            print(json.dumps(set_roles(pares), ensure_ascii=False))
        elif a.cmd == "set-nucleo":
            kw = {}
            if a.inicio is not None:
                kw["inicio"] = _fecha_arg(a.inicio)
            if a.entrega is not None:
                kw["entrega"] = _fecha_arg(a.entrega)
            print(json.dumps(set_nucleo(a.tema, **kw), ensure_ascii=False))
        elif a.cmd == "set-diseno":
            if set_diseno(a.value):
                print("diseno actualizado")
                import visuales  # las figuras ya construidas toman el nuevo sistema de diseño
                n = len(visuales.aplicar_diseno(repo_root()))
                print(f"{n} figura(s) actualizadas con el nuevo sistema de diseño")
            else:
                print(f"el paso {DISENO} está fijado: diseno no cambia")
        elif a.cmd == "current":
            print(current_run(a.step) or "")
    except ConfigError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
