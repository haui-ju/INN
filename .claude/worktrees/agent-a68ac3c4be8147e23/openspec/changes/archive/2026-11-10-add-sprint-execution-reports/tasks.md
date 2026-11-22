## 1. Playbook y plantillas

- [x] 1.1 Escribir `common/sprint-reports/guia.md` (reglas, bitácora, resultados de pruebas, riesgos y cambios, evidencias, informe de avance con sus nueve puntos, Sprint Review, retrospectiva, errores y checklist, Referencias solo con fuentes ya verificadas: Schwaber y Sutherland 2020 y Anderson 2010); verificar que cubre cada requisito de las dos specs y que no usa las expresiones prohibidas
- [x] 1.2 Crear `common/sprint-reports/models/` con `log-1-bitacora-sprint.md`, `rep-1-informe-avance.md`, `rep-2-acta-review-retro.md` y `README.md` (ficha, instrucciones, formato, ejemplo y checklist; ejemplos coherentes con el plan, el diseño y las historias del proyecto de referencia, con el avance 1 y el avance 2 para probar la no repetición)
- [x] 1.3 Añadir `12-make-ceremonies-kanban` y `13-design-html-boards` a los prerrequisitos de `16-make-sprint-report` en `pipeline.json`; verificar con `diff` que solo cambian esas líneas y que el pipeline sigue con 20 pasos

## 2. Validación

- [x] 2.1 Registrar `"implementation-log"` y `"sprint-report"` en `RULES` de `validate_run.py`; implementar `rules/implementation_log.py` (`PREFIJOS = ["BIT", "RIE"]`: estructura, módulos, entradas, resultados de pruebas, riesgos, evidencias, fechas y trazabilidad contra plan, diseño e historias) y `tests/test_implementation_log.py` con los ejemplos de las plantillas
- [x] 2.2 Implementar `rules/sprint_report.py` (nueve puntos, cifras contra `boards.calcular`, pies de foto, pruebas contra la bitácora, riesgos, plan del siguiente sprint, acta, no repetición contra el avance anterior, citas) y `tests/test_sprint_report.py` con los ejemplos de las plantillas, un `data.json` generado con `boards.py` para cada corte y una bitácora de ejemplo; la skill y el validador comparten una función que calcula las líneas «Cifras»

## 3. Skills

- [x] 3.1 Crear `.claude/skills/15-make-implementation-log/SKILL.md` (fuentes obligatorias, reglas, flujo con confirmación, escritura, validación y registro)
- [x] 3.2 Crear `.claude/skills/15-make-implementation-log-update/SKILL.md` y `references/dependencias.md`
- [x] 3.3 Crear `.claude/skills/16-make-sprint-report/SKILL.md` (pide el sprint, registra con `--sprint N`)
- [x] 3.4 Crear `.claude/skills/16-make-sprint-report-update/SKILL.md` y `references/dependencias.md`

## 4. Verificación

- [x] 4.1 Ejecutar `openspec validate add-sprint-execution-reports --strict`, `openspec validate --specs --strict`, las pruebas del kit y la comprobación de que las skills `15-…` y `16-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa
