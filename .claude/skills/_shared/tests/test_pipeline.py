import json
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
SKILLS = HERE.parent
PIPE = json.loads((HERE / "pipeline.json").read_text(encoding="utf-8"))["skills"]
SECCIONES_INFORME = ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "1.10",
                     "2.1", "2.2", "2.3", "2.4", "2.5", "3.1", "3.2", "4", "5"]


def instaladas():
    return [s for s in PIPE if (SKILLS / s["nombre"]).is_dir()]


class TestPipeline(unittest.TestCase):
    def test_orden_consecutivo_igual_al_numero(self):
        self.assertEqual([s["orden"] for s in PIPE], list(range(len(PIPE))))
        for s in PIPE:
            self.assertEqual(int(s["nombre"][:2]), s["orden"], s["nombre"])
        self.assertEqual(len({s["nombre"] for s in PIPE}), len(PIPE))

    def test_esquema_de_nombres_y_carpeta_numerada(self):
        for s in PIPE:
            n = s["nombre"]
            self.assertRegex(n, r"^\d{2}-(init|make|design)(-[a-z0-9]+)*$")
            self.assertEqual(n.split("-")[1], s["verbo"], n)
            if s["carpeta"] is None:
                continue
            esperada = n if s["verbo"] == "design" else n.replace("-make-", "-", 1)
            self.assertEqual(s["carpeta"], esperada, n)

    def test_secuencia_completa(self):
        self.assertEqual([s["nombre"] for s in PIPE], [
            "00-init", "01-make-project-brief", "02-design-system", "03-make-business-diagnosis",
            "04-make-strategic-analysis", "05-make-problem-objectives", "06-make-bi-solution",
            "07-make-data-model-kpi", "08-make-etl", "09-make-dashboard", "10-make-storytelling",
            "11-make-conclusions", "12-make-report", "13-make-annex-html"])

    def test_skills_base_instaladas(self):
        for n in ("00-init", "01-make-project-brief", "02-design-system"):
            self.assertTrue((SKILLS / n / "SKILL.md").exists(), n)

    def test_cada_skill_instalada_tiene_su_nombre(self):
        for s in instaladas():
            for nombre in [s["nombre"]] + ([s["nombre"] + "-update"] if s["update"] else []):
                f = SKILLS / nombre / "SKILL.md"
                self.assertTrue(f.exists(), nombre)
                m = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", f.read_text(encoding="utf-8"))
                self.assertIsNotNone(m, nombre)
                self.assertEqual(m.group(1), nombre)
                self.assertLessEqual(len(m.group(2)), 1024, nombre)

    def test_update_declarado_si_y_solo_si_existe(self):
        for s in instaladas():
            self.assertEqual(s["update"], (SKILLS / (s["nombre"] + "-update")).is_dir(), s["nombre"])

    def test_cada_update_tiene_sus_dependencias(self):
        for s in instaladas():
            if s["update"] and s["nombre"] != "00-init":
                self.assertTrue((SKILLS / (s["nombre"] + "-update") / "references" / "dependencias.md").exists(), s["nombre"])

    def test_no_hay_skills_numeradas_fuera_del_pipeline(self):
        nombres = {s["nombre"] for s in PIPE} | {s["nombre"] + "-update" for s in PIPE}
        for d in SKILLS.iterdir():
            if d.is_dir() and d.name[:2].isdigit():
                self.assertIn(d.name, nombres, d.name)

    def test_prerrequisitos_son_pasos_anteriores(self):
        orden = {s["nombre"]: s["orden"] for s in PIPE}
        for s in PIPE:
            self.assertNotIn("requiere_por_avance", s, s["nombre"])
            for r in s["requiere"]:
                self.assertIn(r, orden, s["nombre"])
                self.assertLess(orden[r], s["orden"], f"{s['nombre']} requiere {r}")

    def test_carpetas_de_corrida_unicas(self):
        carpetas = [s["carpeta"] for s in PIPE if s["carpeta"]]
        self.assertEqual(len(carpetas), len(set(carpetas)))

    def test_secciones_unicas_y_completas(self):
        todas = [x for s in PIPE for x in s["secciones"]]
        self.assertEqual(len(todas), len(set(todas)), "sección declarada en dos skills")
        self.assertEqual(todas, SECCIONES_INFORME)

    def test_las_rutas_citadas_en_las_skills_existen(self):
        repo = SKILLS.parent.parent
        for d in SKILLS.iterdir():
            f = d / "SKILL.md"
            if not (d.is_dir() and d.name[:2].isdigit() and f.exists()):
                continue
            for p in set(re.findall(r"`((?:common|\.claude/skills/_shared)/[\w./-]+)`", f.read_text(encoding="utf-8"))):
                self.assertTrue((repo / p.rstrip(".")).exists(), f"{d.name}: {p}")


if __name__ == "__main__":
    unittest.main()
