"""Validador del paso 08-make-etl (sección 3.1, anexos A y B y evidencia.json) y comparación con la hoja de respuestas."""
import csv
import filecmp
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import etl_fixtures as EF  # noqa: E402
import etl_verificacion as EV  # noqa: E402
import projectcfg as P  # noqa: E402
import runs as R  # noqa: E402
import validate_run as V  # noqa: E402

COMMON = HERE.parents[2] / "common" / "08-etl"
SKILLS = HERE.parent


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run = EF.crear(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def msgs(self, run=None):
        return [f"{f}: {m}" for f, m in V.validate(run or self.run)]

    def assertIncidencia(self, texto, run=None):
        m = self.msgs(run)
        self.assertTrue(any(texto in x for x in m), m)

    def edita(self, archivo, a, b, run=None):
        f = (run or self.run) / archivo
        t = f.read_text(encoding="utf-8")
        assert a in t, a
        f.write_text(t.replace(a, b, 1), encoding="utf-8")

    def evidencia(self, run=None):
        return json.loads(((run or self.run) / "evidencia.json").read_text(encoding="utf-8"))

    def guarda(self, ev, run=None):
        ((run or self.run) / "evidencia.json").write_text(json.dumps(ev, ensure_ascii=False, indent=2), encoding="utf-8")


class TestPlaybook(unittest.TestCase):
    def test_guia_y_plantillas_con_las_cinco_partes(self):
        self.assertTrue((COMMON / "guia.md").is_file())
        plantillas = sorted((COMMON / "models").glob("etl-*.md"))
        self.assertEqual([p.name for p in plantillas], ["etl-1-seccion-3-1.md", "etl-2-anexo-a.md", "etl-3-anexo-b.md", "etl-4-guia-power-query.md", "etl-5-evidencia-json.md"])
        self.assertTrue((COMMON / "models" / "README.md").is_file())
        for p in plantillas:
            t = p.read_text(encoding="utf-8")
            self.assertIn("| **Entregable** |", t, p.name)
            for parte in ("## Instrucciones para el agente", "## Formato", "## Ejemplo", "## Checklist"):
                self.assertIn(parte, t, f"{p.name}: {parte}")

    def test_la_guia_dice_que_lo_ejecuta_el_equipo(self):
        t = (COMMON / "guia.md").read_text(encoding="utf-8")
        self.assertIn("no ejecuta Power Query ni Power BI", t)
        self.assertIn("evidencia.json", t)

    def test_las_skills_existen(self):
        for s in ("08-make-etl", "08-make-etl-update"):
            self.assertTrue((SKILLS / s / "SKILL.md").is_file(), s)
        self.assertTrue((SKILLS / "08-make-etl-update" / "references" / "dependencias.md").is_file())
        t = (SKILLS / "08-make-etl" / "SKILL.md").read_text(encoding="utf-8")
        for frase in ("datagen.py", "--confirmar", "revisor-redactor", "etl_verificacion.py", "no ejecuta"):
            self.assertIn(frase, t, frase)


class TestEjemplo(Base):
    def test_ejemplo_sin_incidencias(self):
        self.assertEqual(self.msgs(), [])

    def test_seccion_disponible_y_archivos(self):
        estado = {s["seccion"]: s["estado"] for s in P.secciones(self.root)}
        self.assertEqual(estado["3.1"], "disponible")
        for f in ("secciones/3.1.md", "anexos/A.md", "anexos/B.md", "evidencia.json", "materiales/guia-power-query.md", "README.md"):
            self.assertTrue((self.run / f).is_file(), f)

    def test_los_ejemplos_de_las_plantillas_son_coherentes_entre_si(self):
        ev = self.evidencia()
        self.assertEqual(sum(1 for r in ev["reglas"]), 6)
        self.assertEqual({t["nombre"] for t in ev["tablas"]} & {"FUE-01", "FUE-02", "FUE-03", "fPedidos", "dTurno"}, {"FUE-01", "FUE-02", "FUE-03", "fPedidos", "dTurno"})


class TestEvidencia(Base):
    def test_sin_evidencia(self):
        (self.run / "evidencia.json").unlink()
        self.assertIncidencia("falta la evidencia del equipo")

    def test_evidencia_desactualizada_tras_regenerar_los_datos(self):
        (self.run / "evidencia.json").rename(self.run / "evidencia-desactualizada.json")
        self.assertIncidencia("quedó desactualizada porque se regeneraron los datos")

    def test_json_invalido(self):
        (self.run / "evidencia.json").write_text("{no", encoding="utf-8")
        self.assertIncidencia("no es un JSON válido")

    def test_regla_sin_evidencia(self):
        ev = self.evidencia()
        ev["reglas"] = [r for r in ev["reglas"] if r["codigo"] != "REG-03"]
        self.guarda(ev)
        self.assertIncidencia("REG-03: la regla no tiene filas antes y después en la evidencia")

    def test_cifra_de_la_tabla_distinta_de_la_evidencia(self):
        self.edita("secciones/3.1.md", "| 1600 | 1568 |", "| 1600 | 1560 |")
        self.assertIncidencia("REG-03: «filas después» dice 1560 y la evidencia 1568")

    def test_cifra_en_el_texto_que_no_esta_en_la_evidencia(self):
        self.edita("secciones/3.1.md", "**Extracción.** Cada fuente", "**Extracción.** Se leyeron 9999 filas en total. Cada fuente")
        self.assertIncidencia("cita 9999 filas y esa cantidad no está en la evidencia")

    def test_cifra_del_texto_que_si_esta_en_la_evidencia(self):
        self.edita("secciones/3.1.md", "**Extracción.** Cada fuente", "**Extracción.** Se cargaron 1550 filas de pedidos. Cada fuente")
        self.assertEqual(self.msgs(), [])


class TestSeccion(Base):
    def test_fuente_del_brief_ausente(self):
        t = (self.run / "secciones" / "3.1.md").read_text(encoding="utf-8")
        fila = next(l for l in t.splitlines() if l.startswith("| FUE-03 | Precios"))
        self.edita("secciones/3.1.md", fila + "\n", "")
        self.assertIncidencia("FUE-03: la fuente del brief no está en la tabla de extracción")

    def test_filas_leidas_distintas(self):
        self.edita("secciones/3.1.md", "| fue-01-caja.csv | 1200 |", "| fue-01-caja.csv | 1100 |")
        self.assertIncidencia("FUE-01: la tabla dice 1100 filas leídas y la evidencia 1200")

    def test_defecto_sin_regla(self):
        self.edita("secciones/3.1.md", "| `nulo` |", "| `duplicado` |")
        self.assertIncidencia("el defecto «nulo» de data/respuestas/defectos.csv no tiene una regla REG-nn que lo trate")

    def test_defecto_desconocido(self):
        self.edita("secciones/3.1.md", "| `nulo` |", "| `otro` |")
        self.assertIncidencia("el defecto «otro» debe ser uno de")

    def test_tabla_del_modelo_fuera_de_la_carga(self):
        self.edita("secciones/3.1.md", "| dTurno | 3 |\n", "")
        self.assertIncidencia("dTurno: la tabla del modelo no está en la tabla de carga")

    def test_filas_cargadas_distintas(self):
        self.edita("secciones/3.1.md", "| fPedidos | 1550 |", "| fPedidos | 1500 |")
        self.assertIncidencia("fPedidos: la tabla dice 1500 filas cargadas y la evidencia 1550")

    def test_tabla_sin_titulo(self):
        self.edita("secciones/3.1.md", "Tabla 4: Tablas cargadas al modelo\n\n", "")
        self.assertIncidencia("hay una tabla sin su título")

    def test_sin_declarar_datos_generados(self):
        t = (self.run / "secciones" / "3.1.md").read_text(encoding="utf-8").replace("generados", "reales").replace("generado", "real")
        (self.run / "secciones" / "3.1.md").write_text(t, encoding="utf-8")
        self.assertIncidencia("3.1 no lo declara")

    def test_modo_real_no_exige_declarar_datos_generados(self):
        cfg = self.root / "project" / "config.yaml"
        cfg.write_text(cfg.read_text(encoding="utf-8").replace("modo_datos: generado", "modo_datos: real"), encoding="utf-8")
        t = (self.run / "secciones" / "3.1.md").read_text(encoding="utf-8").replace("generados", "reales").replace("generado", "real")
        (self.run / "secciones" / "3.1.md").write_text(t, encoding="utf-8")
        self.assertFalse(any("3.1 no lo declara" in m for m in self.msgs()))

    def test_sin_lectura(self):
        self.edita("secciones/3.1.md", "**Lectura del ETL.**", "**Nota.**")
        self.assertIncidencia("falta la «**Lectura del ETL.**»")

    def test_encabezado_exacto(self):
        self.edita("secciones/3.1.md", "## 3.1. Construcción de la solución ETL", "## 3.1. ETL")
        self.assertIncidencia("la primera línea debe ser «## 3.1. Construcción de la solución ETL»")

    def test_costos_sin_explicar_con_archivos_de_apoyo(self):
        t = (self.run / "secciones" / "3.1.md").read_text(encoding="utf-8")
        (self.run / "secciones" / "3.1.md").write_text(t.replace("El costo estimado de cada línea", "La cifra de cada línea"), encoding="utf-8")
        self.assertIncidencia("el modelo tiene costo_estimado y 3.1 no explica cómo se calcula")

    def test_sin_archivos_de_apoyo_no_exige_los_costos(self):
        for f in (self.root / "data").glob("apoyo-*.csv"):
            f.unlink()
        t = (self.run / "secciones" / "3.1.md").read_text(encoding="utf-8")
        (self.run / "secciones" / "3.1.md").write_text(t.replace("El costo estimado de cada línea", "La cifra de cada línea"), encoding="utf-8")
        self.assertFalse(any("costo_estimado" in m for m in self.msgs()))

    def test_codigo_citado_sin_definir(self):
        self.edita("secciones/3.1.md", "**Carga.** El modelo", "**Carga.** Según REG-09, el modelo")
        self.assertIncidencia("código citado sin definir: REG-09")


class TestVerificacion(Base):
    def test_coincide_en_el_ejemplo(self):
        self.assertEqual(EV.comparar(self.root, self.evidencia())["estado"], "coincide")

    def test_estado_coincide_pero_el_texto_no_lo_dice(self):
        self.edita("secciones/3.1.md", "Los totales del modelo cargado coinciden", "Los totales del modelo cargado se parecen")
        self.assertIncidencia("la «Verificación» no lo dice")

    def test_diferencias_en_la_evidencia_sin_tabla(self):
        ev = self.evidencia()
        ev["verificacion"] = {"estado": "diferencias", "diferencias": [{"tabla": "fPedidos", "mes": "2026-02", "esperado": 520, "obtenido": 500}]}
        self.guarda(ev)
        self.edita("secciones/3.1.md", "no tienen diferencias", "no tienen desvíos")
        m = self.msgs()
        self.assertTrue(any("no las menciona" in x for x in m), m)
        self.assertTrue(any("la evidencia tiene 1 diferencias" in x for x in m), m)

    def test_verificacion_guardada_distinta_de_la_actual(self):
        pedidos = self.root / "data" / "salida" / "fPedidos.csv"
        filas = pedidos.read_text(encoding="utf-8").splitlines()
        pedidos.write_text("\n".join(filas[:-30]) + "\n", encoding="utf-8")
        self.assertIncidencia("la verificación guardada dice «coincide» y la comparación actual con data/respuestas/ dice «diferencias»")

    def test_diferencia_por_mes_con_desvio_y_regla_probable(self):
        pedidos = self.root / "data" / "salida" / "fPedidos.csv"
        filas = pedidos.read_text(encoding="utf-8").splitlines()
        pedidos.write_text("\n".join(filas[:-30]) + "\n", encoding="utf-8")  # 30 líneas de Rappi de febrero
        r = EV.comparar(self.root, self.evidencia())
        self.assertEqual(r["estado"], "diferencias")
        d = {(x["medida"], x["mes"], x.get("canal")): x for x in r["diferencias"]}
        lineas = d[("lineas", "2026-02", "Rappi")]
        self.assertEqual((lineas["esperado"], lineas["obtenido"], lineas["desvio"]), (480, 450, -30))
        self.assertIn("filas de menos", lineas["regla_probable"])
        self.assertIn("Convertir las fechas a AAAA-MM-DD", lineas["regla_probable"])
        self.assertEqual(d[("ventas", "2026-02", "Rappi")]["desvio"], -1800.0)

    def test_filas_de_mas_apuntan_a_duplicados_o_invalidos(self):
        pedidos = self.root / "data" / "salida" / "fPedidos.csv"
        t = pedidos.read_text(encoding="utf-8").splitlines()
        pedidos.write_text("\n".join(t + t[1:11]) + "\n", encoding="utf-8")
        r = EV.comparar(self.root, self.evidencia())
        self.assertTrue(any("filas de más" in x["regla_probable"] and "Quitar los pedidos repetidos" in x["regla_probable"] for x in r["diferencias"]), r)

    def test_sin_salida_compara_los_totales_de_la_evidencia(self):
        shutil.rmtree(self.root / "data" / "salida")
        ev = self.evidencia()
        self.assertEqual(EV.comparar(self.root, ev)["fuente"], "totales")
        self.assertEqual(EV.comparar(self.root, ev)["estado"], "coincide")
        ev["totales"]["ventas_total"] = 78000.0
        r = EV.comparar(self.root, ev)
        self.assertEqual((r["estado"], r["diferencias"][0]["mes"], r["diferencias"][0]["desvio"]), ("diferencias", "total", -1200.0))

    def test_sin_salida_ni_totales(self):
        shutil.rmtree(self.root / "data" / "salida")
        self.assertEqual(EV.comparar(self.root, {})["estado"], "sin_datos_del_equipo")

    def test_sin_hoja_de_respuestas(self):
        shutil.rmtree(self.root / "data" / "respuestas")
        self.assertEqual(EV.comparar(self.root, self.evidencia())["estado"], "sin_respuestas")

    def test_produccion_y_precio(self):
        (self.root / "data" / "salida" / "fProduccion.csv").write_text("fecha_key,turno_key,pollos_preparados,pollos_vendidos,pollos_merma\n1,1,100,94,6\n2,1,120,100,20\n", encoding="utf-8")
        (self.root / "data" / "salida" / "fPrecioInsumo.csv").write_text("fecha_key,precio_kg,valor_imputado\n1,6.0,1\n1,7.0,0\n2,6.0,0\n2,6.0,0\n", encoding="utf-8")
        r = EV.comparar(self.root, self.evidencia())
        medidas = {(x["tabla"], x["mes"], x["medida"]) for x in r["diferencias"]}
        self.assertEqual(medidas, {("fProduccion", "2026-02", "vendidos"), ("fProduccion", "2026-02", "merma"), ("fPrecioInsumo", "2026-02", "precio_medio")})

    def test_numeros_con_coma_decimal_y_registros_invalidos_excluidos(self):
        d = self.root / "data" / "salida"
        with open(d / "fPedidos.csv", newline="", encoding="utf-8") as f:
            filas = list(csv.reader(f))
        filas = [filas[0]] + [[c.replace("45.0", "45,0") for c in fila] for fila in filas[1:]] + [["1", "1", "99,9", "0", "0"]]  # el último es inválido
        with open(d / "fPedidos.csv", "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(filas)
        self.assertEqual(EV.comparar(self.root, self.evidencia())["estado"], "coincide")

    def test_cli_con_salida_compara_las_tablas_y_no_los_totales_tecleados(self):
        ruta = self.run / "evidencia.json"
        ev = self.evidencia()
        ev["totales"]["comision_total"] = 9000.0  # se ignora: hay tablas exportadas
        ev["verificacion"] = {"estado": "diferencias", "diferencias": []}
        self.guarda(ev)
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(EV.main(["comparar", "--raiz", str(self.root), "--evidencia", str(ruta), "--actualizar"]), 0)
        self.assertEqual(json.loads(out.getvalue())["fuente"], "salida")
        self.assertEqual(self.evidencia()["verificacion"]["estado"], "coincide")

    def test_cli_sin_subcomando_como_lo_llama_datagen(self):
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(EV.main(["--raiz", str(self.root)]), 0)
        self.assertEqual(json.loads(out.getvalue())["estado"], "coincide")

    def test_cli_sin_salida_y_con_totales_distintos(self):
        shutil.rmtree(self.root / "data" / "salida")
        ruta = self.run / "evidencia.json"
        ev = self.evidencia()
        ev["totales"]["lineas_total"] = 1500
        self.guarda(ev)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(EV.main(["comparar", "--raiz", str(self.root), "--evidencia", str(ruta), "--actualizar"]), 0)
        v = self.evidencia()["verificacion"]
        self.assertEqual(v["estado"], "diferencias")
        self.assertEqual(v["diferencias"][0]["medida"], "lineas")


class TestAnexoA(Base):
    def test_campo_del_modelo_sin_origen(self):
        self.edita("anexos/A.md", "dia_semana; es_feriado", "dia_semana")
        self.assertIncidencia("dCalendario.es_feriado: el campo del modelo no tiene origen ni cálculo")

    def test_tabla_del_modelo_sin_fila(self):
        t = (self.run / "anexos" / "A.md").read_text(encoding="utf-8")
        fila = next(l for l in t.splitlines() if l.startswith("| dLocal |"))
        self.edita("anexos/A.md", fila + "\n", "")
        self.assertIncidencia("dLocal.local_key: el campo del modelo no tiene origen ni cálculo")

    def test_campo_que_no_existe_en_el_modelo(self):
        self.edita("anexos/A.md", "| dLocal | local_key; local; zona |", "| dLocal | local_key; local; zona; mapa |")
        self.assertIncidencia("dLocal.mapa: el campo no existe en el modelo")

    def test_origen_invalido(self):
        self.edita("anexos/A.md", "| fPrecioInsumo | precio_kg | FUE-03.precio_kg |", "| fPrecioInsumo | precio_kg | alguna parte |")
        self.assertIncidencia("el origen «alguna parte» debe ser")

    def test_origen_de_una_fuente_que_no_existe(self):
        self.edita("anexos/A.md", "| fPrecioInsumo | precio_kg | FUE-03.precio_kg |", "| fPrecioInsumo | precio_kg | FUE-09.precio_kg |")
        self.assertIncidencia("el origen «FUE-09.precio_kg» debe ser")

    def test_origen_de_un_archivo_de_apoyo(self):
        self.edita("anexos/A.md", "| fPrecioInsumo | precio_kg | FUE-03.precio_kg |", "| fPrecioInsumo | precio_kg | apoyo-costos-operativos.total |")
        self.assertEqual(self.msgs(), [])

    def test_fuente_sin_campos_en_el_diccionario(self):
        t = (self.run / "anexos" / "A.md").read_text(encoding="utf-8")
        for fila in [l for l in t.splitlines() if l.startswith("| FUE-02 |") and "pedido_id" in l or l.startswith("| FUE-02 | monto") or l.startswith("| FUE-02 | comision")]:
            self.edita("anexos/A.md", fila + "\n", "")
        self.assertIncidencia("FUE-02: la fuente del brief no tiene campos en el diccionario")

    def test_regla_del_diccionario_sin_definir_en_3_1(self):
        self.edita("anexos/A.md", "| texto | REG-05 |", "| texto | REG-08 |")
        self.assertIncidencia("la regla REG-08 no está definida en 3.1")

    def test_destino_que_no_existe_en_el_modelo(self):
        self.edita("anexos/A.md", "| fPedidos.cantidad |", "| fPedidos.unidades |")
        self.assertIncidencia("el destino «fPedidos.unidades» no existe en el modelo")

    def test_resultado_de_la_regla_distinto_de_la_evidencia(self):
        self.edita("anexos/A.md", "| REG-03 | 1600 | 1568 | -32 |", "| REG-03 | 1600 | 1570 | -30 |")
        self.assertIncidencia("REG-03: las filas antes y después difieren de la evidencia")

    def test_diferencia_mal_calculada(self):
        self.edita("anexos/A.md", "| REG-03 | 1600 | 1568 | -32 |", "| REG-03 | 1600 | 1568 | -30 |")
        self.assertIncidencia("REG-03: la diferencia debe ser -32")

    def test_regla_de_3_1_sin_fila_en_el_resultado(self):
        self.edita("anexos/A.md", "| REG-06 | 80 | 92 | 12 |\n", "")
        self.assertIncidencia("REG-06: la regla de 3.1 no tiene su fila en el resultado")

    def test_sin_anexo_a(self):
        (self.run / "anexos" / "A.md").unlink()
        self.assertIncidencia("falta el anexo A")

    def test_encabezado_del_anexo(self):
        self.edita("anexos/A.md", "# Anexo A: Diccionario de datos y calidad de datos", "# Anexo A")
        self.assertIncidencia("la primera línea debe ser «# Anexo A: Diccionario de datos y calidad de datos»")


class TestAnexoB(Base):
    def test_paso_sin_bloque(self):
        t = (self.run / "anexos" / "B.md").read_text(encoding="utf-8")
        i, j = t.index("**PAS-05.**"), t.index("**PAS-06.**")
        (self.run / "anexos" / "B.md").write_text(t[:i] + t[j:], encoding="utf-8")
        self.assertIncidencia("PAS-05: el paso de 3.1 no tiene su bloque")

    def test_bloque_vacio(self):
        self.edita("anexos/B.md", "```m\n= Table.FillDown(DiasConPrecio, {\"precio_kg\"})\n```", "```m\n```")
        self.assertIncidencia("PAS-05: el bloque no trae el código ni los pasos")

    def test_bloque_con_pasos_numerados_es_valido(self):
        self.assertEqual(self.msgs(), [])  # PAS-06 y PAS-07 del ejemplo son listas

    def test_bloque_de_un_paso_que_no_esta_en_3_1(self):
        (self.run / "anexos" / "B.md").write_text((self.run / "anexos" / "B.md").read_text(encoding="utf-8") + "\n**PAS-09.** Otro\n\n```m\n= 1\n```\n", encoding="utf-8")
        self.assertIncidencia("PAS-09: el bloque del anexo B no corresponde a ningún paso de 3.1")

    def test_sin_anexo_b(self):
        (self.run / "anexos" / "B.md").unlink()
        self.assertIncidencia("falta el anexo B")


class TestTextoLimpio(Base):
    def test_termino_no_permitido_en_los_anexos(self):
        self.edita("anexos/A.md", "Este anexo lista", "Estos datos simulados listan")
        self.assertIncidencia("término no permitido")


class TestUpdate(Base):
    def test_corregir_una_cifra_cambia_solo_3_1_el_anexo_a_y_la_evidencia(self):
        fork = Path(R.fork(EF.PASO, ["Corregir las filas de REG-03"], root=self.root))
        ev = self.evidencia(fork)
        for r in ev["reglas"]:
            if r["codigo"] == "REG-03":
                r["filas_despues"] = 1570
            if r["codigo"] == "REG-04":
                r["filas_antes"] = 1570
        self.guarda(ev, fork)
        self.edita("secciones/3.1.md", "| 1600 | 1568 |", "| 1600 | 1570 |", fork)
        self.edita("secciones/3.1.md", "| 1568 | 1550 |", "| 1570 | 1550 |", fork)
        self.edita("anexos/A.md", "| REG-03 | 1600 | 1568 | -32 |", "| REG-03 | 1600 | 1570 | -30 |", fork)
        self.edita("anexos/A.md", "| REG-04 | 1568 | 1550 | -18 |", "| REG-04 | 1570 | 1550 | -20 |", fork)
        self.assertEqual(self.msgs(fork), [])
        self.assertTrue(filecmp.cmp(self.run / "anexos" / "B.md", fork / "anexos" / "B.md", shallow=False))
        self.assertTrue(filecmp.cmp(self.run / "materiales" / "guia-power-query.md", fork / "materiales" / "guia-power-query.md", shallow=False))
        cmp = filecmp.dircmp(self.run, fork)
        self.assertEqual(sorted(x for x in cmp.diff_files if x != "README.md"), ["evidencia.json"])

    def test_corregir_solo_el_texto_sin_la_evidencia_se_detecta(self):
        fork = Path(R.fork(EF.PASO, ["Corregir sin evidencia"], root=self.root))
        self.edita("secciones/3.1.md", "| 1600 | 1568 |", "| 1600 | 1570 |", fork)
        self.assertTrue(any("REG-03: «filas después» dice 1570 y la evidencia 1568" in m for m in self.msgs(fork)))

    def test_regenerar_los_datos_marca_la_evidencia_como_desactualizada(self):
        fork = Path(R.fork(EF.PASO, ["Regenerar los datos"], root=self.root))
        (fork / "evidencia.json").rename(fork / "evidencia-desactualizada.json")
        self.assertTrue(any("quedó desactualizada" in m for m in self.msgs(fork)))
        self.assertEqual(self.msgs(), [])  # la base no cambia


if __name__ == "__main__":
    unittest.main()
