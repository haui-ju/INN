"""Kit común del capítulo 1 (diagnostico.py): títulos del índice, lectura de las secciones y comprobaciones comunes."""
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
import diagnostico as D  # noqa: E402
import diagnostico_fixtures as F  # noqa: E402


class TestIndice(unittest.TestCase):
    def test_titulos_sin_parentesis(self):
        t = D.titulos()
        self.assertEqual(t["1.1"], "Nombre de la empresa")
        self.assertEqual(t["1.4"], "Modelo de negocio: Business Model Canvas")
        self.assertEqual(t["1.6"], "Matriz FODA")
        self.assertEqual(t["1.7"], "Diagrama de la problemática: Ishikawa")
        self.assertEqual(t["1.10"], "Objetivos específicos")
        self.assertEqual(D.encabezado("1.5"), "## 1.5. Análisis PESTEL")

    def test_puntos_de_cada_paso(self):
        self.assertEqual(D.puntos_de(D.NEGOCIO), ["1.1", "1.2", "1.3", "1.4"])
        self.assertEqual(D.puntos_de(D.ESTRATEGICO), ["1.5", "1.6", "1.7"])
        self.assertEqual(D.puntos_de(D.PROBLEMA), ["1.8", "1.9", "1.10"])
        self.assertEqual(set(D.FIGURAS), {"1.4", "1.5", "1.6", "1.7"})


class TestUtilidades(unittest.TestCase):
    def test_numero(self):
        self.assertEqual(D.numero("S/ 2 400 000 (2025)"), 2400000)
        self.assertEqual(D.numero("S/ 5 500 (2026)"), 5500)
        self.assertEqual(D.numero("436,4"), 436.4)
        self.assertEqual(D.numero("2,400,000"), 2400000)
        self.assertEqual(D.numero("2.400.000"), 2400000)
        self.assertIsNone(D.numero("Pendiente"))

    def test_citas(self):
        c = D.citas("Texto (Osterwalder & Pigneur, 2010). Según MIDAGRI (2026) y Congreso de la República del Perú (2013).")
        self.assertIn(("Osterwalder & Pigneur", "2010"), c)
        self.assertIn(("MIDAGRI", "2026"), c)
        self.assertEqual(D._token("Osterwalder & Pigneur"), "Osterwalder")
        self.assertEqual(D.citas("Entrega (30-11-2026) y S/ 5 500 (2026)"), [])

    def test_norm_quita_marcador(self):
        self.assertEqual(D.norm("Texto. (modelado por el agente, por no contar con X)"), "texto")


class TestLectura(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.runs = F.crear(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_negocio(self):
        d = D.leer(self.root, D.NEGOCIO)
        self.assertEqual(d["empresa"]["Nombre comercial"], "Pollería Don Tito")
        self.assertTrue(d["mision"].startswith("Servir el mejor pollo"))
        self.assertEqual(len(d["canvas"]), 9)
        self.assertEqual(d["canvas"][2]["bloque"], "Canales")
        self.assertIn("Rappi", d["canvas"][2]["items"])
        self.assertEqual(d["tamano"]["Categoría (Ley 30056)"], "Pequeña empresa")

    def test_estrategico(self):
        d = D.leer(self.root, D.ESTRATEGICO)
        self.assertEqual(len(d["pestel"]), 8)
        self.assertEqual([i["codigo"] for i in d["foda"]["amenazas"]], ["AME-01", "AME-02", "AME-03", "AME-04"])
        self.assertEqual(d["estrategias"][0]["combina"], ["FOR-01", "OPO-01"])
        self.assertEqual(len(d["causas"]), 8)
        self.assertTrue(d["efecto"].startswith("Las ventas crecieron 18 %"))

    def test_problema(self):
        d = D.leer(self.root, D.PROBLEMA)
        self.assertEqual([p["codigo"] for p in d["principales"]], ["CAU-01", "CAU-02", "CAU-04", "CAU-06"])
        self.assertEqual([o["codigo"] for o in d["oe"]], ["OE-01", "OE-02", "OE-03"])
        self.assertEqual(d["matriz"][1]["foda"], ["DEB-01", "AME-02", "FA-01", "DA-01"])
        self.assertEqual(d["matriz"][2]["pestel"], [])
        self.assertEqual(d["matriz"][0]["canvas"], ["Actividades clave", "Canales"])

    def test_corrida_inexistente(self):
        with self.assertRaises(D.SinCorrida):
            D.corrida(self.root, D.NEGOCIO, "01-01-2020-00-00-00")

    def test_dominio_sin_marcadores(self):
        dom = D.dominio(self.root)
        self.assertEqual(dom["datos"]["Nombre comercial"], "Pollería Don Tito")
        self.assertNotIn("modelado", dom["secciones"]["Misión"])

    def test_cli(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(D.main(["leer", "--paso", D.ESTRATEGICO, "--raiz", str(self.root)]), 0)
        self.assertEqual(json.loads(buf.getvalue())["causas"][0]["codigo"], "CAU-01")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(D.main(["titulos"]), 0)
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(D.main(["leer", "--paso", D.NEGOCIO, "--raiz", t]), 1)


class TestComprobaciones(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run = F.crear(self.root, hasta=D.NEGOCIO)[D.NEGOCIO]

    def tearDown(self):
        self.tmp.cleanup()

    def edita(self, punto, a, b):
        f = self.run / "secciones" / f"{punto}.md"
        t = f.read_text(encoding="utf-8")
        assert a in t, a
        f.write_text(t.replace(a, b, 1), encoding="utf-8")

    def test_ejemplo_sin_incidencias(self):
        self.assertEqual(D.check_comunes(self.run, D.puntos_de(D.NEGOCIO)), [])

    def test_encabezado_distinto(self):
        self.edita("1.3", "## 1.3. Industria y tamaño", "## 1.3. Industria")
        inc = D.check_encabezados(self.run, ["1.3"])
        self.assertTrue(any("## 1.3. Industria y tamaño" in m for _, m in inc))

    def test_falta_seccion(self):
        (self.run / "secciones" / "1.2.md").unlink()
        self.assertTrue(D.faltan_secciones(D.check_comunes(self.run, ["1.2"])))

    def test_figura_sin_visual(self):
        (self.run / "visuales" / "bmc.html").unlink()
        (self.run / "leer-imagen" / "bmc.md").unlink()
        inc = D.check_figuras(self.run, ["1.4"])
        self.assertEqual({f for f, _ in inc}, {"visuales/bmc.html", "leer-imagen/bmc.md"})

    def test_figura_ausente_o_en_seccion_sin_imagen(self):
        self.edita("1.4", "<!-- figura: bmc -->", "")
        self.edita("1.1", "**Reseña.**", "<!-- figura: bmc -->\n\n**Reseña.**")
        msgs = [m for _, m in D.check_figuras(self.run, ["1.1", "1.4"])]
        self.assertTrue(any("una sola vez" in m for m in msgs))
        self.assertTrue(any("no lleva imagen" in m for m in msgs))

    def test_nota_de_trabajo(self):
        self.edita("1.2", "**Valores.**", "<!-- revisar con el equipo -->\n\n**Valores.**")
        self.assertTrue(any("comentario" in m for _, m in D.check_figuras(self.run, ["1.2"])))

    def test_marcador_copiado(self):
        self.edita("1.2", "precios justos para", "precios justos (modelado por el agente, por no contar con X) para")
        self.assertTrue(D.check_marcador(self.run, ["1.2"]))

    def test_cita_sin_referencia(self):
        (self.run / "referencias.md").write_text("Osterwalder, A., & Pigneur, Y. (2010). Business model generation.\n", encoding="utf-8")
        msgs = [m for _, m in D.check_citas(self.run, D.puntos_de(D.NEGOCIO))]
        self.assertTrue(any("Congreso de la República del Perú, 2013" in m for m in msgs))

    def test_referencia_sin_anio(self):
        (self.run / "referencias.md").write_text("Osterwalder, A. Business model generation.\n", encoding="utf-8")
        self.assertTrue(any("año" in m for _, m in D.check_citas(self.run, [])))


if __name__ == "__main__":
    unittest.main()
