import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import brief as BR  # noqa: E402
import brief_fixtures as F  # noqa: E402
import projectcfg as P  # noqa: E402
import runs as RUNS  # noqa: E402
import validate_run as V  # noqa: E402

FILA_OE2 = "| OE-02 | Medir la rentabilidad real de cada canal de venta | Canales con margen calculado | 5 de 5 canales | Entrega (30-11-2026) | OG-01 | Margen neto por canal |"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run = F.crear(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def msgs(self, run=None):
        return [f"{f}: {m}" for f, m in V.validate(run or self.run)]

    def edita(self, a, b):
        f = self.run / "brief.md"
        t = f.read_text(encoding="utf-8")
        assert a in t, a
        f.write_text(t.replace(a, b, 1), encoding="utf-8")


class TestLectura(Base):
    def test_el_ejemplo_se_lee_completo(self):
        d = BR.vigente(self.root)
        self.assertEqual(d["nombre"], "Rentabilidad por canal de Pollería Don Tito")
        self.assertEqual(d["secciones"], BR.SECCIONES)
        self.assertTrue(d["tema"].startswith("Un dashboard en Power BI para que la gerencia"))
        self.assertNotIn("Empresa", d["tema"])
        self.assertTrue(d["empresa"].startswith("Pollería Don Tito"))
        self.assertEqual([o["codigo"] for o in d["og"]], ["OG-01"])
        self.assertEqual([o["codigo"] for o in d["oe"]], ["OE-01", "OE-02", "OE-03"])
        self.assertEqual(d["oe"][0]["plazo"], "Entrega (30-11-2026)")
        self.assertEqual(d["oe"][1]["indicador"], "Margen neto por canal")
        self.assertEqual(d["oe"][0]["aporta"], "OG-01")
        self.assertEqual(len(d["problematica"]["evidencia"]), 2)
        self.assertEqual(len(d["decisiones"]), 3)
        self.assertEqual([f["tipo"] for f in d["fuentes"]], ["Generada", "Generada", "Abierta"])
        self.assertEqual(d["calendario"], {"inicio": "01-11-2026", "entrega": "30-11-2026"})
        self.assertEqual([i["codigo"] for i in d["iniciales"]], ["INI-01", "INI-02"])
        self.assertEqual({a["alcance"] for a in d["alcance"]}, {"Incluye", "No incluye", "Herramientas previstas"})

    def test_sin_corrida_vigente(self):
        with tempfile.TemporaryDirectory() as t:
            cfg = P.new_config()
            cfg["proyecto"] = {"nombre": "X", "tema": "", "tipo": "propio", "ruc": None, "rubro": "R"}
            P.save(cfg, t)
            with self.assertRaises(BR.SinBrief):
                BR.vigente(t)

    def test_copia_al_config(self):
        cfg = P.load(self.root)
        self.assertTrue(cfg["proyecto"]["tema"].startswith("Un dashboard en Power BI"))
        self.assertEqual(cfg["calendario"], {"inicio": "01-11-2026", "entrega": "30-11-2026"})

    def test_pendiente_pasa_a_none_en_el_config(self):
        self.edita("| 01-11-2026 | 30-11-2026 |", "| 01-11-2026 | Pendiente |")
        BR.al_config(self.root)
        self.assertEqual(P.load(self.root)["calendario"], {"inicio": "01-11-2026", "entrega": None})

    def test_cli(self):
        self.assertEqual(BR.main(["leer", "--raiz", str(self.root)]), 0)
        self.assertEqual(BR.main(["al-config", "--raiz", str(self.root)]), 0)
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(BR.main(["leer", "--raiz", t]), 1)


class TestValidacion(Base):
    def test_el_ejemplo_es_valido(self):
        self.assertEqual(self.msgs(), [])

    def test_carpeta_numerada(self):
        self.assertEqual(self.run.parent.name, "01-project-brief")

    def test_falta_una_seccion(self):
        self.edita("## 6. Fuentes de datos previstas", "## 6. Otra cosa")
        self.assertIn("brief.md: falta el encabezado «## 6. Fuentes de datos previstas»", self.msgs())

    def test_falta_una_subseccion(self):
        self.edita("### 4.2. Limitaciones", "#### Limitaciones")
        self.assertTrue(any("falta el encabezado «### 4.2.» en la sección 4" in m for m in self.msgs()))

    def test_secciones_fuera_de_orden(self):
        t = (self.run / "brief.md").read_text(encoding="utf-8")
        a = t.index("## 6. Fuentes de datos previstas")
        b = t.index("## 7. Calendario")
        c = t.index("## 8. Supuestos")
        (self.run / "brief.md").write_text(t[:a] + t[b:c] + t[a:b] + t[c:], encoding="utf-8")
        self.assertTrue(any("orden del brief" in m for m in self.msgs()))

    def test_objetivo_sin_metrica_ni_meta(self):
        self.edita(FILA_OE2, "| OE-02 | Medir la rentabilidad real de cada canal de venta |  |  | Entrega (30-11-2026) | OG-01 | Margen neto por canal |")
        m = self.msgs()
        self.assertIn("brief.md: OE-02: falta la metrica", m)
        self.assertIn("brief.md: OE-02: falta la meta", m)

    def test_justificacion_en_un_rotulo_de_uno_o_dos_parrafos(self):
        d = BR.vigente(self.root)
        self.assertEqual(d["justificacion_parrafos"], 2)
        self.assertIn("fijar precios por canal", d["justificacion"])
        self.assertEqual(self.msgs(), [])

    def test_justificacion_con_tres_parrafos(self):
        self.edita("Una solución de BI integra fuentes dispersas", "Un tercer párrafo cualquiera.\n\nUna solución de BI integra fuentes dispersas")
        self.assertTrue(any("la justificación tiene 3 párrafos; debe ser uno o dos" in m for m in self.msgs()), self.msgs())

    def test_sin_justificacion(self):
        self.edita("**Justificación.**", "**Motivo.**")
        self.assertTrue(any("falta la «**Justificación.**»" in m for m in self.msgs()), self.msgs())

    def test_objetivo_sin_indicador(self):
        self.edita(FILA_OE2, FILA_OE2.replace("| Margen neto por canal |", "|  |"))
        self.assertIn("brief.md: OE-02: falta el indicador", self.msgs())

    def test_objetivo_que_no_aporta_al_general(self):
        self.edita("| Entrega (30-11-2026) | OG-01 | Calidad", "| Entrega (30-11-2026) | — | Calidad")
        self.assertIn("brief.md: OE-01: «Aporta a» debe ser OG-01", self.msgs())

    def test_pocos_objetivos_especificos(self):
        t = (self.run / "brief.md").read_text(encoding="utf-8")
        t = re.sub(r"\| OE-0[23] .*\n", "", t)
        (self.run / "brief.md").write_text(t, encoding="utf-8")
        self.assertIn("brief.md: debe haber al menos dos objetivos específicos OE-nn", self.msgs())

    def test_plazo_fuera_del_calendario(self):
        self.edita(FILA_OE2, FILA_OE2.replace("Entrega (30-11-2026)", "Entrega (28-11-2026)"))
        self.assertIn("brief.md: OE-02: el plazo cita 28-11-2026 y la entrega del calendario es 30-11-2026", self.msgs())

    def test_plazo_mal_escrito(self):
        self.edita(FILA_OE2, FILA_OE2.replace("Entrega (30-11-2026)", "Avance 3 (30-11-2026)"))
        self.assertTrue(any("OE-02: el plazo debe ser «Entrega (DD-MM-AAAA)»" in m for m in self.msgs()))

    def test_plazo_pendiente(self):
        self.edita(FILA_OE2, FILA_OE2.replace("Entrega (30-11-2026)", "Entrega (Pendiente)"))
        self.assertEqual(self.msgs(), [])

    def test_entrega_antes_del_inicio(self):
        self.edita("| 01-11-2026 | 30-11-2026 |", "| 01-11-2026 | 30-10-2026 |")
        self.assertTrue(any("la entrega (30-10-2026) es anterior al inicio (01-11-2026)" in x for x in self.msgs()))

    def test_fecha_invalida_y_pendiente(self):
        self.edita("| 01-11-2026 | 30-11-2026 |", "| 31-02-2026 | Pendiente |")
        m = self.msgs()
        self.assertTrue(any("«31-02-2026» no es una fecha DD-MM-AAAA válida" in x for x in m))
        self.assertFalse(any("Entrega: «Pendiente»" in x for x in m))

    def test_calendario_con_dos_filas(self):
        self.edita("| 01-11-2026 | 30-11-2026 |", "| 01-11-2026 | 30-11-2026 |\n| 01-12-2026 | 31-12-2026 |")
        self.assertIn("brief.md: el calendario debe tener una sola fila con «Inicio» y «Entrega»", self.msgs())

    def test_fuente_con_tipo_o_acceso_invalido(self):
        self.edita("| FUE-03 | Precios del pollo vivo en Lima Metropolitana | Abierta |", "| FUE-03 | Precios del pollo vivo en Lima Metropolitana | Web |")
        self.edita("| Precio diario por kilogramo | Público |", "| Precio diario por kilogramo | Libre |")
        m = self.msgs()
        self.assertTrue(any("FUE-03: el tipo debe ser" in x for x in m))
        self.assertTrue(any("FUE-03: el acceso debe ser" in x for x in m))

    def test_sin_decisiones(self):
        t = (self.run / "brief.md").read_text(encoding="utf-8")
        t = re.sub(r"\*\*Decisiones que apoyará el dashboard\.\*\*\n(- .+\n)+", "", t)
        (self.run / "brief.md").write_text(t, encoding="utf-8")
        self.assertTrue(any("Decisiones que apoyará el dashboard" in x for x in self.msgs()))

    def test_vacios(self):
        self.edita("**Usuarios.** Gerente general (decide) y jefe de cocina (ejecuta la producción).", "**Usuarios.** ")
        self.assertTrue(any("«Usuarios» está vacío" in x for x in self.msgs()))

    def test_pendiente_es_un_valor_valido(self):
        self.edita("**Usuarios.** Gerente general (decide) y jefe de cocina (ejecuta la producción).", "**Usuarios.** Pendiente")
        self.assertEqual(self.msgs(), [])

    def test_supuestos_y_riesgos(self):
        self.edita("| INI-01 | Supuesto |", "| INI-01 | Idea |")
        self.assertIn("brief.md: INI-01: el tipo debe ser Supuesto o Riesgo", self.msgs())

    def test_falta_alcance_no_incluye(self):
        self.edita("| No incluye | Contabilidad completa, planillas ni predicción de demanda |\n", "")
        self.assertTrue(any("«Incluye» y «No incluye»" in x for x in self.msgs()))

    def test_config_distinto_del_brief(self):
        P.set_nucleo(tema="Otro tema", root=self.root)
        P.set_nucleo(entrega="29-11-2026", root=self.root)
        m = self.msgs()
        self.assertTrue(any("el tema del config" in x and "01-make-project-brief-update" in x for x in m), m)
        self.assertTrue(any("calendario.entrega del config (29-11-2026) difiere del calendario del brief (30-11-2026)" in x for x in m), m)

    def test_falta_domain_md(self):
        (self.root / "project" / "domain.md").unlink()
        self.assertTrue(any("falta domain.md" in x for x in self.msgs()))

    def test_texto_prohibido(self):
        self.edita("Las fuentes abiertas de precios", "Datos falsos de prueba de precios")
        self.assertTrue(any("término no permitido" in x for x in self.msgs()))


class TestFlujo(Base):
    STEP = "01-make-project-brief"

    def test_flujo_de_la_skill(self):
        self.assertEqual(P.step_info(self.STEP)["carpeta"], "01-project-brief")
        self.assertEqual(P.current_run(self.STEP, self.root), F.RUN)
        self.assertEqual(self.msgs(), [])
        self.assertEqual([a for a in P.check(self.STEP, self.root) if "falta el brief" in a], [])

    def test_el_brief_no_aporta_secciones_al_informe(self):
        self.assertTrue(all(x["estado"] == "pendiente" for x in P.secciones(self.root)))

    def test_update_solo_cambia_lo_afectado(self):
        base = self.run
        fork = RUNS.fork(self.STEP, ["mover la entrega"], root=self.root)
        t = (fork / "brief.md").read_text(encoding="utf-8")
        t = t.replace("| 01-11-2026 | 30-11-2026 |", "| 01-11-2026 | 05-12-2026 |").replace("Entrega (30-11-2026)", "Entrega (05-12-2026)")
        (fork / "brief.md").write_text(t, encoding="utf-8")
        BR.al_config(self.root, fork.name)
        self.assertEqual(self.msgs(fork), [])
        a = (base / "brief.md").read_text(encoding="utf-8").splitlines()
        b = (fork / "brief.md").read_text(encoding="utf-8").splitlines()
        cambiadas = [(x, y) for x, y in zip(a, b) if x != y]
        self.assertEqual(len(a), len(b))
        self.assertEqual(len(cambiadas), 5)  # OG-01, tres OE y la fila del calendario
        self.assertEqual(P.load(self.root)["calendario"]["entrega"], "05-12-2026")

    def test_el_config_sin_copiar_se_detecta(self):
        with tempfile.TemporaryDirectory() as t:
            run = F.crear(t, copiar_al_config=False)
            m = [f"{a}: {b}" for a, b in V.validate(run)]
            self.assertTrue(any("el tema del config" in x for x in m))
            BR.al_config(t)
            self.assertEqual([f"{a}: {b}" for a, b in V.validate(run)], [])


if __name__ == "__main__":
    unittest.main()
