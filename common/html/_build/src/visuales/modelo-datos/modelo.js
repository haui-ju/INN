export const visual = "modelo-datos";
export const fecha = () => null;
export const ancho = "fijo";
export const anchoImagen = 1600;
export const laminas = true;

const ANCHO = 1440;
const CABECERA = 34;
const FILA = 25;
const PIE = 10;
const SEPARACION = 64;

// El modelo declara el tipo de las medidas, no el de cada atributo; el diagrama lo deduce del nombre del campo.
export function tipoDeCampo(nombre) {
  const n = String(nombre).toLowerCase();
  if (n.endsWith("_key") || n === "anio" || n === "mes" || n === "dia" || n.endsWith("_id")) return "int";
  if (n === "fecha" || n.startsWith("fecha_")) return "date";
  if (n.startsWith("hora")) return "time";
  if (n.startsWith("es_") || n.startsWith("tiene_")) return "bool";
  if (n.endsWith("_pct") || /(precio|costo|monto|valor|meta|margen|comision)/.test(n)) return "decimal";
  return "string";
}
const tipoDeMedida = (t) => ({ entero: "int", decimal: "decimal", texto: "string" }[t] || t || "decimal");

// Líneas de relación con notación de pata de gallo: dos trazos en el lado «uno» y la pata de gallo con círculo en el lado «varios».
function simbolos(sx, sy, ex, ey, ladoDesde, ladoHacia) {
  const L = Math.hypot(ex - sx, ey - sy) || 1;
  const ux = (ex - sx) / L, uy = (ey - sy) / L, nx = -uy, ny = ux;
  const p = (x, y) => `${x.toFixed(1)},${y.toFixed(1)}`;
  const uno = (bx, by, dir) => [12, 18].map((d) => `M${p(bx + dir * ux * d + nx * 7, by + dir * uy * d + ny * 7)} L${p(bx + dir * ux * d - nx * 7, by + dir * uy * d - ny * 7)}`).join(" ");
  const varios = (bx, by, dir) => {
    const ax = bx + dir * ux * 15, ay = by + dir * uy * 15;
    return { patas: `M${p(ax, ay)} L${p(bx + nx * 8, by + ny * 8)} M${p(ax, ay)} L${p(bx - nx * 8, by - ny * 8)} M${p(ax, ay)} L${p(bx, by)}`, circulo: { x: bx + dir * ux * 23, y: by + dir * uy * 23 } };
  };
  const trazos = [];
  let circulo = null;
  // extremo de la dimensión (S): `ladoHacia` ; extremo del hecho (E): `ladoDesde`
  if (ladoHacia === "*") { const v = varios(sx, sy, 1); trazos.push(v.patas); circulo = v.circulo; } else trazos.push(uno(sx, sy, 1));
  let circuloE = null;
  if (ladoDesde === "*") { const v = varios(ex, ey, -1); trazos.push(v.patas); circuloE = v.circulo; } else trazos.push(uno(ex, ey, -1));
  return { d: trazos.join(" "), circulos: [circulo, circuloE].filter(Boolean) };
}

// Rejilla impar para que exista una celda central. Las columnas y filas opuestas miden lo mismo: así la central queda en el centro exacto.
function rejilla(n) {
  const cols = n <= 9 ? 3 : 5;
  let filas = 3;
  // Con cinco columnas deja tres celdas libres: si la rejilla se llena, alguna línea acaba pasando sobre otra tabla.
  while (cols * filas < n + (cols === 5 ? 3 : 0)) filas += 2;
  const anchos = cols === 3 ? [360, 360, 360] : [230, 230, 290, 230, 230];
  const hueco = (ANCHO - anchos.reduce((a, b) => a + b, 0)) / (cols - 1);
  const xs = anchos.map((_, c) => anchos.slice(0, c).reduce((a, b) => a + b + hueco, 0));
  return { cols, filas, anchos, xs, centro: (cols * filas - 1) / 2 };
}

// `celdas[i]` es el índice de la tabla que ocupa la celda i; los índices sin tabla son celdas vacías.
function ubicar(tablas, g, celdas) {
  const altos = Array(g.filas).fill(0);
  celdas.forEach((t, i) => {
    if (t >= tablas.length) return;
    const f = Math.floor(i / g.cols);
    for (const k of [f, g.filas - 1 - f]) altos[k] = Math.max(altos[k], tablas[t].h);
  });
  const ys = [];
  let y = 0;
  altos.forEach((h) => { ys.push(y); if (h) y += h + SEPARACION; });
  const cajas = [];
  celdas.forEach((t, i) => {
    if (t >= tablas.length) return;
    const f = Math.floor(i / g.cols), c = i % g.cols, h = tablas[t].h;
    cajas[t] = { x: g.xs[c], y: ys[f] + (altos[f] - h) / 2, w: g.anchos[c], h, cx: g.xs[c] + g.anchos[c] / 2, cy: ys[f] + altos[f] / 2 };
  });
  return { cajas, alto: Math.max(0, y - SEPARACION) };
}

// Punto donde el segmento que une dos centros sale de la caja `a`.
function borde(a, b) {
  const dx = b.cx - a.cx, dy = b.cy - a.cy;
  const t = Math.min(a.w / 2 / Math.abs(dx), a.h / 2 / Math.abs(dy));
  return { x: a.cx + dx * t, y: a.cy + dy * t };
}

function atraviesa(a, b, caja) {
  let min = 0, max = 1;
  for (const [o, d, desde, largo] of [[a.cx, b.cx - a.cx, caja.x, caja.w], [a.cy, b.cy - a.cy, caja.y, caja.h]]) {
    const ini = desde - 6, fin = desde + largo + 6;
    if (d === 0) { if (o < ini || o > fin) return false; continue; }
    min = Math.max(min, Math.min((ini - o) / d, (fin - o) / d));
    max = Math.min(max, Math.max((ini - o) / d, (fin - o) / d));
    if (min > max) return false;
  }
  return true;
}

const giro = (a, b, c) => (b.cx - a.cx) * (c.cy - a.cy) - (b.cy - a.cy) * (c.cx - a.cx);

// Menor es mejor: líneas que no pisan tablas, sin cruces, cortas, y tablas repartidas por igual alrededor del centro.
function costo(tablas, g, enlaces, celdas) {
  const { cajas, alto } = ubicar(tablas, g, celdas);
  let total = alto * 2, dx = 0, dy = 0;
  cajas.forEach((c) => { dx += c.cx - ANCHO / 2; dy += c.cy - alto / 2; });
  total += Math.abs(dx) + Math.abs(dy);
  enlaces.forEach(([i, j], k) => {
    const a = cajas[i], b = cajas[j];
    total += Math.hypot(b.cx - a.cx, b.cy - a.cy);
    for (let t = 0; t < cajas.length; t++) if (t !== i && t !== j && atraviesa(a, b, cajas[t])) total += 20000;
    for (let q = k + 1; q < enlaces.length; q++) {
      const [u, v] = enlaces[q];
      if (u === i || u === j || v === i || v === j) continue;
      const c = cajas[u], d = cajas[v];
      if (giro(a, b, c) * giro(a, b, d) < 0 && giro(c, d, a) * giro(c, d, b) < 0) total += 5000;
    }
  });
  return total;
}

// Fija la central y mejora el resto por intercambios. La semilla es fija: los mismos datos dan siempre el mismo dibujo.
function distribuir(tablas, enlaces, central) {
  const g = rejilla(tablas.length);
  const otros = Array.from({ length: g.cols * g.filas }, (_, i) => i).filter((i) => i !== central);
  const intentos = Math.max(3, Math.ceil(300000 / tablas.length ** 4));
  let semilla = 7, mejor = null, menor = Infinity;
  const azar = () => (semilla = (semilla * 16807) % 2147483647) / 2147483647;
  for (let n = 0; n < Math.min(intentos, 60); n++) {
    const orden = [...otros];
    for (let i = orden.length - 1; i > 0; i--) { const j = Math.floor(azar() * (i + 1)); [orden[i], orden[j]] = [orden[j], orden[i]]; }
    const celdas = [...orden.slice(0, g.centro), central, ...orden.slice(g.centro)];
    let actual = costo(tablas, g, enlaces, celdas), mejora = true;
    while (mejora) {
      mejora = false;
      for (let i = 0; i < celdas.length; i++) for (let j = i + 1; j < celdas.length; j++) {
        if (i === g.centro || j === g.centro || (celdas[i] >= tablas.length && celdas[j] >= tablas.length)) continue;
        [celdas[i], celdas[j]] = [celdas[j], celdas[i]];
        const c = costo(tablas, g, enlaces, celdas);
        if (c < actual - 0.001) { actual = c; mejora = true; } else [celdas[i], celdas[j]] = [celdas[j], celdas[i]];
      }
    }
    if (actual < menor) { menor = actual; mejor = celdas; }
  }
  return ubicar(tablas, g, mejor);
}

// Modelo del diagrama de base de datos: tablas con sus columnas (el hecho con más relaciones al centro, el resto alrededor) y una línea recta por relación.
// La posición y la altura de cada tabla se calculan aquí para que las líneas lleguen exactamente a su borde.
export function modelo(datos) {
  const rels = datos.relaciones || [];
  const dimensiones = (datos.dimensiones || []).map((d) => {
    const filas = [{ nombre: d.clave, tipo: "int", marca: "PK" }, ...(d.atributos || []).filter((a) => a !== d.clave).map((a) => ({ nombre: a, tipo: tipoDeCampo(a), marca: "" }))];
    return { codigo: d.codigo, nombre: d.nombre, clave: d.clave, filas, h: CABECERA + FILA * filas.length + PIE };
  });
  const hechos = (datos.hechos || []).map((h) => {
    const filas = [
      ...(h.claves || []).map((k) => ({ nombre: k, tipo: "int", marca: "FK" })),
      ...(h.medidas || []).map((m) => ({ nombre: m.nombre, tipo: tipoDeMedida(m.tipo), marca: "" })),
    ];
    return { codigo: h.codigo, nombre: h.nombre, granularidad: h.granularidad || "", filas, h: CABECERA + FILA * filas.length + PIE };
  });
  const tablas = [...hechos, ...dimensiones];
  const indice = new Map(tablas.map((t, i) => [t.nombre, i]));
  const unidas = rels.filter((r) => r.desde !== r.hacia && indice.has(r.desde) && indice.has(r.hacia));
  const enlaces = unidas.map((r) => [indice.get(r.desde), indice.get(r.hacia)]);
  const grado = hechos.map((_, i) => enlaces.filter((e) => e.includes(i)).length);
  const central = hechos.length ? grado.indexOf(Math.max(...grado)) : 0;
  const { cajas, alto } = tablas.length ? distribuir(tablas, enlaces, central) : { cajas: [], alto: 0 };
  tablas.forEach((t, i) => Object.assign(t, { x: cajas[i].x, y: cajas[i].y, w: cajas[i].w }));
  const lineas = unidas.map((r, k) => {
    const [desde, hacia] = enlaces[k].map((i) => cajas[i]);
    const { x: sx, y: sy } = borde(hacia, desde), { x: ex, y: ey } = borde(desde, hacia);
    const [lado1 = "*", lado2 = "1"] = String(r.cardinalidad || "*:1").split(":");
    const s = simbolos(sx, sy, ex, ey, lado1, lado2);
    return { codigo: r.codigo, cardinalidad: r.cardinalidad, sx, sy, ex, ey, simbolos: s.d, circulos: s.circulos };
  });
  const relaciones = rels.map((r) => ({ codigo: r.codigo, desde: r.desde, hacia: r.hacia, campos: r.campos, cardinalidad: r.cardinalidad, filtro: r.filtro }));
  return {
    titulo: "Modelo de datos en estrella", proyecto: datos.proyecto || "", corte: null, vacio: hechos.length + dimensiones.length === 0,
    ancho: ANCHO, alto, dimensiones, hechos, lineas, relaciones,
  };
}
