import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import yamlmini as Y  # noqa: E402

SAMPLE = {
    "schema": 3,
    "proyecto": {"nombre": "Pollería: canales", "tema": "Margen # 1", "tipo": "empresa", "ruc": "20123456789", "rubro": "Restaurantes"},
    "calendario": {"inicio": "01-11-2026", "entrega": None},
    "equipo": [{"nombre": "ariel", "rol": None}, {"nombre": "Piero", "rol": "Analista de datos"}],
    "informe": {"secciones": {"1.1": {"skill": "03-make-business-diagnosis", "run": None, "estado": "pendiente"}}},
    "kpi": [{"n": 1, "meta": "30-11-2026"}, {"n": 2, "meta": None}],
    "modo_datos": "generado",
    "etiquetas": ["a", "b c"],
    "vacio": {},
    "nada": [],
    "activo": True,
    "pasos": {"04-make-strategic-analysis": {"run": "10-11-2026-00-00-46", "fijada": False, "historial": ["10-11-2026-00-00-46"]}},
}


class TestYaml(unittest.TestCase):
    def test_ida_y_vuelta(self):
        self.assertEqual(Y.loads(Y.dumps(SAMPLE)), SAMPLE)

    def test_comentarios_a_la_derecha(self):
        txt = Y.dumps(SAMPLE, lambda r: {"modo_datos": "generado o real", "equipo[].rol": "rol libre", "pasos.*.run": "x"}.get(r))
        self.assertIn("modo_datos: generado  # generado o real", txt)
        self.assertIn("rol: null  # rol libre", txt)
        self.assertEqual(Y.loads(txt), SAMPLE)

    def test_ruta_de_comentario_de_lista(self):
        rutas = []
        Y.dumps(SAMPLE, lambda r: rutas.append(r))
        self.assertIn("equipo[].nombre", rutas)
        self.assertIn("kpi[].meta", rutas)
        self.assertIn("pasos.04-make-strategic-analysis.run", rutas)

    def test_numeros_como_texto_se_entrecomillan(self):
        txt = Y.dumps({"ruc": "20123456789"})
        self.assertIn('"20123456789"', txt)
        self.assertEqual(Y.loads(txt)["ruc"], "20123456789")

    def test_leer_comentarios_y_comillas(self):
        d = Y.loads('a: "x # no es comentario"  # sí lo es\nb: \'it\'\'s\'\nc: 3  # tres\n')
        self.assertEqual(d, {"a": "x # no es comentario", "b": "it's", "c": 3})

    def test_lista_al_mismo_nivel_que_la_clave(self):
        self.assertEqual(Y.loads("a:\n- 1\n- 2\n"), {"a": [1, 2]})

    def test_rechaza_flujo_con_contenido(self):
        with self.assertRaises(Y.YamlError) as cm:
            Y.loads("a: 1\nb: [1, 2]\n")
        self.assertEqual(cm.exception.line, 2)

    def test_rechaza_tabuladores_y_clave_repetida(self):
        with self.assertRaises(Y.YamlError):
            Y.loads("a:\n\tb: 1\n")
        with self.assertRaises(Y.YamlError):
            Y.loads("a: 1\na: 2\n")

    def test_rechaza_comillas_sin_cerrar(self):
        with self.assertRaises(Y.YamlError):
            Y.loads('a: "abc\n')

    def test_rechaza_sangria_inesperada(self):
        with self.assertRaises(Y.YamlError):
            Y.loads("a: 1\n   b: 2\n")


if __name__ == "__main__":
    unittest.main()
