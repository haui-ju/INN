export const visual = "foda";
export const fecha = () => null;
export const ancho = "fijo";
export const anchoImagen = 1700;
export const laminas = true;

const CUADRANTES = [
  { clave: "fortalezas", nombre: "Fortalezas", grupo: "Interno", signo: "Favorable", k: "serie-1", letra: "F", icono: "fuerza" },
  { clave: "debilidades", nombre: "Debilidades", grupo: "Interno", signo: "Desfavorable", k: "serie-4", letra: "D", icono: "debil" },
  { clave: "oportunidades", nombre: "Oportunidades", grupo: "Externo", signo: "Favorable", k: "serie-3", letra: "O", icono: "oportunidad" },
  { clave: "amenazas", nombre: "Amenazas", grupo: "Externo", signo: "Desfavorable", k: "serie-2", letra: "A", icono: "amenaza" },
];

const ESTRATEGIAS = [
  { tipo: "FO", nombre: "Estrategias FO", subtitulo: "Fortalezas con oportunidades · ofensivas", icono: "fo", k: "serie-1" },
  { tipo: "FA", nombre: "Estrategias FA", subtitulo: "Fortalezas frente a amenazas · defensivas", icono: "fa", k: "serie-2" },
  { tipo: "DO", nombre: "Estrategias DO", subtitulo: "Debilidades con oportunidades · de reorientación", icono: "do", k: "serie-3" },
  { tipo: "DA", nombre: "Estrategias DA", subtitulo: "Debilidades frente a amenazas · de supervivencia", icono: "da", k: "serie-4" },
];

// Modelo del FODA: dos láminas con proporción de diapositiva: la matriz clásica de cuatro cuadros (fortalezas y debilidades arriba,
// oportunidades y amenazas abajo) y las estrategias cruzadas. La matriz muestra el código y el enunciado de cada ítem; la evidencia
// está en la tabla del informe, para que el texto sea legible en una diapositiva. Cada lámina se puede recortar y pegar sola.
export function modelo(datos) {
  const c = datos.cuadrantes || {};
  const cuadrantes = CUADRANTES.map((q) => ({ ...q, items: (c[q.clave] || []).map((i) => ({ codigo: i.codigo, texto: i.texto, evidencia: i.evidencia || "" })) }));
  const total = cuadrantes.reduce((a, q) => a + q.items.length, 0);
  const lista = datos.estrategias || [];
  const tipos = ESTRATEGIAS.map((e) => ({ ...e, items: lista.filter((x) => x.tipo === e.tipo).map((x) => ({ codigo: x.codigo, texto: x.texto, combina: x.combina || [] })) }));
  const partes = [{ id: "matriz", titulo: "Matriz FODA", cuadrantes }];
  const conEstrategias = tipos.some((e) => e.items.length > 0);
  return { titulo: "Matriz FODA", proyecto: datos.proyecto || "", corte: null, vacio: total === 0, total, laminas: true, partes, conEstrategias, tipos };
}
