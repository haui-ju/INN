"""Armado del informe (report.py): índice, plan, construcción, figuras, tablas, referencias, anexos y HTML."""
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import projectcfg as P  # noqa: E402
import report as R  # noqa: E402
import report_fixtures as RF  # noqa: E402

ANEXO_A = "# Anexo A: Diccionario de datos\n\nTabla 1: Campos de la tabla de ventas\n\n| Campo | Tipo |\n|---|---|\n| fecha | fecha |\n\n<!-- figura: calidad -->\n"


class Base(unittest.TestCase):
    skills = (RF.DIAG, RF.ESTR, RF.OBJ)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.prev = os.environ.get("PROJECT_ROOT")
        os.environ["PROJECT_ROOT"] = str(self.root)
        self.dirs = RF.crear(self.root, self.skills)

    def tearDown(self):
        if self.prev is None:
            os.environ.pop("PROJECT_ROOT", None)
        else:
            os.environ["PROJECT_ROOT"] = self.prev
        self.tmp.cleanup()

    def construir(self, **kw):
        self.run = self.root / "project" / R.CARPETA / "r1"
        self.res = R.construir(self.root, self.run, **kw)
        self.txt = (self.run / R.INFORME).read_text(encoding="utf-8")
        self.falt = (self.run / "faltantes.md").read_text(encoding="utf-8")
        return self.txt


class TestIndice(unittest.TestCase):
    def test_marca_de_imagen_por_punto(self):
        idx = R.cargar_indice()
        self.assertTrue(idx["puntos"]["1.6"]["imagen"])
        self.assertTrue(idx["puntos"]["4"]["imagen"])
        self.assertFalse(idx["puntos"]["1.1"]["imagen"])
        con = [p for p, d in idx["puntos"].items() if d["imagen"]]
        self.assertEqual(con, ["1.4", "1.5", "1.6", "1.7", "2.2", "2.4", "3.2", "4"])

    def test_titulos_limpios_y_capitulos(self):
        idx = R.cargar_indice()
        self.assertEqual(idx["puntos"]["1.4"]["titulo"], "Modelo de negocio: Business Model Canvas")
        self.assertEqual(idx["puntos"]["1.4"]["detalle"], "los nueve bloques del lienzo")
        self.assertEqual(idx["puntos"]["2.5"]["titulo"], "Indicadores clave de rendimiento (KPI)")
        self.assertEqual(idx["puntos"]["4"]["titulo"], "Storytelling con datos")
        self.assertEqual(idx["puntos"]["3.2"]["capitulo"], 3)
        self.assertEqual(list(idx["caps"]), [1, 2, 3, 4, 5])
        self.assertEqual(len(idx["puntos"]), 19)

    def test_anexos_con_su_origen(self):
        an = R.cargar_indice()["anexos"]
        self.assertEqual(list(an), ["A", "B", "C", "D"])
        self.assertEqual([an[x]["origen"] for x in an], ["3.1", "3.1", "3.2", "3.2"])
        self.assertEqual(an["A"]["titulo"], "Diccionario de datos y calidad de datos")

    def test_introducciones_desde_el_playbook(self):
        intro = R.introducciones()
        self.assertEqual(sorted(intro), [1, 2, 3, 4, 5])
        self.assertTrue(intro[1].startswith("Este capítulo presenta a la empresa"))


class TestPlan(Base):
    def test_informe_parcial(self):
        pl = R.plan(self.root)
        self.assertEqual([x["seccion"] for x in pl["incluidas"]], ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "1.10"])
        pend = {x["seccion"]: x["skill"] for x in pl["pendientes"]}
        self.assertEqual(list(pend), ["2.1", "2.2", "2.3", "2.4", "2.5", "3.1", "3.2", "4", "5"])
        self.assertEqual(pend["2.4"], "07-make-data-model-kpi")
        self.assertEqual([a["anexo"] for a in pl["anexos_pendientes"]], ["A", "B", "C", "D"])
        self.assertTrue(pl["brief"])

    def test_figuras_del_plan(self):
        figs = {f["visual"]: f for f in R.plan(self.root)["figuras"]}
        self.assertEqual(list(figs), ["bmc", "pestel", "foda", "ishikawa"])
        self.assertTrue(figs["foda"]["html"] and figs["foda"]["explicacion"])
        self.assertFalse(figs["pestel"]["explicacion"])

    def test_seccion_disponible_sin_archivo(self):
        (self.dirs[RF.ESTR] / "secciones" / "1.5.md").unlink()
        pl = R.plan(self.root)
        self.assertNotIn("1.5", [x["seccion"] for x in pl["incluidas"]])
        x = next(x for x in pl["pendientes"] if x["seccion"] == "1.5")
        self.assertEqual(x["skill"], RF.ESTR)
        self.assertIn("secciones/1.5.md", x["motivo"])

    def test_carpeta_de_corrida_borrada(self):
        shutil.rmtree(self.dirs[RF.OBJ])
        pend = {x["seccion"]: x["motivo"] for x in R.plan(self.root)["pendientes"]}
        self.assertIn("1.8", pend)
        self.assertIn("no existe la carpeta", pend["1.8"])

    def test_cli_plan_json(self):
        import contextlib
        import io
        import json
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(R.main(["plan", "--json", "--raiz", str(self.root)]), 0)
        d = json.loads(buf.getvalue())
        self.assertEqual(len(d["incluidas"]), 10)
        self.assertEqual(d["corridas"][0]["skill"], RF.DIAG)


class TestSinSecciones(Base):
    skills = ()

    def test_ninguna_seccion(self):
        txt = self.construir()
        self.assertNotIn("# Capítulo", txt)
        self.assertIn("## Control del documento", txt)
        self.assertIn("# Referencias bibliográficas", txt)
        for p in R.cargar_indice()["puntos"]:
            self.assertIn(f"\n| {p} |", self.falt)
        self.assertIn("Ninguna de las corridas usadas aporta", self.falt)


class TestConstruir(Base):
    def test_orden_y_titulos_del_indice(self):
        txt = self.construir()
        heads = [l for l in txt.splitlines() if l.startswith("## 1.")]
        self.assertEqual([h.split(".")[0] + "." + h.split(".")[1] for h in heads][:1], ["## 1.1"])
        self.assertEqual(len(heads), 10)
        self.assertIn("## 1.4. Modelo de negocio: Business Model Canvas", txt)
        self.assertNotIn("Modelo de negocio con el lienzo", txt)
        self.assertLess(txt.index("## 1.9."), txt.index("## 1.10."))
        self.assertIn("### Propuesta de valor", txt)

    def test_pendientes_no_aparecen_y_van_a_faltantes(self):
        txt = self.construir()
        self.assertNotIn("# Capítulo 2", txt)
        self.assertNotIn("## 2.1.", txt)
        self.assertIn("| 2.1 | Propuesta de solución en BI | 06-make-bi-solution |", self.falt)
        self.assertNotIn("| 1.1 |", self.falt)
        self.assertNotIn("Pendiente.**", txt)

    def test_no_copia_el_readme_de_las_corridas(self):
        self.assertNotIn("escrita por la prueba", self.construir())

    def test_control_del_documento(self):
        txt = self.construir(curso="Inteligencia de Negocios")
        self.assertIn("| Fecha de entrega | 30-11-2026 |", txt)
        self.assertIn("| Empresa | Pollería Don Tito", txt)
        self.assertIn("| Integrantes | ariel, Piero (Analista de datos) |", txt)
        self.assertIn("| Curso | Inteligencia de Negocios |", txt)
        self.assertIn("| Docente | Pendiente |", txt)
        self.assertIn("| Docente |", self.falt)
        self.assertNotIn("| Curso |", self.falt)
        self.assertNotIn("Versión", txt)
        self.assertIn("Arial 11", txt)

    def test_referencias_combinadas_sin_duplicados(self):
        txt = self.construir()
        refs = txt.split("# Referencias bibliográficas", 1)[1].strip().split("\n\n")
        self.assertEqual(refs, [RF.REF_ISHI, RF.REF_KOTLER, RF.REF_OSTER])

    def test_figura_completa(self):
        txt = self.construir()
        self.assertIn("(INCLUIR IMAGEN: Figura 3: Matriz FODA de Pollería Don Tito. Archivo sugerido: imagenes/foda.html)", txt)
        self.assertIn("**Cómo copiarla.** Abrir [imagenes/foda.html](imagenes/foda.html)", txt)
        self.assertIn("**Cómo leer la figura.** Cruza fortalezas y debilidades con oportunidades y amenazas. La receta propia compensa la presión del costo del pollo. "
                      "La amenaza del insumo se marca en rojo.", txt)
        self.assertNotIn("<!-- figura", txt)
        self.assertTrue((self.run / "imagenes" / "foda.html").is_file())

    def test_figura_sin_explicacion(self):
        txt = self.construir()
        bloque = txt.split("## 1.5.", 1)[1].split("## 1.6.", 1)[0]
        self.assertIn("(INCLUIR IMAGEN: Figura 2: Análisis PESTEL. Archivo sugerido: imagenes/pestel.html)", bloque)
        self.assertNotIn("Cómo leer la figura", bloque)
        self.assertTrue(any("pestel" in a and RF.ESTR in a for a in self.res["avisos"]))
        self.assertIn("| Figura 2 | pestel |", self.falt)

    def test_figura_sin_html(self):
        (self.dirs[RF.ESTR] / "visuales" / "ishikawa.html").unlink()
        txt = self.construir()
        self.assertIn("(INCLUIR IMAGEN: Figura 4: Diagrama de Ishikawa del margen neto. Archivo sugerido: imagenes/ishikawa.html)", txt)
        self.assertIn("no tiene HTML en la corrida de 04-make-strategic-analysis", txt)
        self.assertFalse((self.run / "imagenes" / "ishikawa.html").exists())
        self.assertIn("| Figura 4 | ishikawa |", self.falt)

    def test_numeracion_y_menciones(self):
        txt = self.construir()
        self.assertIn("La Figura 1 muestra los nueve bloques", txt)
        self.assertIn("como muestra la Figura 3.", txt)
        self.assertIn("Tabla 1: Datos del sector", txt)
        self.assertIn("La Tabla 1 resume", txt)
        self.assertIn("Tabla 2: Estrategias cruzadas", txt)
        self.assertEqual(self.res["figuras"], 4)
        self.assertEqual(self.res["tablas"], 2)

    def test_mencion_local_pasa_al_numero_global(self):
        sec = RF.SECCIONES[RF.ESTR]["1.5"] + "\nLa Figura 1 resume el entorno.\n"
        (self.dirs[RF.ESTR] / "secciones" / "1.5.md").write_text(sec, encoding="utf-8")
        self.assertIn("La Figura 2 resume el entorno.", self.construir())

    def test_imagenes_e_indice(self):
        self.construir()
        ind = (self.run / "imagenes" / "INDICE.md").read_text(encoding="utf-8")
        for v, n, s in (("bmc", 1, "1.4"), ("foda", 3, "1.6")):
            self.assertIn(f"| [{v}.html]({v}.html) | Figura {n} | la sección {s} |", ind)

    def test_readme_de_procedencia(self):
        self.construir()
        rd = (self.run / "README.md").read_text(encoding="utf-8")
        self.assertIn("Modo de datos del config: generado", rd)
        self.assertIn(f"| {RF.ESTR} | {RF.RUN} | 1.5, 1.6, 1.7 |", rd)

    def test_no_sobrescribe_un_informe(self):
        self.construir()
        with self.assertRaises(R.ReportError):
            R.construir(self.root, self.run)

    def test_aviso_de_seccion_con_imagen_sin_figura(self):
        (self.dirs[RF.ESTR] / "secciones" / "1.7.md").write_text("## 1.7. Ishikawa\n\nSolo texto.\n", encoding="utf-8")
        self.construir()
        self.assertTrue(any("1.7" in a and "incluye imagen" in a for a in self.res["avisos"]))


class TestIntroducciones(Base):
    skills = (RF.DIAG,)

    def test_capitulo_con_parte_de_sus_secciones(self):
        txt = self.construir()
        intro = txt.split("# Capítulo 1:", 1)[1].split("## 1.1.", 1)[0]
        self.assertIn("Comprende 1.1 Nombre de la empresa, 1.2 Misión y visión, 1.3 Industria y tamaño y 1.4 Modelo de negocio: Business Model Canvas.", intro)
        self.assertNotIn("1.5", intro)
        self.assertNotIn("# Capítulo 3", txt)


class TestAnexos(Base):
    def test_anexo_sin_origen(self):
        self.construir()
        self.assertNotIn("# Anexos", self.txt)
        self.assertIn("| A | Diccionario de datos y calidad de datos | 08-make-etl |", self.falt)
        self.assertFalse((self.run / "anexos").exists())

    def test_anexo_presente(self):
        RF.corrida(self.root, RF.ETL, {"3.1": "## 3.1. Construcción de la solución ETL\n\nEl ETL limpia y carga las ventas.\n"},
                   visuales=["calidad"], anexos={"A": ANEXO_A})
        txt = self.construir()
        self.assertIn("# Capítulo 3: Construcción y calidad del dashboard en Power BI", txt)
        self.assertIn("## Anexo A: Diccionario de datos y calidad de datos", txt)
        self.assertIn("Tabla 3: Campos de la tabla de ventas", txt)
        self.assertIn("(INCLUIR IMAGEN: Figura 5:", txt)
        self.assertNotIn("## Anexo B", txt)
        self.assertIn("| B | Scripts del ETL | 08-make-etl | la corrida", self.falt)
        propio = (self.run / "anexos" / "anexo-a.md").read_text(encoding="utf-8")
        self.assertTrue(propio.startswith("# Anexo A: Diccionario de datos y calidad de datos"))
        self.assertIn("[imagenes/calidad.html](../imagenes/calidad.html)", propio)
        self.assertIn("Figura 5", propio)

    def test_anexos_html_de_la_corrida_vigente(self):
        RF.corrida(self.root, RF.ETL, {"3.1": "## 3.1. ETL\n\nTexto.\n"}, visuales=["calidad"], anexos={"A": ANEXO_A})
        self.construir()
        with self.assertRaises(R.ReportError):
            R.anexos(self.root)
        P.register(R.PASO, "r1", root=self.root)
        d, hechos = R.anexos(self.root)
        self.assertIn("anexo-a.html", hechos)
        self.assertIn("index.html", hechos)
        self.assertEqual(R.anexos(self.root, comprobar=True)[1], [])
        self.assertIn('href="../../imagenes/calidad.html"', (d / "anexos" / "html" / "anexo-a.html").read_text(encoding="utf-8"))
        (self.run / "anexos" / "anexo-a.md").write_text("# Anexo A: cambiado\n", encoding="utf-8")
        self.assertTrue(R.anexos(self.root, comprobar=True)[1])

    def test_informe_sin_anexos(self):
        self.construir()
        P.register(R.PASO, "r1", root=self.root)
        with self.assertRaises(R.ReportError) as cm:
            R.anexos(self.root)
        self.assertIn("3.1", str(cm.exception))


class TestRender(Base):
    def test_html_autonomo_con_los_encabezados_del_markdown(self):
        import doc_html as DH
        from rules import report as RR
        self.construir()
        out, base = R.render(self.run / R.INFORME, self.root)
        self.assertTrue(base)
        h = out.read_text(encoding="utf-8")
        self.assertIsNone(DH.EXTERNO.search(h))
        self.assertEqual(RR.check_html(self.run, RR.vivas(self.txt)), [])
        self.assertIn("INCLUIR IMAGEN: Figura 1", h)


if __name__ == "__main__":
    unittest.main()
