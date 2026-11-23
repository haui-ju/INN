"""Validador del paso 10-make-storytelling (sección 4: hallazgos, cifras, capturas y datos generados) y su -update."""
import filecmp
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dashboard_fixtures as DF  # noqa: E402
import projectcfg as P  # noqa: E402
import report as RP  # noqa: E402
import runs as R  # noqa: E402
import storytelling_fixtures as SF  # noqa: E402
import validate_run as V  # noqa: E402
from rules import storytelling as ST  # noqa: E402

PASO = SF.PASO
COMMON = HERE.parents[2] / "common" / "10-storytelling"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run, self.run9, self.runs = SF.crear(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def msgs(self, run=None):
        return [f"{f}: {m}" for f, m in V.validate(run or self.run)]

    def edita(self, a, b, run=None, rel="secciones/4.md"):
        f = (run or self.run) / rel
        t = f.read_text(encoding="utf-8")
        assert a in t, a
        f.write_text(t.replace(a, b, 1), encoding="utf-8")

    def valores9(self):
        return json.loads((self.run9 / "valores.json").read_text(encoding="utf-8"))

    def guarda_valores9(self, v):
        (self.run9 / "valores.json").write_text(json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")

    def assertIncidencia(self, texto, run=None):
        m = self.msgs(run)
        self.assertTrue(any(texto in x for x in m), m)


class TestPlaybook(unittest.TestCase):
    def test_guia_y_plantillas_con_las_cinco_partes(self):
        self.assertTrue((COMMON / "guia.md").is_file())
        plantillas = sorted((COMMON / "models").glob("st-*.md"))
        self.assertEqual([p.name for p in plantillas], ["st-1-seccion-4.md", "st-2-propuesta.md"])
        self.assertTrue((COMMON / "models" / "README.md").is_file())
        for p in plantillas:
            t = p.read_text(encoding="utf-8")
            self.assertIn("| **Entregable** |", t, p.name)
            for parte in ("## Instrucciones para el agente", "## Formato", "## Ejemplo", "## Checklist"):
                self.assertIn(parte, t, f"{p.name}: {parte}")

    def test_la_guia_dice_que_se_detiene_sin_valores_y_que_las_cifras_salen_de_valores_json(self):
        t = (COMMON / "guia.md").read_text(encoding="utf-8")
        self.assertIn("Sin `valores.json` la skill se detiene", t)
        self.assertIn("Toda cifra con unidad", t)


class TestSkills(unittest.TestCase):
    SKILLS = HERE.parent

    def test_las_dos_skills_existen_con_su_nombre_y_sus_reglas(self):
        for nombre in ("10-make-storytelling", "10-make-storytelling-update"):
            t = (self.SKILLS / nombre / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(t.startswith(f"---\nname: {nombre}\n"), nombre)
            self.assertIn("valores.json", t)
            self.assertIn("revisor-redactor", t)
        base = (self.SKILLS / "10-make-storytelling" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("te detienes", base)
        self.assertIn("datos generados para el proyecto", base)
        self.assertIn("validate_run.py", base)

    def test_el_update_explica_como_encontrar_los_hallazgos_afectados(self):
        t = (self.SKILLS / "10-make-storytelling-update" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("solo los hallazgos que citan ese KPI", t)
        self.assertTrue((self.SKILLS / "10-make-storytelling-update" / "references" / "dependencias.md").is_file())


class TestEjemplo(Base):
    def test_el_ejemplo_de_la_plantilla_valida_sin_incidencias(self):
        self.assertEqual(self.msgs(), [])

    def test_hay_un_hallazgo_por_objetivo_como_minimo(self):
        hall = ST.hallazgos((self.run / "secciones" / "4.md").read_text(encoding="utf-8"))
        self.assertEqual({h["objetivo"] for h in hall}, {"OE-01", "OE-02", "OE-03"})
        self.assertEqual([h["codigo"] for h in hall], ["HLZ-01", "HLZ-02", "HLZ-03", "HLZ-04", "HLZ-05"])

    def test_se_registra_y_deja_la_seccion_4_disponible(self):
        self.assertEqual(P.current_run(PASO, self.root), SF.RUN)
        estado = {x["seccion"]: x["estado"] for x in P.secciones(self.root)}
        self.assertEqual((estado["4"], estado["5"]), ("disponible", "pendiente"))


class TestSinValores(Base):
    def test_sin_valores_json_de_09_se_detiene(self):
        (self.run9 / "valores.json").unlink()
        self.assertIncidencia("no trae valores.json: primero hay que entregar los valores del dashboard")

    def test_sin_corrida_de_09(self):
        import shutil
        shutil.rmtree(self.run9)
        self.assertIncidencia("sin la corrida de 09-make-dashboard")


class TestObjetivos(Base):
    def test_objetivo_sin_hallazgo(self):
        t = (self.run / "secciones" / "4.md").read_text(encoding="utf-8")
        filas = [l for l in t.splitlines() if l.startswith("| HLZ-04")]
        self.assertEqual(len(filas), 1)
        self.edita(filas[0] + "\n", "")
        self.assertIncidencia("OE-03: el objetivo no tiene ningún hallazgo")

    def test_objetivo_que_no_es_del_brief(self):
        self.edita("| HLZ-01 | OE-01 |", "| HLZ-01 | OE-09 |")
        self.assertIncidencia("«OE-09» no es un objetivo específico del brief")

    def test_kpi_que_mide_otro_objetivo(self):
        self.edita("| HLZ-04 | OE-03 | KPI-03 |", "| HLZ-04 | OE-01 | KPI-03 |")
        self.assertIncidencia("KPI-03 mide OE-03 y el hallazgo cita OE-01")

    def test_kpi_que_no_es_del_modelo(self):
        self.edita("| HLZ-01 | OE-01 | KPI-01 |", "| HLZ-01 | OE-01 | KPI-99 |")
        self.assertIncidencia("«KPI-99» no es un KPI de modelo.json")


class TestCifras(Base):
    def test_valor_de_la_tabla_distinto_de_valores_json(self):
        self.edita("| 97,2 % | 98 % o más |", "| 98,5 % | 98 % o más |")
        self.assertIncidencia("el valor «98,5 %» no coincide con valores.json (97.2 para KPI-01)")

    def test_cifra_de_la_narrativa_que_no_esta_en_valores(self):
        self.edita("un margen neto de 8,4 %", "un margen neto de 11 %")
        self.assertIncidencia("la cifra «11 %» no coincide con ningún valor, meta ni diferencia de valores.json")

    def test_se_permite_la_diferencia_entre_valor_y_meta(self):
        self.assertEqual([m for m in self.msgs() if "cifra" in m], [])

    def test_una_diferencia_mal_calculada_no_pasa(self):
        self.edita("3,6 puntos porcentuales", "4,6 puntos porcentuales")
        self.assertIncidencia("la cifra «4,6 puntos porcentuales»")

    def test_cambia_un_valor_del_dashboard_y_se_detecta_en_el_hallazgo(self):
        v = self.valores9()
        v["kpis"][2]["valor"] = 5.1
        self.guarda_valores9(v)
        m = self.msgs()
        self.assertTrue(any("HLZ-04" in x and "6,9 %" in x and "5.1" in x for x in m), m)

    def test_cifras_con_unidad_solo_se_leen_con_pesos_o_porcentaje(self):
        c = ST.cifras("Son 3 páginas y 7 KPI; el margen fue 8,4 %, S/ 6,55 y 3,6 puntos porcentuales.")
        self.assertEqual([x[2] for x in c], [8.4, 6.55, 3.6])


class TestEstado(Base):
    def test_estado_que_no_concuerda_con_la_meta(self):
        self.edita("| 6,9 % | 3 % o menos | No cumple |", "| 6,9 % | 3 % o menos | Cumple |")
        self.assertIncidencia("el estado «Cumple» no concuerda con el valor 6.9 frente a la meta «3 % o menos»")

    def test_kpi_sin_meta_debe_ser_sin_meta(self):
        self.edita("| Pendiente | Sin meta |", "| Pendiente | Cumple |")
        self.assertIncidencia("KPI-05 no tiene meta, su estado debe ser «Sin meta»")

    def test_kpi_con_meta_no_puede_ser_sin_meta(self):
        self.edita("| 98 % o más | No cumple |", "| 98 % o más | Sin meta |")
        self.assertIncidencia("tiene meta «98 % o más» y el estado es «Sin meta»")

    def test_meta_distinta_de_la_de_2_5(self):
        self.edita("| 70 % o más | Cumple |", "| 65 % o más | Cumple |")
        self.assertIncidencia("la meta «65 % o más» no es la de modelo.json")

    def test_estado_fuera_de_la_lista(self):
        self.edita("| No cumple | pag-01 |", "| Parcial | pag-01 |")
        self.assertIncidencia("el estado debe ser uno de")


class TestCapturas(Base):
    def test_hallazgo_sin_captura(self):
        self.edita("| No cumple | pag-01 | Gerente general |", "| No cumple |  | Gerente general |")
        self.assertIncidencia("HLZ-01: no cita ninguna captura del dashboard")

    def test_captura_no_copiada_a_la_corrida(self):
        (self.run / "capturas" / "pag-03.png").unlink()
        self.assertIncidencia("cita la captura pag-03, que no está en capturas/ de esta corrida")

    def test_captura_de_otra_pagina(self):
        self.edita("| No cumple | pag-03 | Jefe de cocina |", "| No cumple | pag-01 | Jefe de cocina |")
        self.assertIncidencia("KPI-03 se ve en PAG-03 y el hallazgo cita pag-01")

    def test_captura_marcada_dos_veces(self):
        self.edita("**Qué muestra.** Como se ve en la", "<!-- captura: pag-02 -->\n\n**Qué muestra.** Como se ve en la")
        self.assertIncidencia("«<!-- captura: pag-02 -->» (está 2 veces)")

    def test_captura_citada_y_sin_marcar(self):
        self.edita("<!-- captura: pag-04 -->\n\n", "")
        self.assertIncidencia("(está 0 veces)")

    def test_captura_marcada_que_ningun_hallazgo_cita(self):
        self.edita("**Qué muestra.** Como se ve en la", "<!-- captura: pag-01 -->\n\n**Qué muestra.** Como se ve en la")
        self.assertIncidencia("«<!-- captura: pag-01 -->» (está 2 veces)")

    def test_la_copia_difiere_de_la_de_09(self):
        (self.run / "capturas" / "pag-02.png").write_bytes(DF.PNG + b"otra")
        self.assertIncidencia("difiere de la captura de 09-make-dashboard")


class TestDatosGenerados(Base):
    def test_sin_declaracion_de_datos_generados(self):
        self.edita("se basan en datos generados para el proyecto", "se basan en las mediciones del equipo")
        self.assertIncidencia("debe decir que los hallazgos se basan en «datos generados para el proyecto»")

    def test_con_datos_reales_no_se_exige(self):
        cfg = self.root / "project" / "config.yaml"
        cfg.write_text(cfg.read_text(encoding="utf-8").replace("modo_datos: generado", "modo_datos: real"), encoding="utf-8")
        self.edita("se basan en datos generados para el proyecto", "se basan en datos autorizados por la empresa")
        self.edita("; no describen el negocio real de una empresa", "")
        self.assertEqual([m for m in self.msgs() if "datos generados" in m], [])

    def test_afirmar_que_describe_el_negocio_real(self):
        self.edita("**Qué decisión apoya.** El gerente general puede confiar", "**Qué decisión apoya.** Esto describe el negocio real y el gerente general puede confiar")
        self.assertIncidencia("no afirmes que los hallazgos describen el negocio real")


class TestEstructura(Base):
    def test_encabezado_exacto(self):
        self.edita("## 4. Storytelling con datos", "## 4. Narrativa")
        self.assertIncidencia("la primera línea debe ser «## 4. Storytelling con datos»")

    def test_falta_el_contexto(self):
        self.edita("**Contexto.**", "**Antecedente.**")
        self.assertIncidencia("falta el «**Contexto.**»")

    def test_falta_prioridades(self):
        self.edita("**Prioridades.**", "**Orden.**")
        self.assertIncidencia("falta las «**Prioridades.**»")

    def test_hallazgo_sin_narrativa(self):
        self.edita("### HLZ-03.", "### HLZ-33.")
        m = self.msgs()
        self.assertTrue(any("HLZ-03: falta su narrativa" in x for x in m), m)
        self.assertTrue(any("HLZ-33: tiene narrativa y no está en la tabla" in x for x in m), m)

    def test_falta_que_decision_apoya(self):
        self.edita("**Qué decisión apoya.** El jefe de cocina", "**Otra cosa.** El jefe de cocina")
        self.assertIncidencia("HLZ-04: falta el «**Qué decisión apoya.**»")

    def test_usuario_que_no_es_del_brief(self):
        self.edita("| Jefe de cocina | Ajustar", "| Contador | Ajustar")
        self.assertIncidencia("«Contador» no es uno de los usuarios del brief")

    def test_hallazgo_sin_decision(self):
        self.edita("| Gerente general | Revisar los registros rechazados antes de fijar precios con diferencias pequeñas |", "| Gerente general |  |")
        self.assertIncidencia("HLZ-01: falta la decisión que apoya")

    def test_codigo_citado_sin_definir(self):
        self.edita("(HLZ-04)", "(HLZ-44)")
        self.assertIncidencia("código citado sin definir: HLZ-44")

    def test_tabla_sin_titulo(self):
        self.edita("Tabla 1: Hallazgos del dashboard\n\n", "")
        self.assertIncidencia("no tiene título «Tabla N: …»")

    def test_termino_no_permitido(self):
        self.edita("dejen de tomarse sin datos", "dejen de tomarse con datos simulados")
        self.assertIncidencia("término no permitido «simulados»")

    def test_comentario_que_no_es_una_captura(self):
        self.edita("**Hallazgos.**", "<!-- revisar -->\n\n**Hallazgos.**")
        self.assertIncidencia("comentario que no es una marca de captura")

    def test_falta_la_seccion(self):
        (self.run / "secciones" / "4.md").unlink()
        self.assertIncidencia("falta el archivo (sección 4 del informe)")


class TestMetasPendientes(Base):
    def test_un_kpi_sin_meta_no_puede_decir_si_es_alto_o_bajo_en_la_tabla(self):
        # el hallazgo de KPI-05 queda con «Sin meta» y no se le calcula estado
        hall = ST.hallazgos((self.run / "secciones" / "4.md").read_text(encoding="utf-8"))
        h5 = next(h for h in hall if h["kpi"] == "KPI-05")
        self.assertEqual((h5["meta"], h5["estado"]), ("Pendiente", "Sin meta"))


class TestInforme(Base):
    def test_el_informe_incluye_la_seccion_4_con_sus_capturas_numeradas(self):
        informe = self.root / "project" / "12-report" / "r1"
        informe.mkdir(parents=True)
        res = RP.construir(self.root, informe)
        txt = (informe / "informe.md").read_text(encoding="utf-8")
        self.assertIn("## 4. Storytelling con datos", txt)
        for pag in ("pag-01", "pag-02", "pag-03", "pag-04"):
            self.assertRegex(txt, rf"Archivo sugerido: \.\./\.\./10-storytelling/[^)]*capturas/{pag}\.png\)")
        self.assertNotIn("<!-- captura", txt)
        self.assertNotIn("{{figura:", txt)
        self.assertFalse([a for a in res["avisos"] if "captura" in a], res["avisos"])
        self.assertEqual(V.validate(informe), [])


class TestUpdate(Base):
    def test_cambiar_un_valor_actualiza_solo_los_hallazgos_que_lo_citan(self):
        v = self.valores9()
        v["kpis"][2]["valor"] = 5.1                   # KPI-03: 6,9 -> 5,1
        self.guarda_valores9(v)
        fork = Path(R.fork(PASO, ["Actualizar HLZ-04 con el nuevo valor de KPI-03"], root=self.root))
        self.edita("| HLZ-04 | OE-03 | KPI-03 | 6,9 % |", "| HLZ-04 | OE-03 | KPI-03 | 5,1 % |", run=fork)
        self.edita("una merma de 6,9 %, 3,9 puntos porcentuales", "una merma de 5,1 %, 2,1 puntos porcentuales", run=fork)
        self.assertEqual(self.msgs(fork), [])
        t0 = (self.run / "secciones" / "4.md").read_text(encoding="utf-8").splitlines()
        t1 = (fork / "secciones" / "4.md").read_text(encoding="utf-8").splitlines()
        cambiadas = [i for i, (a, b) in enumerate(zip(t0, t1)) if a != b]
        self.assertTrue(all("HLZ-04" in t1[i] or "5,1" in t1[i] for i in cambiadas), cambiadas)
        self.assertEqual(len(t0), len(t1))
        self.assertTrue(filecmp.cmp(self.run / "capturas" / "pag-01.png", fork / "capturas" / "pag-01.png", shallow=False))

    def test_el_valor_nuevo_sin_actualizar_el_texto_no_valida(self):
        v = self.valores9()
        v["kpis"][2]["valor"] = 5.1
        self.guarda_valores9(v)
        fork = Path(R.fork(PASO, ["Sin cambios"], root=self.root))
        self.assertTrue(any("HLZ-04" in x and "5.1" in x for x in self.msgs(fork)))


if __name__ == "__main__":
    unittest.main()
