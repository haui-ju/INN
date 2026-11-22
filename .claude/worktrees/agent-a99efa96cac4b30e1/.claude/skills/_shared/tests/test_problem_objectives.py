"""Validador del paso 05-make-problem-objectives (secciones 1.8 a 1.10) contra el brief y las corridas de 03 y 04."""
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

PASO = "05-make-problem-objectives"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.runs = F.crear(self.root)
        self.run = self.runs[PASO]

    def tearDown(self):
        self.tmp.cleanup()

    def msgs(self):
        return [f"{f}: {m}" for f, m in V.validate(self.run)]

    def edita(self, punto, a, b, run=None):
        f = (run or self.run) / "secciones" / f"{punto}.md"
        t = f.read_text(encoding="utf-8")
        assert a in t, a
        f.write_text(t.replace(a, b, 1), encoding="utf-8")

    def assertIncidencia(self, texto):
        m = self.msgs()
        self.assertTrue(any(texto in x for x in m), m)


class TestEjemplo(Base):
    def test_ejemplo_sin_incidencias(self):
        self.assertEqual(self.msgs(), [])

    def test_capitulo_1_completo(self):
        estado = {s["seccion"]: s["estado"] for s in P.secciones(self.root)}
        self.assertEqual([estado[f"1.{i}"] for i in range(1, 11)], ["disponible"] * 10)


class TestProblematica(Base):
    def test_causa_que_no_esta_en_el_ishikawa(self):
        self.edita("1.8", "| CAU-06 | Tres registros", "| CAU-09 | Tres registros")
        self.assertIncidencia("CAU-09: no está en el Ishikawa vigente")

    def test_texto_distinto_del_ishikawa(self):
        self.edita("1.8", "| CAU-02 | Producción por turno sin pronóstico de demanda |", "| CAU-02 | Producción a ojo |")
        self.assertIncidencia("CAU-02: el texto difiere del Ishikawa")

    def test_cantidad_de_causas_principales(self):
        t = (self.run / "secciones" / "1.8.md").read_text(encoding="utf-8")
        for c in ("CAU-02", "CAU-04", "CAU-06"):
            t = "\n".join(ln for ln in t.splitlines() if not ln.startswith(f"| {c} ")) + "\n"
        (self.run / "secciones" / "1.8.md").write_text(t, encoding="utf-8")
        self.assertIncidencia("hay 1 causas principales")

    def test_falta_el_enunciado(self):
        self.edita("1.8", "**Enunciado.**", "**Resumen.**")
        self.assertIncidencia("falta «**Enunciado.**»")


class TestObjetivos(Base):
    def test_objetivo_editado(self):
        self.edita("1.10", "| 5 de 5 canales |", "| 4 de 5 canales |")
        self.assertIncidencia("OE-02: «meta» difiere del brief")

    def test_objetivo_que_no_esta_en_el_brief(self):
        self.edita("1.10", "| OE-03 | Identificar", "| OE-04 | Identificar")
        m = self.msgs()
        self.assertTrue(any("falta OE-03" in x for x in m), m)
        self.assertTrue(any("OE-04 no está en el brief vigente" in x for x in m), m)

    def test_og_editado(self):
        self.edita("1.9", "| 3 decisiones documentadas |", "| 5 decisiones documentadas |")
        self.assertIncidencia("OG-01: «meta» difiere del brief")


class TestMatriz(Base):
    def test_causa_principal_sin_objetivo(self):
        self.edita("1.10", "| OE-02 | CAU-01, CAU-04 |", "| OE-02 | CAU-01 |")
        self.assertIncidencia("la causa principal CAU-04 no está articulada")

    def test_indicador_distinto(self):
        self.edita("1.10", "| Actividades clave; Estructura de costos | Porcentaje de merma por turno |", "| Actividades clave; Estructura de costos | Merma |")
        self.assertIncidencia("OE-03: el indicador debe ser el del brief")

    def test_codigo_inexistente_en_04(self):
        self.edita("1.10", "| DEB-03, DO-01 |", "| DEB-03, DO-05 |")
        self.assertIncidencia("OE-01: cita DO-05, que no está en la matriz FODA vigente")

    def test_bloque_del_canvas_desconocido(self):
        self.edita("1.10", "| Actividades clave; Canales |", "| Procesos; Canales |")
        self.assertIncidencia("«Procesos» no es un bloque del Canvas")

    def test_falta_fila_de_un_oe(self):
        t = (self.run / "secciones" / "1.10.md").read_text(encoding="utf-8")
        t = "\n".join(ln for ln in t.splitlines() if not ln.startswith("| OE-03 | CAU-")) + "\n"
        (self.run / "secciones" / "1.10.md").write_text(t, encoding="utf-8")
        self.assertIncidencia("la matriz no tiene la fila de OE-03")

    def test_pestel_vacio_sin_raya(self):
        self.edita("1.10", "| DEB-02, DO-02 | — |", "| DEB-02, DO-02 | |")
        self.assertIncidencia("OE-03: la columna PESTEL")

    def test_sin_corrida_de_04(self):
        cfg = P.load(self.root)
        cfg["pasos"]["04-make-strategic-analysis"]["run"] = None
        P.save(cfg, self.root)
        self.assertIncidencia("no se puede comprobar la matriz sin la corrida vigente de 04-make-strategic-analysis")

    def test_falta_una_seccion(self):
        (self.run / "secciones" / "1.9.md").unlink()
        self.assertIncidencia("secciones/1.9.md: falta el archivo")


if __name__ == "__main__":
    unittest.main()
