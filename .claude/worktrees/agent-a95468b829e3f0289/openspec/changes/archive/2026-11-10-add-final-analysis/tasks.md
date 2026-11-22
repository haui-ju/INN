## 1. Playbook y plantillas

- [x] 1.1 Escribir `common/final-analysis/guia.md` (reglas, resultados Lean y decisión, cumplimiento de objetivos con su base de evidencia, Gantt real y métricas acumuladas, validación con usuarios, discusión, conclusiones, recomendaciones y trabajos futuros, errores y checklist, Referencias solo con fuentes ya verificadas: Ries 2011, Little 2014 y Doran 1981); verificar que cubre cada requisito de las dos specs y que no usa las expresiones prohibidas
- [x] 1.2 Crear `common/final-analysis/models/` con `fin-1-resultados-decision.md`, `fin-2-cumplimiento-objetivos.md`, `fin-3-gantt-metricas.md`, `fin-4-validacion-discusion.md`, `fin-5-conclusiones.md` y `README.md` (ficha, instrucciones, formato, ejemplo y checklist; ejemplos coherentes con el plan Lean, el capítulo 1, los informes de sprint de `common/sprint-reports/` y las historias del proyecto de referencia)
- [x] 1.3 Añadir `03-make-company-chapter` a los prerrequisitos de `18-make-final-analysis` en `pipeline.json`; verificar con `diff` que solo cambia esa línea y que el pipeline sigue con 20 pasos

## 2. Validación

- [x] 2.1 Registrar `"lean-results"` y `"final-analysis"` en `RULES` de `validate_run.py`; implementar `rules/lean_results.py` (`PREFIJOS = ["RES"]`: estructura, experimentos del plan, copia exacta de avance y criterio, evidencias, decisión contra los criterios, hipótesis sin fila) y `tests/test_lean_results.py` con los ejemplos de las plantillas y un plan Lean de referencia
- [x] 2.2 Implementar `rules/final_analysis.py` (`PREFIJOS = ["CNC", "REC", "TRF"]`: avances incluidos, objetivos contra el capítulo 1, cifras contra `boards.calcular` sobre los `data.json` de los informes, validación con usuarios, limitaciones, conclusiones con evidencia y cobertura de objetivos) y `tests/test_final_analysis.py` con los ejemplos de las plantillas, los informes de sprint de las plantillas de `common/sprint-reports/` y un análisis parcial

## 3. Skills

- [x] 3.1 Crear `.claude/skills/17-make-lean-results/SKILL.md` (fuentes obligatorias, reglas, flujo con confirmación, escritura, validación y registro)
- [x] 3.2 Crear `.claude/skills/17-make-lean-results-update/SKILL.md` y `references/dependencias.md`
- [x] 3.3 Crear `.claude/skills/18-make-final-analysis/SKILL.md`
- [x] 3.4 Crear `.claude/skills/18-make-final-analysis-update/SKILL.md` y `references/dependencias.md`

## 4. Verificación

- [x] 4.1 Ejecutar `openspec validate add-final-analysis --strict`, `openspec validate --specs --strict`, las pruebas del kit y la comprobación de que las skills `17-…` y `18-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa
