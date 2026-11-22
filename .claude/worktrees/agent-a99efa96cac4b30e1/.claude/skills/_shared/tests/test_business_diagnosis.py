"""Validador del paso 03-make-business-diagnosis (secciones 1.1 a 1.4) sobre los ejemplos de sus plantillas."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagnostico_fixtures as F  # noqa: E402
import projectcfg as P  # noqa: E402
import validate_run as V  # noqa: E402
from rules import business_diagnosis as R  # noqa: E402

PASO = "03-make-business-diagnosis"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run = F.crear(self.root, hasta=PASO)[PASO]

    def tearDown(self):
        self.tmp.cleanup()

    def msgs(self):
        return [f"{f}: {m}" for f, m in V.validate(self.run)]

    def edita(self, punto, a, b):
        f = self.run / "secciones" / f"{punto}.md"
        t = f.read_text(encoding="utf-8")
        assert a in t, a
        f.write_text(t.replace(a, b, 1), encoding="utf-8")

    def assertIncidencia(self, texto):
        m = self.msgs()
        self.assertTrue(any(texto in x for x in m), m)


class TestEjemplo(Base):
    def test_ejemplo_sin_incidencias(self):
        self.assertEqual(self.msgs(), [])

    def test_corrida_completa(self):
        for f in ("secciones/1.1.md", "secciones/1.4.md", "visuales/bmc.html", "visuales/bmc.json", "leer-imagen/bmc.md", "referencias.md", "README.md"):
            self.assertTrue((self.run / f).is_file(), f)

    def test_registro_marca_las_secciones(self):
        estado = {s["seccion"]: s["estado"] for s in P.secciones(self.root)}
        self.assertEqual([estado[p] for p in R.PUNTOS], ["disponible"] * 4)
        self.assertEqual(estado["1.5"], "pendiente")


class TestReglas(Base):
    def test_encabezado(self):
        self.edita("1.1", "## 1.1. Nombre de la empresa", "## 1.1. Empresa")
        self.assertIncidencia("«## 1.1. Nombre de la empresa»")

    def test_falta_fila_de_la_empresa(self):
        self.edita("1.1", "| Ubicación | San Juan de Lurigancho, Lima |\n", "")
        self.assertIncidencia("falta la fila «Ubicación»")

    def test_ruc_con_proyecto_propio(self):
        self.edita("1.1", "No aplica (empresa planteada por el equipo)", "20614837251")
        self.assertIncidencia("No aplica")

    def test_ruc_distinto_del_config(self):
        cfg = P.load(self.root)
        cfg["proyecto"]["tipo"], cfg["proyecto"]["ruc"] = "empresa", "20100047218"
        P.save(cfg, self.root)
        self.edita("1.1", "No aplica (empresa planteada por el equipo)", "20614837251")
        self.assertIncidencia("no coincide con el del config")

    def test_nombre_distinto_de_domain(self):
        self.edita("1.1", "| Nombre comercial | Pollería Don Tito |", "| Nombre comercial | Pollería Tito |")
        self.assertIncidencia("difiere del de domain.md")

    def test_mision_distinta_de_domain(self):
        self.edita("1.2", "Servir el mejor pollo", "Ofrecer el mejor pollo")
        self.assertIncidencia("la misión difiere de la de domain.md")

    def test_falta_la_vision(self):
        self.edita("1.2", "**Visión.**", "**Vista.**")
        self.assertIncidencia("falta la «**Visión.**»")

    def test_categoria_incoherente(self):
        self.edita("1.3", "| Categoría (Ley 30056) | Pequeña empresa |", "| Categoría (Ley 30056) | Mediana empresa |")
        self.assertIncidencia("es «Pequeña empresa», no «Mediana empresa»")

    def test_calculo_en_uit_erroneo(self):
        self.edita("1.3", "| Ventas en UIT | 436 |", "| Ventas en UIT | 480 |")
        self.assertIncidencia("= 436, no 480")

    def test_categoria_desconocida(self):
        self.edita("1.3", "| Categoría (Ley 30056) | Pequeña empresa |", "| Categoría (Ley 30056) | Pyme |")
        self.assertIncidencia("la categoría «Pyme» debe ser")

    def test_ventas_pendientes_con_categoria(self):
        self.edita("1.3", "| Ventas anuales | S/ 2 400 000 (2025) |", "| Ventas anuales | Pendiente |")
        self.edita("1.3", "| Ventas en UIT | 436 |", "| Ventas en UIT | Pendiente |")
        self.assertEqual(self.msgs(), [])

    def test_falta_aspecto_de_industria(self):
        self.edita("1.3", "| Entorno competitivo |", "| Competencia |")
        self.assertIncidencia("falta el aspecto «Entorno competitivo»")

    def test_falta_bloque_del_canvas(self):
        self.edita("1.4", "| Socios clave |", "| Aliados |")
        m = self.msgs()
        self.assertTrue(any("falta el bloque «Socios clave»" in x for x in m), m)
        self.assertTrue(any("bloque desconocido «Aliados»" in x for x in m), m)

    def test_falta_lectura_del_modelo(self):
        self.edita("1.4", "**Lectura del modelo.**", "**Comentario.**")
        self.assertIncidencia("Lectura del modelo")

    def test_marcador_en_el_informe(self):
        self.edita("1.1", "Pollería Don Tito es", "Pollería Don Tito (modelado por el agente, por no contar con X) es")
        self.assertIncidencia("marcador")

    def test_cita_sin_referencia(self):
        (self.run / "referencias.md").unlink()
        self.assertIncidencia("cita sin referencia: Osterwalder & Pigneur, 2010")

    def test_texto_limpio(self):
        self.edita("1.1", "Pollería Don Tito es", "Pollería Don Tito, empresa ficticia, es")
        self.assertIncidencia("término no permitido")


if __name__ == "__main__":
    unittest.main()
