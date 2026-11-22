"""Limpieza de referencia (etl_referencia.py): sus puntos de control coinciden con la hoja de respuestas de datagen.py."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import datagen as G  # noqa: E402
import etl_referencia as ER  # noqa: E402


def leer(ruta):
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class TestPuntosDeControl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.raiz = Path(cls.tmp.name)
        cls.data = cls.raiz / "data"
        G.generar(G.parametros_base(), cls.data)
        cls.p = ER.puntos_de_control(cls.raiz)
        cls.res = cls.data / "respuestas"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_filas_por_fuente_coinciden(self):
        for f in leer(self.res / "filas-por-fuente.csv"):
            c = self.p["fuentes"][f["fuente"]]
            self.assertEqual((c["filas"], c["validas"]), (int(f["filas_brutas"]), int(f["filas_validas"])), f["fuente"])

    def test_cada_defecto_coincide_con_la_hoja(self):
        campos = {"duplicado": "duplicados", "registro_invalido": "invalidos", "formato_fecha": "formato_fecha", "nombre_producto": "nombre_producto",
                  "nulo": "nulo", "dia_sin_precio": "dias_sin_precio"}
        for f in leer(self.res / "defectos.csv"):
            self.assertEqual(self.p["fuentes"][f["fuente"]][campos[f["defecto"]]], int(f["registros"]), (f["fuente"], f["defecto"]))

    def test_pasos_de_pedidos_suman(self):
        x = self.p["pedidos"]
        self.assertEqual(x["filas"] - x["duplicados"], x["tras_duplicados"])
        self.assertEqual(x["tras_duplicados"] - x["invalidos"], x["validas"])
        self.assertEqual((x["sin_homologar"], x["colisiones_de_clave"]), (0, 0))
        self.assertEqual(x["turno_derivable"], x["tras_duplicados"])

    def test_ventas_mes_canal_coinciden(self):
        hoja = {f"{f['mes']}|{f['canal']}": (int(f["lineas"]), float(f["ventas"]), float(f["comision"])) for f in leer(self.res / "ventas-mes-canal.csv")}
        self.assertEqual(set(hoja), set(self.p["ventas_mes_canal"]))
        for k, (n, v, c) in self.p["ventas_mes_canal"].items():
            self.assertEqual(hoja[k][0], n, k)
            self.assertAlmostEqual(hoja[k][1], v, delta=0.05, msg=k)
            self.assertAlmostEqual(hoja[k][2], c, delta=0.05, msg=k)

    def test_costo_estimado_por_mes_coincide_con_el_margen_por_producto(self):
        hoja = {}
        for f in leer(self.res / "margen-canal-producto.csv"):
            hoja[f["mes"]] = hoja.get(f["mes"], 0.0) + float(f["costo_estimado"])
        for m, x in self.p["meses"].items():
            self.assertAlmostEqual(x["costo_estimado"], hoja[m], delta=0.5, msg=m)

    def test_tablas_del_modelo_y_precio(self):
        t = self.p["tablas"]
        self.assertEqual((t["dCalendario"], t["fPrecioInsumo"], t["dProducto"], t["dCanal"], t["dTurno"], t["dKpi"], t["fMetaKpi"]), (457, 457, 8, 5, 3, 7, 105))
        self.assertEqual(t["fProduccion"], self.p["fuentes"]["fue-05"]["validas"])
        pr = self.p["precio"]
        self.assertEqual((pr["filas"] + pr["imputados"], pr["precio_1_julio"], pr["precio_14_julio"]), (pr["dias"], 6.10, 6.90))
        self.assertEqual(sum(int(f["dias_imputados"]) for f in leer(self.res / "precio-mes.csv")), pr["imputados"])

    def test_el_margen_neto_de_cada_mes_sale_de_los_totales_de_la_guia(self):
        kpi = {f["mes"]: float(f["valor"]) for f in leer(self.res / "kpi-esperados.csv") if f["kpi"] == "KPI-03"}
        for m, x in self.p["meses"].items():
            neto = 100 * (x["ventas"] - x["comision"] - x["costo_estimado"] - x["costo_operativo"]) / x["ventas"]
            self.assertAlmostEqual(neto, kpi[m], delta=0.02, msg=m)

    def test_kpi_01_sale_de_filas_validas_entre_filas_leidas(self):
        x = self.p["pedidos"]
        total = [float(f["valor"]) for f in leer(self.res / "kpi-esperados.csv") if f["kpi"] == "KPI-01"]
        self.assertAlmostEqual(100 * x["validas"] / x["filas"], sum(total) / len(total), delta=0.3)


if __name__ == "__main__":
    unittest.main()
