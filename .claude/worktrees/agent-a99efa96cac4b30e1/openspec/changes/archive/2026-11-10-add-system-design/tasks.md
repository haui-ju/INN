# Tasks

## 1. Playbook, modelos, índice y prerrequisitos

- [x] 1.1 Verificar por búsqueda las fuentes (Nygard 2011 para el formato de decisiones de arquitectura; ISO/IEC 25010:2023 ya verificada) y escribir `common/system-design/guia.md` (arquitectura, modelo de datos, interfaz, plan de pruebas, diagramas como texto, errores, checklist y referencias); verificar que cubre cada requisito de la spec `system-design`, que usa «datos de entrada» en lugar de la expresión prohibida y que solo cita fuentes confirmadas
- [x] 1.2 Crear `common/system-design/models/sis-1-arquitectura.md`, `sis-2-modelo-datos.md`, `sis-3-interfaz.md`, `sis-4-plan-pruebas.md` y `README.md` con ficha, instrucciones, formato, ejemplo (incluidos los diagramas Mermaid) y checklist; verificar que los ejemplos son coherentes entre sí y con los RF, RNF, HU, CA y PAN de los ejemplos de `common/requirements/`, `common/user-stories/` y del paquete de Design Thinking de referencia, y que los enlaces resuelven
- [x] 1.3 Corregir en `common/structure/model1.md` las marcas de 5.4, 5.4.1 y 5.4.2 a `[A1+]` y añadir `10-make-user-stories` a los prerrequisitos de `14-make-system-design` en `pipeline.json`; verificar con `diff` que solo cambian esas cuatro líneas, que `pipeline.json` sigue siendo válido con 20 pasos y que `openspec validate --specs --strict` y las pruebas siguen pasando

## 2. Validación

- [x] 2.1 Registrar la carpeta `system-design` en `RULES` e implementar `rules/system_design.py` (arquitectura, modelo de datos, interfaz, plan de pruebas, diagramas, cobertura y existencia de códigos, citas) con pruebas que usen como fixture los ejemplos de las plantillas, una corrida de requerimientos, una de historias y un Design Thinking generado con `build.py`; verificar que pasa con un ejemplo completo y que informa archivo y causa con un RF sin componente, un RNF sin atender, una decisión sin alternativas, una tabla huérfana, una relación con tabla inexistente, un `PAN` sin destino, un `CA` sin caso, un caso sin origen, un componente ausente del diagrama y un `.mmd` que no es un diagrama

## 3. Skill 14-make-system-design

- [x] 3.1 Crear `.claude/skills/14-make-system-design/SKILL.md` (fuentes, preguntas de stack, alojamiento y restricciones con alternativas, propuesta, confirmación, escritura de los cuatro documentos y los diagramas, validación y registro); verificar que aparece en la lista y que cada requisito de la spec tiene una instrucción

## 4. Skill 14-make-system-design-update

- [x] 4.1 Crear `.claude/skills/14-make-system-design-update/SKILL.md` y `references/dependencias.md` (qué archivos y diagramas dependen de cada código y qué corridas posteriores los citan); verificar que sigue el patrón de `run-versioning` y que mantiene los diagramas coherentes con los documentos

## 5. Verificación final

- [x] 5.1 Ejecutar `openspec validate add-system-design --strict`, `openspec validate --specs --strict`, las pruebas del kit y la comprobación de que las skills `14-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa

## Workflow follow-up

- Archivar el cambio. La skill `14-make-system-design` y su `-update` se ejecutan solo cuando el usuario lo pida.
- Continuar con el cambio `add-sprint-execution-reports`.
