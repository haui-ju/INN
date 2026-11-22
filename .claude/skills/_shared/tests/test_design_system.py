import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SKILL = HERE.parent / "02-design-system"
sys.path.insert(0, str(HERE))
import validate_run as V  # noqa: E402
from rules import design_system as D  # noqa: E402

TOKENS = SKILL / "references" / "tokens-base.json"
DESIGN = SKILL / "references" / "design-base.md"
RENDER = SKILL / "scripts" / "render_preview.py"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.run = Path(self.tmp.name) / "02-design-system" / "corrida"
        self.run.mkdir(parents=True)
        shutil.copy(TOKENS, self.run / "tokens.json")
        shutil.copy(DESIGN, self.run / "DESIGN.md")
        self.render()

    def tearDown(self):
        self.tmp.cleanup()

    def render(self):
        subprocess.run([sys.executable, str(RENDER), str(self.run / "tokens.json"), str(self.run / "preview.html"), "--titulo", "Proyecto"],
                       check=True, capture_output=True)

    def tokens(self):
        return json.loads((self.run / "tokens.json").read_text(encoding="utf-8"))

    def save(self, t):
        (self.run / "tokens.json").write_text(json.dumps(t, ensure_ascii=False), encoding="utf-8")

    def msgs(self):
        return [f"{f}: {m}" for f, m in V.validate(self.run)]


class TestContraste(unittest.TestCase):
    def test_negro_sobre_blanco(self):
        self.assertAlmostEqual(D.contraste("#000000", "#FFFFFF"), 21.0, places=2)

    def test_igual_color(self):
        self.assertAlmostEqual(D.contraste("#777777", "#777777"), 1.0, places=2)

    def test_par_conocido(self):
        # #767676 sobre blanco es el gris mínimo que cumple 4,5:1
        self.assertGreaterEqual(D.contraste("#767676", "#FFFFFF"), 4.5)
        self.assertLess(D.contraste("#777777", "#FFFFFF"), 4.6)


class TestSistemaBase(Base):
    def test_base_sin_incidencias(self):
        self.assertEqual(self.msgs(), [])

    def test_render_determinista(self):
        a = (self.run / "preview.html").read_bytes()
        self.render()
        self.assertEqual(a, (self.run / "preview.html").read_bytes())

    def test_preview_autonomo(self):
        h = (self.run / "preview.html").read_text(encoding="utf-8")
        self.assertIn("prefers-color-scheme", h)
        self.assertIn('data-theme="dark"', h)
        self.assertIn('data-theme="light"', h)
        self.assertIsNone(re.search(r"https?://(?!www\.w3\.org/)", h))


class TestIncidencias(Base):
    def test_par_con_poco_contraste(self):
        t = self.tokens()
        t["color"]["claro"]["texto-secundario"] = "#A0A0A0"
        self.save(t)
        self.render()
        self.assertTrue(any("tokens.json" in m and "claro" in m and "texto-secundario" in m and "mínimo 4.5" in m for m in self.msgs()))

    def test_oscuro_incompleto(self):
        t = self.tokens()
        del t["color"]["oscuro"]["alerta"]
        self.save(t)
        self.assertTrue(any("mismas claves" in m for m in self.msgs()))

    def test_tema_por_defecto_oscuro_llega_al_preview(self):
        t = self.tokens()
        t["tema-defecto"] = "oscuro"
        self.save(t)
        self.render()
        self.assertEqual(self.msgs(), [])
        self.assertIn("--tema-defecto: oscuro;", (self.run / "preview.html").read_text(encoding="utf-8"))

    def test_sin_tema_por_defecto_no_define_la_variable(self):
        t = self.tokens()
        t.pop("tema-defecto", None)
        self.save(t)
        self.render()
        self.assertEqual(self.msgs(), [])
        self.assertNotIn("--tema-defecto:", (self.run / "preview.html").read_text(encoding="utf-8"))

    def test_los_tokens_base_abren_en_oscuro_y_traen_ocho_series(self):
        t = self.tokens()
        self.assertEqual(t["tema-defecto"], "oscuro")
        for tema in ("claro", "oscuro"):
            self.assertEqual([k for k in t["color"][tema] if k.startswith("serie-")], [f"serie-{i}" for i in range(1, 9)])

    def test_tema_por_defecto_invalido(self):
        t = self.tokens()
        t["tema-defecto"] = "azul"
        self.save(t)
        self.assertTrue(any("tema-defecto debe ser claro o oscuro" in m for m in self.msgs()), self.msgs())

    def test_token_inexistente_en_design_md(self):
        p = self.run / "DESIGN.md"
        p.write_text(p.read_text(encoding="utf-8") + "\nUsa `color.claro.acento-suave`.\n", encoding="utf-8")
        self.assertIn("DESIGN.md: token inexistente: color.claro.acento-suave", self.msgs())

    def test_componente_sin_estados(self):
        p = self.run / "DESIGN.md"
        txt = p.read_text(encoding="utf-8").replace("- **Estados:** normal, hover, foco, deshabilitado\n", "")
        p.write_text(txt, encoding="utf-8")
        self.assertIn("DESIGN.md: componente «Botón» sin «Estados»", self.msgs())

    def test_componente_ausente(self):
        p = self.run / "DESIGN.md"
        txt = p.read_text(encoding="utf-8").replace("### Tarjeta", "### Panel")
        p.write_text(txt, encoding="utf-8")
        self.assertIn("DESIGN.md: falta el componente «Tarjeta»", self.msgs())

    def test_recurso_externo(self):
        p = self.run / "preview.html"
        p.write_text(p.read_text(encoding="utf-8").replace("</head>", '<link rel="stylesheet" href="https://fonts.example.com/x.css"></head>'), encoding="utf-8")
        self.assertTrue(any("recurso externo" in m for m in self.msgs()))

    def test_preview_desalineado(self):
        p = self.run / "preview.html"
        p.write_text(p.read_text(encoding="utf-8").replace("--c-acento: #A67C00;", "--c-acento: #FF0000;", 1), encoding="utf-8")
        self.assertTrue(any("--c-acento" in m for m in self.msgs()))

    def test_preview_modificado_a_mano(self):
        p = self.run / "preview.html"
        p.write_text(p.read_text(encoding="utf-8").replace("<title>Sistema de diseño</title>", "<title>Otro título</title>", 1), encoding="utf-8")
        self.assertTrue(any("preview.html: no es la plantilla vista-previa con los tokens de tokens.json" in m for m in self.msgs()))

    def test_acento_fuerte_sin_contraste(self):
        t = self.tokens()
        t["color"]["claro"]["acento-fuerte"] = "#D4704F"
        self.save(t)
        self.render()
        self.assertTrue(any("contraste" in m and "acento-fuerte" in m for m in self.msgs()))

    def test_texto_prohibido_en_design_md(self):
        p = self.run / "DESIGN.md"
        p.write_text(p.read_text(encoding="utf-8") + "\nEjemplos con datos de prueba.\n", encoding="utf-8")
        self.assertTrue(any("DESIGN.md" in m and "prueba" in m for m in self.msgs()))


if __name__ == "__main__":
    unittest.main()
