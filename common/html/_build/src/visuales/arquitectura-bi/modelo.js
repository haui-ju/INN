export const visual = "arquitectura-bi";
export const fecha = () => null;
export const ancho = "completo";
export const anchoImagen = 1560;

const CAPAS = {
  fuentes: { tono: "neutro", icono: "fuentes", subtitulo: "De dónde salen los datos" },
  etl: { tono: "alerta", icono: "etl", subtitulo: "Extraer, depurar y cargar" },
  almacenamiento: { tono: "exito", icono: "almacenamiento", subtitulo: "Dónde queda el modelo" },
  visualizacion: { tono: "marca", icono: "visualizacion", subtitulo: "Dónde se consulta" },
};

// Modelo de la arquitectura: cuatro capas en orden, cada una con sus componentes y las herramientas elegidas (o pendientes).
export function modelo(datos) {
  const capas = (datos.capas || []).map((c, i) => ({
    clave: c.clave, nombre: c.nombre, numero: i + 1, ...(CAPAS[c.clave] || { tono: "neutro", icono: "fuentes", subtitulo: "" }),
    herramientas: (c.herramientas || []).map((h) => ({ nombre: h, pendiente: String(h).trim().toLowerCase() === "pendiente" })),
    componentes: (c.componentes || []).map((x) => ({ codigo: x.codigo, nombre: x.nombre, funcion: x.funcion || "", entradaSalida: x.entrada_salida || "" })),
  }));
  const total = capas.reduce((a, c) => a + c.componentes.length, 0);
  return { titulo: "Arquitectura de BI", proyecto: datos.proyecto || "", corte: null, vacio: total === 0, total, capas };
}
