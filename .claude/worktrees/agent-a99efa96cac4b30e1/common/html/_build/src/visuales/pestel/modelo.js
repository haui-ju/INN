export const visual = "pestel";
export const fecha = () => null;
export const ancho = "fijo";
export const anchoImagen = 1120;

const FACTORES = [
  { clave: "politico", nombre: "Político", icono: "politico" },
  { clave: "economico", nombre: "Económico", icono: "economico" },
  { clave: "social", nombre: "Social", icono: "social" },
  { clave: "tecnologico", nombre: "Tecnológico", icono: "tecnologico" },
  { clave: "ecologico", nombre: "Ecológico", icono: "ecologico" },
  { clave: "legal", nombre: "Legal", icono: "legal" },
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
  return { titulo: "Análisis PESTEL", proyecto: datos.proyecto || "", corte: null, vacio: total === 0, total, factores };
}
