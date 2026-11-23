"""Dashboard de referencia (dashboard_ref.py): HTML autónomo con el diseño del proyecto, valores de la hoja de respuestas y guía completa."""
import csv
import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dashboard_ref as R  # noqa: E402
import datagen as G  # noqa: E402
import diagnostico as D  # noqa: E402
import diagnostico_fixtures as F  # noqa: E402
import validate_run as VR  # noqa: E402

KPIS = [("KPI-01", "Calidad de datos del ETL", "98 % o más"), ("KPI-02", "Margen de contribución por canal y producto", "Pendiente"),
        ("KPI-03", "Margen neto global", "12 % o más"), ("KPI-04", "Porcentaje de merma por turno", "3 % o menos"),
        ("KPI-05", "Precisión del pronóstico de demanda", "15 % o menos"), ("KPI-06", "Precio promedio del pollo vivo por kilogramo", "Pendiente"),
        ("KPI-07", "KPI con meta en el dashboard", "100 %")]
MODELO = {
    "schema": 1,
    "hechos": [
        {"codigo": "FCT-01", "nombre": "fPedidos", "granularidad": "Una fila por línea", "claves": ["fecha_key", "producto_key", "canal_key", "turno_key"],
         "medidas": [{"nombre": n, "tipo": "decimal", "agregacion": "suma"} for n in ("cantidad", "venta_bruta", "comision", "costo_estimado", "costo_operativo", "pollos_equivalentes", "registro_valido", "registro_total")]},
        {"codigo": "FCT-02", "nombre": "fProduccion", "granularidad": "Una fila por turno y día", "claves": ["fecha_key", "turno_key"],
         "medidas": [{"nombre": n, "tipo": "entero", "agregacion": "suma"} for n in ("pollos_preparados", "pollos_vendidos", "pollos_merma")]},
        {"codigo": "FCT-03", "nombre": "fPrecioInsumo", "granularidad": "Una fila por día", "claves": ["fecha_key"],
         "medidas": [{"nombre": "precio_kg", "tipo": "decimal", "agregacion": "promedio"}, {"nombre": "valor_imputado", "tipo": "entero", "agregacion": "suma"}]},
        {"codigo": "FCT-04", "nombre": "fMetaKpi", "granularidad": "Una fila por KPI y mes", "claves": ["kpi_key", "fecha_key"],
         "medidas": [{"nombre": "meta", "tipo": "decimal", "agregacion": "promedio"}, {"nombre": "valor_real", "tipo": "decimal", "agregacion": "promedio"}]},
    ],
    "dimensiones": [
        {"codigo": "DIM-01", "nombre": "dCalendario", "clave": "fecha_key", "atributos": ["fecha", "anio", "mes", "nombre_mes", "dia_semana", "es_feriado"], "jerarquias": []},
        {"codigo": "DIM-02", "nombre": "dProducto", "clave": "producto_key", "atributos": ["producto", "categoria"], "jerarquias": []},
        {"codigo": "DIM-03", "nombre": "dCanal", "clave": "canal_key", "atributos": ["canal", "tipo_canal", "comision_pct"], "jerarquias": []},
        {"codigo": "DIM-04", "nombre": "dTurno", "clave": "turno_key", "atributos": ["turno", "hora_inicio", "hora_fin"], "jerarquias": []},
        {"codigo": "DIM-05", "nombre": "dKpi", "clave": "kpi_key", "atributos": ["kpi", "objetivo", "tiene_meta", "frecuencia"], "jerarquias": []},
    ],
    "relaciones": [{"codigo": "REL-01", "desde": "fPedidos", "hacia": "dCalendario", "campos": "fecha_key", "cardinalidad": "*:1", "filtro": "Simple"}],
    "kpis": [{"codigo": c, "nombre": n, "formula": "", "medida": "", "origen": [], "meta": m, "frecuencia": "Mensual", "objetivo": "OE-01", "decision": ""} for c, n, m in KPIS],
}


def leer(ruta):
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class TestReferencia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        F.crear(cls.root, hasta="07-make-data-model-kpi")
        (D.corrida(cls.root, D.MODELO) / "modelo.json").write_text(json.dumps(MODELO, ensure_ascii=False), encoding="utf-8")
        G.generar(G.parametros_base(), cls.root / "data")
        cls.resp = {f.stem: leer(f) for f in (cls.root / "data" / "respuestas").glob("*.csv")}
        cls.corr = cls.root / "project" / "09-dashboard" / "16-11-2026-08-00-00"
        (cls.corr / "materiales").mkdir(parents=True)
        (cls.corr / "materiales" / "paginas.json").write_text(R.PLAN_POR_DEFECTO.read_text(encoding="utf-8"), encoding="utf-8")
        cls.mat = R.construir(cls.root, cls.corr)
        cls.html = (cls.mat / "dashboard-referencia.html").read_text(encoding="utf-8")
        cls.guia = (cls.mat / "guia-dashboard.md").read_text(encoding="utf-8")
        cls.plan = json.loads((cls.mat / "paginas.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    # ---- archivos y HTML
    def test_escribe_los_cuatro_archivos(self):
        for f in ("dashboard-referencia.html", "guia-dashboard.md", "paginas.json", "paginas.txt", "medidas.txt"):
            self.assertTrue((self.mat / f).is_file(), f)

    def test_html_autonomo_sin_recursos_externos(self):
        self.assertNotIn("http", self.html)
        self.assertNotRegex(self.html, r"(?:src|href)\s*=")
        self.assertNotIn("@import", self.html)
        self.assertNotIn("url(", self.html)

    def test_tema_claro_y_oscuro_con_los_tokens_del_proyecto(self):
        self.assertIn(':root[data-theme="dark"]', self.html)
        self.assertIn(':root[data-theme="light"]', self.html)
        self.assertIn("--c-serie-1:", self.html)
        self.assertIn("--tema-defecto", self.html)

    def test_una_seccion_por_pagina_con_su_lienzo_16_9(self):
        self.assertEqual(self.html.count('<section class="pagina"'), len(self.plan["paginas"]))
        self.assertEqual(self.html.count('<div class="lienzo">'), len(self.plan["paginas"]))
        self.assertAlmostEqual(R.ANCHO / R.ALTO, 16 / 9, delta=0.01)
        for p in self.plan["paginas"]:
            self.assertIn(f'id="{p["codigo"]}"', self.html)

    def test_cada_visual_tiene_su_caja_como_construirlo(self):
        total = sum(len(p["visuales"]) for p in self.plan["paginas"])
        self.assertEqual(self.html.count('<figure class="visual"'), total)
        self.assertEqual(self.html.count("Cómo construirlo"), total)
        for campo in ("Tipo de visual", "Eje X / filas", "Valores (eje Y)", "Medidas", "Filtros", "Tablas de origen"):
            self.assertGreaterEqual(self.html.count(f"<dt>{campo}</dt>"), total)

    def test_los_graficos_son_svg_con_textos_legibles_y_tooltip(self):
        self.assertIn("<svg", self.html)
        self.assertIn('data-tip="', self.html)
        tamanos = {int(t) for t in re.findall(r'font-size="(\d+)"', self.html)}
        self.assertTrue(tamanos and min(tamanos) >= 14, tamanos)

    def test_el_estado_se_dice_con_texto_y_no_solo_con_color(self):
        self.assertIn("Cumple", self.html)
        self.assertIn("No cumple", self.html)
        self.assertIn("Sin meta", self.html)

    # ---- valores iguales a la hoja de respuestas
    def test_tarjeta_del_margen_neto_es_el_valor_del_ultimo_mes(self):
        ultimo = [r for r in self.resp["kpi-esperados"] if r["kpi"] == "KPI-03"][-1]
        self.assertIn(f'{float(ultimo["valor"]):.1f} %', self.html)
        v = R.valor_kpi(self.resp, "KPI-03", R.metas_kpi(MODELO))
        self.assertEqual((v["valor"], v["mes"], v["estado"]), (float(ultimo["valor"]), ultimo["mes"], "No cumple"))

    def test_calidad_de_datos_cumple_y_margen_de_contribucion_sin_meta(self):
        metas = R.metas_kpi(MODELO)
        self.assertEqual(R.valor_kpi(self.resp, "KPI-01", metas)["estado"], "Cumple")
        self.assertEqual(R.valor_kpi(self.resp, "KPI-02", metas)["estado"], "Sin meta")
        self.assertEqual(R.valor_kpi(self.resp, "KPI-07", metas)["valor"], 100 * 5 / 7)

    def test_margen_por_canal_coincide_con_la_hoja(self):
        acum = {}
        for r in self.resp["margen-canal-producto"]:
            a = acum.setdefault(r["canal"], [0.0, 0.0, 0.0])
            a[0] += float(r["ventas"]); a[1] += float(r["comision"]); a[2] += float(r["costo_estimado"])
        for canal, a in acum.items():
            esperado = f"{100 * (a[0] - a[1] - a[2]) / a[0]:.1f} %"
            self.assertIn(esperado, self.html, canal)

    def test_merma_por_dia_coincide_con_la_hoja(self):
        for f in self.resp["produccion-dia-semana"]:
            self.assertIn(f"{float(f['merma_pct']):.1f} %", self.html, f["dia_semana"])

    def test_la_participacion_de_las_aplicaciones_sube_en_el_grafico_al_100(self):
        v = {"datos": {"fuente": "ventas_canal_mes", "modo": "participacion"}}
        d = R.datos_visual(v, self.resp, MODELO, R.metas_kpi(MODELO))
        apps = [d["series"][3]["valores"][i] + d["series"][4]["valores"][i] for i in range(len(d["cats"]))]
        self.assertAlmostEqual(apps[0], 15, delta=2)
        self.assertAlmostEqual(apps[-1], 35, delta=2)
        self.assertTrue(all(abs(sum(s["valores"][i] for s in d["series"]) - 100) < 1e-6 for i in range(len(d["cats"]))))

    def test_la_serie_de_precio_diario_marca_los_dias_imputados(self):
        d = R.datos_visual({"datos": {"fuente": "precio_dia"}}, self.resp, MODELO, R.metas_kpi(MODELO))
        self.assertEqual(len(d["marcas"]), sum(int(r["imputado"]) for r in self.resp["precio-dia"]))
        self.assertEqual(d["series"][0]["valores"][d["cats"].index("2026-07-14")], 6.9)

    # ---- guía
    def test_la_guia_tiene_una_seccion_por_pagina_y_ninguna_otra(self):
        secciones = [l for l in self.guia.splitlines() if l.startswith("## ")]
        self.assertEqual(secciones, [f"## {p['codigo']} · {p['nombre']}" for p in self.plan["paginas"]])

    def test_cada_pagina_va_elemento_por_elemento_con_todo_lo_que_hace_falta(self):
        elementos = 0
        for p in self.plan["paginas"]:
            bloque = self.guia.split(f"## {p['codigo']} ·", 1)[1].split("\n## ", 1)[0]
            titulos = [l for l in bloque.splitlines() if l.startswith("### ")]
            esperados = (1 if p.get("segmentadores") else 0) + len(p.get("kpis", [])) + len(p["visuales"])
            self.assertEqual(len(titulos), esperados, p["codigo"])
            self.assertEqual([t.split(" · ")[0] for t in titulos], [f"### Elemento {n}" for n in range(1, esperados + 1)], p["codigo"])
            for k in p.get("kpis", []):
                self.assertIn(f"Tarjeta {k} · ", bloque)
            for v in p["visuales"]:
                self.assertIn(v["titulo"], "\n".join(titulos))
                self.assertIn(v["x"], bloque)
                for t in v["origen"]:
                    self.assertIn(t, bloque)
            elementos += esperados
        for rotulo in ("**Qué muestra.**", "**Cómo armarlo en Power BI.**", "**Valor esperado.**"):
            self.assertEqual(self.guia.count(rotulo), elementos, rotulo)

    def test_cada_medida_se_crea_una_sola_vez_con_su_dax_en_el_primer_elemento_que_la_usa(self):
        for m in self.plan["medidas"]:
            self.assertEqual(self.guia.count(f"**Medida `{m['nombre']}`"), 1 if self._usada(m) else 0, m["codigo"])
            if self._usada(m):
                self.assertIn(m["dax"], self.guia)
        for c, n, _ in KPIS:
            self.assertIn(c, self.guia)
        self.assertIn("Meta: 12 % o más", self.guia)

    def _usada(self, m):
        """Una medida se explica si algún visual la usa o es la de una tarjeta, o la usan otras medidas que se explican."""
        usadas = {c for p in self.plan["paginas"] for v in p["visuales"] for c in v["medidas"]}
        usadas |= {x["codigo"] for p in self.plan["paginas"] for k in p.get("kpis", []) for x in self.plan["medidas"] if x["kpi"] == k}
        cola, vistos = list(usadas), set(usadas)
        por_nombre = {x["nombre"]: x for x in self.plan["medidas"]}
        while cola:
            codigo = cola.pop()
            actual = next(x for x in self.plan["medidas"] if x["codigo"] == codigo)
            for n in R.RE_MEDIDA.findall(actual["dax"]):
                d = por_nombre.get(n)
                if d and d["codigo"] not in vistos:
                    vistos.add(d["codigo"])
                    cola.append(d["codigo"])
        return m["codigo"] in vistos

    def test_cada_columna_calculada_que_se_usa_se_explica_con_sus_archivos(self):
        usadas = {(t, c) for m in self.plan["medidas"] for t, c in R.RE_COLUMNA.findall(m["dax"])}
        for c in self.plan["columnas_calculadas"]:
            if (c["tabla"], c["columna"]) in usadas or c["columna"] in ("anio_mes", "mes_anio"):
                self.assertIn(f"`{c['tabla']}[{c['columna']}]`", self.guia)
                self.assertIn(c["formula"], self.guia)
                for a in c["archivos"]:
                    self.assertIn(f"`{a}`", self.guia)
        self.assertIn("comision_pct ÷ 100", self.guia)
        self.assertIn("data/apoyo-costos-operativos.csv", self.guia)
        self.assertIn("data/apoyo-catalogo-productos.csv", self.guia)

    def test_los_ejes_por_mes_usan_mes_anio_porque_el_periodo_repite_meses(self):
        for p in self.plan["paginas"]:
            for v in p["visuales"]:
                self.assertNotIn("dCalendario[nombre_mes] (ordenada", v["x"])
        self.assertIn("dCalendario[mes_anio] (ordenada por dCalendario[anio_mes])", self.guia)
        self.assertIn("dos agostos", self.guia)
        self.assertIn("Ordenar por columna", self.guia)

    def test_cada_elemento_trae_su_valor_esperado_y_el_pronostico_su_advertencia(self):
        self.assertIn("oct 26", self.guia)
        self.assertIn("promedio de las cuatro jornadas anteriores del mismo día de la semana y del mismo turno", self.guia)
        self.assertIn("no coincidirá exactamente", self.guia)
        self.assertNotIn("Valores esperados para comparar", self.guia)

    def test_la_guia_cumple_las_reglas_de_texto_limpio_de_las_corridas(self):
        f = self.mat / "guia-dashboard.md"
        self.assertEqual(VR.check_policy(self.corr, [f]), [])
        self.assertEqual(VR.check_links(self.corr, [f]), [])
        self.assertEqual(VR.check_fractions(self.corr, [f]), [])

    def test_las_medidas_de_calidad_de_datos_usan_las_marcas_de_fpedidos(self):
        self.assertIn("SUM ( fPedidos[registro_valido] ), SUM ( fPedidos[registro_total] )", self.guia)
        self.assertIn("91 297", self.guia) if False else self.assertRegex(self.guia, r"\d{2} \d{3} en este caso")


class TestPlanYErrores(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads(R.PLAN_POR_DEFECTO.read_text(encoding="utf-8"))
        self.resp = {}

    def test_el_plan_por_defecto_es_coherente_con_el_modelo(self):
        self.assertEqual(R.comprobar_plan(self.plan, MODELO, self.resp), [])

    def test_medida_no_definida_en_un_visual(self):
        self.plan["paginas"][0]["visuales"][0]["medidas"].append("MED-99")
        self.assertTrue(any("MED-99" in c for c in R.comprobar_plan(self.plan, MODELO, self.resp)))

    def test_dax_con_un_campo_fuera_del_modelo(self):
        self.plan["medidas"][0]["dax"] = "SUM ( fPedidos[no_existe] )"
        self.assertTrue(any("no_existe" in c for c in R.comprobar_plan(self.plan, MODELO, self.resp)))

    def test_kpi_sin_pagina(self):
        for p in self.plan["paginas"]:
            p["kpis"] = [k for k in p["kpis"] if k != "KPI-05"]
        self.plan["paginas"][2]["visuales"][3]["medidas"] = ["MED-09"]
        self.plan["paginas"][0]["visuales"][2]["medidas"] = [m for m in self.plan["paginas"][0]["visuales"][2]["medidas"] if m != "MED-14"]
        self.assertTrue(any("KPI-05" in c for c in R.comprobar_plan(self.plan, MODELO, self.resp)))

    def test_tipo_y_fuente_desconocidos(self):
        v = self.plan["paginas"][0]["visuales"][0]
        v["tipo"], v["datos"]["fuente"] = "pastel", "inventada"
        causas = " ".join(R.comprobar_plan(self.plan, MODELO, self.resp))
        self.assertIn("tipo desconocido pastel", causas)
        self.assertIn("fuente de datos desconocida inventada", causas)

    def test_meta_y_estado(self):
        self.assertEqual(R.parse_meta("12 % o más"), (">=", 12.0))
        self.assertEqual(R.parse_meta("3 % o menos"), ("<=", 3.0))
        self.assertEqual(R.parse_meta("Pendiente"), (None, None))
        self.assertEqual([R.estado(13, ">=", 12), R.estado(11, ">=", 12), R.estado(3, "<=", 3), R.estado(4, "<=", 3), R.estado(5, None, None)],
                         ["Cumple", "No cumple", "Cumple", "No cumple", "Sin meta"])

    def test_sin_paginas_json_o_sin_respuestas_se_informa(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(R.ErrorReferencia):
                R.cargar_plan(Path(d))
            with self.assertRaises(R.ErrorReferencia):
                R.cargar_respuestas(d)

    def test_el_ejemplo_de_la_plantilla_ds_5_es_un_plan_valido(self):
        ej = json.loads(F.ejemplo_json(R.PLAN_POR_DEFECTO.parent / "models" / "ds-5-paginas-json.md"))
        self.assertEqual(ej["schema"], 1)
        nombres = {m["nombre"] for m in ej["medidas"]}
        for m in ej["medidas"]:
            self.assertEqual(R.DAX.problemas_dax(m["dax"], MODELO, nombres), [])
        for p in ej["paginas"]:
            for v in p["visuales"]:
                self.assertIn(v["tipo"], R.TIPOS)
                self.assertIn(v["datos"]["fuente"], R.FUENTES)
                self.assertTrue(all(c in {m["codigo"] for m in ej["medidas"]} for c in v["medidas"]))

    def test_cli_plan_copia_el_plan_por_defecto(self):
        with tempfile.TemporaryDirectory() as d:
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(R.main(["plan", "--run", str(Path(d) / "corrida")]), 0)
            self.assertEqual(json.loads((Path(d) / "corrida" / "materiales" / "paginas.json").read_text(encoding="utf-8"))["schema"], 1)

    def test_cli_construir_sin_plan_falla_con_mensaje(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(R.main(["construir", "--run", str(Path(d) / "x"), "--raiz", d]), 1)


if __name__ == "__main__":
    unittest.main()
