# Proposal

## Why

El proyecto ya tiene requerimientos, historias, diseño del sistema y una arquitectura fijada (`override.md`), pero no hay un paso que los convierta en la definición que un equipo necesita para programar: qué se construye exactamente, cómo navega el usuario, qué decisiones técnicas se tomaron y cómo se guardan los datos. Sin esa definición, la construcción se improvisa y el stack se redescubre en cada conversación. Hacerlo ahora permite que las skills siguientes (plan de implementación y cascarón de la app) partan de documentos claros y trazables.

## What Changes

- Se agregan dos skills de generación, cada una con su `-update`:
  - `21-make-app-definition` (con `21-make-app-definition-update`): detecta qué componentes tiene la app y genera los documentos de producto: **PRD**, **APP-FLOW** y, solo si hay interfaz propia, el **brief de diseño**.
  - `22-make-app-technical-definition` (con `22-make-app-technical-definition-update`): entrevista técnica y genera los **TRD** por componente y el documento de **esquema de datos** del backend o la base de datos.
- Las salidas van a `project/app/definition/<corrida>/` con subcarpetas `common/`, `backend/`, `database/`, `frontend/` y `openrpa/`, creando solo las de los componentes que existen. Lo común a varios componentes (PRD, APP-FLOW, brief de diseño y la sección común de despliegue y CI) vive en `common/` y no se duplica.
- El TRD parte con lo ya decidido (`override.md`, las decisiones `ADR-nn` y los RNF del diseño del sistema) y pregunta **solo lo que falta**, con una recomendación del agente para cada pregunta: empaquetado, lenguaje y framework, micro-frontends o servicio único o microservicios, Docker u otra herramienta, linter y formateador, destino de despliegue (AWS, Cloudflare, Vercel, contenedores o híbrido), motor de base de datos y dónde se aloja (contenedor con el backend, aparte o una instancia ya existente cuyo enlace da el usuario), caché, ORM, CI (GitHub Actions, Jenkins), herramientas de scraping, S3, EC2 y similares.
- Para un proyecto solo de Telegram, APP-FLOW describe el flujo conversacional y los comandos, y no se genera brief de diseño.
- Idioma: nombres de carpetas, archivos, códigos y contenido de los documentos en inglés; README y todo texto que ve el usuario en español.
- Se amplía el orden de skills en `pipeline.json` con los pasos 21 y 22 y sus prerrequisitos.
- Fuera de alcance (otros changes): el plan de implementación en changes de OpenSpec (`add-app-implementation-plan`) y el cascarón del código (`add-app-scaffold-skill`).

## Capabilities

### New Capabilities

- `app-definition-docs`: generación del PRD, APP-FLOW y brief de diseño en `project/app/definition/`, con detección de componentes, documentos comunes y trazabilidad a requerimientos, historias y diseño del sistema.
- `app-trd-interview`: entrevista técnica con recomendación del agente, TRD por componente, sección común de despliegue y CI, y documento de esquema de datos.

### Modified Capabilities

- `skill-pipeline`: el orden fijo de las skills crece con `21-make-app-definition` y `22-make-app-technical-definition`, cada una con su homóloga `-update`.

## Impact

- Nuevas skills en `.claude/skills/` (`21-*`, `22-*` y sus `-update`), playbooks `common/app-definition/` y `common/app-technical-definition/` con `guia.md` y `models/`.
- Código compartido: `pipeline.json`, módulos de reglas nuevos en `_shared/rules/` (por ejemplo `app_definition.py`, `app_technical_definition.py`) y pruebas en `_shared/tests/`; `projectcfg.py` y `runs.py` se usan sin cambios porque `carpeta` admite `app/definition`.
- Carpeta de trabajo nueva `project/app/` (el código de la app se creará después en `project/app/backend`, `project/app/frontend`, etc., fuera de esta definición).
- Las corridas de pasos anteriores no cambian; sin dependencias externas nuevas.
