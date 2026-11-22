export const visual = "pestel";
export const fecha = () => null;
export const ancho = "fijo";
export const anchoImagen = 1120;

const FACTORES = [
  { clave: "politico", k: "serie-5", letra: "P", nombre: "Político", icono: "politico" },
  { clave: "economico", k: "serie-4", letra: "E", nombre: "Económico", icono: "economico" },
  { clave: "social", k: "serie-7", letra: "S", nombre: "Social", icono: "social" },
  { clave: "tecnologico", k: "serie-3", letra: "T", nombre: "Tecnológico", icono: "tecnologico" },
  { clave: "ecologico", k: "serie-6", letra: "E", nombre: "Ecológico", icono: "ecologico" },
  { clave: "legal", k: "serie-8", letra: "L", nombre: "Legal", icono: "legal" },
];

// Modelo del PESTEL: seis factores en orden fijo, cada hallazgo con su efecto, su tipo (oportunidad o amenaza) y su fuente.
export function modelo(datos) {
  const por = Object.fromEntries((datos.factores || []).map((f) => [f.clave, f]));
  const factores = FACTORES.map((f) => ({
    ...f,
    items: ((por[f.clave] || {}).items || []).map((i) => ({
      codigo: i.codigo, texto: i.texto, efecto: i.efecto || "", tipo: i.tipo || "", fuente: i.fuente || "", favorable: i.tipo === "Oportunidad",
    })),
  }));
  const total = factores.reduce((a, f) => a + f.items.length, 0);
  const todos = factores.flatMap((f) => f.items);
  const oportunidades = todos.filter((i) => i.favorable).length;
  const amenazas = todos.filter((i) => i.tipo === "Amenaza").length;
  return { titulo: "Análisis PESTEL", proyecto: datos.proyecto || "", corte: null, vacio: total === 0, total, oportunidades, amenazas, factores };
}
