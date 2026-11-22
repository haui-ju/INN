// Parte pura de la captura de imagen: no toca el DOM y se prueba con node.
export const ESCALAS = [2, 3, 4];

export function escalaValida(x) {
  const n = parseInt(x, 10);
  return ESCALAS.includes(n) ? n : 2;
}

export function nombreArchivo(visual, fecha) {
  return `${visual}${fecha ? `-${fecha}` : ""}.png`;
}

// SVG con el área capturada dentro de un foreignObject. El CSS (tokens, estilos y fuentes) viaja dentro.
export function escaparCss(css) {
  return css.replace(/&/g, "&amp;").replace(/</g, "&lt;");
}

export function construirSvg({ ancho, alto, css, html, tema }) {
  const w = Math.ceil(ancho);
  const h = Math.ceil(alto);
  const estilo = `width:${w}px;font-family:var(--fuente);color:var(--c-texto);background:var(--c-fondo);font-size:var(--t-base);line-height:1.55`;
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" data-theme="${tema === "dark" ? "dark" : "light"}">` +
    `<foreignObject x="0" y="0" width="${w}" height="${h}"><div xmlns="http://www.w3.org/1999/xhtml" style="${estilo}">` +
    `<style>${escaparCss(css)}</style>${html}</div></foreignObject></svg>`
  );
}
