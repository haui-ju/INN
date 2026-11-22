import { useEffect, useMemo, useState } from "react";
import { Copy, Download, Moon, Sun } from "lucide-react";
import { Button } from "../ui/button.jsx";
import { Select } from "../ui/select.jsx";
import { ESCALAS, escalaValida } from "../captura/captura-pura.js";
import { copiar, crearPng, descargar } from "../captura/captura.js";

function leer(clave) {
  try { return localStorage.getItem(clave); } catch (e) { return null; }
}
function guardar(clave, valor) {
  try { localStorage.setItem(clave, valor); } catch (e) { /* sin almacenamiento */ }
}

export function App({ visual, datos, modelo, fecha, Vista, ancho = "fijo", anchoImagen = 0 }) {
  const m = useMemo(() => modelo(datos), [datos]);
  const [tema, setTema] = useState(leer("tema") === "dark" ? "dark" : "light");
  const [escala, setEscala] = useState(escalaValida(leer("escala-imagen")));
  const [aviso, setAviso] = useState("");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", tema);
    guardar("tema", tema);
  }, [tema]);

  const cambiarEscala = (v) => {
    const n = escalaValida(v);
    setEscala(n);
    guardar("escala-imagen", String(n));
  };

  async function accion(modo) {
    setAviso("Preparando imagen…");
    try {
      const blob = await crearPng(escala, tema, anchoImagen);
      if (modo === "copiar") {
        const r = await copiar(blob, visual, fecha(datos));
        setAviso(r.modo === "copiada" ? "Imagen copiada al portapapeles." : `No se pudo copiar; se descargó ${r.archivo}`);
      } else {
        setAviso(`Descargada: ${descargar(blob, visual, fecha(datos))}`);
      }
    } catch (e) {
      setAviso("No se pudo crear la imagen en este navegador.");
    }
  }

  return (
    <div className={`mx-auto w-full p-3 sm:p-6 ${ancho === "completo" ? "max-w-none sm:px-8" : "max-w-[1120px]"}`}>
      <div data-no-captura className="mb-4 flex flex-wrap items-center gap-2">
        <label className="inline-flex items-center gap-2 text-sm text-muted-foreground">
          Escala
          <Select value={String(escala)} onChange={(e) => cambiarEscala(e.target.value)} aria-label="Escala de la imagen">
            {ESCALAS.map((n) => <option key={n} value={n}>×{n}</option>)}
          </Select>
        </label>
        <Button onClick={() => accion("copiar")}><Copy aria-hidden="true" />Copiar imagen</Button>
        <Button variant="outline" onClick={() => accion("descargar")}><Download aria-hidden="true" />Descargar imagen</Button>
        <Button variant="ghost" size="icon" onClick={() => setTema(tema === "dark" ? "light" : "dark")} aria-label="Alternar tema claro y oscuro" title="Tema">
          {tema === "dark" ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}
        </Button>
        <span role="status" aria-live="polite" className="text-sm text-muted-foreground">{aviso}</span>
      </div>
      <main id="captura" data-captura className="rounded-xl bg-background p-4 sm:p-8">
        <Vista m={m} />
      </main>
    </div>
  );
}
