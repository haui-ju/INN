"""Visuales de los capítulos 1 y 2 (bmc, pestel, foda, ishikawa, arquitectura-bi, modelo-datos): registro, extracción por corrida, explicación y construcción."""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagnostico_fixtures as F  # noqa: E402
import html_tpl as H  # noqa: E402
import visuales as VI  # noqa: E402

COMUN = HERE.parents[2] / "common" / "html"
CAP1 = ["arquitectura-bi", "bmc", "foda", "ishikawa", "modelo-datos", "pestel"]


class TestRegistro(unittest.TestCase):
    def test_registros_completos_y_coherentes(self):
        for reg in (VI.VISUALES, VI.EXTRACTORES, VI.EXPLICACION, VI.PROPOSITOS, VI.TITULOS, VI.ORIGEN):
            self.assertEqual(sorted(reg), CAP1)
        self.assertEqual(VI.PLANTILLAS, CAP1)
        for v, (plantilla, paso, carpeta) in VI.VISUALES.items():
            self.assertTrue((COMUN / plantilla / "index.html").is_file(), v)
            self.assertEqual(carpeta, paso.replace("-make-", "-", 1))
            self.assertEqual(VI.ORIGEN[v][0], paso)

    def test_origen(self):
        self.assertEqual(VI.origen("ishikawa"), ("04-make-strategic-analysis", "secciones/1.7.md", "04-make-strategic-analysis-update"))
        self.assertEqual(VI.origen("bmc")[0], "03-make-business-diagnosis")
        self.assertIsNone(VI.origen("gantt"))

    def test_los_propositos_son_una_frase_limpia(self):
        for v, t in VI.PROPOSITOS.items():
            self.assertEqual(VI._frases(t), 1, v)
            self.assertNotRegex(t.lower(), r"falso|inventad|simulad|ficticio")


class TestConProyecto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.runs = F.crear(cls.root, hasta="07-make-data-model-kpi")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_extraer_desde_la_vigente(self):
        b = VI.extraer("bmc", self.root)
        self.assertEqual(b["empresa"], "Pollería Don Tito")
        self.assertEqual([x["clave"] for x in b["bloques"]][:3], ["segmentos", "propuesta", "canales"])
        self.assertIn("Producción por turno", b["bloques"][6]["items"])
        p = VI.extraer("pestel", self.root)
        self.assertEqual([f["clave"] for f in p["factores"]], ["politico", "economico", "social", "tecnologico", "ecologico", "legal"])
        f = VI.extraer("foda", self.root)
        self.assertEqual(len(f["estrategias"]), 6)
        self.assertEqual(f["estrategias"][0]["combina"], ["FOR-01", "OPO-01"])
        i = VI.extraer("ishikawa", self.root)
        self.assertEqual(i["categorias"][0]["nombre"], "Método")
        self.assertFalse(i["efecto"].endswith("."))

    def test_los_datos_cumplen_el_esquema_del_mock(self):
        for v in CAP1:
            mock = json.loads((COMUN / v / "mock.json").read_text(encoding="utf-8"))
            self.assertEqual(set(VI.extraer(v, self.root)), set(mock), v)

    def test_extraer_de_una_corrida_indicada(self):
        run = self.runs["04-make-strategic-analysis"]
        nueva = run.parent / "20-11-2026-09-00-00"
        (nueva / "secciones").mkdir(parents=True)
        for p in ("1.5", "1.6", "1.7"):
            (nueva / "secciones" / f"{p}.md").write_text((run / "secciones" / f"{p}.md").read_text(encoding="utf-8"), encoding="utf-8")
        t = (nueva / "secciones" / "1.7.md").read_text(encoding="utf-8").replace("| CAU-08 |", "| CAU-09 |")
        (nueva / "secciones" / "1.7.md").write_text(t, encoding="utf-8")
        codigos = [c["codigo"] for cat in VI.extraer("ishikawa", self.root, run=nueva.name)["categorias"] for c in cat["causas"]]
        self.assertIn("CAU-09", codigos)
        codigos = [c["codigo"] for cat in VI.extraer("ishikawa", self.root)["categorias"] for c in cat["causas"]]
        self.assertIn("CAU-08", codigos)

    def test_sin_fuente(self):
        with self.assertRaises(VI.SinFuente):
            VI.extraer("bmc", self.root, run="01-01-2020-00-00-00")
        with tempfile.TemporaryDirectory() as t:
            F.base(t)
            with self.assertRaises(VI.SinFuente):
                VI.extraer("pestel", Path(t))
            self.assertTrue(all(m for m in VI.disponibles(Path(t)).values()))
        run = self.runs["04-make-strategic-analysis"]
        vacia = run.parent / "21-11-2026-09-00-00"
        (vacia / "secciones").mkdir(parents=True)
        for p in ("1.5", "1.6", "1.7"):
            (vacia / "secciones" / f"{p}.md").write_text(f"## {p}. X\n", encoding="utf-8")
        with self.assertRaises(VI.SinFuente) as e:
            VI.extraer("pestel", self.root, run=vacia.name)
        self.assertIn("secciones/1.5.md", str(e.exception))

    def test_explicaciones_validas(self):
        for v in CAP1:
            d = VI.extraer(v, self.root)
            txt = VI.leer_imagen(v, d)
            self.assertEqual(VI.validar_explicacion(txt, VI.resaltado(v, d)), [], v)
            self.assertIn(f"Figura X: {VI.TITULOS[v]}.", txt)
        txt = VI.leer_imagen("pestel", VI.extraer("pestel", self.root))
        self.assertIn("4 son oportunidades y 4 son amenazas", txt)

    def test_explicacion_con_datos_minimos(self):
        for v in CAP1:
            vacio = H.limpiar(json.loads((COMUN / v / "mock.json").read_text(encoding="utf-8")))
            dice, resalta = VI.EXPLICACION[v](vacio)
            self.assertTrue(dice.endswith("."), v)
            self.assertIsNone(resalta)

    def test_construir_en_la_corrida(self):
        run = self.runs["03-make-business-diagnosis"]
        for f in ("visuales/bmc.html", "visuales/bmc.json", "leer-imagen/bmc.md"):
            self.assertTrue((run / f).is_file(), f)
        html = (run / "visuales" / "bmc.html").read_text(encoding="utf-8")
        self.assertIn("Pollería Don Tito", html)
        self.assertEqual(json.loads((run / "visuales" / "bmc.json").read_text(encoding="utf-8")), VI.extraer("bmc", self.root))

    def test_cli(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(VI.main(["origen", "--visual", "foda"]), 0)
            self.assertEqual(VI.main(["disponibles", "--raiz", str(self.root)]), 0)
        self.assertIn("04-make-strategic-analysis · secciones/1.6.md", buf.getvalue())
        self.assertIn("ishikawa: disponible", buf.getvalue())
        with tempfile.TemporaryDirectory() as d:
            run = self.runs["04-make-strategic-analysis"].name
            with redirect_stdout(io.StringIO()):
                self.assertEqual(VI.main(["construir", "--visual", "pestel", "--run", run, "--carpeta", str(Path(d) / "visuales"), "--raiz", str(self.root)]), 0)
            self.assertTrue((Path(d) / "visuales" / "pestel.html").is_file())
            self.assertTrue((Path(d) / "leer-imagen" / "pestel.md").is_file())


if __name__ == "__main__":
    unittest.main()
