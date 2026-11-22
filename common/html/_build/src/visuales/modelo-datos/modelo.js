export const visual = "modelo-datos";
export const fecha = () => null;
export const ancho = "completo";
export const anchoImagen = 1440;

const ANCHO = 1280;
const ALTO_DIM = 152;
const ALTO_HECHO_BASE = 124;
const SEPARACION = 168;

// Modelo del esquema en estrella: las dimensiones arriba, los hechos abajo y una línea curva por cada relación, con su cardinalidad.
// La posición de cada tarjeta se calcula aquí para que las líneas lleguen exactamente a su borde.
export function modelo(datos) {
  const rels = datos.relaciones || [];
  const nd = (datos.dimensiones || []).length;
  const nh = (datos.hechos || []).length;
  const anchoDim = Math.min(200, Math.floor((ANCHO - (nd + 1) * 14) / Math.max(nd, 1)));
  const sepDim = nd ? (ANCHO - nd * anchoDim) / (nd + 1) : 0;
  const anchoHecho = Math.min(380, Math.floor((ANCHO - (nh + 1) * 28) / Math.max(nh, 1)));
  const sepHecho = nh ? (ANCHO - nh * anchoHecho) / (nh + 1) : 0;
  const maxMedidas = Math.max(1, ...(datos.hechos || []).map((h) => (h.medidas || []).length));
  const ALTO_HECHO = ALTO_HECHO_BASE + 34 * Math.ceil(maxMedidas / 1.6);
  const yHecho = ALTO_DIM + SEPARACION;
  const dimensiones = (datos.dimensiones || []).map((d, i) => ({
    codigo: d.codigo, nombre: d.nombre, clave: d.clave, atributos: d.atributos || [], jerarquias: d.jerarquias || [],
    k: `serie-${(i % 8) + 1}`, x: Math.round(sepDim + i * (anchoDim + sepDim)), y: 0, w: anchoDim, h: ALTO_DIM,
  }));
  const hechos = (datos.hechos || []).map((h, j) => ({
    codigo: h.codigo, nombre: h.nombre, granularidad: h.granularidad || "", claves: h.claves || [],
    medidas: (h.medidas || []).map((x) => ({ nombre: x.nombre, agregacion: x.agregacion || "" })),
    x: Math.round(sepHecho + j * (anchoHecho + sepHecho)), y: yHecho, w: anchoHecho, h: ALTO_HECHO,
  }));
  const lineas = [];
  hechos.forEach((h) => {
    const propias = rels.filter((r) => r.desde === h.nombre).map((r) => ({ r, d: dimensiones.find((x) => x.nombre === r.hacia) })).filter((e) => e.d);
    propias.sort((a, b) => a.d.x - b.d.x);
    propias.forEach(({ r, d }, idx) => {
      const sx = d.x + d.w / 2, sy = d.y + d.h;
      const ex = Math.round(h.x + (h.w * (idx + 1)) / (propias.length + 1)), ey = h.y;
      const m = Math.round((sy + ey) / 2);
      const [lado1 = "*", lado2 = "1"] = String(r.cardinalidad || "*:1").split(":");
      lineas.push({ codigo: r.codigo, cardinalidad: r.cardinalidad, ladoDesde: lado1, ladoHacia: lado2, filtro: r.filtro, k: d.k, sx, sy, ex, ey, d: `M${sx},${sy} C${sx},${m} ${ex},${m} ${ex},${ey}` });
    });
  });
  const relaciones = rels.map((r) => ({ codigo: r.codigo, desde: r.desde, hacia: r.hacia, campos: r.campos, cardinalidad: r.cardinalidad, filtro: r.filtro }));
  return {
    titulo: "Modelo de datos en estrella", proyecto: datos.proyecto || "", corte: null, vacio: hechos.length + dimensiones.length === 0,
    ancho: ANCHO, alto: yHecho + ALTO_HECHO, dimensiones, hechos, lineas, relaciones,
  };
}
