## 1. Playbook, plantillas y prerrequisitos

- [x] 1.1 Escribir `common/report/guia.md` (orden, marcas y versiones acumuladas, tabla de qué pasos alimentan cada avance, puntos derivados y sin fuente, numeración, figuras, referencias cruzadas, referencias bibliográficas, faltantes, formatos de salida, errores y checklist) y verificar que cubre cada requisito de la spec y que no usa las expresiones prohibidas
- [x] 1.2 Crear `common/report/models/` con `rep-0-control-documento.md`, `rep-9-referencias.md` (lista cerrada de las referencias verificadas de los playbooks, extraídas de ellos, sin añadir fuentes nuevas) y `README.md` (ficha, instrucciones, formato, ejemplo y checklist)
- [x] 1.3 Añadir a `pipeline.json` el campo `requiere_por_avance` de la skill 19 (derivado de las marcas del índice y de `report_map.json`), aceptar `--avance N` en `projectcfg.py check` y ampliar `test_projectcfg.py`; verificar que las demás skills no cambian y que el pipeline sigue con 20 pasos

## 2. Armado y validación

- [x] 2.1 Crear `.claude/skills/_shared/report_map.json` y `report.py` (`plan`, `construir` y `render`: puntos por marca, bloques por encabezado numerado, re-numeración y niveles, figuras y evidencias, referencias, faltantes, HTML autónomo) con `tests/test_report.py` que arma los avances 1 y 2 y el final con las corridas de las plantillas de los demás pasos
- [x] 2.2 Registrar `"report": "report"` en `RULES` de `validate_run.py`; implementar `rules/report.py` (puntos, orden, versiones, figuras, referencias, referencias cruzadas, no repetición, faltantes, HTML) y `tests/test_report_rules.py` con los documentos que arma el script

## 3. Skill

- [x] 3.1 Crear `.claude/skills/19-make-report/SKILL.md` (fuentes obligatorias, reglas, flujo con plan y confirmación, escritura con `report.py`, validación y registro); sin `-update`

## 4. Verificación

- [x] 4.1 Ejecutar `openspec validate add-report-assembly --strict`, `openspec validate --specs --strict`, las pruebas del kit y la comprobación de que la skill `19-make-report` aparece ordenada en `.claude/skills/` y no existe `19-make-report-update`; verificar que todo pasa
