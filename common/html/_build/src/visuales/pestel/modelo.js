export const visual = "pestel";
export const fecha = () => null;
export const ancho = "fijo";
export const anchoImagen = 1700;
export const laminas = true;

const FACTORES = [
  { clave: "politico", nombre: "Político", icono: "politico", k: "serie-5", letra: "P" },
  { clave: "economico", nombre: "Económico", icono: "economico", k: "serie-4", letra: "E" },
  { clave: "social", nombre: "Social", icono: "social", k: "serie-7", letra: "S" },
  { clave: "tecnologico", nombre: "Tecnológico", icono: "tecnologico", k: "serie-3", letra: "T" },
  { clave: "ecologico", nombre: "Ecológico", icono: "ecologico", k: "serie-6", letra: "E" },
  { clave: "legal", nombre: "Legal", icono: "legal", k: "serie-8", letra: "L" },
];

// Modelo del PESTEL: dos láminas de tres factores (para que el texto sea legible en una diapositiva), cada una con su título,
// su balance de oportunidades y amenazas y, por factor, cada hallazgo con su efecto, su tipo y su fuente.
const PARTES = [
  { claves: ["politico", "economico", "social"], titulo: "Análisis PESTEL (1 de 2): político, económico y social" },
  { claves: ["tecnologico", "ecologico", "legal"], titulo: "Análisis PESTEL (2 de 2): tecnológico, ecológico y legal" },
];

export function modelo(datos) {
  const por = Object.fromEntries((datos.factores || []).map((f) => [f.clave, f]));
  const factores = FACTORES.map((f) => ({
    ...f,
    items: ((por[f.clave] || {}).items || []).map((i) => ({
      codigo: i.codigo, texto: i.texto, efecto: i.efecto || "", tipo: i.tipo || "", fuente: i.fuente || "", favorable: i.tipo === "Oportunidad",
    })),
  }));
  const total = factores.reduce((a, f) => a + f.items.length, 0);
  const partes = PARTES.map((p) => {
    const propios = factores.filter((f) => p.claves.includes(f.clave));
    const todos = propios.flatMap((f) => f.items);
    return { titulo: p.titulo, factores: propios, oportunidades: todos.filter((i) => i.favorable).length, amenazas: todos.filter((i) => i.tipo === "Amenaza").length };
  });
  return { titulo: "Análisis PESTEL", proyecto: datos.proyecto || "", corte: null, vacio: total === 0, total, laminas: true, partes };
}
