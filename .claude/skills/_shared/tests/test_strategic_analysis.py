"""Validador del paso 04-make-strategic-analysis (secciones 1.5 a 1.7) sobre los ejemplos de sus plantillas."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagnostico_fixtures as F  # noqa: E402
import projectcfg as P  # noqa: E402
import validate_run as V  # noqa: E402

PASO = "04-make-strategic-analysis"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run = F.crear(self.root, hasta=PASO)[PASO]

    def tearDown(self):
        self.tmp.cleanup()

    def msgs(self):
        return [f"{f}: {m}" for f, m in V.validate(self.run)]

    def edita(self, punto, a, b):
        f = self.run / "secciones" / f"{punto}.md"
        t = f.read_text(encoding="utf-8")
        assert a in t, a
        f.write_text(t.replace(a, b, 1), encoding="utf-8")

    def assertIncidencia(self, texto):
        m = self.msgs()
        self.assertTrue(any(texto in x for x in m), m)


class TestEjemplo(Base):
    def test_ejemplo_sin_incidencias(self):
        self.assertEqual(self.msgs(), [])

    def test_tres_visuales_con_explicacion(self):
        for v in ("pestel", "foda", "ishikawa"):
            self.assertTrue((self.run / "visuales" / f"{v}.html").is_file(), v)
            self.assertTrue((self.run / "leer-imagen" / f"{v}.md").is_file(), v)

    def test_registro_marca_las_secciones(self):
        estado = {s["seccion"]: s["estado"] for s in P.secciones(self.root)}
        self.assertEqual([estado[p] for p in ("1.5", "1.6", "1.7")], ["disponible"] * 3)


class TestPestel(Base):
    def test_factor_sin_hallazgo(self):
        self.edita("1.5", "| AMB-01 | Ecológico | La Ley 30884 regula el plástico de un solo uso y los envases descartables | Sube el costo de los envases para llevar y delivery | Amenaza | Congreso de la República del Perú (2018) |\n", "")
        self.edita("1.6", "AMB-01, LEG-01", "LEG-01")
        self.assertIncidencia("factor Ecológico")

    def test_hallazgo_sin_fuente(self):
        self.edita("1.5", "| Oportunidad | Microsoft (2026) |", "| Oportunidad | |")
        self.assertIncidencia("TEC-01: falta la fuente")

    def test_fuente_sin_anio(self):
        self.edita("1.5", "Contratos de la empresa con Rappi y PedidosYa, 2026", "Contratos de la empresa con Rappi y PedidosYa")
        self.assertIncidencia("TEC-02: la fuente debe llevar su año")

    def test_factor_que_no_coincide_con_el_codigo(self):
        self.edita("1.5", "| SOC-01 | Social |", "| SOC-01 | Económico |")
        self.assertIncidencia("SOC-01: el factor debe ser «Social»")

    def test_tipo_invalido(self):
        self.edita("1.5", "| Permite planificar precios y compras con menos incertidumbre | Oportunidad |", "| Permite planificar precios y compras con menos incertidumbre | Neutral |")
        self.assertIncidencia("ECO-02: el tipo debe ser Oportunidad o Amenaza")


class TestFoda(Base):
    def test_oportunidad_sin_respaldo(self):
        self.edita("1.6", "| OPO-02 | Más pedidos de delivery en el distrito | SOC-01 |", "| OPO-02 | Más pedidos de delivery en el distrito | Conversaciones con clientes |")
        self.assertIncidencia("OPO-02: la evidencia debe citar un hallazgo PESTEL")

    def test_cuadro_vacio(self):
        txt = (self.run / "secciones" / "1.6.md").read_text(encoding="utf-8")
        inicio = txt.index("| Código | Fortaleza |")
        fin = txt.index("| Código | Debilidad |")
        (self.run / "secciones" / "1.6.md").write_text(txt[:inicio] + txt[fin:], encoding="utf-8")
        self.assertIncidencia("Fortaleza")

    def test_estrategia_mal_combinada(self):
        self.edita("1.6", "| FO-01 | FO | Usar un dashboard de BI para identificar los canales y productos que más dejan y reforzar en ellos la marca | FOR-01, OPO-01 |",
                   "| FO-01 | FO | Usar un dashboard de BI para identificar los canales y productos que más dejan y reforzar en ellos la marca | DEB-01, OPO-01 |")
        self.assertIncidencia("FO-01: una estrategia FO combina fortalezas con oportunidades")

    def test_falta_un_tipo_de_estrategia(self):
        self.edita("1.6", "| DA-01 | DA | Monitorear el precio del pollo vivo y su efecto en el margen para ajustar precios y compras | DEB-01, AME-01 |\n", "")
        self.assertIncidencia("falta al menos una estrategia DA")

    def test_codigo_citado_sin_definir(self):
        self.edita("1.6", "| DEB-03, OPO-01 |", "| DEB-03, OPO-07 |")
        m = self.msgs()
        self.assertTrue(any("código citado sin definir: OPO-07" in x for x in m), m)
        self.assertTrue(any("combina OPO-07, que no está en la matriz FODA" in x for x in m), m)


class TestIshikawa(Base):
    def test_efecto_distinto_del_brief(self):
        self.edita("1.7", "**Efecto.** Las ventas crecieron 18 %", "**Efecto.** Las ventas subieron 18 %")
        self.assertIncidencia("el efecto no coincide con el problema principal del brief")

    def test_categoria_desconocida(self):
        self.edita("1.7", "| CAU-03 | Mano de obra |", "| CAU-03 | Personas |")
        self.assertIncidencia("CAU-03: categoría «Personas» desconocida")

    def test_pocas_causas_y_categorias(self):
        t = (self.run / "secciones" / "1.7.md").read_text(encoding="utf-8")
        filas = [ln for ln in t.splitlines() if ln.startswith("| CAU-0") and ("Método" not in ln)]
        for ln in filas:
            t = t.replace(ln + "\n", "")
        (self.run / "secciones" / "1.7.md").write_text(t, encoding="utf-8")
        m = self.msgs()
        self.assertTrue(any("al menos 6" in x for x in m), m)
        self.assertTrue(any("al menos 4 de las 6M" in x for x in m), m)

    def test_causa_sin_evidencia(self):
        self.edita("1.7", "| Observación en caja, 2026 |", "| |")
        self.assertIncidencia("CAU-03: falta la evidencia")

    def test_sin_figura(self):
        (self.run / "visuales" / "ishikawa.html").unlink()
        self.assertIncidencia("visuales/ishikawa.html")


class TestUnaFiguraPorSeccion(Base):
    def test_cada_seccion_marca_una_sola_figura(self):
        self.assertEqual(self.msgs(), [])
        self.edita("1.6", "<!-- figura: foda -->", "<!-- figura: foda -->\n\n<!-- figura: foda -->")
        self.assertIncidencia("debe marcar una sola vez la figura con la línea «<!-- figura: foda -->»")


if __name__ == "__main__":
    unittest.main()
