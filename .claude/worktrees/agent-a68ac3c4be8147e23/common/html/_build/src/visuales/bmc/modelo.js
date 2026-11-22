export const visual = "bmc";
export const fecha = () => null;
export const ancho = "completo";
export const anchoImagen = 1560;

// Disposición clásica del lienzo en diez columnas (en pantallas anchas); en teléfono, una columna en este mismo orden.
const BLOQUES = [
  { clave: "socios", nombre: "Socios clave", icono: "socios", area: "lg:col-start-1 lg:col-span-2 lg:row-start-1 lg:row-span-2" },
  { clave: "actividades", nombre: "Actividades clave", icono: "actividades", area: "lg:col-start-3 lg:col-span-2 lg:row-start-1" },
  { clave: "recursos", nombre: "Recursos clave", icono: "recursos", area: "lg:col-start-3 lg:col-span-2 lg:row-start-2" },
  { clave: "propuesta", nombre: "Propuesta de valor", icono: "propuesta", area: "lg:col-start-5 lg:col-span-2 lg:row-start-1 lg:row-span-2", tono: "marca" },
  { clave: "relaciones", nombre: "Relaciones con clientes", icono: "relaciones", area: "lg:col-start-7 lg:col-span-2 lg:row-start-1" },
  { clave: "canales", nombre: "Canales", icono: "canales", area: "lg:col-start-7 lg:col-span-2 lg:row-start-2" },
  { clave: "segmentos", nombre: "Segmentos de clientes", icono: "segmentos", area: "lg:col-start-9 lg:col-span-2 lg:row-start-1 lg:row-span-2" },
  { clave: "costos", nombre: "Estructura de costos", icono: "costos", area: "lg:col-start-1 lg:col-span-5 lg:row-start-3" },
  { clave: "ingresos", nombre: "Fuentes de ingresos", icono: "ingresos", area: "lg:col-start-6 lg:col-span-5 lg:row-start-3" },
];

// Modelo del Canvas: los nueve bloques en su lugar del lienzo, con sus elementos tal como vienen.
export function modelo(datos) {
  const por = Object.fromEntries((datos.bloques || []).map((b) => [b.clave, b]));
  const bloques = BLOQUES.map((b) => ({ ...b, tono: b.tono || "neutro", items: ((por[b.clave] || {}).items || []).filter(Boolean) }));
  const total = bloques.reduce((a, b) => a + b.items.length, 0);
  return { titulo: "Business Model Canvas", proyecto: datos.empresa || datos.proyecto || "", corte: null, vacio: total === 0, total, bloques };
}
