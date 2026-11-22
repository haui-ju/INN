"""El índice maestro del informe (common/structure/model1.md) y su coherencia con pipeline.json."""
import json
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
INDICE = HERE.parents[2] / "common" / "structure" / "model1.md"
PIPE = json.loads((HERE / "pipeline.json").read_text(encoding="utf-8"))["skills"]
PUNTO = re.compile(r"^- (\d+(?:\.\d+)?)\. (.+)$")


def puntos():
    out = []
    for linea in INDICE.read_text(encoding="utf-8").splitlines():
        m = PUNTO.match(linea)
        if m:
            out.append((m.group(1), m.group(2), "(incluye imagen)" in m.group(2)))
    return out


class TestIndice(unittest.TestCase):
    def test_cinco_capitulos_en_orden(self):
        caps = re.findall(r"(?m)^## Capítulo (\d+): (.+)$", INDICE.read_text(encoding="utf-8"))
        self.assertEqual([int(n) for n, _ in caps], [1, 2, 3, 4, 5])
        self.assertEqual(caps[0][1], "Diagnóstico estratégico y análisis del negocio")
        self.assertEqual(caps[1][1], "Diseño técnico de solución en Inteligencia de Negocios")
        self.assertEqual(caps[2][1], "Construcción y calidad del dashboard en Power BI")

    def test_numeracion_sin_saltos_ni_repetidos(self):
        nums = [n for n, _, _ in puntos()]
        self.assertEqual(len(nums), len(set(nums)))
        por_cap = {}
        for n in nums:
            cap, _, sub = n.partition(".")
            por_cap.setdefault(int(cap), []).append(int(sub) if sub else 0)
        for cap, subs in por_cap.items():
            esperado = [0] if subs == [0] else list(range(1, len(subs) + 1))
            self.assertEqual(subs, esperado, f"capítulo {cap}")

    def test_cada_punto_tiene_una_skill_y_viceversa(self):
        indice = [n for n, _, _ in puntos()]
        pipeline = [x for s in PIPE for x in s["secciones"]]
        self.assertEqual(indice, pipeline)

    def test_puntos_del_capitulo_1(self):
        cap1 = {n: t for n, t, _ in puntos() if n.startswith("1.")}
        for n, palabra in (("1.1", "Nombre de la empresa"), ("1.2", "Misión y visión"), ("1.3", "Industria y tamaño"),
                           ("1.4", "Business Model Canvas"), ("1.5", "PESTEL"), ("1.6", "FODA"), ("1.7", "Ishikawa"),
                           ("1.8", "Problemática central"), ("1.9", "Objetivo general"), ("1.10", "Objetivos específicos")):
            self.assertIn(palabra, cap1[n], n)

    def test_marca_de_imagen(self):
        con = [n for n, _, img in puntos() if img]
        self.assertEqual(con, ["1.4", "1.5", "1.6", "1.7", "2.2", "2.4", "3.2", "4"])
        self.assertFalse(dict((n, i) for n, _, i in puntos())["1.1"])

    def test_sin_marcas_de_avance_ni_versiones(self):
        txt = INDICE.read_text(encoding="utf-8")
        self.assertNotRegex(txt, r"\[A[123]\+?\]")
        self.assertNotIn("Historial de versiones", txt)
        self.assertNotIn("trasladable", txt)

    def test_anexos_a_d(self):
        anexos = re.findall(r"(?m)^- Anexo ([A-Z]): (.+)$", INDICE.read_text(encoding="utf-8"))
        self.assertEqual([a for a, _ in anexos], ["A", "B", "C", "D"])
        self.assertIn("Diccionario de datos", anexos[0][1])
        self.assertIn("Referencias bibliográficas", INDICE.read_text(encoding="utf-8"))

    def test_reglas_de_contenido(self):
        txt = INDICE.read_text(encoding="utf-8")
        self.assertIn("**Reglas de contenido.**", txt)
        self.assertIn("se cita por su número", txt)


if __name__ == "__main__":
    unittest.main()
