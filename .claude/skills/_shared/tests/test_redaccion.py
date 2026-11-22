"""Revisor de calidad de redacción (redaccion.py): cada rasgo se avisa y el texto cuidado queda sin avisos."""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import redaccion as R  # noqa: E402

BUENO = ("El margen neto de Pollería Don Tito cayó de 14 % a 8 % en 2026, aunque las ventas crecieron 18 % en el mismo año. "
         "Las aplicaciones cobran entre 25 % y 30 % de comisión (MIDAGRI, 2026). La gerencia fijaba el mismo precio en todos los canales sin descontar esa comisión ni el costo del insumo. "
         "Con el modelo, cada canal muestra su margen. Eso permite ajustar combos. "
         "La merma es de 7 %, frente a un 3 % de referencia en el rubro, y el objetivo OE-03 busca reducirla turno por turno con el pronóstico de demanda. Se revisa a diario.")


def tipos(txt, **kw):
    return {a["tipo"] for a in R.revisar(txt, **kw)}


class TestRevisor(unittest.TestCase):
    def test_texto_cuidado_sin_avisos(self):
        self.assertEqual(R.revisar(BUENO), [])

    def test_relleno_e_inflado(self):
        t = tipos("Es importante destacar que el sistema es robusto y fundamental para 2026 y el margen de 8 %.")
        self.assertIn("relleno", t)
        self.assertIn("inflado", t)

    def test_gerundio_y_contraste(self):
        self.assertIn("gerundio", tipos("El modelo une las fuentes de 2026, permitiendo así optimizar las decisiones."))
        self.assertIn("contraste", tipos("No solo mide el margen de 8 %, sino que también guía la producción."))

    def test_frase_larga(self):
        self.assertIn("frase-larga", tipos(" ".join(["palabra"] * 60) + ". Fin de 2026."))
        self.assertNotIn("frase-larga", tipos(" ".join(["palabra"] * 60) + ".", max_frase=80))

    def test_arranque_repetido(self):
        self.assertIn("arranque-repetido", tipos("El margen cayó 8 %. El costo subió 5 %. El precio no cambió 3 %."))

    def test_parrafo_sin_dato(self):
        self.assertIn("sin-dato", tipos("La empresa quiere mejorar sus decisiones " + "con mejor información disponible " * 8 + "para el negocio."))

    def test_cifra_codigo_o_cita_cuentan_como_dato(self):
        base = "La empresa quiere mejorar sus decisiones " + "con mejor información disponible " * 8
        self.assertNotIn("sin-dato", tipos(base + "según OE-02."))
        self.assertNotIn("sin-dato", tipos(base + "(Kimball & Ross, 2013)."))

    def test_ritmo_uniforme(self):
        t = " ".join("La caja registra la venta del día de hoy." for _ in range(10))
        self.assertIn("ritmo", tipos(t))

    def test_sigla_sin_definir_y_definida(self):
        self.assertIn("sigla", tipos("El módulo XYZ calcula el margen de 8 % en 2026."))
        self.assertNotIn("sigla", tipos("El Módulo de Cálculo (XYZ) calcula el margen de 8 %. El XYZ corre a diario."))
        self.assertNotIn("sigla", tipos("El proceso ETL de la caja carga 8 % más datos."))

    def test_se_ignoran_tablas_codigo_encabezados_y_marcas(self):
        t = ("## 2.1. Es importante destacar\n\n| Es importante destacar | robusto |\n|---|---|\n| fundamental | integral |\n\n```\nEs importante destacar\n```\n\n"
             "<!-- figura: foda -->\n\n(INCLUIR IMAGEN: Figura 1: Matriz FODA. Archivo sugerido: imagenes/foda.html)\n\nTabla 1: Es fundamental\n")
        self.assertEqual(R.revisar(t), [])

    def test_cli(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_text("Es importante destacar que el margen es de 8 % en 2026.\n", encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(R.main(["revisar", str(f)]), 0)
            self.assertIn("relleno", buf.getvalue())
            self.assertIn("1 aviso(s), 1 bloqueante(s)", buf.getvalue())
            self.assertIn("R-01 relleno · bloqueante", buf.getvalue())
            with redirect_stdout(io.StringIO()):
                self.assertEqual(R.main(["revisar", str(f), "--estricto"]), 1)
            g = Path(d) / "y.md"
            g.write_text(" ".join(["palabra"] * 60) + ". Fin de 2026.\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(R.main(["revisar", str(g), "--estricto"]), 0)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(R.main(["revisar", str(Path(d) / "no.md")]), 2)


class TestReglas(unittest.TestCase):
    def test_cada_tipo_tiene_su_regla_documentada(self):
        guia = (HERE.parents[2] / "common" / "redaccion" / "guia.md").read_text(encoding="utf-8")
        for tipo, (regla, bloq) in R.REGLAS.items():
            self.assertRegex(guia, rf"\| {regla} \| `{tipo}` \| {'Bloqueante' if bloq else 'Recomendada'} \|", tipo)


class TestAgente(unittest.TestCase):
    REPO = HERE.parents[2]

    def test_el_agente_es_solo_lectura_y_lee_la_guia(self):
        txt = (self.REPO / ".claude" / "agents" / "revisor-redactor.md").read_text(encoding="utf-8")
        import re
        m = re.match(r"---\nname: revisor-redactor\ndescription: (.+)\ntools: (.+)\n---\n", txt)
        self.assertIsNotNone(m)
        herramientas = {x.strip() for x in m.group(2).split(",")}
        self.assertTrue(herramientas.isdisjoint({"Write", "Edit", "NotebookEdit", "Agent"}), herramientas)
        self.assertIn("common/redaccion/guia.md", txt)
        self.assertIn("redaccion.py revisar", txt)

    def test_las_skills_que_escriben_secciones_invocan_al_agente(self):
        for s in ("03-make-business-diagnosis", "04-make-strategic-analysis", "05-make-problem-objectives", "06-make-bi-solution", "07-make-data-model-kpi"):
            for nombre in (s, s + "-update"):
                t = (self.REPO / ".claude" / "skills" / nombre / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("revisor-redactor", t, nombre)
                self.assertIn("common/redaccion/guia.md", t, nombre)

    def test_las_reglas_de_la_guia_estan_completas(self):
        guia = (self.REPO / "common" / "redaccion" / "guia.md").read_text(encoding="utf-8")
        import re
        self.assertEqual(sorted(set(re.findall(r"\| (R-\d\d) \|", guia))), [f"R-{i:02d}" for i in range(1, 18)])
        self.assertEqual(sorted(set(re.findall(r"\| (I-\d) \|", guia))), [f"I-{i}" for i in range(1, 8)])


if __name__ == "__main__":
    unittest.main()
