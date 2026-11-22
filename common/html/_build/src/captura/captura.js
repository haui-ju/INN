// Captura de imagen en el navegador: rasteriza el área [data-captura] a PNG, la copia o la descarga.
import { construirSvg, escalaValida, nombreArchivo } from "./captura-pura.js";

function areaSvg(tema, anchoMin = 0) {
  const area = document.getElementById("captura");
  const clon = area.cloneNode(true);
  clon.querySelectorAll("[data-no-captura]").forEach((n) => n.remove());
  clon.querySelectorAll("[data-scroll]").forEach((n) => { n.style.overflow = "visible"; });
  let ancho = Math.max(area.offsetWidth, anchoMin);
  area.querySelectorAll("[data-scroll]").forEach((n) => {
    ancho = Math.max(ancho, n.scrollWidth + (area.offsetWidth - n.clientWidth));
  });
  const caja = document.createElement("div");
  caja.style.cssText = `position:absolute;left:-99999px;top:0;width:${ancho}px`;
  caja.appendChild(clon);
  document.body.appendChild(caja);
  const alto = clon.scrollHeight;
  document.body.removeChild(caja);
  const css = document.getElementById("tokens").textContent + document.getElementById("estilos").textContent;
  const html = new XMLSerializer().serializeToString(clon);
  return construirSvg({ ancho, alto, css, html, tema });
}

export function crearPng(escala, tema, anchoMin = 0) {
  const factor = escalaValida(escala);
  const svg = areaSvg(tema, anchoMin);
  return new Promise((ok, mal) => {
    const img = new Image();
    img.onload = () => {
      const c = document.createElement("canvas");
      c.width = img.width * factor;
      c.height = img.height * factor;
      const ctx = c.getContext("2d");
      ctx.scale(factor, factor);
      ctx.drawImage(img, 0, 0);
      c.toBlob((b) => (b ? ok(b) : mal(new Error("sin imagen"))), "image/png");
    };
    img.onerror = () => mal(new Error("no se pudo dibujar"));
    img.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
  });
}

export function descargar(blob, visual, fecha) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = nombreArchivo(visual, fecha);
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  return a.download;
}

// Copia al portapapeles; si el navegador no lo permite, descarga y lo informa.
export async function copiar(blob, visual, fecha) {
  try {
    if (!(navigator.clipboard && window.ClipboardItem)) throw new Error("sin portapapeles");
    await navigator.clipboard.write([new ClipboardItem({ "image/png": blob })]);
    return { modo: "copiada" };
  } catch (e) {
    return { modo: "descargada", archivo: descargar(blob, visual, fecha) };
  }
}
