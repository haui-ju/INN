# Design

## Context

El repositorio genera cada entregable con una skill numerada, un playbook en `common/<tema>/`, un módulo de reglas en `.claude/skills/_shared/rules/`, corridas versionadas en `project/<carpeta>/<fecha-hora>/` y una homóloga `-update` que bifurca la corrida (specs `skill-pipeline`, `run-versioning`, `project-config`). `runs.py` y `projectcfg.py` resuelven la carpeta de un paso desde `pipeline.json` (`carpeta`), por lo que un valor anidado como `app/definition` funciona sin cambiar el kit. La arquitectura del proyecto ya está fijada en `override.md` y en las `ADR-nn` de `project/system-design`. Ver proposal.md para la motivación.

## Goals / Non-Goals

**Goals:**
- Dos skills (21 y 22) que dejen la definición del producto y la técnica listas, trazables a RF, HU, ADR y TBL.
- La entrevista técnica solo pregunta lo que no está decidido y siempre con recomendación.
- Carpetas por componente creadas solo si el componente existe; documentos comunes sin duplicar.

**Non-Goals:**
- No se genera el plan de implementación ni código (changes `add-app-implementation-plan` y `add-app-scaffold-skill`).
- No se rediseña el sistema: un conflicto con una `ADR` se resuelve con `14-make-system-design-update`.
- No se guardan secretos ni valores de variables de entorno.
- No se cambia la numeración ni el contenido de skills existentes.

## Decisions

**1. Dos skills, no una.** `21-make-app-definition` produce lo que es producto (PRD, APP-FLOW, brief de diseño) y `22-make-app-technical-definition` lo técnico (TRD y esquema). La segunda necesita la primera porque el TRD cita funcionalidades y flujos, y la entrevista es larga y conviene poder repetirla sin rehacer el producto. *Alternativa descartada:* una sola skill con todos los documentos; mezcla preguntas de producto y técnicas y obliga a repetirlo todo ante un cambio de stack.

**2. Carpeta única `app/definition` con corridas de ambos pasos.** `pipeline.json` usa `carpeta: "app/definition"` para 21 y 22. La corrida de 22 es una copia de la vigente de 21 más los documentos técnicos, y se registra en su propio paso; cada `README.md` dice de qué paso proviene. Si se actualiza 21 después de 22, la validación de 22 compara los documentos de producto con los de la corrida vigente de 21 y avisa que debe volver a ejecutarse. *Alternativas descartadas:* dos carpetas (`app/definition` y `app/technical`), que parte la estructura `common/…` que el usuario quiere unificada; y subcarpetas de corrida por paso, que complican la lectura.

**3. Componentes confirmados, no deducidos en silencio.** La lista se infiere de los componentes del diseño del sistema y de `override.md`, y se confirma. Para este proyecto resulta `backend`, `database` y `openrpa`; el canal Telegram es un adaptador del backend, no un frontend. *Alternativa descartada:* tratar Telegram como frontend; obligaría a un brief de diseño y TRD de interfaz que no aplican.

**4. Documentos comunes en `common/`, específicos en el componente.** PRD, APP-FLOW, brief de diseño y el TRD común (despliegue, CI, entornos y catálogo de variables) van en `common/`; el TRD de cada componente y el esquema de datos van en su carpeta. El esquema de datos va en `database/` si existe ese componente y en `backend/` si no. *Alternativa descartada:* un TRD único; mezclaría decisiones de componentes que se despliegan y versionan por separado.

**5. Tabla de decisiones con estado como motor de la entrevista.** Antes de preguntar, la skill arma una tabla (`decided` u `open`, fuente, recomendación) con `override.md`, las `ADR`, los RNF y el PRD; solo las `open` se preguntan, en lotes por componente y con la recomendación como respuesta por omisión. Esto evita repreguntar lo ya fijado (Python, LangGraph, Docker, App Runner, PostgreSQL) y hace verificable que ninguna decisión queda abierta al escribir. Catálogo mínimo de preguntas en la guía, no en código, para que se amplíe sin cambiar la skill.

**6. Variables de entorno como contrato.** El TRD común y cada TRD lista nombre, propósito y quién provee el valor, nunca el valor. Es la entrada que usará el cascarón para crear `.env` y `README`. La validación busca cadenas con forma de clave. *Alternativa descartada:* guardar valores en el config; viola `project-config` (sin secretos).

**7. Idioma.** Archivos, carpetas, códigos (`FEAT-nn`) y contenido de los documentos en inglés; README y texto al usuario en español. La skill y su guía siguen en español como el resto de las skills del repo, y la regla de texto limpio se aplica a ambos idiomas ampliando la lista de términos prohibidos solo en el módulo de reglas nuevo.

**8. Reglas y pruebas dentro del patrón existente.** Un módulo por skill en `_shared/rules/` (`app_definition.py`, `app_technical_definition.py`) con `PREFIJOS` y `validar`, detectado por `validate_run.py`, y pruebas con fixtures en `_shared/tests/` como las de `user_stories`. No se añaden dependencias.

## Risks / Trade-offs

- [El esquema de datos duplica `modelo-datos.md` del diseño del sistema] → Se construye desde él (cada `TBL-nn` se cita) y agrega tipos, índices y flujos de vida; la validación exige cobertura completa y marca divergencias.
- [Las recomendaciones del agente pueden contradecir `ADR` existentes] → Se marca el conflicto y se resuelve con el usuario antes de escribir; si cambia la arquitectura se propone `14-make-system-design-update`.
- [Corridas de 22 desactualizadas respecto a 21] → La validación compara y avisa; el `-update` de 21 recuerda ejecutar 22 de nuevo.
- [La regla de texto limpio choca con ejemplos de variables de entorno] → Los documentos nombran las variables sin la palabra prohibida «placeholder» ni «datos de ejemplo»; la regla ya existe en `policy.json` y se prueba con el catálogo de variables.
- [Entrevista larga] → Solo se pregunta lo `open`, por lotes de componente y con respuesta corta «recomendado».
- [`override.md` es específico de este proyecto] → La skill lo trata como fuente opcional; sin él, la tabla de decisiones se arma solo con las `ADR` y los RNF.

## Migration Plan

Los cambios son aditivos: dos entradas nuevas en `pipeline.json`, módulos de reglas y carpetas nuevas. Ninguna corrida existente se modifica. Revertir es quitar las dos entradas y los archivos nuevos.

## Open Questions

- Ninguna que cambie las specs o las tareas. Los nombres definitivos de los modelos (`models/*.md`) se fijan al escribirlos.
