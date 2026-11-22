# Tasks

## 1. Pipeline y estructura base

- [x] 1.1 Añadir a `pipeline.json` las entradas `21-make-app-definition` y `22-make-app-technical-definition` (carpeta `app/definition`, `update: true`, prerrequisitos según la spec) con `orden` consecutivo; verificar con `projectcfg.py check` y la prueba de `pipeline.json` que el orden es consecutivo y resuelve la carpeta anidada.
- [x] 1.2 Comprobar con una prueba que `runs.py new` y `projectcfg.py register` crean y registran una corrida en `project/app/definition/` para ambos pasos sin cambios en el kit.

## 2. Skill 21: definición del producto

- [x] 2.1 Crear `common/app-definition/guia.md` y `models/` (`prd.md`, `app-flow.md`, `design-brief.md`, `README.md`) con reglas, formularios, cantidades de referencia y checklist; verificar leyendo que cada plantilla tiene sus secciones y que la guía cita la regla de componentes y de idioma.
- [x] 2.2 Escribir `.claude/skills/21-make-app-definition/SKILL.md` (fuentes, propuesta de componentes con confirmación, escritura y registro) y su `-update`; verificar con una revisión que el brief y `override.md` están en las fuentes y que el flujo no escribe sin confirmación.
- [x] 2.3 Implementar `_shared/rules/app_definition.py` (estructura, componentes confirmados, citas `HU`/`RF`/`UI`/`ADR`, trazabilidad del PRD y del APP-FLOW, texto limpio); verificar con pruebas en `_shared/tests/` que pasa una corrida válida y falla en `HU-99`, en una historia sin flujo y en un brief sin interfaz.

## 3. Skill 22: entrevista y definición técnica

- [x] 3.1 Crear `common/app-technical-definition/guia.md` con el catálogo de preguntas por componente (opciones, ventajas, desventajas y recomendación) y los modelos de TRD común, TRD por componente y esquema de datos; verificar que el catálogo cubre todas las preguntas de la spec y que cada pregunta tiene al menos dos opciones.
- [x] 3.2 Escribir `.claude/skills/22-make-app-technical-definition/SKILL.md` con la tabla de decisiones (`decided`/`open`), la entrevista solo de lo abierto, la detección de conflictos con `ADR` y la confirmación previa, y su `-update`; verificar con una revisión que no repregunta lo fijado en `override.md` y no pide credenciales.
- [x] 3.3 Implementar `_shared/rules/app_technical_definition.py` (TRD por componente, decisiones abiertas, citas `ADR`/`RNF`/`TBL`, cobertura del esquema, búsqueda de secretos, texto limpio y comparación con la corrida vigente de 21); verificar con pruebas que fallan una `TBL` ausente, una decisión `open`, una cadena con forma de clave y un componente sin TRD.

## 4. Integración y cierre

- [x] 4.1 Ejecutar `validate_run.py` sobre una corrida generada para este proyecto (backend, database, openrpa, sin frontend) preparada como fixture; verificar que no hay incidencias y que no existe `frontend/` ni `design-brief.md`.
- [x] 4.2 Probar los dos `-update` sobre una copia de la corrida: cambiar el flujo de `/vendedor` y el ORM; verificar que el fork solo modifica los archivos afectados y registra el historial.
- [x] 4.3 Actualizar `openspec/ROADMAP.md` y la lista de skills de la documentación del repositorio con los pasos 21 y 22; ejecutar la suite completa de `_shared/tests/` y `openspec validate add-app-definition-skills --type change` y verificar que terminan sin fallos.

## Workflow follow-up

- Los changes `add-app-implementation-plan` (plan de changes de OpenSpec por repositorio) y `add-app-scaffold-skill` (cascarón y variables de entorno) usan estas corridas como entrada y no forman parte de este change.
