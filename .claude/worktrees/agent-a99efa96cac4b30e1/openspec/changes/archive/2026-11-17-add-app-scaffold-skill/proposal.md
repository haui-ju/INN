# Proposal

## Why

Las skills de definición de la app (PRD, TRD, APP-FLOW, esquema, plan de implementación) dejan decidido qué se construye y con qué stack, pero nadie crea los repositorios. Hoy el equipo tendría que armar a mano cada carpeta (generador del framework, `git`, `.gitignore`, `.env`, README, OpenSpec), con riesgo de commitear secretos o de que cada repo quede distinto. Una skill de cascarón convierte el TRD y el plan en repos listos para empezar a implementar, de forma repetible y sin tocar nada publicado.

## What Changes

- Nueva skill numerada `24-make-app-scaffold` (con `-update`) que lee el TRD y el plan de implementación vigentes y crea, bajo `project/app/`, una carpeta por cada componente que aplique: `frontend`, `backend`, `database` y `openrpa`.
- Para cada componente ejecuta el generador oficial del stack elegido en el TRD, tomado de una tabla stack → comando que vive en un playbook (`common/app-scaffold/guia.md`), por ejemplo `pnpm create next-app@latest <name> --yes` para Next.js. Antes de correr cualquier comando que use la red, muestra la lista exacta y pide confirmación; un modo `--dry-run` solo imprime los comandos.
- En cada repo: `git init` local (nunca crea ni sube un repositorio remoto), `.gitignore` que excluye `.env`, secretos, dependencias y salidas de build, `.env` con valores de ejemplo y `.env.example`, archivos de linter, formateador y Docker según el TRD, y un `README.md` en español con la arquitectura del repo, cómo ejecutarlo y la tabla de variables de entorno con qué poner en cada una (`OPENAI_API_KEY`, `TELEGRAM_BOT_TOKEN`, claves de AWS, `DATABASE_URL`).
- Inicializa un `openspec/` propio en cada repo y crea los stubs de changes a partir del `plan.json` de ese componente en el plan de implementación vigente (hay un `plan.json` por componente; el tope de changes por repo lo fija ese plan).
- Es idempotente: no sobrescribe archivos existentes sin preguntar, no escribe secretos reales y nunca hace `git add` ni commit de `.env`.
- Guarda una corrida versionada (`project/app-scaffold/<corrida>/`) con el manifiesto de lo creado y los comandos ejecutados, la registra en el config y la valida como las demás skills. Los repos generados viven en `project/app/` y no se copian en el fork.
- Todo identificador, nombre de archivo y comentario de código va en inglés; el README de cada repo y los mensajes al usuario, en español.

## Capabilities

### New Capabilities

- `app-scaffold`: creación y validación del cascarón inicial de los repos de la app (generadores por stack, git local, `.gitignore`, `.env`, README, OpenSpec por repo), con confirmación previa a los comandos de red, modo de simulación e idempotencia.

### Modified Capabilities

- `skill-pipeline`: se agrega un requisito para declarar `24-make-app-scaffold` (y su `-update`) en `pipeline.json` con prerrequisitos en el TRD y el plan de implementación. No se modifica el requisito vigente de los veintidós pasos para no chocar con los changes hermanos; el recuento total se reconcilia al archivar.

## Impact

- Código nuevo en `.claude/skills/_shared/`: `app_scaffold.py` (planificación, simulación, ejecución y manifiesto), `rules/app_scaffold.py` (validaciones) y pruebas en `tests/`; entrada en `pipeline.json`.
- Playbook `common/app-scaffold/guia.md` con `models/` (plantillas de `.gitignore`, `.env.example`, README en español y archivos de Docker/linter por stack).
- Skills `.claude/skills/24-make-app-scaffold/` y `24-make-app-scaffold-update/`.
- Depende de los changes `add-app-definition-skills` (TRD, corrida vigente de la skill 22) y `add-app-implementation-plan` (un `plan.json` por componente, corrida vigente de la skill 23); ambos ya están implementados y sus nombres de archivo y el esquema de `plan.json` (`_shared/plan_schema.py`) son los reales.
- Ejecuta herramientas externas (`pnpm`, `uv`, `git`, `docker`, `openspec`) solo con confirmación; no agrega dependencias al repo de skills.
