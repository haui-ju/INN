"""Validador de la corrida del informe (rules/report.py, cargado por validate_run.py para la carpeta 12-report)."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import report as R  # noqa: E402
import report_fixtures as RF  # noqa: E402
import validate_run as V  # noqa: E402
from rules import report as RR  # noqa: E402


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.prev = os.environ.get("PROJECT_ROOT")
        os.environ["PROJECT_ROOT"] = str(self.root)
        RF.crear(self.root)
        self.run = self.root / "project" / R.CARPETA / "21-11-2026-12-00-00"
        R.construir(self.root, self.run, curso="Inteligencia de Negocios", docente="Ana Pérez")
        R.render(self.run / R.INFORME, self.root)
        self.inf = self.run / R.INFORME

    def tearDown(self):
        if self.prev is None:
            os.environ.pop("PROJECT_ROOT", None)
        else:
            os.environ["PROJECT_ROOT"] = self.prev
        self.tmp.cleanup()

    def cambiar(self, viejo, nuevo, archivo=None):
        f = archivo or self.inf
        t = f.read_text(encoding="utf-8")
        self.assertIn(viejo, t)
        f.write_text(t.replace(viejo, nuevo, 1), encoding="utf-8")

    def mensajes(self):
        return [m for _, m in RR.validar(self.run)]

    def assertIncidencia(self, texto):
        ms = self.mensajes()
        self.assertTrue(any(texto in m for m in ms), f"no se informó «{texto}»: {ms}")


class TestCorridaLimpia(Base):
    def test_sin_incidencias(self):
        self.assertEqual(RR.validar(self.run), [])

    def test_validate_run_carga_las_reglas_por_la_carpeta(self):
        self.assertEqual(V.modulo_reglas(R.CARPETA), "report")
        self.assertEqual(V.validate(self.run), [])


class TestIncidencias(Base):
    def test_marca_de_figura_sin_reemplazar(self):
        self.cambiar("Las causas se agrupan", "<!-- figura: foda -->\n\nLas causas se agrupan")
        self.assertIncidencia("no se reemplazó")

    def test_figura_salteada(self):
        self.cambiar("(INCLUIR IMAGEN: Figura 2:", "(INCLUIR IMAGEN: Figura 7:")
        self.assertIncidencia("debe ser la 2")

    def test_sin_como_copiarla(self):
        self.cambiar("**Cómo copiarla.** Abrir [imagenes/foda.html]", "Abrir [imagenes/foda.html]")
        self.assertIncidencia("no lleva la línea «Cómo copiarla»")

    def test_html_de_figura_inexistente(self):
        (self.run / "imagenes" / "bmc.html").unlink()
        self.assertIncidencia("apunta a imagenes/bmc.html")

    def test_imagen_incrustada_y_archivo_de_imagen(self):
        self.cambiar("El lienzo resume", "![lienzo](lienzo.png)\n\nEl lienzo resume")
        (self.run / "lienzo.png").write_bytes(b"\x89PNG")
        self.assertIncidencia("no se incrustan")
        self.assertIncidencia("no incluye archivos de imagen")

    def test_seccion_en_informe_y_en_faltantes(self):
        self.cambiar("| 2.1 |", "| 1.1 |", self.run / "faltantes.md")
        self.assertIncidencia("la sección 1.1 está en el informe y en faltantes.md")
        self.assertIncidencia("la sección 2.1 no está en el informe ni en faltantes.md")

    def test_seccion_con_imagen_sin_marcador(self):
        t = self.inf.read_text(encoding="utf-8")
        ini = t.index("(INCLUIR IMAGEN: Figura 4:")
        fin = t.index("## 1.8.")
        self.inf.write_text(t[:ini] + t[fin:], encoding="utf-8")
        self.assertIncidencia("la sección 1.7 lleva la marca «(incluye imagen)»")

    def test_referencia_duplicada_y_desordenada(self):
        self.cambiar(RF.REF_ISHI + "\n", RF.REF_OSTER + "\n\n" + RF.REF_ISHI + "\n")
        self.assertIncidencia("está repetida")
        self.assertIncidencia("orden alfabético")

    def test_tabla_de_versiones(self):
        self.cambiar("## Control del documento\n", "## Control del documento\n\n| Versión | Fecha |\n|---|---|\n| v1 | 01-11-2026 |\n")
        self.assertIncidencia("una sola entrega")

    def test_dato_de_portada_ausente(self):
        self.cambiar("| Docente | Ana Pérez |\n", "")
        self.assertIncidencia("«Docente»")

    def test_titulo_y_orden_de_secciones(self):
        self.cambiar("## 1.2. Misión y visión", "## 1.2. Misión")
        self.assertIncidencia("debe titularse «Misión y visión»")
        t = self.inf.read_text(encoding="utf-8")
        a, b = t.index("## 1.9."), t.index("## 1.10.")
        c = t.index("# Referencias bibliográficas")
        self.inf.write_text(t[:a] + t[b:c] + t[a:b] + t[c:], encoding="utf-8")
        self.assertIncidencia("fuera del orden del índice")

    def test_tabla_salteada(self):
        self.cambiar("Tabla 2: Estrategias cruzadas", "Tabla 5: Estrategias cruzadas")
        self.assertIncidencia("la Tabla 5 debe ser la 2")

    def test_anexo_sin_su_archivo(self):
        self.cambiar("# Referencias bibliográficas", "# Anexos\n\n## Anexo A: Diccionario de datos y calidad de datos\n\nTexto.\n\n# Referencias bibliográficas")
        self.assertIncidencia("falta el archivo del Anexo A")
        self.assertIncidencia("el Anexo A está en el informe y en faltantes.md")

    def test_html_desactualizado(self):
        self.cambiar("## 1.2. Misión y visión", "## 1.2. Misión y visión\n\n### Valores\n\nRespeto.")
        self.assertIncidencia("los encabezados no coinciden")

    def test_html_de_imagen_fuera_del_indice(self):
        (self.run / "imagenes" / "extra.html").write_text("<!doctype html><title>x</title>", encoding="utf-8")
        self.assertIncidencia("no figura en imagenes/INDICE.md")

    def test_sin_faltantes_ni_readme(self):
        (self.run / "faltantes.md").unlink()
        (self.run / "README.md").unlink()
        self.assertIncidencia("falta el archivo")
        self.assertIn(("README.md", "falta el archivo (procedencia del informe)"), RR.validar(self.run))


if __name__ == "__main__":
    unittest.main()
