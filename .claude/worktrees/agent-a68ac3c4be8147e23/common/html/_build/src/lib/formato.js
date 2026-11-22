// Funciones puras de formato (sin React ni DOM). Los indicadores se muestran tal como vienen en `calculado`.
export function fmt(iso) {
  if (!iso) return "";
  const [a, m, d] = String(iso).split("-");
  return `${d}-${m}-${a}`;
}

export function dia(iso) {
  const [a, m, d] = String(iso).split("-").map(Number);
  return Date.UTC(a, m - 1, d) / 86400000;
}

export function corteTexto(datos) {
  return datos.fecha_corte ? `al ${fmt(datos.fecha_corte)}` : "Línea base";
}

const MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
export function mesCorto(iso) {
  const [a, m] = String(iso).split("-");
  return `${MESES[Number(m) - 1]} ${a}`;
}

// Textos de los indicadores a partir de `calculado` (solo da formato; no recalcula nada).
export function textos(datos) {
  const c = datos.calculado || {};
  const g = (datos.gantt && datos.gantt.tareas) || [];
  const tb = (datos.tablero && datos.tablero.tarjetas) || [];
  const total = g.length || tb.length;
  const t = { corte: corteTexto(datos), avance_global: `${c.avance_global || 0} %` };
  for (const [n, v] of Object.entries(c.avance_por_sprint || {})) t[`avance_sprint:${n}`] = `${v} %`;
  t.tareas_hechas = `${c.tareas_hechas || 0} de ${total}`;
  t.atrasadas = String((c.atrasadas || []).length);
  const tc = c.tiempo_ciclo_promedio_dias;
  t.tiempo_ciclo = tc == null ? "Sin datos" : `${tc.toFixed(1).replace(".", ",")} días`;
  const r = c.rendimiento_por_semana || {};
  const k = Object.keys(r).length;
  const n = Object.values(r).reduce((a, s) => a + s, 0);
  t.rendimiento = k === 0 ? "Sin datos" : `${n} ${n === 1 ? "tarea" : "tareas"} en ${k} ${k === 1 ? "semana" : "semanas"}`;
  const lim = {};
  for (const col of (datos.tablero && datos.tablero.columnas) || []) lim[col.nombre] = col.wip;
  for (const [col, cant] of Object.entries(c.wip_actual || {})) t[`wip:${col}`] = lim[col] ? `${cant} de ${lim[col]}` : String(cant);
  return t;
}

export function superadas(datos) {
  const lim = {};
  for (const col of (datos.tablero && datos.tablero.columnas) || []) lim[col.nombre] = col.wip;
  const wip = (datos.calculado || {}).wip_actual || {};
  return Object.keys(wip).filter((col) => lim[col] && wip[col] > lim[col]).sort();
}

// Fechas como días (UTC) para armar rejillas de tiempo.
export function diaSemana(d) {
  return (new Date(d * 86400000).getUTCDay() + 6) % 7; // 0 = lunes
}
export function isoDe(d) {
  return new Date(d * 86400000).toISOString().slice(0, 10);
}
export function nombreMes(iso) {
  return mesCorto(iso);
}
export function iniciales(nombre) {
  const p = String(nombre || "").trim().split(/\s+/).filter(Boolean);
  return ((p[0] || "")[0] || "").toUpperCase() + ((p[1] || "")[0] || "").toUpperCase();
}
