export const visual = "foda";
export const fecha = () => null;
export const ancho = "fijo";
export const anchoImagen = 1120;

const CUADRANTES = [
  { clave: "fortalezas", nombre: "Fortalezas", grupo: "Interno", signo: "Favorable", tono: "exito", icono: "fuerza" },
  { clave: "debilidades", nombre: "Debilidades", grupo: "Interno", signo: "Desfavorable", tono: "alerta", icono: "debil" },
  { clave: "oportunidades", nombre: "Oportunidades", grupo: "Externo", signo: "Favorable", tono: "marca", icono: "oportunidad" },
  { clave: "amenazas", nombre: "Amenazas", grupo: "Externo", signo: "Desfavorable", tono: "error", icono: "amenaza" },
];

// Modelo del FODA: cuatro cuadrantes (interno arriba, externo abajo) con sus ítems tal como vienen.
export function modelo(datos) {
  const base = { titulo: "Diagnóstico FODA", proyecto: datos.proyecto || "", corte: null, vacio: true };
  const c = datos.cuadrantes || {};
  const cuadrantes = CUADRANTES.map((q) => ({ ...q, items: (c[q.clave] || []).map((i) => ({ codigo: i.codigo, texto: i.texto, evidencia: i.evidencia || "" })) }));
  const total = cuadrantes.reduce((a, q) => a + q.items.length, 0);
  return { ...base, vacio: total === 0, total, cuadrantes };
}
