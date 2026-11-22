"""Proyecto de ejemplo con el brief del ejemplo de brief-1-nucleo.md registrado como corrida vigente."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import projectcfg as P  # noqa: E402

COMMON = HERE.parents[2] / "common"
RUN = "10-11-2026-07-00-00"


def brief_md():
    t = (COMMON / "01-project-brief" / "models" / "brief-1-nucleo.md").read_text(encoding="utf-8")
    return re.findall(r"```markdown\n(.*?)```", t, flags=re.S)[-1].strip() + "\n"


def crear(raiz, copiar_al_config=True, domain=True):
    """Config del ejemplo, domain.md y el brief como corrida vigente; devuelve la carpeta de la corrida."""
    import brief as BR
    raiz = Path(raiz)
    if not (raiz / "project" / "config.yaml").exists():
        cfg = P.new_config()
        cfg["proyecto"] = {"nombre": "Rentabilidad por canal de Pollería Don Tito", "tema": "", "tipo": "propio", "ruc": None, "rubro": "restaurantes"}
        cfg["equipo"] = [{"nombre": "ariel", "rol": None}, {"nombre": "Piero", "rol": "Analista de datos"}]
        P.save(cfg, raiz)
    run = raiz / "project" / BR.CARPETA / RUN
    run.mkdir(parents=True)
    (run / "brief.md").write_text(brief_md(), encoding="utf-8")
    (run / "README.md").write_text("# Procedencia\n", encoding="utf-8")
    P.register(BR.PASO, RUN, root=raiz)
    if domain and not (raiz / "project" / "domain.md").exists():
        (raiz / "project" / "domain.md").write_text("# Dominio del proyecto\n\nTipo: propio\n", encoding="utf-8")
    if copiar_al_config:
        BR.al_config(raiz)
    return run
