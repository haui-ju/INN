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

const ESTRATEGIAS = [
  { tipo: "FO", nombre: "Estrategias FO", subtitulo: "Fortalezas con oportunidades · ofensivas", icono: "fo" },
  { tipo: "FA", nombre: "Estrategias FA", subtitulo: "Fortalezas frente a amenazas · defensivas", icono: "fa" },
  { tipo: "DO", nombre: "Estrategias DO", subtitulo: "Debilidades con oportunidades · de reorientación", icono: "do" },
  { tipo: "DA", nombre: "Estrategias DA", subtitulo: "Debilidades frente a amenazas · de supervivencia", icono: "da" },
];

// Modelo del FODA: cuatro cuadrantes (interno arriba, externo abajo) y, si las hay, las estrategias cruzadas por tipo.
export function modelo(datos) {
  const base = { titulo: "Matriz FODA", proyecto: datos.proyecto || "", corte: null, vacio: true };
  const c = datos.cuadrantes || {};
  const cuadrantes = CUADRANTES.map((q) => ({ ...q, items: (c[q.clave] || []).map((i) => ({ codigo: i.codigo, texto: i.texto, evidencia: i.evidencia || "" })) }));
  const total = cuadrantes.reduce((a, q) => a + q.items.length, 0);
  const lista = datos.estrategias || [];
  const estrategias = ESTRATEGIAS.map((e) => ({
    ...e,
    items: lista.filter((x) => x.tipo === e.tipo).map((x) => ({ codigo: x.codigo, texto: x.texto, combina: (x.combina || []).join(" · ") })),
  }));
  const conEstrategias = estrategias.some((e) => e.items.length > 0);
  return { ...base, vacio: total === 0, total, cuadrantes, estrategias, conEstrategias };
}
