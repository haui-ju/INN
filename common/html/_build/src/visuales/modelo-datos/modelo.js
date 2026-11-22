export const visual = "modelo-datos";
export const fecha = () => null;
export const ancho = "fijo";
export const anchoImagen = 1600;
export const laminas = true;

const ANCHO = 1440;
const CABECERA = 50;
const FILA = 25;
const PIE = 12;
const SEPARACION = 100;

// Modelo del diagrama de base de datos: tablas con sus columnas (dimensiones arriba, hechos abajo) y una línea por relación con su cardinalidad.
// La posición y la altura de cada tabla se calculan aquí para que las líneas lleguen exactamente a su borde.
export function modelo(datos) {
  const rels = datos.relaciones || [];
  const nd = (datos.dimensiones || []).length;
  const nh = (datos.hechos || []).length;
  const anchoDim = Math.min(280, Math.floor((ANCHO - (nd + 1) * 14) / Math.max(nd, 1)));
  const sepDim = nd ? (ANCHO - nd * anchoDim) / (nd + 1) : 0;
  const anchoHecho = Math.min(420, Math.floor((ANCHO - (nh + 1) * 28) / Math.max(nh, 1)));
  const sepHecho = nh ? (ANCHO - nh * anchoHecho) / (nh + 1) : 0;
  const dimensiones = (datos.dimensiones || []).map((d, i) => {
    const filas = [{ nombre: d.clave, rol: "PK" }, ...(d.atributos || []).filter((a) => a !== d.clave).map((a) => ({ nombre: a, rol: "" }))];
    const jer = (d.jerarquias || []).join("; ");
    return {
      codigo: d.codigo, nombre: d.nombre, clave: d.clave, filas, jerarquia: jer,
      x: Math.round(sepDim + i * (anchoDim + sepDim)), y: 0, w: anchoDim, h: CABECERA + FILA * filas.length + (jer ? 30 : 0) + PIE,
    };
  });
  const altoDim = Math.max(0, ...dimensiones.map((d) => d.h));
  const yHecho = altoDim + SEPARACION;
  const hechos = (datos.hechos || []).map((h, j) => {
    const filas = [
      ...(h.claves || []).map((k) => ({ nombre: k, rol: "FK" })),
      ...(h.medidas || []).map((m) => ({ nombre: m.nombre, rol: "Σ", detalle: [m.tipo, m.agregacion].filter(Boolean).join(" · ") })),
    ];
    return {
      codigo: h.codigo, nombre: h.nombre, granularidad: h.granularidad || "", filas,
      x: Math.round(sepHecho + j * (anchoHecho + sepHecho)), y: yHecho, w: anchoHecho, h: CABECERA + FILA * filas.length + 34 + PIE,
    };
  });
  const altoHecho = Math.max(0, ...hechos.map((h) => h.h));
  const lineas = [];
  hechos.forEach((h) => {
    const propias = rels.filter((r) => r.desde === h.nombre).map((r) => ({ r, d: dimensiones.find((x) => x.nombre === r.hacia) })).filter((e) => e.d);
    propias.sort((a, b) => a.d.x - b.d.x);
    propias.forEach(({ r, d }, idx) => {
      const sx = d.x + d.w / 2, sy = d.y + d.h;
      const ex = Math.round(h.x + (h.w * (idx + 1)) / (propias.length + 1)), ey = h.y;
      const m = Math.round((sy + ey) / 2);
      const [lado1 = "*", lado2 = "1"] = String(r.cardinalidad || "*:1").split(":");
      lineas.push({ codigo: r.codigo, cardinalidad: r.cardinalidad, ladoDesde: lado1, ladoHacia: lado2, sx, sy, ex, ey, d: `M${sx},${sy} C${sx},${m} ${ex},${m} ${ex},${ey}` });
    });
  });
  const relaciones = rels.map((r) => ({ codigo: r.codigo, desde: r.desde, hacia: r.hacia, campos: r.campos, cardinalidad: r.cardinalidad, filtro: r.filtro }));
  return {
    titulo: "Modelo de datos en estrella", proyecto: datos.proyecto || "", corte: null, vacio: hechos.length + dimensiones.length === 0,
    ancho: ANCHO, alto: yHecho + altoHecho, dimensiones, hechos, lineas, relaciones,
  };
}
