"""Proyecto de ejemplo del paso 08-make-etl: el de los capítulos 1 y 2, los datos de data/ (hoja de respuestas y salida del equipo) y una corrida de 08 armada con los ejemplos de las plantillas."""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagnostico_fixtures as F  # noqa: E402
import projectcfg as P  # noqa: E402

PASO = "08-make-etl"
RUN = "16-11-2026-08-00-00"
COMMON = HERE.parents[2] / "common" / "08-etl" / "models"
MODELOS = {"secciones/3.1.md": "etl-1-seccion-3-1.md", "anexos/A.md": "etl-2-anexo-a.md", "anexos/B.md": "etl-3-anexo-b.md",
           "materiales/guia-power-query.md": "etl-4-guia-power-query.md"}

DEFECTOS = [("FUE-01", "nombre_producto", 35, "Homologar los nombres de producto"), ("FUE-01", "formato_fecha", 60, "Convertir las fechas a AAAA-MM-DD"),
            ("FUE-02", "duplicado", 32, "Quitar los pedidos repetidos"), ("FUE-01", "registro_invalido", 18, "Descartar los registros sin cantidad"),
            ("FUE-01", "nulo", 25, "Reemplazar los turnos vacíos"), ("FUE-03", "dia_sin_precio", 12, "Completar los días sin precio")]
VENTAS = [("2026-01", "Salón", 400, 18000.0, 0.0), ("2026-01", "Rappi", 150, 9000.0, 2250.0),
          ("2026-02", "Salón", 520, 23400.0, 0.0), ("2026-02", "Rappi", 480, 28800.0, 7200.0)]
PRODUCCION = [("2026-01", "Mañana", 100, 94, 6), ("2026-02", "Mañana", 120, 112, 8)]
PRECIO = [("2026-01", 6.5, 1), ("2026-02", 6.5, 0)]


def ejemplo(ruta):
    """Último bloque de markdown de una plantilla (con cuatro comillas si el ejemplo trae bloques de código)."""
    t = Path(ruta).read_text(encoding="utf-8")
    cuatro = re.findall(r"````markdown\n(.*?)````", t, flags=re.S)
    return (cuatro or re.findall(r"```markdown\n(.*?)```", t, flags=re.S))[-1].strip() + "\n"


def ejemplo_json(ruta):
    return re.findall(r"```json\n(.*?)```", Path(ruta).read_text(encoding="utf-8"), flags=re.S)[-1].strip() + "\n"


def _csv(ruta, cabecera, filas):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cabecera)
        w.writerows(filas)


def datos(raiz):
    """data/respuestas/ (lo esperado) y data/salida/ (lo que exportó el equipo), coherentes con el ejemplo de evidencia.json."""
    d = Path(raiz) / "data"
    _csv(d / "respuestas" / "defectos.csv", ["fuente", "defecto", "registros", "regla_sugerida"], DEFECTOS)
    _csv(d / "respuestas" / "ventas-mes-canal.csv", ["mes", "canal", "lineas", "ventas", "comision"], VENTAS)
    _csv(d / "respuestas" / "produccion-mes-turno.csv", ["mes", "turno", "preparados", "vendidos", "merma"], PRODUCCION)
    _csv(d / "respuestas" / "precio-mes.csv", ["mes", "precio_medio", "dias_imputados"], PRECIO)
    _csv(d / "apoyo-catalogo-productos.csv", ["producto", "categoria", "precio_lista", "pollos_equivalentes", "kg_pollo_vivo", "costo_otros", "alias"],
         [("Pollo entero", "Pollo", 60.0, 1.0, 1.9, 6.0, "Pollo a la brasa|1 pollo")])
    _csv(d / "apoyo-costos-operativos.csv", ["mes", "planilla", "alquiler", "servicios", "otros", "total"], [("2026-01", 5000, 1500, 700, 300, 7500)])
    s = d / "salida"
    _csv(s / "dCalendario.csv", ["fecha_key", "fecha", "anio", "mes"], [(1, "2026-01-15", 2026, 1), (2, "2026-02-15", 2026, 2)])
    _csv(s / "dCanal.csv", ["canal_key", "canal"], [(1, "Salón"), (2, "Rappi")])
    _csv(s / "dTurno.csv", ["turno_key", "turno"], [(1, "Mañana")])
    filas = []
    for mes, canal, n, v, c in VENTAS:
        filas += [(int(mes[-1]), 1 if canal == "Salón" else 2, v / n, c / n, 1)] * n
    _csv(s / "fPedidos.csv", ["fecha_key", "canal_key", "venta_bruta", "comision", "registro_valido"], filas)
    _csv(s / "fProduccion.csv", ["fecha_key", "turno_key", "pollos_preparados", "pollos_vendidos", "pollos_merma"],
         [(int(m[-1]), 1, p, v, x) for m, _, p, v, x in PRODUCCION])
    precio = []
    for m, medio, imp in PRECIO:
        precio += [(int(m[-1]), medio - 0.5, imp), (int(m[-1]), medio + 0.5, 0)]
    _csv(s / "fPrecioInsumo.csv", ["fecha_key", "precio_kg", "valor_imputado"], precio)


def corrida(raiz, registrar=True):
    """Escribe la corrida de 08 con los ejemplos de sus plantillas y la registra."""
    run = Path(raiz) / "project" / "08-etl" / RUN
    for destino, plantilla in MODELOS.items():
        f = run / destino
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(ejemplo(COMMON / plantilla), encoding="utf-8")
    (run / "evidencia.json").write_text(ejemplo_json(COMMON / "etl-5-evidencia-json.md"), encoding="utf-8")
    (run / "README.md").write_text("# Procedencia\n\nModo de datos: generado.\n", encoding="utf-8")
    if registrar:
        P.register(PASO, RUN, root=raiz)
    return run


def crear(raiz):
    """Proyecto con 01 a 07, los datos y la corrida de 08; devuelve la carpeta de la corrida."""
    F.crear(Path(raiz), hasta="07-make-data-model-kpi")
    datos(raiz)
    return corrida(raiz)
