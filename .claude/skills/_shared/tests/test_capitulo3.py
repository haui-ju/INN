"""Integración del capítulo 3: corridas de 03 a 09 armadas en un informe con 3.1, 3.2, las capturas y los anexos A a D."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dashboard_fixtures as DF  # noqa: E402
import etl_fixtures as EF  # noqa: E402
import report as R  # noqa: E402
import validate_run as VR  # noqa: E402


class TestInformeConCapitulo3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        DF.crear(cls.root)
        EF.datos(cls.root)
        EF.corrida(cls.root)
        cls.informe = cls.root / "project" / "12-report" / "r1"
        cls.informe.mkdir(parents=True)
        cls.res = R.construir(cls.root, cls.informe)
        cls.txt = (cls.informe / "informe.md").read_text(encoding="utf-8")
        cls.falt = (cls.informe / "faltantes.md").read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_secciones_3_1_y_3_2_entran_al_informe(self):
        self.assertIn("## 3.1. ", self.txt)
        self.assertIn("## 3.2. ", self.txt)
        self.assertNotIn("<!-- captura", self.txt)

    def test_las_capturas_se_numeran_despues_de_las_figuras_y_enlazan_a_su_corrida(self):
        for n, pag in zip(range(7, 11), range(1, 5)):
            self.assertRegex(self.txt, rf"\(INCLUIR IMAGEN: Figura {n}: .*Archivo sugerido: \.\./\.\./09-dashboard/[^)]*capturas/pag-0{pag}\.png\)")
        self.assertEqual(list(self.informe.rglob("*.png")), [])

    def test_los_cuatro_anexos_entran(self):
        for letra in "ABCD":
            self.assertIn(f"## Anexo {letra}: ", self.txt)
            self.assertTrue((self.informe / "anexos" / f"anexo-{letra.lower()}.md").is_file(), letra)

    def test_faltantes_solo_lista_los_capitulos_4_y_5(self):
        secciones = self.falt.split("## Anexos")[0]
        self.assertIn("| 4 |", secciones)
        self.assertIn("| 5 |", secciones)
        self.assertNotIn("| 3.1 |", secciones)
        self.assertNotIn("| 3.2 |", secciones)
        self.assertNotIn("08-make-etl | la sección", self.falt)
        self.assertNotIn("09-make-dashboard | la sección", self.falt)

    def test_el_armado_no_avisa_de_capturas_ni_de_imagenes_faltantes(self):
        self.assertFalse([a for a in self.res["avisos"] if "captura" in a or "(incluye imagen)" in a], self.res["avisos"])

    def test_el_informe_valida(self):
        self.assertEqual(VR.validate(self.informe), [])


if __name__ == "__main__":
    unittest.main()
