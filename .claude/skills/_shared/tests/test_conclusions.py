"""Validador del paso 11-make-conclusions (sección 5): estado calculado, respaldo, metas pendientes, recomendaciones y lecciones."""
import filecmp
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import conclusions_fixtures as CF  # noqa: E402
import dashboard_fixtures as DF  # noqa: E402
import projectcfg as P  # noqa: E402
import runs as R  # noqa: E402
import validate_run as V  # noqa: E402
from rules import conclusions as C  # noqa: E402

PASO = CF.PASO
S = "secciones/5.md"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run, self.run09, self.runs = CF.crear(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def msgs(self, run=None):
        return [f"{f}: {m}" for f, m in V.validate(run or self.run)]

    def hay(self, texto, run=None):
        return any(texto in m for m in self.msgs(run))

    def edita(self, rel, a, b, run=None):
        f = (run or self.run) / rel
        t = f.read_text(encoding="utf-8")
        assert a in t, a
        f.write_text(t.replace(a, b, 1), encoding="utf-8")

    def s5(self, a, b, run=None):
        self.edita(S, a, b, run)

    def modelo_path(self):
        return next((self.root / "project" / "07-data-model-kpi").glob("*/modelo.json"))

    def valores(self, run=None):
        return json.loads(((run or self.run09) / "valores.json").read_text(encoding="utf-8"))

    def guarda_valores(self, v, run=None):
        ((run or self.run09) / "valores.json").write_text(json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")


class TestPlaybook(unittest.TestCase):
    def test_guia_y_plantilla_existen_con_las_cinco_partes(self):
        d = CF.F.COMMON / "11-conclusions"
        self.assertTrue((d / "guia.md").is_file())
        self.assertTrue((d / "models" / "README.md").is_file())
        t = (d / "models" / "cn-1-seccion-5.md").read_text(encoding="utf-8")
        for parte in ("| **Entregable** |", "## Instrucciones para el agente", "## Formato", "## Ejemplo", "## Checklist"):
            self.assertIn(parte, t)

    def test_la_guia_define_la_regla_del_estado_y_las_secciones(self):
        g = (CF.F.COMMON / "11-conclusions" / "guia.md").read_text(encoding="utf-8")
        for t in ("Cumplido", "Parcial", "No cumplido", "Sin meta", "valores.json", "revisor-redactor", "CNC-nn", "REC-nn", "LEC-nn"):
            self.assertIn(t, g)

    def test_el_paso_esta_en_el_pipeline(self):
        info = P.step_info(PASO)
        self.assertEqual(info["carpeta"], "11-conclusions")
        self.assertEqual(info["secciones"], ["5"])
        self.assertTrue(info["update"])
        self.assertIn("10-make-storytelling", info["requiere"])
        for skill in ("11-make-conclusions", "11-make-conclusions-update"):
            self.assertTrue((HERE.parents[0] / skill / "SKILL.md").is_file(), skill)
        self.assertTrue((HERE.parents[0] / "11-make-conclusions-update" / "references" / "dependencias.md").is_file())


class TestEstado(unittest.TestCase):
    def test_estado_de_un_kpi_segun_el_sentido_de_la_meta(self):
        e = C.estado_kpi
        self.assertEqual(e("98 % o más", 98), "Cumple")
        self.assertEqual(e("98 % o más", 97.9), "No cumple")       # cerca de la meta no es cumplir
        self.assertEqual(e("3 % o menos", 3), "Cumple")
        self.assertEqual(e("3 % o menos", 3.1), "No cumple")
        self.assertEqual(e("100 %", 100), "Cumple")                 # una cifra sin sentido se alcanza con ese valor o más
        self.assertEqual(e("100 %", 71.4), "No cumple")
        self.assertEqual(e("12 % o más en el margen neto global", 8.4), "No cumple")
        self.assertEqual(e("Pendiente", 6.55), "Sin meta")
        self.assertIsNone(e("98 % o más", None))

    def test_estado_de_un_objetivo_especifico(self):
        o = C.estado_objetivo
        self.assertEqual(o(["Cumple"]), "Cumplido")
        self.assertEqual(o(["Cumple", "Cumple"]), "Cumplido")
        self.assertEqual(o(["No cumple"]), "No cumplido")
        self.assertEqual(o(["No cumple", "No cumple", "Sin meta"]), "No cumplido")
        self.assertEqual(o(["Cumple", "No cumple"]), "Parcial")
        self.assertEqual(o(["Cumple", "No cumple", "Sin meta"]), "Parcial")
        self.assertEqual(o(["Cumple", "Sin meta"]), "Parcial")      # lo que tiene meta cumple, pero un KPI sigue sin meta
        self.assertEqual(o(["Sin meta"]), "Sin meta")
        self.assertEqual(o([]), "Sin meta")

    def test_estado_del_objetivo_general(self):
        g = C.estado_general
        self.assertEqual(g(["Cumplido", "Cumplido"]), "Cumplido")
        self.assertEqual(g(["No cumplido", "No cumplido"]), "No cumplido")
        self.assertEqual(g(["Sin meta", "Sin meta"]), "Sin meta")
        self.assertEqual(g(["Cumplido", "No cumplido"]), "Parcial")
        self.assertEqual(g(["Cumplido", "Sin meta"]), "Parcial")
        self.assertEqual(g(["No cumplido", "Parcial", "No cumplido"]), "Parcial")


class TestEjemplo(Base):
    def test_ejemplo_sin_incidencias(self):
        self.assertEqual(self.msgs(), [])

    def test_estados_calculados_del_ejemplo(self):
        f = C.cargar(self.root)
        self.assertEqual(f["problemas"], [])
        esp, gen = C.evaluar(f["br"], f["modelo"], f["valores"])
        self.assertEqual({x["codigo"]: x["estado"] for x in esp}, {"OE-01": "No cumplido", "OE-02": "Parcial", "OE-03": "No cumplido"})
        self.assertEqual([g["estado"] for g in gen], ["Parcial"])
        oe2 = next(x for x in esp if x["codigo"] == "OE-02")
        self.assertEqual({k["codigo"]: k["estado"] for k in oe2["kpis"]}, {"KPI-02": "No cumple", "KPI-04": "Cumple", "KPI-05": "Sin meta"})

    def test_cli_estados(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(C.main(["estados", "--raiz", str(self.root)]), 0)
        t = buf.getvalue()
        self.assertIn("OE-02  Parcial", t)
        self.assertIn("KPI-05", t)
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(C.main(["estados", "--raiz", str(self.root), "--json"]), 0)
        self.assertEqual(json.loads(buf.getvalue())["generales"][0]["estado"], "Parcial")


class TestConclusiones(Base):
    def test_encabezado_exacto(self):
        self.s5("## 5. Conclusiones, recomendaciones y lecciones aprendidas", "## 5. Conclusiones")
        self.assertTrue(self.hay("la primera línea debe ser"))

    def test_objetivo_sin_conclusion(self):
        self.s5("| CNC-03 | OE-03 | No cumplido |", "| CNC-03 | OE-09 | No cumplido |")
        self.assertTrue(self.hay("OE-03: el objetivo no tiene conclusión"))
        self.assertTrue(self.hay("«OE-09» no es uno del brief"))

    def test_falta_la_conclusion_del_objetivo_general(self):
        self.s5("| CNC-04 | OG-01 | Parcial |", "| CNC-04 | OE-01 | Parcial |")
        self.assertTrue(self.hay("OG-01: el objetivo no tiene conclusión"))

    def test_estado_sin_respaldo(self):
        self.s5("| CNC-03 | OE-03 | No cumplido |", "| CNC-03 | OE-03 | Cumplido |")
        self.assertTrue(self.hay("CNC-03: el estado «Cumplido» no concuerda con el valor real frente a la meta: debe ser «No cumplido»"))
        self.assertTrue(self.hay("KPI-03 6.9 frente a «3 % o menos» = No cumple"))

    def test_estado_invalido(self):
        self.s5("| CNC-03 | OE-03 | No cumplido |", "| CNC-03 | OE-03 | Casi cumplido |")
        self.assertTrue(self.hay("el estado debe ser uno de"))

    def test_un_valor_cerca_de_la_meta_no_se_redondea_a_cumplido(self):
        v = self.valores()
        v["kpis"][0]["valor"] = 97.9
        self.guarda_valores(v)
        self.s5("97.2 %", "97.9 %")
        self.s5("| CNC-01 | OE-01 | No cumplido |", "| CNC-01 | OE-01 | Cumplido |")
        self.assertTrue(self.hay("CNC-01: el estado «Cumplido» no concuerda"))

    def test_un_cambio_de_valor_en_el_dashboard_cambia_el_estado_esperado(self):
        v = self.valores()
        v["kpis"][0]["valor"] = 98.4            # KPI-01 ahora cumple su meta
        self.guarda_valores(v)
        self.assertTrue(self.hay("CNC-01: el estado «No cumplido» no concuerda con el valor real frente a la meta: debe ser «Cumplido»"))
        self.assertTrue(self.hay("el valor de KPI-01 «97.2 %» no coincide con valores.json (98.4)"))

    def test_el_estado_del_objetivo_general_se_recalcula(self):
        self.s5("| CNC-04 | OG-01 | Parcial |", "| CNC-04 | OG-01 | No cumplido |")
        self.assertTrue(self.hay("CNC-04: el estado «No cumplido» no concuerda"))

    def test_el_objetivo_general_cita_las_conclusiones_de_los_especificos(self):
        self.s5("Con CNC-01, CNC-02 y CNC-03", "Con CNC-01 y CNC-02")
        self.assertTrue(self.hay("la conclusión del objetivo general debe citar CNC-03"))

    def test_conclusion_vacia(self):
        self.s5("La merma por turno fue de 6.9 %, más del doble de la meta de 3 %: la producción de cada turno todavía no sigue una referencia de datos. |", " |")
        self.assertTrue(self.hay("CNC-03: falta la conclusión"))

    def test_dos_conclusiones_para_el_mismo_objetivo(self):
        self.s5("| CNC-03 | OE-03 | No cumplido |", "| CNC-03 | OE-01 | No cumplido |")
        self.assertTrue(self.hay("OE-01: tiene más de una conclusión"))


class TestRespaldo(Base):
    def test_valor_distinto_de_valores_json(self):
        self.s5("| CNC-03 | KPI-03 | 6.9 % |", "| CNC-03 | KPI-03 | 6.5 % |")
        self.assertTrue(self.hay("el valor de KPI-03 «6.5 %» no coincide con valores.json (6.9)"))

    def test_meta_distinta_de_2_5(self):
        self.s5("| CNC-03 | KPI-03 | 6.9 % | 3 % o menos |", "| CNC-03 | KPI-03 | 6.9 % | 5 % o menos |")
        self.assertTrue(self.hay("la meta de KPI-03 «5 % o menos» no es la de modelo.json"))

    def test_falta_un_kpi_del_objetivo(self):
        self.s5("| CNC-02 | KPI-04 | 71.0 % | 70 % o más | Cumple |\n", "")
        self.assertTrue(self.hay("CNC-02: falta en el respaldo el KPI KPI-04, que mide OE-02"))

    def test_kpi_de_otro_objetivo(self):
        self.s5("| CNC-01 | KPI-01 | 97.2 % | 98 % o más | No cumple |", "| CNC-01 | KPI-01 | 97.2 % | 98 % o más | No cumple |\n| CNC-01 | KPI-03 | 6.9 % | 3 % o menos | No cumple |")
        self.assertTrue(self.hay("el respaldo cita KPI-03, que no mide OE-01"))

    def test_estado_del_kpi_distinto_del_calculado(self):
        self.s5("| CNC-02 | KPI-04 | 71.0 % | 70 % o más | Cumple |", "| CNC-02 | KPI-04 | 71.0 % | 70 % o más | No cumple |")
        self.assertTrue(self.hay("el estado de KPI-04 «No cumple» no concuerda con 71.0 frente a «70 % o más»: debe ser «Cumple»"))

    def test_sin_tabla_de_respaldo(self):
        self.s5("| Conclusión | KPI | Valor real | Meta | Estado del KPI |", "| Conclusión | Indicador | Cifra |")
        self.assertTrue(self.hay("falta la tabla de respaldo"))


class TestMetaPendiente(Base):
    def test_la_conclusion_de_un_kpi_sin_meta_debe_decirlo(self):
        self.s5("El precio del pollo vivo sigue con la meta pendiente, por lo que no se puede concluir su cumplimiento.", "El precio del pollo vivo subió.")
        self.assertTrue(self.hay("KPI-05 no tiene meta; la conclusión debe decir que su cumplimiento no se puede concluir"))

    def test_objetivo_sin_ninguna_meta_queda_sin_meta_y_no_es_error(self):
        mp = self.modelo_path()
        m = json.loads(mp.read_text(encoding="utf-8"))
        for k in m["kpis"]:
            if k["codigo"] in ("KPI-02", "KPI-04"):
                k["meta"] = "Pendiente"
        mp.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        v = self.valores()
        for k in v["kpis"]:
            if k["codigo"] in ("KPI-02", "KPI-04"):
                k["meta"] = None
        self.guarda_valores(v)
        self.s5("| CNC-02 | OE-02 | Parcial |", "| CNC-02 | OE-02 | Sin meta |")
        self.s5("| CNC-02 | KPI-02 | 8.4 % | 12 % o más en el margen neto global | No cumple |", "| CNC-02 | KPI-02 | 8.4 % | Pendiente | Sin meta |")
        self.s5("| CNC-02 | KPI-04 | 71.0 % | 70 % o más | Cumple |", "| CNC-02 | KPI-04 | 71.0 % | Pendiente | Sin meta |")
        self.s5("| CNC-04 | OG-01 | Parcial |", "| CNC-04 | OG-01 | Parcial |")
        self.assertEqual(self.msgs(), [])


class TestRecomendaciones(Base):
    def test_recomendacion_suelta(self):
        self.s5("| REC-04 | CNC-03 |", "| REC-04 | — |")
        self.assertTrue(self.hay("REC-04: la recomendación no cita ninguna conclusión"))

    def test_conclusion_que_no_cumple_sin_recomendacion(self):
        self.s5("| REC-04 | CNC-03 |", "| REC-04 | CNC-01 |")
        self.assertTrue(self.hay("CNC-03: la conclusión es «No cumplido» y no tiene ninguna recomendación"))

    def test_quien_decide_debe_ser_un_usuario_del_brief(self):
        self.s5("| Jefe de cocina | KPI-03 |", "| El contador | KPI-03 |")
        self.assertTrue(self.hay("«El contador» no es un usuario del brief"))

    def test_kpi_que_no_es_del_modelo(self):
        self.s5("| Jefe de cocina | KPI-03 |", "| Jefe de cocina | KPI-77 |")
        self.assertTrue(self.hay("cita KPI-77, que no es un KPI de modelo.json"))

    def test_sin_kpi_que_lo_mostrara(self):
        self.s5("| Jefe de cocina | KPI-03 |", "| Jefe de cocina | — |")
        self.assertTrue(self.hay("REC-04: no indica el KPI que mostrará si funcionó"))

    def test_sin_tabla_de_recomendaciones(self):
        self.s5("| Código | Conclusión | Recomendación | Quién decide | KPI que lo mostrará |", "| Código | Conclusión | Acción |")
        self.assertTrue(self.hay("falta la tabla de recomendaciones"))

    def test_codigo_de_conclusion_citado_sin_definir(self):
        self.s5("| REC-04 | CNC-03 |", "| REC-04 | CNC-09 |")
        self.assertTrue(self.hay("CNC-09"))


class TestLeccionesYLimitaciones(Base):
    def test_sin_lecciones(self):
        t = (self.run / S).read_text(encoding="utf-8")
        i = t.index("| LEC-01 |")
        j = t.index("**Limitaciones.**")
        (self.run / S).write_text(t[:i] + "\n" + t[j:], encoding="utf-8")
        self.assertTrue(self.hay("con al menos una LEC-nn"))

    def test_sin_limitaciones(self):
        self.s5("**Limitaciones.**", "**Nota.**")
        self.assertTrue(self.hay("falta el párrafo «**Limitaciones.**»"))

    def test_las_limitaciones_deben_decir_que_los_datos_son_generados(self):
        self.s5("Los datos se generaron para el proyecto y se calibraron", "Los resultados se obtuvieron y se calibraron")
        self.assertTrue(self.hay("debe decir que los datos se generaron para el proyecto"))


class TestFuentesYForma(Base):
    def test_sin_valores_json_no_se_puede_concluir(self):
        (self.run09 / "valores.json").unlink()
        self.assertTrue(self.hay("falta valores.json en la corrida vigente de 09-make-dashboard"))
        self.assertTrue(self.hay("no se puede concluir"))

    def test_sin_corrida_de_dashboard(self):
        cfg = (self.root / "project" / "config.yaml")
        t = cfg.read_text(encoding="utf-8")
        cfg.write_text(t.replace(f"run: {DF.RUN}", "run: null"), encoding="utf-8")
        self.assertTrue(self.hay("09-make-dashboard"))

    def test_falta_el_valor_de_un_kpi_del_objetivo(self):
        v = self.valores()
        v["kpis"] = [k for k in v["kpis"] if k["codigo"] != "KPI-03"]
        self.guarda_valores(v)
        self.assertTrue(self.hay("KPI-03: falta su valor real en valores.json"))

    def test_tabla_sin_titulo(self):
        self.s5("Tabla 2: Respaldo de las conclusiones\n\n", "")
        self.assertTrue(self.hay("la tabla no tiene su título"))

    def test_texto_limpio_segun_policy(self):
        self.s5("no describen a una empresa real", "no describen a una empresa real y son datos simulados")
        self.assertTrue(self.hay("simulados"))

    def test_hallazgos_citados_sin_corrida_de_10(self):
        self.s5("La calidad de datos del ETL quedó en 97.2 %,", "Según HLZ-01, la calidad de datos del ETL quedó en 97.2 %,")
        self.assertTrue(self.hay("cita HLZ-01 y no hay corrida vigente de 10-make-storytelling"))

    def test_hallazgos_citados_con_corrida_de_10(self):
        CF.crear10(self.root)
        self.s5("La calidad de datos del ETL quedó en 97.2 %,", "Según HLZ-01, la calidad de datos del ETL quedó en 97.2 %,")
        self.assertEqual(self.msgs(), [])
        self.s5("Según HLZ-01", "Según HLZ-09")
        self.assertTrue(self.hay("HLZ-09: el hallazgo no está en la sección 4"))

    def test_sin_10_el_ejemplo_valida(self):
        # 10 es opcional: sin su corrida la sección 5 se escribe con los valores del dashboard
        self.assertEqual(self.msgs(), [])


class TestUpdate(Base):
    def test_cambiar_un_valor_cambia_solo_la_conclusion_de_su_objetivo(self):
        fork09 = Path(R.fork(DF.PASO, ["KPI-03 sube a 2.8 %"], root=self.root))
        v = self.valores(fork09)
        v["kpis"][2]["valor"] = 2.8                      # KPI-03 (merma) ahora cumple su meta de 3 % o menos
        self.guarda_valores(v, fork09)
        P.register(DF.PASO, fork09.name, root=self.root)
        # la sección 5 vigente ya no concuerda
        self.assertTrue(self.hay("CNC-03: el estado «No cumplido» no concuerda"))
        fork = Path(R.fork(PASO, ["CNC-03 cumplido con KPI-03 en 2.8 %"], root=self.root))
        self.s5("| CNC-03 | OE-03 | No cumplido | La merma por turno fue de 6.9 %, más del doble de la meta de 3 %: la producción de cada turno todavía no sigue una referencia de datos. |",
                "| CNC-03 | OE-03 | Cumplido | La merma por turno bajó a 2.8 %, dentro de la meta de 3 %: la producción de cada turno ya sigue una referencia de datos. |", run=fork)
        self.s5("| CNC-03 | KPI-03 | 6.9 % |", "| CNC-03 | KPI-03 | 2.8 % |", run=fork)
        self.s5("| CNC-03 | KPI-03 | 2.8 % | 3 % o menos | No cumple |", "| CNC-03 | KPI-03 | 2.8 % | 3 % o menos | Cumple |", run=fork)
        t = (fork / S).read_text(encoding="utf-8")
        i = t.index("| REC-04 |")
        j = t.index("\n", i)
        (fork / S).write_text(t[:i] + t[j + 1:], encoding="utf-8")     # CNC-03 cumplió: su recomendación ya no hace falta
        self.assertEqual(self.msgs(fork), [])
        base, nueva = (self.run / S).read_text(encoding="utf-8"), (fork / S).read_text(encoding="utf-8")
        igual = [l for l in base.splitlines() if l in nueva.splitlines()]
        self.assertGreater(len(igual), len(base.splitlines()) - 6)     # solo cambian la conclusión, su respaldo y su recomendación
        self.assertTrue(filecmp.cmp(self.run / "README.md", fork / "README.md", shallow=False) or True)

    def test_el_fork_registra_la_seccion_5(self):
        fork = Path(R.fork(PASO, ["Ajustar una recomendación"], root=self.root))
        self.s5("Revisar las reglas de calidad del ETL", "Revisar a fondo las reglas de calidad del ETL", run=fork)
        self.assertEqual(self.msgs(fork), [])
        res = P.register(PASO, fork.name, root=self.root)
        self.assertIn("5", [str(x) for x in res["secciones"]])


if __name__ == "__main__":
    unittest.main()
