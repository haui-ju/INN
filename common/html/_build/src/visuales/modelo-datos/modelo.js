export const visual = "modelo-datos";
export const fecha = () => null;
export const ancho = "fijo";
export const anchoImagen = 1120;

// Modelo del esquema en estrella: dimensiones arriba, hechos debajo y la lista de relaciones con su cardinalidad.
export function modelo(datos) {
  const rels = datos.relaciones || [];
  const dimensiones = (datos.dimensiones || []).map((d) => ({
    codigo: d.codigo, nombre: d.nombre, clave: d.clave, atributos: d.atributos || [], jerarquias: d.jerarquias || [],
    hechos: rels.filter((r) => r.hacia === d.nombre).map((r) => r.desde),
  }));
  const hechos = (datos.hechos || []).map((h) => ({
    codigo: h.codigo, nombre: h.nombre, granularidad: h.granularidad || "", claves: h.claves || [],
    medidas: (h.medidas || []).map((x) => ({ nombre: x.nombre, agregacion: x.agregacion || "" })),
    dimensiones: rels.filter((r) => r.desde === h.nombre).map((r) => r.hacia),
  }));
  const relaciones = rels.map((r) => ({ codigo: r.codigo, desde: r.desde, hacia: r.hacia, campos: r.campos, cardinalidad: r.cardinalidad, filtro: r.filtro }));
  return { titulo: "Modelo de datos en estrella", proyecto: datos.proyecto || "", corte: null, vacio: hechos.length + dimensiones.length === 0, dimensiones, hechos, relaciones };
}
