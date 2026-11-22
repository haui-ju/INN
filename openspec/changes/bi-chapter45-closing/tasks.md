# Tasks

## 1. Base y contrato con el capítulo 3

- [ ] 1.1 Revisar lo aplicado de `bi-chapter3-build` (formato de `valores.json`, nombre y contenido de `capturas/`, marcador `<!-- captura: <id> -->` y códigos `PAG` y `MED`) y ajustar estas tareas si algo difiere; verificar que `projectcfg.py check --skill 10-make-storytelling` avisa por 09 cuando falta su corrida.

## 2. Skill 10-make-storytelling

- [ ] 2.1 Crear `common/10-storytelling/guia.md` y `models/` (README y plantilla de la sección 4, con ficha, instrucciones, formato, ejemplo y checklist); verificar que la plantilla tiene las cinco partes.
- [ ] 2.2 Crear `_shared/rules/storytelling.py` con `PREFIJOS` (`HLZ`) y las comprobaciones de la spec `data-storytelling`: encabezado de `secciones/4.md`, cada `OE` con hallazgo, cada hallazgo con captura, cada cifra presente en `valores.json`, declaración de datos generados y títulos de tabla; verificar con pruebas de cada escenario.
- [ ] 2.3 Escribir `.claude/skills/10-make-storytelling/SKILL.md` (fuentes, propuesta de hallazgos con confirmación, escritura, revisión de redacción, validación y registro); verificar con una prueba de flujo que una corrida de ejemplo valida y deja la sección 4 disponible.
- [ ] 2.4 Escribir `10-make-storytelling-update/SKILL.md` y `references/dependencias.md`; verificar con una prueba que cambiar un valor del dashboard actualiza solo los hallazgos que lo citan.

## 3. Skill 11-make-conclusions

- [ ] 3.1 Crear `common/11-conclusions/guia.md` y `models/` (README y plantilla de la sección 5); verificar que la plantilla tiene las cinco partes.
- [ ] 3.2 Crear `_shared/rules/conclusions.py` con `PREFIJOS` (`CNC`, `REC`, `LEC`) y las comprobaciones de la spec `report-conclusions`: encabezado de `secciones/5.md`, una conclusión por `OE` y una del `OG`, estado respaldado por valor y meta (con sentido del indicador), KPI sin meta declarado, recomendaciones ligadas a una conclusión, limitación de datos generados; verificar con pruebas de cada escenario.
- [ ] 3.3 Escribir `.claude/skills/11-make-conclusions/SKILL.md`; verificar con una prueba de flujo que una corrida de ejemplo valida y deja la sección 5 disponible.
- [ ] 3.4 Escribir `11-make-conclusions-update/SKILL.md` y `references/dependencias.md`; verificar con una prueba que cambiar una meta cambia solo la conclusión de su objetivo y las recomendaciones ligadas a ella.

## 4. Integración

- [ ] 4.1 Armar un informe de prueba con `report.py construir` sobre corridas de ejemplo de 03 a 11; verificar que los cinco capítulos aparecen completos, que la sección 4 trae sus capturas numeradas y que `faltantes.md` queda sin secciones ni anexos pendientes.
- [ ] 4.2 Ejecutar `python3 -m unittest discover -s .claude/skills/_shared/tests`, `python3 .claude/skills/_shared/html_tpl.py comprobar` y `openspec validate bi-chapter45-closing --strict`; verificar que todo pasa.
- [ ] 4.3 Actualizar `openspec/ROADMAP.md` si nombra estas skills; verificar que las referencias a 10 y 11 coinciden con `pipeline.json`.

## Workflow follow-up

- Sincronizar las specs y archivar el change con `/opsx:archive`.
