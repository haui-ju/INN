"""Integración del cierre: corridas de 03 a 11 armadas en un informe completo, con sus cinco capítulos y los anexos A a D."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import conclusions_fixtures as CF  # noqa: E402
import dashboard_fixtures as DF  # noqa: E402
import etl_fixtures as EF  # noqa: E402
import projectcfg as P  # noqa: E402
import report as R  # noqa: E402
import storytelling_fixtures as SF  # noqa: E402
import validate_run as VR  # noqa: E402


class TestInformeCompleto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        run9, _ = DF.crear(cls.root)
        EF.datos(cls.root)
        EF.corrida(cls.root)
        SF.corrida(cls.root, run9)
        run11 = cls.root / "project" / "11-conclusions" / CF.RUN
        (run11 / "secciones").mkdir(parents=True)
        (run11 / "secciones" / "5.md").write_text(DF.F.ejemplo(CF.MODELOS / "cn-1-seccion-5.md"), encoding="utf-8")
        (run11 / "README.md").write_text("# Procedencia\n\nModo de datos: generado.\n", encoding="utf-8")
        P.register(CF.PASO, CF.RUN, root=cls.root)
        cls.informe = cls.root / "project" / "12-report" / "r1"
        cls.informe.mkdir(parents=True)
        cls.res = R.construir(cls.root, cls.informe)
        cls.txt = (cls.informe / "informe.md").read_text(encoding="utf-8")
        cls.falt = (cls.informe / "faltantes.md").read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_los_cinco_capitulos_estan_en_el_informe(self):
        for h in ("## 3.1. ", "## 3.2. ", "## 4. ", "## 5. "):
            self.assertIn(h, self.txt, h)
        for letra in "ABCD":
            self.assertIn(f"## Anexo {letra}: ", self.txt)

    def test_faltantes_ya_no_lista_nada_pendiente(self):
        secciones = self.falt.split("## Secciones")[1].split("## Anexos")[0]
        for p in ("| 3.1 |", "| 3.2 |", "| 4 |", "| 5 |"):
            self.assertNotIn(p, secciones, p)
        self.assertNotIn("falta ejecutar", self.falt)

    def test_las_capturas_de_la_seccion_4_se_numeran_aparte_de_las_de_3_2(self):
        capt = [l for l in self.txt.splitlines() if l.startswith("(INCLUIR IMAGEN:") and ".png" in l]
        self.assertGreaterEqual(len(capt), 8)
        numeros = [int(l.split("Figura ")[1].split(":")[0]) for l in capt]
        self.assertEqual(numeros, sorted(numeros))
        self.assertTrue(any("10-storytelling" in l for l in capt))
        self.assertTrue(any("09-dashboard" in l for l in capt))

    def test_sin_avisos_de_imagenes_y_el_informe_valida(self):
        self.assertFalse([a for a in self.res["avisos"] if "captura" in a or "(incluye imagen)" in a], self.res["avisos"])
        self.assertEqual(VR.validate(self.informe), [])


if __name__ == "__main__":
    unittest.main()
