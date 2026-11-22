"""Conversión de Markdown a HTML estándar (doc_html.py) con la hoja de estilos del estándar visual."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import doc_html as DH  # noqa: E402
import html_tpl as H  # noqa: E402


class TestDocHtml(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name) / "anexos"
        self.d.mkdir()
        (self.d / "uno.md").write_text("# Uno\n\nVer [dos](dos.md).\n", encoding="utf-8")
        (self.d / "dos.md").write_text("# Dos\n\n| a | b |\n|---|---|\n| 1 | 2 |\n", encoding="utf-8")
        self.tk = H.cargar_tokens(".", "base")

    def tearDown(self):
        self.tmp.cleanup()

    def test_estilos_del_estandar_visual(self):
        self.assertIn("--", DH._estilos_visuales())
        self.assertTrue(any(f.is_file() for f in DH.ESTILOS_VISUALES))

    def test_construir_y_comprobar(self):
        hechos = DH.construir(self.d, self.d / "html", self.tk, "Anexos")
        self.assertEqual(hechos, ["dos.html", "index.html", "uno.html"])
        self.assertEqual(DH.comprobar(self.d, self.d / "html", self.tk, "Anexos"), [])
        self.assertIn('href="dos.html"', (self.d / "html" / "uno.html").read_text(encoding="utf-8"))

    def test_enlaces_a_otros_archivos_se_reubican(self):
        (self.d.parent / "imagenes").mkdir()
        (self.d.parent / "imagenes" / "foda.html").write_text("<!doctype html>", encoding="utf-8")
        (self.d / "tres.md").write_text("# Tres\n\nAbrir [foda](../imagenes/foda.html) y [uno](uno.md#uno).\n", encoding="utf-8")
        DH.construir(self.d, self.d / "html", self.tk, "Anexos")
        h = (self.d / "html" / "tres.html").read_text(encoding="utf-8")
        self.assertIn('href="../../imagenes/foda.html"', h)
        self.assertIn('href="uno.html#uno"', h)
        self.assertEqual(DH.comprobar(self.d, self.d / "html", self.tk, "Anexos"), [])

    def test_markdown_cambiado(self):
        DH.construir(self.d, self.d / "html", self.tk, "Anexos")
        (self.d / "dos.md").write_text("# Dos\n\nOtro texto.\n", encoding="utf-8")
        inc = DH.comprobar(self.d, self.d / "html", self.tk, "Anexos")
        self.assertIn(("dos.html", "no coincide con lo que se genera desde su Markdown"), inc)


class TestTemaPorDefecto(unittest.TestCase):
    def test_la_plantilla_lee_el_tema_defecto_de_los_tokens(self):
        t = (Path(__file__).resolve().parents[4] / "common" / "document-html" / "plantilla.html").read_text(encoding="utf-8")
        self.assertIn("--tema-defecto", t)
        self.assertIn("guardado === 'dark' || guardado === 'light' ? guardado : defecto", t)


if __name__ == "__main__":
    unittest.main()
