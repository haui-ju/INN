export const visual = "ishikawa";
export const fecha = () => null;
export const ancho = "completo";
export const anchoImagen = 1560;

// Modelo del Ishikawa: el efecto a la derecha y las categorías repartidas arriba y abajo de la espina.
export function modelo(datos) {
  const categorias = (datos.categorias || [])
    .map((c) => ({ nombre: c.nombre, causas: (c.causas || []).map((x) => ({ codigo: x.codigo, texto: x.texto })) }))
    .filter((c) => c.causas.length > 0);
  const mitad = Math.ceil(categorias.length / 2);
  const arriba = categorias.slice(0, mitad);
  const abajo = categorias.slice(mitad);
  const total = categorias.reduce((a, c) => a + c.causas.length, 0);
  return {
    titulo: "Diagrama de Ishikawa", proyecto: datos.proyecto || "", corte: null, vacio: total === 0, total,
    efecto: datos.efecto || "", arriba, abajo, columnas: Math.max(arriba.length, abajo.length, 1),
  };
}
