export const visual = "ishikawa";
export const fecha = () => null;
export const ancho = "completo";
export const anchoImagen = 1640;

const ORDEN_6M = ["Método", "Mano de obra", "Materiales", "Maquinaria", "Medición", "Medio ambiente"];

// Modelo del Ishikawa: el efecto en la cabeza del pez y las categorías 6M repartidas arriba y abajo de la espina, cada una con su color.
export function modelo(datos) {
  const categorias = (datos.categorias || [])
    .map((c, i) => {
      const pos = ORDEN_6M.indexOf(c.nombre);
      return { nombre: c.nombre, k: `serie-${((pos >= 0 ? pos : i) % 8) + 1}`, causas: (c.causas || []).map((x) => ({ codigo: x.codigo, texto: x.texto })) };
    })
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
