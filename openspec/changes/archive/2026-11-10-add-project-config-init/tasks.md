# Tasks

## 1. Kit compartido

- [x] 1.1 Crear `.claude/skills/_shared/pipeline.json` (20 skills con orden, verbo, carpeta y prerrequisitos) y `policy.json` (términos prohibidos y excepciones); verificar con un script que ambos son JSON válido, que los nombres siguen el esquema `[dos dígitos]-[verbo]-[nombre]`, que no hay números ni carpetas repetidos y que el orden coincide con el de la spec `skill-pipeline`
- [x] 1.2 Implementar `projectcfg.py` (leer y validar el config, `register` con la regla de `fijada`, `check` de prerrequisitos solo para skills existentes) con pruebas en `_shared/tests/`; verificar con `python3 -m unittest` que pasan los casos: `schema` desconocido rechazado, `modo_datos` inválido rechazado, corrida nueva mueve el puntero, corrida nueva con `fijada` no lo mueve, carpeta inexistente avisada
- [x] 1.3 Implementar `runs.py` (`new`, `fork`, corrida vigente) con pruebas; verificar que `new` crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/`, que `fork` crea `<fecha-hora>-fork` idéntica a la base salvo su `README.md` (comparación con `diff -r`) y que la base no cambia
- [x] 1.4 Implementar `validate_run.py` con las reglas genéricas y las del Design Thinking; verificar que pasa sin incidencias sobre `project/design-thinking/10-11-2026-00-00-46` y que reporta archivo y causa en una copia temporal con un enlace roto, un código citado sin definir y un término prohibido

## 2. Skill 00-init y config del proyecto

- [x] 2.1 Crear `.claude/skills/00-init/SKILL.md` con las preguntas (tema, empresa, rubro, enfoque, resultado esperado, equipo, fechas de los avances), el resumen con confirmación y el modo de edición cuando el config ya existe; verificar que la skill aparece en la lista de skills con el nombre `00-init`
- [x] 2.2 Ejecutar `00-init` con el usuario para crear `project/config.json`, proponiendo los datos desde el `ENF-01` de la corrida existente y registrando esa corrida en el paso `05-make-design-thinking`; verificar con `projectcfg.py` que el config valida, tiene tres avances y que el historial del paso 05 incluye `10-11-2026-00-00-46`

## 3. Renombre y adaptación de las skills de Design Thinking

- [x] 3.1 Renombrar con `git mv` a `05-make-design-thinking` y `06-make-design-thinking-prototypes` y actualizar `name:`, README, scripts, la plantilla `dt-4b-inventario-pantallas.md` y las menciones cruzadas; verificar con `grep` que los nombres antiguos solo quedan en lo archivado, en el cambio `reorder-report-index` y en los textos «Purpose» de las specs principales
- [x] 3.2 Hacer que `05-make-design-thinking` lea el config (deja de preguntar tema y enfoque, indica `00-init` si falta), use `runs.py new` en lugar de `new_run.sh`, registre su corrida al terminar y compruebe prerrequisitos; verificar generando el paquete por defecto en una carpeta temporal con un config de prueba y comprobando con `diff -r` que es idéntico al paquete existente y que el paso quedó registrado
- [x] 3.3 Hacer que `06-make-design-thinking-prototypes` tome la corrida del config (la muestra para confirmar y solo lista si se rechaza) y registre su paso con el enlace del tablero en `salidas`; verificar ejecutando `read_run.py`, `plan_run.py` y `patch_run.py --dry-run` sobre la corrida vigente del config y comprobando el registro en una copia temporal del config

## 4. Patrón de update

- [x] 4.1 Crear `.claude/skills/05-make-design-thinking-update/SKILL.md` con el flujo (config, base, prerrequisitos, cambios del usuario, plan con confirmación, fork, edición de lo afectado, validador, registro) y `references/dependencias.md` con la tabla de qué archivos dependen de qué códigos; verificar que la skill aparece en la lista y que cada requisito de `run-versioning` tiene una instrucción

## 5. Documentación y verificación final

- [x] 5.1 Escribir `.claude/skills/_shared/README.md` con la guía para crear una skill nueva y su `update` (preguntar y confirmar, playbook con modelos, carpeta de corrida, registro en el config, prerrequisitos, texto limpio); verificar que cubre cada requisito de `skill-pipeline`
- [x] 5.2 Ejecutar la verificación global: `openspec validate add-project-config-init --strict`, listado ordenado de `.claude/skills/`, validación del config, `grep` de los nombres antiguos y comparación del generador por defecto con el paquete; verificar que todo pasa

## Workflow follow-up

- Diferida (se hará cuando el usuario pida ejecutar la skill): probar el patrón `-update` sobre una copia temporal de la corrida existente (quitar una idea, corregir una cita, correr el validador y comprobar que se detecta la omisión de un archivo dependiente).
- Archivar el cambio y corregir directamente los textos «Purpose» de las specs `design-thinking-package-generation` y `design-thinking-prototype-mockups`, que nombran las skills antiguas.
- Continuar con el cambio 2 de la hoja de ruta (sistema de diseño).
