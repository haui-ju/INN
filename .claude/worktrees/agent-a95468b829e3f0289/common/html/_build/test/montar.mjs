// Monta una plantilla compilada en jsdom y escribe lo que quedó en pantalla (verifica el paquete real de React).
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";

const html = readFileSync(process.argv[2], "utf8");
const dom = new JSDOM(html, { runScripts: "dangerously", pretendToBeVisual: true, url: "http://localhost/" });
await new Promise((r) => setTimeout(r, 400));
const d = dom.window.document;
console.log(JSON.stringify({
  raiz: d.getElementById("raiz").textContent,
  codigos: [...d.querySelectorAll("[data-codigo]")].map((n) => n.getAttribute("data-codigo")),
  ind: Object.fromEntries([...d.querySelectorAll("[data-ind]")].map((n) => [n.getAttribute("data-ind"), n.textContent])),
  botones: [...d.querySelectorAll("button")].map((b) => (b.textContent.trim() || b.getAttribute("aria-label"))),
  escalas: [...d.querySelectorAll("#captura ~ *, select option")].map((o) => o.textContent).filter((t) => /^×/.test(t)),
  superadas: d.body.textContent.split("límite superado").length - 1,
  tema: d.documentElement.getAttribute("data-theme"),
  fuera: d.querySelectorAll("[data-no-captura]").length,
  captura: d.getElementById("captura") ? d.getElementById("captura").hasAttribute("data-captura") : false,
}));
