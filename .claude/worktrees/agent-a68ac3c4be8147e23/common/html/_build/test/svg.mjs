// Construye el SVG de una captura con la parte pura (para comprobar que es XML válido).
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const aqui = dirname(fileURLToPath(import.meta.url));
const pura = await import(join(aqui, "..", "src", "captura", "captura-pura.js"));
const [tema] = process.argv.slice(2);
process.stdout.write(pura.construirSvg({ ancho: 800.4, alto: 600.2, css: 'a>b{content:"x & y <z>"}', html: "<div xmlns=\"http://www.w3.org/1999/xhtml\">Hola</div>", tema }));
