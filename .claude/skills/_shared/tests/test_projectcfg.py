import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import projectcfg as P  # noqa: E402

DIAG = "03-make-business-diagnosis"
ESTR = "04-make-strategic-analysis"
OBJ = "05-make-problem-objectives"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "project").mkdir()
        (self.root / ".claude" / "skills").mkdir(parents=True)
        cfg = P.new_config()
        cfg["proyecto"] = {"nombre": "X", "tema": "T", "tipo": "propio", "ruc": None, "rubro": "R"}
        P.save(cfg, self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def txt(self):
        return P.config_path(self.root).read_text(encoding="utf-8")


class TestValidacion(Base):
    def test_config_nuevo(self):
        cfg = P.load(self.root)
        self.assertEqual(cfg["schema"], 3)
        self.assertEqual(cfg["calendario"], {"inicio": None, "entrega": None})
        self.assertEqual(cfg["pasos"], {})
        for k in ("enfoque", "resultado_esperado", "avances"):
            self.assertNotIn(k, cfg)
        secs = cfg["informe"]["secciones"]
        self.assertEqual(list(secs)[:2], ["1.1", "1.2"])
        self.assertEqual(list(secs)[-1], "5")
        self.assertTrue(all(e["estado"] == "pendiente" and e["run"] is None for e in secs.values()))
        self.assertEqual(secs["1.6"]["skill"], ESTR)

    def test_schema_desconocido(self):
        P.config_path(self.root).write_text("schema: 99\n", encoding="utf-8")
        with self.assertRaises(P.ConfigError) as cm:
            P.load(self.root)
        self.assertIn("99", str(cm.exception))

    def test_schema_2_rechazado_remite_a_00_init(self):
        P.config_path(self.root).write_text("schema: 2\n", encoding="utf-8")
        with self.assertRaises(P.ConfigError) as cm:
            P.load(self.root)
        self.assertIn("00-init", str(cm.exception))

    def test_modo_datos_invalido(self):
        cfg = P.load(self.root)
        cfg["modo_datos"] = "simulado"
        with self.assertRaises(P.ConfigError):
            P.save(cfg, self.root)

    def test_texto_no_permitido(self):
        cfg = P.load(self.root)
        cfg["proyecto"]["tema"] = "datos de prueba"
        with self.assertRaises(P.ConfigError):
            P.save(cfg, self.root)

    def test_yaml_invalido(self):
        P.config_path(self.root).write_text("schema: 3\nproyecto: [1, 2]\n", encoding="utf-8")
        with self.assertRaises(P.ConfigError) as cm:
            P.load(self.root)
        self.assertIn("YAML", str(cm.exception))
        self.assertIn("línea 2", str(cm.exception))

    def test_tipo_empresa_exige_ruc_de_11_digitos(self):
        cfg = P.load(self.root)
        cfg["proyecto"]["tipo"] = "empresa"
        with self.assertRaises(P.ConfigError):
            P.save(cfg, self.root)
        cfg["proyecto"]["ruc"] = "123"
        with self.assertRaises(P.ConfigError):
            P.save(cfg, self.root)
        cfg["proyecto"]["ruc"] = "20123456789"
        P.save(cfg, self.root)
        self.assertEqual(P.load(self.root)["proyecto"]["ruc"], "20123456789")

    def test_tipo_propio_sin_ruc(self):
        cfg = P.load(self.root)
        cfg["proyecto"]["ruc"] = "20123456789"
        with self.assertRaises(P.ConfigError):
            P.save(cfg, self.root)

    def test_tipo_invalido(self):
        cfg = P.load(self.root)
        cfg["proyecto"]["tipo"] = "otro"
        with self.assertRaises(P.ConfigError):
            P.save(cfg, self.root)

    def test_comentarios_se_conservan_al_registrar(self):
        self.assertIn("modo_datos: generado  # generado = datos generados para el proyecto", self.txt())
        P.register(DIAG, "A", root=self.root)
        txt = self.txt()
        self.assertIn("modo_datos: generado  # generado", txt)
        self.assertIn("run: A  # carpeta de la corrida vigente", txt)
        self.assertIn("fijada: false  # true = ninguna corrida nueva", txt)
        self.assertIn("estado: disponible  # disponible = tiene corrida", txt)

    def test_set_diseno_respeta_fijada(self):
        self.assertTrue(P.set_diseno("project/02-design-system/X/DESIGN.md", self.root))
        self.assertEqual(P.load(self.root)["diseno"], "project/02-design-system/X/DESIGN.md")
        cfg = P.load(self.root)
        cfg["pasos"]["02-design-system"] = {"run": "X", "fijada": True, "historial": ["X"]}
        P.save(cfg, self.root)
        self.assertFalse(P.set_diseno("project/02-design-system/Y/DESIGN.md", self.root))
        self.assertEqual(P.load(self.root)["diseno"], "project/02-design-system/X/DESIGN.md")


class TestCalendario(Base):
    def test_fechas_validas_y_orden(self):
        cfg = P.load(self.root)
        cfg["calendario"]["inicio"] = "31-02-2026"
        self.assertTrue(any("no es una fecha DD-MM-AAAA válida" in e for e in P.validate(cfg)))
        cfg["calendario"] = {"inicio": "01-11-2026", "entrega": "30-10-2026"}
        self.assertTrue(any("igual o posterior al inicio" in e for e in P.validate(cfg)))
        cfg["calendario"]["entrega"] = "01-11-2026"
        self.assertEqual(P.validate(cfg), [])

    def test_fecha_pendiente(self):
        cfg = P.load(self.root)
        cfg["calendario"] = {"inicio": "01-11-2026", "entrega": None}
        self.assertEqual(P.validate(cfg), [])

    def test_set_nucleo_copia_y_conserva_comentarios(self):
        r = P.set_nucleo("Tema nuevo", inicio="01-11-2026", entrega="30-11-2026", root=self.root)
        cfg = P.load(self.root)
        self.assertEqual(cfg["proyecto"]["tema"], "Tema nuevo")
        self.assertEqual(cfg["calendario"], {"inicio": "01-11-2026", "entrega": "30-11-2026"})
        self.assertEqual(r["calendario"]["entrega"], "30-11-2026")
        self.assertIn("lo define 01-make-project-brief", self.txt())

    def test_set_nucleo_rechaza_sin_escribir(self):
        antes = self.txt()
        with self.assertRaises(P.ConfigError):
            P.set_nucleo(inicio="01-11-2026", entrega="30-10-2026", root=self.root)
        self.assertEqual(self.txt(), antes)

    def test_cli_set_nucleo(self):
        os.environ["PROJECT_ROOT"] = str(self.root)
        try:
            self.assertEqual(P.main(["set-nucleo", "--tema", "T", "--inicio", "01-11-2026", "--entrega", "30-11-2026"]), 0)
            self.assertEqual(P.load(self.root)["calendario"]["entrega"], "30-11-2026")
            self.assertEqual(P.main(["set-nucleo", "--entrega", "-"]), 0)
            self.assertIsNone(P.load(self.root)["calendario"]["entrega"])
            self.assertEqual(P.main(["set-nucleo", "--entrega", "mal"]), 1)
        finally:
            os.environ.pop("PROJECT_ROOT", None)


class TestRoles(Base):
    NOMBRES = ["ariel", "Piero", "ju"]

    def setUp(self):
        super().setUp()
        cfg = P.load(self.root)
        cfg["equipo"] = [{"nombre": n, "rol": None} for n in self.NOMBRES]
        P.save(cfg, self.root)

    def roles(self):
        return {m["nombre"]: m["rol"] for m in P.load(self.root)["equipo"]}

    def test_reparto_valido_parcial(self):
        P.set_roles({"ariel": "Analista de datos", "ju": "Desarrollador Power BI"}, self.root)
        self.assertEqual(self.roles(), {"ariel": "Analista de datos", "Piero": None, "ju": "Desarrollador Power BI"})
        self.assertIn("rol: Analista de datos  # responsabilidad en el proyecto", self.txt())

    def test_integrante_sin_rol_aceptado(self):
        self.assertEqual(P.validate(P.load(self.root)), [])

    def _rechaza(self, reparto, fragmento):
        antes = self.txt()
        with self.assertRaises(P.ConfigError) as cm:
            P.set_roles(reparto, self.root)
        self.assertIn(fragmento, str(cm.exception))
        self.assertEqual(self.txt(), antes)

    def test_persona_ausente(self):
        self._rechaza({"ariel": "Analista", "Luis": "Diseñador"}, "Luis no pertenece al equipo")

    def test_rol_vacio_o_largo(self):
        self._rechaza({"ariel": "  "}, "entre 1 y 60")
        self._rechaza({"ariel": "x" * 61}, "entre 1 y 60")


class TestRegistro(Base):
    def test_corrida_nueva_mueve_el_puntero(self):
        P.register(DIAG, "A", root=self.root)
        r = P.register(DIAG, "B", root=self.root)
        e = P.load(self.root)["pasos"][DIAG]
        self.assertTrue(r["movido"])
        self.assertEqual((e["run"], e["historial"]), ("B", ["A", "B"]))

    def test_fijada_no_mueve_el_puntero(self):
        P.register(DIAG, "A", root=self.root)
        cfg = P.load(self.root)
        cfg["pasos"][DIAG]["fijada"] = True
        P.save(cfg, self.root)
        r = P.register(DIAG, "B", root=self.root)
        e = P.load(self.root)["pasos"][DIAG]
        self.assertFalse(r["movido"])
        self.assertEqual((e["run"], e["historial"]), ("A", ["A", "B"]))

    def test_no_mover_conserva_puntero(self):
        P.register(DIAG, "A", root=self.root)
        r = P.register(DIAG, "B-fork", root=self.root, mover=False)
        e = P.load(self.root)["pasos"][DIAG]
        self.assertFalse(r["movido"])
        self.assertEqual((e["run"], e["historial"]), ("A", ["A", "B-fork"]))

    def test_sin_duplicados_en_historial(self):
        P.register(DIAG, "A", root=self.root)
        P.register(DIAG, "A", root=self.root)
        self.assertEqual(P.load(self.root)["pasos"][DIAG]["historial"], ["A"])

    def test_paso_desconocido(self):
        with self.assertRaises(P.ConfigError):
            P.register("05-make-design-thinking", "A", root=self.root)

    def test_salida(self):
        P.set_salida("09-make-dashboard", "enlace", "https://app.powerbi.com/x", self.root)
        self.assertEqual(P.load(self.root)["pasos"]["09-make-dashboard"]["salidas"]["enlace"], "https://app.powerbi.com/x")


class TestSecciones(Base):
    def estado(self):
        return {s: (e["estado"], e["run"]) for s, e in P.load(self.root)["informe"]["secciones"].items()}

    def test_skill_terminada_marca_sus_secciones(self):
        r = P.register(ESTR, "A", root=self.root)
        self.assertEqual(r["secciones"], ["1.5", "1.6", "1.7"])
        st = self.estado()
        for s in ("1.5", "1.6", "1.7"):
            self.assertEqual(st[s], ("disponible", "A"))
        self.assertEqual(st["1.4"], ("pendiente", None))

    def test_update_fallido_conserva_run(self):
        P.register(ESTR, "A", root=self.root)
        P.register(ESTR, "A-fork", root=self.root, mover=False)
        self.assertEqual(self.estado()["1.6"], ("disponible", "A"))

    def test_update_valido_mueve_run(self):
        P.register(ESTR, "A", root=self.root)
        P.register(ESTR, "A-fork", root=self.root)
        self.assertEqual(self.estado()["1.6"], ("disponible", "A-fork"))

    def test_paso_fijado(self):
        P.register(ESTR, "A", root=self.root)
        cfg = P.load(self.root)
        cfg["pasos"][ESTR]["fijada"] = True
        P.save(cfg, self.root)
        P.register(ESTR, "B", root=self.root)
        self.assertEqual(self.estado()["1.5"], ("disponible", "A"))

    def test_skill_sin_secciones(self):
        r = P.register("01-make-project-brief", "B", root=self.root)
        self.assertEqual(r["secciones"], [])
        self.assertTrue(all(e == ("pendiente", None) for e in self.estado().values()))

    def _crear_runs(self):
        for paso, carpeta in ((DIAG, "03-business-diagnosis"), (ESTR, "04-strategic-analysis"), (OBJ, "05-problem-objectives")):
            (self.root / "project" / carpeta / "A").mkdir(parents=True)
            P.register(paso, "A", root=self.root)

    def test_consulta_informe_parcial(self):
        self._crear_runs()
        res = P.secciones(self.root)
        disp = [x["seccion"] for x in res if x["estado"] == "disponible"]
        pend = {x["seccion"]: x["skill"] for x in res if x["estado"] == "pendiente"}
        self.assertEqual(disp, ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "1.10"])
        self.assertEqual(pend["2.1"], "06-make-bi-solution")
        self.assertEqual(pend["5"], "11-make-conclusions")

    def test_consulta_sin_secciones(self):
        res = P.secciones(self.root)
        self.assertTrue(all(x["estado"] == "pendiente" and x["motivo"].startswith("falta ejecutar") for x in res))

    def test_carpeta_borrada(self):
        self._crear_runs()
        (self.root / "project" / "04-strategic-analysis" / "A").rmdir()
        res = {x["seccion"]: x for x in P.secciones(self.root)}
        self.assertEqual(res["1.6"]["estado"], "pendiente")
        self.assertIn("no existe la carpeta", res["1.6"]["motivo"])
        self.assertEqual(self.estado()["1.6"], ("disponible", "A"))  # no se borra el registro

    def _escribir_sin_validar(self, cfg):
        import yamlmini
        P.config_path(self.root).write_text(yamlmini.dumps(cfg, P.comentario), encoding="utf-8")

    def test_seccion_desconocida(self):
        cfg = P.load(self.root)
        cfg["informe"]["secciones"]["9.9"] = {"skill": "x", "run": None, "estado": "pendiente"}
        self._escribir_sin_validar(cfg)
        with self.assertRaises(P.ConfigError) as cm:
            P.load(self.root)
        self.assertIn("9.9", str(cm.exception))

    def test_seccion_nueva_se_completa(self):
        cfg = P.load(self.root)
        del cfg["informe"]["secciones"]["2.4"]
        self._escribir_sin_validar(cfg)
        secs = list(P.load(self.root)["informe"]["secciones"])
        self.assertIn("2.4", secs)
        self.assertEqual(secs.index("2.4"), secs.index("2.5") - 1)

    def test_skill_equivocada(self):
        cfg = P.load(self.root)
        cfg["informe"]["secciones"]["1.1"]["skill"] = OBJ
        self.assertTrue(any("1.1.skill" in e for e in P.validate(cfg)))

    def test_cli_secciones(self):
        os.environ["PROJECT_ROOT"] = str(self.root)
        try:
            self.assertEqual(P.main(["secciones"]), 0)
            self.assertEqual(P.main(["secciones", "--json"]), 0)
        finally:
            os.environ.pop("PROJECT_ROOT", None)


class TestPrerrequisitos(Base):
    def setUp(self):
        super().setUp()
        (self.root / "project" / "domain.md").write_text("# Dominio\n", encoding="utf-8")

    def instalar(self, *skills):
        for s in skills:
            (self.root / ".claude" / "skills" / s).mkdir()

    def test_carpeta_inexistente_avisada(self):
        self.instalar(DIAG)
        P.register("01-make-project-brief", "B", root=self.root)
        P.register(DIAG, "NOEXISTE", root=self.root)
        av = P.check(ESTR, self.root)
        self.assertTrue(any("NOEXISTE" in a and "no existe" in a for a in av))

    def test_paso_instalado_sin_corrida_avisa(self):
        self.instalar(DIAG)
        av = P.check(ESTR, self.root)
        self.assertTrue(any(DIAG in a for a in av))

    def test_aviso_si_falta_domain_md(self):
        (self.root / "project" / "domain.md").unlink()
        self.assertTrue(any("domain.md" in a for a in P.check(DIAG, self.root)))
        self.assertFalse(any("domain.md" in a for a in P.check("01-make-project-brief", self.root)))

    def test_prerrequisito_no_instalado_se_omite(self):
        P.register("01-make-project-brief", "B", root=self.root)
        self.assertEqual(P.check("08-make-etl", self.root), [])

    def test_corrida_existente_sin_avisos(self):
        self.instalar(DIAG)
        (self.root / "project" / "03-business-diagnosis" / "A").mkdir(parents=True)
        P.register(DIAG, "A", root=self.root)
        P.register("01-make-project-brief", "B", root=self.root)
        self.assertEqual(P.check(ESTR, self.root), [])

    def test_aviso_si_falta_el_brief_desde_la_skill_03(self):
        for skill in (DIAG, "07-make-data-model-kpi", "12-make-report"):
            self.assertTrue(any("brief" in a and "01-make-project-brief" in a for a in P.check(skill, self.root)), skill)
        for skill in ("00-init", "01-make-project-brief", "02-design-system"):
            self.assertFalse(any("falta el brief" in a for a in P.check(skill, self.root)), skill)
        P.register("01-make-project-brief", "B", root=self.root)
        self.assertFalse(any("falta el brief" in a for a in P.check(DIAG, self.root)))

    def test_cli_check_sin_avance(self):
        os.environ["PROJECT_ROOT"] = str(self.root)
        try:
            self.assertEqual(P.main(["check", "--skill", DIAG]), 0)
            with self.assertRaises(SystemExit):
                P.main(["check", "--skill", DIAG, "--avance", "1"])
        finally:
            os.environ.pop("PROJECT_ROOT", None)


if __name__ == "__main__":
    unittest.main()
