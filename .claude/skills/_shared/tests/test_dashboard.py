"""Validador del paso 09-make-dashboard (sección 3.2, anexos C y D, valores.json y capturas) y el DAX propuesto desde modelo.json."""
import filecmp
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dashboard_dax as DAX  # noqa: E402
import dashboard_fixtures as DF  # noqa: E402
import projectcfg as P  # noqa: E402
import runs as R  # noqa: E402
import validate_run as V  # noqa: E402

PASO = DF.PASO
MODELO_PATH = DF.F.COMMON / "07-data-model-kpi" / "models" / "dm-3-modelo-json.md"


def modelo_ejemplo():
    return json.loads(DF.F.ejemplo_json(MODELO_PATH))


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run, self.runs = DF.crear(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def msgs(self, run=None):
        return [f"{f}: {m}" for f, m in V.validate(run or self.run)]

    def edita(self, rel, a, b, run=None):
        f = (run or self.run) / rel
        t = f.read_text(encoding="utf-8")
        assert a in t, a
        f.write_text(t.replace(a, b, 1), encoding="utf-8")

    def s32(self, a, b, run=None):
        self.edita("secciones/3.2.md", a, b, run)

    def valores(self, run=None):
        return json.loads(((run or self.run) / "valores.json").read_text(encoding="utf-8"))

    def guarda_valores(self, v, run=None):
        ((run or self.run) / "valores.json").write_text(json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")

    def assertIncidencia(self, texto):
        m = self.msgs()
        self.assertTrue(any(texto in x for x in m), m)


class TestPlaybook(unittest.TestCase):
    COMMON = HERE.parents[2] / "common" / "09-dashboard"

    def test_guia_y_plantillas_con_las_cinco_partes(self):
        self.assertTrue((self.COMMON / "guia.md").is_file())
        plantillas = sorted((self.COMMON / "models").glob("ds-*.md"))
        self.assertEqual([p.name for p in plantillas], ["ds-1-paginas.md", "ds-2-medidas.md", "ds-3-especificacion.md", "ds-4-valores-json.md", "ds-5-paginas-json.md"])
        self.assertTrue((self.COMMON / "models" / "README.md").is_file())
        for p in plantillas:
            t = p.read_text(encoding="utf-8")
            self.assertIn("| **Entregable** |", t, p.name)
            for parte in ("## Instrucciones para el agente", "## Formato", "## Ejemplo", "## Checklist"):
                self.assertIn(parte, t, f"{p.name}: {parte}")

    def test_la_guia_dice_que_el_equipo_construye_y_la_skill_no_inventa(self):
        t = (self.COMMON / "guia.md").read_text(encoding="utf-8")
        self.assertIn("no abre Power BI", t)
        self.assertIn("Nunca inventa un valor", t)
        self.assertIn("07-make-data-model-kpi-update", t)


class TestEjemplo(Base):
    def test_ejemplo_sin_incidencias(self):
        self.assertEqual(self.msgs(), [])

    def test_registrado_en_el_config(self):
        self.assertEqual(P.current_run(PASO, self.root), DF.RUN)


class TestEstructura(Base):
    def test_sin_3_2(self):
        (self.run / "secciones" / "3.2.md").unlink()
        self.assertIncidencia("falta el archivo (sección 3.2 del informe)")

    def test_encabezado_exacto(self):
        self.s32("## 3.2. Construcción del dashboard en Power BI", "## 3.2. El dashboard")
        self.assertIncidencia("la primera línea debe ser «## 3.2. Construcción del dashboard en Power BI»")

    def test_las_marcas_de_captura_no_son_comentarios(self):
        self.assertFalse(any("comentario" in m for m in self.msgs()))
        self.s32("<!-- captura: pag-01 -->", "<!-- captura: pag-01 -->\n\n<!-- nota del equipo -->")
        self.assertIncidencia("comentario que no es una marca de captura")

    def test_tabla_sin_titulo(self):
        self.s32("Tabla 1: Páginas del dashboard\n\n", "")
        self.assertIncidencia("no tiene título «Tabla N: …»")

    def test_codigo_pag_citado_sin_definir(self):
        self.s32("**Lectura del dashboard.** ", "**Lectura del dashboard.** La página PAG-09 muestra más. ")
        self.assertIncidencia("código citado sin definir: PAG-09")

    def test_lectura_y_metas_pendientes(self):
        self.s32("**Lectura del dashboard.**", "**Resumen.**")
        self.assertIncidencia("falta la «**Lectura del dashboard.**»")

    def test_meta_pendiente_sin_parrafo(self):
        self.s32("**Metas pendientes.**", "**Otras.**")
        self.assertIncidencia("falta la «**Metas pendientes.**» con KPI-05")


class TestPaginas(Base):
    def test_kpi_sin_pagina(self):
        self.s32("| Mes | KPI-05 |", "| Mes | KPI-04 |")
        self.assertIncidencia("KPI-05: el KPI no aparece en ninguna página")

    def test_pagina_sin_usuario(self):
        self.s32("| Gerente general | Tarjeta del porcentaje de registros válidos", "|  | Tarjeta del porcentaje de registros válidos")
        self.assertIncidencia("PAG-01: no indica qué usuario del brief la consulta")

    def test_usuario_que_no_es_del_brief(self):
        self.s32("| Jefe de cocina |", "| Contador |")
        self.assertIncidencia("PAG-03: el usuario «Contador» no es uno de los del brief")

    def test_pagina_sin_visualizaciones_ni_filtros(self):
        self.s32("| Mes, turno y local | KPI-03 |", "|  | KPI-03 |")
        self.assertIncidencia("PAG-03: falta sus filtros")

    def test_pagina_con_un_kpi_que_no_existe(self):
        self.s32("| KPI-02; KPI-04 |", "| KPI-02; KPI-09 |")
        self.assertIncidencia("PAG-02: cita KPI-09, que no es un KPI de modelo.json")


class TestCapturas(Base):
    def test_captura_sin_entregar(self):
        (self.run / "capturas" / "pag-03.png").unlink()
        self.assertIncidencia("falta la captura de la página PAG-03")

    def test_valor_que_muestra_una_pagina_sin_captura(self):
        (self.run / "capturas" / "pag-03.png").unlink()
        self.assertIncidencia("KPI-03: cita un valor que muestra PAG-03 y falta su captura")

    def test_captura_sin_marcar_o_repetida(self):
        self.s32("<!-- captura: pag-02 -->\n\n", "")
        self.assertIncidencia("debe marcar una sola vez la captura de la página con la línea «<!-- captura: pag-02 -->»")

    def test_captura_de_una_pagina_que_no_existe(self):
        self.s32("<!-- captura: pag-04 -->", "<!-- captura: pag-04 -->\n\n<!-- captura: pag-08 -->")
        self.assertIncidencia("la captura «pag-08» no corresponde a ninguna página")

    def test_captura_vacia_no_cuenta(self):
        (self.run / "capturas" / "pag-01.png").write_bytes(b"")
        self.assertIncidencia("falta la captura de la página PAG-01")


class TestValores(Base):
    def test_sin_valores_json(self):
        (self.run / "valores.json").unlink()
        self.assertIncidencia("valores.json: falta el archivo")

    def test_un_kpi_sin_valor(self):
        v = self.valores()
        v["kpis"] = [k for k in v["kpis"] if k["codigo"] != "KPI-03"]
        self.guarda_valores(v)
        self.assertIncidencia("KPI-03: falta su valor real")
        self.assertIncidencia("KPI-03: el valor real de 3.2 no está en valores.json")

    def test_valor_citado_distinto_de_valores_json(self):
        self.s32("| 97,2 % |", "| 92,7 % |")
        self.assertIncidencia("KPI-01: el valor real citado «92,7 %» no coincide con valores.json (97.2)")

    def test_el_valor_se_compara_con_los_decimales_mostrados(self):
        v = self.valores()
        v["kpis"][0]["valor"] = 97.24
        self.guarda_valores(v)
        self.assertEqual(self.msgs(), [])

    def test_estado_que_no_concuerda_con_la_meta(self):
        self.s32("| 71,0 % | 70 % o más | Cumple |", "| 71,0 % | 70 % o más | No cumple |")
        self.assertIncidencia("KPI-04: el estado «No cumple» no concuerda con el valor 71.0 frente a la meta «70 % o más»")

    def test_menos_es_mejor_en_la_merma(self):
        v = self.valores()
        v["kpis"][2]["valor"] = 2.5
        self.guarda_valores(v)
        self.s32("| 6,9 % | 3 % o menos | No cumple |", "| 2,5 % | 3 % o menos | Cumple |")
        self.assertEqual(self.msgs(), [])

    def test_estado_invalido(self):
        self.s32("| No cumple | PAG-01 |", "| Regular | PAG-01 |")
        self.assertIncidencia("KPI-01: el estado debe ser uno de Cumple, No cumple, Sin meta")

    def test_kpi_sin_meta_debe_ser_sin_meta(self):
        self.s32("| Pendiente | Sin meta | PAG-04 |", "| Pendiente | Cumple | PAG-04 |")
        self.assertIncidencia("KPI-05: no tiene meta, su estado debe ser «Sin meta»")

    def test_meta_distinta_de_modelo_json(self):
        self.s32("| 98 % o más |", "| 95 % o más |")
        self.assertIncidencia("KPI-01: la meta «95 % o más» no es la de modelo.json («98 % o más»)")

    def test_meta_de_valores_json_con_2_5_pendiente(self):
        v = self.valores()
        v["kpis"][4]["meta"] = 7
        self.guarda_valores(v)
        self.assertIncidencia("KPI-05: valores.json trae una meta y 2.5 sigue «Pendiente»: ciérrala con 07-make-data-model-kpi-update")

    def test_meta_de_2_5_ausente_en_valores_json(self):
        v = self.valores()
        v["kpis"][0]["meta"] = None
        self.guarda_valores(v)
        self.assertIncidencia("KPI-01: la meta de 2.5 («98 % o más») no está en valores.json")

    def test_schema_y_unidad(self):
        v = self.valores()
        v["schema"] = 2
        v["kpis"][1]["unidad"] = ""
        self.guarda_valores(v)
        self.assertIncidencia("schema debe ser 1")
        self.assertIncidencia("KPI-02: faltan la unidad o el periodo")

    def test_json_invalido(self):
        (self.run / "valores.json").write_text("{no", encoding="utf-8")
        self.assertIncidencia("valores.json: no es un JSON válido")

    def test_pagina_que_no_lista_el_kpi(self):
        self.s32("| 12 % o más en el margen neto global | No cumple | PAG-02 |", "| 12 % o más en el margen neto global | No cumple | PAG-01 |")
        self.assertIncidencia("KPI-02: la página PAG-01 no lista este KPI")


class TestMedidas(Base):
    def test_campo_fuera_del_modelo(self):
        self.edita("anexos/C.md", "SUM(fPedidos[venta_bruta])", "SUM(fPedidos[margen])")
        self.assertIncidencia("la medida «Suma de venta_bruta» cita el campo «fPedidos[margen]», que no está en modelo.json")

    def test_tabla_fuera_del_modelo(self):
        self.edita("anexos/C.md", "SUM(fPedidos[venta_bruta])", "SUM(fVentas[venta_bruta])")
        self.assertIncidencia("cita la tabla «fVentas», que no está en modelo.json")

    def test_medida_citada_sin_definir(self):
        self.edita("anexos/C.md", "[Suma de pollos_merma], [Suma de pollos_preparados]", "[Suma de pollos_perdidos], [Suma de pollos_preparados]")
        self.assertIncidencia("cita la medida «[Suma de pollos_perdidos]», que no está definida en el anexo")

    def test_kpi_sin_su_medida(self):
        self.edita("anexos/C.md", "### MED-10. % Merma", "### MED-10. Merma turno")
        self.edita("anexos/C.md", "| MED-10 | % Merma |", "| MED-10 | Merma turno |")
        self.assertIncidencia("KPI-03: el anexo no define su medida «% Merma»")

    def test_marca_revisar_sin_resolver(self):
        self.edita("anexos/C.md", "DIVIDE([Suma de registro_valido], COUNTROWS(fPedidos))", "/* revisar: denominador */ DIVIDE([Suma de registro_valido], [Suma de registro_valido])")
        self.assertIncidencia("el DAX conserva una marca «revisar» sin resolver")

    def test_medida_en_tabla_sin_dax_y_al_reves(self):
        self.edita("anexos/C.md", "| MED-12 | Precio pollo vivo | Medida | KPI-05 | fPrecioInsumo[precio_kg] |\n", "")
        self.assertIncidencia("MED-12: tiene su DAX y falta en la tabla de medidas")

    def test_encabezado_y_titulo_del_anexo(self):
        self.edita("anexos/C.md", "# Anexo C: Medidas y cálculos del dashboard", "# Anexo C: Medidas")
        self.assertIncidencia("anexos/C.md: la primera línea debe ser «# Anexo C: Medidas y cálculos del dashboard»")
        self.edita("anexos/C.md", "Tabla 1: Medidas del dashboard\n\n", "")
        self.assertIncidencia("anexos/C.md: la tabla de la línea")

    def test_falta_el_anexo_c(self):
        (self.run / "anexos" / "C.md").unlink()
        self.assertIncidencia("anexos/C.md: falta el archivo")


class TestAnexoD(Base):
    def test_pagina_sin_descripcion(self):
        t = (self.run / "anexos" / "D.md").read_text(encoding="utf-8")
        i = t.index("### PAG-03.")
        j = t.index("### PAG-04.")
        (self.run / "anexos" / "D.md").write_text(t[:i] + t[j:], encoding="utf-8")
        self.assertIncidencia("PAG-03: la página no tiene su «### PAG-03. Nombre» con su descripción")

    def test_descripcion_vacia(self):
        self.edita("anexos/D.md", "**Descripción.** Sigue el precio por kilogramo del pollo vivo semana a semana. Apoya la decisión de anticipar compras ante una subida. La captura de esta página está en la sección 3.2.", "**Descripción.**")
        self.assertIncidencia("PAG-04: falta la «**Descripción.**» de la página")

    def test_pagina_que_3_2_no_tiene(self):
        with open(self.run / "anexos" / "D.md", "a", encoding="utf-8") as f:
            f.write("\n### PAG-07. Extra\n\n**Descripción.** Una página más.\n")
        self.assertIncidencia("PAG-07: describe una página que no está en 3.2")

    def test_no_repite_la_marca_de_captura(self):
        with open(self.run / "anexos" / "D.md", "a", encoding="utf-8") as f:
            f.write("\n<!-- captura: pag-01 -->\n")
        self.assertIncidencia("repite la marca «<!-- captura: … -->»")

    def test_falta_el_anexo_d(self):
        (self.run / "anexos" / "D.md").unlink()
        self.assertIncidencia("anexos/D.md: falta el archivo")


class TestFuentes(Base):
    def test_sin_modelo_json(self):
        (self.runs["07-make-data-model-kpi"] / "modelo.json").unlink()
        self.assertIncidencia("sin el modelo.json de 07-make-data-model-kpi")

    def test_sin_corrida_del_modelo(self):
        cfg = self.root / "project" / "config.yaml"
        t = cfg.read_text(encoding="utf-8")
        cfg.write_text(t.replace(f"run: {DF.F.RUNS['07-make-data-model-kpi']}", "run: null"), encoding="utf-8")
        self.assertIncidencia("sin la corrida de 07-make-data-model-kpi")


class TestDax(unittest.TestCase):
    def setUp(self):
        self.modelo = modelo_ejemplo()

    def test_una_medida_base_por_campo_usado_con_su_agregacion(self):
        base = {b["nombre"]: b["dax"] for b in DAX.medidas_base(self.modelo)}
        self.assertEqual(base["Suma de venta_bruta"], "SUM(fPedidos[venta_bruta])")
        self.assertEqual(base["Promedio de precio_kg"], "AVERAGE(fPrecioInsumo[precio_kg])")
        self.assertNotIn("Suma de cantidad", base)
        self.assertEqual(len(base), 7)

    def test_margen_neto_resta_comision_y_costo(self):
        k = next(k for k in self.modelo["kpis"] if k["codigo"] == "KPI-02")
        m = DAX.medida_kpi(k, self.modelo)
        self.assertEqual(m["nombre"], "Margen neto %")
        self.assertIn("DIVIDE([Suma de venta_bruta] - [Suma de comision] - [Suma de costo_estimado], [Suma de venta_bruta])", m["dax"])
        self.assertEqual(m["revisar"], [])

    def test_merma_es_una_razon_de_dos_campos(self):
        k = next(k for k in self.modelo["kpis"] if k["codigo"] == "KPI-03")
        self.assertIn("DIVIDE([Suma de pollos_merma], [Suma de pollos_preparados])", DAX.medida_kpi(k, self.modelo)["dax"])

    def test_promedio_se_apoya_en_la_medida_base(self):
        k = next(k for k in self.modelo["kpis"] if k["codigo"] == "KPI-05")
        self.assertIn("[Promedio de precio_kg]", DAX.medida_kpi(k, self.modelo)["dax"])

    def test_lo_que_no_puede_relacionar_queda_para_revisar(self):
        for codigo in ("KPI-01", "KPI-04"):
            k = next(k for k in self.modelo["kpis"] if k["codigo"] == codigo)
            m = DAX.medida_kpi(k, self.modelo)
            self.assertTrue(m["revisar"], codigo)
            self.assertIn("revisar", m["dax"])
        k = {"codigo": "KPI-X", "medida": "X", "formula": "Pollos regalados entre pollos preparados", "origen": ["fProduccion.pollos_preparados"]}
        self.assertIn("Pollos regalados", DAX.medida_kpi(k, self.modelo)["revisar"])

    def test_proponer_numera_primero_las_base_y_luego_los_kpi(self):
        p = DAX.proponer(self.modelo)
        self.assertEqual([m["codigo"] for m in p][:2], ["MED-01", "MED-02"])
        self.assertEqual([m["kpi"] for m in p if m["kpi"]], [k["codigo"] for k in self.modelo["kpis"]])
        self.assertEqual(len(p), 12)

    def test_solo_cita_campos_del_modelo(self):
        for m in DAX.proponer(self.modelo):
            self.assertEqual([x for x in DAX.problemas_dax(m["dax"], self.modelo, [p["nombre"] for p in DAX.proponer(self.modelo)]) if "no está en modelo.json" in x], [], m["codigo"])

    def test_problemas_dax(self):
        self.assertEqual(DAX.problemas_dax("SUM(fPedidos[venta_bruta])", self.modelo), [])
        self.assertTrue(DAX.problemas_dax("SUM(fPedidos[margen])", self.modelo))
        self.assertTrue(DAX.problemas_dax("SUM('fVentas'[venta_bruta])", self.modelo))
        self.assertTrue(DAX.problemas_dax("DIVIDE([A], [B])", self.modelo, ["A"]))
        self.assertEqual(DAX.problemas_dax("CALCULATE([A], dCanal[tipo_canal] = \"Propio\")", self.modelo, ["A"]), [])

    def test_cli(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "modelo.json"
            ruta.write_text(json.dumps(self.modelo), encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(DAX.main([str(ruta)]), 0)
        self.assertIn("MED-09 · Margen neto % (KPI-02)", buf.getvalue())
        self.assertIn("¡revisar!", buf.getvalue())


class TestUpdate(Base):
    def test_reemplazar_una_captura_deja_identico_el_anexo_c(self):
        fork = Path(R.fork(PASO, ["Reemplazar la captura de PAG-03"], root=self.root))
        (fork / "capturas" / "pag-03.png").write_bytes(DF.PNG + b"nueva")
        self.edita("secciones/3.2.md", "una merma de más del doble de la meta", "una merma de más del doble de la meta fijada", run=fork)
        self.assertEqual(self.msgs(fork), [])
        self.assertTrue(filecmp.cmp(self.run / "anexos" / "C.md", fork / "anexos" / "C.md", shallow=False))
        self.assertTrue(filecmp.cmp(self.run / "anexos" / "D.md", fork / "anexos" / "D.md", shallow=False))
        self.assertTrue(filecmp.cmp(self.run / "valores.json", fork / "valores.json", shallow=False))
        self.assertFalse(filecmp.cmp(self.run / "capturas" / "pag-03.png", fork / "capturas" / "pag-03.png", shallow=False))
        self.assertTrue(filecmp.cmp(self.run / "capturas" / "pag-01.png", fork / "capturas" / "pag-01.png", shallow=False))

    def test_meta_en_valores_json_sin_cerrar_2_5_no_valida_en_el_fork(self):
        fork = Path(R.fork(PASO, ["Cerrar la meta de KPI-05"], root=self.root))
        v = self.valores(fork)
        v["kpis"][4]["meta"] = 7
        self.guarda_valores(v, fork)
        # sin cerrar la meta en 2.5 (07-make-data-model-kpi-update) el fork no valida
        self.assertTrue(any("ciérrala con 07-make-data-model-kpi-update" in m for m in self.msgs(fork)))


if __name__ == "__main__":
    unittest.main()
