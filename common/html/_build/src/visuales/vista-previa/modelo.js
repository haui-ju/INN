export const visual = "vista-previa";
export const fecha = () => null;
export const ancho = "fijo";
export const anchoImagen = 0;

// Modelo de la vista previa: los datos son los tokens del sistema de diseño.
export function modelo(datos) {
  const base = { titulo: "Sistema de diseño", proyecto: datos.proyecto || "", corte: null, vacio: true };
  const tk = datos.tokens;
  if (!tk || !tk.color || !tk.color.claro) return base;
  return {
    ...base,
    vacio: false,
    colores: Object.keys(tk.color.claro),
    escala: Object.entries(tk.tipografia.escala).map(([k, v]) => ({ clave: k, valor: v })),
    espacios: Object.entries(tk.espacio).map(([k, v]) => ({ clave: k, valor: v })),
    radios: Object.entries(tk.radio).map(([k, v]) => ({ clave: k, valor: v })),
    sombras: Object.keys(tk.sombra),
  };
}
