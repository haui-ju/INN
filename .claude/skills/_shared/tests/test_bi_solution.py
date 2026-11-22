"""Validador del paso 06-make-bi-solution (secciones 2.1 a 2.3) contra el brief y su figura arquitectura-bi."""
import filecmp
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagnostico as D  # noqa: E402
import diagnostico_fixtures as F  # noqa: E402
import html_tpl as H  # noqa: E402
import projectcfg as P  # noqa: E402
import runs as R  # noqa: E402
import validate_run as V  # noqa: E402
import visuales as VI  # noqa: E402

PASO = "06-make-bi-solution"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.runs = F.crear(self.root, hasta=PASO)
        self.run = self.runs[PASO]

    def tearDown(self):
        self.tmp.cleanup()

    def msgs(self, run=None):
        return [f"{f}: {m}" for f, m in V.validate(run or self.run)]

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

    def test_secciones_disponibles_y_figura(self):
        estado = {s["seccion"]: s["estado"] for s in P.secciones(self.root)}
        self.assertEqual([estado[f"2.{i}"] for i in (1, 2, 3)], ["disponible"] * 3)
        self.assertEqual(estado["2.4"], "pendiente")
        for f in ("visuales/arquitectura-bi.html", "visuales/arquitectura-bi.json", "leer-imagen/arquitectura-bi.md"):
            self.assertTrue((self.run / f).is_file(), f)

    def test_encabezados_exactos(self):
        self.assertEqual(D.encabezado("2.2"), "## 2.2. Arquitectura de Inteligencia de Negocios")
        self.edita("2.3", "## 2.3. Herramientas utilizadas", "## 2.3. Herramientas")
        self.assertIncidencia("la primera línea debe ser «## 2.3. Herramientas utilizadas»")

    def test_check_avisa_si_falta_el_capitulo_1(self):
        (self.root / ".claude" / "skills" / "05-make-problem-objectives").mkdir(parents=True)
        self.assertEqual(P.check(PASO, self.root), [])
        cfg = P.load(self.root)
        cfg["pasos"]["05-make-problem-objectives"]["run"] = None
        P.save(cfg, self.root)
        self.assertTrue(any("05-make-problem-objectives" in a for a in P.check(PASO, self.root)), P.check(PASO, self.root))


class TestPlaybook(unittest.TestCase):
    COMMON = HERE.parents[2] / "common" / "06-bi-solution"

    def test_guia_y_plantillas_con_las_cinco_partes(self):
        self.assertTrue((self.COMMON / "guia.md").is_file())
        plantillas = sorted(p for p in (self.COMMON / "models").glob("bs-*.md"))
        self.assertEqual([p.name for p in plantillas], ["bs-1-propuesta.md", "bs-2-arquitectura.md", "bs-3-herramientas.md"])
        self.assertTrue((self.COMMON / "models" / "README.md").is_file())
        for p in plantillas:
            t = p.read_text(encoding="utf-8")
            self.assertIn("| **Entregable** |", t, p.name)
            for parte in ("## Instrucciones para el agente", "## Formato", "## Ejemplo", "## Checklist"):
                self.assertIn(parte, t, f"{p.name}: {parte}")
            self.assertGreaterEqual(t.count("```markdown"), 2, p.name)


class TestPropuesta(Base):
    def test_objetivo_sin_fila(self):
        t = (self.run / "secciones" / "2.1.md").read_text(encoding="utf-8")
        t = "\n".join(ln for ln in t.splitlines() if not ln.startswith("| OE-03 ")) + "\n"
        (self.run / "secciones" / "2.1.md").write_text(t, encoding="utf-8")
        self.assertIncidencia("OE-03: el objetivo no aparece en la tabla de la propuesta")

    def test_objetivo_que_no_es_del_brief(self):
        self.edita("2.1", "| OE-03 | CAP-05", "| OE-09 | CAP-05")
        m = self.msgs()
        self.assertTrue(any("OE-09 no es un objetivo específico del brief" in x for x in m), m)
        self.assertTrue(any("OE-03: el objetivo no aparece" in x for x in m), m)

    def test_componente_inexistente(self):
        self.edita("2.1", "| OE-01 | CAP-04, CAP-05 |", "| OE-01 | CAP-04, CAP-09 |")
        self.assertIncidencia("OE-01: cita CAP-09, que no está en la tabla de 2.2")

    def test_fila_sin_componentes(self):
        self.edita("2.1", "| OE-01 | CAP-04, CAP-05 |", "| OE-01 | |")
        self.assertIncidencia("OE-01: la fila no cita ningún componente")

    def test_faltan_decisiones_usuarios_y_respuesta(self):
        self.edita("2.1", "**Decisiones que apoya.**", "**Decisiones.**")
        self.edita("2.1", "**Usuarios.**", "**Quiénes.**")
        self.edita("2.1", "**Respuesta a la problemática.**", "**Respuesta.**")
        for x in ("falta «**Decisiones que apoya.**»", "falta «**Usuarios.**»", "falta «**Respuesta a la problemática.**»"):
            self.assertIncidencia(x)


class TestArquitectura(Base):
    def test_capa_ausente(self):
        t = (self.run / "secciones" / "2.2.md").read_text(encoding="utf-8")
        t = "\n".join(ln for ln in t.splitlines() if not ln.startswith("| CAP-05 ")) + "\n"
        (self.run / "secciones" / "2.2.md").write_text(t, encoding="utf-8")
        self.assertIncidencia("falta la capa de almacenamiento")

    def test_capas_fuera_de_orden(self):
        self.edita("2.2", "| CAP-04 | ETL |", "| CAP-04 | Almacenamiento |")
        self.edita("2.2", "| CAP-05 | Almacenamiento |", "| CAP-05 | ETL |")
        self.assertIncidencia("las capas deben ir en el orden Fuentes, ETL, Almacenamiento, Visualización")

    def test_capa_desconocida(self):
        self.edita("2.2", "| CAP-06 | Visualización |", "| CAP-06 | Presentación |")
        self.assertIncidencia("CAP-06: la capa «Presentación» no es una de")

    def test_fuente_del_brief_no_usada(self):
        self.edita("2.2", "Precios del pollo vivo en Lima Metropolitana (FUE-03)", "Precios del pollo vivo en Lima Metropolitana")
        self.assertIncidencia("FUE-03: la fuente del brief no figura en la capa de fuentes")

    def test_fuente_que_no_es_del_brief(self):
        self.edita("2.2", "Sistema de caja de los locales (FUE-01)", "Sistema de caja de los locales (FUE-07)")
        m = self.msgs()
        self.assertTrue(any("FUE-01: la fuente del brief no figura" in x for x in m), m)
        self.assertTrue(any("cita FUE-07, que no es una fuente del brief" in x for x in m), m)

    def test_marca_de_figura_obligatoria(self):
        self.edita("2.2", "<!-- figura: arquitectura-bi -->", "")
        self.assertIncidencia("debe marcar una sola vez la figura con la línea «<!-- figura: arquitectura-bi -->»")

    def test_figura_sin_construir(self):
        (self.run / "visuales" / "arquitectura-bi.html").unlink()
        self.assertIncidencia("falta el visual de la figura")

    def test_figura_en_una_seccion_sin_imagen(self):
        self.edita("2.3", "## 2.3. Herramientas utilizadas", "## 2.3. Herramientas utilizadas\n\n<!-- figura: arquitectura-bi -->")
        self.assertIncidencia("la sección 2.3 no lleva imagen")

    def test_codigo_cap_citado_sin_definir(self):
        self.edita("2.2", "**Lectura de la arquitectura.** El dato", "**Lectura de la arquitectura.** Según CAP-12, el dato")
        self.assertIncidencia("código citado sin definir: CAP-12")


class TestHerramientas(Base):
    def test_herramienta_sin_justificacion(self):
        self.edita("2.3", "El volumen del proyecto cabe en un modelo por importación y no exige un servidor ni costo adicional", "")
        self.assertIncidencia("HER-02: la herramienta «Modelo semántico de Power BI» no tiene justificación")

    def test_herramienta_sin_alternativa(self):
        self.edita("2.3", "Excel con tablas dinámicas, que limita la interacción entre páginas", "")
        self.assertIncidencia("HER-03: la herramienta «Power BI Desktop» no tiene alternativa descartada")

    def test_etl_pendiente_no_es_error(self):
        self.assertEqual(self.msgs(), [])
        self.assertIn("Pendiente", (self.run / "secciones" / "2.3.md").read_text(encoding="utf-8"))

    def test_pendiente_en_visualizacion(self):
        self.edita("2.3", "| HER-04 | Power BI Service | Visualización |", "| HER-04 | Pendiente | Visualización |")
        self.assertIncidencia("HER-04: «Pendiente» solo se acepta en la capa de ETL o de almacenamiento")

    def test_pendiente_sin_motivo(self):
        self.edita("2.3", "Se decide al construir el capítulo 3, según el tiempo disponible y la facilidad de documentar cada paso", "")
        self.assertIncidencia("HER-01: la herramienta pendiente necesita su motivo")

    def test_falta_power_bi_en_visualizacion(self):
        t = (self.run / "secciones" / "2.3.md").read_text(encoding="utf-8").replace("Power BI Desktop", "Tableau").replace("Power BI Service", "Tableau Cloud")
        (self.run / "secciones" / "2.3.md").write_text(t, encoding="utf-8")
        self.assertIncidencia("Power BI debe figurar como herramienta de la capa de visualización")

    def test_capa_sin_herramienta(self):
        t = (self.run / "secciones" / "2.3.md").read_text(encoding="utf-8")
        t = "\n".join(ln for ln in t.splitlines() if not ln.startswith("| HER-02 ")) + "\n"
        (self.run / "secciones" / "2.3.md").write_text(t, encoding="utf-8")
        self.assertIncidencia("ninguna herramienta (ni «Pendiente») para la capa de almacenamiento")


class TestVisual(Base):
    def test_extraccion(self):
        d = VI.extraer("arquitectura-bi", self.root)
        self.assertEqual([c["clave"] for c in d["capas"]], ["fuentes", "etl", "almacenamiento", "visualizacion"])
        self.assertEqual([len(c["componentes"]) for c in d["capas"]], [3, 1, 1, 1])
        self.assertEqual(d["capas"][1]["herramientas"], ["Pendiente"])
        self.assertEqual(d["capas"][3]["herramientas"], ["Power BI Desktop", "Power BI Service"])

    def test_explicacion_y_construccion(self):
        d = VI.extraer("arquitectura-bi", self.root)
        txt = VI.leer_imagen("arquitectura-bi", d, F.INTERPRETACION)
        self.assertEqual(VI.validar_explicacion(txt, False), [])
        self.assertIn("3 fuentes", txt)
        self.assertIn("1 herramienta está pendiente de decidir", txt)
        html = (self.run / "visuales" / "arquitectura-bi.html").read_text(encoding="utf-8")
        self.assertIn("Pollería Don Tito", html)
        self.assertEqual(json.loads((self.run / "visuales" / "arquitectura-bi.json").read_text(encoding="utf-8")), d)

    def test_sin_fuente(self):
        with self.assertRaises(VI.SinFuente):
            VI.extraer("arquitectura-bi", self.root, run="01-01-2020-00-00-00")


class TestUpdate(Base):
    def test_completar_la_herramienta_de_etl_cambia_solo_lo_afectado(self):
        fork = Path(R.fork(PASO, ["Decidir Power Query como herramienta de ETL"], root=self.root))
        self.edita("2.3", "| HER-01 | Pendiente | ETL | Extraer, depurar, homologar y anexar las tres fuentes | Se decide al construir el capítulo 3, según el tiempo disponible y la facilidad de documentar cada paso | Power Query y scripts de Python, en evaluación |",
                   "| HER-01 | Power Query | ETL | Extraer, depurar, homologar y anexar las tres fuentes | Viene integrada con Power BI y deja cada paso registrado y repetible | Scripts de Python, que exigen más mantenimiento |", run=fork)
        self.edita("2.2", "Proceso ETL (herramienta pendiente)", "Proceso ETL en Power Query", run=fork)
        VI.construir("arquitectura-bi", self.root, fork / "visuales", H.cargar_tokens(None, "base"), run=fork.name)
        self.assertEqual(self.msgs(fork), [])
        cmp = filecmp.dircmp(self.run, fork)
        self.assertEqual(sorted(cmp.diff_files), ["README.md"] if "README.md" in cmp.diff_files else [])
        sec = filecmp.dircmp(self.run / "secciones", fork / "secciones")
        self.assertEqual(sorted(sec.diff_files), ["2.2.md", "2.3.md"])
        self.assertTrue(filecmp.cmp(self.run / "secciones" / "2.1.md", fork / "secciones" / "2.1.md", shallow=False))
        nuevo = json.loads((fork / "visuales" / "arquitectura-bi.json").read_text(encoding="utf-8"))
        self.assertEqual(nuevo["capas"][1]["herramientas"], ["Power Query"])
        self.assertEqual(nuevo["capas"][1]["componentes"][0]["nombre"], "Proceso ETL en Power Query")


if __name__ == "__main__":
    unittest.main()
