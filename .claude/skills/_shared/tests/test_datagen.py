"""Generador de datos (datagen.py): reproducibilidad, calibración con el informe, defectos, hoja de respuestas y volumen."""
import csv
import datetime as dt
import filecmp
import io
import json
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import datagen as G  # noqa: E402


def leer(ruta):
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fecha(s):
    s = s.split(" ")[0]
    return dt.datetime.strptime(s, "%Y-%m-%d" if "-" in s else "%d/%m/%Y").date()


class TestGeneracion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.data = Path(cls.tmp.name) / "data"
        cls.params = G.parametros_base()
        t = time.time()
        cls.resumen = G.generar(cls.params, cls.data)
        cls.segundos = time.time() - t

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_un_csv_por_fuente_y_los_archivos_de_apoyo(self):
        for archivo in ("fue-01-caja.csv", "fue-02-rappi.csv", "fue-03-pedidosya.csv", "fue-04-whatsapp.csv", "fue-05-produccion.csv",
                        "fue-06-precios-pollo.csv", "apoyo-catalogo-productos.csv", "apoyo-costos-operativos.csv", "README.md"):
            self.assertTrue((self.data / archivo).is_file(), archivo)
        for archivo in ("filas-por-fuente", "ventas-mes-canal", "produccion-mes-turno", "precio-mes", "defectos", "kpi-esperados"):
            self.assertTrue((self.data / "respuestas" / f"{archivo}.csv").is_file(), archivo)
        self.assertEqual(list(leer(self.data / "fue-03-pedidosya.csv")[0]), ["nro_pedido", "fecha", "item", "cant", "total", "comision_pct", "estado"])

    def test_reproducible_byte_a_byte(self):
        with tempfile.TemporaryDirectory() as d:
            G.generar(self.params, Path(d))
            for f in sorted(p for p in self.data.rglob("*") if p.is_file()):
                self.assertTrue(filecmp.cmp(f, Path(d) / f.relative_to(self.data), shallow=False), f.name)

    def test_otra_semilla_cambia_los_datos(self):
        corto = dict(self.params, periodo={"inicio": "2026-01-01", "fin": "2026-03-31"})
        a = G.simular(corto)["filas"]["fue-01"]
        b = G.simular(dict(corto, semilla=7))["filas"]["fue-01"]
        self.assertNotEqual(a, b)

    def test_cifras_calibradas_con_el_informe(self):
        for nombre, esperado, obtenido, tol, ok in self.resumen["calibracion"]:
            self.assertTrue(ok, f"{nombre}: esperado {esperado}, obtenido {obtenido}")
        r = self.resumen
        self.assertAlmostEqual(r["margen_neto"][0], 14.0, delta=0.5)
        self.assertAlmostEqual(r["margen_neto"][-1], 8.0, delta=0.5)
        self.assertAlmostEqual(r["merma_pct"], 7.0, delta=0.4)
        self.assertAlmostEqual(r["crecimiento_pct"], 18.0, delta=2.5)
        self.assertEqual((r["precio_1_julio"], r["precio_14_julio"]), (6.10, 6.90))

    def test_comisiones_por_aplicacion(self):
        rappi = [f for f in leer(self.data / "fue-02-rappi.csv") if f["comision"] and f["monto"]]
        self.assertTrue(all(abs(float(f["comision"]) - round(float(f["monto"]) * 0.30, 2)) < 0.011 for f in rappi))
        self.assertEqual({f["comision_pct"] for f in leer(self.data / "fue-03-pedidosya.csv")}, {"25"})

    def test_participacion_de_las_aplicaciones_sube_de_15_a_35(self):
        ap = self.resumen["participacion_apps"]
        self.assertTrue(abs(ap[0] - 15) <= 2 and abs(ap[-1] - 35) <= 2)
        self.assertTrue(all(b >= a - 0.5 for a, b in zip(ap, ap[1:])))

    def test_cada_tipo_de_defecto_esta_presente_y_cuantificado(self):
        filas = leer(self.data / "respuestas" / "defectos.csv")
        tipos = {f["defecto"] for f in filas}
        self.assertEqual(tipos, set(G.TIPOS))
        self.assertTrue(all(int(f["registros"]) > 0 and f["regla_sugerida"] for f in filas))

    def test_defectos_coinciden_con_lo_que_hay_en_los_archivos(self):
        cont = {(f["fuente"], f["defecto"]): int(f["registros"]) for f in leer(self.data / "respuestas" / "defectos.csv")}
        for fu, archivo in (("fue-01", "fue-01-caja.csv"), ("fue-02", "fue-02-rappi.csv"), ("fue-03", "fue-03-pedidosya.csv"), ("fue-04", "fue-04-whatsapp.csv")):
            vistas, dup = set(), 0
            for f in leer(self.data / archivo):
                k = tuple(f.values())
                dup += k in vistas
                vistas.add(k)
            self.assertEqual(dup, cont.get((fu, "duplicado"), 0), fu)
        d = fecha(self.params["periodo"]["inicio"])
        total = (fecha(self.params["periodo"]["fin"]) - d).days + 1
        self.assertEqual(total - len(leer(self.data / "fue-06-precios-pollo.csv")), cont[("fue-06", "dia_sin_precio")])
        unicas = {tuple(f.values()): f for f in leer(self.data / "fue-01-caja.csv")}.values()   # el duplicado se cuenta solo como duplicado
        self.assertEqual(sum("/" in f["fecha"] for f in unicas), cont[("fue-01", "formato_fecha")])

    def test_hoja_de_respuestas_coincide_con_una_limpieza_de_referencia(self):
        """Limpieza hecha aquí con reglas independientes del generador: debe dar los totales de la hoja de respuestas."""
        esperado, vistos = {}, {}

        def suma(mes, canal, venta, comision):
            x = esperado.setdefault((mes, canal), [0, 0.0, 0.0])
            x[0] += 1
            x[1] += venta
            x[2] += comision

        def nuevo(fu, fila):
            k = (fu, tuple(fila.values()))
            if k in vistos:
                return False
            vistos[k] = True
            return True

        for f in leer(self.data / "fue-01-caja.csv"):
            if not nuevo("1", f) or f["cantidad"] in ("", "0") or f["precio_unitario"] == "":
                continue
            suma(fecha(f["fecha"]).strftime("%Y-%m"), f["canal"], int(f["cantidad"]) * float(f["precio_unitario"]) - float(f["descuento"] or 0), 0.0)
        for f in leer(self.data / "fue-02-rappi.csv"):
            if nuevo("2", f) and f["monto"] != "" and f["estado"] == "ENTREGADO":
                suma(fecha(f["fecha_hora"]).strftime("%Y-%m"), "Rappi", float(f["monto"]), float(f["comision"]))
        for f in leer(self.data / "fue-03-pedidosya.csv"):
            if nuevo("3", f) and f["total"] != "" and f["estado"] == "ENTREGADO":
                suma(fecha(f["fecha"]).strftime("%Y-%m"), "PedidosYa", float(f["total"]), round(float(f["total"]) * int(f["comision_pct"]) / 100, 2))
        for f in leer(self.data / "fue-04-whatsapp.csv"):
            if nuevo("4", f) and f["cantidad"] not in ("", "0") and f["monto"] != "":
                suma(fecha(f["fecha"]).strftime("%Y-%m"), "WhatsApp", float(f["monto"]), 0.0)
        hoja = {(f["mes"], f["canal"]): f for f in leer(self.data / "respuestas" / "ventas-mes-canal.csv")}
        self.assertEqual(set(hoja), set(esperado))
        for k, (n, v, c) in esperado.items():
            self.assertEqual(int(hoja[k]["lineas"]), n, k)
            self.assertAlmostEqual(float(hoja[k]["ventas"]), v, delta=0.05, msg=k)
            self.assertAlmostEqual(float(hoja[k]["comision"]), c, delta=0.05, msg=k)

    def test_margen_por_canal_y_producto_suma_a_la_hoja_de_ventas(self):
        r = self.data / "respuestas"
        base = {(f["mes"], f["canal"]): f for f in leer(r / "ventas-mes-canal.csv")}
        suma = {}
        for f in leer(r / "margen-canal-producto.csv"):
            x = suma.setdefault((f["mes"], f["canal"]), [0, 0.0, 0.0])
            x[0] += int(f["lineas"])
            x[1] += float(f["ventas"])
            x[2] += float(f["comision"])
            venta, com, costo = float(f["ventas"]), float(f["comision"]), float(f["costo_estimado"])
            self.assertAlmostEqual(float(f["margen_contribucion_pct"]), 100 * (venta - com - costo) / venta, delta=0.01)
        self.assertEqual(set(suma), set(base))
        for k, (n, v, c) in suma.items():
            self.assertEqual(n, int(base[k]["lineas"]), k)
            self.assertAlmostEqual(v, float(base[k]["ventas"]), delta=0.1, msg=k)
            self.assertAlmostEqual(c, float(base[k]["comision"]), delta=0.1, msg=k)

    def test_los_martes_sobra_pollo_y_los_domingos_falta(self):
        r = self.data / "respuestas"
        dias = {f["dia_semana"]: f for f in leer(r / "produccion-dia-semana.csv")}
        self.assertEqual(len(dias), 7)
        self.assertGreater(float(dias["Martes"]["merma_pct"]), 9.0)
        self.assertLess(float(dias["Domingo"]["merma_pct"]), 5.0)
        self.assertEqual(sum(int(f["preparados"]) for f in dias.values()), sum(int(f["preparados"]) for f in leer(r / "produccion-mes-turno.csv")))

    def test_precio_diario_con_marca_de_imputado(self):
        r = self.data / "respuestas"
        filas = leer(r / "precio-dia.csv")
        a, b = fecha(self.params["periodo"]["inicio"]), fecha(self.params["periodo"]["fin"])
        self.assertEqual(len(filas), (b - a).days + 1)
        cont = {(f["fuente"], f["defecto"]): int(f["registros"]) for f in leer(r / "defectos.csv")}
        self.assertEqual(sum(int(f["imputado"]) for f in filas), cont[("fue-06", "dia_sin_precio")])
        self.assertEqual(sum(int(f["dias_imputados"]) for f in leer(r / "precio-mes.csv")), cont[("fue-06", "dia_sin_precio")])
        por_dia = {f["fecha"]: float(f["precio_kg"]) for f in filas}
        self.assertEqual((por_dia["2026-07-01"], por_dia["2026-07-14"]), (6.10, 6.90))

    def test_pronostico_de_referencia_y_su_kpi(self):
        r = self.data / "respuestas"
        filas = leer(r / "pronostico-referencia.csv")
        self.assertGreater(len(filas), 1000)
        for f in filas[:200]:
            v, p = float(f["vendidos"]), float(f["pronostico"])
            self.assertAlmostEqual(float(f["error_pct"]), 100 * abs(v - p) / v, delta=0.01)
        kpi5 = [f for f in leer(r / "kpi-esperados.csv") if f["kpi"] == "KPI-05"]
        self.assertEqual(len(kpi5), 15)

    def test_filas_por_fuente_y_calidad(self):
        for f in leer(self.data / "respuestas" / "filas-por-fuente.csv"):
            self.assertLessEqual(int(f["filas_validas"]), int(f["filas_brutas"]))
        k = [float(f["valor"]) for f in leer(self.data / "respuestas" / "kpi-esperados.csv") if f["kpi"] == "KPI-01"]
        self.assertTrue(all(97.0 <= x <= 100 for x in k))

    def test_volumen_y_ventas_coherentes_con_las_uit_del_informe(self):
        self.assertGreaterEqual(sum(self.resumen["filas_brutas"].values()), 90000)
        anual = self.params["ventas_anuales_uit"] * self.params["valor_uit"]
        self.assertAlmostEqual(self.resumen["ventas_ultimos_12"], anual, delta=anual * 0.05)
        self.assertLess(self.segundos, 30)

    def test_cobertura_de_todos_los_dias_y_turnos_de_produccion(self):
        a, b = fecha(self.params["periodo"]["inicio"]), fecha(self.params["periodo"]["fin"])
        dias = {(fecha(f["fecha"]), f["turno"]) for f in leer(self.data / "fue-05-produccion.csv")}
        self.assertEqual(len(dias), ((b - a).days + 1) * 3)
        meses = {fecha(f["fecha"]).strftime("%Y-%m") for f in leer(self.data / "fue-01-caja.csv")}
        self.assertEqual(len(meses), 15)

    def test_costos_operativos_y_catalogo_permiten_calcular_el_margen(self):
        ops = leer(self.data / "apoyo-costos-operativos.csv")
        self.assertEqual(len(ops), 15)
        self.assertTrue(all(int(o["total"]) == sum(int(o[k]) for k in ("planilla", "alquiler", "servicios", "otros")) for o in ops))
        cat = {c["producto"]: c for c in leer(self.data / "apoyo-catalogo-productos.csv")}
        self.assertEqual(len(cat), 8)
        alias = {a for c in cat.values() for a in c["alias"].split("|")}
        usados = {f["producto"] for f in leer(self.data / "fue-02-rappi.csv")}
        self.assertTrue(usados <= set(cat) | alias)

    def test_el_telefono_de_whatsapp_esta_en_la_fuente_para_anonimizarlo(self):
        tel = {f["telefono"] for f in leer(self.data / "fue-04-whatsapp.csv")}
        self.assertTrue(all(len(t) == 9 and t.startswith("9") for t in tel))

    def test_readme_declara_datos_generados(self):
        t = (self.data / "README.md").read_text(encoding="utf-8")
        self.assertIn("Estos datos son generados", t)
        self.assertIn("2025-08-01", t)


class TestToleranciasYParametros(unittest.TestCase):
    def test_cifra_fuera_de_tolerancia_no_entrega_archivos(self):
        p = G.parametros_base()
        p["tolerancias"] = dict(p["tolerancias"], ventas_anuales_pct=0.00001)
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(G.ErrorDatos) as e:
                G.generar(p, Path(d) / "data")
            self.assertIn("ventas de los últimos 12 meses", str(e.exception))
            self.assertEqual(list((Path(d) / "data").glob("*.csv")) if (Path(d) / "data").exists() else [], [])

    def test_los_parametros_salen_del_brief_y_del_informe(self):
        textos = {"brief.md": "| Incluye | Ventas, de abril de 2025 a junio de 2026 |", "secciones/1.3.md": "Con ventas anuales de S/ 3 000 000, equivalentes a unas 500 UIT.\n| UIT de referencia | S/ 5 500 (2026) |"}
        antes = G._texto_vigente
        G._texto_vigente = lambda raiz, paso, archivo: textos.get(archivo, "")
        try:
            p = G.derivar_parametros(".")
        finally:
            G._texto_vigente = antes
        self.assertEqual(p["periodo"], {"inicio": "2025-04-01", "fin": "2026-06-30"})
        self.assertEqual((p["ventas_anuales"], p["ventas_anuales_uit"], p["valor_uit"]), (3000000, 500, 5500))
        self.assertIn("periodo", p["origen"])

    def test_cli_parametros_y_generar_sin_confirmar(self):
        with tempfile.TemporaryDirectory() as d:
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(G.main(["parametros", "--raiz", d]), 0)
                self.assertEqual(G.main(["generar", "--raiz", d]), 0)
            self.assertEqual(json.loads((Path(d) / "data" / "parametros.json").read_text(encoding="utf-8"))["schema"], 1)
            self.assertIn("--confirmar", buf.getvalue())
            self.assertEqual(list((Path(d) / "data").glob("*.csv")), [])

    def test_generar_sin_parametros_falla_con_un_mensaje_claro(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(G.main(["generar", "--raiz", d, "--confirmar"]), 1)


if __name__ == "__main__":
    unittest.main()
