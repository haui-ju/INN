#!/usr/bin/env node
/**
 * Comprobaciones locales del pipeline de skills de BI (sin Python).
 * Uso: node scripts/check-pipeline.mjs
 *      npm run check:pipeline
 *
 * Revisa .claude/skills/_shared/pipeline.json: orden consecutivo igual al número de la skill,
 * carpetas numeradas únicas, secciones del informe únicas y presentes en el índice,
 * skills numeradas instaladas que figuran en el pipeline y enlaces relativos de cada SKILL.md.
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const skillsRoot = join(root, '.claude', 'skills');
const errors = [];
const fail = (msg) => errors.push(msg);

const pipe = JSON.parse(readFileSync(join(skillsRoot, '_shared', 'pipeline.json'), 'utf8')).skills;

// 1) Orden consecutivo, número del nombre = orden, esquema de nombres y carpeta numerada
pipe.forEach((s, i) => {
  if (s.orden !== i) fail(`${s.nombre}: orden ${s.orden}, se esperaba ${i}`);
  if (Number.parseInt(s.nombre.slice(0, 2), 10) !== s.orden) fail(`${s.nombre}: el número no coincide con el orden`);
  if (!/^\d{2}-(init|make|design)(-[a-z0-9]+)*$/.test(s.nombre)) fail(`${s.nombre}: nombre fuera del esquema`);
  if (s.carpeta) {
    const esperada = s.verbo === 'design' ? s.nombre : s.nombre.replace('-make-', '-');
    if (s.carpeta !== esperada) fail(`${s.nombre}: carpeta ${s.carpeta}, se esperaba ${esperada}`);
  }
  for (const r of s.requiere) {
    const req = pipe.find((x) => x.nombre === r);
    if (!req) fail(`${s.nombre}: requiere ${r}, que no está en el pipeline`);
    else if (req.orden >= s.orden) fail(`${s.nombre}: requiere ${r}, que no es anterior`);
  }
});

// 2) Carpetas y secciones únicas
const carpetas = pipe.map((s) => s.carpeta).filter(Boolean);
if (new Set(carpetas).size !== carpetas.length) fail('hay carpetas de corrida repetidas');
const secciones = pipe.flatMap((s) => s.secciones || []);
const repetidas = secciones.filter((x, i) => secciones.indexOf(x) !== i);
if (repetidas.length) fail(`secciones declaradas en dos skills: ${[...new Set(repetidas)].join(', ')}`);

// 3) Cada sección del índice tiene skill y viceversa
const indice = readFileSync(join(root, 'common', 'structure', 'model1.md'), 'utf8');
const puntos = [...indice.matchAll(/^- (\d+(?:\.\d+)?)\. /gm)].map((m) => m[1]);
if (JSON.stringify(puntos) !== JSON.stringify(secciones)) {
  fail(`el índice (${puntos.join(', ')}) no coincide con las secciones del pipeline (${secciones.join(', ')})`);
}

// 4) Skills numeradas instaladas que no están en el pipeline, y homólogas -update
const nombres = new Set(pipe.flatMap((s) => [s.nombre, `${s.nombre}-update`]));
for (const d of readdirSync(skillsRoot, { withFileTypes: true })) {
  if (d.isDirectory() && /^\d{2}/.test(d.name) && !nombres.has(d.name)) fail(`skill fuera del pipeline: ${d.name}`);
}
for (const s of pipe) {
  if (!existsSync(join(skillsRoot, s.nombre))) continue;
  if (s.update !== existsSync(join(skillsRoot, `${s.nombre}-update`))) fail(`${s.nombre}: update=${s.update} no coincide con lo instalado`);
}

// 5) Enlaces relativos rotos en los SKILL.md
const linkRe = /\]\(([^)]+)\)/g;
for (const name of readdirSync(skillsRoot)) {
  const skillMd = join(skillsRoot, name, 'SKILL.md');
  if (!existsSync(skillMd)) continue;
  const text = readFileSync(skillMd, 'utf8');
  for (const m of text.matchAll(linkRe)) {
    const rel = m[1];
    if (!rel.startsWith('.')) continue;
    const target = resolve(dirname(skillMd), rel.split('#')[0]);
    if (!existsSync(target)) fail(`enlace roto en ${name}/SKILL.md → ${rel}`);
  }
}

if (errors.length) {
  console.error(`\nFAIL: ${errors.length} incidencia(s)`);
  for (const e of errors) console.error(' -', e);
  process.exit(1);
}
console.log(`PASS check-pipeline (${pipe.length} skills, ${secciones.length} secciones)`);
process.exit(0);
