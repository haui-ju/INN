# Design

## Context

Las skills del repo siguen un patrón: skill numerada en `.claude/skills/`, playbook en `common/<tema>/guia.md` con `models/`, lógica en `_shared/*.py` con reglas en `_shared/rules/`, corridas en `project/<carpeta>/<fecha>/` registradas en `project/config.yaml`, y una skill `-update` que bifurca (`skill-pipeline`, `run-versioning`, `project-config`). Esta skill se aparta de un punto: su resultado principal son repositorios vivos en `project/app/`, no archivos de una corrida. Los changes `add-app-definition-skills` (TRD) y `add-app-implementation-plan` (un `plan.json` por componente en `project/app/implementation-plan/<corrida>/<componente>/`) ya están implementados; esta skill lee sus corridas vigentes. Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- Repos listos para implementar, repetibles y seguros (sin secretos, sin remotos).
- Una sola fuente de verdad del stack (el TRD) y una sola tabla stack → comando (el playbook).
- Ejecutar comandos externos solo con confirmación, con modo de simulación.

**Non-Goals:**
- No implementa funcionalidades de la app ni escribe código de negocio.
- No crea repositorios remotos, no publica ni configura despliegues reales (ni AWS ni Vercel).
- No instala herramientas del sistema (`pnpm`, `uv`, `docker`): comprueba que existan y avisa.

## Decisions

**1. Los repos viven en `project/app/<componente>/`; la corrida guarda solo un manifiesto.** El `-update` no puede "bifurcar" un repo con historia git sin copiar gigas de dependencias. La corrida `project/app-scaffold/<fecha>/` registra qué comandos corrieron, con qué stack y qué archivos nacieron. *Alternativa descartada:* copiar los repos dentro de la corrida; duplica `node_modules` y rompe `git`.

**2. Planificar, confirmar, ejecutar en tres fases dentro de `app_scaffold.py`.** `plan()` produce una lista de pasos (comando, directorio, ¿usa red?, archivos que crea) sin tocar el disco; `--dry-run` la imprime; `run()` la ejecuta solo tras la confirmación. Así la prueba verifica el plan sin ejecutar comandos externos. *Alternativa descartada:* ejecutar mientras se decide; no se puede probar ni revertir.

**3. Tabla stack → comando en el playbook, no en el código.** `common/app-scaffold/guia.md` contiene la tabla (Next.js con `pnpm create next-app@latest <name> --yes`, Python con `uv init`, Postgres con `docker compose`, OpenRPA con su estructura de proyecto) y el script la parsea. Un stack ausente obliga a preguntar. Mantiene el conocimiento revisable por el usuario sin tocar Python.

**4. Plantillas para lo que no genera el framework.** `models/` guarda `.gitignore` por stack, `.env.example`, README en español con marcadores y archivos de Docker/linter. Las variables se derivan del TRD (servicios usados) y cada una declara su descripción para el README, de modo que README y `.env.example` no se desincronicen.

**5. Seguridad por construcción.** Los valores de `.env` son marcadores (`replace-with-...`); la validación rechaza valores con formato de clave real (`sk-`, `AKIA...`, tokens de Telegram con su patrón); `.env` se escribe después de `.gitignore`, y la skill nunca ejecuta `git add -A`: solo agrega archivos de plantilla nombrados. No se hace commit inicial salvo que el usuario lo pida.

**6. OpenSpec por repo, solo con los changes del plan.** `openspec init` en cada repo (con confirmación, usa herramienta externa) y un stub por change del `plan.json` de ese componente (en la corrida vigente del plan de implementación), usando `openspec new change`. El tope de changes por repo lo impone el plan, no esta skill.

**7. Idempotencia por archivo.** Antes de escribir, la skill compara con lo existente; para cada diferencia ofrece omitir, conservar o reemplazar. Una segunda ejecución sin cambios del TRD no produce diferencias. El `-update` añade un componente o regenera archivos concretos.

**8. Numeración.** `24-make-app-scaffold` va después de las skills de definición y de plan, que ocupan 21 a 23 (confirmado).

## Risks / Trade-offs

- [Generadores interactivos o que cambian sus flags (`create-next-app`)] → La tabla fija los flags no interactivos y la prueba manual inicial valida cada fila antes de darla por buena.
- [Herramienta ausente (`pnpm`, `uv`, `docker`)] → El plan comprueba su presencia y detiene ese componente con un aviso, sin dejar carpetas a medias.
- [Un fallo a mitad de camino deja un repo parcial] → El manifiesto marca cada paso como hecho; el `-update` retoma desde el primer paso incompleto.
- [Dependencia de nombres de archivo de los changes hermanos] → La lectura del TRD y de los planes está aislada en una función.
- [El detector de "valor que parece real" da falsos positivos] → Solo revisa `.env*` y se limita a prefijos conocidos; el aviso permite continuar tras confirmar.

## Open Questions

- Ninguna: los nombres de archivo del TRD y de los planes quedaron fijados por las skills 22 y 23.
