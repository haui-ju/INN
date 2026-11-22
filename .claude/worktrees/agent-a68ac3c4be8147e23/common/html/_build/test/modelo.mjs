// Ejecuta el modelo puro de un visual sobre unos datos y escribe el resultado como JSON (sin React ni DOM).
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const aqui = dirname(fileURLToPath(import.meta.url));
const src = join(aqui, "..", "src");
const [visual, ruta] = process.argv.slice(2);
const datos = JSON.parse(readFileSync(ruta, "utf8"));
const formato = await import(join(src, "lib", "formato.js"));
const mod = await import(join(src, "visuales", visual, "modelo.js"));
const pura = await import(join(src, "captura", "captura-pura.js"));
console.log(JSON.stringify({
  textos: formato.textos(datos),
  superadas: formato.superadas(datos),
  fecha: mod.fecha(datos),
  modelo: mod.modelo(datos),
  archivo: pura.nombreArchivo(mod.visual, mod.fecha(datos)),
}));
