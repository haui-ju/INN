import filecmp
import re
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import projectcfg as P  # noqa: E402
import runs as R  # noqa: E402

STEP = "04-make-strategic-analysis"


def tree(p):
    return {str(f.relative_to(p)): f.read_bytes() for f in sorted(p.rglob("*")) if f.is_file()}


class TestRuns(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        cfg = P.new_config()
        cfg["proyecto"] = {"nombre": "X", "tema": "T", "tipo": "propio", "ruc": None, "rubro": "R"}
        P.save(cfg, self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_new_crea_carpeta_con_formato(self):
        d = R.new(STEP, self.root)
        self.assertTrue(d.is_dir())
        self.assertEqual(d.parent, self.root / "project" / "04-strategic-analysis")
        self.assertRegex(d.name, r"^\d{2}-\d{2}-\d{4}-\d{2}-\d{2}-\d{2}$")

    def test_new_mismo_segundo_no_choca(self):
        t = time.localtime()
        a = R.new(STEP, self.root, t)
        b = R.new(STEP, self.root, t)
        self.assertNotEqual(a, b)

    def test_paso_sin_carpeta(self):
        with self.assertRaises(P.ConfigError):
            R.new("13-make-annex-html", self.root)

    def test_fork_identico_salvo_readme_y_base_intacta(self):
        base = R.new(STEP, self.root, time.strptime("01-01-2026-10-00-00", "%d-%m-%Y-%H-%M-%S"))
        (base / "bloques").mkdir()
        (base / "bloques" / "a.md").write_text("# A\n", encoding="utf-8")
        (base / "README.md").write_text("# Procedencia\n", encoding="utf-8")
        P.register(STEP, base.name, root=self.root)
        antes = tree(base)
        fk = R.fork(STEP, ["quitar FOD-03"], root=self.root)
        self.assertTrue(fk.name.endswith("-fork"))
        self.assertRegex(fk.name, r"^\d{2}-\d{2}-\d{4}-\d{2}-\d{2}-\d{2}-fork$")
        self.assertEqual(tree(base), antes)
        a, b = tree(base), tree(fk)
        self.assertEqual(set(a), set(b))
        self.assertEqual([k for k in a if a[k] != b[k]], ["README.md"])
        txt = (fk / "README.md").read_text(encoding="utf-8")
        self.assertIn(base.name, txt)
        self.assertIn("quitar FOD-03", txt)

    def test_fork_sin_corrida_vigente(self):
        with self.assertRaises(P.ConfigError):
            R.fork(STEP, [], root=self.root)

    def test_fork_base_indicada_inexistente(self):
        with self.assertRaises(P.ConfigError):
            R.fork(STEP, [], base="no-existe", root=self.root)

    def test_fork_no_encadena_nombres(self):
        base = R.new(STEP, self.root)
        f1 = R.fork(STEP, ["x"], base=base.name, root=self.root)
        f2 = R.fork(STEP, ["y"], base=f1.name, root=self.root)
        self.assertEqual(len(re.findall("fork", f2.name)), 1)


if __name__ == "__main__":
    unittest.main()
