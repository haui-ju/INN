# Tasks

## 1. Playbook y plantillas

- [x] 1.1 Crear `common/app-scaffold/guia.md` con las reglas, la tabla stack → comando (Next.js, Python, PostgreSQL, OpenRPA) y la política de red; verificar que cada fila trae comando, indicador de red y archivos que crea.
- [x] 1.2 Crear `common/app-scaffold/models/` con las plantillas de `.gitignore` por stack, `.env.example`, README en español con marcadores, Dockerfile y configuración de linter y formateador; verificar con una prueba que cada plantilla se renderiza sin marcadores sin resolver.

## 2. Planificación y simulación

- [x] 2.1 Implementar en `_shared/app_scaffold.py` la lectura del TRD vigente y del `plan.json` de cada componente del plan vigente, y la lista de componentes que aplican; verificar con pruebas de proyecto sin frontend y de TRD ausente.
- [x] 2.2 Implementar `plan()` y `--dry-run`: pasos con comando, directorio, uso de red y archivos, sin tocar el disco; verificar con una prueba que el modo de simulación no crea ninguna carpeta y que el comando de Next.js sale como `pnpm create next-app@latest <name> --yes`.

## 3. Ejecución segura

- [x] 3.1 Implementar la ejecución con confirmación previa de los comandos de red, `git init` local sin remotos, `.gitignore` antes de `.env`, `.env` con valores de ejemplo y `.env.example`; verificar con pruebas en un directorio temporal que no hay remotos y que `.env` queda fuera del índice.
- [x] 3.2 Implementar el README en español con la tabla de variables derivada del TRD y la inicialización de `openspec/` con los stubs de cada `plan.json`; verificar con pruebas que cada variable de `.env.example` está en el README y que los changes creados coinciden con el plan.
- [x] 3.3 Implementar la idempotencia (omitir, conservar, reemplazar) y la reanudación desde el manifiesto; verificar con una prueba que una segunda ejecución sin cambios no modifica archivos.

## 4. Skill, pipeline y validación

- [x] 4.1 Escribir `rules/app_scaffold.py` (carpetas, git, `.gitignore`, `.env.example`, README, OpenSpec, valores que parecen reales) y registrarla en `validate_run.py`; verificar con pruebas de `.env` en el índice, README sin variable y valor con formato de clave real.
- [x] 4.2 Crear `.claude/skills/24-make-app-scaffold/SKILL.md` y `24-make-app-scaffold-update/SKILL.md`, agregarlas a `pipeline.json` con sus prerrequisitos y registrar la corrida en el config; verificar con `projectcfg.py check --skill 24-make-app-scaffold` y con la prueba de pipeline.
- [ ] 4.3 Ejecutar la suite de `_shared/tests/` y una corrida de simulación contra el TRD y el plan reales; verificar que termina sin fallos y que el manifiesto lista los comandos previstos.

## Workflow follow-up

- Número de la skill (24) y nombres de archivo del TRD y de los planes confirmados con las skills 22 y 23 ya implementadas.
