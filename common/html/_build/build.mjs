// Compila cada visual de common/html/ a un único HTML autónomo (React + Tailwind + fuentes incrustadas).
// Solo para desarrollo: el kit copia los index.html ya compilados. Uso: npm run build
import { build } from "esbuild";
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const aqui = dirname(fileURLToPath(import.meta.url));
const comun = join(aqui, "..");
const src = join(aqui, "src");
const dist = join(aqui, "dist");
mkdirSync(dist, { recursive: true });

function fuente(familia, archivo, pesos) {
  const b64 = readFileSync(join(aqui, "node_modules", archivo)).toString("base64");
  return `@font-face{font-family:"${familia}";font-style:normal;font-weight:${pesos};font-display:swap;src:url(data:font/woff2;base64,${b64}) format("woff2")}`;
}

// 1. CSS de Tailwind (tema ligado a las variables de los tokens) + fuentes en base64
execFileSync(join(aqui, "node_modules", ".bin", "tailwindcss"), ["-i", join(src, "styles.css"), "-o", join(dist, "estilos.css"), "--minify"], { cwd: aqui, stdio: "pipe" });
const fuentes = [
  fuente("Newsreader", "@fontsource-variable/newsreader/files/newsreader-latin-wght-normal.woff2", "200 800"),
  fuente("Instrument Sans", "@fontsource-variable/instrument-sans/files/instrument-sans-latin-wght-normal.woff2", "400 700"),
].join("\n");
// Sin direcciones externas en el archivo: se quita el comentario de licencia de Tailwind.
const estilos = fuentes + "\n" + readFileSync(join(dist, "estilos.css"), "utf8").replace(/\/\*![\s\S]*?\*\//g, "").trim();

// 2. Un HTML por visual
const pagina = readFileSync(join(aqui, "pagina.html"), "utf8");
const visuales = readdirSync(join(src, "visuales"), { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name).sort();
for (const v of visuales) {
  const meta = JSON.parse(readFileSync(join(src, "visuales", v, "meta.json"), "utf8"));
  const mock = JSON.parse(readFileSync(join(comun, v, "mock.json"), "utf8"));
  const salida = await build({
    entryPoints: [join(src, "visuales", v, "index.jsx")],
    bundle: true, minify: true, write: false, format: "iife", jsx: "automatic", target: "es2020", legalComments: "none",
    define: { "process.env.NODE_ENV": '"production"' }, loader: { ".js": "jsx" },
  });
  // Los mensajes de error de React llevan una dirección de texto (no se carga nada); se acorta para que el HTML no tenga URLs.
  const app = salida.outputFiles[0].text.replace(/<\/script/gi, "<\\/script").replaceAll("https://react.dev/", "react.dev/");
  const datos = JSON.stringify(mock).replace(/<\//g, "<\\/");
  const html = pagina.replace("{{titulo}}", () => meta.titulo).replace("{{estilos}}", () => estilos).replace("{{datos}}", () => datos).replace("{{app}}", () => app);
  if (!existsSync(join(comun, v))) mkdirSync(join(comun, v), { recursive: true });
  writeFileSync(join(comun, v, "index.html"), html);
  console.log(`${v}: ${(html.length / 1024).toFixed(0)} KB`);
}
