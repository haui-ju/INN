"""Validador del paso 07-make-data-model-kpi (secciones 2.4 y 2.5 y modelo.json) contra el brief y su figura modelo-datos."""
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

PASO = "07-make-data-model-kpi"


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

    def json(self, run=None):
        return json.loads(((run or self.run) / "modelo.json").read_text(encoding="utf-8"))

    def guarda_json(self, j, run=None):
        ((run or self.run) / "modelo.json").write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")

    def sin_fila(self, punto, prefijo):
        f = self.run / "secciones" / f"{punto}.md"
        f.write_text("\n".join(ln for ln in f.read_text(encoding="utf-8").splitlines() if not ln.startswith(prefijo)) + "\n", encoding="utf-8")

    def assertIncidencia(self, texto):
        m = self.msgs()
        self.assertTrue(any(texto in x for x in m), m)


class TestPlaybook(unittest.TestCase):
    COMMON = HERE.parents[2] / "common" / "07-data-model-kpi"

    def test_guia_y_plantillas_con_las_cinco_partes(self):
        self.assertTrue((self.COMMON / "guia.md").is_file())
        plantillas = sorted(p for p in (self.COMMON / "models").glob("dm-*.md"))
        self.assertEqual([p.name for p in plantillas], ["dm-1-modelo.md", "dm-2-kpi.md", "dm-3-modelo-json.md"])
        self.assertTrue((self.COMMON / "models" / "README.md").is_file())
        for p in plantillas:
            t = p.read_text(encoding="utf-8")
            self.assertIn("| **Entregable** |", t, p.name)
            for parte in ("## Instrucciones para el agente", "## Formato", "## Ejemplo", "## Checklist"):
                self.assertIn(parte, t, f"{p.name}: {parte}")

    def test_el_ejemplo_de_modelo_json_coincide_con_las_secciones(self):
        with tempfile.TemporaryDirectory() as t:
            run = Path(t)
            (run / "secciones").mkdir()
            for punto, archivo in {"2.4": "dm-1-modelo.md", "2.5": "dm-2-kpi.md"}.items():
                (run / "secciones" / f"{punto}.md").write_text(F.ejemplo(self.COMMON / "models" / archivo), encoding="utf-8")
            (run / "modelo.json").write_text(F.ejemplo_json(self.COMMON / "models" / "dm-3-modelo-json.md"), encoding="utf-8")
            from rules import data_model_kpi as K
            self.assertEqual(K.check_json(D.leer_modelo(run)), [])


class TestEjemplo(Base):
    def test_ejemplo_sin_incidencias(self):
        self.assertEqual(self.msgs(), [])

    def test_capitulo_2_completo_y_archivos(self):
        estado = {s["seccion"]: s["estado"] for s in P.secciones(self.root)}
        self.assertEqual([estado["2.4"], estado["2.5"]], ["disponible", "disponible"])
        for f in ("modelo.json", "visuales/modelo-datos.html", "visuales/modelo-datos.json", "leer-imagen/modelo-datos.md"):
            self.assertTrue((self.run / f).is_file(), f)

    def test_encabezados_exactos(self):
        self.assertEqual(D.encabezado("2.4"), "## 2.4. Diseño del modelado de datos: hechos, dimensiones y relaciones")
        self.edita("2.5", "## 2.5. Indicadores clave de rendimiento", "## 2.5. KPI")
        self.assertIncidencia("la primera línea debe ser «## 2.5. Indicadores clave de rendimiento»")

    def test_check_avisa_si_falta_la_arquitectura(self):
        for s in ("05-make-problem-objectives", "06-make-bi-solution"):
            (self.root / ".claude" / "skills" / s).mkdir(parents=True)
        self.assertEqual(P.check(PASO, self.root), [])
        cfg = P.load(self.root)
        cfg["pasos"]["06-make-bi-solution"]["run"] = None
        P.save(cfg, self.root)
        self.assertTrue(any("06-make-bi-solution" in a for a in P.check(PASO, self.root)))


class TestHechos(Base):
    def test_hecho_sin_granularidad(self):
        self.edita("2.4", "| Una fila por local, turno y día |", "| |")
        self.assertIncidencia("FCT-02: la tabla de hechos fProduccion no declara su granularidad")

    def test_medida_sin_agregacion(self):
        self.edita("2.4", "pollos_merma (suma)", "pollos_merma")
        self.assertIncidencia("FCT-02: la medida «pollos_merma» necesita su agregación")

    def test_hecho_sin_claves(self):
        self.edita("2.4", "| fecha_key |\n\n**Dimensiones.**", "| |\n\n**Dimensiones.**")
        self.assertIncidencia("FCT-03: la tabla de hechos fPrecioInsumo no tiene claves")

    def test_sin_tabla_de_hechos(self):
        self.edita("2.4", "| Código | Tabla de hechos | Granularidad | Medidas | Claves |", "| Código | Tabla de hechos | Granularidad | Cantidades | Claves |")
        self.assertIncidencia("falta la tabla de hechos")


class TestDimensiones(Base):
    def test_falta_la_dimension_de_tiempo(self):
        for pref in ("| REL-01 ", "| REL-06 ", "| REL-09 "):
            self.sin_fila("2.4", pref)
        t = (self.run / "secciones" / "2.4.md").read_text(encoding="utf-8").replace("dCalendario", "dPeriodoX")
        (self.run / "secciones" / "2.4.md").write_text(t, encoding="utf-8")
        self.assertIncidencia("KPI-02 tiene frecuencia mensual y el modelo no tiene dimensión de tiempo")

    def test_dimension_sin_atributos(self):
        self.edita("2.4", "| fecha; anio; mes; nombre_mes; dia_semana; es_feriado |", "| |")
        self.assertIncidencia("DIM-01: la dimensión dCalendario no tiene atributos")

    def test_dimension_suelta(self):
        for pref in ("| REL-05 ", "| REL-08 "):  # dTurno está unida por fPedidos y por fProduccion
            self.sin_fila("2.4", pref)
        self.assertIncidencia("DIM-05: la dimensión dTurno no participa en ninguna relación")


class TestRelaciones(Base):
    def test_relacion_a_tabla_inexistente(self):
        self.edita("2.4", "| REL-03 | fPedidos | dCanal |", "| REL-03 | fPedidos | dCanales |")
        self.assertIncidencia("REL-03: «dCanales» no es una dimensión definida")

    def test_relacion_desde_tabla_inexistente(self):
        self.edita("2.4", "| REL-07 | fProduccion | dLocal |", "| REL-07 | fProduccionX | dLocal |")
        self.assertIncidencia("REL-07: «fProduccionX» no es una tabla de hechos definida")

    def test_cardinalidad_y_filtro_invalidos(self):
        self.edita("2.4", "| REL-01 | fPedidos | dCalendario | fecha_key | *:1 | Simple |", "| REL-01 | fPedidos | dCalendario | fecha_key | varios | Doble |")
        self.assertIncidencia("REL-01: la cardinalidad debe ser una de")
        self.assertIncidencia("REL-01: la dirección del filtro debe ser Simple o Ambos")

    def test_campo_que_no_une_las_tablas(self):
        self.edita("2.4", "| REL-04 | fPedidos | dLocal | local_key |", "| REL-04 | fPedidos | dLocal | sucursal_key |")
        self.assertIncidencia("REL-04: el campo «sucursal_key» no está entre las claves de fPedidos")

    def test_codigo_citado_sin_definir(self):
        self.edita("2.4", "**Lectura del modelo.** Con este modelo", "**Lectura del modelo.** Según REL-20, con este modelo")
        self.assertIncidencia("código citado sin definir: REL-20")

    def test_marca_de_figura(self):
        self.edita("2.4", "<!-- figura: modelo-datos -->", "")
        self.assertIncidencia("debe marcar una sola vez la figura con la línea «<!-- figura: modelo-datos -->»")


class TestKpi(Base):
    def test_objetivo_sin_kpi(self):
        self.sin_fila("2.5", "| KPI-03 |")
        j = self.json()
        j["kpis"] = [k for k in j["kpis"] if k["codigo"] != "KPI-03"]
        self.guarda_json(j)
        self.assertIncidencia("OE-03: el objetivo no tiene ningún KPI")

    def test_kpi_con_campo_fuera_del_modelo(self):
        self.edita("2.5", "fProduccion.pollos_merma; fProduccion.pollos_preparados; dTurno.turno", "fProduccion.pollos_merma; fProduccion.pollos_sobrantes; dTurno.turno")
        self.assertIncidencia("KPI-03: el campo «fProduccion.pollos_sobrantes» no está en el modelo de datos")

    def test_kpi_con_tabla_fuera_del_modelo(self):
        self.edita("2.5", "fPrecioInsumo.precio_kg; dCalendario.fecha", "fPrecios.precio_kg; dCalendario.fecha")
        self.assertIncidencia("KPI-05: el origen «fPrecios.precio_kg» cita la tabla fPrecios, que no está en el modelo")

    def test_kpi_sin_meta(self):
        self.edita("2.5", "| KPI-04 | 70 % o más |", "| KPI-04 | |")
        self.assertIncidencia("KPI-04: falta la meta")

    def test_meta_pendiente_no_es_error(self):
        self.assertEqual(self.msgs(), [])
        self.assertIn("| KPI-05 | Pendiente |", (self.run / "secciones" / "2.5.md").read_text(encoding="utf-8"))

    def test_frecuencia_invalida(self):
        self.edita("2.5", "| KPI-03 | 3 % o menos | Diaria |", "| KPI-03 | 3 % o menos | Cada rato |")
        self.assertIncidencia("KPI-03: la frecuencia debe ser una de")

    def test_objetivo_que_no_es_del_brief(self):
        self.edita("2.5", "| KPI-04 | 70 % o más | Mensual | OE-02 |", "| KPI-04 | 70 % o más | Mensual | OE-08 |")
        self.assertIncidencia("KPI-04: el objetivo «OE-08» no es un OE del brief vigente")

    def test_ningun_kpi_se_llama_como_el_indicador(self):
        self.edita("2.5", "| KPI-03 | Porcentaje de merma por turno |", "| KPI-03 | Merma |")
        self.assertIncidencia("OE-03: ningún KPI se llama como su indicador del brief")

    def test_kpi_sin_fila_de_gestion(self):
        self.sin_fila("2.5", "| KPI-05 | Pendiente |")
        self.assertIncidencia("KPI-05: no tiene fila en la tabla de meta, frecuencia y decisión")


class TestModeloJson(Base):
    def test_falta_el_archivo(self):
        (self.run / "modelo.json").unlink()
        self.assertIncidencia("modelo.json: falta modelo.json")

    def test_json_invalido(self):
        (self.run / "modelo.json").write_text("{ no es json", encoding="utf-8")
        self.assertIncidencia("modelo.json: no es un JSON válido")

    def test_tabla_de_mas_en_el_json(self):
        j = self.json()
        j["hechos"].append({"codigo": "FCT-09", "nombre": "fExtra", "granularidad": "x", "medidas": [], "claves": []})
        self.guarda_json(j)
        self.assertIncidencia("FCT-09 (hecho) está en modelo.json y no figura en las secciones")

    def test_kpi_que_falta_en_el_json(self):
        j = self.json()
        j["kpis"] = j["kpis"][:-1]
        self.guarda_json(j)
        self.assertIncidencia("KPI-05 (KPI) figura en las secciones y falta en modelo.json")

    def test_meta_distinta(self):
        j = self.json()
        j["kpis"][0]["meta"] = "90 % o más"
        self.guarda_json(j)
        self.assertIncidencia("KPI-01: «meta» difiere de las secciones")

    def test_medida_con_tipo_invalido(self):
        j = self.json()
        j["hechos"][0]["medidas"][0]["tipo"] = "texto"
        self.guarda_json(j)
        self.assertIncidencia("FCT-01: el tipo de cantidad debe ser entero o decimal")

    def test_relacion_distinta(self):
        j = self.json()
        j["relaciones"][0]["cardinalidad"] = "1:1"
        self.guarda_json(j)
        self.assertIncidencia("REL-01: «cardinalidad» difiere de las secciones")


class TestVisual(Base):
    def test_extraccion_desde_modelo_json(self):
        d = VI.extraer("modelo-datos", self.root)
        self.assertEqual([h["nombre"] for h in d["hechos"]], ["fPedidos", "fProduccion", "fPrecioInsumo"])
        self.assertEqual(len(d["dimensiones"]), 5)
        self.assertEqual(len(d["relaciones"]), 9)
        self.assertNotIn("kpis", d)

    def test_explicacion_y_construccion(self):
        d = VI.extraer("modelo-datos", self.root)
        txt = VI.leer_imagen("modelo-datos", d, F.INTERPRETACION)
        self.assertEqual(VI.validar_explicacion(txt, False), [])
        self.assertIn("3 tablas de hechos y 5 dimensiones unidas por 9 relaciones", txt)
        self.assertIn("Pollería Don Tito", (self.run / "visuales" / "modelo-datos.html").read_text(encoding="utf-8"))

    def test_sin_modelo_json_no_hay_fuente(self):
        (self.run / "modelo.json").unlink()
        with self.assertRaises(VI.SinFuente):
            VI.extraer("modelo-datos", self.root)


class TestInforme(Base):
    def test_el_capitulo_2_aparece_completo_con_sus_dos_figuras(self):
        import report as RP
        run = self.root / "project" / RP.CARPETA / "r1"
        res = RP.construir(self.root, run)
        txt = (run / RP.INFORME).read_text(encoding="utf-8")
        for p in ("2.1", "2.2", "2.3", "2.4", "2.5"):
            self.assertIn(p, res["incluidas"])
        self.assertIn("(INCLUIR IMAGEN: Figura 5: Arquitectura de BI. Archivo sugerido: imagenes/arquitectura-bi.html)", txt)
        self.assertIn("(INCLUIR IMAGEN: Figura 6: Modelo de datos en estrella. Archivo sugerido: imagenes/modelo-datos.html)", txt)
        self.assertEqual(res["figuras"], 6)
        faltantes = (run / "faltantes.md").read_text(encoding="utf-8")
        for p in ("2.1", "2.2", "2.3", "2.4", "2.5"):
            self.assertNotIn(f"| {p} |", faltantes)
        self.assertEqual(res["pendientes"], ["3.1", "3.2", "4", "5"])
        self.assertEqual(V.validate(run), [])


class TestUpdate(Base):
    def test_agregar_un_kpi_cambia_solo_2_5_y_el_json(self):
        fork = Path(R.fork(PASO, ["Agregar el KPI de pedidos por turno"], root=self.root))
        self.edita("2.5", "| KPI-05 | Precio promedio del pollo vivo por kilogramo | Promedio del precio diario por kilogramo en el periodo | Precio pollo vivo | fPrecioInsumo.precio_kg; dCalendario.fecha |",
                   "| KPI-05 | Precio promedio del pollo vivo por kilogramo | Promedio del precio diario por kilogramo en el periodo | Precio pollo vivo | fPrecioInsumo.precio_kg; dCalendario.fecha |\n"
                   "| KPI-06 | Pollos vendidos por turno | Suma de los pollos vendidos, por turno | Pollos vendidos | fProduccion.pollos_vendidos; dTurno.turno |", run=fork)
        self.edita("2.5", "| KPI-05 | Pendiente | Semanal | OE-02 | Anticipar compras ante subidas del precio del pollo vivo |",
                   "| KPI-05 | Pendiente | Semanal | OE-02 | Anticipar compras ante subidas del precio del pollo vivo |\n"
                   "| KPI-06 | Pendiente | Diaria | OE-03 | Definir cuántos pollos hornear por turno y día de la semana |", run=fork)
        j = self.json(fork)
        j["kpis"].append({"codigo": "KPI-06", "nombre": "Pollos vendidos por turno", "formula": "Suma de los pollos vendidos, por turno", "medida": "Pollos vendidos",
                          "origen": ["fProduccion.pollos_vendidos", "dTurno.turno"], "meta": "Pendiente", "frecuencia": "Diaria", "objetivo": "OE-03",
                          "decision": "Definir cuántos pollos hornear por turno y día de la semana"})
        self.guarda_json(j, fork)
        self.assertEqual(self.msgs(fork), [])
        self.assertTrue(filecmp.cmp(self.run / "secciones" / "2.4.md", fork / "secciones" / "2.4.md", shallow=False))
        self.assertTrue(filecmp.cmp(self.run / "visuales" / "modelo-datos.html", fork / "visuales" / "modelo-datos.html", shallow=False))
        sec = filecmp.dircmp(self.run / "secciones", fork / "secciones")
        self.assertEqual(sorted(sec.diff_files), ["2.5.md"])
        self.assertEqual(len(D.leer_modelo(fork)["kpis"]), 6)

    def test_el_json_desactualizado_en_el_fork_se_detecta(self):
        fork = Path(R.fork(PASO, ["Agregar un KPI sin actualizar el json"], root=self.root))
        self.edita("2.5", "| KPI-05 | Pendiente | Semanal |", "| KPI-05 | 5 S/ por kg o menos | Semanal |", run=fork)
        self.assertTrue(any("KPI-05: «meta» difiere de las secciones" in m for m in self.msgs(fork)))


if __name__ == "__main__":
    unittest.main()
