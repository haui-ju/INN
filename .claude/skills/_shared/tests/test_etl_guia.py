"""Guía de ETL a la medida (etl_guia.py): trae los puntos de control reales, los pasos, las reglas y las tablas del modelo."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import datagen as G  # noqa: E402
import diagnostico_fixtures as F  # noqa: E402
import etl_guia as EG  # noqa: E402
import etl_referencia as ER  # noqa: E402


class TestGuia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.raiz = Path(cls.tmp.name)
        F.crear(cls.raiz, hasta="07-make-data-model-kpi")
        params = G.parametros_base()
        G.generar(params, cls.raiz / "data")
        (cls.raiz / "data" / "parametros.json").write_text(json.dumps(params), encoding="utf-8")
        cls.pc = ER.puntos_de_control(cls.raiz)
        cls.ruta = EG.construir(cls.raiz, None, cls.raiz / "guia.md")
        cls.txt = cls.ruta.read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_trae_los_puntos_de_control_de_cada_paso(self):
        p, f = self.pc["pedidos"], self.pc["fuentes"]
        for v in (p["filas"], p["duplicados"], p["tras_duplicados"], p["invalidos"], p["validas"], f["fue-01"]["filas"], f["fue-03"]["formato_fecha_archivo"],
                  self.pc["telefonos_distintos"], self.pc["tablas"]["fProduccion"]):
            self.assertIn(EG.n(v), self.txt, v)
        self.assertIn(EG.s(self.pc["totales"]["ventas"]), self.txt)
        self.assertIn(EG.s(self.pc["efecto_ventas"]["duplicados"]), self.txt)

    def test_los_pasos_y_las_reglas_estan_completos(self):
        self.assertEqual(sorted(set(re.findall(r"^### (PAS-\d\d)\.", self.txt, flags=re.M)) | set(re.findall(r"^\| (PAS-\d\d) \|", self.txt, flags=re.M)))[0], "PAS-01")
        for i in range(1, 17):
            self.assertIn(f"PAS-{i:02d}", self.txt)
        for i in range(1, 8):
            self.assertIn(f"REG-{i:02d}", self.txt)

    def test_cada_regla_cubre_un_tipo_de_defecto_de_la_hoja(self):
        for d in G.TIPOS:
            self.assertIn(f"`{d}`", self.txt, d)

    def test_cada_fuente_trae_su_codigo_m_y_su_muestra(self):
        for archivo in ("fue-01-caja.csv", "fue-02-rappi.csv", "fue-03-pedidosya.csv", "fue-04-whatsapp.csv", "fue-05-produccion.csv", "fue-06-precios-pollo.csv"):
            self.assertIn(archivo, self.txt)
        self.assertGreaterEqual(self.txt.count("```m"), 20)
        self.assertIn("Number.FromText", self.txt)
        self.assertIn('"en-US"', self.txt)

    def test_el_codigo_m_no_tiene_campos_que_se_refieran_a_si_mismos(self):
        for bloque in re.findall(r"```m\n(.*?)```", self.txt, flags=re.S):
            for campo in re.findall(r"[\[ ,](\w+) = (\w+)[,\]]", bloque):
                self.assertNotEqual(campo[0], campo[1], f"{campo[0]} = {campo[0]} es circular en M")

    def test_las_tablas_del_modelo_y_las_relaciones_salen_de_modelo_json(self):
        modelo = json.loads(next((self.raiz / "project" / "07-data-model-kpi").glob("*/modelo.json")).read_text(encoding="utf-8"))
        for h in modelo["hechos"] + modelo["dimensiones"]:
            self.assertIn(f"`{h['nombre']}`", self.txt)
        for r in modelo["relaciones"]:
            self.assertIn(r["codigo"], self.txt)

    def test_declara_que_no_se_ejecuto_y_que_los_datos_son_generados(self):
        self.assertIn("No se ejecutó Power Query", self.txt)
        self.assertIn("generados para el proyecto", self.txt)

    def test_el_telefono_no_pasa_al_modelo(self):
        self.assertIn("Ley 29733", self.txt)
        self.assertIn("cliente_id", self.txt)

    def test_se_puede_regenerar_con_la_misma_salida(self):
        otra = EG.construir(self.raiz, None, self.raiz / "otra.md")
        self.assertEqual(otra.read_text(encoding="utf-8"), self.txt)


if __name__ == "__main__":
    unittest.main()
