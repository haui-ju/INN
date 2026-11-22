import sys
import tempfile
import types
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import validate_run as V  # noqa: E402


class TestValidate(unittest.TestCase):
    """Validaciones genéricas sobre una corrida mínima en una carpeta numerada sin reglas propias."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.run = Path(self.tmp.name) / "99-sin-reglas" / "corrida"
        (self.run / "bloques").mkdir(parents=True)
        (self.run / "documento.md").write_text("# Documento\n\nVer [bloque](bloques/a.md). FOD-01 resume la fortaleza.\n", encoding="utf-8")
        (self.run / "bloques" / "a.md").write_text("# Bloque\n\n| Código | Ítem |\n|---|---|\n| FOD-01 | Marca conocida |\n", encoding="utf-8")
        (self.run / "README.md").write_text("# Procedencia\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def add(self, rel, text):
        with (self.run / rel).open("a", encoding="utf-8") as fh:
            fh.write(text)

    def test_corrida_limpia(self):
        self.assertEqual(V.validate(self.run), [])

    def test_enlace_roto(self):
        self.add("documento.md", "\n[x](bloques/no-existe.md)\n")
        self.assertIn(("documento.md", "enlace roto: bloques/no-existe.md"), V.validate(self.run))

    def test_termino_prohibido_y_readme_exento(self):
        self.add("documento.md", "\nson datos de prueba\n")
        self.add("README.md", "\nsimulación con fines de estudio, datos inventados\n")
        inc = V.validate(self.run)
        self.assertTrue(any(f == "documento.md" and "prueba" in m for f, m in inc))
        self.assertFalse(any(f == "README.md" for f, _ in inc))

    def test_fraccion_incoherente(self):
        self.add("documento.md", "\n9 de 8 casos y 3 de 8 casos (90%)\n")
        msgs = [m for f, m in V.validate(self.run) if f == "documento.md"]
        self.assertTrue(any("9 de 8" in m for m in msgs))
        self.assertTrue(any("3 de 8" in m and "90%" in m for m in msgs))

    def test_excepcion_falso_positivo(self):
        self.add("documento.md", "\nhubo un falso positivo\n")
        self.assertEqual(V.validate(self.run), [])

    def test_codigo_sin_definir(self):
        files = V.md_files(self.run)
        self.add("documento.md", "\nVer FOD-99.\n")
        inc = V.check_codes(self.run, V.md_files(self.run), ["FOD"])
        self.assertEqual([(f.name, m) for f, m in inc], [("documento.md", "código citado sin definir: FOD-99")])
        self.assertTrue(files)

    def test_modulo_de_reglas_por_carpeta_numerada(self):
        self.assertEqual(V.modulo_reglas("01-project-brief"), "project_brief")
        self.assertEqual(V.modulo_reglas("02-design-system"), "design_system")
        self.assertIsNone(V.modulo_reglas("99-sin-reglas"))

    def test_reglas_del_paso_se_aplican(self):
        run = Path(self.tmp.name) / "01-project-brief" / "corrida"
        run.mkdir(parents=True)
        (run / "README.md").write_text("# Procedencia\n", encoding="utf-8")
        self.assertIn(("brief.md", "falta el archivo"), V.validate(run))

    def test_cli(self):
        self.assertEqual(V.main([str(self.run)]), 0)
        self.assertEqual(V.main([str(self.run / "no-existe")]), 2)
        self.assertIsInstance(V, types.ModuleType)


if __name__ == "__main__":
    unittest.main()
