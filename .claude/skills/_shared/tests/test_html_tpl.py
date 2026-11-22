import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import html_tpl as H  # noqa: E402

COMUN = HERE.parents[2] / "common" / "html"
EJEMPLO = json.loads((COMUN / "foda" / "mock.json").read_text(encoding="utf-8"))
EXTERNOS = [r"<script[^>]+src\s*=", r"<link[^>]+href\s*=", r"@import", r"url\(\s*[\"']?(?:https?:)?//", r"https?://(?!www\.w3\.org/)"]


def fuera_de_bloques(t):
    return H.RE_DATOS.sub("", H.RE_TOKENS.sub("", t))


PLANTILLAS = ["arquitectura-bi", "bmc", "foda", "ishikawa", "modelo-datos", "pestel", "vista-previa"]


class TestBiblioteca(unittest.TestCase):
    def test_hay_las_plantillas_con_sus_archivos(self):
        self.assertEqual(H.visuales(), PLANTILLAS)
        for v in H.visuales():
            for f in ("index.html", "README.md", "mock.json"):
                self.assertTrue((COMUN / v / f).is_file(), f"{v}/{f}")
        for f in ("DESIGN.md", "README.md"):
            self.assertTrue((COMUN / f).is_file(), f)

    def test_plantillas_sincronizadas_con_sus_fuentes(self):
        self.assertEqual(H.comprobar(), [])

    def test_comprobar_detecta_fuentes_cambiadas(self):
        original = H.huella_fuentes
        try:
            H.huella_fuentes = lambda: "otra"
            self.assertTrue(any("recompilaron" in m for m in H.comprobar()))
        finally:
            H.huella_fuentes = original

    def test_sin_recursos_externos(self):
        for v in H.visuales():
            t = (COMUN / v / "index.html").read_text(encoding="utf-8")
            for rx in EXTERNOS:
                self.assertIsNone(re.search(rx, t, re.I), f"{v}: {rx}")
            self.assertIn('name="viewport"', t)
            self.assertIn('data-theme="light"', t)
            self.assertIn("prefers-color-scheme", t)
            self.assertIn("<noscript>", t)

    def test_cada_plantilla_tiene_los_dos_bloques_una_vez(self):
        for v in H.visuales():
            t = (COMUN / v / "index.html").read_text(encoding="utf-8")
            self.assertEqual(len(H.RE_TOKENS.findall(t)), 1)
            self.assertEqual(len(H.RE_DATOS.findall(t)), 1)

    def test_mock_valido(self):
        for v in H.visuales():
            m = json.loads((COMUN / v / "mock.json").read_text(encoding="utf-8"))
            self.assertEqual(m["schema"], 1)

    def test_los_mock_traen_datos_de_ejemplo(self):
        f = json.loads((COMUN / "foda" / "mock.json").read_text(encoding="utf-8"))
        self.assertTrue(all(f["cuadrantes"][c] for c in ("fortalezas", "debilidades", "oportunidades", "amenazas")))
        self.assertEqual({e["tipo"] for e in f["estrategias"]}, {"FO", "FA", "DO", "DA"})
        b = json.loads((COMUN / "bmc" / "mock.json").read_text(encoding="utf-8"))
        self.assertEqual(len(b["bloques"]), 9)
        self.assertTrue(all(x["items"] for x in b["bloques"]))
        e = json.loads((COMUN / "pestel" / "mock.json").read_text(encoding="utf-8"))
        self.assertEqual(len(e["factores"]), 6)
        self.assertTrue(all(x["items"] for x in e["factores"]))
        i = json.loads((COMUN / "ishikawa" / "mock.json").read_text(encoding="utf-8"))
        self.assertTrue(i["efecto"] and len(i["categorias"]) >= 4)
        p = json.loads((COMUN / "vista-previa" / "mock.json").read_text(encoding="utf-8"))
        self.assertEqual(p["tokens"], H.cargar_tokens(None, "base"))

    def test_los_mock_no_se_declaran_falsos(self):
        for v in H.visuales():
            txt = (COMUN / v / "mock.json").read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"falso|inventad|simulad|de prueba|ficticio", txt, re.I), v)


class TestLimpiar(unittest.TestCase):
    def test_limpiar_deja_las_mismas_claves_sin_contenido(self):
        for v in H.visuales():
            m = json.loads((COMUN / v / "mock.json").read_text(encoding="utf-8"))
            c = H.limpiar(m)
            self.assertEqual(set(c), set(m))
            self.assertEqual(c["schema"], 1)
            self.assertNotIn("FOR-01", json.dumps(c))
        c = H.limpiar(json.loads((COMUN / "foda" / "mock.json").read_text(encoding="utf-8")))
        self.assertEqual(c, {"schema": 1, "proyecto": "", "cuadrantes": {"fortalezas": [], "debilidades": [], "oportunidades": [], "amenazas": []}, "estrategias": []})
        self.assertEqual(H.limpiar(json.loads((COMUN / "ishikawa" / "mock.json").read_text(encoding="utf-8"))), {"schema": 1, "proyecto": "", "efecto": "", "categorias": []})
        self.assertEqual(H.limpiar(json.loads((COMUN / "bmc" / "mock.json").read_text(encoding="utf-8"))), {"schema": 1, "proyecto": "", "empresa": "", "bloques": []})
        self.assertEqual(H.limpiar(json.loads((COMUN / "vista-previa" / "mock.json").read_text(encoding="utf-8"))), {"schema": 1, "proyecto": "", "tokens": {}})

    def test_limpiar_no_modifica_el_mock(self):
        antes = (COMUN / "foda" / "mock.json").read_text(encoding="utf-8")
        H.limpiar(json.loads(antes))
        self.assertEqual((COMUN / "foda" / "mock.json").read_text(encoding="utf-8"), antes)

    def test_cli_limpiar(self):
        r = subprocess.run([sys.executable, str(HERE / "html_tpl.py"), "limpiar", "--visual", "foda"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["cuadrantes"]["fortalezas"], [])
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(HERE / "html_tpl.py"), "limpiar", "--visual", "foda", "--salida", str(Path(d) / "d.json")], capture_output=True, text=True)
            self.assertEqual(json.loads((Path(d) / "d.json").read_text(encoding="utf-8"))["cuadrantes"]["amenazas"], [])
        r = subprocess.run([sys.executable, str(HERE / "html_tpl.py"), "limpiar", "--visual", "nada"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)


class TestCopiar(unittest.TestCase):
    def setUp(self):
        self.base = H.cargar_tokens(None, "base")

    def test_la_plantilla_trae_los_tokens_base_y_su_mock(self):
        for v in H.visuales():
            mock = json.loads((COMUN / v / "mock.json").read_text(encoding="utf-8"))
            self.assertEqual((COMUN / v / "index.html").read_text(encoding="utf-8"), H.copiar_texto(v, mock, self.base))

    def test_solo_cambian_los_dos_bloques(self):
        otros = json.loads(json.dumps(self.base))
        otros["color"]["claro"]["acento"] = "#336699"
        for v in ("bmc", "foda", "ishikawa", "pestel"):
            a = (COMUN / v / "index.html").read_text(encoding="utf-8")
            b = H.copiar_texto(v, EJEMPLO, otros)
            self.assertNotEqual(a, b)
            self.assertEqual(fuera_de_bloques(a), fuera_de_bloques(b))
            self.assertIn("--c-acento: #336699;", b)

    def test_datos_embebidos_iguales_a_los_dados(self):
        h = H.copiar_texto("foda", EJEMPLO, self.base)
        m = H.RE_DATOS.search(h)
        self.assertEqual(json.loads(m.group(2).replace("<\\/", "</")), EJEMPLO)

    def test_escapa_el_cierre_de_script_en_los_datos(self):
        d = json.loads(json.dumps(EJEMPLO))
        d["proyecto"] = "</script><b>x</b>"
        h = H.copiar_texto("foda", d, self.base)
        self.assertNotIn("</script><b>", h)
        self.assertEqual(json.loads(H.RE_DATOS.search(h).group(2).replace("<\\/", "</"))["proyecto"], "</script><b>x</b>")

    def test_tokens_css_con_las_tres_familias(self):
        css = H.tokens_css(self.base)
        for v in ("--fuente:", "--fuente-titulos:", "--fuente-mono:", "--c-acento-fuerte:", 'data-theme="dark"', "prefers-color-scheme"):
            self.assertIn(v, css)

    def test_tema_defecto_solo_si_los_tokens_lo_declaran(self):
        sin = {k: v for k, v in self.base.items() if k != "tema-defecto"}
        self.assertNotIn("--tema-defecto", H.tokens_css(sin))
        self.assertIn("--tema-defecto: oscuro;", H.tokens_css({**sin, "tema-defecto": "oscuro"}))
        self.assertNotIn("--tema-defecto", H.tokens_css({**sin, "tema-defecto": "otro"}))

    def test_las_plantillas_fijan_el_tema_antes_de_pintar(self):
        for v in H.visuales():
            t = (COMUN / v / "index.html").read_text(encoding="utf-8")
            self.assertIn("--tema-defecto", t, v)
            self.assertIn('localStorage.getItem("tema")', t, v)

    def test_cli_copiar_y_comprobar(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "data.json"
            p.write_text(json.dumps(EJEMPLO, ensure_ascii=False), encoding="utf-8")
            r = subprocess.run([sys.executable, str(HERE / "html_tpl.py"), "copiar", "--visual", "foda", "--datos", str(p), "--salida", str(Path(d) / "k.html")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual((Path(d) / "k.html").read_text(encoding="utf-8"), H.copiar_texto("foda", EJEMPLO, self.base))
            r = subprocess.run([sys.executable, str(HERE / "html_tpl.py"), "copiar", "--visual", "nada", "--datos", str(p), "--salida", str(Path(d) / "x.html")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
        r = subprocess.run([sys.executable, str(HERE / "html_tpl.py"), "comprobar"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()
